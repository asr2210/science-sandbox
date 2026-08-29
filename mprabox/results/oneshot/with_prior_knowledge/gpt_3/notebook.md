# Lab Notebook

## Initial read: 2026-05-27

The objective is to design a 50,000 sequence MPRA training library, each sequence 200 bp, for learning general regulatory grammar across cell types rather than maximizing activity in K562, HepG2, or SK-N-SH specifically. The evaluator is one-shot: I must not inspect or modify `prepare.py`, and I may run it exactly once after the design is finalized.

The prior result table is highly informative. At 50k, DHS-topic sampling is the strongest overall starting point, with `dhs_sei` close behind and mixtures with random synthetic sequences helping some eval sets while hurting others. Fully random synthetic sequences are not useless: they do well on eval_08 and reach respectable general performance, which suggests the model benefits from broad sequence-space coverage and not only annotated functional sequence. However, DHS-derived sequence is consistently better on most evals, implying natural genomic k-mer composition and real motif syntax matter at this training size.

I do not have the DHS, SEI, or MPRA pools. Since this run must be self-contained and one-shot, my working theory is that the best feasible design is a hybrid that approximates what the strongest baselines provide: natural-like regulatory backgrounds, broad motif-family coverage, controlled negative/background variation, and explicit perturbation series that make motif grammar learnable from only 50k examples. I will avoid making the library specific to the three measured cell lines by including ubiquitous and lineage-diverse transcription factor motifs, promoter-like sequences, enhancer-like sequences, insulator-like CTCF sequences, low-complexity/repeat-like genomic contexts, and nonfunctional random/genomic-null sequences.

Key design constraints I am adopting:

- Diversity should cover GC from very AT-rich to CpG-rich, because regulatory models often confound motif effects with background composition if the library is narrow.
- Motif grammar should include single motifs, motif clusters, paired motifs with varied spacing/orientation, promoter architectures, and mutated/ablated controls.
- The library should include both functional-looking and nonfunctional-looking sequences. Prior random sequence performance indicates broad negatives/noise are useful, but too much random sequence likely reduces biological relevance.
- Exact duplicates should be avoided; near-duplicates are acceptable only in deliberate perturbation families where the label contrast teaches motif effects.

Plan: create `library/generate.py` that deterministically emits 50,000 sequences. The main components will be synthetic regulatory grammar families rather than downloaded data, because downloading and processing a full DHS-like corpus would be fragile and time-consuming for a one-shot run, and I need a reproducible artifact in the repo. The generator will use motif consensus/IUPAC patterns from broad TF families, sampled into variable genomic backgrounds, plus designed motif-pair and mutation controls.

## Generator design

I implemented a deterministic generator with five strata:

1. 19,000 enhancer-like sequences. These use genomic-like first-order backgrounds with varied GC/CpG behavior, then embed one to eight motifs sampled from broad TF families. About half contain a deliberate paired motif template with varied spacing and orientation, because cooperative motif syntax is a central regulatory grammar feature.
2. 9,000 promoter-like sequences. These are enriched for CpG/GC backgrounds and use rough core/promoter-proximal grammar: TATA, INR, DPE, BRE, CCAAT, GC boxes, ETS, and E-boxes around a jittered pseudo-TSS.
3. 5,000 architectural/insulator-like sequences. These emphasize CTCF, YY1, RFX, REST-like motifs, SP1, and ETS on balanced-to-GC backgrounds.
4. 8,000 perturbation-family sequences. Each family produces paired motif variants: intact pair, mutated left motif, mutated right motif, and spacing/orientation perturbation. These are meant to teach causal motif dependence with close local controls.
5. 9,000 null/background sequences. These include uniform random DNA, genomic-like backgrounds, repeat/microsatellite-like tracts, and simple low-complexity inserts. This preserves the lesson from the prior synthetic baseline that broad coverage of inactive or unusual sequence space can improve some eval sets.

