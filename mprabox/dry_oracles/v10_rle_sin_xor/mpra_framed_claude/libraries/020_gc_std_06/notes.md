# 020 — per-seq target GC ~ Normal(0.5, 0.06)

## Result
- eval_01 mean_r = **0.5180**
- K562 r = 0.9876 (drop), HepG2 r = 0.5679, SK-N-SH r = -0.001
- Realized GC std = 0.067

## Reading
Back to baseline. GC std 0.06 is too wide — K562 r drops from 0.994 to 0.988 because the model trains on too-disperse GC. Optimum is between 0.02-0.04 target std.
