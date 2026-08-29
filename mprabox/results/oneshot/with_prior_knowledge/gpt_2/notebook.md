# Lab Notebook

## Initial read

- Objective: design a one-shot 50,000 x 200 bp MPRA training library for broad regulatory grammar across cell types, then run prepare.py exactly once.
- Constraint: do not inspect or modify prepare.py. I will treat it as a black-box assay and only call it after finalizing sequences.
- Prior results indicate DHS/topic-weighted genomic regulatory sequence is strongest at 50k, while random synthetic sequence helps some eval sets (notably eval_08) but hurts most others. My starting hypothesis is that a mostly genomic cis-regulatory library with a small synthetic/motif-diversity tail has the best performance-to-size ratio.


## Data acquisition plan

- Chosen primary source: ENCODE SCREEN/Weng Lab GRCh38 cCREs. This is a practical substitute for the unavailable DHS pool because it aggregates candidate regulatory elements across many biosamples and regulatory classes, rather than the three assayed cell lines only.
- Secondary source: UCSC ENCODE TF ChIP clustered sites. These are not a complete regulatory universe, but they enrich for transcription-factor-bound windows and should complement cCREs with motif-dense examples.
- I am downloading hg38 FASTA so I can extract exact 200 bp genomic windows from coordinates. I will filter ambiguous bases and blacklist non-canonical/random contigs.
- Planned composition after seeing prior results: mostly genomic cCRE/TF-bound windows, plus a small synthetic component. I do not want a large random tail because prior dhs_synth lost on most evals even though it helped eval_08.


## Composition decision

- I will make the final library 80% SCREEN cCRE windows, 12% high-confidence ENCODE TF ChIP clusters, 5% motif-spiked synthetic sequences, 2% random genomic background windows, and 1% i.i.d. random DNA.
- Rationale: prior data strongly favors DHS-like genomic regulatory sequence at 50k. A small synthetic/random component is retained to cover motif combinations and sequence-space regions that pure cCRE sampling will miss, but kept small because large synthetic fractions lowered most eval metrics.
- cCRE quota will be class-stratified, not frequency-proportional: dELS largest, then pELS/PLS, with explicit coverage of CA, TF, CTCF, and H3K4me3-associated classes. This should approximate broad regulatory programs without specializing to K562/HepG2/SK-N-SH.
- TFBS quota will be TF-name stratified among high-score/source-count clusters to avoid simply selecting the most abundant factors. This adds motif grammar examples even where the cCRE registry may be sparse.


## First generation QC

- First full generation succeeded: 50,000 unique sequences, all 200 bp and A/C/G/T only.
- GC distribution mean was ~0.491, but there was a small extreme tail down to 2% GC and up to 91.5% GC. Those are likely low-complexity or repeat-adjacent genomic windows, especially near telomeric/centromeric contexts.
- Decision: add conservative sequence QC before final generation: retain 200 bp windows with GC between 18% and 82% and no homopolymer longer than 20. This keeps promoter CpG-rich and AT-rich regulatory windows, but removes pathological sequence that is unlikely to improve a compact training set.


## DHS subset decision

- I found public Meuleman/Weng synthetic-sequence classifier files: 160,000 training DHS-centered 200 bp raw sequences, exactly 10,000 per DHS NMF component, plus validation/test splits. This is the closest downloadable source to the best prior DHS/topic family.
- Final adjustment: make this curated DHS/component set the dominant source. I will sample 42,000 sequences, exactly 2,625 per component, using a weighted-without-replacement score based on component proportion, total DHS signal, and number of biosamples. This approximates topic-upweighted DHS while preserving equal component coverage.
- The remaining 8,000 sequences will be complementary: 4,000 class-balanced cCRE windows, 1,500 high-confidence TF ChIP cluster windows, 1,500 motif-spiked synthetic sequences, 500 random genomic windows, and 500 i.i.d. random sequences.
- This is a deliberate move toward the strongest prior evidence: mostly DHS, but not pure DHS, with a small component for non-DHS/background and synthetic motif combinations.


## Final pre-assay library

- Final hard validation before prepare.py: 50,000 lines, 50,000 unique sequences, zero invalid length/alphabet records.
- Final source blocks in output order: 42,000 DHS/component sequences, 4,000 cCRE windows, 1,500 TFBS windows, 1,500 motif-spiked synthetic sequences, 500 random genomic windows, 500 i.i.d. random sequences.
- Final GC distribution: min 20%, mean ~45.3%, max 82%. This is somewhat AT-shifted because the DHS component set contains many distal/accessibility sequences, but still covers promoter-like GC-rich windows through PLS/cCRE/TFBS classes.
- I considered using cCREs alone, but switched after finding the curated DHS component sequences because the prior result table strongly favors DHS/topic-like designs at 50k. I considered a larger synthetic fraction, but prior synth-heavy mixtures lost on most eval sets; the final synthetic/random fraction is 5% total plus 1% random genomic.

## What I would try next

- If another shot were available, I would compare several DHS sampling schemes without touching prepare.py: pure equal-component DHS, signal/proportion-weighted DHS, and a rare-component-upweighted DHS/cCRE mixture.
- I would also add explicit low-complexity and repeat-mask annotations instead of the current simple GC/homopolymer filter, and test whether promoter/TSS orientation matters for any model class.
- If the full Meuleman DHS index with component loadings were convenient to process, I would sample directly from all ~3M DHSs with topic-proportional weights, since that was the best prior baseline.


## Final assay result

- prepare.py was called exactly once on library/sequences.txt.
- Result: eval_01 mean_r = 0.6982. Mean across the 14 eval mean_r values = 0.7323.
- This did not beat the best prior DHS/topic result on eval_01. The likely reason is that the public 160k DHS component classifier subset is balanced and curated for component classification, not the full DHS topic-weighted sampling distribution used by the top prior baseline. The equal-component design probably improved breadth but lost the topic/signal distribution that the black-box eval rewarded.
- Stronger-than-average points: eval_02/06/14 near 0.789 and eval_09 at 0.7953. Weak points: eval_08 at 0.6516 and eval_12 at 0.6614, consistent with the library still being too genomic-DHS-like for the hardest/background-sensitive eval sets.

