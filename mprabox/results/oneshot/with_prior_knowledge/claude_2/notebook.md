# MPRA Library Design Lab Notebook

## Date: 2026-05-27
## Goal
Design a 50,000-sequence (200bp each) MPRA library that maximizes
mean Pearson r across 14 anonymous eval sets, training models
of regulatory grammar generalizable across cell types.

## Initial analysis of prior results

### Best single strategy: `dhs_topic`
- eval_01 = 0.7232 (best across all)
- Mean across 14 evals ≈ 0.769
- Uses DHS elements weighted by NMF topic loadings → upweights
  cell-type-specific accessible regions

### Where dhs_topic loses
- **eval_08**: dhs_topic = 0.7011 (mid-pack). Winners: `synth_oracle` (0.7696),
  `dhs_synth` (0.7523). Strong signal that eval_08 favors sequence diversity
  or synthetic/decoy distributions.
- **eval_13**: dhs_topic = 0.7271. Winners: `dhs_sei` (0.7578),
  `sei_class` (0.7354). SEI chromatin states help.
- **eval_07**: dhs_topic = 0.7398. Winners: `dhs_sei` (0.7640), `dhs_random`
  (0.7615). Suggests broader DHS sampling and chromatin states help.

### Key insight from mixtures
Mixing always degrades eval_01 a bit but can rescue eval_08/13:
- dhs_topic eval_01 = 0.7232, eval_08 = 0.7011
- dhs_synth eval_01 = 0.7174, eval_08 = 0.7523 (+0.05 eval_08, -0.006 eval_01)
- dhs_sei eval_01 = 0.7201, eval_13 = 0.7578 (+0.03 eval_13, -0.003 eval_01)
- 3-way mixtures (dhs_sei_synth, dhs_stratified_sei_synth) hurt eval_01 too much

### `mpra_real` is worst
Real noisy labels < oracle labels. This tells us that **the eval models
are trained via an oracle scoring procedure** — so picking diverse sequences
that span the oracle's feature space is what matters; experimental noise hurts.

### Learning curve insight
At 50k we are far from saturation (dhs_topic goes 0.72 → 0.85 by 300k). Per
sequence ROI is HIGH. Each well-chosen sequence delivers signal; we should
maximize information per sequence, not chase volume.

## Design theory

A good MPRA training library for **general** regulatory grammar should:
1. **Cover diverse regulatory grammar contexts** — promoters, enhancers,
   silencers, insulators, repeats, structural elements.
2. **Span the genomic feature distribution** — GC content, dinucleotide
   composition, motif density.
3. **Cover cell-type-specific and constitutive elements** — avoid bias
   toward a few cell types.
4. **Include negative/random examples** — so the model learns what is NOT
   regulatory (decoy/noise robustness; helps eval_08).
5. **Have low redundancy** — duplicates and near-duplicates waste capacity.

## Strategy plan
Build a multi-component library:
- **Primary (~60-70%)**: DHS-topic-weighted from Meuleman et al 2020.
  This is the best single source — biological regulatory diversity.
- **Chromatin states (~10-15%)**: Stratified across chromatin state classes
  (e.g., active enhancer, polycomb, heterochromatin, CTCF) — helps eval_13.
- **Random synthetic (~10-15%)**: Pure i.i.d {ACGT} sequences for coverage
  of sequence space — helps eval_08.
- **Optional augmentation**: Reverse complements, motif-injection, dinuc shuffles.

Total = 50,000 unique sequences, each exactly 200bp.

## Data sources I'll try to download
1. Meuleman DHS index — https://www.meuleman.org/research/dhsindex/
2. ENCODE cCRE registry — https://screen.encodeproject.org/
3. hg38 reference genome — for extracting sequences
4. ChromHMM 18-state model — for chromatin states
5. JASPAR motifs — for motif-rich augmentation (optional)

## Execution notes
- ONE prepare.py call. NO probing. Design first, evaluate once.
- Will track decisions in this file as I go.

---

## Final design (decided 2026-05-27)

### Composition of 50,000 sequences
| Component | Count | % | Source |
|-----------|------:|--:|--------|
| DHS topic-weighted | 35,000 | 70% | Meuleman 2020, weight = max_NMF_loading * mean_signal |
| ENCODE cCREs class-stratified | 10,000 | 20% | 1,250 each from 8 cCRE classes (PLS, pELS, dELS, CA, CA-CTCF, CA-TF, CA-H3K4me3, TF) |
| Random synthetic | 5,000 | 10% | i.i.d. uniform {A,C,G,T} |

