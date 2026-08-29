# 011 — Sharpr-MPRA filtered to GC ∈ [0.45, 0.55]

## Design
Same as 009 but only fragments with 145bp-internal GC in [0.45, 0.55] (n=317,992 available, sampled 50k). Padded with random uniform flanks for overall GC=0.503.

## Result
- eval_01 mean_r = **0.4978** (vs full Sharpr 0.4987, random uniform 0.5177)
- K562 r = 0.940 (vs full Sharpr 0.929, random uniform 0.994)
- HepG2 r = 0.559 (vs full Sharpr 0.547)
- SK-N-SH r = -0.006

## Reading
GC filtering to match the eval distribution didn't help — actually slightly worse. K562 r jumped from 0.929 to 0.940 (composition fix), but HepG2 also moved slightly. The net effect is identical to full Sharpr within noise.

**The eval doesn't just care about GC. It cares about the FULL composition profile.** Real DNA fragments — even GC-matched ones — have dinucleotide and higher-order correlations that random uniform doesn't have. The model trained on real-DNA fragments is being evaluated on what behaves like random uniform.

## Implication
Real MPRA sequences can't be salvaged by composition matching alone. Their multi-nucleotide structure is the issue. Time to test fixed-position motifs (exp 012) and very narrow GC variations (exp 013).
