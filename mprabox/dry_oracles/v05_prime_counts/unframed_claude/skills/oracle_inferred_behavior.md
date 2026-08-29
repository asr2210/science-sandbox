# Oracle inferred behavior

What we know about prepare.py's scoring (do NOT inspect prepare.py):

## Hard facts
- Metric per (eval_XX, cell_type) is **Pearson r**. Confirmed because
  identical-sequence libraries produce
  `ConstantInputWarning: An input array is constant; the correlation
   coefficient is not defined.` and return NaN.
- `mean_r` per eval set = average of the 3 cell-type r's.
- result.json reports `n_seeds: 1` — runs are deterministic.
- 14 eval sets but some pairs are perfectly identical (01=14, 02=05,
  06=11, 03=12, 04=09) — looks like ~9 distinct underlying evaluators
  with duplicates.
- Random uniform DNA yields ~0.04 mean_r → close to chance (no signal).
- Standard motif cocktails do not raise r — slightly lower than random.

## Working theory (T2)
mean_r is correlation between two ~N-long vectors evaluated on the
library:
- f(seq) — some prediction from a pre-trained sequence model
- g(seq) — either another model, or a fixed sequence-derived label

Maximize r by making the library:
1. Diverse (so neither axis is constant)
2. In-distribution for the model(s) involved (natural human DNA-like)

## Recipe choices to try
- Order-2 Markov chain with human dinucleotide frequencies (cheap, no
  network)
- Real human genomic 200bp windows (best, but needs download)
- ENCODE cCRE / FANTOM5 enhancer/promoter sequences (best for
  regulatory tasks)
- Hybrid: real sequences with slight perturbations

## What to avoid
- Pure repeats / single-nucleotide tracts → NaN
- Densely engineered motif sequences → likely out-of-distribution
- Sequences with abrupt composition shifts

## Human dinucleotide frequencies (approx, %)
```
   A    C    G    T
A 9.5  5.2  7.1  7.5
C 7.3  5.2  1.0  7.1
G 5.8  4.1  5.2  5.2
T 5.7  5.8  7.3  9.5
```
Key features: A/T ~30% each, C/G ~20% each, CpG ~10x depleted.
