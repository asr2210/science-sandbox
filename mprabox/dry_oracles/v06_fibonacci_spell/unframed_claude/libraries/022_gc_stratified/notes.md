# Experiment 022: GC-stratified hg38 sampling

## Plan
Force 4 equal GC buckets (30-40, 40-50, 50-60, 60-70%) at 12.5k each.
Tests whether flattening GC distribution beyond natural-peaked helps.

## Result
- eval_01 mean_r = **0.1347** — within noise of natural random (~0.135)
- The 60-70% GC bucket took 502k attempts to fill (very rare in hg38)
- No net effect on score: flattening GC neither helps nor hurts much

## Implication
Even strongly altering the GC distribution doesn't move the needle.
The model is robust to GC distribution changes — what matters is the
*local* genomic context, and that's preserved either way.

## Next
Try greedy 10-mer coverage from larger candidate pool (4^10 = 1M kmers
won't saturate at 50k * 190 events). Will test if greedy diversity at
unsaturating k helps. If not, moving to mixed mega-library + final.
