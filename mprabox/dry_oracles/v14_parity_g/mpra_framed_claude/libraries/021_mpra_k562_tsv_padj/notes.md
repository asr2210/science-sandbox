# 021 — K562 TSV padj filter

Replaced K562 BED with K562 TSV selection: allele=ref, window=center, padj<0.05, top 22k by |lfc|. SKNSH 25k BED + HepG2 3k strict BED unchanged.

**Result:** mean_r = 0.0042 (vs 015's 0.0045 — slight drop).
- K562 = 0.0014 (down from 015's 0.0024)
- HepG2 = 0.0040 (matches 015's 0.0044)
- SKNSH = 0.0074 (up slightly from 015's 0.0066)

Last K562 |lfc| kept = 1.506, vs 015's 1.69 (BED-based). 70,236 TSV rows survive padj<0.05+ref+center filters.

**Interpretation:** padj filter does NOT add value over the BED's existing magnitude ranking. The K562 BED is already curated — its top 22k by |lfc| likely IS statistically significant. The TSV-derived top 22k pulls in a different population (probably wider chromosomal coverage, different window centers) that doesn't predict as well.

**Lesson:** for K562, sticking with BED-based |lfc| ranking is best. Statistical significance is redundant when the BED is already pre-filtered.

**Next (022):** K562 budget exploration. 022 tests if K562 sweet spot is actually NOT 22k but somewhere else — try K15 + H3-strict + S25 + 7k filler from broadly-active or moderate HepG2 (replicates). Determine if K562 r is plateaued or still climbing with smaller K562 budget.
