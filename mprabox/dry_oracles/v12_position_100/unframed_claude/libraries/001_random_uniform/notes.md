# 001 random_uniform

**Design:** 50000 sequences x 200bp, each base uniform i.i.d. over {A,C,G,T}. Seed 42.

**Result:** eval_01 = 0.0648, mean across 14 evals = 0.0817.

**Key observations:**
- Confirmed evals come in identical pairs in v12:
  - eval_01 = eval_14 = 0.0648
  - eval_02 = eval_05 = 0.0634
  - eval_03 = eval_12 = 0.0782
  - eval_04 = eval_09 = 0.0813
  - eval_06 = eval_11 = 0.0653
  - eval_07, eval_08, eval_10, eval_13 are distinct
- Easiest evals (random hits highest): eval_07=0.131, eval_10=0.119, eval_13=0.119 — likely have GC/composition signal that random already partially captures.
- Hardest: eval_08=0.0563.
- prepare.py runtime ~57s wall, ~27s internal.

**Implication:** with 30 experiments and ~1 min per run, budget is plentiful. Can afford a few mistakes.
