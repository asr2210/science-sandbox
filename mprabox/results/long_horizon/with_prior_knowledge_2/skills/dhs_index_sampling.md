# Skill: sampling sequences from the DHS Index

## What this does
Draws 200bp sequences centered on Meuleman 2020 DHS Index summits, with
arbitrary per-element weights. Validated end-to-end in experiment 001:
mean_signal-weighted sampling reproduces the published `dhs_topic`
baseline (eval_01 ≈ 0.7242 vs 0.7232).

## Reference files (under `data/`)
- `data/genome/hg38.2bit` (797 MB) — UCSC, https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.2bit
- `data/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz` (87 MB) —
  Zenodo, https://zenodo.org/records/3838751/files/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz

## DHS Index columns (TSV, gzipped, ~3.59M rows after filtering)
| col | name | type | notes |
|-----|------|------|-------|
| 1 | seqname | str | filter to chr1–22, chrX, chrY (keeps ~3.59M) |
| 2 | start | int | element start |
| 3 | end | int | element end |
| 4 | identifier | str | "1.10011" style |
| 5 | mean_signal | float | mean DNase signal across 733 biosamples; quartiles 0.22 / 0.41 / 0.76; tail to ~428 |
| 6 | numsamples | int | number of biosamples in which element is called accessible (1–733); use this for breadth-weighting |
| 7 | summit | int | best place to center a 200bp window |
| 8 | core_start | int | high-confidence core |
| 9 | core_end | int | high-confidence core |
| 10 | component | str | dominant NMF topic (16 categorical labels: "Tissue invariant", "Cardiac", "Neural", ...) |

**Note**: the public TSV does NOT carry the per-element 16-component
NMF loadings — only the dominant `component` label. To approximate
`dhs_topic` weighting, weight by `mean_signal`. To stratify across
topics, sample equal numbers from each `component` value.

## Recipe — weighted sampling that hits exactly N valid 200bp ACGT seqs
1. Stream the gzipped TSV; keep `(chrom_idx, summit, weight_column)` in
   numpy arrays (~50–100 MB RAM for 3.59M rows).
2. Open hg38 with `twobitreader.TwoBitFile(path)`; cache `len(tb[c])`
   per chrom so you can drop windows that fall off the chromosome.
3. For each seed:
   - `rng = np.random.default_rng(seed)`
   - `probs = weights / weights.sum()`
   - Oversample by ~20% (e.g. `n_request = N + 10_000`) with
     `rng.choice(n_total, size=n_request, replace=False, p=probs)` —
     this is fast enough on 3.59M elements (a few seconds).
   - Iterate, drop windows with N or off-chromosome edges, append to
     a list; pull more in batches of ~10k until length >= N.
   - Truncate to exactly N.
4. Validation: each `sequences_*.txt` must have exactly 50,000 lines,
   each exactly 200 ACGT chars. Quick check:
   `awk '{n++; if(length($0)!=200||$0!~/^[ACGT]+$/) bad++} END{print n, bad}' file`

## Joint distribution of mean_signal × numsamples (validated 2026-04-24)
- `mean_signal`: highly skewed; quartiles 0.22 / 0.41 / 0.76; tail to 428.
- `numsamples`: also highly skewed; median = 3; p90=43, p99=365, max=733.
- log(ms) vs log(ns) Pearson r = 0.635 — correlated but not equivalent.
  Each axis weights different elements; combining adds independent signal.
- 17% of all DHS elements are in the "Primitive / embryonic" component
  (low mean_signal, low numsamples). The smallest component is "Stromal A"
  (1.6% of elements) but it has *median ns = 116* — these are the
  housekeeping / broadly-accessible elements.
- "Tissue invariant" component (4.4%) has high *signal* (median 0.874) but
  low *numsamples* (median 2). The name is misleading — it's named for
  enrichment of tissue-invariant TFs, not for cross-tissue accessibility.

## Sampling-strategy results (this run)
- `mean_signal`-weighted only (001): eval_01=0.7242, cross-14=0.7511.
  Per-seed eval_01 std ~ 0.025.
- `numsamples`-weighted only (002): eval_01=0.7152, cross-14=0.7534.
  Per-seed eval_01 std ~ 0.003 (very tight — the high-ns tail is small,
  so seeds collide on the same elements).
- 50/50 mixture (003): eval_01=0.7327, cross-14=0.7735. **Beats both
  pure forms on 13/14 evals.** Key insight: the two axes are
  COMPLEMENTARY, not substitutes.

## Things that bit me
- 6.1s per seed for the sampling loop. 3 seeds + load = ~21s total.
  Don't bother parallelising.
- Some elements appear in multiple seeds because high-weight DHS sites
  are likely to be drawn by all three seeds (~1700 overlap between
  seeds 0 and 1 at mean_signal-weighting). This is *intended* —
  sampling is without replacement *within* a seed, not across seeds.
- The `meuleman.org/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz`
  URL 404s. Use Zenodo: `https://zenodo.org/records/3838751/files/`.