The motif list intentionally spans ubiquitous factors and many tissue/pathway families: SP/KLF, ETS, AP-1, CREB, E-box, NF-Y, NRF1, YY1, CTCF, RFX, REST-like sequence, GATA, FOXA, HNF4, CEBP, RUNX, SPI/PU.1, IRF/ISRE, NF-kB, STAT, SMAD, TEAD, MEF2, SOX, POU, p53, HIF, EGR, and homeodomain motifs. This is not cell-line-specific to K562/HepG2/SK-N-SH; those cell types will see familiar motifs, but so should many other regulatory contexts.

The main risk is that synthetic consensus motifs may be too clean compared with natural DHS sequence. To compensate, the generator uses degenerate IUPAC motifs, reverse complements, motif mutations, motif spacing jitter, broad background GC variation, CpG suppression/boosting, and repeat-like sequence. I expect this to underperform a true DHS-topic sample on natural eval sets but potentially improve robustness on evals where synthetic diversity matters.

First validation run exposed a repeat-generation edge case: for dinucleotide units with only five copies, the maximum possible tract length could be shorter than the requested 12 bp minimum. I fixed this by making the lower bound no larger than the actual maximum tract length. This is a generator correctness fix, not a design change.

The successful generation run wrote exactly 50,000 unique sequences. Independent validation found zero bad lines: every line is 200 bp and contains only A/C/G/T. The generated GC distribution is intentionally broad: about 2,945 sequences below 30% GC, 7,530 from 30-40%, 12,174 from 40-50%, 14,342 from 50-60%, 10,302 from 60-70%, and 2,707 above 70%. This spread is deliberate because the prior results suggest a narrow functional-only library is not ideal, and real regulatory sequence spans both AT-rich distal enhancers and CpG-rich promoter contexts.

I also added a top-level `generate.py` wrapper that calls `library/generate.py`, because the written instructions ask for `generate.py` while the output belongs under `library/`.

## Final pre-submission decision

I am proceeding with the synthetic hybrid design rather than attempting a late download of DHS/SEI data. The reason is pragmatic: prior baselines show DHS-topic sampling is strong, but reproducing the exact Meuleman DHS topic-weighted pool without the provided precomputed data would require downloading large genomic resources and recreating topic metadata under time and reliability uncertainty. A brittle partial DHS approximation could easily be worse than a carefully controlled synthetic design. The current library is internally consistent, reproducible, broad in background composition, and encodes the motif and spacing grammars I most want a 50k training set to teach.

If I had another shot, I would try to combine this design with a real natural-sequence component: sample 20-30k windows from a downloaded cCRE/DHS/ENCODE registry across many biosamples, then reserve 20-30k for the controlled motif perturbation and null families here. I would also replace consensus motifs with sampled PWMs from JASPAR/HOCOMOCO to make motif instances less idealized.

## Final evaluation result

The one allowed `prepare.py` call completed in 641.1 seconds and wrote `library/result.json`. Mean Pearson r by eval set was:

- eval_01: 0.6187
- eval_02: 0.6985
- eval_03: 0.6666
- eval_04: 0.6810
- eval_05: 0.6180
- eval_06: 0.6994
- eval_07: 0.5823
- eval_08: 0.6373
- eval_09: 0.7357
- eval_10: 0.6663
- eval_11: 0.6081
- eval_12: 0.5740
- eval_13: 0.5874
- eval_14: 0.6994

The unweighted average across the 14 eval means is 0.64805. This did not beat the prior DHS-derived or random-synthetic 50k baselines. The most likely explanation is that natural sequence distribution matters more than my motif-grammar hypothesis at this size: the synthetic library likely over-represents clean motif consensus instances and under-represents natural local syntax, weak motifs, evolutionary sequence context, and annotation-derived hard negatives. The outcome supports using real DHS/cCRE sequence as the backbone and synthetic perturbation as an augmentation rather than the majority of the library.
