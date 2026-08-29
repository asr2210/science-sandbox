# Experiment 002 — AP-1 motif at center

## What I tested
50,000 random 200bp seqs with TGAGTCA (canonical AP-1) inserted at pos 96-102.

## Result
eval_01: 0.331 → **0.278** (drop of ~0.05). Every single eval went DOWN.

## Interpretation
This contradicts T0 strongly. Three possible mechanisms:
1. **Variance reduction.** Identical 7bp at same position removes ~3.5% of sequence variance. If the score is Pearson r computed over our 50K library between two correlated predictors (or pred vs. some sequence-derived target), reducing variance in the library reduces the dynamic range of the predictions and lowers r.
2. **Motif-specific decorrelation.** AP-1 may activate one oracle (e.g., k562-trained) more than another, creating outliers that decorrelate them.
3. **Distribution shift.** Real-looking motif at fixed position is unnatural and pushes seqs out of the joint training distribution of whichever model(s) score.

(1) is most parsimonious given the uniform drop across all evals.

## Theory update → T1
**Diversity in the library matters.** Random uniform DNA gives substantial baseline r (~0.33) because the library spans the natural prediction range. Anything that reduces per-position entropy or makes sequences more similar to each other likely HURTS the score. We want to *maximize* across-library variance in the score-relevant signal.

## Next
Exp 003: bias library GC content into four bins (0.30, 0.45, 0.55, 0.70) — keeps per-position entropy but increases between-sequence variance in a salient axis. If T1 right, score goes up. If not, GC is not the right axis.
