# 028 slide_topic_blend

**Design:** Top 50k cCREs by TFBS density → topic-cluster (50) → balance 250/cluster (=12.5k) → 4 slides each.

**Result:** eval_01 = 0.0760. Same as 020 family. eval_03=0.0961 (highest seen).

**Lesson:** Adding topic clustering within the top-TFBS subset doesn't break the eval_01 ceiling. The TFBS-density filter already implies enough diversity.

**Decision:** 020-recipe variants saturate at 0.0760-0.0766. For final libraries (029, 030), use defensive replicates of the proven 020 recipe with different seeds.
