# Library optimization for black-box MPRA-like scorers

## Setup
Scorer takes a 50k × 200bp DNA library, returns Pearson r across 14 eval sets.
Eval reports mean_r, k562_r, hepg2_r, sknsh_r (suggests MPRA-like regulatory activity prediction).

## What we learned

### 1. Real DNA dominates random (lever +0.22)
Random uniform sampling → 0.46. Real hg38 200bp slices → 0.68.
The scorer's predictor is trained on real DNA — random sequences fall
outside its training distribution and produce uninformative outputs.

### 2. Within-library variance is required (lever +0.01)
Pearson r is bounded by variance of the features the scorer reads.
Restricting per-sequence GC to narrow band (40-55%) collapsed score
from 0.68 → 0.46. Widening it with mixed sources lifted to 0.69.

### 3. Variance must stay inside the predictor's training distribution
chrY satellites + chromHMM Het/Quies regions added wide GC variance
but DROPPED score — they're outside the euchromatic real-DNA manifold
the predictor was trained on. Heterochromatin/satellite repeats are
not useful for boosting r.

### 4. TSS-proximal regulatory enrichment at ~30% is the sweet spot
ENCODE cCRE labels {PLS, DNase-H3K4me3, pELS} are TSS-proximal,
high-GC, and regulatory-active. At ~30% of library they push high-GC
pole and lift score. At 50% they over-shift composition and drop it.

### 5. Synthetic motif insertion didn't help
Inserting 3-5 known TF motifs into real DNA gave no lift. Real
regulatory regions already contain natural motif arrangements.

## Winning recipe (eval_01 = 0.694)
- 5,000 each from chr22, chr19, chr17, chr20 (gene-dense, 200bp random slices)
- 5,000 from whole hg38 (length-weighted random, mid-low GC variance)
- 10,000 from ENCODE cCREs all categories (natural cCRE mix)
- 15,000 from ENCODE cCRE PLS|DNase-H3K4me3|pELS (TSS-proximal high-GC)
- Shuffle, take 50,000

## Useful data sources
- hg38.fa indexed with pyfaidx (use `as_raw=True, sequence_always_upper=True`)
- ENCODE GRCh38 cCREs: V4 BED at downloads.wenglab.org (~1M regions)
- Roadmap chromHMM (E123 = K562 15-state) for heterochromatin filtering
- FANTOM5 enhancers (didn't help, but available)
- Cell-type ATAC/DNase peaks (didn't help — too cell-specific)

## Iteration loop pattern
1. Generate 50k library deterministically (seeded np.random)
2. `python3 prepare.py libraries/NNN_*/` (~13s)
3. Read result.json eval_01 mean_r as primary; eval_07, eval_13 as secondary
4. Update notes.md, results.tsv, notebook.md; commit
5. Plan next based on hypothesis

## Things to try next time
- Find/download actual MPRA-tested sequences (likely predictor training set)
- Active-learning loop: score subset, retain top-scoring, mutate, rescore
- Specifically target TSS-flanking regions (±500bp) from GENCODE
- Sequence-to-activity model trained on ENCODE MPRA, rank-and-select
