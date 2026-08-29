# prepare.py behavior (observed empirically)

## Inputs / outputs
- Call: `python3 prepare.py libraries/NNN_name/`
- Reads: `libraries/NNN_name/sequences_0.txt` (50,000 lines of 200bp `ACGT`)
- Writes: `libraries/NNN_name/result.json` with 14 eval entries + `n_seeds`,
  `time_s`.

## Timing
- ~31s "training" wall time reported inside the script
- ~1 minute total real time on this machine (including model setup + eval)
- Per-experiment budget is therefore cheap: many experiments per hour are
  feasible.

## Eval structure (from random-baseline run)
The 14 anonymous eval sets contain duplicates. Confirmed pairs/groups (random
baseline, identical r to 4 decimals):
- {eval_01, eval_02, eval_05, eval_14} → all 0.5131-0.5132
- {eval_06, eval_11} → 0.5123
- {eval_03, eval_12} → 0.5176
- {eval_04, eval_09} → 0.4175
Singletons: eval_07 (highest, 0.579 on random), eval_08 (lowest, 0.16),
eval_10 (0.52), eval_13 (0.56).

So practical distinct eval signals are ~7. Treat eval_01 as the primary
metric. Treat **eval_08** as the canary for genuine regulatory grammar
learning — it is the only set on which random sequences fail badly.

## Random baseline numbers (anchor)
50k uniform random 200bp sequences → eval_01=0.5131, mean across 14 evals
~0.49. This is the floor every library must beat.

## SK-N-SH systematically lowest
Across all evals, sknsh_r < k562_r and hepg2_r. This may reflect either fewer
training signal in the K562/HepG2/SK-N-SH measurements or a harder target —
worth noting when interpreting per-cell-type results.
