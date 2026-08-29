# 005 — 90% random + 10% cCRE

**Design.** 45k uniform random + 5k ENCODE V4 cCREs (proportions of 003 scaled to 5k), interleaved.

**Result.** eval_01 = **0.4069** (Δ-0.012 vs random; Δ+0.013 vs cCRE). K562 = 0.566, HepG2 = 0.590, SK-N-SH = 0.064.

| | eval_01 | K562 | HepG2 | SK-N-SH |
|---|---|---|---|---|
| 001 random | 0.4192 | 0.590 | 0.623 | 0.045 |
| 005 mix90 | 0.4069 | 0.566 | 0.590 | 0.064 |
| 004 mix50 | 0.3956 | 0.551 | 0.563 | 0.072 |
| 003 cCRE | 0.3942 | 0.546 | 0.558 | 0.079 |

**Interpretation — sub-additive interpolation, biology-weighted.**
- 10% cCRE moved K562/HepG2 ~50% of the way toward cCRE level. So cCRE influence on the model is *disproportionate* to its share of the library.
- 10% cCRE moved SK-N-SH ~55% of the way (0.045→0.064, with cCRE max ~0.079).
- **Net mean_r dropped from 0.4192 to 0.4069** — biology hurts net metric even at small dose.

**Theory v5.** Adding cCREs to random consistently degrades K562/HepG2 r more than it lifts SK-N-SH (in mean_r terms). Either:
1. The eval distribution for K562/HepG2 is mostly composition-driven (random-like), and cCRE contamination shifts the model's learned distribution away from random.
2. SK-N-SH has so little dynamic range / signal-to-noise in this MPRA that even with perfect biology training, r maxes out near 0.1.

In either case, **simple mixing of random + cCRE doesn't beat pure random** on eval_01.

**Key open question.** Is the K562/HepG2 drop from random → cCRE driven by (a) k-mer composition shift, or (b) presence of real motifs distorting the learned function? And is the SK-N-SH lift from cCREs driven by (a') composition shift, or (b') real motifs?

**Next.** Mononucleotide-shuffled cCREs. Preserves k-mer composition of each cCRE exactly, destroys motifs. If shuffled cCRE matches real cCRE on K562/HepG2 → composition explains the drop. If shuffled cCRE keeps SK-N-SH at ~0.045 → real motifs drive the SK-N-SH lift.
