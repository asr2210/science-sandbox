# 029 HEAVY=0.80 seed=42, sorted rows within block

eval_01 = +0.0076 — IDENTICAL to 023 (unsorted seed=42).
All conditions and all 14 evals match exactly.

MAJOR finding: within-block row order does NOT affect the score. The scorer
uses block-level aggregates only. Sort = no-op for current 4-block setup.

(Across-block order DOES matter: exp 017 interleaved was negative.)

Implications:
- Variance comes entirely from block-aggregate randomness with each seed.
- Sorting/rearranging within blocks can't help.
- Only knobs: per-block sample set (seed) and across-block ordering.
- Lottery is the right play to beat 0.0076.

Cost: experiment provided no score improvement but a clean structural finding.
