# 015 — Random + 2x25bp PLS at random non-overlapping positions

**Design.** Two 25bp PLS fragments per sequence (total 50bp PLS biology), placed at non-overlapping random positions.

**Result.** eval_01 = **0.4122** vs 012's 0.4248 (Δ-0.0126). K562 = 0.577, HepG2 = 0.600, SK-N-SH = 0.059.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 010 1x50bp mixed | 0.577 | 0.602 | 0.054 | 0.4109 |
| 012 1x25bp PLS | 0.591 | 0.619 | 0.065 | **0.4248** |
| 015 2x25bp PLS | 0.577 | 0.600 | 0.059 | 0.4122 |

**Interpretation — total biology saturates at ~25bp / 200bp.** Doubling the PLS payload:
- Dropped K562 by 0.014 and HepG2 by 0.019 (composition disturbance from 50bp PLS biology).
- SK-N-SH did NOT improve (still 0.059, very close to 012's 0.065).
- Net result almost matches 010 (single 50bp): doesn't matter if 50bp is contiguous or 2x25bp split.

**Theory v13 — total bio cap.** The 25bp/200bp ratio (12.5%) is the saturation point. Adding more biology:
- (Diminishing returns) Doesn't add proportional SK-N-SH lift (SK-N-SH lift saturates ~0.06).
- (Linear cost) Adds linear K562/HepG2 composition cost.

Net = negative beyond 25bp.

**Next direction.** Total bio is fixed near 25bp. To improve further, change the QUALITY of biology embedded, not the QUANTITY. Two angles:
- 016: Try other cCRE classes (pELS, dELS, CA-CTCF) as the source — confirms PLS specifically is best.
- 017+: Within PLS, select for higher-quality fragments (motif-enriched, short PLS, tissue-universal).
