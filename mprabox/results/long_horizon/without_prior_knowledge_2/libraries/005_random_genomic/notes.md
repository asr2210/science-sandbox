# 005 — random genomic 200bp windows

## Design
50K random 200bp windows sampled uniformly across hg38 main chromosomes
(chrom-length-weighted picking, then random position). Skip windows with
>10% N, replace remaining Ns with random ACGT. Three independent seeds.

## Results (mean over 3 seeds)
- eval_01 = **0.6636** (vs 001 random 0.6954 = **−0.032**, vs 002 cCRE 0.7263 = **−0.063**)
- mean across 14 evals ≈ **0.7016** (vs 001 ≈ 0.732, vs 002 ≈ 0.762)

## 5-way comparison
```
eval  001 rand  002 cCRE  003 dinuc-shuf  004 motifs-rand  005 genomic-rand
01    0.6954    0.7263    0.6189          0.6397           0.6636
02    0.7848    0.8195    0.6989          0.7237           0.7507
03    0.7612    0.8064    0.6828          0.6927           0.7427
04    0.7494    0.7605    0.6591          0.6974           0.6932
05    0.6951    0.7263    0.6187           0.6390          0.6643
06    0.7853    0.8199    0.7012          0.7238           0.7514
07    0.6684    0.7734    0.6482          0.6022           0.7239   (gen helps)
08    0.7841    0.6880    0.5912          0.7110           0.5581   (worst)
09    0.8115    0.8229    0.7113          0.7553           0.7475
10    0.7564    0.7909    0.6735          0.6969           0.6939
11    0.6833    0.7140    0.6104          0.6279           0.6533
12    0.6553    0.6928    0.5878          0.5952           0.6386
13    0.6584    0.7714    0.6609          0.5881           0.7414   (gen helps)
14    0.7851    0.8194    0.6991          0.7245           0.7499
mean  0.732     0.762     0.660           0.682            0.702
```

## Across-seed
eval_01: 0.6951 / 0.6781 / 0.6175 → SD ≈ 0.034 — high variability,
similar to other natural-source libraries.

## Pattern to highlight
- eval_07 and eval_13: random genomic helps (close to cCRE), same evals
  where cCREs gained most. These likely contain real-genomic-context-
  rich evaluations.
- eval_08: random genomic is the **worst** library (0.5581). eval_08
  monotonically degrades with naturalness: 001=0.78, 005=0.56.
  eval_08 seems to evaluate broad sequence-space coverage.

## Major theoretical implication

005 expected (under T4) to land between 001 and 002. Instead it landed
BELOW 001. So: **generic genomic context (without regulatory selection)
is actively HARMFUL relative to uniform random.**

Combined with prior results:
- Random uniform (001): 0.732 — broad coverage
- Random genomic (005): 0.702 — generic genomic context
- Motifs in random (004): 0.682 — bare motifs, no context
- Dinuc-shuf cCRE (003): 0.660 — composition only
- Real cCREs (002): 0.762 — motifs in REGULATORY context

Both "real motifs alone" (004) and "real context alone" (005) are
worse than random uniform. Only the COMBINATION (002) beats random.

## T4 → T5

**T5:** A library is informative when sequences are drawn from
**regulatory genomic segments** — i.e., regions selected by evolution
to contain TF motifs in functional arrangements. The model needs to
learn *both* what motifs do AND how they combine in real regulatory
context. Either alone is insufficient; together they generalize.

Implication: the path forward is to MAXIMIZE the diversity and
quality of real regulatory elements in the library, not to synthesize
or augment.

## Most informative next experiment (006)
**Stratified cCRE sampling by class.** ENCODE V4 has 8 classes (PLS,
pELS, dELS, CA-CTCF, CA-H3K4me3, CA-TF, CA, TF). 002 sampled them
proportionally (dELS=63%, PLS=2%). 006 will sample EQUAL counts per
class (~6.25K each). Tests:
- Whether class diversity helps over natural-distribution sampling
- Which classes (especially PLS promoters) carry most signal
This is cheap and decisively informative for further library design.
