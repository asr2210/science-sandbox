# Experiment 006: cCREs + GENCODE TSS

## Design
50,000 sequences = 35K cCREs (dELS-heavy) + 15K protein-coding gene
TSS-centered 200bp windows. Seed=6.

## Results vs 003
| eval | 003 (50K cCRE) | 006 (35K cCRE + 15K TSS) | Δ |
|---|---|---|---|
| 01 | 0.0758 | **0.0708** | -0.005 (-7%) |
| 03 | 0.0949 | 0.0968 | +0.002 (+2%) |
| 07 | 0.1444 | 0.1403 | -0.004 (-3%) |
| 08 | 0.0652 | 0.0616 | -0.004 (-6%) |
| 10 | 0.1277 | 0.1187 | -0.009 (-7%) |
| 13 | 0.1429 | 0.1366 | -0.006 (-4%) |
Time: 50s

## What I learned (counter-intuitive!)
**Adding TSS-centered windows HURT every eval set except eval_03.**
Possible reasons:
1. TSS regions are highly redundant in sequence character (canonical
   promoter elements: TATA, INR, CpG islands, GC-box). 15K TSS
   sequences add less diversity than 15K random cCREs would.
2. TSS replaced 15K diverse cCRE sequences (mostly dELS) → net loss
   of regulatory grammar coverage.
3. Promoters and enhancers may engage different MPRA regimes; mixing
   may confuse the model's regression head.
4. cCRE PLS already covers TSS-like content; adding raw TSS is
   redundant + biased.

eval_03 went UP slightly — it may weight K562/HepG2 promoter
activity (which TSS targets) more than enhancer activity.

## Theory update
**More-of-the-same regulatory content is harmful when it crowds out
diverse content.** The 003 mix (balanced PLS/pELS/dELS/CA/random) is a
local optimum that's hard to beat by ADDING categories — only by
REPLACING with categorically different sources.

## Next
Need a different lever. Either:
- Cell-type-specific ChIP-seq peaks (better labels for measured cells)
- Wider per-cCRE windows with overlap (multi-window augmentation)
- Conservation-weighted sampling
- Or stratification by predicted activity (motif-density binning)
