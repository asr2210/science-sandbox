"""013_gradient_plus_motif — 009-style composition gradient (det counts + random
shuffle) PLUS row-index-proportional insertion of "0123" motif at random positions.
"""
import os, numpy as np
N, L = 50_000, 200
MOTIF = "0123"  # uniform composition motif
M = len(MOTIF)
MAX_INSERTS = 15
rng = np.random.default_rng(505)

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c_at = int(round(2 + 96 * frac))
    c_gc = 100 - c_at
    chars = [0]*c_at + [1]*c_gc + [2]*c_gc + [3]*c_at
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)

    # Insert K motifs at random non-overlapping positions
    K = int(round(MAX_INSERTS * frac))
    if K > 0:
        possible_starts = list(range(0, L - M + 1))
        rng.shuffle(possible_starts)
        used = []
        for start in possible_starts:
            if all(abs(start - u) >= M for u in used):
                used.append(start)
                if len(used) == K:
                    break
        for start in used:
            for j, ch in enumerate(MOTIF):
                row[start + j] = int(ch)

    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} gradient+motif (max {MAX_INSERTS} '0123' inserts) to {out}")
