# 020 — Random + 1x25bp motif-enriched PLS

**Design.** Like 012 but only keep 25bp PLS fragments containing >=1 match to canonical TF motifs (TATA, CCAAT, SP1, E-box, REST, POU, NFkB, NR, GATA). 50k accepted from 336k attempts (14.9% pass rate).

**Result.** eval_01 = **0.4180** — WORSE than 012 in ALL three cell types. K562 = 0.586, HepG2 = 0.614, SK-N-SH = 0.055.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 012 PLS (no selection) | 0.591 | 0.619 | **0.065** | **0.4248** |
| 020 PLS motif-enriched | 0.586 | 0.614 | 0.055 | 0.4180 |

**Interpretation — selection collapsed diversity.** Keeping only motif-positive fragments narrows the fragment pool from ~50K to ~50K from 7x smaller effective parent pool (333K candidate fragments → 50K accepted; each PLS contributes only ~1 accepted fragment after multiple offset rejections). The resulting fragments come from a heavily down-sampled subset of PLS regions and at biased offsets within each PLS window.

The model's K562/HepG2 fit drops because the fragment composition becomes more biased (likely higher GC, more CpG-dense), and SK-N-SH drops because the diverse contextual variety is replaced by motif-centric monoculture.

**Theory v18 — DIVERSITY > DENSITY for fragment selection.** The model benefits from seeing varied promoter contexts (some core-motif-centric, some pioneer-factor-adjacent, some spacer regions), not just motif-densest subsets. Selection-based enrichment LOSES.

**Next.** 021 — try GC-compensated random background (random sampled at 48% GC instead of 50%) to compensate for CpG-rich PLS fragments (~60% GC). Net composition would be ~49.5% GC, slightly below 50%. Tests whether tiny composition tuning recovers HepG2.
