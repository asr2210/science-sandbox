# Experiment 013 — paired flanks + asymmetric stratification (NEW BEST 0.166)

## Design
- 15K cCRE-centered (uniform, natural distribution; ~12K dELS)
- 5K CTCF-only (boosted from natural ~570)
- 5K DNase-H3K4me3 (boosted from natural ~370)
- 25K paired flanks (one per positive, ±1.5-3kb, cCRE-overlap-checked)

## Result — NEW BEST (mean_r 0.166)
| eval | 005 | 010 | 011 | **013** |
|------|-----|-----|-----|---------|
| 01   |0.156|0.166|0.135|**0.173** |
| 02   |0.157|0.167|0.135|**0.173** |
| 03   |0.168|0.175|0.151|**0.184** |
| 04   |0.150|0.169|0.154|**0.169** |
| 06   |0.187|0.193|0.133|**0.218** |
| 07   |0.174|0.167|0.187|0.177    |
| 10   |0.117|0.146|0.159|0.151    |
| 11   |0.187|0.193|0.133|**0.218** |
| 13   |0.157|0.121|0.158|0.126    |
| mean |0.156|0.158|0.140|**0.166** |

Wins: 9/14 evals new best. K562_r = +0.074 on enhancer evals
(eval_06/11) — by far the best K562 result yet (010 had +0.037, 005
had +0.025). eval_06/11 themselves at 0.218 are absolute new highs.

Losses: eval_10 down slightly (-0.005 vs 011), eval_13 still poor
(0.126).

eval_08 still 0.036, K562_r = -0.01 — universal floor.

## Interpretation
Asymmetric stratification works beautifully:
- Boosting CTCF (5K) and DNH3 (5K) gives those types enough density
  for the model to learn the relevant motifs.
- Preserving natural dELS dominance (~12K dELS in uniform sample)
  keeps the enhancer signal intact — actually IMPROVES it (0.218 vs
  010's 0.193). Possibly because the model now has cleaner
  type-vs-flank discrimination per category.
- K562 jumps to +0.07 on enhancer evals — the model is finally
  learning K562-specific enhancer features, not just averaging.

## Residual gap → eval_13 (0.126)
eval_13 history:
- 002 (random chr22):       0.176 (best)
- 011 (1:1:1:1:1 strat):    0.158 (2nd)
- 005 (50/50 mix):          0.157
- 009 (25K rand + strat):   0.156
- 013 (asym strat + flank): 0.126
- 010 (uniform cCRE+flank): 0.121
- 012 (cCRE+flank+rand):    0.118 (worst)

Things 011 has that 013 lacks: 5K PLS, 5K pELS (in 013 these come from
the 15K uniform sample, ~570 PLS + ~2.4K pELS). PLS is starved in 013.

## Theory update (T12 → T13)
- Asymmetric stratification is the right pattern: keep natural
  dominance of "main type" (dELS for enhancer evals), boost rare
  types (CTCF, DNH3) for their target evals.
- eval_13 may want PLS (promoter) content too.

## Next
014 = expand asymmetric stratification to include PLS boost:
- 10K uniform (~8K dELS + ~2K others)
- 5K CTCF + 5K DNH3 + 5K PLS = 15K boosted
- 25K paired flanks

Trade-off: drops dELS from ~12K to ~8K, may lose some eval_06/11
gain. But should lift eval_13 if PLS hypothesis is right.
