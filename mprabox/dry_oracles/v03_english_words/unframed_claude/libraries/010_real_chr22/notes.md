Real chr22 fragments (GRCh38, sampled from ACGT runs ≥200bp).
eval_01 mean=0.4001, K562=0.5445, HepG2=0.5520, SKNSH=0.1039.
vs random uniform (mean=0.42, K562=0.59, HepG2=0.62, SKNSH=0.06).

Key insight: REAL DNA nearly DOUBLES SKNSH r (0.06 → 0.10)
but hurts K562 (-0.05) and HepG2 (-0.07).
Net mean is slightly lower, but the SKNSH lever is huge.

Hypothesis: SKNSH predictor learns from real genomic context; random
sequences are OOD for it. K562/HepG2 predictors are more robust to random
inputs. The mean is dominated by SKNSH headroom, so finding ways to lift
SKNSH without crushing K562/HepG2 is the optimization path.
