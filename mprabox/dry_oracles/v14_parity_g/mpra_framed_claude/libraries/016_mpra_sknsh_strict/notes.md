# 016 — SKNSH stringency test (S12 strict, H3 strict, K35 fill)

Wanted to test whether SKNSH benefits from a strict |lfc| filter the way HepG2 did. Cut SKNSH to top 12k (|lfc|≥0.48) and let K562 expand to 35k to fill (|lfc| dropped to 1.15).

**Result:** mean_r = 0.0028 (DOWN from 015's 0.0045).
- K562 avg = 0.0004 (dropped from 0.0024 — K562 doesn't tolerate |lfc|≥1.15)
- HepG2 avg = 0.0008 (dropped from 0.0044 — same 3k strict HepG2 sequences, why did HepG2 collapse?)
- SKNSH avg = 0.0071 (flat — strict SKNSH didn't help)

**Two findings:**
1. SKNSH stringency does NOT help. SKNSH r is flat across [no filter] and [|lfc|≥0.48]. Implication: SKNSH MPRA data has a wider activity-to-signal mapping than K562/HepG2 — most SKNSH BED entries carry usable signal regardless of magnitude.

2. K562 expanding from 22k → 35k DESTROYED K562 signal. K562 |lfc| threshold of 1.15 is below the K562 cliff. K562 wants |lfc|≥~1.7+.

3. HepG2 strict 3k didn't help on its own — its signal seems COUPLED to the rest of the library. Possible reason: model capacity is split across cells; when K562 dominates with noisy lower-|lfc| sequences, HepG2 signal degrades too.

**Next (017):** Try different augmentation — ALT alleles for top K562 sequences (paired contrast for high-magnitude).
