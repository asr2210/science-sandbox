# Exp 009 — Real chr22 random 200bp tiles

50k random 200bp windows from human chr22 (hg38). Skipped N-containing
or low-complexity (≥20bp homopolymer) windows.

## Result — BREAKTHROUGH

| metric  | random 50% | exp 002 motif | real chr22 |
|---------|-----------:|--------------:|-----------:|
| eval_01 | 0.2307     | 0.2541        | **0.3202** |
| k562    | 0.1361     | 0.1262        | 0.1443     |
| hepg2   | -0.0742    | 0.0186        | **0.1990** |
| sknsh   | 0.6302     | 0.6174        | 0.6173     |

Real DNA jumps mean_r by 0.066 over our best synthetic.
- HepG2 dominates the gain: -0.07 → +0.20 (huge — real DNA has natural
  low-GC + dinucleotide structure HepG2 model rewards).
- SKNSH and K562 unchanged.
- chr22 is ~48% GC, mid-range.

**Implication**: the scoring model is well-calibrated to natural human
DNA statistics (CpG depletion, dinucleotide bias, motif distribution).
Synthetic random with iid uniform bases is OUT-OF-DISTRIBUTION for HepG2.
