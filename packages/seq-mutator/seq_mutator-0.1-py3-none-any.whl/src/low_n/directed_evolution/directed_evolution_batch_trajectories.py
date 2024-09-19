import torch

from transformers import AutoTokenizer, EsmForMaskedLM

import copy
import pandas as pd
import numpy as np

import cyclopts


app = cyclopts.App()

def IntroduceMutations(sequence, wt_sequence, mutated_positions, num_mutations, trust_radius, amino_acids):
    rng = np.random.default_rng()
    num_mutations = min(num_mutations, trust_radius)
    if trust_radius>=len(mutated_positions)+num_mutations:
        positions = rng.choice(range(1,len(sequence)), num_mutations, replace=False)
        mutated_positions.update(positions)
    elif trust_radius==len(mutated_positions):
        positions = rng.choice(list(mutated_positions), num_mutations, replace=False)
    else:
        n_new_positions = trust_radius-len(mutated_positions)
        positions = rng.choice(range(1,len(sequence)), n_new_positions, replace=False)
        mutated_positions.update(positions)
        np.append(positions, rng.choice(list(mutated_positions), num_mutations-n_new_positions, replace=False))

    for i in set(positions):
        amino_set = list(amino_acids.keys())
        amino_set.remove(sequence[i])
        substitution = rng.choice(amino_set)
        sequence = sequence[:i] + substitution + sequence[i+1:]
        if substitution==wt_sequence[i]:
            mutated_positions.remove(i)
    return sequence

def ScoreProtein(sequence, top_model): #only for testing, obsolete once Jan's methods are used
    batch_tokens = tokenizer(sequence, return_tensors="pt", padding=False).input_ids
    with torch.no_grad():
        sequence_representation = protein_model(batch_tokens, output_hidden_states=True).hidden_states[-1].mean(1).numpy()[:,:]
    return np.dot(sequence_representation, top_model)


@app.default
def main(wildtype_sequence: str='./input_files/PAS_WT.txt', n_iterations: int=20, batch_size: int=1, trust_radius: int=7, temperature: float=0.1):
    amino_acids = {'A': 2,'C': 10,'D': 15,'E': 16,'F': 7,'G': 1,'H': 19,'I': 5,'K':17,'L': 4,'M': 6,'N': 13,'P': 0,'Q': 14,'R': 18,'S': 11,'T': 12,'V': 3,'W': 9,'Y': 8}

    wt_sequence = ''
    with open(wildtype_sequence, 'r') as file:
        for line in file: #TODO: Use Biopython for this
            wt_sequence += line.strip()
    seq_length = len(wt_sequence)

    esm_model_version = "facebook/esm2_t6_8M_UR50D"
    tokenizer = AutoTokenizer.from_pretrained(esm_model_version)
    protein_model = EsmForMaskedLM.from_pretrained(esm_model_version)

    top_model = np.loadtxt('./input_files/low_n_weights_test.csv')

    n_initial_mutations = np.random.poisson(2)+1

    current_proposal = []
    mutated_positions = []
    for i in range(batch_size):
        mutated_positions.append(set())
        current_proposal.append(IntroduceMutations(wt_sequence, wt_sequence, mutated_positions[i], n_initial_mutations, trust_radius))
    current_score = ScoreProtein(current_proposal, top_model)

    results = []
    for i in range(batch_size):
        results.append([[current_proposal[i],current_score[i],"yes"]])
    rng = np.random.default_rng()
    for i in range(0,n_iterations):
        new_candidate = []
        for j in range(0,batch_size):
            new_mutated_positions = copy.deepcopy(mutated_positions)
            new_candidate.append(IntroduceMutations(current_proposal[j], wt_sequence, new_mutated_positions[j], rng.poisson(rng.random()*1.5)+1, trust_radius)) # Draw from pois(mu) with mu drawn uniformly from [1,2.5]
        new_score = ScoreProtein(new_candidate, top_model)
        for j in range(0,batch_size):
            acceptance_prob = min(1,np.exp((new_score[j]-current_score[j])/temperature))
            if rng.random()>acceptance_prob:
                results[j].append([new_candidate[j],new_score[j],"score"])
            else:
                results[j].append([new_candidate[j],new_score[j],"yes"])
                current_proposal[j] = new_candidate[j]
                current_score[j] = new_score[j]
                mutated_positions[j] = new_mutated_positions[j]

    for i in range(batch_size):
        pd.DataFrame(results[i],columns=["sequence","score","accepted?"]).to_csv("./directed_evolution/de_test_"+str(i)+".csv")