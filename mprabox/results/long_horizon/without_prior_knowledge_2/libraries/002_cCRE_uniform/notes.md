# 002 — cCRE uniform sample

## Design
50K cCREs uniformly sampled (without replacement) from 2.35M ENCODE V4
cCREs (ENCFF420VPZ.bed). 200bp window centered on each midpoint, extracted
from hg38.2bit. Soft-mask uppercased; N → uniform random ACGT.
Class proportions ≈ natural cCRE distribution: dELS 63% / pELS 11% /
CA 10% / CA-CTCF 5% / TF 4% / CA-H3K4me3 3% / PLS 2% / CA-TF 1%.

## Results (mean over 3 seeds)
- eval_01 = **0.7263** (vs 001 random 0.6954, **+0.031**)
- mean across 14 evals ≈ **0.762** (vs 001 ≈ 0.732, **+0.030**)
- per cell type avg: K562=0.764, HepG2=0.756, SK-N-SH=0.764

## Per-eval delta vs 001
01:+0.031 02:+0.035 03:+0.045 04:+0.011 05:+0.031 06:+0.035 07:**+0.105**
08:**−0.096** 09:+0.011 10:+0.034 11:+0.031 12:+0.038 13:**+0.113** 14:+0.034

cCRE wins on 13/14. Biggest wins: **eval_07 (+0.105), eval_13 (+0.113)**.
Big loss: **eval_08 (−0.096)**. eval_08 was 001's strongest eval (0.7841)
and dropped to 0.6880 with cCREs. This is informative.

## Across-seed variability
eval_01 by seed: 0.6976 / 0.7306 / 0.7506 → SD ≈ 0.027 (~10× higher than
001). Each seed samples a different 50K subset from 2.35M, so realized
libraries differ more than three independent uniform-random draws.
Implication: cCRE comparisons need bigger effect sizes to be conclusive,
or the experiment should fix the cCRE pool differently.

## Cell-type pattern
K562/HepG2/SK-N-SH all roughly equal under cCRE training (spread ≈ 0.01),
vs random where SK-N-SH systematically led. cCREs are pan-tissue
selected — the model presumably learns features common across the three.

## What this updates in T1
**T2:** Real regulatory elements modestly improve generalization
(~+0.025–0.03 mean) on most evals, confirming that the dense/coherent
TF motif content of natural sequences gives the model better signal
than the chance motifs in random DNA. BUT — eval_08's −0.096 says
natural sequences also LOSE coverage of some sequence space that random
covers. So "natural" trades coverage for density.

eval_07 and eval_13's huge wins (+0.10, +0.11) suggest those evals are
dominated by sequence types that are over-represented in cCREs (real
enhancers/promoters).

## Mechanism question for next experiment
Where does the +0.03 mean improvement come from?
(a) Real TF motifs in cCRE sequences? OR
(b) Natural compositional features (GC content, dinucleotide
    frequencies, k-mer biases) that random uniform DNA lacks?

Experiment 003 should be **dinucleotide-shuffled cCREs**: take the same
50K cCRE sequences but shuffle nucleotides (preserving dinucleotide
freq, destroying motifs). Compare to 001 and 002:
- 003 ≈ 002 → gain is compositional
- 003 ≈ 001 → gain is real motifs
- 003 between → both contribute (most likely)
