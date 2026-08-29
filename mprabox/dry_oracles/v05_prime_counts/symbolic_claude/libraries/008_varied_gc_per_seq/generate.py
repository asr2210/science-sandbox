"""Each sequence has a random per-sequence GC fraction sampled
uniformly from [0.1, 0.9]. Within each sequence, positions are i.i.d.
This maximizes per-sequence composition variance while keeping
per-position alphabet diversity broad."""
import random, os
random.seed(42)
N, L = 50_000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
alpha = "0123"
with open(out_path, "w") as f:
    for _ in range(N):
        gc = random.uniform(0.1, 0.9)
        at = 1.0 - gc
        # split AT into 0,3 and GC into 1,2 each roughly equally with jitter
        a_frac = random.uniform(0.3, 0.7) * at
        t_frac = at - a_frac
        c_frac = random.uniform(0.3, 0.7) * gc
        g_frac = gc - c_frac
        w = [a_frac, c_frac, g_frac, t_frac]
        f.write("".join(random.choices(alpha, weights=w, k=L)) + "\n")
print(f"Wrote {N} varied-GC sequences")
