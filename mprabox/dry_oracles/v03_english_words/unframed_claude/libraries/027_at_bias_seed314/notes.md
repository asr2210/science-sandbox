# Exp 027 — AT-bias 0.27/0.23/0.23/0.27, seed=314

**Hypothesis**: Slight AT shift (GC=46%) might unlock a small lift if
the model "expects" something between pure random (50%) and natural
(~41%).

**Result**: eval_01 = 0.4273.

vs seed=314 pure random (0.4277): -0.0004 (neutral, within noise).

**Takeaway**: Slight AT bias doesn't move the needle. The model is
essentially flat across GC ∈ [0.46, 0.50] but cliff-drops outside.
