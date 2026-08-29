# 005 — random uniform + Poisson(2) JASPAR motif insertions (stochastic realizations)

## Design
Base: random uniform 200bp. For each seq, K~Poisson(2)∈[1,5] motifs are inserted at random non-overlapping positions. Motifs sampled uniformly from JASPAR 2024 vertebrate (879 PWMs). Each motif realized by stochastic PWM draw.

## Result
- eval_01 mean_r = **0.5180** (vs random uniform 0.5177; basically identical)
- K562 r = 0.9907 (random uniform 0.9946 — tiny drop)
- HepG2 r = 0.5696 (random uniform 0.5674 — tiny lift)
- SK-N-SH r = −0.0062 (still flat)
- 21 bp avg motif coverage per 200bp sequence; GC distribution unchanged.

## Reading
Adding 2 stochastic JASPAR motifs per sequence (~10% sequence coverage) makes essentially no difference to mean_r. Net effect ≈ +0.0003.

Two interpretations:
1. The motifs are too WEAK (stochastic sampling gives degenerate realizations) and the model can't reliably detect them as patterns.
2. Motifs truly don't help on this benchmark — eval activity is essentially composition-driven and any motif content is invisible.

To disambiguate, exp 006 will try **stronger, denser** motif insertions (consensus realizations, more motifs per sequence, more motif coverage). If those also don't help, interpretation #2 wins and motif injection is a dead lever.
