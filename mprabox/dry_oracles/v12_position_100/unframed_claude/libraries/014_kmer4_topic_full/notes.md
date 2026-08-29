# 014 kmer4_topic_full

**Design:** 4-mer K-Means(80) on FULL 2.35M cCRE pool. Sample at most PER_CLUSTER=625 per cluster (no replacement). Fill residual to 50k from remaining pool (no replacement). All 50k unique.

**Result:** eval_01 = 0.0739 (vs 011's 0.0760). Marginally worse.

**Cluster sizes:** 6 .. 54k — heavy imbalance even with 4-mer features at this scale. ~6 small clusters (<10k) provided <PER_CLUSTER members, so most of the library still came from the dense clusters via residual fill.

**Interpretation:** 
- Scaling up the pool 10x and clusters 80 vs 50 did NOT help.
- 011's "1000 per cluster" may have leaned on some duplication-via-replacement for small clusters (need to check), OR the 250k subsample happened to be more informative.
- Either way: refining the same recipe more doesn't break through. The ceiling at ~0.076 is real for cCRE-only libraries.

**Next:** try a categorically different source. Real published MPRA-tested sequences from Sharpr-MPRA or Tewhey 2016. These sequences are KNOWN to have activity distributions the model should care about.
