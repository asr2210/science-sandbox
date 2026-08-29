# Exp 015 — multi-chromosome real DNA tiles (chr1/18/19/22)

50k 200bp windows, ~12.5k from each of chr1, chr18, chr19, chr22.

## Result

| metric  | chr22 alone | chr18 alone | multi-chrom |
|---------|------------:|------------:|------------:|
| eval_01 | 0.3202      | 0.3043      | 0.3157      |
| k562    | 0.1443      | 0.1438      | 0.1446      |
| hepg2   | 0.1990      | 0.1978      | 0.2017      |
| sknsh   | 0.6173      | 0.5715      | 0.6008      |

Mid-way between chr22 (best) and chr18 (worst). HepG2 marginally up
(+0.003) but SKNSH lost 0.017. K562 unchanged.

Interpretation: chr22 alone is best because chr22's GC distribution
(47% mean) is close to SKNSH's 50% optimum while still hitting HepG2's
AT-preference and K562 baseline. Adding chr18 (40% GC) drags SKNSH down
without helping HepG2 (already saturated at +0.20).

Diversity hypothesis (theory v7) NOT supported in this form — chr22
already has enough GC diversity internally.

**Pivot**: try cCRE class-specific subsets (dELS = distal enhancer-like
elements) — should still be naturalistic but maybe more "MPRA-active"
than random tiles.
