"""Stratified homopolymers: 12,500 sequences each of '0...0', '1...1', '2...2', '3...3'.

Tests whether any single base is intrinsically preferred. If mean_r is similar
to random (~0), then the per-base preferences must cancel. If shifted, the
direction tells us about average homopolymer preference.
"""
import os

L = 200
PER_CHAR = 12500
ALPHA = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for c in ALPHA:
        line = c * L + "\n"
        for _ in range(PER_CHAR):
            f.write(line)

print(f"Wrote {4*PER_CHAR} homopolymer sequences to {out_path}")
