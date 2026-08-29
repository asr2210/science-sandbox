# 026 — Real K562 H3K27ac peaks + augmented K562 motifs

## Method
25k real K562 H3K27ac peaks, augment by inserting 6 K562 motifs.
25k dinuc-shuffled (preserves dinuc composition including added motifs).

## Results (eval_01)
mean_r = +0.0021 (K562=+0.0054, HepG2=+0.0025, SKNSH=-0.0017)

## Lesson
- Augmenting real peaks with synthetic motifs DOES give positive K562
  (+0.0054), but lower than pure synthetic exp 012 (+0.0089).
- Augmentation doesn't break the +0.0045 plateau.
- Real-genomic backbones add unhelpful variance.

## Implication
- Pure synthetic > hybrid > real-only for K562 r on eval_01.
- Each design tweak rearranges per-cell lift but ceiling is firm.

## Next (exp 027)
Try exp 012 with denser motifs (14 vs 12) and a slightly broader panel
including motifs that also help HepG2 (NR half-site, CCAAT). See if a
small panel tweak can crack +0.0045.
