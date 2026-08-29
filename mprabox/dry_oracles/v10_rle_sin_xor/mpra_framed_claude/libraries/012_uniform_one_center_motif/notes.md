# 012 — random uniform + ONE consensus motif at FIXED center position

## Design
50k random uniform 200bp. Insert exactly one JASPAR consensus motif (sampled uniformly from 870 vertebrate motifs, length 6-20) at fixed center position (start = (200-L)//2). GC=0.497.

## Result
- eval_01 mean_r = **0.5191** (vs random uniform 0.5177; first non-noise gain!)
- K562 r = 0.9934 (kept high)
- HepG2 r = 0.5685 (up from 0.557 — biggest gain)
- SK-N-SH r = -0.005

## Reading
First experiment to BEAT random uniform — barely. The HepG2 gain (+0.011) is the source. K562 unchanged.

**Hypothesis:** The eval may train its model on data with fixed-position motifs (like a STARR-seq or MPRA construct where motifs land at a fixed location relative to the promoter). Random-position motifs (exp 005, 006) didn't help, but FIXED-position motifs do, slightly.

Or simpler: the model finds it easier to learn motif-importance when the motif is always at the same position. Random-position motifs add noise to position-aware features.

## Implication
Try more variations of fixed-structure designs:
- Fixed center + flanking N-spacer (rigid construct)
- 2-3 consensus motifs at fixed positions (cassettes)
- HepG2/liver-specific motif subset at center
