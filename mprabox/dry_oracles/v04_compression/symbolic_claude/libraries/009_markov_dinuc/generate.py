"""1st-order Markov chain with mild dinucleotide bias.
Approximates natural DNA-like correlations. Tests if biological prior helps.

Transition matrix chosen to favor 'CG-avoid, AT-rich, mild correlations':
- Most rows ~uniform with slight self-preference
- Suppress 12->21 (CpG-like) somewhat
"""
import os, random
random.seed(42)

# Mild self-correlation + slight CpG suppression (assume 1=C, 2=G)
# rows: current char; cols: next char; values: probabilities
P = {
    "0": [0.30, 0.20, 0.20, 0.30],  # A -> A,C,G,T
    "1": [0.25, 0.30, 0.15, 0.30],  # C -> A,C,G(suppressed),T
    "2": [0.30, 0.25, 0.30, 0.15],  # G -> A,C,G,T
    "3": [0.30, 0.20, 0.20, 0.30],  # T -> A,C,G,T
}
chars = "0123"

def next_char(curr):
    probs = P[curr]
    return random.choices(chars, weights=probs, k=1)[0]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        seq = [random.choice(chars)]
        for _ in range(199):
            seq.append(next_char(seq[-1]))
        f.write("".join(seq) + "\n")
print("wrote 50000 Markov dinucleotide-biased sequences")
