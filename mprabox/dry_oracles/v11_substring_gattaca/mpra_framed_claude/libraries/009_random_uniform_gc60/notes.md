# 009 random uniform GC=0.60

50k 200bp sequences sampled with P(G)=P(C)=0.30, P(A)=P(T)=0.20. Seed 0.

## Result
- mean_r = 0.857 (eval_01 = 0.867)
- vs GC=0.5 (exp 001): +0.005 mean, +0.005 eval_01 — first true improvement
- SKNSH jumped from ~0.84 → ~0.90 across most evals
- K562 dropped ~0.02-0.05 per eval
- HepG2 unchanged

## Takeaway
GC content is a real lever. Higher GC = better SKNSH (neural / GC-rich), worse
K562 (erythroid / AT-balanced). HepG2 (hepatic) tolerates both.

Net positive at GC=0.6, but the K562 tradeoff means an even higher GC could
hurt overall. Next: try GC=0.65 to map the curve.
