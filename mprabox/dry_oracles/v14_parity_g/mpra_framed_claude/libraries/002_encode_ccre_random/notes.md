# 002 — Random ENCODE V4 cCREs (200bp centered)

**Source:** ENCODE V4 cCRE registry (ENCFF864OWG, 2.35M elements). Sampled 50,000 at random uniformly, extracted 200bp centered on each.

**Predicted:** Modestly positive mean_r (0.1–0.3). Real regulatory grammar should provide learnable signal.

**Got:** Essentially zero. Range -0.0045 to +0.0040 across 14 evals.

**Critical observation:** 95% of V4 cCREs are labeled "Low-DNase" — meaning most are weakly active across tissues. Random sampling captures mostly inactive elements.

**Lesson:** Real genomic context is NOT sufficient. The library must have **activity variance** — sequences spanning weak to strong — for the model to learn a signal/noise gradient.

Runtime: 68s wall.
