# 009 4 buckets HEAVY=0.5

eval_01 mean=-0.0000 (worse than HEAVY=0.7). HEAVY=0.5 too weak.

eval_01 sweep (cond_b in parens):
- 0.25 (random): -0.0011 (b=-0.0025)
- 0.50: -0.0000 (b=0.0001)
- 0.70: +0.0023 (b=0.0052)
- 0.85: +0.0022 (b=0.0118) ← peak b
- 0.95: -0.0008 (b=0.0005)

Sweet spot for eval_01 sum near HEAVY=0.7-0.85. Best signal driver is b.

Next: try HEAVY=0.85 PLUS within-seq Markov structure (STAY=0.4) to boost c.
