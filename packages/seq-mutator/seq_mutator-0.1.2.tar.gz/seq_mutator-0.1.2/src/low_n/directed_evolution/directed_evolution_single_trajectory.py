import torch

from esm import pretrained
import pandas as pd
import numpy as np
from scipy.spatial import distance


amino_acids = {'A': 2,'C': 10,'D': 15,'E': 16,'F': 7,'G': 1,'H': 19,'I': 5,'K':17,'L': 4,'M': 6,'N': 13,'P': 0,'Q': 14,'R': 18,'S': 11,'T': 12,'V': 3,'W': 9,'Y': 8}

wt_sequence = ''
with open('./input_files/PAS_WT.txt', 'r') as file:
    for line in file: #TODO: Use Biopython for this
        wt_sequence += line.strip()
seq_length = len(wt_sequence)

protein_model, alphabet = pretrained.load_model_and_alphabet("esm2_t6_8M_UR50D")
protein_model.eval()
batch_converter = alphabet.get_batch_converter()

top_model = np.loadtxt('./input_files/low_n_weights_test.csv')

n_iterations = 20 # 3000
temperature = 0.01
trust_radius = 15

n_initial_mutations = np.random.poisson(2)+1


def IntroduceMutations(sequence, num_mutations):
    rng = np.random.default_rng()
    positions = rng.choice(range(1,len(sequence)-1), num_mutations)
    for i in positions:
        amino_set = list(amino_acids.keys())
        amino_set.remove(sequence[i])
        sequence = sequence[:i] + rng.choice(amino_set) + sequence[i+1:]
    return sequence

def ScoreProtein(sequence, top_model): #only for testing, obsolete once Jan's methods are used
    _,_,batch_tokens = batch_converter([("protein1",sequence)])
    with torch.no_grad():
        sequence_representation = protein_model(batch_tokens, repr_layers=[6])["representations"][6][0, 1:seq_length+1].mean(0).numpy() #first token is beginning-of-sequence token, similarly last token just signals end-of-sequence, so their omitted
    return np.inner(sequence_representation, top_model)


current_proposal = IntroduceMutations(wt_sequence, n_initial_mutations)
current_score = ScoreProtein(current_proposal, top_model)

results = [[current_proposal,current_score,"yes"]]
rng = np.random.default_rng()
for i in range(0,n_iterations):
    new_candidate = IntroduceMutations(current_proposal, rng.poisson(rng.random()*1.5)+1) # Draw from pois(mu) with mu drawn uniformly from [1,2.5]
    new_score = ScoreProtein(new_candidate, top_model)
    acceptance_prob = min(1,np.exp((new_score-current_score)/temperature))
    if distance.hamming(list(new_candidate),list(wt_sequence))*seq_length>=trust_radius:
        results.append([new_candidate,new_score,"trust radius"])
    elif rng.random()>acceptance_prob:
        results.append([new_candidate,new_score,"score"])
    else:
        results.append([new_candidate,new_score,"yes"])
        current_proposal = new_candidate
        current_score = new_score

pd.DataFrame(results,columns=["sequence","score","accepted?"]).to_csv("./directed_evolution/de_test.csv")