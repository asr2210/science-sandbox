# 005 Markov runs (STAY=0.7)

eval_01 = -0.0011. Still noise on primary metric.
Notable bumps: eval_07 a=0.0133, eval_13 a=0.0173 (positive); eval_03/12 c=-0.0105 (negative);
eval_04/09 b=0.0058 (positive); eval_10 c=-0.0088 (negative).

Pattern: cond_a goes UP when within-seq entropy is reduced (motif buckets exp 004 also
had eval_13 a=0.0172, eval_07 a=0.0084). Suggests cond_a may reward lower per-seq
entropy / longer runs. But this isn't enough to move eval_01.

Next: try EXTREME per-sequence compositional bias (4 buckets each biased 90% toward
one char). Combines two ideas: low entropy + 4-bucket separation.