All sequences are 200bp, extracted as ±100 around DHS summit / cCRE midpoint,
from hg38 canonical chromosomes (autosomes + X + Y, excluding ALT/random/M).
N-containing windows rejected; duplicates pruned.

### Reasoning for each component

**DHS topic-weighted (70%)** — the proven best single source. Prior dhs_topic
baseline achieved 0.7232 on eval_01 (best single). Sampling weighted by
`mean_signal * max_topic_loading` upweights:
- Strong DHS signal (`mean_signal`) — high-quality regulatory elements
- High cell-type-specific loading (`max_load`) — distinctive cell-type programs
I deliberately did NOT stratify equally across topics, because the prior
`dhs_stratified` baseline (equal counts per topic) underperformed
`dhs_topic` at 50k (0.7055 vs 0.7232). Stratification helps at small
library sizes but hurts at 50k by forcing inclusion of low-quality
elements from over-represented topics.

**cCREs class-stratified (20%)** — adds functional class diversity that
the topic weighting may under-sample. Specifically:
- 1,250 PLS (promoter-like) — proximal promoter grammar
- 1,250 CA-CTCF — CTCF insulator grammar (often a "boundary" function
  not the focus of DHS NMF topics)
- 1,250 CA-H3K4me3 — H3K4me3-marked accessible regions
- 1,250 each of pELS, dELS, CA, CA-TF, TF — broad enhancer/TF grammar
This is intended to provide stronger coverage of CTCF and promoter grammar.

**Random synthetic (10%)** — pure i.i.d. {ACGT}. Prior data shows:
- synth_oracle achieves eval_08 = 0.7696 (vs dhs_topic = 0.7011)
- dhs_synth (50/50 mix) achieves eval_08 = 0.7523
- 10% synth should give ~0.005-0.01 eval_08 gain at <0.002 eval_01 cost
Provides sequence-space coverage; teaches model what "non-biological"
sequences look like; helps unusual / decoy-style eval sets.

### Components I considered but EXCLUDED

- **SEI chromatin state regions** — would help eval_13 (dhs_sei +0.03 over
  dhs_topic). Excluded because (a) requires downloading SEI annotation
  files I haven't tested, (b) my cCREs partially fill the chromatin-state
  niche, (c) added complexity for marginal expected gain.
- **Random genomic windows (non-DHS)** — would add heterochromatin/intron
  diversity. Excluded because the oracle's labels on these regions are
  uncertain, and dhs_random (which has lots of low-activity windows)
  underperformed dhs_topic.
- **Dinucleotide-shuffled DHS** — would create context-matched "negatives".
  Excluded because mpra_real (real noisy labels) underperformed
  mpra_oracle, suggesting the system prefers cleaner, more informative
  examples over diversity-for-diversity's-sake.
- **Reverse complements of DHS** — would double data with no new info.
  Models typically learn strand-invariance; this just inflates count.
- **JASPAR motif-injected sequences** — would force motif coverage, but
  motifs are already richly present in DHS regions; risk of motif-grammar
  over-fitting outweighs benefit.
- **Mouse / cross-species regulatory regions** — orthogonal but the
  evaluation is human cell types (K562, HepG2, SK-N-SH), so cross-species
  signal could be misleading.

### Risks / What I would try next
- If I had a second shot, I would:
  1. Compare my 70/20/10 mix vs pure dhs_topic in a held-out probe
  2. Test adding 5-10% SEI chromatin-state regions for eval_13
  3. Try 5% dinuc-shuffled DHS as context-matched "low activity" anchors
  4. Try LASSO-based subset selection: use the oracle to score a larger
     candidate pool, then pick a 50k subset that maximizes diversity in
     embedding space (e.g., DNABERT embeddings) — this would beat any
     hand-tuned mixture
- Main risk: the cCREs (20%) overlap substantially with DHS regions (since
  cCREs are derived from DHS), so the marginal information added may be
  smaller than expected. If true, my library is effectively ~90% DHS-like
  + 10% synth, which is similar to dhs_synth (eval_01 = 0.7174). That
  would put me slightly behind pure dhs_topic on eval_01 but possibly
  ahead on overall mean.
- Backup safety: 70% strong DHS backbone keeps me close to dhs_topic
  performance even if cCREs and synth add little.

### Verification (post-generation)
- 50,000 lines: ✅
- All 200 chars: ✅
- Only {A,C,G,T}: ✅
- All 50,000 unique: ✅
- GC content mean ≈ 0.499, SD ≈ 0.107: ✅ (consistent with mixed regulatory + synthetic)
