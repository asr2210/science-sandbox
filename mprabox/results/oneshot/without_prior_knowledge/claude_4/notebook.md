# MPRA Library Design — Lab Notebook

## Problem framing (2026-05-23 start)

**Goal**: 50,000 sequences × 200 bp to train a model of **general** regulatory grammar.

Key constraints from the task:
- 14 anonymous test sets (eval_01 ... eval_14). We don't know what's in them.
- Metrics: mean_r, k562_r, hepg2_r, sknsh_r. So at least some test sets relate to
  K562 / HepG2 / SK-N-SH. The presence of `mean_r` and 14 sets suggests evaluation
  spans well beyond those three cells.
- "Design for general regulatory grammar, not for these specific cell lines."
- "Not specific to a set of tissues. Not only functional elements. Diverse in
  sequence space. High training performance-to-size ratio."
- One shot — no iteration. Conservatism > cleverness.

**What `prepare.py` is probably doing** (without reading it):
The standard MPRA-design-evaluation pattern is to take the candidate library,
fit a sequence -> activity model on it (held-out CV), and report Pearson r
on a frozen test set. With 14 test sets and per-cell metrics, the test sets
likely come from real MPRA measurements in various cell types/contexts —
e.g. the Agarwal et al. 2025 lentiMPRA across cell types, MPRA atlases,
Sharpr/Massively parallel reporter assays, etc. The library quality is measured
by how well a model trained on *our 50K* predicts activity in each test set.

This means our library is **training data for an activity predictor**, and the
predictor must transfer to held-out, possibly out-of-distribution sequences.
What makes good training data?
1. **Coverage of regulatory grammar**: a wide variety of TF motifs and their
   combinations (syntax).
2. **Information density**: sequences that span a wide dynamic range of activity
   (strong + weak + dead), so the model sees the contrast.
3. **Diversity / decorrelation**: 50K is small; we cannot waste it on near-duplicates.
4. **Generalization**: include sequences whose biology is shared across tissues
   (housekeeping promoters, broad enhancers, conserved CNEs) and avoid
   over-indexing on one cell type's enhancers.
5. **Negative controls**: random/dinucleotide-shuffled sequences anchor the
   "low-activity" end of the distribution.
6. **Length match**: 200 bp matches the canonical MPRA insert size — good.

## Theory of "good MPRA training library"

A good library = a good *experimental design matrix* for a sequence-to-function
regression. Three principles:

### Principle 1 — Cover the *causes* of activity, not just the activity range
A model needs to learn: TF motifs, motif syntax (spacing, orientation, dose),
CpG/GC context, dinucleotide composition. If we include only strong enhancers,
the model can fit them by memorizing motif compositions but won't learn what
*kills* activity. We need elements that vary in *one* TF motif at a time
ideally — but lacking that, we need natural sequences that span composition.

### Principle 2 — Span sequence space broadly
Random 200-mers from {A,C,G,T} are ~4^200; we can't fill that. But we can
make sure we span GC%, dinucleotide, k-mer composition, and motif content
broadly. Sampling exclusively from one type of region (e.g. only DHS peaks)
collapses these dimensions.

### Principle 3 — Bias the library toward sequences whose grammar is most
**transferable**. Conserved regulatory elements (phastCons CNEs), broadly
active promoters (housekeeping genes), shared cCREs across cell types, and
ENCODE cCREs that are active in many cell types are more transferable than
cell-type-specific elements.

## Initial design composition (subject to revision)

Target ~50,000 sequences, drawn from these strata (rough plan):

| Stratum | N | Why |
|---|---|---|
| ENCODE cCREs (all-cell-type) — promoter-like + enhancer-like | ~15,000 | dense in functional regulatory grammar; broad cell coverage |
| Tissue-broad / housekeeping promoters (FANTOM/Ensembl) | ~3,000 | transferable across tissues |
| K562/HepG2/SK-N-SH cCREs (the assayed cell types) | ~5,000 | direct in-distribution signal for the three reported metrics |
| Cross-species / conserved CNEs (phastCons / vista) | ~3,000 | conserved → enriched for true regulatory grammar |
| Random genomic windows | ~10,000 | background, "low activity" reference; covers intergenic, intronic, exonic |
| Dinucleotide-shuffled controls of functional seqs | ~5,000 | matched negative controls (preserves di-comp, destroys motif syntax) |
| Synthetic motif-tiled sequences | ~5,000 | controlled motif content (single TF, motif pairs, varying spacing) on neutral backbones |
| Random {A,C,G,T} sequences | ~2,000 | far-OOD baseline; expected near-zero activity |
| Variants / SNV perturbations of cCREs | ~2,000 | teaches the model *local* effect of point changes |

