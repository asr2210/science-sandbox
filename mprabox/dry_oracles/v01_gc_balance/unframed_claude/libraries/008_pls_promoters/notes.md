# 008_pls_promoters

50k 200bp windows from PLS (promoter-like signature) cCREs only (~40k regions).

## Result
DISASTER:
eval_01: 0.0879 (vs 0.6840 cCRE-all)
eval_07: -0.0965 (NEGATIVE!)
eval_13: -0.0789 (NEGATIVE!)

## Interpretation
PLS regions are CpG islands → ~65%+ GC. Same GC-rich crash we saw in exp 002.
Promoter sequences are TOO GC-rich; their composition is outside the natural
genomic distribution that the scorer's predictor was tuned for.

This confirms the GC content effect is dominating. Promoter regions are
biologically the most regulatory, but compositionally they're the worst input
to the scorer.

For best performance, need sequences with REGULATORY motifs but in ~40-50% GC
distribution. dELS (distal enhancers) likely satisfy this — they're not
CpG islands but still regulatory-active.

## Next
- 009: shuffled chr22 (test motif vs composition)
- 010: dELS only (distal enhancers, less GC-rich)
- 011: K562-specific accessible regions
