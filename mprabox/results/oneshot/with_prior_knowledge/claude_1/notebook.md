# MPRA Library Design — Lab Notebook

## Setup
- Target: 50,000 sequences × 200 bp, ACGT only
- Goal: train a model of regulatory grammar that generalises across cell types
- One-shot evaluation against 14 anonymous test sets (no iteration)
- Available data: `dhs_index.txt.gz` (3,591,898 DHS elements with Meuleman 2020
  16-component assignments + mean signal + summit), `hg38.fa.gz` reference

## Reading the prior-results table

Top performers at 50k, ranked by eval_01:
1. `dhs_topic` 0.7232 — DHS sampled proportional to NMF topic loadings
2. `dhs_sei`   0.7201 — 50/50 DHS_topic + SEI class-weighted
3. `dhs_synth` 0.7174 — 50/50 DHS_topic + random synth
4. `dhs_random` 0.7089
5. `dhs_stratified` 0.7055

Mean across all 14 evals (rough):
- dhs_topic ~ 0.763
- dhs_sei   ~ 0.759
- dhs_synth ~ 0.759
- synth_oracle ~ 0.722

Observations:
- DHS-derived strategies clearly dominate; synthetic-only is the floor.
- The "best" strategy at every library size from 10k–300k is DHS-based.
- Adding chromatin-state (SEI) or synthetic does NOT beat pure DHS-topic on average.
- However: eval_08 is a clear outlier. dhs_topic gets 0.7011, while
  dhs_synth gets 0.7523 and synth_oracle 0.7696. eval_08 rewards sequence
  diversity beyond what genomic samples provide.
- mpra_real (using noisy experimental labels) loses badly to mpra_oracle —
  signals that label noise is more harmful than coverage gain.

## Theory of a good library

For training a deep regulatory-grammar model, what matters is:
1. **Motif coverage** — the model needs to see most cis-regulatory grammar
   units (TF binding sites and combinations) in informative contexts.
2. **Signal range** — examples spanning low and high activity. Too many
   "active enhancer" examples means the model can't learn what makes
   something inactive.
3. **Sequence diversity** — varied background (GC content, repeats,
   k-mer composition) so the model doesn't overfit to genomic biases.
4. **Cell-type breadth** — for cross-cell-type generalisation we want
   elements from many tissue programs, not just K562/HepG2/SK-N-SH.
5. **Low label noise** — oracle-labelled (by `prepare.py`) so this is
   automatic; nothing for me to fix here.

DHS regions across 16 NMF components naturally cover (1) and (4): they
are functional regulatory elements drawn from 733 biosamples.

To address (2) and (3), some synthetic / non-DHS content is helpful but
expensive (each random seq dilutes the regulatory training signal).

## What I'll build

I cannot reproduce `dhs_topic` exactly because the index gives only the
dominant component per element, not the full 16-loading vector. My
approximation:

  stratified across the 16 components × within-topic weighting by
  mean_signal

This captures the two ideas behind dhs_topic:
- broad coverage of every chromatin program (the "topic" axis)
- preference for elements with stronger signal (a proxy for high
  topic loading — high-loading elements tend to have stronger,
  cell-type-specific accessibility)

Composition plan (final): 50,000 sequences total
- ~45,000 DHS-derived (stratified-topic × signal-weighted)
- ~5,000  synthetic random (i.i.d. uniform A/C/G/T)

Rationale for the synthetic 10%:
- eval_08 gives synth-heavy strategies a +0.05 boost over pure DHS.
- 50/50 dhs+synth costs ~0.006 on eval_01 vs. pure DHS.
- A 10% synthetic floor should capture most of the eval_08 upside
  with negligible cost elsewhere. Better than nothing in expectation.

Sequence extraction:
- 200bp window centred on the DHS summit (or core mid-point if summit
  missing). DHS cores are usually <200bp so we will extend outward
  symmetrically.
- Reject anything containing N's.
- All sequences ACGT-uppercase.

## What I am NOT doing and why

- **Downloading SEI** — SEI components require running their model on
  the genome (~3M regions). Not feasible in one shot, and the prior
  results show SEI mixed with DHS does *not* beat pure DHS-topic.
- **Reverse-complement augmentation in the library itself** — the model
  presumably handles strand internally; including the reverse complement
  of a sequence as a separate library member would waste capacity.
- **TF-motif-planted synthetics** — interesting but unvalidated; pure
  random was the empirically-validated booster in prior results.
- **mpra_oracle source** — only 0.6643 on eval_01; published MPRA
  libraries are over-concentrated and provide weaker training signal
  than DHS.

## Result

Final library: 50,000 unique 200bp sequences, ACGT only, GC mean 0.458.
Sampled without replacement from the 3.59M Meuleman DHS pool, weighted by
sqrt(mean_signal). 200bp windows centred on each DHS summit; 2 N-containing
windows rejected and resampled.

Overall **mean_r across 14 evals = 0.7882** (prior best `dhs_topic` ≈ 0.763,
synth_oracle floor ≈ 0.722).

Per-eval (mine vs prior best dhs_topic 50k):

| eval | mine   | dhs_topic | Δ      |
|------|--------|-----------|--------|
| 01   | 0.7476 | 0.7232    | +0.024 |
| 02   | 0.8410 | 0.8138    | +0.027 |
| 03   | 0.8269 | 0.7933    | +0.034 |
| 04   | 0.7805 | 0.7904    | -0.010 |
| 05   | 0.7475 | 0.7230    | +0.025 |
| 06   | 0.8411 | 0.8136    | +0.028 |
| 07   | 0.7949 | 0.7398    | +0.055 |
| 08   | 0.7146 | 0.7011    | +0.014 |
| 09   | 0.8465 | 0.8601    | -0.014 |
| 10   | 0.8175 | 0.7904    | +0.027 |
| 11   | 0.7342 | 0.7098    | +0.024 |
| 12   | 0.7104 | 0.6822    | +0.028 |
| 13   | 0.7914 | 0.7271    | +0.064 |
| 14   | 0.8409 | 0.8144    | +0.027 |

Beat dhs_topic on 12/14 evals; small losses on eval_04 and eval_09.
Largest gains on eval_13 (+0.064) and eval_07 (+0.055), which were the
two weakest spots for dhs_topic.

My read: the prior `dhs_topic` baseline likely allocates samples per topic
(small topics over-represented in proportional-to-loading sampling).
Sampling globally weighted by sqrt(signal) — letting natural topic
prevalence determine the marginal — gives broader coverage of strong
elements without forcing equal-per-topic representation. The eval_08
gain is modest, consistent with eval_08 preferring some non-genomic
sequence diversity (not added here).

## What I'd try next (if I had another shot)

1. Pull actual Meuleman NMF loading matrix and reproduce true topic
   weighting (vs. my dominant-component approximation).
2. Sweep DHS / synth mixture ratio in 5% steps to find the optimum.
3. Add ENCODE cCRE PLS (promoter-like) sequences as a small distinct
   bucket — promoters tend to be very motif-rich and may complement DHS.
4. Add a small fraction of dinucleotide-shuffled DHS sequences as
   biologically-plausible negatives.
