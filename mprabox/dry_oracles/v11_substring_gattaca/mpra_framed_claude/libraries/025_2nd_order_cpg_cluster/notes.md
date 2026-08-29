# 025 2nd-order Markov: CpG island core (CGCG clusters)

50k Markov. 1st-order base from exp 021. 2nd-order overrides:
- P(C | xy=CG) = 0.50 (boost C after CG → CGC)
- P(G | xy=GC) = 0.75 (boost G after GC → GCG)

Realized: GC=0.66 (shifted up from 1st-order's 0.62 due to overrides),
CpG rate=0.23, CGCG count=12/seq.

## Result
- **mean_r = 0.879 (eval_01 = 0.895)** — NEW BEST
- vs 021 (best 1st-order): +0.005 mean, +0.005 eval_01
- SKNSH huge: 0.96 (vs 0.95 in 021)

Cell breakdown (easy evals):
| cell  | 021  | 025  | Δ     |
|-------|------|------|-------|
| K562  | 0.84 | 0.84 | 0     |
| HepG2 | 0.89 | 0.88 | -0.01 |
| SKNSH | 0.95 | 0.96 | +0.01 |

## Takeaway
**Local CpG-island clustering is a usable signal.** The 5-7bp CGCG runs
clustered ~12 times per sequence boosted performance, especially for
SKNSH. Local uniformity rule didn't break because:
- Cluster span (5-7bp) is shorter than CNN receptive field
- Alternating CGCG is structured (not monotonous like polyA)
- ~6% of bases in clusters (low overall fraction)

**Confound:** Realized GC drifted to 0.66 (was 0.62 target). Some of the
gain may be due to higher CpG composition rather than clustering.

## Next
- Stronger 2nd-order overrides to push clustering more
- Or: control by running 1st-order at GC=0.66 to isolate structural
  contribution
