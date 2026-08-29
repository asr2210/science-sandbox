# Exp 007: TFBS canonical motif injection (mapping A=0,C=1,G=2,T=3)

## What
50k random uniform backgrounds + K ~ U{0,15} canonical TFBS motifs per sequence.
Library: TATA, CCAAT, Sp1, CRE, E-box, NR half-site, AP-1, and reverse complements.

## Result (eval_01)
- mean = 0.4197 (vs random 0.4192) — essentially tied
- K562 = 0.5930, HepG2 = 0.6230, SKNSH = 0.0429

## Interpretation
TFBS-canonical motifs neither helped nor hurt. Either:
1. Alphabet mapping wrong (motifs appear as ~random 8-mers)
2. Both models give similar predictions for random and motif-rich sequences, so no
   stretch effect on correlation
3. Models don't care strongly about these specific motifs

Better than exp 006 (random 8-mers, 0.4038), so canonical motifs are slightly less
hurtful than random 8-mers — weak signal that some motifs are recognized.

## Implications
- Direct motif insertion at small K doesn't move the needle.
- Try STRATIFIED stretch — half random + half heavily-motif-packed, to see if
  mean shift between strata inflates the Pearson r.
