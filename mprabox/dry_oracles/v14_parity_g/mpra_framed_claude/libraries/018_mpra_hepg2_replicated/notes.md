# 018 — HepG2 strict 3k × 2 dups; K562 cut to 19k

**Result:** mean_r = 0.0038 (down from 015's 0.0045).
- K562 avg = 0.0007 (collapsed — K562 needs ≥22k, not 19k)
- HepG2 avg = 0.0049 (UP from 0.0044 — slight gain from replication)
- SKNSH avg = 0.0057 (slight drop)

eval_13 mean = 0.0080 (best single-eval mean ever; K562=0.0075, HepG2=0.0095, SKNSH=0.0069). Whatever eval_13 tests, this library is best for it.

**Lessons:**
- HepG2 replication does modestly help HepG2.
- K562 at 19k unique (|lfc|≥1.86) is WORSE than 22k at |lfc|≥1.69. Confirms K562 wants COVERAGE not just stringency — the 3k extra sequences in 015 (|lfc| 1.69-1.86) carry usable signal.
- Net result: replicating HepG2 helps less than maintaining K562 coverage.

**Next (019):** Try broadly-active cross-cell elements — sequences strong in BOTH K562 and HepG2 (13,359 such elements). These should give simultaneous K562+HepG2 signal. Plus HepG2 ultra-strict + SKNSH all.
