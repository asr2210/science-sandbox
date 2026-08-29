# 008_three_way_mix_shuffled — notes

## Design
20K natural + 15K cCRE + 15K dinucleotide-shuffled natural. Shuffle uses
Altschul-Erickson Eulerian-path algorithm; preserves 2-mer counts.

## Result (39s training, 72s wall)
- eval_01: 0.4934 — essentially tied with exp 004 (0.4937)
- All evals within 0.005 of exp 004
- eval_08 = 0.0914 — still immune

## Interpretation
- Adding a 3rd source (shuffled natural) does NOT help beyond 2-way mix.
- The plateau at ~0.49 holds.
- Shuffled controls do NOT help eval_08, even though they're high-entropy.
  So eval_08 isn't testing "anti-natural composition." It's testing
  something else.

## Implication
Library composition is at a saturation point with natural+regulatory mix.
To break the plateau, I'd need either:
- A fundamentally new sequence class I haven't considered
- Cross-species DNA (mouse, etc.)
- Or accept the plateau as the floor of model capacity

## What eval_08 isn't
- Not "natural genomic" (random did 0.11, natural did 0.09)
- Not "regulatory" (cCRE did 0.08)
- Not "high-entropy" (shuffled didn't help)
- Not "motif-rich" (synthetic motifs did 0.04, worst)

eval_08 may test sequences with one specific signal class (e.g., very
specific TFs not in genome neighborhoods, or sequences from very low
expression where the signal is too weak to learn).
