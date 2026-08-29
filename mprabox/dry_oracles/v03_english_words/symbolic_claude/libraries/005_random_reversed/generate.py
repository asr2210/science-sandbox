"""Exp 005: same sequences as exp 001 (random uniform seed=0) but REVERSED ORDER.

Diagnostic: if target is content-based, r should equal exp 001 (~0.42, same set).
If target is index-based (per-position target labels), reversing order flips the
correlation sign or changes it substantially.
"""
import os

SRC = os.path.join(os.path.dirname(__file__), "..", "001_random_uniform", "sequences_0.txt")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

with open(SRC, "rb") as f:
    lines = f.readlines()
assert len(lines) == 50_000, len(lines)
lines.reverse()
with open(OUT, "wb") as f:
    f.writelines(lines)
print(f"Wrote {len(lines)} reversed sequences to {OUT}")
