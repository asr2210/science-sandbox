# Experiment 003: Real ENCODE cCRE genomic regulatory regions

## Design
50,000 200bp sequences sampled from hg38 at ENCODE Registry V4 cCRE
coordinates. Composition:
- 12,500 PLS (promoter-like; pool=46K)
- 12,500 pELS (proximal enhancer-like; pool=243K)
- 12,500 dELS (distal enhancer-like; pool=1.4M)
- 6,250 mixed CA-*/TF (pool=558K)
- 6,250 random autosomal background (non-cCRE)

Each cCRE centered to a 200bp window. N-windows rejected. Seed=3.

## Hypothesis
Real genomic regulatory DNA has natural TF motif content AND realistic
context (motif co-occurrence, biased base composition, real grammar) —
should give a much bigger jump than synthetic motif insertion.

## Results vs exp 001 (baseline)
| eval | 001 random | 003 cCREs | Δ | % gain |
|---|---|---|---|---|
| 01 | 0.0619 | **0.0758** | +0.014 | +22% |
| 02 | 0.0601 | 0.0742 | +0.014 | +23% |
| 03 | 0.0756 | 0.0949 | +0.019 | +26% |
| 04 | 0.0737 | 0.0863 | +0.013 | +17% |
| 06 | 0.0615 | 0.0753 | +0.014 | +22% |
| 07 | 0.1219 | 0.1444 | +0.023 | +18% |
| 08 | 0.0442 | 0.0652 | +0.021 | **+48%** |
| 10 | 0.1176 | 0.1277 | +0.010 | +9% |
| 13 | 0.1220 | 0.1429 | +0.021 | +17% |

All sets improved. Largest gains on eval_08 (+48%) and eval_03 (+26%).
Time: 53s.

## Per-cell-type observation
K562 and HepG2 scores improved more than SKNSH on most sets. SKNSH still
the hardest cell type to predict. Possibly:
1. cCREs are enriched for blood/liver-relevant TFs (more ENCODE data)
2. SKNSH is a neuroblastoma line; neural-specific regulatory grammar is
   underrepresented in our cCRE pool

## What I learned
- Real genomic sequence content is **massively more informative** than
  random or motif-augmented random.
- The same model architecture (we didn't change prepare.py) learns much
  better when given naturalistic sequence input.
- Suggests the model relies on context, not just motif presence.
- The 22% jump on eval_01 is a strong baseline to beat in the next 27
  experiments.

## Next
Test whether the 6,250 random background sequences are helping or hurting.
- Option A: drop random background, use all 50K as cCREs (more diverse)
- Option B: replace random with dinucleotide-shuffled cCREs (cleaner
  motif-free negative control)
- Choose A first: more regulatory diversity is the cleanest hypothesis.
