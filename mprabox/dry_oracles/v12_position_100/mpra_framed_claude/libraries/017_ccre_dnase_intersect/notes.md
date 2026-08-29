# Experiment 017: cCRE-DNase intersection (high-confidence regulatory)

## Design
- 30K DNase peaks (10K each cell) where peak summit falls within a cCRE
  (validated by BOTH cell-type accessibility AND cross-tissue catalog)
- 15K cCREs that do NOT overlap any peak from our 3 cells (broad
  regulatory grammar from other tissues)
- 5K random
Seed=17.

Intersection counts found:
- K562: 205,820 cCRE-overlapping peaks (87% of K562 peaks overlap a cCRE)
- HepG2: 82,729 (93% overlap)
- SKNSH: 134,226 (87% overlap)

## Results — in noise band, K562/HepG2 slight up
eval_01 = **0.0757** (K562=0.0811, HepG2=0.0807, SKNSH=0.0652)

| eval | 009 | 017 | Δ |
|---|---|---|---|
| 01 mean | 0.0772 | 0.0757 | -0.0015 |
| 01 K562 | 0.0799 | **0.0811** | +0.0012 |
| 01 HepG2 | 0.0812 | 0.0807 | ~0 |
| 01 SKNSH | 0.0705 | 0.0652 | -0.0053 |
| 07 | 0.1437 | 0.1409 | -0.0028 |
| 08 | 0.0639 | 0.0578 | -0.0061 |

K562 hit a new high (0.0811, but within noise of 009's 0.0799).
Mean is dragged down by SKNSH (0.0652).

## What I learned
**Label confidence (intersection) marginally helps the "easy" cells**
but not enough to break noise band. SKNSH drops further (-0.005).
Eval_08 also drops significantly (-0.006) — perhaps eval_08 rewards
the broader low-confidence cCRE diversity that this design excludes.

## Theory update
- Intersection labels favor K562/HepG2 slightly (cleaner accessibility
  signal in well-characterized cells)
- BUT removing the cCRE-only diversity hurts on hard evals (08) and SKNSH
- Net: in noise band as expected

## Next: try TF ChIP-seq for CTCF (exp 018)
CTCF has the strongest, most well-defined motif in the genome (CCCTC
binding pattern). ChIP-seq peaks contain CTCF motifs at high density.
Including CTCF ChIP-seq peaks from our 3 cells gives the model concentrated
motif training data — qualitatively NEW signal vs DNase (accessibility)
or cCRE (regulatory annotation).

Plan: 15K cCRE + 20K DNase (~7K each cell) + 10K CTCF ChIP (~3.3K each
cell) + 5K random.
