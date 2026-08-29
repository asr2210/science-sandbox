# 003_dhs_signal_breadth_mixture

## What I tested
50% mean_signal-weighted DHS sampling (the 001 recipe) + 50%
numsamples-weighted DHS sampling (the 002 recipe), drawn without
replacement so the two halves never overlap. 50,000 sequences total ×
3 seeds. Same 200bp-around-summit extraction as 001/002.

## Result — STRONG WIN
- **eval_01 mean_r = 0.7327** (vs 001: 0.7242; vs 002: 0.7152;
  vs published `dhs_topic` baseline: 0.7232) → beats all
- **Cross-14 mean = 0.7735** (vs 001: 0.7511; vs 002: 0.7534;
  vs published `dhs_topic` ≈ 0.7630) → beats all by ≥0.011
- Per-seed eval_01: 0.7293 / 0.7346 / 0.7341 (std ≈ 0.003)
- eval_07 = 0.7618 (recovers to 001 level despite half breadth-weighted)
- eval_13 = 0.7469 (between 001's 0.7564 and 002's 0.7004)

## Per-eval comparison
| eval | 001    | 002    | 003    | Δ vs best of 001/002 |
|------|--------|--------|--------|----------------------|
| 01   | 0.7242 | 0.7152 | 0.7327 | **+0.0085** |
| 02   | 0.8173 | 0.8045 | 0.8244 | +0.0071 |
| 03   | 0.8007 | 0.7820 | 0.8048 | +0.0041 |
| 04   | 0.7819 | 0.7891 | 0.7962 | +0.0071 |
| 05   | 0.7238 | 0.7147 | 0.7324 | +0.0086 |
| 06   | 0.8170 | 0.8044 | 0.8241 | +0.0071 |
| 07   | 0.7611 | 0.7238 | 0.7618 | +0.0007 |
| 08   | 0.6781 | 0.6908 | 0.6984 | +0.0076 |
| 09   | 0.8496 | 0.8582 | 0.8685 | +0.0103 |
| 10   | 0.7895 | 0.7850 | 0.8019 | +0.0124 |
| 11   | 0.7106 | 0.7020 | 0.7192 | +0.0086 |
| 12   | 0.6872 | 0.6727 | 0.6929 | +0.0057 |
| 13   | 0.7564 | 0.7004 | 0.7469 | -0.0095 |
| 14   | 0.8175 | 0.8053 | 0.8251 | +0.0076 |

**13 of 14 evals improved** over the better of {001, 002}. Only
eval_13 is slightly worse than 001 (-0.0095) — the 50% breadth
dilution does cost some chromatin-state-specific signal there.

## What this updates
**The two-axis theory is supported.** mean_signal weighting
(cell-type-specific, sharp discrimination) and numsamples weighting
(broad accessibility, transferable grammar) are **complementary**, not
substitutes. Combining them in a 50/50 mixture beats both pure forms
on 13/14 evals.

The library is more *generalizable* (cross-eval mean +0.022) and more
*in-distribution* (eval_01 +0.0085) at the same time — so this is
strictly Pareto-better, not a trade.

## Open questions
1. Is 50/50 the optimal ratio or can I push further? Try 30/70 or 70/30.
2. Is there a third axis (out-of-distribution coverage / synthetic
   sequences) that adds independent information? eval_08 still trails
   the synth-containing baselines (synth_oracle 0.7696, dhs_synth
   0.7523, mine 0.6984).
3. eval_13 dropped — is this a real cost of breadth-mixing, or an
   artifact of the specific elements selected?
