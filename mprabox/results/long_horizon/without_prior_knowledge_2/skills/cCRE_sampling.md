# Skill: sampling 200bp sequences from ENCODE cCREs

When designing a library from natural regulatory elements.

## Inputs
- `data/cCRE/ENCFF420VPZ.bed` — ENCODE V4 cCRE BED9+ (2,348,854 elements,
  GRCh38). Column 10 = class (PLS, pELS, dELS, CA-CTCF, CA-H3K4me3,
  CA-TF, CA, TF). Class proportions:
  ```
  dELS         1,469,205  62.6%
  pELS           249,464  10.6%
  CA             245,985  10.5%
  CA-CTCF        126,034   5.4%
  TF             105,286   4.5%
  CA-H3K4me3      79,246   3.4%
  PLS             47,532   2.0%
  CA-TF           26,102   1.1%
  ```
- `data/genome/hg38.2bit` — GRCh38 reference, read with `twobitreader`.

## Recipe (uniform sample, 200bp centered on midpoint)
```python
import twobitreader, numpy as np

MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
HALF = 100

# 1. parse BED, keep only main chroms; record (chrom, midpoint, class)
rows = []
with open("data/cCRE/ENCFF420VPZ.bed") as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if p[0] not in MAIN_CHROMS: continue
        rows.append((p[0], (int(p[1]) + int(p[2])) // 2, p[9]))

# 2. uniform sample (oversample to absorb edge failures)
rng = np.random.default_rng(seed)
idx = rng.choice(len(rows), size=int(50_000 * 1.05), replace=False)

# 3. extract 200bp; replace N with random ACGT
tb = twobitreader.TwoBitFile("data/genome/hg38.2bit")
ALPHABET = np.array(list("ACGT"))
out = []
for i in idx:
    chrom, mid, _ = rows[i]
    L = len(tb[chrom])
    if mid - HALF < 0 or mid + HALF > L: continue
    seq = tb[chrom][mid - HALF: mid + HALF].upper()
    seq = "".join(c if c in "ACGT" else ALPHABET[rng.integers(0,4)] for c in seq)
    out.append(seq)
    if len(out) == 50_000: break
```

## Stratified sampling
For balanced class representation, draw equal counts per class:
```python
by_class = {}
for r in rows:
    by_class.setdefault(r[2], []).append(r)
target_per_class = 50_000 // len(by_class)  # ~6,250
sampled = []
for cls, recs in by_class.items():
    idx = rng.choice(len(recs), size=target_per_class, replace=False)
    sampled.extend([recs[i] for i in idx])
```

## Gotchas
- `twobitreader` returns mixed-case (lowercase = soft-masked repeats).
  Always `.upper()` and handle Ns.
- Some cCREs are <200bp wide; centering and extending to 200bp is fine
  but means flanking non-cCRE genomic context is included. This is
  probably desirable for context-dependent motif learning.
- Per-seed sampling produces correlated-but-distinct libraries; SD
  across seeds is ~10× larger than for pure random libraries because
  the 50K subset choice itself varies.
- chrM and unplaced contigs (`chrUn_*`, `chr*_random`, `chr*_alt`) excluded.

## When to use this
- Any experiment that wants natural regulatory sequence content
- As a starting point for ablations (shuffled controls, class-stratified)
- As a base for mixture libraries (random + natural)

## Empirical baseline (from 002_cCRE_uniform)
50K uniform cCRE sample produced eval_01=0.7263 (vs 0.6954 for uniform
random). Mean across 14 evals: ~0.762. eval_08 dropped 0.096 vs random,
others gained 0.01–0.11 — natural sequences trade some sequence-space
coverage for motif density.
