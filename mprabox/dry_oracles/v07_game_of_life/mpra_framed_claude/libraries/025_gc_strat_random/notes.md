# Experiment 025 — GC-stratified random uniform DNA

## Design
50K i.i.d. random DNA, 10K per GC bin. Each bin uses per-base
probabilities tuned to hit the target GC (0.30, 0.40, 0.50, 0.60,
0.70). NO motifs, NO natural syntax — only GC composition is
controlled.

## Result
- eval_01: 0.3899 (Δ −0.0040 vs GC-strat natural, +0.0210 vs random uniform)
- K562: 0.6041, HepG2: 0.4249, SK-N-SH: 0.1407

## Interpretation — the decomposition
| Library | eval_01 | Δ vs ceiling |
|---|---|---|
| Random uniform 40% GC (exp 008) | 0.3689 | −0.025 |
| GC-strat random uniform (this) | 0.3899 | −0.004 |
| GC-strat natural (exp 014) | 0.3939 | 0 |
| 4-way ceiling (best) | 0.3961 | +0.002 |

GC stratification of random sequence closes **84%** of the gap between
random uniform and natural (+0.021 of the +0.025 gap). The remaining
**16%** (+0.004) is real (>3σ noise) — driven by motif/syntax content
that random sequences lack.

## Refines T8 → T11
**T11: GC composition is necessary and almost sufficient.** Matching
the natural GC distribution alone delivers ~84% of the achievable
mean_r. Real natural sequence content (motifs, dinuc structure)
contributes a small but reproducible additional gain of ~0.004.

So a maximally informative library is NOT "all GC-stratified random."
The motif premium is real but small relative to the GC effect.

## Implication
Library design priority is:
1. **GC distribution** (huge effect, +0.025)
2. **Motif/syntax content** (small effect, +0.004)
3. Source identity (zero effect once 1 & 2 are met)

## Next direction (exp 026)
Decompose the +0.004 "motif premium" further. What aspect of natural
sequence delivers it? Candidates:
- **Dinucleotide content** (CpG depletion, dinuc biases)
- **k-mer content** (trinucleotide, longer)
- **Actual TFBS motifs**

Plan: dinucleotide-shuffle of GC-strat natural. Preserves both GC AND
dinuc but destroys higher-order motif positions. If matches ceiling →
dinuc is the residual. If falls back toward GC-strat random → real
motifs matter.
