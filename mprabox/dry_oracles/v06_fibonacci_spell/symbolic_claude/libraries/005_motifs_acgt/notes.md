# 005 — Motif insertion (0123 -> ACGT mapping)

## Setup
Uniform random length-200 base + 0-12 insertions of universal TF motifs
(TATA, E-box, GC box, CAAT, AP-1, CRE, NF-kB, GATA, HNF4) encoded as
A=0,C=1,G=2,T=3. Vary insertion count per sequence.

## Result
- eval_01 mean=0.1227 (k562=0.0315, hepg2=0.1481, sknsh=0.1886)
- Worse than 003 Dirichlet (0.1349), barely above random (0.1183)

## Interpretation
Two possibilities (not mutually exclusive):
1. Mapping 0->A,1->C,2->G,3->T is wrong (motifs not recognized)
2. Motif insertion HOMOGENIZED composition (reducing the Dirichlet
   compositional variance that was driving the 003 gain)

Note: 005 used uniform random base, so it doesn't carry the +0.017 from
Dirichlet baseline. Need to disentangle: try motifs ON TOP of Dirichlet
base, or try a different mapping.
