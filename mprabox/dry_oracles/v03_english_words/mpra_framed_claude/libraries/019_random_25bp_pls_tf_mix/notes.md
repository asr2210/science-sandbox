# 019 — Random + 1x25bp: 50% PLS, 50% TF cCRE

**Design.** Half sequences get PLS 25bp fragment, half get TF 25bp fragment. All in 50/50 randomly-shuffled order.

**Result.** eval_01 = **0.4229** vs 012's 0.4248 (Δ-0.0019). K562 = 0.585, HepG2 = 0.611, SK-N-SH = **0.072** (highest yet).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 012 PLS | 0.591 | 0.619 | 0.065 | **0.4248** |
| 018 TF | 0.583 | 0.609 | 0.071 | 0.4210 |
| 019 50/50 PLS+TF | 0.585 | 0.611 | **0.072** | 0.4229 |

**Interpretation — mixing doesn't combine additively.** SK-N-SH stayed at TF-like 0.072 (good!) but K562/HepG2 dragged down to TF-like values, NOT PLS-like. The model's K562/HepG2 capability is compositionally limited — even half PLS sequences can't restore the K562/HepG2 ceiling once the other half has TF-like (lower GC) sequences.

**Theory v17 — composition is global, not per-sequence.** The model learns a global composition expectation from the training distribution. When half the training has TF-like composition, that pulls K562/HepG2 fit toward the average. SK-N-SH lift, by contrast, comes from specific motif patterns in training examples — and 25k TF sequences contain enough neural motif examples to fully capture the SK-N-SH lift.

**Implication for strategy.** To break 0.4248: keep ALL 50k sequences PLS-composition (preserve K562/HepG2), then ADD a small motif modification (per-sequence or per-subset) that selectively boosts SK-N-SH WITHOUT changing global composition.

**Next.** 020 — PLS fragments selected for high motif content. Scan each candidate 25bp PLS fragment for matches to canonical TF motifs (TATA, CCAAT, GC-box, E-box CAGCTG, NEUROD core); accept only fragments with ≥1 motif hit. Same composition class, denser motif content.
