# 017 — K562 ref + alt for top |lfc| sequences

Built on 015. Reduced K562 unique ref count to 17k and added 5k alt-allele sequences (single bp swap) for the top 5k K562 by |lfc|. HepG2 3k strict + SKNSH 25k unchanged.

**Result:** mean_r = 0.0029 (DOWN from 015's 0.0045).
- K562 avg = **-0.0006** (collapsed from 0.0024)
- HepG2 avg = **0.0056** (UP from 0.0044 — new HepG2 high!)
- SKNSH avg = 0.0037 (dropped from 0.0066)

**Surprising:** K562 alt-allele augmentation HURT K562 (probably ref+alt pair confuses model) but HELPED HepG2 (?!). And SKNSH dropped.

**Hypothesis on the HepG2 boost:** the K562 ALT sequences may statistically resemble HepG2-active patterns (because K562 variants tested often overlap HepG2 regulatory regions). The alt-allele perturbations may have created sequences that, paired with HepG2 strict 3k, give better HepG2 contrast.

**Hypothesis on K562 drop:** training on (seq_ref, K562_label_ref) AND (seq_alt, K562_label_alt) where seq differs by 1bp creates noisy targets for K562 specifically — the model sees near-identical sequences with different labels and degrades.

**Takeaway:** K562 alt-allele pairing breaks K562 prediction. Don't pair K562 ref+alt in same library.

**Next (018):** Reset to 015 baseline. Test HepG2-replicate strategy: HepG2 3k strict × 2 replicates = 6 slots, drop 3 from K562. Tests if HepG2 sequences need MORE repetition (multiple "MPRA measurements") to learn from.
