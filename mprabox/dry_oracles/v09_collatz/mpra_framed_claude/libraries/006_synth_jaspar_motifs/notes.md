# 006_synth_jaspar_motifs

## Design
50,000 fully synthetic 200bp sequences. Each is a random scaffold
(GC 40–55%) with 2–5 JASPAR vertebrate-core TF motifs inserted at
random non-overlapping positions. Motifs sampled from 879 JASPAR
2024 vertebrate PFMs (probabilistic sample, not consensus).

## Hypothesis
If motif identity is the dominant determinant of MPRA activity,
synthetic motif insertion should give HepG2 r > 0.18 (matching
cCREs). If genomic context (flanking sequence, motif grammar,
realistic composition) is required, performance should drop.

## Result vs 001 (random) and 002 (cCRE)
                eval_01  K562    HepG2   SKNSH   eval_08
001 random:     0.2307   0.139   -0.089  0.642   0.089
002 cCRE:       0.3154   0.145   +0.177  0.625   0.076
006 synth:      0.2212   0.140   -0.069  0.593   0.091

Synthetic is WORSE than random baseline!
- K562: 0.140 (ceiling)
- HepG2: -0.069 (about the same as random, NOT cCRE-like)
- SKNSH: 0.593 (LOWER than random 0.642 — synthetic constrained
                 composition reduces signal)

## Interpretation (big result)
**Motif identity alone is not enough.** Even with 2–5 high-quality
JASPAR motifs planted per sequence, the model trained on synthetic
sequences cannot predict HepG2 — same as random sequences.

Synthetic library also LOSES SKNSH signal (0.593 vs 0.642 random),
because the motif-insertion procedure pins composition to a narrower
range (~50% GC + planted motifs), reducing the compositional spread
random sequences have. Composition is genuinely informative for
SKNSH — and constraining composition hurts.

The roughly 0.18 HepG2 lift from natural cCREs is NOT explainable by
motif identity. It must require:
- The natural co-occurrence pattern / grammar of motifs (specific
  spacings, orientations, combinations)
- The realistic flanking composition (not GC-uniform random)
- The specific motif INSTANCES (not PWM-sampled)
- Or some non-motif signal in natural regions

## Theory T4 → T5
- Motif identity is necessary but not sufficient.
- Natural cCREs carry irreducible context information that synthetic
  libraries miss. This is consistent with the regulatory-grammar
  hypothesis: position/spacing/combinations of motifs matter.
- Cross-cell-type generalization needs natural context, not just
  motif content.
- The plateau at 0.32 is set by what natural cCREs provide. To break
  it, must either (a) use higher-quality natural regions (signal
  filter, promoter focus, conserved regions), (b) add data-axis
  diversity that natural cCREs alone lack (e.g. silencer-like
  regions), or (c) accept the plateau as a model-architecture
  limit.

## Next
Experiment 007: promoter-focused dense library. PLS cCREs (~41K
promoter-like elements) — known to be the most cell-type-invariant
regulatory class — sampled 10K regions × 5 tiles. Tests whether the
"most universally regulatory" element class lifts performance above
the cCRE-mixed plateau.
