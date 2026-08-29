# GC content shifts cell-type prediction (measured from random uniform libraries)

Tested random uniform libraries at GC=0.5, 0.6, 0.7 (exp 001, 009, 010).
Per-cell average correlations across all 14 evals:

| GC  | K562 avg | HepG2 avg | SKNSH avg | mean_r |
|-----|----------|-----------|-----------|--------|
| 0.50 | 0.82 | 0.88 | 0.84 | 0.852 |
| 0.60 | 0.80 | 0.86 | 0.90 | **0.857** |
| 0.70 | 0.78 | 0.80 | 0.95 | 0.835 |

## Per-cell GC preferences
- **SKNSH (neuronal):** monotonically prefers higher GC; saturates ~0.95 at GC≥0.7
- **HepG2 (hepatic):** peak near GC=0.5; degrades 0.88 → 0.80 from 0.5 → 0.7
- **K562 (erythroid):** mild preference for GC=0.5; small linear decline with GC

## How to use
1. If a library targets a single known cell type, match GC to its preference.
2. For balanced unknown-cell-type prediction, GC≈0.60 is the net optimum here.
3. Test whether within-library GC MIX beats fixed GC=0.6 (TBD in exp 011+).

## Why this likely generalizes
Cell types share GC preferences with their lineages (CpG islands at TSSs in
neural-active regions, AT-rich elements in hematopoietic lineage). A library
GC-balanced for representative cell types should transfer to held-out cell
types with similar lineage biology.

**Risk:** GC=0.6 overfits to neural-like cells. If eval cells are all
AT-balanced (muscle, T cells), GC=0.5 wins. Empirical mid is 0.55-0.60.
