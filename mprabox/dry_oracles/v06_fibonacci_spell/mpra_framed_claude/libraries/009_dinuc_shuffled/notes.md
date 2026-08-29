# 009 — Dinucleotide-shuffled chr22 windows

## What I tested
50k chr22 random 200bp windows, each Altschul-Erickson dinucleotide-
shuffled (preserves dinucleotide counts exactly, destroys all higher-
order structure: motifs, repeats, k-mer patterns).

## Result
- eval_01 = **0.1333** (003 natural chr22: 0.1341) — *essentially same*
- mean of evals = 0.1271 (003: 0.1281)
- K562: 0.039 (003: 0.037) — slightly higher!
- HepG2: 0.166 (003: 0.169)
- SK-N-SH: 0.195 (003: 0.196)
- eval_08: 0.061 (003: 0.060)

## WHAT THIS MEANS — BIG FINDING
Dinucleotide composition ALONE explains essentially all of the
genomic advantage. Motifs, repeats, and higher-order structure
contribute almost nothing measurable to the model's performance.

The model trained on 50k random ACGT (0.116) vs 50k dinuc-shuffled
chr22 (0.133) gains the entire 0.017 from preserving dinucleotide
composition. Adding real motifs back (0.134) gives no additional
lift.

## Theory rewrite
Previous theory: motifs matter most. **Wrong.** At this scale
(50k × 200bp, small CNN), the model is essentially learning
"this looks compositionally like a genomic sequence → activity
proxy from GC/CpG/dinucleotide signature." It doesn't learn
fine motif syntax.

Implication: random-genomic plateau (~0.134) is the compositional
ceiling. To break through, I need either:
(a) A different compositional regime (high-GC, promoter-like)
(b) A model upgrade (can't — fixed) OR
(c) Sequences whose composition matches the eval distribution
    even more closely than random chr22 does.

## What to try next
010: GC-rich chr22 windows (top quartile by GC). Tests if biasing
the compositional distribution toward GC-rich (promoter-like)
sequences helps. If yes → composition direction matters; if no →
median genomic composition is what the eval rewards.
