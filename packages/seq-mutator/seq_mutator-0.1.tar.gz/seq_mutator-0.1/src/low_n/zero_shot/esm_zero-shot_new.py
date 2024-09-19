import argparse
import pathlib

import torch

from transformers import AutoTokenizer, EsmForMaskedLM
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
    parser.add_argument("--nogpu", action="store_true", help="Do not use GPU even if available")
    return parser


def label_row(row, sequence, token_probs, tokenizer, offset_idx, mutation_positions=None):
    wt, idx, mt = row[0], int(row[1:-1]) - offset_idx, row[-1]
    assert sequence[idx] == wt, "The listed wildtype does not match the provided sequence"

    wt_encoded, mt_encoded = tokenizer.convert_tokens_to_ids(wt), tokenizer.convert_tokens_to_ids(mt)

    if mutation_positions is not None:
        position = mutation_positions.index(int(row[1:-1]))
        score = token_probs[0, position, mt_encoded] - token_probs[0, position, wt_encoded]
    else:
        score = token_probs[0, 1 + idx, mt_encoded] - token_probs[0, 1 + idx, wt_encoded]
    return score.item()


def main(args):
    # Load the deep mutational scan
    df = pd.read_csv(args.dms_input)
    mutation_positions = list(df.apply(lambda row: int(row["mutation"][1:-1]),1).unique())
    esm_cache_directory = "/scratch/tmp/ebeurer/cache/huggingface/hub"
    sequence = ''
    with open(args.sequence, 'r') as file:
        for line in file: #TODO: Use Biopython for this
            sequence += line.strip()

    # inference for each model
    for model_location in args.model_location:
        tokenizer = AutoTokenizer.from_pretrained(model_location)
        model = EsmForMaskedLM.from_pretrained(model_location, cache_dir=esm_cache_directory)
        model.eval()
        model = model.cuda()

        

        data = [sequence]
        batch_tokens = tokenizer(data, return_tensors="pt", padding=False)

        all_token_probs = []
        for i in tqdm(mutation_positions):
            batch_tokens_masked = batch_tokens.input_ids.clone()
            batch_tokens_masked[0, i] = tokenizer.mask_token_id
            with torch.no_grad():
                logits = model(batch_tokens_masked.cuda()).logits
                token_probs = torch.log_softmax(logits, -1)
            all_token_probs.append(token_probs[:, i])  # vocab size
        token_probs = torch.cat(all_token_probs, dim=0).unsqueeze(0)
        print(token_probs)
        df[model_location] = df.apply(
            lambda row: label_row(
                row[args.mutation_col],
                sequence,
                token_probs,
                tokenizer,
                args.offset_idx,
                mutation_positions
            ),
            axis=1,
        )

    df.to_csv(args.dms_output)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
