# Skill: ENCODE cCRE-based sequence sampling

How to draw 200 bp regulatory-element-centered sequences from the ENCODE
SCREEN candidate cis-Regulatory Element (cCRE) Registry.

## Reference data
- BED file: `data/cCRE/GRCh38-cCREs.bed` (V3, ~1.06M elements, GRCh38).
- Source: `https://downloads.wenglab.org/V3/GRCh38-cCREs.bed`
- Genome: `data/genome/hg38.2bit` from UCSC. Read with `twobitreader`.

## BED columns (V3)
1. chrom
2. start (0-based)
3. end
4. EH38D... internal ID
5. EH38E... accession
6. cCRE class string, e.g. `dELS,CTCF-bound`. The first comma-separated
   token is the **primary class**; "CTCF-bound" is a qualifier appended
   when the element overlaps a CTCF ChIP-seq peak.

## Primary class counts (V3)
| class            | count   |
|------------------|---------|
| dELS             | 789,200 |
| pELS             | 172,027 |
| PLS              |  40,891 |
| CTCF-only        |  35,839 |
| DNase-H3K4me3    |  25,921 |

(Counts include CTCF-bound and unbound subsets, lumped under primary class.)

## Window extraction
- 200 bp window centered on cCRE midpoint: `mid = (start + end) // 2`,
  `start = mid - 100`, `end = mid + 100`.
- Reject windows that exceed chromosome bounds (rare; <0.01% of cCREs).
- Upper-case the extracted sequence; replace residual `N` bases (also rare,
  comes from soft-masked or unmapped regions in 2bit) with random `ACGT`
  using the same RNG used for sampling.

## Sampling patterns
- **class-balanced**: sample N/5 from each of the 5 primary classes.
  Used in `libraries/001_ccre_class_balanced/`.
- **class-proportional**: sample uniformly across all cCREs (dominated by
  dELS, ~75% of pool). Equivalent in spirit to dhs_random/sei_random.
- **CTCF-bound only**: filter to elements whose class string ends with
  `,CTCF-bound`. Useful as a chromatin-architecture-focused subset.

## Reproducibility
- Use a per-seed `random.Random(seed)` for both the index shuffle and the
  N-substitution. Do NOT use `numpy.random.default_rng` unless you also
  pin numpy version explicitly.
- Sample WITHOUT replacement within a class (track `used` set keyed by
  `(chrom, midpoint)`).

## Performance
- Loading + sampling 50K sequences across 3 seeds takes ~17 s on this box.
- I/O on the 2bit file is the bottleneck; the cCRE BED parses in <2 s.

## Reference template
See `libraries/001_ccre_class_balanced/generate.py` for the canonical
implementation pattern.

## Empirical priors from experiments in this repo
- **001 (10K-per-class, no random)** → eval_01 = 0.7262, eval_08 = 0.6849.
  Class-balanced cCRE matches/marginally beats dhs_topic on most evals but
  loses on eval_08 (which rewards sequence-space diversity).
- **002 (8K-per-class + 10K iid random)** → eval_01 = 0.7278 (still up),
  eval_08 = 0.7149 (+0.030 vs 001). Mixed-source 80/20 is Pareto-improving.
  iid random helps eval_08 specifically (likely distribution-matching to
  synthetic eval set).
- **003 (8K-per-class + 10K random genomic windows, non-cCRE)** → eval_01
  = 0.7301 (new best), eval_07 + 0.015, eval_13 + 0.021, but eval_08
  collapsed back to 0.6755. Random genomic ≠ iid random — they help
  disjoint eval sets.
- **004 (40K cCRE + 5K iid + 5K human genomic)** → eval_01 = 0.7395, mean 14
  = 0.7825. Two random sources at half-mass synergize 2–3× over linear
  additive prediction. Pareto-best over 001/002/003 on every eval.
- **005 (35K cCRE + 5K iid + 5K human-gen + 5K mono-shuffled)** → eval_01 =
  0.7343 (down). Mono-shuffled is informationally redundant with iid (no
  structure either way). 3rd source on the SAME axis hurts because cCRE
  backbone gets diluted.
- **006 (35K cCRE + 5K iid + 5K human-gen + 5K mouse-gen)** → eval_01 =
  0.7468, mean 14 = 0.7908. NEW BEST on every eval. Cross-species genomic
  is a real third orthogonal axis. Per-seed spread tightened from ~0.06
  to 0.02 — mouse component reduces seed variance.
- Per-seed eval_01 spread WAS ~0.04–0.07 at 50K libraries with 3 seeds (pre-006).
  Adding mouse genomic dropped it to ~0.02. A ±0.005 difference between
  two experiments without the mouse component is within seed noise; WITH
  it, ±0.005 is borderline interpretable.

## RNG hygiene for multi-source generators
When a generate.py mixes cCRE sampling with random generation (or any other
generative source), use **distinct random.Random streams** per source:

```python
ccre_rng   = random.Random(seed * 2 + 1)
random_rng = random.Random(seed * 2 + 2)
shuffle_rng = random.Random(seed * 2 + 3)
```

This way, swapping the random component (e.g., iid → genomic-window) for an
ablation experiment doesn't perturb the cCRE sample, so the comparison is
clean.

For 4-source generators (e.g. 004/005/006), we used the convention
`seed * 4 + offset` with offsets 11, 13, 17, 19, 23, 29 reserved for
iid / human-genomic / final-shuffle / mouse-genomic / shuffled-genomic /
shuffler. Pick offsets so that previously-tested experiments use the same
stream when you want byte-identical replays.

## Cross-species sampling (mouse mm10)
- Mouse genome: `data/genome/mm10.2bit` (~700 MB, 21 canonical chroms).
- Use chroms `chr1–chr19, chrX` (skip chrY for parity with human chrX-only).
- Same `extract_window` logic; no cCRE-overlap filter (mouse cCREs aren't
  in our annotation set; mouse intergenic ≠ human cCRE by definition).
- Empirical (006): adding 5K mouse non-cCRE windows to a library that
  already contains 5K iid + 5K human non-cCRE lifted eval_01 by +0.0125
  AND tightened per-seed spread by 3× vs the human-only equivalent.
