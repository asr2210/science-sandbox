# 013 kmer6_topic_dhs

**Design:** 6-mer cluster (100 clusters via MiniBatchKMeans) on 150k cCRE windows; sample 500 per cluster. Failed: cluster sizes 1..12k (extreme imbalance), so oversampling small clusters with replacement created lots of duplicates.

**Result:** eval_01 = 0.0458 (BIG REGRESSION).

**Lesson:** oversampling small clusters with replacement is BAD — duplicates in the training library actively hurt the model. The lift in exp 011 came from 4-mer (256d, more balanced clusters), not from finer features.

**Next:** keep 4-mer but use ALL cCREs (2.35M pool), avoid oversampling.
