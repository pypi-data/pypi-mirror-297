import argparse
import pathlib

import torch

from esm import pretrained
import pandas as pd
from tqdm import tqdm


def create_parser():
    parser = argparse.ArgumentParser(
        description="Label a deep mutational scan with predictions from an ensemble of ESM-1v models."
    )

    parser.add_argument(
        "--model-location",
        type=str,
        help="PyTorch model file OR name of pretrained model to download (see README for models)",
        nargs="+",
    )
    parser.add_argument(
        "--sequence",
        type=pathlib.Path,
        help="Base sequence to which mutations were applied",
    )
    parser.add_argument(
        "--dms-input",
        type=pathlib.Path,
        help="CSV file containing the deep mutational scan",
    )
    parser.add_argument(
        "--mutation-col",
        type=str,
        default="mutant",
        help="column in the deep mutational scan labeling the mutation as 'AiB'"
    )
    parser.add_argument(
        "--dms-output",
        type=pathlib.Path,
        help="Output file containing the deep mutational scan along with predictions",
    )
    parser.add_argument(
        "--offset-idx",
        type=int,
        default=0,
        help="Offset of the mutation positions in `--mutation-col`"
    )
    parser.add_argument(
        "--scoring-strategy",
        type=str,
        default="wt-marginals",
        choices=["wt-marginals", "pseudo-ppl", "masked-marginals"],
        help=""
    )
    parser.add_argument("--nogpu", action="store_true", help="Do not use GPU even if available")
    return parser


def label_row(row, sequence, token_probs, alphabet, offset_idx, mutation_positions=None):
    wt, idx, mt = row[0], int(row[1:-1]) - offset_idx, row[-1]
    assert sequence[idx] == wt, "The listed wildtype does not match the provided sequence"

    wt_encoded, mt_encoded = alphabet.get_idx(wt), alphabet.get_idx(mt)

    if mutation_positions is not None:
        position = mutation_positions.index(int(row[1:-1]))
        score = token_probs[0, position, mt_encoded] - token_probs[0, position, wt_encoded]
    else:
        score = token_probs[0, 1 + idx, mt_encoded] - token_probs[0, 1 + idx, wt_encoded]
    return score.item()


def compute_pppl(row, sequence, model, alphabet, offset_idx, nogpu=False):
    wt, idx, mt = row[0], int(row[1:-1]) - offset_idx, row[-1]
    assert sequence[idx] == wt, "The listed wildtype does not match the provided sequence"

    # modify the sequence
    sequence = sequence[:idx] + mt + sequence[(idx + 1) :]

    # encode the sequence
    data = [
        ("protein1", sequence),
    ]

    batch_converter = alphabet.get_batch_converter()

    batch_labels, batch_strs, batch_tokens = batch_converter(data)

    wt_encoded, mt_encoded = alphabet.get_idx(wt), alphabet.get_idx(mt)

    # compute probabilities at each position
    log_probs = []
    for i in range(1, len(sequence) - 1):
        batch_tokens_masked = batch_tokens.clone()
        batch_tokens_masked[0, i] = alphabet.mask_idx
        with torch.no_grad():
            if torch.cuda.is_available() and not nogpu:
                batch_tokens_masked = batch_tokens_masked.cuda()
            token_probs = torch.log_softmax(model(batch_tokens_masked)["logits"], dim=-1)
        log_probs.append(token_probs[0, i, alphabet.get_idx(sequence[i])].item())  # vocab size
    return sum(log_probs)


def main(args):
    # Load the deep mutational scan
    df = pd.read_csv(args.dms_input)
    mutation_positions = list(df.apply(lambda row: int(row["mutation"][1:-1]),1).unique())
    sequence = ''
    with open(args.sequence, 'r') as file:
        for line in file: #TODO: Use Biopython for this
            sequence += line.strip()

    # inference for each model
    for model_location in args.model_location:
        model, alphabet = pretrained.load_model_and_alphabet(model_location)
        model.eval()
        if torch.cuda.is_available() and not args.nogpu:
            model = model.cuda()
            print("Transferred model to GPU")

        batch_converter = alphabet.get_batch_converter()

        data = [
            ("protein1", sequence),
        ]
        batch_labels, batch_strs, batch_tokens = batch_converter(data)

        if args.scoring_strategy == "wt-marginals":
            with torch.no_grad():
                if torch.cuda.is_available() and not args.nogpu:
                    batch_tokens = batch_tokens.cuda()
                token_probs = torch.log_softmax(model(batch_tokens)["logits"], dim=-1)
            df[model_location] = df.apply(
                lambda row: label_row(
                    row[args.mutation_col],
                    sequence,
                    token_probs,
                    alphabet,
                    args.offset_idx,
                ),
                axis=1,
            )
        elif args.scoring_strategy == "masked-marginals":
            all_token_probs = []
            for i in tqdm(mutation_positions):
                batch_tokens_masked = batch_tokens.clone()
                batch_tokens_masked[0, i] = alphabet.mask_idx
                with torch.no_grad():
                    if torch.cuda.is_available() and not args.nogpu:
                        batch_tokens_masked = batch_tokens_masked.cuda()
                    token_probs = torch.log_softmax(
                        model(batch_tokens_masked)["logits"], dim=-1
                    )
                all_token_probs.append(token_probs[:, i])  # vocab size
            token_probs = torch.cat(all_token_probs, dim=0).unsqueeze(0)
            df[model_location] = df.apply(
                lambda row: label_row(
                    row[args.mutation_col],
                    sequence,
                    token_probs,
                    alphabet,
                    args.offset_idx,
                    mutation_positions
                ),
                axis=1,
            )
        elif args.scoring_strategy == "pseudo-ppl":
            tqdm.pandas()
            df[model_location] = df.progress_apply(
                lambda row: compute_pppl(
                    row[args.mutation_col], sequence, model, alphabet, args.offset_idx, args.nogpu
                ),
                axis=1,
            )

    df.to_csv(args.dms_output)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
