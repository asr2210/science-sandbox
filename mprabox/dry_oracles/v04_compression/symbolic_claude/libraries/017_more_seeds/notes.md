# 017 numpy PCG64 seed=42

Same iid uniform distribution but using numpy's PCG64 instead of
Python's Mersenne Twister.

## Result
- eval_01 = 0.3425. **NEW BEST.**
- Up from Python random best 0.329 (seed=2).
- Implies subtle correlation differences between RNGs matter.
- All evals improved over previous bests.
