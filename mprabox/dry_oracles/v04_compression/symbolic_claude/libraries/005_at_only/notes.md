# 005 AT-only random

50K random sequences over {0,3} only.

## Result
- eval_01: 0.1601 (better than GC-only 0.019, still worse than uniform)
- Strong asymmetry: {0,3} preserves much more info than {1,2}.
- Suggests eval distribution / oracle is more sensitive to {1,2} chars
  being present (or {0,3} alone is closer to genomic AT-rich background).
