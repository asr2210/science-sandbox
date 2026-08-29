# 020 — HepG2 ref + alt augmentation

Tried adding alt-allele variants for top 3k HepG2 strict (similar to 017 but for HepG2). SKNSH cut to 22k, K562 held at 22k.

**Result:** mean_r = 0.0028 (down from 015's 0.0045).
- K562 = 0.0014 (dropped)
- HepG2 = 0.0022 (dropped from 0.0044 — alt pairing didn't help)
- SKNSH = 0.0048 (dropped — 22k vs 25k matters slightly)

**Two confounds:** my SNV-only filter (requiring parseable single-bp ref/alt and `ref_seq[center] == ref_base`) ended up dropping many HepG2 entries that had window=left/right shifts or indel ref/alt. Effective HepG2 threshold dropped to |lfc|≥1.76 (vs 015's 3.76).

**Lesson confirmed:** ref+alt augmentation hurts whichever cell it's applied to. Don't pair MPRA alleles in training.

**Next (021):** Pivot — try TSV padj-filtered selection. K562 from TSV with padj<0.05 + |lfc|≥1.5. Tests whether statistical significance adds value beyond magnitude.
