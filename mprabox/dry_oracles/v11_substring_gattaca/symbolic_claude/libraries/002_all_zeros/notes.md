# 002 all_zeros

50,000 copies of "0"*200. Returns NaN for everything.

**KEY DISCOVERY:** Triggers `ConstantInputWarning: An input array is constant;
the correlation coefficient is not defined.` (from scipy.stats.pearsonr).

This tells us:
- `mean_r` is a **Pearson correlation coefficient**, not a mean reward.
- The scoring computes two arrays of length 50,000 derived from our sequences,
  and reports Pearson r between them across the library.
- Identical sequences → both arrays constant → correlation undefined → NaN.

Implication: We need library-level **variance** in derived features.
The 0.85 we got from uniform random is *r* between two derived feature arrays.
To push higher, we need sequences where the two underlying derived properties
are even more tightly correlated than under random.
