# 018 rc_augmented

**Design:** 25k topic-stratified cCREs + 25k their reverse complements.

**Result:** eval_01 = 0.0745. Within noise of cCRE plateau. Notable: eval_13 = 0.1435 (highest in this family) — RC augmentation may slightly help RC-sensitive evals.

**Interpretation:** RC augmentation neither helps nor hurts eval_01. Mostly equivalent.

**Note:** prepare.py ran in 15s instead of 50-75s — perhaps the model trains faster with duplicated (RC-mirror) sequences. Doesn't change result.
