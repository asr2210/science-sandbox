# Exp 002: TF motif pool

**Hypothesis**: Embedding 3 canonical TF motifs per sequence will raise mean_r
notably above random baseline. Tests if the metric is sensitive to motif content.

**Method**: For each of 50k random 200bp sequences, embed 3 randomly-chosen
motifs from a pool of 15 canonical enhancer/promoter motifs (AP-1, CREB,
NF-kB, GATA, E-box, TATA, CCAAT, SP1, HNF1, HNF4, ETS, etc.) at random positions.

**Results**:
- eval_01: 0.4232 (vs 0.4203 random) → +0.003
- K562: 0.5940 (vs 0.5847) → +0.01
- HepG2: 0.6235 (vs 0.6175) → +0.006
- SKNSH: 0.0521 (vs 0.0587) → -0.007 (slight regression)

**Interpretation**: Marginal effect. The pool of canonical motifs is a mild
positive for K562/HepG2 but slight negative for SKNSH. Two possible reasons:
(1) 200bp random already contains many short motifs by chance; (2) the metric
isn't dominated by motif content alone.

**Implications**: I need stronger perturbations. Will try:
- Extreme composition (GC content sweep, all-N homopolymers)
- Higher motif density / repeated motifs
- Real genomic sequences (if data available)
