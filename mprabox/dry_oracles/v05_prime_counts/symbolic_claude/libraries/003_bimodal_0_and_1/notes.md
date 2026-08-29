# 003_bimodal_0_and_1

25,000 all-0 and 25,000 all-1 sequences (only 2 unique).

Result: condition_a/b give small *negative* r (~-0.02). condition_c gives NaN (with warning) — so condition_c's secondary array is also constant when only 2 unique inputs of these extremes.

Implications:
- The metric is r per-condition between two 50K vectors derived from our library.
- One vector becomes constant when all our sequences yield the same value for condition_c.
- Bimodal extreme sequences score WORSE than random uniform (negative vs +0.04).
- "Designing variance" alone is not enough; quality of variance matters.
