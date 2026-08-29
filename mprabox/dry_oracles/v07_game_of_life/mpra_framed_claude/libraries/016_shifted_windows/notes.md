# Experiment 016 — shifted-window augmentation

## Design
10K random anchor positions in hg38 (length-weighted). For each
anchor, 5 windows at offsets [-50, -25, 0, +25, +50] centered on
the anchor. Total 50K, but only 10K unique "scenes."

## Result
- eval_01: 0.3882 (Δ +0.0006 vs natural baseline 0.3876)
- K562: 0.5965, HepG2: 0.4234, SK-N-SH: 0.1446

Within noise of plain natural. **Augmentation is neutral.**

## Interpretation
Effectively 5x redundancy on 10K unique anchors. The model
generalizes the same as on 50K independent natural windows.
So:
- The model is not bottlenecked by # unique training scenes at N=10K
- Or shift-invariance is already easy / baked into the architecture
- Or shifts of ±50bp don't materially change the regulatory context

Either way: training-time augmentation via offset jitter is not a
lever for this task.

## Cumulative result table
| design | eval_01 | mechanism |
|---|---|---|
| 4-way mix s=1 (010) | 0.3961 | GC + reg (high noise sample) |
| GC + reg (015) | 0.3945 | GC + reg combined |
| GC-strat (014) | 0.3939 | GC balance |
| max diversity (009) | 0.3939 | broad mix |
| 4-way mix s=0 (002) | 0.3937 | GC + reg |
| activity contrast (005) | 0.3934 | GC + reg |
| activity quintiles (004) | 0.3919 | reg-only stratification |
| minimal reg (013) | 0.3893 | low reg dose |
| RC aug (012) | 0.3883 | RC augmentation |
| **shifted aug (016)** | **0.3882** | **window jitter** |
| mouse-only (006) | 0.3880 | cross-species |
| natural (001) | 0.3876 | length-weighted |
| TF-density (011) | 0.3831 | regulatory excess |
| dinuc shuffle (007) | 0.3733 | composition only |
| random uniform (008) | 0.3689 | no structure |

The ceiling cluster (0.394 ± 0.002) is reached by 5+ designs that
all involve GC distribution balancing. Nothing has pushed beyond.

## Next plan
Try GC-shape variants — does eval expect uniform GC or skewed GC?
- exp 017: high-GC heavy (30K high-GC + 15K low + 5K mid)
- If lifts: eval is high-GC, oversampling helps
- If drops: uniform GC was already optimal
