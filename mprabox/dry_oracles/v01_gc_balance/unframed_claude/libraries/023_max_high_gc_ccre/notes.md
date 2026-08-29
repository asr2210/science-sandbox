# 023_max_high_gc_ccre

Push cCRE PLS+DNase-H3K4me3 to 50% of library.

## Result
eval_01: 0.6865 — DROP from 022's 0.6930
eval_04: 0.6342 (continues rising)
eval_07: 0.7358 (further drop)
GC mean=0.515 std=0.129

## Curve: high-GC fraction vs eval_01
- 019: ~14% → 0.6895
- 021: ~14% (no chrX) → 0.6908
- 022: 30% → 0.6930 ← peak
- 023: 50% → 0.6865

30% is the sweet spot for eval_01. Beyond that, library shifts too far
toward GC-rich CpG-island promoters and loses variance benefit.

## Next
- 024: keep 30% high-GC but add cCRE subcategories (dELS, pELS) for
  more enhancer diversity within mid-GC range.
