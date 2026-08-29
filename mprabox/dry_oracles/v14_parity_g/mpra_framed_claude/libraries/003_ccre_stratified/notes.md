# 003 — Stratified ENCODE cCREs

Stratified sample across PLS/pELS/dELS/TF/CA classes from ENCODE V4 file ENCFF420VPZ. Designed to give the model balanced exposure to promoter-like, enhancer-like, and TF-binding regulatory grammars.

**Predicted:** Some positive signal (mean_r 0.1–0.3) once classes were balanced.

**Got:** Still ~0 (mean_r -0.0014). Same as random.

**Conclusion:** Real regulatory grammar + class balance is not enough. The model is unable to extract signal from any of these libraries. Time to test a fundamentally different design.
