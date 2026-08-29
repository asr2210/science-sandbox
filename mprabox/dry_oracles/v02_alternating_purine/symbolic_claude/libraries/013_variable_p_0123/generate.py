"""Exp 013: variable p_template per sequence with 0,1,2,3 template.

Each sequence draws p ~ Uniform[0.05, 0.95]. Per-position: with prob p
the position is the template base (i mod 4); else uniform over the
other 3 bases. Expected match count per sequence varies from ~10 to ~190.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 13
P_LO, P_HI = 0.05, 0.95

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
template_tile = np.broadcast_to(template, (N, L))

# per-sequence p
p_per_seq = rng.uniform(P_LO, P_HI, size=N)  # (N,)
keep_mask = rng.random((N, L)) < p_per_seq[:, None]  # broadcast

rand_alt = rng.integers(0, 3, size=(N, L), dtype=np.uint8)
alt = (template_tile + 1 + rand_alt) % 4
seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

# sanity: match-count distribution
match_count = (seqs == template[None, :]).sum(axis=1)
print(f"wrote {N}; match count mean={match_count.mean():.1f}, "
      f"std={match_count.std():.1f}, min={match_count.min()}, max={match_count.max()}")
print(f"per-position base-0 freq at pos 0: {(seqs[:,0]==0).mean():.3f}")
print(f"unique seqs: {len(set(map(bytes, seqs)))}")
