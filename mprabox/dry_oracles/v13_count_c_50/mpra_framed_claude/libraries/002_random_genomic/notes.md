# 002 — Random Genomic Windows (hg38)

**Hypothesis:** Real genomic sequences should outperform uniform random
because they contain naturally-composed motifs and realistic
flanking/spacing. Predicted mean_r jump from 0.15 to 0.30–0.45.

**Design:** 50,000 windows of 200bp sampled uniformly at random across
chr1..22 + chrX + chrY, weighted by chromosome length. N-containing
windows rejected (4.8% rejection rate). 50% reverse-complement for
strand balance. Seed 0.

**Results (mean_r per eval):**
- eval_01: **0.5037** (PRIMARY) — up from 0.1294 (+0.374)
- eval_02/05: 0.5050 — up from 0.1281
- eval_03/12: 0.5198 — up from 0.0771
- eval_04/09: 0.3869 — basically unchanged from 0.3902
- eval_06/11: 0.5047 — up from 0.1189
- eval_07: **0.6369** — up from -0.1416 (+0.778!)
- eval_08: **-0.1364** — down from 0.5795 (-0.716!) ← STARK INVERSION
- eval_10: 0.4551 — up from 0.0938
- eval_13: **0.6212** — up from -0.1470 (+0.768!)
- eval_14: 0.5037
- Mean across 14 evals: **0.458** (up from 0.158)

**What this tells me:**

1. **Massive overall win:** mean_r tripled. Real genomic sequences are
   much better training data than random in aggregate. Confirms basic
   prior.

2. **eval_07 and eval_13 were craving real biology.** They went from
   the worst evals (-0.14 ish) to the BEST evals (+0.62, +0.64). These
   are clearly motif-grounded evaluation sets where compositional
   matching alone is insufficient — you need real motifs in real
   contexts.

3. **eval_08 INVERTED.** This is the most informative single finding
   so far. eval_08 went from +0.58 (high) to -0.14 (negative). Whatever
   eval_08 measures, training on real genome makes the model
   systematically MISpredict it.
   - **Working hypothesis:** eval_08 evaluates *synthetic* / *shuffled*
     / *non-genomic* test sequences. A model trained on uniform random
     sees test sequences as in-distribution and gets correct sign. A
     model trained on genomic learns "natural compositional patterns
     → high activity" and applies the inverse to non-natural test
     sequences. Need to confirm.
   - Alternative: eval_08 evaluates a *negative-set-style* prediction
     (e.g., "is this a control inactive sequence?") where the
     direction of correlation flips between training types.
   - Either way, eval_08 will need careful handling — likely the
     library needs to *include* shuffled/synthetic sequences too.

4. **eval_04/09 are unchanged at 0.39.** These evals are insensitive
   to the random→genomic switch entirely. Their signal is driven by
   something both random and genomic share — probably overall GC
   content variation or sequence complexity. To improve eval_04/09 I
   will need to vary something orthogonal to "is it real genomic vs
   not."

**Theory updates:**

v1 said composition (random) gets ~0.15, motif coverage (genomic) gets
much more. Confirmed for ~10 of 14 evals. But theory v1 missed two
phenomena:

- **Distributional matching is a separate axis from biological
  realism.** eval_08 was *better* with random; the model learned
  something the test set rewarded that genomic training overwrote. So
  "is this sequence in-distribution with the training set?" matters
  independently.
- **Some evals (04/09) are insensitive to both** — they live on a
  composition axis I haven't varied. Need to vary GC explicitly or
  length-fragment structure.

**Theory v2 (refined):**

A good library has FIVE properties:
- (a) Compositional coverage — k-mer distribution matches real
  regulatory DNA (~+0.15 mean_r baseline).
- (b) Motif coverage — diverse TFBSs at realistic densities
  (~+0.30 additional from genomic).
- (c) Multi-cell-type motif coverage (untested).
- (d) Distributional breadth — the *training distribution* should
  include both natural and unnatural sequences so the model doesn't
  collapse to one mode. eval_08 says this matters a lot.
- (e) GC/compositional variety — the library should span the GC range
  to handle eval_04/09 style measures.

**Next:** Experiment 003. The biggest single deficit is eval_08
(-0.14). The biggest free lift would be enriching for active
regulatory regions (ENCODE cCREs) since random genomic is mostly
non-regulatory dark matter. Two competing directions:

- (A) ENCODE cCRE-enriched library — push regulatory signal higher,
  may help eval_07/13 reach ceiling.
- (B) Mixed library: 50% genomic + 50% shuffled/random — recover
  eval_08 without losing eval_07/13. Test the "distributional
  breadth" hypothesis directly.

I'll do (A) first because regulatory enrichment is the largest known
lever in MPRA literature, and reserves cell-type-breadth specifically
for the goal of generalization. Then (B) as a control if eval_08
remains problematic.
