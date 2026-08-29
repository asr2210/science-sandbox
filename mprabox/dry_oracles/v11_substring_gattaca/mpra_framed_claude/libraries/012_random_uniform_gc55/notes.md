# 012 random uniform GC=0.55

50k 200bp sequences, fixed GC=0.55. Seed 0.

## Result
- mean_r = 0.857 (eval_01 = 0.868) — slightly best eval_01 yet
- Tied with GC=0.6 on mean, marginally edges on eval_01
- Better K562 (0.84) and HepG2 (0.88) than GC=0.6, slightly worse SKNSH (0.88)

## Takeaway
GC peak is a plateau in [0.55, 0.60]. Either GC=0.55 or GC=0.6 is a
defensible choice. eval_01 prefers 0.55 by 0.001; mean is tied. Within noise.

GC=0.55 may be slightly more balanced across cells → marginally better for
generalization to unknown cell types whose GC preference is uncertain.
