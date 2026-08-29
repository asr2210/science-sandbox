# MPRA one-shot notebook

## Initial reading

The task is to design a single 50,000-sequence MPRA training library. Each sequence must be exactly 200 bp and contain only A, C, G, and T. The evaluation is anonymous across 14 sets and can be called only once, so I am treating it as a final wet-lab submission rather than a tuning loop.

The provided baseline table is the main local evidence. At 50k, DHS-topic sampling is strongest overall for the listed eval sets, especially on eval_01, eval_02, eval_03, eval_05, eval_06, eval_09, eval_11, eval_12, and eval_14. Mixtures with synthetic random sequence improve eval_08 substantially, and mixtures with SEI-like chromatin states help eval_07/eval_13. This suggests the hidden benchmark rewards natural regulatory sequence distribution strongly, but also has some components where broader sequence-space coverage matters.

## Design theory

A compact MPRA training library should maximize information about regulatory grammar rather than only maximize activity. I want the library to cover:

- Native enhancer/promoter sequence contexts: real grammar, realistic GC/CpG/repeat structure, motif spacing, and local dependencies.
- Broad regulatory programs: promoter-like CpG-rich regions, distal enhancer-like regions, insulators/CTCF, immune/stress, developmental TF programs, liver/neural/hematopoietic examples, and inactive/background sequence.
- Controlled synthetic perturbations: motif combinations, spacing/orientation variants, motif copy number, weak/strong motif variants, and GC-matched nulls. These should help a model separate motif grammar from genomic confounders.
- Distributional negatives: random genomic windows and dinucleotide-preserving shuffled sequences to prevent the model from only learning open-chromatin priors.

Given the baseline evidence, the core should remain natural regulatory sequence. I will not make a pure synthetic or pure MPRA-prior library. A conservative target mix is roughly 70-80% public natural regulatory/genomic sequence and 20-30% synthetic/perturbed sequence. If public cCRE/DHS data can be downloaded quickly, I will sample from it. If not, the fallback is a synthetic regulatory grammar library with realistic GC and motif families.

## Constraints and data hygiene

The no-peek rule forbids reading any other run or prior experiment artifacts. I will only use files in this run directory and public references downloaded into `data/`. I will not inspect `prepare.py` further or call it until final evaluation.

## Data chosen

I found public SCREEN Registry V4 GRCh38 cCRE subtype BED files and downloaded:

- `GRCh38-cCREs.PLS.bed`: promoter-like signatures.
- `GRCh38-cCREs.pELS.bed`: proximal enhancer-like signatures.
- `GRCh38-cCREs.dELS.bed`: distal enhancer-like signatures.
- `GRCh38-cCREs.CA-CTCF.bed`: CTCF-associated accessible elements.
- `GRCh38-cCREs.CA.bed`: other candidate accessible elements.

This is a reasonable public substitute for the DHS/topic strategy in the baseline because it provides many accessible/regulatory elements across cell types and element classes. I am also downloading hg38 so the generator can extract the true 200 bp genomic windows around sampled elements.

The planned library composition is:

- 32,000 cCRE-centered native windows, weighted toward enhancer-like and promoter-like elements.
- 6,000 nearby jittered cCRE windows, to expose boundary and flanking-context variation rather than only exact cCRE centers.
- 4,000 random genomic background windows from canonical chromosomes, filtered for N and extreme GC.
- 4,000 dinucleotide-preserving or mononucleotide-preserving shuffles of cCRE windows as hard negatives with similar base composition.
- 4,000 synthetic motif grammar sequences covering common regulatory families and motif combinations.

This keeps about 76% natural regulatory sequence, 8% natural background, 8% shuffled controls, and 8% synthetic grammar. The composition deliberately stays close to the strongest baseline signal while adding coverage for eval sets where random/synthetic mixtures helped.

## Implementation details

I wrote `library/generate.py` with a fixed random seed (`20260629`) so the submitted sequence file is reproducible from the downloaded references.

The final quotas are:

- Native cCRE-centered windows: 15,000 dELS, 6,000 pELS, 5,000 PLS, 3,000 CA-CTCF, and 3,000 CA.
- Jittered cCRE windows: 2,500 dELS, 1,200 pELS, 800 PLS, 800 CA-CTCF, and 700 CA, with centers offset up to +/-180 bp before extracting the 200 bp window.
- Random genomic background: 4,000 windows sampled by chromosome length from canonical chromosomes.
- Shuffled controls: 4,000 mononucleotide shuffles of accepted cCRE windows.
- Synthetic grammar: 4,000 motif-bearing sequences.

