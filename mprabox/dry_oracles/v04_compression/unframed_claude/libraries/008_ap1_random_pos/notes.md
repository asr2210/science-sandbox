# Experiment 008 — AP-1 at random position

## Result
eval_01: 0.261 (vs 0.278 in exp 002 fixed-pos AP-1; vs 0.328 in exp 006 motif-pool random-pos).

## Interpretation
**Random positioning did NOT save AP-1.** Having TGAGTCA in EVERY sequence — at any position — hurts more than having it at a fixed center.

This rejects my earlier interpretation that fixed-position variance loss was the mechanism. The real mechanism:
- Every seq containing the same 7-mer creates a shared signal across the library.
- The 14 evals likely compute Pearson r where shared signals across all seqs either compress prediction dynamic range or decorrelate scoring models.
- Pool of 8 motifs (exp 006) didn't hurt because no single 7-mer appears in all seqs; each motif appears in ~6250/50000 = 12.5% of seqs.

## Theory update → T5
The scorer's Pearson r is hurt by ANY feature shared by all or most seqs. Random uniform DNA wins because it has minimum library-wide systematic features — only natural noise. The best paths forward:

1. **Lateral**: keep diversity high; if adding motifs, use very large pools so each individual motif is in <5% of seqs.
2. **Sub-baseline structure**: try to make the library statistics EVEN MORE uniform than i.i.d. — e.g., perfectly balanced per-column nt counts, or balanced k-mer counts.
3. **Constructive perturbation**: very hard without knowing the target. But e.g., features that correlate strongly with whatever the target measures.

## Next
Exp 009: Perfect per-column balance — each of 200 columns has exactly 12500 A, C, G, T. Removes the binomial sampling noise that i.i.d. random uniform has. If it helps even slightly, sub-uniform strategies are worth pursuing.
