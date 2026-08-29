# 002 — TF motifs in random background

## What I tested
50k 200bp sequences. Each: random ACGT background with 2-3 motifs from a
curated 60-motif TF set (bHLH, bZIP, GATA, ETS, FOX, NF-kB, SP/KLF, MEF2,
HNF, C/EBP, etc.) inserted at random non-overlapping positions, random
orientation. Seed=42.

## Result
- eval_01 = 0.1239  (random=0.1160) → **+0.008**
- mean of evals = 0.1170 (random=0.1088)
- K562 lifted: 0.0109 → 0.0223  (still near zero)
- HepG2 ~flat: ~0.15
- SK-N-SH ~flat: ~0.19
- eval_08 unchanged at 0.056

## What this means
Adding motifs gives only marginal improvement. The motifs are real and
should activate reporters, but the model trained on this library transfers
poorly to whatever the eval sets are. Hypotheses for the small effect:
1. **Synthetic background ≠ genomic background.** Random ACGT context
   teaches the model "motif in random context", but eval sequences likely
   are genomic, with realistic dinucleotide composition and chromatin
   biases.
2. **Sparse, isolated motifs.** Real CREs typically have motif clusters,
   specific spacing, homotypic repeats. 2-3 random motifs in 200bp don't
   capture this syntax.
3. **Motif coverage may still be too narrow.** 60 motifs is a fraction
   of the human TFome (~1500 TFs).
4. **K562 motifs may need specific syntax.** K562 is hematopoietic;
   GATA1/KLF1/NFE2 sites might need cooperative arrangements.

## Theory update
"Motif presence" alone is not the dominant signal. **Motif context and
syntax matter as much as motif identity.** A library of motifs floating
in random oceans doesn't teach the model to recognize real CREs.

## What to try next
Experiment 003: real genomic sequences from a known regulatory element
catalog (or a tiled chromosome). This tests whether realistic context
beats synthetic motif-in-random-background. If yes → context matters.
If no → eval is testing something else entirely.