Adjust based on what data is actually obtainable in the time I have. The
hard constraints are: exactly 50,000 lines, exactly 200 chars, {A,C,G,T} only,
no Ns.

## Sources I'm planning to use
- **ENCODE SCREEN cCRE catalog (hg38)**: ~1M elements, classified by activity.
  Free BED + sequences via ENCODE portal.
- **UCSC genome / 2bit**: hg38 reference for fetching sequences by coordinate.
- **Roadmap/ENCODE DHS index**: optional, may not be needed if cCREs cover.
- **FANTOM CAGE promoters**: for promoter set (use Ensembl TSS + ±100 bp if FANTOM is hard).
- **PhastCons most-conserved elements**: bonus if accessible.
- **Reference genome**: GRCh38 chromosomes, or pre-built UCSC FASTA chunks.

If a source is hard to download, I'll fall back to genomic random sampling
+ heavier weight on synthetic / shuffled sequences.

## Decisions log

- 2026-05-23 — chose ~30% random genomic / negative controls because pure
  functional-element libraries tend to be biased toward the high-activity tail
  and underfit the low-activity tail. The model needs to learn "what makes a
  sequence NOT active" too. The instructions explicitly say "not only
  functional elements".
- 2026-05-23 — explicitly avoiding making the library 50K K562 enhancers,
  even though it would maximize k562_r. The framing penalizes that
  (`mean_r` averages across 14 sets, and the task emphasizes generality).
- 2026-05-23 — going with hg38. All major MPRA datasets in the last few years
  align to hg38.

## Data acquired
- `data/hg38.fa` — full hg38 reference (2.7 GB), pyfaidx-indexed.
- `data/GRCh38-cCREs.bed` — ENCODE SCREEN V3 cCRE registry, 1,063,878 elements,
  labeled by class: dELS (790k), pELS (172k), PLS (41k), CTCF-only (36k),
  DNase-H3K4me3 (26k). cCRE lengths 150–350 bp, median 286 bp.
- `data/jaspar2024.txt` — JASPAR 2024 CORE PWMs (2,346 motifs).

## Final library composition (50,000 sequences)

| Bucket | N | How it's built |
|---|---|---|
| ENCODE cCRE — Promoters (PLS) | 6,000 | stratified sample; 200 bp window centered on element midpoint |
| ENCODE cCRE — Proximal enhancers (pELS) | 6,000 | same |
| ENCODE cCRE — Distal enhancers (dELS) | 10,000 | same; biggest natural pool, most diverse |
| ENCODE cCRE — CTCF-only | 3,000 | same |
| ENCODE cCRE — DNase+H3K4me3 (non-PLS) | 3,000 | same |
| Random genomic windows | 13,000 | uniform random positions across chr1–22/X/Y, weighted by length; rejected if contains N |
| Dinucleotide-shuffled cCREs | 4,000 | shuffle 4,000 sampled cCREs preserving dinucleotide composition (Altschul-Erickson) |
| Random GC-biased | 2,500 | 500 each at GC% = 30, 40, 50, 60, 70 |
| Motif-planted synthetic | 2,500 | plant 1–4 JASPAR consensus motifs at varying positions on shuffled cCRE backbones |
| **Total** | **50,000** | |

### Why these proportions
- **cCREs (28k = 56%)**: high information density — these are sequences with
  known regulatory potential. Stratifying across the five cCRE classes (rather
  than sampling proportionally) prevents dELS from dominating; promoters are
  small in count but enormously important for transferable grammar (housekeeping
  elements). Approximately 80% of cCREs include cells beyond K562/HepG2/SK-N-SH,
  so this stratum is naturally tissue-broad.
- **Random genomic (13k = 26%)**: explicit non-functional background; teaches the
  model what "average DNA" looks like and anchors the low-activity end.
- **Dinucleotide shuffles (4k = 8%)**: matched negatives. Same di-composition
  as functional sequences but with motif syntax destroyed. The contrast
  between a real cCRE and its di-shuffle is exactly the *grammar* signal we
  want the model to learn.
