# Exp 013 — Mixed DHS peaks (K562 + HepG2 + SK-N-SH from chr1/18/19/22)

50k 200bp windows centered on ENCODE DNase-seq narrowPeak peaks
(equal parts K562, HepG2, SK-N-SH).

## Result

| metric  | chr22 random | DHS mixed |
|---------|-------------:|----------:|
| eval_01 | 0.3202       | 0.2674    |
| k562    | 0.1443       | 0.1286    |
| hepg2   | 0.1990       | 0.0510    |
| sknsh   | 0.6173       | 0.6226    |

DHS peaks crashed HepG2 (-0.148). Reason: open chromatin regions
are GC-rich (~58% mean GC vs 47% for chr22 average). HepG2 model
strongly prefers AT-context.

| set | chr22 mean GC |
|-----|-------------:|
| K562 DHS | 0.577 |
| HepG2 DHS | 0.558 |
| SKNSH DHS | 0.606 |
| chr22 random | 0.470 |

Lesson: DHS-enrichment ≠ MPRA-friendly. The model rewards real GENOMIC
composition (CpG-depleted, AT-biased context), not just open chromatin
or known regulatory motifs.

K562 model: even K562 DHS peaks didn't boost K562 score over chr22
random. The model isn't tracking "K562-active" — it's tracking
"natural DNA composition with right GC".
