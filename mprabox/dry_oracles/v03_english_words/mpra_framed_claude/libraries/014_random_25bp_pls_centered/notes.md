# 014 — Random + 1x25bp PLS CENTERED on midpoint

**Design.** As 012, but the 25bp slice is taken from the exact PLS midpoint (positions 88-112 of the 200bp window) instead of a random offset.

**Result.** eval_01 = **0.4196** vs 012's 0.4248 (Δ-0.0052). K562 = 0.586, HepG2 = 0.612, SK-N-SH = 0.061.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 012 PLS 25bp (rand offset) | 0.591 | 0.619 | 0.065 | **0.4248** |
| 014 PLS 25bp (centered) | 0.586 | 0.612 | 0.061 | 0.4196 |

**Interpretation — diversity beats targeting.** Centering on the midpoint:
- Reduces fragment diversity (all fragments cover the same TSS-adjacent positions).
- Slightly biased composition (PLS midpoints are CpG-rich → composition shift hurts K562/HepG2).
- Doesn't increase SK-N-SH lift (already saturates at ~0.06).

**Theory v12 — fragment DIVERSITY matters as much as fragment quality.** Random offsets sample across the full 200bp PLS window, giving the model exposure to:
- Core promoter motifs (when slice happens to land on TSS region)
- Pioneer factor binding sites (often upstream/downstream of TSS)
- Insulator/spacer sequences (also informative for promoter biology)

Centering all fragments on TSS region loses this diversity AND adds CpG-skew composition disturbance.

**Theory v12 corollary.** The model is learning a *distribution* over motif contexts, not specific motifs. More diverse fragments → more contexts learned → better generalization. This explains why pure PLS-centered loses to random-offset PLS even though the former is "more biologically targeted."

**Next.** 015 will test whether DOUBLING the PLS payload (2x25bp at random non-overlapping positions, total 50bp biology) helps or hurts. Diagnostic: 010 (1x50bp single fragment) lost vs 012 (1x25bp); does TWO 25bp fragments help where ONE 50bp didn't?
