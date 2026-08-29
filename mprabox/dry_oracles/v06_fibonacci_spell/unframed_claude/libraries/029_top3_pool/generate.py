"""Experiment 029: Top-3 seed pool — 16.7k each from seeds 6, 42, 777.

Combines best three single-seed draws (0.1387, 0.1359, 0.1358) into one
50k library. Tests whether averaging upper-tail draws preserves their
"luck" or regresses to mean.
"""
from pathlib import Path

ROOT = Path(__file__).parents[2]
LIB = ROOT / "libraries"

def read(p):
    with open(p) as f:
        return [l.strip() for l in f if l.strip()]

s6   = read(LIB / "006_genome_windows" / "sequences_0.txt")
s42  = read(LIB / "025_seedsweep"      / "sequences_0.txt")
s777 = read(LIB / "027_seedsweep"      / "sequences_0.txt")

# Take 16,667 from each (last gets 16,666)
out = s6[:16_667] + s42[:16_667] + s777[:16_666]
assert len(out) == 50_000, len(out)

# Deterministic shuffle so they're interleaved
import random
random.Random(29).shuffle(out)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} sequences from top-3 seed pool")
