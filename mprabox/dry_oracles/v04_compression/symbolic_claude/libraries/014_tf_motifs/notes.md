# 014 TF motifs in random background

3-5 of {TATA, CAAT, GC-box, E-box, GATA, AP-1, CRE, NF-kB} per seq
embedded in iid random.

## Result
- eval_01 = 0.2846 (within noise of 0.30 baseline).
- eval_07 = 0.4287 (marginal up).
- TF motifs don't substantially help. Either the embeddings break iid,
  or these specific motifs are not what the eval rewards.
