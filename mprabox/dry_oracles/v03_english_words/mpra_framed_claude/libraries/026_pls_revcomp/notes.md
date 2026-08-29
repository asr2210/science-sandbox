# 026 — 012 + 50% revcomp augmentation

eval_01 = **0.4155**. K562 0.584, HepG2 0.612, SK-N-SH 0.051.

Revcomp augmentation HURT, especially SK-N-SH (0.051 vs 012's 0.065).

**Theory v21 — model uses strand-specific promoter context.** Promoter motifs are NOT orientation-agnostic at the promoter level: TATA box, Inr, downstream promoter elements all have positional/directional context relative to TSS. Revcomping disrupts the upstream/downstream relationships the model learns.
