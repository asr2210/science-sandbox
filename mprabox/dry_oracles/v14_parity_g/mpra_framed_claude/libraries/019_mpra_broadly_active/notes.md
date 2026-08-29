# 019 — Broadly-active cross-cell elements

11k K562∩HepG2 strong (|lfc|≥1.5 in both) + 3k HepG2 ultra-strict + 14k K562-only fill + 25k SKNSH.

**Result:** mean_r = 0.0043 (down from 015's 0.0045 — essentially tied).
- K562 avg = 0.0020 (matches 015)
- HepG2 avg = 0.0042 (matches 015)
- SKNSH avg = 0.0068 (matches 015)

eval_13 HepG2 = **0.0106** (new HepG2 single-eval high), eval_13 mean = 0.0079.

**Interpretation:** Broadly-active sequences are roughly equivalent to K562-strong alone in terms of contribution. They don't ADD generalization signal beyond what already-stratified K562/HepG2 strict provides. The HepG2 ultra-strict 3k is already capturing the most informative HepG2 sequences; adding HepG2-moderate (|lfc| 1.5-3.7) sequences via the broadly-active pool doesn't sharpen HepG2 signal further.

**Next (020):** Try HepG2 alt-allele augmentation. K562 alt-pairing destroyed K562 (017) but oddly HELPED HepG2 there. Test if HepG2 ref+alt explicit pairing for HepG2-strict 3k helps HepG2 (or breaks it like K562).
