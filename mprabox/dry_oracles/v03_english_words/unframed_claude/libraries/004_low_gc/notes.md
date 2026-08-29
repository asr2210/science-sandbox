# Exp 004: GC=30% biased random

**Hypothesis**: Test the other composition extreme symmetrically.

**Method**: p(A)=p(T)=0.35, p(C)=p(G)=0.15.

**Results**:
- eval_01 mean=0.3692 (vs 0.4203 random, vs 0.3567 high-GC)
- K562=0.5100, HepG2=0.5363, SKNSH=0.0613

**Interpretation**: Both directions hurt, high GC hurts more (-0.064 vs -0.051).
The optimum is near 50% GC. The metric is sensitive to library composition
diversity: pushing toward any single base reduces effective k-mer diversity.

SKNSH score (0.0613) actually slightly *improved* over random (0.0587)
under low GC. Possibly neural enhancers favor AT-rich sequences (homeobox
motifs like ATTA are AT-rich). Worth keeping in mind.

**Implications**: Composition is the dominant lever found so far, but in the
sense of "diversity matters". Random (50% GC) is at or near optimum. Now I
must find a different lever — motif density, structured sequences, or
natural-like composition.