For natural windows, I extract 200 bp from hg38 around the cCRE center, randomly reverse complement about half, and reject any sequence with non-ACGT bases, GC outside 0.20-0.82, or an 18 bp homopolymer. These filters are intentionally mild: the goal is to remove ambiguous/low-complexity artifacts without erasing real promoter CpG-rich sequence or AT-rich enhancers.

The synthetic component uses common regulatory motif families: SP1/KLF, AP-1, CREB, E-box, ETS, GATA, FOXA, HNF, NFY, NF-kB, IRF, STAT, CTCF, SOX, POU, MEF2, TATA, RUNX, TEAD, SMAD, and CEBP. I grouped them into promoter, housekeeping, enhancer, immune, liver, neural, insulator, developmental, and minimal-promoter grammars. Motifs are placed with varied spacing, orientation, copy number, and GC-matched backgrounds. This is not meant to dominate the library; it is a small designed perturbation panel to help learn grammar variables that may be underrepresented in raw genomic sampling.

## Pre-evaluation validation

I ran `python library/generate.py`, which wrote `library/sequences.txt`.

Validation results before the final evaluation call:

- Number of lines: 50,000.
- Unique sequences: 50,000.
- Bad lengths: 0.
- Bad characters: 0.
- Observed line length set: only 200.
- GC range: 0.20 to 0.82, mean 0.482.

At this point the library is ready for the one allowed evaluation.

## Final evaluation

I ran the one allowed final command:

`python prepare.py library/sequences.txt`

The evaluation completed in 920.7 seconds and wrote `library/result.json`.

Final mean_r scores:

| eval | mean_r | K562 | HepG2 | SK-N-SH |
|---|---:|---:|---:|---:|
| eval_01 | 0.7253 | 0.7204 | 0.7222 | 0.7332 |
| eval_02 | 0.8174 | 0.8137 | 0.8096 | 0.8289 |
| eval_03 | 0.8008 | 0.8000 | 0.7907 | 0.8117 |
| eval_04 | 0.7758 | 0.7755 | 0.7727 | 0.7790 |
| eval_05 | 0.7252 | 0.7193 | 0.7227 | 0.7336 |
| eval_06 | 0.8182 | 0.8145 | 0.8103 | 0.8299 |
| eval_07 | 0.7530 | 0.7551 | 0.7469 | 0.7571 |
| eval_08 | 0.6934 | 0.7033 | 0.6803 | 0.6966 |
| eval_09 | 0.8398 | 0.8390 | 0.8370 | 0.8434 |
| eval_10 | 0.7769 | 0.7887 | 0.7608 | 0.7810 |
| eval_11 | 0.7127 | 0.7085 | 0.7106 | 0.7189 |
| eval_12 | 0.6883 | 0.6898 | 0.6828 | 0.6922 |
| eval_13 | 0.7515 | 0.7508 | 0.7389 | 0.7647 |
| eval_14 | 0.8174 | 0.8138 | 0.8098 | 0.8287 |

The average of the 14 reported mean_r values is 0.7640. The lowest eval mean is eval_12 at 0.6883 and the highest is eval_09 at 0.8398.

Compared with the provided 50k baselines, this design improves over `dhs_topic` on eval_01 (0.7253 vs 0.7232), eval_02 (0.8174 vs 0.8138), eval_03 (0.8008 vs 0.7933), eval_05 (0.7252 vs 0.7230), eval_06 (0.8182 vs 0.8136), eval_11 (0.7127 vs 0.7098), eval_12 (0.6883 vs 0.6822), and eval_14 (0.8174 vs 0.8144). It is weaker on eval_04, eval_07, eval_08, eval_09, eval_10, and eval_13. The major miss is eval_08, where the baseline table suggests much larger random/synthetic fractions help; I only allocated 8% synthetic and 8% shuffled controls.

## What I would try next

If I had another shot, I would test a slightly larger synthetic/random component, probably 20-25%, while retaining a cCRE-heavy core. I would also add true dinucleotide-preserving shuffles and explicit GC/length/motif-density stratification buckets. The cCRE-based approach appears strong for promoter/enhancer-like evals, but the lower eval_08 result suggests some hidden sets reward broader sequence-space or negative-control coverage more than I allowed.
