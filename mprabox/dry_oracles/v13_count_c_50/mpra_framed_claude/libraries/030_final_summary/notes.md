# Experiment 030 — final summary of the 30-experiment campaign

## Best library
**013 — 35k multi-chrom-5 random genomic + 15k type-balanced cCRE supplement.**
eval_01 = **0.5765**. Robust across seeds (016 reproduced at 0.5762).
Generated from chr8/chr19/chr21/chr22/chrX with type-balanced cCRE pull
of 3k each {PLS, pELS, dELS, CTCF-only, DNase-H3K4me3} centered on
cCRE midpoints.

## Final theory (v22) — the eval_01 saddle

eval_01 generalization is the sum of three components:

| component | value | source |
|-----------|-------|--------|
| baseline floor (uniform random) | 0.129 | exp 001 |
| dinucleotide composition of library | +0.337 | exp 026 − floor |
| motif grammar in BASE | +0.110 | exp 013 − exp 026 |
| cCRE supplement composition shift | +0.022 | exp 013 − exp 022/017 |
| **TOTAL** | **0.598 nominal / 0.5765 observed** | |

(The decomposition is approximate because shuffle removes some
correlated signal; exp 022/017 prove the supplement contribution is
purely compositional.)

## Levers explored (and their findings)

### What works (proven gains)
- **mc5 over single chrom or all chroms**: chr8/19/21/22/X balances
  composition diversity (exp 007/009).
- **Type-balanced cCRE supplement at 30% of library** (exp 013).
- **Real motif grammar in the BASE** (exp 026): provides +0.110 floor
  via natural cis-regulatory features.
- **Composition shift via cCRE supplement** (exp 017/022): contributes
  +0.022 purely through GC distribution shape — motif content of the
  supplement does NOT contribute.

### What doesn't work (ceiling-confirmation)
- More motif density per window (exp 028 motif-only enrichment): ≈0.
- More motif types — PLS-only (025), PhastCons-only (014): ≈0 or worse.
- CpG over-enrichment within supplement (024): -0.011.
- Narrow high-GC supplement (019, 021): big eval_08 win but eval_01 -0.03.
- Chr19-only supplement (018): -0.014.
- Three-source mix mc5+cCRE+PhastCons (015): -0.001 (interpolative).
- Mild PhastCons sliver in supplement (029): -0.002 (within noise).
- RC augmentation (023): neutral.
- Different seed (016): noise only (σ≈0.001).
- Replacing mc5 base with cCRE-overlap (027): -0.067 (breaks composition).

### Eval class structure
Eight independent eval directions (group structure in skills/):
- **HIGH-GC favoring**: 04, 08 — cCRE pushes up, PhastCons pushes down.
- **LOW-GC favoring**: 07, 13 — PhastCons pushes up, cCRE-only pushes down.
- **eval_01 (primary)**: at the SADDLE — invariant to GC sliding within
  ~0.005 across all near-optimal libraries (013, 022, 023, 025, 028, 029).
- **eval_10**: weak, mostly insensitive.

## Why 013 sits at the saddle
The 0.5765 ceiling is the apex of a 2D trade-off surface
(motif-density × GC-composition). Sliding either dimension shifts gains
between opposite eval classes; eval_01 averages across cell types and
therefore is invariant to the swap. To break this saddle one would need
to ADD signal orthogonal to the trade-off — e.g., truly designed motif
sequences (not natural genomic), synthetic TF binding sites at known
spacings, or new library MATERIAL outside the {genomic, cCRE,
PhastCons} space the campaign sampled.

## Per-eval library recommendations (titrate composition)
| target eval | best library | eval score |
|-------------|--------------|------------|
| eval_01 (primary) | 013 | 0.5765 |
| eval_04 | 013 | 0.5774 |
| eval_07 | 029 (more PhastCons) | 0.6211 |
| eval_08 | 019 (narrow high-GC) | 0.2254 |
| eval_10 | 013 | 0.5087 |
| eval_13 | 029 (more PhastCons) | 0.6038 |

## Recommended single library
**013** for eval_01. To improve eval_07/13 at small eval_08 cost, swap
to **029**. Neither breaks the saddle for eval_01.

## Methodological notes
- Noise floor σ≈0.001 per seed at fixed library (exp 016).
- True library-design effect size needs Δ≥0.005 to be confidently real.
- Shuffle decomposition (exp 026) is the cleanest tool for isolating
  motif vs composition contributions in this regime.
- The cCRE supplement's value is composition, not motifs — surprising
  finding, replicated across 017/022/025.
