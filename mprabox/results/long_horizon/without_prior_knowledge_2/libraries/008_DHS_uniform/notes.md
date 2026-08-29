# 008 — DHS Index uniform sample

## Design
50K DHS Index elements (Meuleman 2020, ~3.59M total on main chroms),
uniform random sample, 200bp centered on summit. Sister-comparison
to 002 (uniform cCRE sample). Tests annotation-source effect.

## Results (mean over 3 seeds)
- eval_01 = **0.6914** (vs 002 cCRE uniform 0.7263 = **−0.035**)
- mean across 14 evals ≈ **0.7297** (vs 002 ≈ 0.7665, **−0.037**)

## Per-eval delta vs 002 (cCRE uniform)
01:−0.035 02:−0.038 03:−0.039 04:−0.031 05:−0.035 06:−0.038 07:−0.037
08:−0.051 09:−0.034 10:−0.040 11:−0.034 12:−0.033 13:−0.033 14:−0.038

**ALL 14 evals worse**, by 0.031–0.051. Strong, uniform signal that
cCREs are the better source for this ML task. eval_08 still the worst
eval, even with a different annotation source.

## Across-seed
eval_01: 0.6969 / 0.6996 / 0.6776 → SD ≈ 0.012. Lower variance than
002 (SD≈0.025) — DHS uniform is more homogeneous across seeds.

## Comparison to expected branching
Pre-experiment hypothesis was three-way:
- 008 ≈ 002 → annotation source neutral
- 008 > 006 → DHS captures more diversity
- 008 < 002 → cCREs better-curated

Result: **008 ≪ 002**, the third branch and the worst case. DHS Index
adds nothing useful relative to ENCODE cCREs and in fact hurts
performance significantly.

## Why might DHS underperform cCRE?
1. **Annotation noise**: DHS sites include any DNase peak; cCREs apply
   ChIP-seq filtering (H3K4me3, H3K27ac, CTCF) for regulatory class
   assignment, which selects cleaner regulatory elements.
2. **Width / centering**: DHS summits are sharp DNase signal peaks;
   cCRE midpoints span a curated regulatory window. 200bp centered on
   a sharp summit may be more redundant (same flanking context) than
   200bp centered on cCRE midpoints which span varied regulatory shapes.
3. **Distribution skew**: 3.59M DHS vs 2.35M cCRE; uniform sampling of
   the larger pool dilutes "interesting" regulatory regions with weak
   peaks called only in 1-2 samples.

## What this updates in the theory
**T7 (new):** Annotation curation matters more than annotation breadth.
The cCRE pipeline (ENCODE V4) selects regulatory elements with stronger
multi-mark support; uniform DHS sampling is biased toward rare/weak
DHS sites because most DHS calls come from few samples. For an MPRA
training library, **regulatory-class-curated annotations beat
broad-coverage annotations** at equal sequence count.

**T6 (refined):** "Real regulatory content" is not monolithic — the
quality of the regulatory annotation is a first-order driver. cCREs >
DHS Index uniformly across evals.

## Best library so far
006 stratified, mean ≈ 0.775. Unchanged.

## Most informative next experiment (009)
**Filter DHS by signal strength.** Take only DHS sites with mean_signal
in the top quartile and numsamples ≥ 5 — i.e., DHS sites that are
strong AND consistently called. This isolates whether the curation
effect (T7) is real: if filtered-DHS ≈ 002 cCRE, then strength of
peak/curation is the active variable. If filtered-DHS still < cCRE,
then the cCRE annotation pipeline is doing more than peak-filtering
(class-based regulatory typing helps independently).
