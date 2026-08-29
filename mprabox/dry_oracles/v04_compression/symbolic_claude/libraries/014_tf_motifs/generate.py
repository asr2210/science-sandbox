"""Random uniform background with embedded common TF motifs.
Assumes 0=A, 1=C, 2=G, 3=T.

Motif set:
- TATA box:    TATAAA   -> 303000
- CAAT box:    CCAAT    -> 11003
- GC box (Sp1):GGGCGG   -> 222122
- E-box:       CACGTG   -> 102132
- GATA:        GATAA    -> 20300
- AP-1:        TGACTCA  -> 320130
- CRE:         TGACGTCA -> 32012310
- NF-kB:       GGGRNNYYCC -> using GGGAAATCCC -> 2220003111
"""
import os, random
random.seed(42)
L = 200
motifs = [
    "303000", "11003", "222122", "102132",
    "20300", "320130", "32012310", "2220003111",
]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        seq = [random.choice("0123") for _ in range(L)]
        # insert 3-5 motifs per sequence at random positions
        n_motifs = random.randint(3, 5)
        for _ in range(n_motifs):
            m = random.choice(motifs)
            pos = random.randint(0, L - len(m))
            for j, ch in enumerate(m):
                seq[pos + j] = ch
        f.write("".join(seq) + "\n")
print("wrote 50000 sequences with embedded TF motifs")
