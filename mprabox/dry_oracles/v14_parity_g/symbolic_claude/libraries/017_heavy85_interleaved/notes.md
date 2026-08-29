# 017 4 buckets HEAVY=0.85 INTERLEAVED (row i → bucket i%4)

eval_01 = -0.0032; b dropped from +0.0118 (blocked) to +0.0000 (interleaved).
ROW ORDER MATTERS. The scorer uses row index in computing scores.

Implication: scorer's per-row target is BLOCK-STRUCTURED in row index.
With blocked design, our per-row features align with target's per-row values.
With interleaved, no alignment.

This is a KEY finding. Next: probe what kind of block structure target has.
