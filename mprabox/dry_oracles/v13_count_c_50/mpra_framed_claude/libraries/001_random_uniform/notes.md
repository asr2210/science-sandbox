# 001 — Random Uniform Sequences

**Hypothesis being tested:** Establish a floor for eval metrics when the
library carries zero biological signal. Calibrate pipeline timing.

**Design:** 50,000 sequences, each 200 nt, A/C/G/T sampled uniformly
i.i.d. NumPy seed 0.

**Results (mean_r per eval):**
- eval_01: 0.1294 (PRIMARY)
- eval_02/05: 0.1281
- eval_03/12: 0.0771
- eval_04/09: 0.3902
- eval_06/11: 0.1189
- eval_07: -0.1416
- eval_08: 0.5795   ← surprisingly high
- eval_10: 0.0938
- eval_13: -0.1470
- eval_14: 0.1294
- Across-eval mean: ~0.158
- prepare.py time: 36 s (1m 5s wall)

**What this tells me:**

1. **Many eval sets are paired / nearly identical.** Notice the
   duplicates: {01,14}, {02,05}, {03,12}, {04,09}, {06,11}. So there
   are really ~9 distinct evaluation distributions, not 14. eval_07/13
   are similar but not identical (both very negative). eval_08 and
   eval_10 are unique.

2. **K562 is *always* learnable, even from random sequences.** Every
   single eval's K562_r is between +0.17 and +0.33 even with a
   biology-free training set. This means the K562 prediction head is
   picking up on a coarse signal — probably GC content / k-mer
   composition — that correlates with K562 measurements even when no
   real motifs are present. K562 has a strong dependence on simple
   sequence composition statistics.

3. **HepG2 is the opposite — variable and sign-dependent.** HepG2_r
   ranges from -0.33 (eval_07) to +0.76 (eval_08). A random library
   can either predict HepG2 well or anti-predict, depending on the
   eval set. This suggests HepG2 has eval sets with very different
   compositional profiles (some perhaps biased high-GC, others
   low-GC), and the random library learns the wrong thing on the
   wrong-direction ones.

4. **eval_07 and eval_13 are "anti-correlated" by the random model
   (mean_r ≈ -0.15).** Whatever these evals are testing, our random
   training has biased the model in the wrong direction. They are
   probably testing something the random library actively misleads
   the model about (perhaps sequences with strong specific motif
   activity where the random model has learned the wrong default).

5. **eval_08 is extremely high (mean=0.58)** even from random
   sequences. This is the eval most predictable by simple stats. It
   might be a low-activity / "is this likely silent?" type measure
   where the bulk of test sequences are predictable by composition
   alone.

6. **eval_04/09 (mean=0.39) is also unusually high** from random —
   suggesting GC / composition–driven prediction is partially
   sufficient. These evals may test against compositionally simple
   targets.

**Theory updates:**
- Confirmed: random sequences carry *some* coarse signal that
  generalizes — GC / composition. So the model is not purely useless.
- New idea: matching the *compositional distribution* (k-mer
  distribution, GC) of test sequences may be much more important than
  I'd assumed. Naïve random gives a flat GC ≈ 0.5 distribution; real
  test sequences likely have varied GC.
- New idea: eval_07/13 are critical to watch — they are where random
  is *worst*. If they stay negative as I move toward better libraries,
  there's something systematically wrong I'm missing.

**Next:** Random genomic windows from hg38 (experiment 002). Expect a
broad lift in all evals, with the strongest improvement on eval_07/13
(where motif structure should now align with what test sequences
have).
