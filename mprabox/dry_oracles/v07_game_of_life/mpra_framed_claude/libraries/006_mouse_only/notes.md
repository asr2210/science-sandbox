# Experiment 006 — 50K mouse-only natural

## Design
50K random 200bp windows from mm39 (chr1-19, X, Y), length-weighted.

## Result
- eval_01: 0.388 (Δ +0.000 vs exp 001 human-only at 0.388)
- K562: 0.596 (vs 0.596), HepG2: 0.423 (vs 0.423), SK-N-SH: 0.145 (vs 0.143)

## Major finding
Mouse natural ≈ human natural across every metric. The eval set is
species-agnostic. The model is learning CONSERVED regulatory grammar,
not human-specific features.

## Implication
The dominant signal in MPRA-eval performance is **naturalness of the
sequence distribution**, not species, not regulatory-element selection.
This is a much stronger claim than I'd previously held.

If naturalness is the signal, what aspect of naturalness?
- Dinucleotide / k-mer composition?
- TF motif content at natural rates?
- Higher-order syntactic patterns (motif spacing, repeats)?
- Cell-type-invariant chromatin context?

Need a dinucleotide-shuffle test to disambiguate.
