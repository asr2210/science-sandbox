# 006 — Human dinuc first-order Markov

## Hypothesis
Sequences matching human bulk-genome dinucleotide statistics (CpG-suppressed,
TpA-suppressed, ~50% GC) should be more "natural" and might score higher.

## Results
eval_01 = **0.1676** (random 0.3157). Big drop.

## Update to theory
Matching human genomic dinuc stats HURTS. So the underlying predictor was NOT
trained on bulk human genome — almost certainly trained on UNIFORM RANDOM
MPRA-style libraries (where dinucleotides are independent at 50% GC).

Random uniform 50%-GC is OUR best baseline because it MATCHES the predictor's
training distribution. Push by adding bio motif content WITHOUT shifting
overall base composition.

## Next
Exp 007: random + insert longer literature-validated regulatory cores.
