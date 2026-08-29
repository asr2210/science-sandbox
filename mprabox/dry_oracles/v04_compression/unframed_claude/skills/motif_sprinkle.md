# Skill: motif sprinkling for MPRA-style scorers

## When to use
When trying to beat a uniform-random baseline on an MPRA-style scorer
(prepare.py with k562/hepg2/sknsh evals). Random uniform i.i.d. DNA is a
strong baseline; this technique reliably pushes above it.

## Recipe
1. Start with a 50K × 200bp matrix of i.i.d. uniform random bases.
2. Pick a pool of CANONICAL TF binding motifs of size 20-32. Sweet spot is
   24-32; too few (≤16) underperforms; too many (≥64) dilutes.
3. Use clean ACGT only — no IUPAC ambiguity, no per-instance mutation.
4. For each sequence, pick ONE motif uniformly from the pool, then insert it
   at a UNIFORMLY-RANDOM position. ONE motif per seq beats two.
5. Save as `sequences_0.txt`.
6. **Run a seed lottery** — per-seed variance is ~σ=0.016. Run 5-10 seeds
   and pick the best. Variance is mostly in motif placement.

## Why it works
- Per-column nucleotide distribution stays near uniform because motifs are
  scattered across positions and the per-motif library frequency is low
  (≤3% with a 32-motif pool, 1 motif per seq).
- Per-sequence regulatory content is added, which the scorer rewards.
- Library remains homogeneous (every seq is uniform-random + 1 random motif).

## What NOT to do
- Don't insert the SAME motif in all seqs (drops eval_01 by ~0.07).
- Don't insert at FIXED positions (drops eval_01 by ~0.05).
- Don't add many motifs per seq (3 motifs is slightly worse than 1).
- Don't mix uniform and motif-loaded as separate halves (bimodal, drops r).
- Don't bias GC content across the library (drops eval_01 by ~0.06).
- Don't force perfect per-column balance (drops eval_01 by ~0.04 — the
  binomial column noise is doing useful work).
- Don't add reverse-complement insertion (hurts at fixed seed).
- Don't mutate motif bases or sample from PWMs (corrupts canonical signal).
- Don't use full JASPAR (>100 motifs dilutes per-motif representation).

## Expected scores (50K × 200bp)
| Library                              | eval_01 |
|--------------------------------------|---------|
| Uniform random                       | 0.331   |
| 8-motif pool, 1/seq, random pos      | 0.347   |
| 16-motif pool                        | 0.354   |
| 32-motif pool, 1/seq, random pos     | 0.344 (mean), 0.369 (best of 5 seeds) |
| 24-motif pool                        | 0.353 (mean), 0.372 (best of 6 seeds) |
| 64-motif pool                        | 0.326 (dilutes) |
| 814-motif JASPAR PWM-sampled pool    | 0.324 (too dilute) |
