# 024 tfbs_dhs_slide

**Design:** Score each cCRE by TFBS_count × log(1 + max_DHS_signal_in_400bp); top 12.5k × 4 sliding windows.

**Result:** eval_01 = 0.0763. Same as 020/023 (0.0764/0.0766). Joint TFBS×DHS scoring adds nothing.

**Lesson:** The selection criterion among "high-quality cCREs" doesn't matter much. TFBS density alone is enough to identify the most informative regions. Adding DHS signal as a multiplier doesn't surface a different subset.
