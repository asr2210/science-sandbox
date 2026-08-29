# Experiment 029 — synthesis seed=1 (noise control on 028)

## Design
Identical to 028, SEED=1.

## Result
- eval_01: 0.3949
- K562: 0.6067, HepG2: 0.4324, SK-N-SH: 0.1455

## Synthesis 2-seed estimate
- seed 0 (028): 0.3941
- seed 1 (029): 0.3949
- mean: 0.3945, range: 0.0008

Very stable. Synthesis design noise is <0.001 between seeds.

## Comparison to other ceiling designs
| design | mean eval_01 | seeds | σ |
|---|---|---|---|
| 4-way mix (002/010/022) | 0.3951 | 3 | 0.0012 |
| synthesis (028/029) | 0.3945 | 2 | 0.0004 |
| GC-strat nat (014) | 0.3939 | 1 | — |
| multispecies GC (020) | 0.3947 | 1 | — |

All within 1σ of each other. Hard ceiling at 0.395 ± 0.002.
