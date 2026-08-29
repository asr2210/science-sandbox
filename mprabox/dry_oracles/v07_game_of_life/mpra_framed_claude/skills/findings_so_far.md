# Empirical findings — v07 run

This file is for findings in the **current** v07 run. Findings from
prior runs (v04) are below as INHERITED HYPOTHESES — they must be
validated in v07 before being treated as load-bearing.

## v07 findings
(to be populated as experiments complete)

| Library | eval_01 | mean_r | Notes |
|---|---|---|---|

## Inherited hypotheses from v04 (UNVERIFIED in v07)
These were observed empirically in v04. The v07 eval sets may differ.
Treat as priors / starting hypotheses only.

- Pure random uniform DNA: eval_01 ≈ 0.31 (composition floor)
- Pure natural genomic windows (chr1-22,X,Y): eval_01 ≈ 0.48
- Pure cCRE-centered: eval_01 ≈ 0.34 (activity-range collapse)
- 50/50 natural + cCRE: eval_01 ≈ 0.49
- Pure synthetic motif insertion in random bg: eval_01 ≈ 0.15
- Natural + cCRE + DHS + mouse (4-way): eval_01 ≈ 0.50 (v04 best)
- eval_08 was always ~0.08-0.11 regardless of library in v04
- K562_r == HepG2_r exactly in v04 (label set may merge them)
- Noise floor in v04: ~0.004 between seeds on same design

## v04 working theory (T3) inherited as starting point
A library is informative iff its sequence distribution **matches the
distribution of plausible regulatory genomes** the eval set is drawn from.
Within that constraint, motif content + activity-range diversity help.
Violating naturalness costs more than added motif density gains.
