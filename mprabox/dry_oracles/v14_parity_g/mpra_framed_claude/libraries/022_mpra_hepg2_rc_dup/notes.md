# 022 — HepG2 strict + RC augmentation

Layout: SKNSH 22k, HepG2 3k strict + 3k RC = 6 slots, K562 22k.

**Result:** mean_r = 0.0036 (vs 015's 0.0045 — significant drop).
- K562 = 0.0023 (matches 015)
- HepG2 = 0.0029 (DOWN from 015's 0.0044 and 018's 0.0049 same-strand dups)
- SKNSH = 0.0061 (slight drop from 015's 0.0066, attributable to 22k vs 25k)

**Interpretation:** RC augmentation actively HURTS. Same-strand dups in 018 helped HepG2 (0.0049) but RC pairs hurt it. The model is NOT RC-equivariant: RC of a high-activity sequence appears as a distinct (random-looking) input, and presenting two contradictory labels for what's effectively the same regulatory element damages training.

**Lesson:** No RC augmentation for MPRA. Each unique high-activity site contributes once or as same-strand dups, never as RC pairs.

**Next (023):** Test K562 selection with min-distance spacing. Top 22k K562 has 6,457 pairs within 1kb (30% clustering); chr19 alone has 2,287 (10%). Spacing-enforced selection may free slots for distinct loci with lower |lfc|, retaining diversity.
