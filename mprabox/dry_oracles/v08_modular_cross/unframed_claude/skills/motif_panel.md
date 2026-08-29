# Motif panels for cell-line-specific MPRA design

## Cell-line-specific TF motifs (consensus, IUPAC ambiguous)

### K562 (erythroid leukemia)
- GATA1:   `WGATAR`         (e.g. AGATAA, TGATAG)
- KLF1:    `GGGGTG`         or `CACCC`
- NFE2:    `TGCTGASTCAGCA`  (MAF half + AP-1)
- TAL1/SCL: `CANNTG` (E-box, often `CAGCTG` or `CATCTG`)
- LDB1/LMO2: associated complex with GATA1
- AP-1 (broadly active too): `TGASTCA`

### HepG2 (hepatocellular)
- HNF1A:   `GTTAATNATTAAC`  (palindromic, AT-rich, ~13bp)
- HNF4A:   `AGGTCANAGGTCA`  (DR1, nuclear receptor direct repeat)
- CEBPA:   `TTGCGCAAT`      or `TTGCGYAAY`
- FOXA1:   `TGTTTAC`        or `TGTTTGY`
- PPARA:   `AGGTCA`         (also broad)
- LXR/RXR: half-sites `AGGTCA`

### SK-N-SH (neuroblastoma)
- ASCL1:   `CAGCTG`         (E-box)
- NEUROD1: `CAGATG`         (E-box variant)
- REST/NRSF: `TTCAGCACCNNGGNNAGT` (REPRESSOR — predicts LOW activity)
- CREB:    `TGACGTCA`       (cAMP-responsive, active in neurons)
- POU3F2:  `ATGCATAT`       (neural POU)
- LHX2:    `TAATTA`         (homeobox)

### Universal / housekeeping
- AP-1:    `TGASTCA`
- SP1:     `GGGCGGGG`       (GC-box)
- NF-Y:    `CCAAT`
- CREB:    `TGACGTCA`
- ETS:     `GGAAG[T/C]`
- E-box:   `CACGTG`
- YY1:     `CCATNTT`
- TATA:    `TATAAA`         (promoter)
- INR:     `YYANWYY`        (promoter)

## Background composition heuristics (empirical)
- K562 enhancers: GC-rich (~55-65%)
- HepG2 enhancers: AT-rich (~30-45%) — HNF1A/FOXA bind AT-rich
- SK-N-SH enhancers: roughly neutral (~45-55%)

## Notes
- Always try forward and reverse-complement of each motif.
- Density matters: typically 5-10 motifs per 200bp sequence to
  produce a strong predicted-active signal.
- For "null" sequences: AT-rich poly-N or repeat-rich sequences with
  no detectable motifs give a clear "inactive" prediction.
