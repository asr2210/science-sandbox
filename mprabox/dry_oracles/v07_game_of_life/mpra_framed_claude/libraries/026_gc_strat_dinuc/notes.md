# Experiment 026 — GC-stratified dinuc-shuffled natural

## Design
50K dinucleotide-shuffled natural windows, 10K per GC bin.
Preserves GC + natural dinucleotide frequencies (CpG depletion).
Destroys all k-mer structure k≥3 (motifs, codons, repeats).

## Result
- eval_01: 0.3853 (Δ −0.0086 vs GC-strat natural, −0.0046 vs GC-strat random)
- K562: 0.5923, HepG2: 0.4199, SK-N-SH: 0.1437

## The cleanest decomposition
| library | GC | dinuc | motif | eval_01 | gain |
|---|---|---|---|---|---|
| random uniform 40% GC (008) | 40% | flat | none | 0.3689 | — |
| dinuc-shuffled nat (007) | natural | natural | none | 0.3733 | +0.004 |
| GC-strat random (025) | strat | flat | none | 0.3899 | +0.021 from GC |
| GC-strat dinuc (this) | strat | natural | none | 0.3853 | −0.005 dinuc vs flat |
| GC-strat natural (014) | strat | natural | yes | 0.3939 | +0.009 motifs vs dinuc |
| 4-way ceiling | mixed | natural | yes | 0.3951 | +0.001 |

## Surprising finding
Natural-like dinucleotide content (CpG depletion) is **slightly
detrimental** at matched GC (−0.005). I.i.d. random outperforms
natural-dinuc under GC control. Possible reasons:
- Eval may not have natural CpG depletion (e.g., MPRA synthetic
  inserts), so dinuc-matching to hg38 mismatches eval.
- Reduced effective sequence diversity from dinuc constraints.
- At extreme GC bins (>65%), dinuc shuffle struggles to produce
  varied sequences from CpG-depleted source.

## T11 → T12
**Decomposition of the random-to-natural lift (+0.025):**
- **GC composition: +0.021** (dominant)
- **Higher-order motifs (k≥3): +0.009** (above i.i.d. random)
- **Dinucleotide structure (natural): −0.005** (slightly negative)

So the motif premium isn't k=2; it's real motif content. And
natural-DNA dinuc statistics are slightly *worse* than i.i.d.
under GC control.

## Implication for library design
- Maximize GC distribution coverage (huge lever)
- Use natural sequence (for motifs) — don't shuffle
- Dinuc-shuffle is a poor synthetic substitute

## Next direction (exp 027)
Test whether real motifs of various complexity drive the +0.009.
Plant explicit TFBS PWM matches into GC-strat random scaffolds.
Or: use only sequences containing high-information k-mers (k=6
or k=8). If motif "doses" lift mean_r linearly, motif content
itself is the actual lever.
