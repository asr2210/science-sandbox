# 020 — cCRE 013 with width-filtered (no genomic flank)

## Design
Identical class counts to 013 (10K each PLS, CA-CTCF, CA-TF, CA-H3K4me3
+ 2.5K each pELS, dELS, CA, TF) but draws only from cCREs >=200bp wide.
With the 200bp window centered on midpoint, the extracted 200bp lies
entirely inside the cCRE element — no flanking genomic context.

Width filter retains ~80% of cCREs per class (smallest pool: CA-TF
at 23,185 >=200bp, easily supports the 10K target).

200bp centered on cCRE midpoint (same window placement as 013).

## Results (mean over 3 seeds)
- eval_01 = **0.6969** (vs 013 0.7477 = **−0.051**)
- mean across 14 evals = **0.7317** (vs 013 0.7900 = **−0.058**)

## Per-eval delta vs 013
01:−0.051 02:−0.056 03:−0.061 04:−0.038 05:−0.051 06:−0.056 07:−0.079
08:−0.083 09:−0.044 10:−0.062 11:−0.050 12:−0.054 13:−0.077 14:−0.056

**Loses on ALL 14 evals**, by 0.038-0.083. Average −0.058.

## Per-seed eval_01 — bimodal
seed 0: 0.6780  (480s training)
seed 1: 0.7341  (920s training — long tail)
seed 2: 0.6787  (515s training)

SD ≈ 0.032 (vs 013's 0.008 = **4x higher variance**). Two seeds
landed near 0.68, one landed near 013-typical 0.73. The fact that
the long-training seed (920s) hit higher accuracy hints that the
no-flank task is harder to converge on; seeds 0 and 2 may have
stopped at worse optima.

Even taking seed 1 as the best-case (0.7341), 020 is *still* worse
than every cCRE recipe except 010/014. The cCRE element alone is
weaker than cCRE + flank.

## Branching outcome
Pre-experiment branches:
- 020 > 013 → flank is noise (no)
- 020 ≈ 013 → flank neutral (no)
- 020 < 013 → flanking context provides useful signal (yes, strongly)

Result: **020 ≪ 013 by 0.058**. Flanking genomic context contributes
substantially to 013's performance.

## What this updates in the theory

**T17 (new — cCRE-flanking context is informative):** The 200bp
window captures more than the cCRE element itself; the surrounding
genomic context contributes ~0.058 mean correlation. Possible
mechanisms: (a) cCRE boundary calls underestimate the true regulatory
element; (b) flanking sequence carries co-binding TF motifs,
nucleosome positioning signals, or local GC context that completes
the regulatory grammar; (c) the ~50bp average flank gives the model
context to identify which cCRE class the central element belongs to,
acting as an implicit class hint.

**T13 (re-refined):** Functional specificity helps, but element
boundaries are not the unit of function. The cCRE call is a *peak
center*, not a sharp regulatory boundary; the model needs ~100bp
around the peak, not just the peak itself.

**T16 (consistent):** Mixing-based dilution (019) still hurts less
(−0.013) than removing flank (−0.058). The atlas mixing penalty
is small compared to the context loss penalty.

**T8 (refined):** Rare-class upweighting helps *given that windows
include flank*. The principle is a multiplier on a base recipe, not
a substitute for getting the window right. Strip the context and
the upweighting gain shrinks but doesn't reverse: 020 (0.7317) >
014 rare-only-with-flank (0.7155), so the 4-class rare-only structure
still helps even without flank — but much less than with flank.

## Best library so far
**013 cCRE extreme upweight (10K/2.5K), mean ≈ 0.7900**. Holds,
now reinforced — its margin over alternatives includes the
~0.058 flank-context contribution.

## Process note
Single-seed local mode (3 sequential runs on local GPU). spark06
remains hung — same workaround as 018, 019. Total runtime 1911s.

## Most informative next experiment (021)
Now that we know flank matters (T17), test whether *expanding* the
window beyond 200bp helps further. Use 013's class composition but
extract 400bp windows around midpoint, centre-cropped to 200bp by
the model — wait, model takes 200bp. Better: compare
(a) tightly cropped on cCRE peak summit (off-center extraction) vs
(b) 013 default (midpoint).

Alternative: keep the 200bp budget but *off-center* the extraction
so the cCRE is in a random position within the window (rather than
always centered). This tests whether positional bias matters: a model
trained on always-centered cCREs may overfit to position; off-center
training data may force position-invariant feature learning that
generalizes better.

Going with off-center variant (021): same 013 class counts, same
cCREs, but extract 200bp such that the cCRE midpoint is at a
uniformly random position within ±50bp of window center. Tests
positional invariance.
