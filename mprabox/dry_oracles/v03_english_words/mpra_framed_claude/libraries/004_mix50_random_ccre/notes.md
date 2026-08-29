# 004 — 50/50 random + cCRE mix

**Design.** 25k uniform random + 25k ENCODE V4 cCREs (proportions of 003 scaled to 25k), interleaved.

**Result.** eval_01 = **0.3956** — essentially identical to pure cCRE (003 = 0.3942), NOT in-between random and cCRE. K562 = 0.551, HepG2 = 0.563, SK-N-SH = 0.072.

| | eval_01 | K562 | HepG2 | SK-N-SH |
|---|---|---|---|---|
| 001 random | 0.4192 | 0.590 | 0.623 | 0.045 |
| 003 cCRE | 0.3942 | 0.546 | 0.558 | 0.079 |
| **004 mix50** | **0.3956** | **0.551** | **0.563** | **0.072** |

**Interpretation — additivity refuted.**
- K562/HepG2 r is *dominated* by the cCRE half of the training data, not the random half. Mixing 50% random sequences does NOT preserve random's K562/HepG2 advantage.
- SK-N-SH lift from cCREs is also slightly muted (0.072 vs 0.079).
- The model behaves as if the cCRE distribution forces the prediction head into a narrower output range, and the random half doesn't pull it back.

**Theory v4.** The model trained by `prepare.py` is sensitive to the *narrowest* distribution shape present in training. When biology-shaped cCRE sequences are added to a uniform random pool, the model's effective output range narrows to fit cCREs, hurting its ability to predict the wider distribution that K562/HepG2 evaluations apparently span.

This means the two generalization dimensions (compositional entropy ↔ biological grammar) **are not additive**. There may be a SMALL dose of biology that doesn't contaminate the composition signal — or biology may need to be *blended into the composition itself* rather than added as a separate subset.

**Next.** Two informative paths:
1. Small dose test: 90% random + 10% cCRE. If K562/HepG2 recovers AND SK-N-SH lifts, small biology dose is the right move.
2. Disentanglement: shuffled cCREs (preserve k-mer composition, destroy motifs). If shuffled cCREs match real cCREs on K562/HepG2 but match random on SK-N-SH, we've directly identified composition vs grammar as the two levers.

I'll do (1) first since it could yield a directly improved library, then (2) as a deeper diagnostic.
