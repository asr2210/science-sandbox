# Experiment 019: Multi-seed pool + revcomp augmentation

## Plan
Stack 018 (4 seeds x 12.5k) with 017 (50% revcomp). With pooling reducing
seed variance, if revcomp gives a real lift it should show as ~0.137-0.140.

## Result
- eval_01 mean_r = **0.1346** — no lift over 018 (0.1357) or 014 (0.1350)
- Revcomp augmentation = no-op (with variance properly controlled)

## Implication
The 017 result (0.1379) was likely just upper-tail noise. Multi-seed
pooling collapses both samplers to ~0.135.

## Theory update
Revcomp/pool both null. The scorer's response to "uniform-random hg38"
plateaus at ~0.135 +- 0.005. To beat this we need *structural* changes
in the input distribution — not just augmentation. Candidates:
- Promoter/TSS-proximal regions (regulatory density)
- ENCODE TF ChIP-seq peak windows (factor-bound regions)
- GC-content stratification (uniform vs natural GC)

## Next
020: Promoter-enriched library — windows centered on RefSeq TSS sites
(if available locally). Tests whether regulatory density matters more
than uniform genome sampling.
