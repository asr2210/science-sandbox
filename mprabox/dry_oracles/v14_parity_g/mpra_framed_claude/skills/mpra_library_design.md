# MPRA Library Design — Key Findings

## Task context
prepare.py runs a black-box MPRA simulator on a 50,000 × 200bp library,
trains a sequence-to-activity model from scratch, evaluates on 14
anonymous held-out sets (eval_01 primary). Goal: high mean Pearson r,
ideally generalizing to cell types beyond the labeled K562/HepG2/SK-N-SH.

## What does NOT work (mean_r ≈ 0, 0.005 noise floor)
- Pure random A/C/G/T sequences
- Random ENCODE V4 cCREs (mostly inactive)
- Stratified ENCODE cCREs (PLS/pELS/dELS/CA mix)
- TF motif insertions in random background (25 canonical TFs, 1-6 copies)
- ENCODE DNase peaks from K562/HepG2/SK-N-SH directly
- DNase peaks + dinucleotide-shuffled controls (pos/neg contrast)
- Top DNase peaks duplicated 10x (5000 unique × 10 copies)

## What gives signal (first hints with mean_r ≈ 0.003, eval_13 K562 = 0.014)
- 200bp sequences from Tewhey lab ENCODE MPRA element BED files
  (excl chr7/13): K562 ENCFF822KPE, HepG2 ENCFF887WCC, SK-N-SH ENCFF861MOC

## Why distribution-matching matters
The simulator was almost certainly trained on (or computes activity
consistent with) Gosai et al. 2024 (Malinois) / Siraj et al. 2024
MPRA datasets — the only published MPRA cataloguing K562+HepG2+SK-N-SH
with 200bp library design. Eval sets are likely held-out chr7/chr13
sequences from this dataset.

A model trained on sequences distributionally similar to the simulator's
training set will produce coherent activity predictions; a model trained
on synthetic or out-of-distribution sequences gets noise from the
simulator and learns nothing.

## Key resources
- hg38.fa from UCSC (`hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`)
- ENCODE V4 cCRE BED: `ENCFF420VPZ.bed` (with PLS/pELS/dELS classes)
- DNase narrowPeak: K562 ENCFF821KDJ, HepG2 ENCFF341XEM, SK-N-SH ENCFF752OZB
- **Tewhey lab MPRA element BEDs (most useful)**:
  - K562   ENCSR971PLA → ENCFF822KPE.bed (228k 200bp regions)
  - HepG2  ENCSR833BYO → ENCFF887WCC.bed (109k 200bp regions)
  - SK-N-SH (Siraj) → ENCFF861MOC.bed (28k 200bp regions)
- Tewhey lab TSVs with chr/pos/ref/alt/log2FoldChange:
  - K562   ENCFF141ZOX.tsv (493k variant×allele rows)
  - HepG2  ENCFF876WFL.tsv (311k, but most NA chr)
  - SK-N-SH ENCFF521IVN.tsv (251k variant×allele rows)

## Open hypotheses to test
- Including alt-allele sequences with ref pairs (ENCODE/Tewhey variant MPRA design)
- Filtering by activity magnitude (top |log2FC|)
- Expanding to broader chromatin-accessible regions of similar genomic context
- More diverse cell-type DNase sources (broader regulatory motif coverage)
