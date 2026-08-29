# Experiment 027 — JASPAR-motif-planted GC-strat random scaffolds

## Design
50K sequences: GC-strat random scaffolds (5 bins × 10K) with
3 random JASPAR-vertebrate consensus motifs planted at random
non-overlapping positions per sequence (873 motifs to choose from).

## Result
- eval_01: 0.3885 (Δ −0.0014 vs GC-strat random, −0.0054 vs GC-strat natural)
- K562: 0.6053, HepG2: 0.4237, SK-N-SH: 0.1366

## Interpretation
Motif planting did NOT lift performance. In fact, slightly hurt
(within noise) vs pure GC-strat random.

This is a strong constraint on the "motif" mechanism:
- Random injection of 3 isolated motifs ≠ natural motif content.
- Motif co-occurrence, spacing, and position relative to scaffold
  context matter — not just motif presence.
- Or: planting destroys some scaffold property that helps
  (e.g., the model relies on local GC/dinuc around each base, and
  planted motifs disrupt it).

## T12 → T13
**The "motif premium" of +0.009 (exp 026) is NOT exploitable by
synthetic motif content.** Natural sequences carry their motifs
embedded in their natural context (TSS proximity, co-binding TF
clusters, spacing constraints). Random injection breaks this.

So motifs are not a usable lever beyond what natural sequence
already provides. The 0.395 ceiling is hard.

## Implication
**Library design has saturated.** Engineering beyond natural
sequence (motif planting, dinuc shuffle, random) cannot exceed
the ceiling reached by GC-strat natural ~0.394 or 4-way mix
~0.395. The remaining +0.001 between best and worst ceiling-tier
libraries is noise.

## Next direction (exp 028)
Synthesis library — combine all positive learnings:
- GC stratification (T8: +0.021)
- Multi-source within each GC bin (T10: source identity fungible)
- Multi-genome (T4: doesn't hurt)

If this matches or exceeds 0.3961 (best so far, exp 010 seed=1),
confirms synthesis is principled best design.
