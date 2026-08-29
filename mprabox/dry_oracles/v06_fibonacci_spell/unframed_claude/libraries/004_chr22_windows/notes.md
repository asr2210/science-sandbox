# Experiment 004: Real human chr22 random 200bp windows

## Plan
Sample 50,000 random 200bp windows from chr22 (hg38), rejecting any with N.

## Result
- eval_01 mean_r = **0.1346** (K562=0.036, HepG2=0.171, SKNSH=0.197)
- +0.017 over random baseline (0.1176 → 0.1346, +14.5%)
- K562 r tripled (0.012 → 0.036) — big proportional move
- HepG2 +0.019, SKNSH +0.008

## Big finding
**Real human DNA scores meaningfully higher than random.** The scorer values
naturalistic sequence content. K562 is the most responsive to natural DNA.

## Theory update
T3 partially confirmed: natural-like content matters. Hypothesis becomes:
the scorer rewards (a) realistic k-mer/dinucleotide distributions, (b) the
presence of natural regulatory grammar that random shuffling destroys.

## Next
Push further — sample 200bp windows centered on **regulatory elements** (ENCODE
cCREs) which should be enriched for active enhancers/promoters. If score goes
up further, we're on the right track.
