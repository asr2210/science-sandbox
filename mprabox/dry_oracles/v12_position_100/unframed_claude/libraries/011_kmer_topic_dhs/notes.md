# 011 kmer_topic_dhs

**Design:** 4-mer feature clustering of 250k cCRE windows via MiniBatch K-Means (50 clusters), then 1000 sequences sampled per cluster = 50k. Proxy for LDA topic modeling on DHS sequences.

**Result:** eval_01 = 0.0760. The BEST so far (vs prior best 004 TFBS=0.0764, essentially tied).

**Interpretation:** Topic-style (k-mer cluster) sampling provides a marginal lift over flat cCRE sampling (0.0760 vs 0.0745). Direction is correct but magnitude tiny. Not the 0.7+ baseline some external comparisons claim.

**Two paths to test next:**
- Higher-k clustering (motif level, 6/7-mer with more clusters)
- MPRA-derived sequences (downloads from published studies)
