# Experiment 012: K562 DNase peak-centered 200bp windows

## Plan
50k 200bp windows centered on K562 DNase peaks (118k peaks total). Tests
whether cell-type-specific accessible chromatin helps.

## Result
- eval_01 mean_r = **0.1258** (K562=0.031, HepG2=0.162, SKNSH=0.184)
- WORSE than full-genome random (0.1387)
- WORSE than cCREs (0.1285)
- K562 r DROPPED vs genome random (0.049 → 0.031) despite K562-specific input!

## Big finding
Even using K562 DNase peaks does NOT improve K562 prediction. Specialization
on any subset of the genome reduces effective informativeness.

## Theory update
T9 reinforced: the scorer wants DIVERSE training data spanning the natural
genome distribution. Any concentration on a subset (cCREs, DNase peaks,
single chromosome, balanced chroms) reduces score, even when the subset is
cell-type-relevant.

The model must need varied "negative" examples (low-activity sequences) to
learn the activity gradient. DNase peaks are mostly "active" → degenerate
training set → poor model.

## Next
Try cross-species: mouse genome random windows mixed in. Adds genuinely
novel sequence content beyond human. May add or hurt; informative either way.
