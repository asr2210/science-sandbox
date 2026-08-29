GC65 random (P(C)=P(G)=0.325). eval_01 mean=0.3853 vs baseline 0.4203 → worse.
K562 0.585→0.540, HepG2 0.618→0.561, SKNSH 0.059→0.056.
Pushing GC up uniformly hurts both K562 and HepG2. SKNSH unchanged.
Possibly the eval predictor expects near-50% GC; or this skews the
distribution of predicted activities in a way that compresses the correlation.
