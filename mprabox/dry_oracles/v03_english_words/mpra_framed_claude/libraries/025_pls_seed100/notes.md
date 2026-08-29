# 025 — 012 recipe with SEED=100

eval_01 = **0.4225** (vs 012's 0.4248). K562 0.584, HepG2 0.613, SK-N-SH 0.071.

Same recipe, different seed: 0.4225 vs 0.4248 = Δ-0.0023. Initial estimate of noise floor.

Notable: K562/HepG2 DROPPED but SK-N-SH JUMPED to 0.071. Seed 12 sampled a slightly less CpG-rich fragment set; seed 100 sampled fewer high-motif fragments per cell type.

Combined with 030 (seed=50, eval_01=0.4133), noise floor is much larger than initially thought.
