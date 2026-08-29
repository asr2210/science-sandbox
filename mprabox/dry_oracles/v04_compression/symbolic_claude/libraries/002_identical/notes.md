# 002 identical sequences

50K copies of one random 200-mer. Tests diversity penalty.

## Result
NaN across all eval sets. Warning: "ConstantInputWarning: An input array
is constant; the correlation coefficient is not defined."

## Crucial insight
The score is a **Pearson correlation**, not a mean. This means:
- The oracle labels our 50K sequences with truth values y
- A learner f is fit on (X, y)  
- f is evaluated on held-out eval sets using Pearson r
- If our sequences are all identical → all predictions identical → r undefined

**Reframing**: We are designing a training set for an oracle-distillation
task. We want sequences that, when paired with oracle labels, let the
learner generalize to the eval distribution.

## Strategy implications
- Diversity is critical (no duplicates).
- Want sequences where oracle gives high variance in labels (informative).
- Want sequences spanning the oracle's input distribution (probably
  natural-ish DNA-like sequences if MPRA).
- Random uniform may be low-info because oracle gives flat/low values on
  OOD random noise.
