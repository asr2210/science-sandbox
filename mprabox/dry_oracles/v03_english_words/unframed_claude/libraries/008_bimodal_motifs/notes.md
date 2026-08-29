Bimodal: 25k random + 25k random with 4 motifs each. eval_01 mean=0.4246.
vs random uniform seed 42 (0.4235): essentially no change (within noise).
vs 004 mixed motifs (0.4156): slightly better but still ~baseline.
Conclusion: increasing predicted-activity variance alone (via bimodal
motif/random) does NOT push r past 0.42. The ceiling is the predictor's
ability to RANK sequences correctly, not library variance.

Need to test next: do "real-looking" sequences score better than uniform
random? (test in-distribution vs OOD predictor accuracy)
