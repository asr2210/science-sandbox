# Lab notebook

## Initial read
I read instructions.md. The task is a one-shot MPRA library design: exactly 50,000 DNA sequences, each 200 bp, aimed at learning general regulatory grammar across cell types. The strongest prior 50k baseline is DHS topic-weighted, with DHS+SEI and DHS+synthetic close behind. Pure synthetic helps eval_08 but underperforms broadly, so I should keep the library dominated by real regulatory genomic DNA and reserve a minority for synthetic perturbations/diversity.

Important constraints: I must not inspect or modify prepare.py, and I may call it exactly once at the end. I will document design decisions here as I make them.

## Working theory
A high-value 50k training library should cover common regulatory grammars with enough natural genomic context to expose motif syntax, spacing, GC/CpG structure, repeats, and weak/background sequence. The prior results suggest broad accessible regulatory DNA is a better size-efficient training distribution than curated MPRA constructs or chromatin-state regions alone. However, a small fraction of synthetic or shuffled sequences can widen coverage and help learn negative/low-activity sequence space.

I will use ENCODE SCREEN cCREs as an accessible, downloadable proxy for the unavailable DHS pool. I will stratify across promoter-like, enhancer-like, CTCF/TF, and accessible-only classes so the library is not tissue-specific and not only strong enhancers/promoters. I will add controlled synthetic motif grammar and dinucleotide-shuffled genomic controls rather than i.i.d. random only.

## Data source decision
I will use ENCODE SCREEN V4 human cCREs in GRCh38 as my primary regulatory source. The SCREEN download page reports 2,348,854 human cCREs across 1,888 cell/tissue types, which fits the goal of broad regulatory grammar rather than specificity to K562, HepG2, or SK-N-SH. I will not use assay labels or cell-line-specific signal; only the cCRE class and genomic sequence.

Planned allocation: mostly real cCRE sequence, balanced enough to prevent enhancer dominance. Tentative classes: PLS, pELS, dELS, CA-CTCF, CA-H3K4me3, CA-TF, CA, TF-only, plus a smaller set of dinucleotide-shuffled cCRE controls and synthetic motif-grammar sequences. This follows the prior evidence that DHS-like real sequence is strongest, while random/synthetic diversity helps a hard eval set but hurts broad performance if overused.

## Implementation adjustment
The UCSC command-line utilities available at the standard linux.x86_64 path are not executable on this aarch64 machine. I will use Python packages instead where possible. This affects extraction mechanics only, not the design: cCRE intervals from UCSC, hg38 sequence, deterministic sampling, then validation.

## Generated library
I generated `library/sequences.txt` with 50000 unique 200 bp sequences. Real cCRE selected by class: {'PLS': 2488, 'pELS': 8500, 'dELS': 11000, 'CTCF': 4896, 'H3K4me3': 1216, 'DNase': 0}. Extra components: {'dinuc_markov_shuffled': 4000, 'motif_synthetic': 2500, 'composition_random': 15400}. GC mean/min/max: 0.4972/0.22/0.82. The final ordering is shuffled so components are not block-structured.

## First generation check and adjustment
The first generation pass produced a valid 50,000-sequence file, but only about 28,100 sequences were real cCRE windows because the sampled UCSC track exposed mostly PLS, pELS, dELS, CTCF, and H3K4me3 labels; my planned DNase-only bucket was absent. That would force 15,400 composition-random fallbacks, which is too much given the prior evidence that real regulatory sequence is stronger at 50k.

I adjusted the generator to remove the unavailable DNase bucket, increase dELS/pELS representation, and query 330 deterministic tiles rather than 230. The revised intent is roughly 42,000 real cCRE windows plus 4,000 dinucleotide/Markov-shuffled controls, 2,500 motif-grammar synthetic sequences, and only a small random-composition filler if class shortages remain.

## Generated library
I generated `library/sequences.txt` with 50000 unique 200 bp sequences. Real cCRE selected by class: {'PLS': 3500, 'pELS': 10000, 'dELS': 22000, 'CTCF': 5000, 'H3K4me3': 1500}. Extra components: {'dinuc_markov_shuffled': 4000, 'motif_synthetic': 2500, 'composition_random': 1500}. GC mean/min/max: 0.4959/0.22/0.82. The final ordering is shuffled so components are not block-structured.

## Final evaluation
I ran the single permitted command `python3 prepare.py library/sequences.txt` after local validation. It evaluated 50,000 sequences against 14 anonymous test sets and wrote `library/result.json`.

Final mean_r by eval set: eval_01 0.7275, eval_02 0.8231, eval_03 0.8030, eval_04 0.7867, eval_05 0.7273, eval_06 0.8236, eval_07 0.7501, eval_08 0.7190, eval_09 0.8574, eval_10 0.7952, eval_11 0.7152, eval_12 0.6892, eval_13 0.7423, eval_14 0.8235. The unweighted average across the 14 mean_r values is 0.7702. This improves over the prior dhs_topic baseline on eval_01, eval_02, eval_03, eval_05, eval_06, eval_08, eval_10, eval_11, eval_12, eval_13, and eval_14, while it is slightly below dhs_topic on eval_04 and eval_09 and below dhs_sei on eval_07.

If I had another shot, I would try to recover more all-biosample DHS-like sequence rather than relying on cCREs alone, and I would test a smaller synthetic/random fraction because the final design still used 8,000 non-native sequences. I would also look for a newer ARM-friendly way to consume SCREEN V4 downloads directly, which may provide richer CA-only classes than the UCSC cCRE mirror used here.
