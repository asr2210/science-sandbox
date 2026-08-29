# 008 — 50/50 mix of chr22 random + chr22+motifs

## What I tested
25k chr22 random windows + 25k chr22 windows with 2 motifs embedded.
50k unique source positions. Seed=42.

## Result
- eval_01 = **0.1345** (003: 0.134, 006: 0.135 — identical)
- mean of evals = 0.1290
- All cell types same as 006.

## What this means
Mixing didn't help. The 50/50 blend matches either component alone.
The plateau is genuine, not artifact of any single design.

## Theory update
The eval ceiling for "random-genomic-derived libraries" with a
fixed model is ~0.135. To break through, we need a *qualitatively
different* source distribution — promoter-focused, multi-source, or
fundamentally different syntax.

## What to try next
009: filter cCREs to promoter-like signatures (PLS) only. Tests if
a focused PROMOTER library helps (different cCRE subclass than 004's
mix of all cCRE types).
