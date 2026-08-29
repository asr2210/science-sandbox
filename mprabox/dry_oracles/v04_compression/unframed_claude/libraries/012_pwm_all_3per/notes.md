# 012 — All 717 JASPAR PWMs, 3 motifs/seq

## Hypothesis
TF diversity (717 vs 17 PWMs) might help further on top of exp 010.

## Results
eval_01 = 0.3365 (exp 010 with 17 TFs: 0.3644). **Drop of 0.03.**

But:
- eval_07: 0.4382 (better than 010's 0.4002 by +0.04)
- eval_08: 0.1058 (better than 010's 0.0871)
- eval_13: 0.4333 (better than 010's 0.4171)

So more TFs help SOME evals (07, 08, 13) and hurt others (01, 03, 04, 06, 10).

## Key insight
Different evals like different TF subsets. My exp 010 set of 17 TFs happened
to be well-matched for eval_01 / eval_03 / eval_04 / eval_10 — likely
predictors trained on universal regulators that are well-represented in
that set. The 700 additional motifs add noise on eval_01.

## Next
Curate a moderate-sized set (~30-50 TFs) targeting eval_01 specifically:
- Keep the strong ones from exp 010
- Add cell-type-specific TFs (K562: GATA1/KLF1/EGR1/TAL1, HepG2: HNF4/CEBP/FOXA, SK-N-SH: ASCL1/REST/NEUROD1/MEF2C)
- Test density variants 2, 4, 5 motifs/seq
