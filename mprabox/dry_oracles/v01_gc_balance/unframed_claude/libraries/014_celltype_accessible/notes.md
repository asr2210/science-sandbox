# 014_celltype_accessible

50k 200bp sequences centered on K562/HepG2/SKNSH ATAC/DNase peak summits
(17k + 17k + 16k).

## Result
eval_01: 0.3930 — DOWN from 0.68 plateau.
K562_r: 0.4673 (vs 0.3670 HepG2_r, vs 0.3447 SKNSH_r within this library)
eval_04: 0.4905 — slight improvement (eval_04 likes accessibility)

## Interpretation
Cell-type accessible peaks crashed the score, same pattern as PLS (exp 008).
ATAC/DNase peaks have GC-rich profile (TF binding sites + open chromatin).
Compositional bias trumps any cell-type targeting benefit.

eval_04 prefers accessibility (intriguing) but eval_01 punishes the GC shift.

## Important takeaway
The score is dominated by overall library COMPOSITION distribution, not
cell-type specificity. K562 column doesn't reward K562-targeted sequences
specifically more than chr22-random does (K562 in chr22-random was 0.690).
