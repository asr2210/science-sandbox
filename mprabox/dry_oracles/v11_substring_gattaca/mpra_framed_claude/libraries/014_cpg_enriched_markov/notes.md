# 014 CpG-enriched 1st-order Markov chain

50k 200bp sequences from a Markov chain with T[C→G]=0.50 (vs iid 0.275).
Stationary marginal came out to GC=0.49 (not 0.55 as planned — chain
construction was approximate). CpG dinucleotide rate=0.117 vs iid ~0.060.

## Result
- mean_r = 0.858 (eval_01 = 0.872) — NEW BEST eval_01
- vs GC=0.55 uniform (exp 012): +0.001 mean, +0.004 eval_01
- HepG2 ↑ to ~0.90 (was 0.88 at GC=0.55, ~0.86 at GC=0.6)
- K562 ↓ slightly (0.85)
- SKNSH ↓ slightly (0.86)

## Takeaway
**The model CAN extract dinucleotide signal.** CpG enrichment helped HepG2
substantially while keeping other cells roughly stable. This is the first
non-composition lever I've found that works.

The fact that CpG matters for HepG2 specifically makes biological sense:
hepatocyte regulatory regions include CpG island promoters that are active
in liver. Tissue-specific CpG island composition shifts MPRA response.

## Next
Push CpG enrichment harder and tune GC to 0.55 (instead of 0.49) for the
best of both signals.
