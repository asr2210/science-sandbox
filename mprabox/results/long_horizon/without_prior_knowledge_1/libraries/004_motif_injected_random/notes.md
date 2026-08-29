# 004_motif_injected_random — notes

## Design
50K x 200 bp. Each sequence: uniform-random ACGT background. Insert
N motifs (N uniform on {1,2,3,4,5}). Each motif: PWM sampled uniformly
from JASPAR 2024 CORE non-redundant (2,346 motifs); one binding-site
instance sampled by drawing from each PWM column; placed at random
non-overlapping position; 50/50 forward/reverse strand.
Mean GC = 0.494, sd = 0.037.

## Hypothesis
Per exp 003 reading: "the cCRE gain is motif-driven." Predicted:
this library would beat random on motif-rewarding evals (07, 13) and
roughly match cCRE on those, while staying near-random on eval_08.

## Result vs. previous

| eval | rand   | cCRE   | shuf   | **motif** | Δ(motif−rand) | Δ(motif−cCRE) |
|------|--------|--------|--------|-----------|---------------|---------------|
| 01   | 0.6954 | 0.7133 | 0.6500 | 0.6861    | -0.009        | -0.027        |
| 02   | 0.7848 | 0.8046 | 0.7343 | 0.7754    | -0.009        | -0.029        |
| 03   | 0.7612 | 0.7870 | 0.7169 | 0.7503    | -0.011        | -0.037        |
| 04   | 0.7494 | 0.7733 | 0.6833 | 0.7408    | -0.009        | -0.033        |
| 05   | 0.6951 | 0.7133 | 0.6498 | 0.6856    | -0.010        | -0.028        |
| 06   | 0.7853 | 0.8048 | 0.7365 | 0.7759    | -0.009        | -0.029        |
| 07   | 0.6684 | 0.7452 | 0.6675 | 0.6636    | **-0.005**    | -0.082        |
| 08   | 0.7841 | 0.6380 | 0.6430 | 0.7679    | -0.016        | **+0.130**    |
| 09   | 0.8115 | 0.8385 | 0.7392 | 0.8029    | -0.009        | -0.036        |
| 10   | 0.7564 | 0.7635 | 0.7107 | 0.7565    | +0.000        | -0.007        |
| 11   | 0.6833 | 0.7010 | 0.6408 | 0.6743    | -0.009        | -0.027        |
| 12   | 0.6553 | 0.6757 | 0.6168 | 0.6454    | -0.010        | -0.030        |
| 13   | 0.6584 | 0.7422 | 0.6880 | 0.6460    | **-0.012**    | -0.096        |
| 14   | 0.7851 | 0.8046 | 0.7342 | 0.7760    | -0.009        | -0.029        |

Mean across 14 evals: rand 0.738, cCRE 0.748, shuf 0.687, **motif 0.732**.

## Interpretation

**Motif insertion failed to recover the cCRE gain on motif-rewarding
evals.** This falsifies my reading of exp 003. The predictions were:
- "motif insertion ≈ cCRE on eval_07" → reality: motif 0.664 vs cCRE 0.745. **NO.**
- "motif insertion ≈ cCRE on eval_13" → reality: motif 0.646 vs cCRE 0.742. **NO.**
- "motif insertion ≈ random on eval_08" → reality: motif 0.768 vs random 0.784. **roughly.**

Most evals: motif-injected is essentially identical to (slightly worse
than) uniform random. The motifs are providing essentially no useful
training signal.

**Most striking single number:** eval_07 went random=0.668 → cCRE=0.745
(+0.077 motif gain), but motif-injection→0.664 (no gain at all). The
cCRE gain on eval_07 is therefore NOT from "motifs anywhere" — it's
from motifs in some specific context that random placement doesn't
provide.

Possible causes:
1. **JASPAR pool too broad.** I sampled uniformly from all 2,346 motifs.
   Most TFs are not expressed in K562/HepG2/SKNSH. So the model is
   trained on lots of "motifs" that have no causal effect on activity
   — the labels are not correlated with the inserted motifs.
2. **Random placement destroys syntax.** Real regulatory regions have
   motifs in specific spacings and combinations. Random placement
   creates "wrong" combinations that don't encode any function.
3. **Sampled instances are too central / too consensus.** Each
   instance is drawn from the PWM, giving on-average a strong consensus
   site. Real binding sites vary in affinity — and reduced-affinity
   sites carry information about gradient.
4. **Density mismatch.** Real cCREs may have different motif densities.

Eval_08 partially recovered (vs cCRE) because the background is
uniform-random — confirming the eval_08 signature is composition-
uniform-rewarding.

## What this changes (theory update)

I'm rolling back the strong claim that "the cCRE gain is purely
motif-driven." More accurate:

> The cCRE gain depends on motifs IN CONTEXT. Naked PWM-instance
> insertion into random backgrounds does not transfer. What's needed is
> some combination of (a) cell-type-relevant motif identity, (b) real
> co-occurrence / spacing patterns, (c) realistic binding-site
> affinity distribution, or (d) something else that genomic regions
> have but motif insertion doesn't.

The wide-composition vs narrow-composition story still holds (motif
library uses uniform composition and recovers eval_08). The
"motifs alone are sufficient" reading does not hold.

## Next experiment

Two strong candidates:
1. **Mixture: 25K cCRE + 25K uniform random.** Practical: tests
   whether the strengths additively combine (cCRE motifs on 07/13,
   random composition on eval_08). Should beat both pure libraries
   if mixtures are the right strategy.
2. **JASPAR-restricted motif insertion: only TFs expressed in
   K562/HepG2/SKNSH.** Diagnostic: tests whether it was really
   "wrong motifs" that killed exp 004. Requires expression data.

Going with (1) — mixture — first. Higher-impact, simpler, and a
necessary step toward a strong library regardless of why exp 004
failed. Then circle back to disambiguating exp 004's failure mode.
