# 028 — SKNSH from TSV padj<0.05

Layout: H3 BED strict (first), K22 BED (second), SKNSH 25k TSV padj<0.05 (last, fill).

**Result:** mean_r = 0.0015 (DISASTER vs 015's 0.0045).
- K562 = -0.0017 (negative!)
- HepG2 = 0.0009
- SKNSH = 0.0054

**Interpretation:** SKNSH TSV padj<0.05 selection is STRICTLY WORSE than BED selection. Possible reasons:
1. SKNSH BED ENCFF861MOC may be pre-filtered for quality the TSV doesn't reflect.
2. Many TSV padj<0.05 SKNSH variants overlap with K562/HepG2 BED entries — when ordered SKNSH last, only weaker TSV variants get picked.
3. The TSV variant pool is biased toward high-effect alleles, which may not generalize well.

Also K562 r went NEGATIVE — the composition shift apparently hurt K562 prediction calibration too.

**Note on first run (wrong order):** When SKNSH was processed first, it consumed top K562/HepG2 BED variants because variant pool is shared across Tewhey cells. Re-ran with HepG2 → K562 → SKNSH order to preserve K562/HepG2 strict thresholds.

**Lesson:** Don't use TSV padj<0.05 for any cell. BED is better.

**Next (029):** Final consolidation: 015 base is genuinely the operating point. Try one more — exactly 015 but use HepG2 from TSV padj<0.05 (smaller set, but high signal density). HepG2 BED is huge (97k) but the TSV padj<0.05 may give a different selection with potentially higher per-cell |lfc| density.
