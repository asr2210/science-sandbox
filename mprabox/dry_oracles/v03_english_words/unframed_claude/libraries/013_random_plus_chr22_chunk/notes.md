Intra-seq chimera (100bp random + 100bp chr22). eval_01 mean=0.4069.
K562 0.552, HepG2 0.570, SKNSH 0.098.
Slightly better than 50/50 inter-seq mix (011: 0.397), but still below
random uniform (0.42). Bringing chr22 "into" sequences instead of as
separate items helps a little — gradient in OOD-ness rather than binary.
SKNSH stays at 0.10; K562/HepG2 still drop ~0.04-0.05 from random.
Net mean still negative vs random baseline.

Need smaller chr22 fraction per seq, or replace chr22 with synthetic
neural-specific motifs.