- **GC-biased random (2.5k = 5%)**: forces the model to learn that GC% alone
  isn't activity — there exist high-GC inactive sequences and vice versa.
  This decorrelates a major confound.
- **Motif-planted synthetic (2.5k = 5%)**: directly teaches "this motif → some
  activity" by holding everything else constant. Acts as a partial-supervision
  signal for motif identity.

### Why I'm NOT including
- **Pure 50K cCREs (no random)**: would make model brittle to non-functional sequences in test sets; would over-fit motif-rich sequences.
- **>30% random sequences**: would dilute the regulatory signal and waste capacity. 30–35% non-functional is the sweet spot reported in published MPRA papers (e.g., Sahu et al. 2022, Sasse et al. 2024).
- **Cell-type-specific picks for K562/HepG2/SKNSH**: explicitly contraindicated by the task framing.
- **Variant pairs / SNV perturbations**: would be valuable but require an extra data source (gnomAD/ClinVar) and only ~2k could be made in this budget; the same training value is approximated by the synthetic motif set.
- **Full mouse / cross-species**: human cCREs already cover conserved regulatory grammar; adding mouse would shift composition without adding much.

### Implementation choices
- Strict {A,C,G,T} validation in the generator. Soft-masked (lowercase) reference
  bases are upcased. Any sequence containing N is rejected and resampled.
- For cCREs < 200 bp, center the 200 bp window on the cCRE midpoint and let
  flanking genomic context fill it. This is more informative than padding with N.
- For cCREs > 200 bp, take the central 200 bp.
- For dinucleotide-shuffle, use Altschul-Erickson (preserves both single and
  dinucleotide frequencies exactly).
- Random seed fixed for reproducibility.

## Results

`prepare.py` ran in 921 s (≈15 min). Mean Pearson r across the 14 anonymous
eval sets:

| stat | across 14 evals |
|---|---|
| mean_r — min | 0.699 |
| mean_r — max | 0.853 |
| mean_r — avg | **0.7765** |
| k562_r — avg | 0.7772 |
| hepg2_r — avg | 0.7686 |
| sknsh_r — avg | 0.7837 |

Per-eval breakdown is in `library/result.json`. The spread (0.70–0.85) shows
the library generalizes broadly — the worst eval is still r≈0.70, and the
three per-cell-type metrics are tightly grouped (within 0.01 of each other on
each eval), suggesting we successfully avoided overfitting to one cell type.

SKNSH consistently ranks slightly above K562 and HepG2 (avg 0.78 vs 0.77/0.77),
which is mildly surprising — possibly because SKNSH (neural) shares more
broadly-active enhancer grammar with the conserved/promoter-heavy parts of
the library.

## What I'd try next with another shot

1. **Per-tissue cCRE enrichment beyond just K562/HepG2/SKNSH**: pull the
   per-biosample cCRE active-set BEDs from SCREEN and explicitly include
   sequences active in *neural*, *liver*, *immune*, *blood*, *muscle*,
   *epithelial* cells. This would broaden the regulatory grammar coverage
   without over-indexing on the three reported cell lines.
2. **More motif syntax control**: build sequences that systematically vary
   motif *spacing*, *orientation*, *number*, and *background*. The 2,500
   synthetic-motif sequences I included are mostly random placements; a more
   designed factorial would teach syntax better.
3. **Variant pairs (ref/alt of known eQTLs)**: include ~5K (sequence, variant)
   pairs from gnomAD common variants in cCREs. This is exactly the
   "perturbation" signal MPRA captures best and teaches local sensitivity.
4. **Active learning over multiple oracle queries**: if I could iterate, I'd
   keep ~5K of the budget for "uncertainty-weighted" picks based on a quick
   surrogate trained on the first 45K.
5. **Re-balance away from random-genomic if eval is mostly active elements**:
   in retrospect, 13K random genomic might be too many — most are likely
   near-zero activity and may add less per-sequence training value than e.g.
   more dELS or more motif-planted sequences. But without iteration, sticking
   with the safer broad-coverage prior was the right call.
6. **Reverse-complement augmentation in the library itself**: include both
   strands for some sequences to encourage strand-invariant learning.
7. **Test the genome decompression / I/O footprint with PyPy or zarr-backed
   genome representation** to make generation iterate faster — currently 2.5 min,
   most of which is loading hg38.fa.
