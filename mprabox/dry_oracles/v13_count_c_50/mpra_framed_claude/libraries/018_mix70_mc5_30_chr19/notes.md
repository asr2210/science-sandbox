# Experiment 018 — chr19-only genomic supplement (composition substitution)

## Result vs cCRE supplements
| eval | 013 (real cCRE) | 017 (shuffled cCRE) | 018 (chr19) | 018 vs 013 |
|------|-----------------|---------------------|-------------|------------|
| 01 ★ | 0.5765 | 0.5761 | 0.5625 | **-0.014** |
| 04 | 0.5774 | 0.5766 | 0.5469 | -0.031 |
| 07 | 0.6037 | 0.6024 | 0.6083 | +0.005 |
| 08 | 0.1730 | 0.1884 | 0.1005 | **-0.073** |
| 13 | 0.5865 | 0.5852 | 0.5927 | +0.006 |

## Library composition
| library | supp GC mean | lib GC mean | lib GC std |
|---------|--------------|-------------|------------|
| 013 (cCRE) | ~0.55 | 0.460 | 0.1152 |
| 017 (shuf) | ~0.55 (preserved) | 0.459 | 0.1153 |
| 018 (chr19) | 0.478 | 0.445 | 0.1030 |

## Conclusion: not "high GC" — the SHAPE of the GC distribution matters
The chr19 supplement raises GC less (0.478 vs ~0.55) and narrows the
spread (std 0.103 vs 0.115). Eval_08, which is composition-sensitive,
collapses from 0.17 → 0.10. eval_01 drops 0.014.

So theory v12 ("composition fully explains") needs refinement:
**It's not motif identity, but it's not just mean GC either.**
The SPECIFIC dinuc/GC distribution of cCREs — long tail of CpG-island-
like high-GC sequences — is what supplies the eval-relevant composition.

## Theory v13
The supplement supplies a *distribution* of compositions. cCREs happen
to have a wide GC distribution that overlaps the eval distribution well,
particularly in the high-GC tail that eval_08 needs. Uniform chromosomes
miss the high-GC tail.

Two paths forward:
1. SHARPER composition recipe — explicitly select high-GC genomic windows
   (cheap, no curation needed)
2. EVEN MORE high-GC — use CpG island annotations as supplement
