# Experiment 004 — dense motif library (~10 motifs/seq)

## What I did
50,000 seqs: each is concatenation of ~70% TF motifs (random pick from
pool of 16) + random spacer, padded to 200bp.

## Result (eval_01)
- mean_r = **0.3805**  (baseline 0.519, **−0.14**)
- k562_r = 0.6706 (−0.32)
- hepg2_r = 0.4732 (−0.09)
- sknsh_r = -0.0021 (~same)

## Interpretation
Dense motifs make everything worse. SKNSH still pinned at 0.

Pattern after 4 experiments:
- baseline uniform random: K562=0.99, HepG2=0.57, SKNSH=0  → 0.519
- any composition shift: K562 drops sharply; HepG2 slightly; SKNSH unchanged

K562 r is a **fragile artifact of uniform 50% GC**, not real signal capture.
SKNSH may simply be impossible to lift — but I haven't tried real-DNA-like
distributions yet. Next test: 41% GC (real human genome composition).
