"""Random uniform background with 5 random short k-mer 'motifs'
embedded at random positions. Tests if local structure/repetition of
candidate motifs helps the learner.

Each sequence has ~50% random background, ~50% repeated motifs.
"""
import os, random
random.seed(42)

L = 200
N = 50000
# A small bank of 5-mers to draw from; each sequence picks 5 motifs
# and tiles them into random positions
motif_bank = []
random.seed(7)
for _ in range(64):
    motif_bank.append("".join(random.choice("0123") for _ in range(5)))

random.seed(42)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        seq = [random.choice("0123") for _ in range(L)]
        # insert ~10 motif copies at random positions
        for _ in range(10):
            m = random.choice(motif_bank)
            pos = random.randint(0, L - len(m))
            for j, ch in enumerate(m):
                seq[pos + j] = ch
        f.write("".join(seq) + "\n")
print("wrote 50000 sequences with embedded 5-mer motifs")
