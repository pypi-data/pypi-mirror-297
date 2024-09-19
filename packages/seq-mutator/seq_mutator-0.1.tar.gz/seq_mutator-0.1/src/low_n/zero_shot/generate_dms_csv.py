import argparse
import pathlib
import pandas as pd


def create_parser():
    parser = argparse.ArgumentParser(
        description="Create a csv file with single mutations at every position with every possible amino acid substitution"
    )
    parser.add_argument(
        "--sequence-file",
        type=pathlib.Path,
        help="File containing the protein sequence to be mutated",
    )
    parser.add_argument(
        "--output-file",
        type=pathlib.Path,
        help="Where to store the resulting csv"
    )
    return parser

def main(args):
    output = pd.DataFrame(columns=['mutation'])
    sequence = ''
    with open(args.sequence_file, 'r') as file:
        for line in file: #TODO: Use Biopython for this
            sequence += line.strip()
    
    amino_acids = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    for i in range(1,len(sequence)):
        wt = sequence[i]
        for char in amino_acids:
            if char==wt:
                continue
            output.loc[len(output.index)]=wt+str(i+1)+char
    
    output.to_csv(args.output_file)

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)