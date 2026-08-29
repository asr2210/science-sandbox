# Per-column balanced uniform 50% GC library

Construct a library where each column 0..199 contains exactly N/4 of each
nucleotide across the 50,000 sequences. Maintains the random uniform
expectations exactly while removing per-position sampling noise.

```python
import numpy as np
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

def per_col_balanced(seed):
    rng = np.random.default_rng(seed)
    base_vec = np.repeat(np.arange(4, dtype=np.int8), N // 4)
    matrix = np.empty((N, L), dtype=np.int8)
    for j in range(L):
        matrix[:, j] = base_vec[rng.permutation(N)]
    return ["".join(ALPHABET[row]) for row in matrix]
```

Properties:
- Library mean GC: exactly 0.5
- Per-column counts: exactly N/4 each base
- Per-sequence GC: Bin(L, 0.5) distribution (natural binomial variation)
- Pairwise column dinucleotide distribution: ≈ uniform (each of 16 dinucleotides
  ≈ N/16 = 3125 across each column pair, in expectation)

Performance on this task: mean_r ≈ 0.519 on eval_01 (varies ±0.005 by seed).
Essentially equivalent to plain random uniform (also 0.519) but very slightly
more stable.
