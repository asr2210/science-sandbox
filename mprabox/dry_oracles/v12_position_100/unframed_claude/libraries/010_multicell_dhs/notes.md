# 010 multicell_dhs

**Design:** Multi-cell DHS pool (K562 + HepG2 + SK-N-SH), top 50k by max signal across 15 ENCODE peak files. 50bp dedup buckets to avoid near-identical peaks.

**Result:** eval_01 = 0.0712. Same band.

**Updated:** ALL bio-grounded DHS libraries (K562, multi-cell, cCRE-class) score 0.07-0.075. The 0.7+ baseline must use a structurally different design.

Likely culprits:
1. Topic-modeled k-mer cluster sampling (LDA on 6-mers, sample uniformly per topic)
2. Active-MPRA-tested sequences from a specific assay
3. Some completely different design family I haven't thought of

Next: try 6-mer-clustered DHS via minibatch k-means (proxy for topic modeling).
