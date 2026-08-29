# Experiment 005: 25K cCREs + 25K dinucleotide-matched Markov controls

## Design
- 25,000 real cCREs (8K dELS + 6K pELS + 4K PLS + 4K CA_TF + 3K CTCF)
- 25,000 Markov-generated sequences: dinucleotide transition matrix
  computed from the real cCREs, sampled to length 200bp each
- Composition matched but motifs and higher-order grammar destroyed
- Seed=5

## Results vs 003 (50K real cCREs)
| eval | 003 | 005 | Δ | rel |
|---|---|---|---|---|
| 01 | 0.0758 | 0.0727 | -0.003 | -4% |
| 03 | 0.0949 | 0.0897 | -0.005 | -5% |
| 07 | 0.1444 | 0.1411 | -0.003 | -2% |
| 08 | 0.0652 | 0.0604 | -0.005 | -7% |
| 10 | 0.1277 | 0.1291 | +0.001 | +1% |
| 13 | 0.1429 | 0.1359 | -0.007 | -5% |
Time: 40s

## What I learned
- Markov controls (motif-free, composition-matched) slightly **hurt**
  the library (~5% drop) but DON'T crash it.
- Interpretation: motifs/grammar DO contribute, but the model still
  learns from the 25K real cCREs even when half the library is
  composition-matched noise.
- **25K cCREs alone ≈ 0.0727; 50K cCREs ≈ 0.0758.** Diminishing returns
  from doubling cCRE count — only +0.003 (4%).
- This suggests we're approaching a ceiling on what additional cCRE
  diversity can buy. The bottleneck may be label noise, model
  architecture, or eval-set intrinsic difficulty.

## Insights
- The model is already extracting most of the signal achievable from
  cCRE training data with ~25K diverse examples.
- To push past 0.076, I likely need either:
  1. Different sequence SOURCES (not just cCREs)
  2. Better activity-stratified sampling
  3. Data augmentation strategies that effectively multiply training
     examples

## Next
GENCODE TSS-proximal windows mixed with cCREs as exp 006. TSS regions
are high-activity by definition (promoters are gold-standard regulatory)
and may add a different signal than cCRE PLS (which is broader/more
inclusive). Tests whether different annotation-type genomic features
add complementary information.
