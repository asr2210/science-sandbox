# 008 tight_constrained

Tight composition: each char count ∈ [48,52]. Direct construction (no rejection).

Result: eval_01 mean_r = **0.8377** (worse than 007's 0.8597, better than exact balance's 0.8185).

Updated curve (composition std vs eval_01 mean_r):
- std 0 (exact balance):    0.8185
- std 1.4 ([48,52]):        0.8377
- std 3   ([45,55]):        0.8597 ← peak
- std 6.1 (uniform random): 0.8526

Peak is near [45,55]. Next: try [44,56] / [43,57] to see if peak is broader.
Also explore other dimensions (k-mer, position) to break past 0.86.
