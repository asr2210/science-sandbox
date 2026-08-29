"""Experiment 003: Single periodic pattern probe.

50,000 copies of "0123" repeated 50 times (length 200).
Each string has identical positional structure with period 4 and phase 0.
"""
import os

L = 200
N = 50_000
pattern = ("0123" * (L // 4))[:L]
assert len(pattern) == L

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join([pattern] * N) + "\n")

print(f"Wrote {N} copies of period-4 pattern: {pattern[:20]}...")
