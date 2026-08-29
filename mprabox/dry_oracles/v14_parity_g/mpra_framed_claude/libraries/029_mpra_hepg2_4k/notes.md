# 029 — HepG2 expanded to 4k (smallest expansion)

Layout: K22 strict, H4 (|lfc|≥3.34), S24.

**Result:** mean_r = 0.0045 (TIED with 015, possibly slightly better: 0.00454 vs 015's 0.00447).
- K562 = 0.0028 (UP from 015's 0.0024)
- HepG2 = 0.0039 (slight drop from 0.0044)
- SKNSH = 0.0069 (UP from 0.0066)

**Surprise:** Tiny HepG2 expansion (+1k unique) HELPED K562 and SKNSH r! K562 selection didn't change (still K22), so the improvement comes from training-set composition broadening.

**Updated picture of HepG2 expansion vs mean:**
- H3 strict (015): mean=0.00447, H=0.0044
- H4 (029): mean=0.00454, H=0.0039 (K↑, S↑)
- H6 (024): mean=0.00434, H=0.0027 (K↑, S↑↑ but H↓↓ overall worse)

**Inflection point appears around H4-5.** HepG2 expansion lifts cross-cell prediction (K and S) while costing HepG2-specific signal.

eval_13 mean = 0.0072 (matches 015's 0.0078 — best single-eval still strong).

**Next (030):** Push to H5 @ |lfc|≥3.10 to confirm inflection. If H5 mean > H4, sweet spot is H5. If H5 < H4, then H4 is local optimum.
