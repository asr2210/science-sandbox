# 028 — 012 + 25% sequences with planted neural motif

eval_01 = **0.4232**. K562 0.590, HepG2 0.620, SK-N-SH 0.060.

Added 6bp neural-specific motifs (NEUROD CAGCTG, REST core, POU3F) to 25% of sequences alongside the PLS 25bp fragment. No SK-N-SH lift — confirms 002's finding that planted consensus motifs in isolation don't add value, even when stacked on a PLS base. The model needs realistic motif CONTEXT (genomic flanking), not bare consensuses.
