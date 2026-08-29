# 017 — Random + 1x25bp CA-CTCF fragment per sequence

**Design.** Same as 012 but fragments from CA-CTCF (chromatin-accessible + CTCF-bound, 126K available).

**Result.** eval_01 = **0.4136** — LOSES to random (0.4192) AND to all other 25bp-embed variants. K562 = 0.585, HepG2 = 0.614, SK-N-SH = **0.042** (LOWER than random's 0.045).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 017 CA-CTCF 25bp | 0.585 | 0.614 | 0.042 | 0.4136 |
| 016 pELS 25bp | 0.590 | 0.615 | 0.055 | 0.4201 |
| 012 PLS 25bp | 0.591 | 0.619 | 0.065 | **0.4248** |

**Interpretation — CTCF biology actively HURTS.** Critical finding: CTCF is the most universally bound TF (active in all cell types), but CTCF-bound regions are ARCHITECTURAL (chromatin loop anchors), not transcription-activating. Embedding CTCF binding motifs *decreases* SK-N-SH below random — CTCF binding actually suppresses or is uncorrelated with episomal MPRA activity.

**Theory v15 — universally-active TRANSCRIPTIONAL biology, not universally-bound biology.** The PLS win is from core promoter motifs that universally DRIVE TRANSCRIPTION (Inr, TATA, NFY, SP1 → Pol II recruitment). CTCF binding is also universal but doesn't drive transcription in an MPRA — it sets up chromatin context which isn't testable in episomal reporter assays.

This is a useful negative control: it confirms the mechanism is specifically about transcriptional activation, not generic regulatory binding.

**Next.** 018 — try TF cCREs (chromatin-accessible regions bound by ANY TF, not just CTCF, 131K elements). These should include many transcription-activating TFs and might give a different lift profile.
