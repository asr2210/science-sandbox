# Lab Notebook

## Initial interpretation
The task is to design a one-shot 50,000 sequence, 200 bp MPRA training library for learning general regulatory grammar, not merely maximizing activity in K562, HepG2, or SK-N-SH. The evaluation is opaque and must be treated as a wet-lab assay; I will not inspect prepare.py. I will use the known structure of regulatory DNA and ML training-set design principles: cover endogenous regulatory examples, negatives/backgrounds, motif grammar perturbations, GC/repeat/low-complexity variation, and synthetic motif combinations that expose nonlinear interactions.

Key constraint: the final file must contain exactly 50,000 unique-looking 200 bp A/C/G/T sequences. I will bias toward diversity and interpretability rather than overfitting to three cell types.

## Literature and data notes
I searched for MPRA library design and regulatory grammar work. Key ideas I am carrying forward: synthetic libraries have been used to systematically test TF binding site copy number, spacing, combination, and order; larger regulatory sequence studies combine known motifs, genomic contexts, and synthetic random sequence backgrounds; and current motif databases such as JASPAR provide broad TF binding profiles useful for not limiting the design to one tissue. I will use a broad motif vocabulary rather than K562/HepG2/SK-N-SH-specific peak sets.

I attempted to download JASPAR 2024 vertebrate PFMs as an external motif source. If usable, the generator will parse PFMs and sample motif instances from many TF families. If this fails, I will fall back to an embedded consensus motif panel covering the same broad families.

## Generator design
I wrote generate.py as a deterministic sequence generator rather than a static hand-edited sequence file. The library is split into six categories: promoter-like CpG/TATA/Inr/SP1/CCAAT grammar; enhancer-like clustered multi-motif modules; spacing/copy-number/orientation syntax series; motif perturbation sequences with partially broken sites; composition controls spanning GC, CpG, AT-patchy, repeats, and palindromes; and a family-balanced motif panel. This is intended to expose a model to both regulatory signal and non-regulatory/background variation.

The generator parses the downloaded JASPAR 2024 vertebrate non-redundant PFM file and filters to motifs 6-24 bp with at least moderate information content. Motifs are grouped into coarse TF families for balanced sampling. I corrected an early family-name mismatch (ETS case and SOX as its own family) before producing the library.

## Additional data-source consideration
I also searched for genome-derived sequence sources. ENCODE SCREEN/cCREs and FANTOM5 enhancers provide broad, multi-cell-type regulatory annotations; EPDnew provides curated human promoters. These are attractive because the objective asks for general regulatory grammar, not only three MPRA cell lines. Full integration would require genomic sequence extraction from hg38 intervals. Given the one-shot constraint and the need to avoid fragile external dependencies in the final generator, I am keeping the primary library synthetic/motif-driven but borrowing the conceptual split: promoters, enhancers, CTCF/TF modules, and composition controls.

## Pre-assay validation
Generation completed with 873 parsed JASPAR motifs across 15 inferred motif families. The final quotas are: 8,500 promoter-like, 10,500 enhancer clusters, 12,000 syntax/copy/spacing series, 7,500 motif perturbations, 6,500 composition controls, and 5,000 family-balanced motif panel sequences. Independent validation showed exactly 50,000 lines, all exactly 200 bp, only A/C/G/T, and zero duplicate sequences. GC spans 0.15-0.85 with mean about 0.525, intentionally broad enough to cover AT-rich enhancers, CpG-rich promoters, and neutral backgrounds.

## Final assay result
I ran the black-box evaluation once after validation. The per-evaluation mean_r values ranged from 0.5724 to 0.7298, with an average mean_r of 0.646321 across the 14 anonymous test sets. Strongest performance was eval_09 (mean_r 0.7298); weakest were eval_13 (0.5724) and eval_12 (0.5727), suggesting that at least some hidden test regimes prefer sequence distributions or grammars underrepresented by this design.

If I had another shot, I would prioritize adding true genome-derived sequence contexts from broad cCRE/FANTOM/promoter annotations, especially matched positive/negative genomic neighborhoods, while retaining the synthetic motif perturbation series. I would also run ablations comparing the six categories to see whether composition controls or high-density motif clusters dilute training signal.
