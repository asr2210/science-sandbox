# 020_ca_tf_only — notes

## Design
50K x 200bp sampled WITH REPLACEMENT (~1.92x per element)
from the 26,102 CA-TF cCREs. Same central-200bp extraction.
CA-TF = chromatin-accessible region with TF binding (no
chromatin-mark evidence, no CTCF). Smallest SCREEN class.

## Result vs. other small-pool libraries

| eval | TF014 (105K)| PLS006 (47K)| CA-TF020 (26K) |
|------|-------------|-------------|----------------|
| 01   | 0.6509      | 0.5903      | **0.5128**     |
| 02   | 0.7333      | 0.6657      | **0.5808**     |
| 03   | 0.7229      | 0.6278      | **0.5639**     |
| 04   | 0.6793      | 0.7022      | **0.5634**     |
| 05   | 0.6514      | 0.5901      | **0.5127**     |
| 06   | 0.7344      | 0.6655      | **0.5808**     |
| 07   | 0.7160      | 0.5091      | **0.5378**     |
| 08   | 0.5401      | 0.4774      | **0.4085**     |
| 09   | 0.7324      | 0.7543      | **0.6063**     |
| 10   | 0.6842      | 0.5925      | **0.5571**     |
| 11   | 0.6411      | 0.5789      | **0.5036**     |
| 12   | 0.6227      | 0.5372      | **0.4817**     |
| 13   | 0.7177      | 0.4912      | **0.5191**     |
| 14   | 0.7327      | 0.6661      | **0.5811**     |

Mean: TF 0.683, PLS 0.604, **CA-TF 0.536** — worst single-class
library. Worst library OVERALL by 0.07 below PLS.

## Interpretation

**Hypothesis (B) "Pool too small" CONFIRMED, dramatically.**
The 26K-element pool with ~1.92x replication produces the worst
single-class library by a wide margin. The combination of:
1. Small pool (~26K unique vs typical 50K-249K)
2. Forced replication (each element seen ~2x in training)
3. Class-narrow grammar (CA-TF is itself a specialized
   sub-population)

stacks penalties multiplicatively. The model overfits to the
small repetitive set rather than learning generalizable grammar.

**Eval_08 collapses to 0.41** — the model trained on this
narrow library is essentially worse than chance on this eval.

**Cell-type ordering breaks!** Usually SKNSH > K562 > HepG2;
here SKNSH > HepG2 > K562. K562 in particular is hit hard
(0.48 vs typical 0.69 baseline). This is the first library
where K562 underperforms HepG2 systematically. CA-TF cCREs may
be poorly represented in K562, so a CA-TF-trained model has
worse K562 generalization specifically.

## Theory update

**New rule: pool size matters when below ~50K unique elements.**
At ~26K with replacement, pool diversity is so compressed that
the small per-element class quality cannot rescue performance.

This re-frames the earlier 016 RC result: halving the pool
from 50K → 25K cost only -0.017 because the underlying class
(pELS) was high-quality. Halving from 26K → effectively 13K
unique-pre-replication content (with 2x re-views) drops -0.07
or more because BOTH the pool size and the per-element quality
are weak.

**Single-class library matrix completed:**
| class       | pool   | mean   | evidence type           |
|-------------|--------|--------|-------------------------|
| pELS        | 249K   | 0.758  | DNase + chromatin marks |
| dELS        | 1.47M  | 0.756  | DNase + chromatin marks |
| CA-H3K4me3  | 79K    | 0.749  | DNase + H3K4me3         |
| CA          | 246K   | 0.718  | DNase only              |
| CA-CTCF     | 126K   | 0.710  | DNase + CTCF            |
| TF          | 105K   | 0.683  | TF-bound only           |
| PLS         | 47K    | 0.604  | TSS-proximal (location) |
| **CA-TF**   | **26K**| **0.536** | DNase + TF-bound (small)|

The hierarchy is now complete. The principle: **(evidence type
+ pool size) jointly predict library quality**. Strong
chromatin-mark evidence with > 50K elements: top tier (pELS,
dELS, CA-H3K4me3). Weak chromatin evidence or small pool:
mid-to-bottom.

## Next experiment

**Exp 021: pELS top-50K-LONGEST cCREs.** Pre-filter pELS pool
by element length, take 50K largest. Tests whether cCRE length
encodes a quality signal (longer = more reliably active /
more regulatory grammar). If length correlates with quality,
this could be the first lever to push past pELS-only's 0.758.
