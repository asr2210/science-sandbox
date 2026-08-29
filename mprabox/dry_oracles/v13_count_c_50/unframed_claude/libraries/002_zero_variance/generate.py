"""Experiment 2: Zero-variance probe.

50,000 copies of a single fixed pseudo-random 200bp sequence.
Goal: diagnose what `mean_r` does when the library has no variance.

Predicted outcome under the "Pearson r between two predictions over my library"
hypothesis: r is undefined (zero variance in one or both vectors) → may default to
0 or NaN. Confirms that variance/spread in the library matters.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=42)
N, L = 50000, 200
alphabet = np.array(list("ACGT"))
single = "".join(alphabet[rng.integers(0, 4, size=L, dtype=np.int8)])

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text(("\n".join([single] * N)) + "\n")

print(f"Wrote {N} copies of one sequence (len {L}) to {out_path}")
print(f"Sequence: {single[:60]}...{single[-20:]}")
