# Lab Notebook

## Initial theory (2026-06-02, before any experiments)

The scorer takes 50,000 sequences of 200bp each and returns scores broken
down by 14 eval sets, with sub-scores `k562_r`, `hepg2_r`, `sknsh_r`.
These cell-line names plus the `_r` suffix strongly suggest the task is
predicting MPRA-style regulatory activity (Pearson r against measured
expression) in:
- K562   = erythroid leukemia
- HepG2  = hepatocellular carcinoma
- SK-N-SH = neuroblastoma

Working hypothesis: each library is treated as a held-out test set; a
pretrained sequence-to-activity model predicts activity for my 50,000
sequences, and the scorer computes some statistic (possibly Pearson r of
predicted activity vs. some target, or mean predicted activity).

If "mean_r" really is Pearson correlation, then constant sequences would
get NaN/zero — so I should test that to verify the metric.

Initial plan (rough):
1. 001 — uniform random baseline (anchor)
2. 002 — GC-rich vs AT-rich (compositional sensitivity)
3. 003 — homopolymer / single-base (extreme composition + low complexity)
4. 004 — known TF motif clusters (K562, HepG2, SK-N-SH specific)
5. 005+ — iterate on whatever signal is strongest

Then I'll let the data drive the next 20+ experiments.

---

## 2026-06-02 — Experiment 001 planning

Goal: establish a random-sequence baseline. This is the null distribution
for "no information about regulatory activity". Any deliberate library
should beat this.

Prediction: low mean_r across all eval sets. If any cell type shows
notably higher random scores, that tells me something about the metric
(e.g., maybe r vs. a target that random sequences happen to satisfy).

Method: uniform i.i.d. nucleotides at each position.

## 2026-06-02 — Experiment 001 result

All eval mean_r in [-0.003, +0.008]. Pure noise floor. Confirms:
- Metric is correlation-like (random ~0).
- Random sequences carry no useful signal.

**Important discovery — duplicate evals:** 01==14, 02==05, 03==12,
04==09, 06==11. So I effectively have 9 distinct evals:
{01,14}, {02,05}, {03,12}, {04,09}, {06,11}, 07, 08, 10, 13.
This is useful — I can use the duplicate pairs as a noise-floor check
when computing tiny effects.

**Updated theory:** scorer presumably computes Pearson r between two
per-sequence quantities derived from my sequences (e.g., model
prediction vs. held-out target prediction, or model prediction vs.
ground-truth measurement function). For uniform-random inputs both
quantities live in a low-variance regime → r ≈ 0. To beat baseline I
need sequences whose two scoring-relevant quantities are predictable
AND span a wide dynamic range.

## 2026-06-02 — Experiment 002 planning

Test compositional sensitivity AND start probing motif effects.
Hypothesis: high-GC content alone may bias scores because regulatory
regions are GC-rich on average. Also include a basic TF-motif library
to see if simple motif insertion alters scores.

Design: split 50k sequences into 5 sub-banks of 10k:
- Bank A: GC=20% (low-complexity AT-rich)
- Bank B: GC=40% (mildly AT)
- Bank C: GC=50% (uniform random — reference)
- Bank D: GC=70% (GC-rich)
- Bank E: GC=85% (very GC-rich)

This is a within-library composition sweep. If the scorer cares about
composition, the r across the union will be non-trivial. If r stays at
zero, composition alone is insufficient.

Caveat: a within-library sweep doesn't isolate which composition is
"best" — it just probes whether composition is a factor. If the result
shows a signal, I'll follow up with single-composition libraries.

---

## 2026-06-02 — Mid-run jumps (exp 003-029 condensed; full per-exp notes in libraries/NNN/notes.md)

Skipping detailed notebook entries — each experiment has its own
`libraries/NNN_*/notes.md` with method, results, lessons, next steps.
Below is the integrated summary that captures the conclusions.

---

## 2026-06-02 — FINAL SUMMARY (after exp 030)

