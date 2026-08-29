# 020 — Multi-window CpGi (extending windowing to second source)

**Hypothesis:** If multi-window helps cCRE, it should help CpGi too.

**Design:** Apply 5-window augmentation to CpGi (1k unique × 5 offsets).
Same exp 019 base elsewhere.

**Results vs exp 019 (best, mean=0.5467):**
- eval_01:    0.5787 (+0.0001)
- eval_04/09: 0.5665 (+0.0007)
- eval_07:    0.6168 (-0.0005)
- eval_08:    0.1743 (-0.0004)
- eval_13:    0.5968 (-0.0005)
- eval_10:    0.5140 (+0.0002)
- Mean:       **0.5468** ← **NEW BEST** (+0.0001 — within noise?)

**Findings:**

Multi-window CpGi gave a barely-measurable improvement (+0.0001).
Tiny. CpGi doesn't benefit much from windowing because:
- CpG islands are inherently positionally well-defined (200bp+ in
  size, dense CpG dinucleotides distributed throughout)
- The signal is compositional (high GC), not motif-grammar — windowing
  doesn't change the compositional signature much
- cCRE windowing helped because TFBSs ARE positionally localized;
  shifting reveals different motif arrangements

**Critical concern:** Improvements are now in 4th decimal. Need to check
seed noise — are these real lifts, or seed variance?

**Plan exp 021:** Run current best library generator with seed=1 to
estimate seed variance. If variance > 0.002, all recent fine-tuning
is within noise and I need bigger swings.
