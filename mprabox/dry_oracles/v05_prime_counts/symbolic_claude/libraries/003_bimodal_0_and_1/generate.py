"""Bimodal library: 25,000 all-zeros + 25,000 all-ones. Tests whether
scoring depends purely on per-sequence variance, and yields a 2-modal
distribution of model outputs."""
import os
N_HALF = 25_000
L = 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    line0 = "0" * L + "\n"
    line1 = "1" * L + "\n"
    f.writelines([line0] * N_HALF)
    f.writelines([line1] * N_HALF)
print(f"Wrote {2 * N_HALF} sequences")