### Best eval_01 score
**exp 012: mean_r = +0.0045** (K562=+0.0089, HepG2=+0.0011, SKNSH=+0.0035)
Library: 25k K562 motif-saturated (12 motifs/seq, GC=65%) + 25k null
(GC=25%, no motifs), seed 501.

### What I tried (30 experiments)
- Random baselines (001, 002 GC sweep)
- Cell-specific motif libraries (005 K562, 006 HepG2, 007 SKNSH)
- Universal saturated motif libraries (008, 014, 020)
- Real ENCODE regulatory sequences (009 cCRE, 010 DHS, 011 dELS, 015
  H3K27ac, 016 shared H3K27ac)
- Tiled / pure-motif designs (013 AP-1 tiles vs poly-A)
- GC contrast extremes (012, 017, 023, 024)
- Hybrid synthetic+real (021, 022, 026)
- Continuous gradients (019)
- Triple-bank designs (004, 025)
- Same-recipe reseeding to estimate variance (027, 028, 029, 030)

### Key findings
1. **eval_01 has high per-library noise (SD ~0.003).** Both exp 005 and
   exp 012 — my top two recipes — dropped from +0.0043/+0.0045 to
   -0.0017/-0.0003 when re-run with new seeds (exp 028-030). The
   "plateau at +0.0045" was the upper tail of ~15 noisy samples around
   0.
2. **Eval duplicates discovered early:** 01==14, 02==05, 03==12, 04==09,
   06==11. Effective 9 distinct eval sets.
3. **Real biology (DHS, cCRE, H3K27ac) usually underperforms synthetic
   motif libraries on eval_01.** Possibly: real sequences include
   promoters that compete with the MPRA minimal promoter, dragging
   model predictions toward "low".
4. **K562 model is the dominant per-cell contributor to eval_01.** Its
   r typically dominates the mean.
5. **K562-specific motifs (GATA1, KLF1, TAL1, NFE2) are essential** for
   K562 signal — universal-motif-only designs (exp 020) BROKE K562 r.
6. **HepG2 model is fragile** — extreme GC contrast (null GC<25) flips
   HepG2 r negative because low-GC null looks "HepG2-typical" to the
   model. Best HepG2 r came from real H3K27ac peaks (exp 015).
7. **SKNSH model is broadly activated** by motif-rich libraries
   regardless of specificity — universal motifs work as well or better
   than SKNSH-specific (NEUROD, POU3F2, homeobox).
8. **Continuous-density gradients fail eval_01 but help eval_08**
   (exp 019: eval_08 mean=+0.0084). Different evals favor different
   library shapes.
9. **Bimodal 50/50 active/null design is what eval_01 rewards.**
10. **Triple-bank hybrids fail** (exp 025: -0.0016) — cross-bank
    pollution destroys per-cell signal more than additive lift gains.

### Per-cell maxima on eval_01 (across all 30 experiments)
- K562 r max: +0.0089 (exp 012, K562 saturated GC=65/25 bimodal)
- HepG2 r max: +0.0069 (exp 015, real H3K27ac peaks dinuc-shuffled)
- SKNSH r max: +0.0074 (exp 024, K562 motifs GC=60/40)
- If achievable simultaneously: mean = +0.0077. But these conditions
  are mutually exclusive in a single homogeneous design AND any single
  observation is dominated by per-seed noise.

### What I'd do with more budget
- Average eval_01 over 20-50 seeds per recipe to find the recipe with
  highest TRUE mean (vs lucky max).
- Try recipes that explicitly minimize per-seed variance, e.g.,
  deterministic motif placement on canonical positions instead of
  random insertion.

### What I'd not bother trying again
- Triple-bank designs (consistently underperform single-focus)
- Extreme GC contrast with null GC<20 (kills HepG2)
- Pure poly-A / homopolymer null (out-of-distribution for models)
- Continuous gradients for eval_01 (gradient hurts, bimodal helps)
