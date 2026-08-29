"""50bp x 4 tandem repeat with a TATA-like motif embedded at unit position 22.
Total motif occurs periodically at positions 22, 72, 122, 172.
Tests if periodic motifs combined with tandem repeats help."""
import random, os
random.seed(43)
N, L = 50_000, 200
UNIT = 50
ALPHA = "0123"
MOTIF = "303000"  # TATAAA
ML = len(MOTIF)
POS_IN_UNIT = 22
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = [random.choice(ALPHA) for _ in range(UNIT)]
        unit[POS_IN_UNIT:POS_IN_UNIT + ML] = list(MOTIF)
        unit_str = "".join(unit)
        f.write(unit_str * (L // UNIT) + "\n")
print(f"Wrote {N} 50bpx4 with periodic TATA motif")
