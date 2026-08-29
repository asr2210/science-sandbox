# 003 genome_random_windows

**Design:** 50k random 200bp windows sampled uniformly from chr17 + chr19 + chr22 (after rejecting any window containing N). Seed 7.

**Result:** eval_01 = 0.0752. Mean ≈ 0.094.

**Interpretation:** Random human DNA barely beats dinucleotide-Markov (0.0730) and is far from the gold-standard ~0.7. Confirms that **regulatory specificity** matters, not generic human DNA — most of the genome is intergenic/intronic and lacks the dense motif structure the model needs to learn from. Next: target ENCODE cCREs (~1M regulatory elements, ~200-400bp each).
