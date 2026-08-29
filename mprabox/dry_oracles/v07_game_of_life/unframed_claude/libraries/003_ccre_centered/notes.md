# 003_ccre_centered

## Hypothesis
Curated ENCODE candidate cis-regulatory elements (cCREs: dELS, pELS, PLS, CTCF) should outperform both random and random-genomic if the eval rewards biological regulatory signal.

## Method
- Loaded 1,063,878 cCREs from ENCODE hg38 BED file (mix of dELS/pELS/PLS/CTCF-bound).
- For each sampled cCRE, took 200bp centered on the cCRE midpoint, extracted from the corresponding chromosome fasta.
- N=50,000, seed 42, rejected anything not pure ACGT.

## Result
- **eval_01 mean_r = 0.3929** (K562=0.6050, HepG2=0.4284, SKNSH=0.1455)
- Virtually identical to chr22 random tiles (0.3928).
- Both biological libraries lose by ~0.005 to random uniform (0.3981).

## Interpretation
Real curated regulatory elements give **no advantage** over random genomic DNA, and a slight disadvantage relative to uniform random. This strongly rules out:
- "Biological motifs matter" hypothesis
- "Enhancer signal increases r" hypothesis
- "Library should resemble real regulatory grammar"

Strong evidence the metric is dominated by library-level base composition / dinucleotide statistics. Random uniform (50% GC) wins because real DNA is AT-rich (~41% GC).

## Next
Test the variance/composition hypothesis directly with bimodal GC (004) and isolated GC sweeps. Also check whether mean GC alone or within-library variance is what matters.
