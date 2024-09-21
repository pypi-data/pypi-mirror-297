# Team UniMuenster 2024 Software Tool

## Description



## Installation

### Prerequisites

- Python 3.6 or higher

#### If you want to use the `search` tool

For performing the evotuning, CSV file with a list of evolutionary related amino acid sequences is required. To generate this file you can use the build in search tool, which make use of the jackhmmer tool. Please install jackhmmer under the following [link](http://hmmer.org/) before using the search tool.

Make sure that then `jackhmmer` is in your PATH. You can check this by running the following command in your terminal:

```bash
jackhmmer -h
```

To perform the search you need to have a protein database available in the FASTA format. You can download the [Uniprot](https://www.uniprot.org/help/downloads) database for this purpose. 

#### GPU training

The tool will automatically detect CUDA viable GPUs and use them.

### Pip

Optionally, you can create a virtual environment:

```bash
python3 -m venv venv
. ven/bin/activate
```



You can install the package via pip:

```bash
pip install seq-mutator
```

If done correctly, the `seq_mutator` executable should be available in your PATH.

```bash
seq_mutator --help
```

Optionally on linux you can install autocompletion capabillities for the tool:

```bash
seq_mutator --install-completion
```

After restarting your terminal you should be able to use the autocompletion for the tool.

### From source

You can also install the package from source. For this you need to clone the repository:

```bash
git clone https://gitlab.igem.org/2024/software-tools/unimuenster.git seq_mutator
```

Optionally, you can create a virtual environment:

```bash
python3 -m venv venv
. ven/bin/activate
```

Then you can install the requirements:

```bash
cd seq_mutator/
pip install -r requirements.txt
```

And finally your should be able to access the cli:

```bash
python3 src/app.py --help
```

## Usage

Before you start please create a working directory where you want to store input files, temporary files and output files. You can do this by running the following command on linux:

```bash
mkdir my_workspace
cd my_workspace/
```

To generally use the tool, open the terminal type the tools name `seq_mutator` followed by the subcommand you want to use (e.g. `seq_mutator command --option value`). You can always get help by using the `--help` flag:

```bash
seq_mutator --help
```

This will list further subcommands and options you can use.

### Low N Protein Engineering

```bash
.
└── data                                    # data directory
    ├── databases                           # databases directory
    │   └── sprot                           # database name
    │       ├── db.fasta                    # original database fasta file
    │       └── db.sqlite                   # database after building
    ├── models--facebook--esm2_t6_8M_UR50D/ # cached hugging face model
    └── projects                            # projects directory
        └── test                            # project name
            ├── hmmer.out                   # result of jackhmmer search
            ├── runs                        # runs directory containing evotuning runs
            │   ├── run1/                   # run name
            │   └── test_run                # run name
            │       ├── checkpoint-3/       # model checkpoint at step 3
            │       ├── checkpoint-11/      # model checkpoint at step 11
            │       └── logs/               # tensorboard logs
            ├── sequences.csv               # csv file with evolutionary related sequences
            ├── activities.csv              # csv file with measured activities
            ├── topmodel.pkl                # pkl file with topmodel state
            └── target.fasta                # target protein fasta file
```


#### Creating a project

For a better organization we make use of projects to store input and output files. Before you start you need to create a new project for your protein target:

```bash
seq_mutator low-n project create my_enzyme --target /path/to/your/enzyme_target.fasta
```

to see all available options run:

```bash
seq_mutator low-n project create --help
```

You can validate the project by running:

```bash
seq_mutator low-n project list # should show your project
```

to see all available options on how to manage your projects (create, list, delete, etc.) run:

```bash
seq_mutator low-n project --help
```

#### Creating and building a database

With the implemented search you can find evolutionary related sequences for your target protein. The search is performed on a protein database, so have to install one first. To make them reusable in your workspace across projects you can create a database:

```bash
seq_mutator low-n databases add db_name /path/to/your/protein_database.fasta
```

You can validate the database by running:

```bash
seq_mutator low-n databases list # should show your database
```

To make the database easily searchable, for the search it is required to `build` the database:

```bash
seq_mutator low-n databases build db_name
```

#### Searching for evolutionary related sequences

Before you continue make sure you have created a project and that you have a database available and built. You can search for evolutionary related sequences by running:

> This will perform a jackhmmer search on the database and store the results in the project directory. The search makes 5 iterations, uses 4 threads and only selects sequences with an E value <= 0.5.

```bash
seq_mutator low-n search db_name my_enzyme --num-iters 5 \
                                            --max-evalue 0.5 \
                                            --num-threads 4
```

#### Evotuning (fine-tuning) a Protein Language Model

Before you continue make sure that the `sequences.csv` is included in your project. If you want to use GPU for training make sure that you have a CUDA viable GPU available. The GPU will be automatically detected. The tool will try to use all the available GPUs.


```bash
seq_mutator low-n evotune --epochs 60 \                                 # training for 60 epochs
                            --project-name my_enzyme \                  # project name    
                            --batch-size 32 \                           # batch size    
                            --take 0.1 \                                # take 10% of the sequences
                            --eval epoch \                              # evaluate on the validation set after each epoch
                            --model "facebook/esm2_t6_8M_UR50D" \       # use the ESM2 model with 8M parameters
                            --tokenizer "facebook/esm2_t6_8M_UR50D" \   # use the ESM2 tokenizer
                            --run "test_run" \                          # run name under which logs and checkpoints will be stored
                            --max-length 1024 \                         # maximum sequence length
                            --lora                                      # use the LORA model
```

Generally a varaible batch size is activated. So if the batch size you picked is too high for your GPU memory the tool will automatically reduce the batch size. 

During training the tool will automatically save model checkpoints and logs in the project directory. You can monitor the training process by launching tensorboard:

```bash
tensorboard --logdir my_workspace/data/projects/my_enzyme/runs/test_run/logs
```

You can also continue training from a checkpoint by running:

```bash
seq_mutator low-n evotune --epochs 60 \                                 # training for 60 epochs
                            --project-name my_enzyme \                  # project name    
                            --batch-size 32 \                           # batch size    
                            --take 0.1 \                                # take 10% of the sequences
                            --eval epoch \                              # evaluate on the validation set after each epoch
                            --model "/path/to/checkpoint" \       # use the ESM2 model with 8M parameters
                            --tokenizer "facebook/esm2_t6_8M_UR50D" \   # use the ESM2 tokenizer
                            --run "test_run" \                          # run name under which logs and checkpoints will be stored
                            --max-length 1024 \                         # maximum sequence length
                            --lora                                      # use the LORA model
```

The number behind then checkpoint folders is the step number. You can find the step number in the tensorboard logs.

For further analysis of the log data we recommend the tool [tbparse](https://tbparse.readthedocs.io/en/latest/) for parsing the tensorboard logs into a `pandas` dataframe.

#### Topmodel

Before you train your topmodel make sure that the `activities.csv` is included in your project. You can train a topmodel by running:

```bash
seq_mutator low-n topmodel --project-name my_enzyme \                   # project name
                            --model "facebook/esm2_t6_8M_UR50D" \       # use the ESM2 model with 8M parameters
                            --tokenizer "facebook/esm2_t6_8M_UR50D"     # use the ESM2 tokenizer
```

If you want to use a fine-tuned model you can specify the checkpoint path:

```bash
seq_mutator low-n topmodel --project-name my_enzyme \                   # project name
                            --model "/path/to/your/checkpoint" \        # use the ESM2 model with 8M parameters
                            --tokenizer "facebook/esm2_t6_8M_UR50D"     # use the ESM2 tokenizer
```

You can then use the topmodel to predict the activity of an input sequence:

```bash
seq_mutator low-n topmodel predict "MAAAK" --project-name my_enzyme
```

The first argument is the sequence you want to predict the activity for. It can be a single sequence or a path to a FASTA or CSV file containing amino acid sequences.


### Restriction Enzyme-Mediated DNA Shuffling

The codon optimization with restriction site insertion is performed in two steps. In the first step possible restriction sites in the overlapping regions are identified and stored as CSV file. The user can the manually check the restriction sites.

In the second step the codon optimization is performed using the updated CSV file with the restriction sites.

The tool outputs the optimized DNA sequences as stdout. You can redirect the output to a file by using the `>` operator.

#### Finding restriction sites

This command requires 3 arguments: 

- `--alignment`: the path to the alignment file in FASTA format containing proteins with at least ~65% sequence identity
- `--codon-table`: the path to the codon table file in CSV format. This codon table is unique for the organism you are working with.
- `--restriction-enzymes`: the path to the restriction enzymes file in CSV format. This file contains the restriction enzymes the tool should try to include into the sequence.

You can run the command as follows:

```bash
seq_mutator shuffle find-hits --alignment /path/to/alignment.fasta \
                                --codon-table /path/to/codon_table.csv \
                                --restriction-enzymes /path/to/restriction_enzymes.csv
```

This command will output a `hits.csv` CSV file containing the restriction sites found in the alignment.

Please review them and save the file.

#### Codon optimization

In the next step the codon optimization can be performed given the `hits.csv` file: 

```bash
seq_mutator shuffle optimize --alignment /path/to/alignment.fasta \
                                --codon-table /path/to/codon_table.csv \
                                --restriction-enzymes /path/to/restriction_enzymes.csv \
                                --hits /path/to/hits.csv
```

The tool will output the optimized DNA sequences as stdout. You can redirect the output to a file by using the `>` operator.

Before ordering the sequence you should further validate the sequences by checking the restriction sites. You should also use tools like XXX to validate if the sequence can be synthesized.

## Contributing

## Authors and acknowledgment

A big thanks to the whole iGEM Team Münster 2024 for investing into the development of this tool. 

Special thanks to:

- Emil Breuer (Author)
- Jan Albrecht (Author)
- Michel Westermann (Co Author)
- Lasse (Advisor)


