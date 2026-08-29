# Exp 008: Markov-1 from natural di-frequencies

**Hypothesis**: Test whether natural's effect comes from base composition
(mono+di freq) or from higher-order motif structure.

**Method**: Compute mono and dinucleotide freqs from data/genome_chunks.txt
(12 Mb), sample 50k 200bp sequences via 1st-order Markov chain.
Natural GC=0.437, CpG conditional P(G|C)=0.057 (CpG-depleted, ✓).

**Results**:
- eval_01 mean=0.4094 (vs random 0.4203, natural 0.3975)
- K562=0.5713 (random 0.585, natural 0.541)
- HepG2=0.5945 (random 0.618, natural 0.552)
- SKNSH=0.0624 (random 0.059, natural 0.099)

**Interpretation**: Composition alone is roughly a halfway point between
random and natural for K562/HepG2 (mild hit). But SKNSH gets only +0.004
from composition (vs +0.040 for full natural). **The big SKNSH gain comes
from HIGHER-ORDER motif structure in real DNA**, not from composition.

**Theory update**: SKNSH model has learned specific neural motifs
(homeobox, bHLH). Natural sequences carry these. Random ones don't.

**Implications**: Add SPECIFIC neural motifs to random sequences. Should
boost SKNSH while leaving K562/HepG2 near random's optimum.
