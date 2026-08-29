# 010 — top cell-type DNase peaks (K562 / HepG2 / SK-N-SH)

## Method
50k = 16.7k top-signal K562 + 16.7k top-signal HepG2 + 16.7k top-signal
SK-N-SH ENCODE DNase narrowPeaks, 200bp centered on each peak summit.

## Results (eval_01)
mean_r=-0.0039, K562=-0.0121, HepG2=+0.0037, SKNSH=-0.0032

## Surprise
K562_r went NEGATIVE (-0.012). Reproducible across many evals (02, 05,
06, 11, 14 all show K562 ~-0.011).

## Hypothesis for negative K562
- Top K562 DHS peaks are dominated by TSS-proximal regions and
  promoters. In MPRA assays (which measure enhancer activity above
  a minimal promoter), native promoter sequences often score LOW
  because they don't add transcription beyond the minimal promoter.
- The K562-trained MPRA model likely predicts these as low-activity,
  but a "ground-truth" reference may have predicted them as high
  because they're chromatin-accessible. The mismatch produces
  negative correlation.

## Implications
- "Open chromatin" ≠ "MPRA-active". The right active sequences are
  likely DISTAL enhancers (dELS), not promoters.
- Don't pick top-signal peaks — they're over-enriched for promoters.
  Random or stratified sampling may work better.

## Next
- Exp 011: dELS-only (distal enhancer-like) + random GENOMIC 200bp
  windows as null (not shuffled). Tests both "distal-only beats
  promoter-mixed" and "real genomic null beats shuffled".
