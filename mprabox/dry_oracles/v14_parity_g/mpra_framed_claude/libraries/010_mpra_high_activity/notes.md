# 010 — Top 50k by |log2FoldChange| across Tewhey BEDs (excl chr7/13)

Same Tewhey lab MPRA pool as 008 (K562 + HepG2 + SK-N-SH BEDs), but instead of uniform sampling, picked the 50k regions with highest |log2FC|. Lowest kept |log2FC| ≈ 1.13 (strong activity).

**Result:** mean of per-eval mean_r = **0.0023** (vs 008's 0.0020). Per-cell-type breakdown:
- K562 avg r = 0.0004
- HepG2 avg r = -0.0012
- **SKNSH avg r = 0.0078** (huge — best per-cell-type signal yet)

Per-eval highlights: eval_03 SKNSH = 0.0172, eval_12 = 0.0172, eval_02 = 0.0126, eval_01 = 0.0119. eval_10 K562 = 0.0073.

**Interpretation:** Magnitude filtering moves the needle on SK-N-SH. The SK-N-SH BED is small (28k), so high-|log2FC| sampling captures most of its tail. K562 (228k pool) and HepG2 (109k) high-activity tails are diluted because their absolute counts are larger.

**Theory update:** Activity magnitude DOES help training signal. But uniform |log2FC| sorting biases coverage toward whichever cell type has the largest |log2FC| tail (SK-N-SH here). To balance: stratify by cell type.

**Next (011):** Per-cell-type top-|log2FC| — equal counts from each cell's top-activity list.
