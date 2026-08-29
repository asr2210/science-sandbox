# 006 — Mononucleotide-shuffled cCREs

**Design.** Same 50K cCRE windows as 003, but each sequence's bases are independently shuffled. Preserves 1-mer composition (GC content) exactly. Destroys all motifs and dinucleotide-level structure.

**Result.** eval_01 = **0.3682** — worst yet. K562 = 0.510, HepG2 = 0.533, SK-N-SH = 0.062.

| | K562 | HepG2 | SK-N-SH | mean_r |
|---|---|---|---|---|
| 001 random (50% GC) | 0.590 | 0.623 | 0.045 | 0.419 |
| 003 real cCRE | 0.546 | 0.558 | **0.079** | 0.394 |
| **006 shuffled cCRE** | **0.510** | **0.533** | **0.062** | **0.368** |

GC content: random=50.0%, real cCRE=48.8%, shuffled cCRE=48.9%.

**Disentanglement.**
- K562/HepG2 r decomposition: random (50% GC) → 0.59/0.62. Shuffled cCRE (48.8% GC, no motifs) → 0.51/0.53 (Δ-0.08/-0.09). Real cCRE (motifs added back) → 0.55/0.56 (Δ+0.04/+0.03 vs shuffled). So *both* composition (dominant) and motifs contribute to K562/HepG2 r.
- SK-N-SH r decomposition: random → 0.045. Shuffled cCRE → 0.062 (Δ+0.017 from composition alone). Real cCRE → 0.079 (Δ+0.017 from motifs on top of composition). Composition and motifs contribute ~equally to SK-N-SH.

**Theory v6.** The K562/HepG2 r ceiling appears to be set by the *match* between training and eval k-mer/composition statistics. Uniform random happens to match the K562/HepG2 eval distribution best. Real biology (even with all its motifs) underperforms because its composition diverges from what the eval expects, even though its motifs add a small recovery.

For SK-N-SH, eval composition is shifted toward biology-like, and real motifs add modest extra lift.

**Implications for library design.**
- Random's K562/HepG2 r ≈ 0.6 may be near the *ceiling* given training-eval composition matching. Hard to beat without changing composition.
- To lift SK-N-SH WITHOUT hurting K562/HepG2, biology must be added in a way that doesn't shift overall composition.
- Direct route: random background + planted real motif INSTANCES (PWM-sampled, longer than consensus, with realistic flanking) — but 002 used short consensuses and didn't help. Need to try with longer/PWM-sampled motifs.

**Open question.** Is the uniform random 0.6 truly a ceiling for K562/HepG2 r, or can a smarter library push above?

**Next.** Test variable-GC random — sequences with GC content drawn uniformly from [0.25, 0.75]. If the model trained on variable-GC random has K562/HepG2 r similar to uniform-50%-GC random, then the eval is robust to composition breadth and we're free to add biology. If variable-GC drops K562/HepG2 r, the eval is composition-narrow and we have very limited room to add biology.
