# Exp 002 — Motif cocktail (8 inserts/seq)

Embedded 8 motifs at random non-overlapping positions, drawn from
universal activator cocktail (AP-1, CRE, ETS, E-box, SP1, KLF, GATA, NFY).

## Result (vs Exp 001 random baseline)

| metric  | random  | exp 002 | delta   |
|---------|--------:|--------:|--------:|
| eval_01 | 0.2307  | 0.2541  | +0.0234 |
| k562    | 0.1361  | 0.1262  | -0.0099 |
| hepg2   | -0.0742 | 0.0186  | +0.0928 |
| sknsh   | 0.6302  | 0.6174  | -0.0128 |

Motifs help, but mostly HepG2 (huge jump). K562 and SK-N-SH slightly worse.
