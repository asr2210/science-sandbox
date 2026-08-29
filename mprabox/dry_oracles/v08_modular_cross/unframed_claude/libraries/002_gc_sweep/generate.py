"""GC-content sweep: 5 banks of 10k sequences at GC = 20/40/50/70/85%."""
import numpy as np
from pathlib import Path

N_PER_BANK = 10_000
L = 200
SEED = 42
GC_LEVELS = [0.20, 0.40, 0.50, 0.70, 0.85]

rng = np.random.default_rng(SEED)
all_lines = []
for gc in GC_LEVELS:
    # P(G) = P(C) = gc/2, P(A) = P(T) = (1-gc)/2
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])  # A C G T
    bases = np.array(list("ACGT"))
    seqs = rng.choice(bases, size=(N_PER_BANK, L), p=probs)
    for row in seqs:
        all_lines.append("".join(row))

assert len(all_lines) == 50_000
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(all_lines) + "\n")
print(f"Wrote {len(all_lines)} sequences (5 banks × {N_PER_BANK})")
