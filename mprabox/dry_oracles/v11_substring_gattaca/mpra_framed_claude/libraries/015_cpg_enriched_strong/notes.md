# 015 Stronger CpG-enriched Markov chain at GC=0.55

50k 200bp sequences from a Markov chain with T[C→G]=0.65 (vs 0.50 in exp 014).
Realized stationary GC=0.55, realized CpG dinucleotide rate=0.179
(vs 0.117 in 014, vs iid ~0.076).

## Result
- **mean_r = 0.868** — NEW BEST (prev best 0.858 at exp 014)
- **eval_01 = 0.884** — NEW BEST (prev best 0.872 at exp 014)
- +0.010 mean, +0.012 eval_01 vs exp 014. Well above noise (~0.003).

Cell-type breakdown (averaged across evals 01,02,05,06,14 — the easy "main" evals):
- K562 ≈ 0.83 (unchanged from exp 014's 0.83)
- HepG2 ≈ 0.90 (unchanged from exp 014's 0.90)
- SKNSH ≈ 0.92 (UP from exp 014's 0.86 — big jump)

## Takeaway
**CpG enrichment is a strong, monotone lever.** Pushing T[C→G] from 0.50→0.65
and fixing GC to 0.55 added +0.010 mean and lifted SKNSH from 0.86 to 0.92.

SKNSH (neuronal) actually benefited more from the stronger CpG signal than
HepG2 did this time. Possible explanation: at the right GC (0.55, not 0.49),
the CpG signal is interpretable by the model as an island-like signature
that all three cell types use to varying degrees.

Hard evals (07, 08, 10, 13) still drag: K562 on eval_08 = 0.54 is the
biggest weakness. eval_07 K562 = 0.76 also weak. These may be hard cell
types or perturbed K562 conditions.

## Next
Two paths to consider:
1. Push T[C→G] even harder (0.75, 0.85) — find the plateau
2. Add a second dinucleotide bias (e.g., depleted TpA, which is also a real
   regulatory signal — TA is unstable / depleted in CpG islands)

Option 2 is more interesting because it tests whether the model has
capacity for multiple dinucleotide signals at once. Run exp 016 with
T[C→G]=0.65 plus depleted T→A (TpA depletion).
