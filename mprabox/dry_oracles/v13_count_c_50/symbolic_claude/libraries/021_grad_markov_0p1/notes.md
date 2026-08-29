# 021 grad_markov_0p1

Gradient + Markov weight 0.1.

## Result
- eval_01: 0.4073 (vs 0.4115 at weight 0.2)

Confirmed peak at weight 0.2.

Markov weight curve:
- 0.0: 0.4078
- 0.1: 0.4073
- 0.2: 0.4115 (peak)
- 0.3: 0.4057
- 0.5: 0.4010

Pure gradient with extreme endpoints might still help. Or try different smoothing
strategy: random walk in composition space (smoother than linear gradient).
