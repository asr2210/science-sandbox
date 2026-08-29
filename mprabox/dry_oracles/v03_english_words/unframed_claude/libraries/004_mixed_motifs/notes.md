Mixed-motif sprinkles (2-3 motifs per sequence, random uniform background).
eval_01 mean=0.4156 vs 0.4203 baseline. Tiny dip. HepG2 slightly up
(0.6228 vs 0.6175), SKNSH DOWN (0.0411 vs 0.0587), K562 ~same.
Adding many motifs uniformly does NOT help. Possibly the motifs reduce
variance in predicted activity (all sequences become "moderately
enhancer-like"), which would hurt a correlation-based score.
Or some of my motifs are wrong/synthetic and act as noise.
