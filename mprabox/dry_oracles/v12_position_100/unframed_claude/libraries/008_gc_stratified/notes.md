# 008 gc_stratified

**Design:** 50k random sequences each with target GC drawn uniformly from [0.2, 0.8]. Tests whether wide GC range alone helps.

**Result:** eval_01 = 0.0651. Essentially identical to random_uniform (0.0648).

**Interpretation:** GC composition diversity does not unlock the score. The label function is NOT primarily GC-dependent.

**Updated:** another stratification dimension (GC) added to the no-effect list.
