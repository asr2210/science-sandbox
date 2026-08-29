# 008 — Tewhey lab MPRA library 200bp regions (excl chr7/13)

Pooled 200bp element regions from Tewhey lab MPRA element-quantification BED files for K562 (ENCFF822KPE, 228k), HepG2 (ENCFF887WCC, 109k), SK-N-SH (ENCFF861MOC, 28k). Excluded chr7 and chr13. Sampled 50k.

**Predicted:** This matches the distribution the simulator likely uses (Gosai/Siraj 2024 study; only published MPRA dataset covering all three target cell types). Should give first real signal.

**Got:** mean_r ~0.003, **eval_13 K562 = 0.0143** (highest single value yet across all experiments), **eval_10 K562 = 0.0096**. eval_08 flipped negative.

**Significance:** First clear "signal-on" experiment. Distribution-matching matters. The model is finally learning something K562-specific that transfers to eval_13.

**Next:** Push further on this direction — try filtering by activity magnitude and/or expanding sequence diversity.
