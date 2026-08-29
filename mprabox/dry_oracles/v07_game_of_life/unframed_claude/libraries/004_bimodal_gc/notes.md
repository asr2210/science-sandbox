# 004_bimodal_gc

## Hypothesis
A bimodal-GC library (50:50 mix of 20%-GC and 80%-GC sequences) has the same library-mean GC (~50%) as random uniform but maximum per-sequence variance. If r benefits from *spread* in features, this should beat random uniform. If r requires per-sequence balanced composition, this should lose.

## Method
- 25,000 sequences at 20% GC (i.i.d. base draws with p=[0.4, 0.1, 0.1, 0.4])
- 25,000 sequences at 80% GC (p=[0.1, 0.4, 0.4, 0.1])
- Shuffled together. Seed 42.

## Result
- **eval_01 mean_r = 0.3401** (K562=0.5255, HepG2=0.3728, SKNSH=0.1219)
- Big drop of ~0.058 vs random uniform (0.3981). All evals down.
- All cell lines hit; not specific to any one.

## Interpretation
Per-sequence composition matters, NOT library-mean composition. Sequences with extreme GC (20% or 80%) appear to be out-of-distribution for whatever the eval is doing, and they drag down r heavily.

Updated theory T3: The metric is sensitive to *per-sequence* base composition; sequences far from ~50% GC behave like noise/OOD and reduce the signal. Library-mean composition is incidental.

## Next
- 005: per-sequence GC drawn uniformly from U(0.1, 0.9). If GC balance matters smoothly, 005 should land between random uniform (0.398) and bimodal (0.340).
- Future: test specific GC values (30%, 40%, 50%, 60%, 70%) to find optimum.
