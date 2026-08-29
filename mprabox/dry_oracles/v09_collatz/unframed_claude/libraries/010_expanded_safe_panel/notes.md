# 010 — expanded 12-motif panel (002 + TATAAA + GGGCGG)

**Hypothesis**: adding TATAAA (TATA box) + GGGCGG (alt SP1) to 002's safe panel will increase diversity and beat 002.

**Result**: eval_01 = **0.2230** (WORSE than 002's 0.2675). HepG2 = -0.087 (regressed from +0.038).

**Interpretation**: ANY addition to 002 panel (here, 003, 006) drives HepG2 negative. Either:
  (a) TATAAA specifically harmful — promoter-shifting bias (model expects enhancer)
  (b) Adding ANY motif beyond 002's 10 dilutes the protective HepG2 signal
  (c) Noise — 002's gain may have been partly luck

**Next**: Exp 011 = pure replication of 002 with different seed. Critical sanity check on whether 0.27 vs 0.22 differences are noise or signal.
