# 009 ccre_class_stratified

**Design:** 50k = 6250 from each of 8 ENCODE cCRE V4 classes (Promoter, Proximal/Distal enhancer, CA, CA-CTCF, CA-TF, CA-H3K4me3, TF). 200bp centered on each cCRE midpoint.

**Result:** eval_01 = 0.0745. Same band as everything else.

**Interpretation:** explicit regulatory-class stratification provides no meaningful lift. Combined with prior negative diversity test (007), I now reject H3 (diversity hypothesis) for any of: source mixture, GC stratification, regulatory-class stratification.

The score's narrow dynamic range (0.064–0.076 for all natural+random+stratified libraries) is the key observation. Either there is a very specific library family that breaks 0.1+ (most likely some MPRA-derived or special construction) or the harness is largely composition-insensitive at this score regime.

**Next:** try public MPRA-tested sequences (real measured activity, so the library matches what test sets contain).
