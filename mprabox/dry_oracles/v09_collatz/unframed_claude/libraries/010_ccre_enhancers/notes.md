# Exp 010 — ENCODE cCRE-centered windows (PLS+pELS+dELS, chr19+chr22)

86k cCREs classified as promoter-like / proximal- or distal-enhancer-like.
Took 200bp windows centered on (or within) each, sampled 50k.

## Result

| metric  | real chr22 | cCREs |
|---------|-----------:|------:|
| eval_01 | 0.3202     | 0.3077 |
| k562    | 0.1443     | 0.1428 |
| hepg2   | 0.1990     | 0.1472 |
| sknsh   | 0.6173     | 0.6331 |

cCREs are **worse** than naive chr22 tiles. Why: regulatory regions
(esp. promoters) are GC-richer than typical genome — that boosts SKNSH
slightly but hurts HepG2 a lot. Net negative.

Lesson: more "regulatory" ≠ better. The model rewards SEQUENCE
COMPOSITION (esp. natural AT-rich context for HepG2) more than just
having TF binding sites.
