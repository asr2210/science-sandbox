# 018 — Random + 1x25bp TF cCRE fragment per sequence

**Design.** Same as 012 but fragments from "TF" class cCREs (chromatin-accessible + TF-bound, excluding CTCF — 105K available).

**Result.** eval_01 = **0.4210** (beats random, loses to PLS). K562 = 0.583, HepG2 = 0.609, **SK-N-SH = 0.071** (HIGHER than PLS's 0.065).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 017 CA-CTCF | 0.585 | 0.614 | 0.042 | 0.4136 |
| 018 TF | 0.583 | 0.609 | **0.071** | 0.4210 |
| 012 PLS | **0.591** | **0.619** | 0.065 | **0.4248** |

**Interpretation — TF cCREs lift SK-N-SH more than PLS, but cost K562/HepG2 composition.** TF cCREs contain diverse TF binding sites (FOX, GATA, POU, REST, NEUROD, etc.) including cell-type-specific neural TFs. SK-N-SH benefits because some of these TFs are active in neurons.

But the broader TF motif diversity comes with lower GC content (no CpG-island constraint like promoters), pushing K562/HepG2 below PLS.

**Theory v16 — two mechanisms.** PLS lifts SK-N-SH via UNIVERSAL core promoter motifs (every cell type uses them at modest strength). TF lifts SK-N-SH via CELL-TYPE-SPECIFIC TF motifs (some neural TFs land in SK-N-SH; the rest of the diverse TF pool helps via similar means in other cells). The mechanisms are partly complementary.

**Practical implication.** If we could combine PLS's K562/HepG2 preservation with TF's SK-N-SH lift, we might break 0.4248.

**Next.** 019 — 50/50 mix: half the sequences get a PLS fragment, half get a TF fragment. The PLS-trained half should preserve K562/HepG2 while the TF-trained half should add SK-N-SH signal. Predicted mean_r ~0.426 if mechanisms combine additively.
