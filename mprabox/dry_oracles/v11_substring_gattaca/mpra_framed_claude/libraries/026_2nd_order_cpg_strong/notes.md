# 026 Stronger 2nd-order CpG clustering

P(C|CG)=0.60, P(G|GC)=0.85. Realized GC=0.70, CpG=0.26, CGCG=17/seq.

## Result
mean_r=0.878, eval_01=0.894. Down -0.001 from 025 (within noise). Peak.

The 025 setup (P(C|CG)=0.50, P(G|GC)=0.75) is the local max for this
override pattern. Going stronger pushes GC and CpG too high (similar to
exp 016 going past T[C→G]=0.65 at GC=0.55).

## Next
Try richer 2nd-order: add CCG, GGC overrides (more diverse CpG-island
trinucleotide structure).
