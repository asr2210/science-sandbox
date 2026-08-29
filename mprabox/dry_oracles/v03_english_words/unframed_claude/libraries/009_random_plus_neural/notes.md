# Exp 009: random + 3 neural-specific motifs

**Hypothesis**: Adding neural motifs (homeobox, bHLH) to random background
would boost SKNSH while keeping K562/HepG2 near optimum.

**Method**: 50k random 200bp, embed 3 motifs from neural pool (TAATTA,
CAGCTG, CATCTG, REST half-sites, etc.) per seq.

**Results**:
- eval_01: 0.4186 (vs random 0.4203) → -0.002 (≈ noise)
- K562: 0.5867 (vs 0.5847) → ~same
- HepG2: 0.6203 (vs 0.6175) → ~same
- SKNSH: 0.0489 (vs 0.0587) → **-0.010** (hurt, opposite of prediction)

**Interpretation**: My neural motif insertions did NOT boost SKNSH —
they hurt it, just like other motif insertions hurt SKNSH (Exp 002, 005).

The SKNSH gain in natural sequences (Exp 006: 0.099) is NOT captured by
adding local motifs in a random background. Must come from something else:
- Higher-order context (long-range structure)
- Specific compositions/genomic features that random doesn't have
- Repeat elements (SINEs, LINEs) which are prevalent in natural DNA

**Implications**: Random-with-motifs strategy is dead. Need to revisit
natural sequences and try to get K562/HepG2 to behave better. Maybe
regulatory-active regions (cCREs) work better than random genomic windows.
