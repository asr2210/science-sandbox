"""50K random uniform sequences with one common TF motif inserted at
random position. Mapping {0=A,1=C,2=G,3=T}.

Motifs:
  TATAAA = TATA box        -> 303000
  GGGCGG = GC box (Sp1)    -> 222122
  CACGTG = E-box (cMyc)    -> 101232
  TGACTCA = AP-1           -> 3201310
  ATTTGCAT = Octamer       -> 03331201
  GGGACTTTCC = NF-kB       -> 2220133311
"""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"
MOTIFS = ["303000", "222122", "101232", "3201310", "03331201", "2220133311"]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = [random.choice(ALPHA) for _ in range(L)]
        m = random.choice(MOTIFS)
        pos = random.randint(0, L - len(m))
        s[pos:pos + len(m)] = list(m)
        f.write("".join(s) + "\n")
print(f"Wrote {N} sequences with injected motifs")
