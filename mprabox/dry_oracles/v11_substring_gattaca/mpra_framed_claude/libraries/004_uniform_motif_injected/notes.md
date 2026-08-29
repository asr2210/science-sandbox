# 004 uniform + JASPAR motif consensus (λ=3)

Random uniform 200bp background; for each, injected k~Poisson(3) motif
consensus strings sampled uniformly from JASPAR2024 vertebrate CORE (879
motifs). Avg 2.99 motifs/seq, ~30bp of motif content per sequence.

## Result
- mean_r = 0.836 (eval_01 = 0.849)
- Random uniform alone scored mean_r=0.852 (eval_01=0.862)
- Worse on every eval, by 0.005–0.025

## Takeaway
Motif consensus injection at this density very slightly hurt. Possible reasons:
1. Motifs displaced random k-mer coverage the model was relying on
2. Consensus-only injection is too repetitive — same ~879 strings repeat ~170×
   each → adds bias the model overfits to
3. Model architecture cannot extract motif-level signal effectively

Next: test whether *composition variance* is the lever (GC-varied uniform).
