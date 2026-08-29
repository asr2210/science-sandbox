# 002 human_dinuc_markov

**Design:** 1st-order Markov chain using approximate genome-wide human dinucleotide frequencies.

**Result:** eval_01 = 0.0730 (vs random 0.0648, +0.008). Mean across 14 ≈ 0.090.

**Interpretation:** human-like dinuc composition gives a small boost. The signal is real but tiny — the model is composition-sensitive but composition alone is far from sufficient. Need true regulatory grammar (motifs, real human regulatory sequences).
