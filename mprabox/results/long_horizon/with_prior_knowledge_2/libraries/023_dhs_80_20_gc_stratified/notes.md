# 023_dhs_80_20_gc_stratified

## What I tested
015 with mix ratio shifted from 70/30 to 80/20 under the same GC
stratification. Hypothesis: 022 showed breadth-axis × strat is
anti-synergistic alone; reducing the breadth allocation might help.

Per-bin counts: 8K signal + 2K breadth across 5 bins. **The 2K
breadth-per-bin crossed the 3K stability floor.** Accepted the
risk under the framing that signal half does the heavy lifting and
breadth is a small perturbation.

## Result — falsified hypothesis, big collapse
| recipe                 | per-bin (sig/brd) | cross-14 | seed std |
|------------------------|-------------------|----------|----------|
| 020 signal-only + strat| 10K / 0           | 0.7841   | 0.006    |
| 015 70/30 + strat      | 7K / 3K           | 0.7960   | 0.017    |
| **023 80/20 + strat**  | **8K / 2K**       | **0.7594** | **0.022** |
| 022 breadth-only + strat| 0 / 10K          | 0.7434   | 0.024    |

Per-seed eval_01: 0.7285 / 0.7412 / 0.6892 (range 0.052). cross-14
= 0.7594 — way below 015 (-0.037) and even below 020 (-0.025).
Predicted [0.785, 0.800]; actual is well outside.

## The interaction is non-monotonic in mix ratio
Sweep through breadth allocation under GC strat:
- 0% breadth: 0.7841 (020, signal-only)
- 20% breadth: 0.7594 (023, this experiment)
- 30% breadth: 0.7960 (015, champion)
- 100% breadth: 0.7434 (022, breadth-only)

Going from 0% → 20% breadth REDUCES performance. Going from 20% →
30% breadth INCREASES it. This is non-monotonic — there's no
smooth interpolation between the endpoints.

## The per-(axis × bin) floor is the real constraint
The non-monotonicity is explained by a hard stability floor:
- 023 breadth: 2K/bin (BELOW 3K floor) — unstable, hurts
- 015 breadth: 3K/bin (AT floor) — stable, helps
- 022 breadth: 10K/bin (above floor BUT axis is anti-synergistic)

Once an axis-bin drops below ~3K, stratified weighted sampling
becomes unstable across seeds; the few high-numsamples elements
in extreme-GC bins get exhausted and rng.choice picks variable
fillers per seed. The per-seed std confirms: 023 std (0.022) is
4× higher than 020 std (0.006), 30% higher than 015 std (0.017).

The per-(axis × bin) floor isn't just an upper bound on bin count
— it's a HARD constraint on every axis × bin cell. Every cell must
have ≥ 3K samples, otherwise stratification destroys the axis
contribution.

## Theory v21 → v22
> **The stability floor is per (axis × bin) cell, not per axis.**
> Every cell in the (axis × bin) lattice must have ≥ ~3K samples,
> or stratification destroys that axis's contribution. 015 works
> because its smallest cell is 3K (breadth × bin). 023 fails
> because its smallest cell drops to 2K. 016 (10 GC bins) failed
> for the same reason on both axes.
>
> This refines v21: the asymmetric (axis × strat) interactions
> only manifest cleanly when each (axis × bin) cell stays above
> floor. Below floor, the axis contribution is replaced by sampling
> noise.
>
> Practical: the design constraint is min(N_axis_i / N_bins) ≥ 3K
> for every axis i. The 70/30 + 5 bins recipe sits exactly at the
> corner of this constraint; deviating in either ratio or bin count
> direction crosses it.

## Implications for remaining experiments
The (mix ratio × bin count) optimization space is constrained:
- More bins → smaller bins, breadth axis crosses floor first
- More signal % → smaller breadth/bin, breadth axis crosses floor
- More breadth % → still bounded above by anti-synergistic axis
- Fewer bins → wider bins → composition partition fails (021)

The design constraints cross at exactly 70/30 + 5 bins for the
DHS Index dimensions. Other axes (cCRE, conservation) may have
different sweet spots.

## Next
- 024: test if the SIGNAL half alone needs stratification, or if
  the BREADTH half alone needs stratification, by stratifying only
  one half of the 70/30 mix. Identifies which half drives the
  015 lift.
- Then explore truly orthogonal axes (chromosome, motif content)
  rather than further mix-ratio tuning.
