# 008_motif_injected

## Hypothesis
Strong TF motifs inserted into random uniform scaffolds (5 motifs per seq from K562/HepG2/SKNSH-relevant TFs) might raise r if both eval predictors agree strongly on motif-rich sequences.

## Method
- Parsed 43 consensus sequences (argmax of PFM) for 25 target TFs from JASPAR 2024 core vertebrate.
- Per sequence: pick 5 random motifs, place at random non-overlapping positions, fill spacers with random uniform bases.
- Library mean GC ≈ 50%.
- Seed 42.

## Result
- **eval_01 mean_r = 0.3850** (K562=0.6057, HepG2=0.4228, SKNSH=0.1265)
- Drop of 0.013 vs random uniform (0.3981).
- K562 and HepG2 each drop ~0.013; SKNSH drops more.

## Interpretation
Inserting motifs **hurts** — adds yet another departure from the random-uniform reference distribution. The eval doesn't reward motif content; it just notices the deviation in statistics.

This strengthens theory T4: random uniform i.i.d. appears to be near a global optimum. Every structural addition I've tried (motifs, biology, anti-repetition, GC spread, GC extremes) makes things worse.

## Next
- 009: noise floor (random uniform, different seed) — establishes how much score can vary on equivalent libraries.
- After that: try a few unusual configurations (e.g., short subsets, library sub-selection) but probably budget mostly toward confirming/exploiting random uniform.
