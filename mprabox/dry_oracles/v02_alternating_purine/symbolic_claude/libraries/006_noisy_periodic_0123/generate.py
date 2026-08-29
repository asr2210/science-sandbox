"""Exp 006: noisy periodic "0123" pattern (period 4).

Each sequence: position i has base (i mod 4) with prob 0.7,
otherwise uniform among the other 3 bases (0.1 each).
All 4 bases appear at every position library-wide.
Tests whether positional periodic structure boosts the score.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 6
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
template = np.arange(L, dtype=np.uint8) % 4  # (L,)
template_tile = np.broadcast_to(template, (N, L))

keep_mask = rng.random((N, L)) < P_TEMPLATE
# For non-keep positions, pick a random base != template[pos]
rand_bases = rng.integers(0, 3, size=(N, L), dtype=np.uint8)
alt = (template_tile + 1 + rand_bases) % 4  # any base != template
seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

# Sanity: per-position base 0 frequency
pos_freq0 = (seqs == 0).mean(axis=0)
print(f"wrote {N}. base-0 freq at pos 0..7: {np.round(pos_freq0[:8], 3)}")
print(f"unique sequences: {len(set(map(bytes, seqs)))} (expect ~{N})")
