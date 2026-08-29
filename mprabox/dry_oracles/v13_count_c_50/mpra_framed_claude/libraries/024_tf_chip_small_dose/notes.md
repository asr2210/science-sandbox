# 024 — Smaller TF ChIP dose (5%) displacing genomic

**Hypothesis:** Halve the exp 023 TF CRM dose (10%→5%) and displace
random genomic (not cCRE). Goal: capture some eval_08 OOD lift
without the eval_07/13 motif damage.

**Design:** 20k genomic + 20k cCRE 5-window + 5k CpGi 5-window
+ 2.5k TF CRM (TFs>=50, summit-centered) + 1.25k uniform + 1.25k shuffled.

**Results vs exp 020 (best, 0.5468) and exp 023 (10% TF, 0.5453):**

| eval | exp 020 | exp 023 | exp 024 | Δ vs 020 |
|------|---------|---------|---------|----------|
| 01   | 0.5778  | 0.5748  | 0.5764  | -0.001   |
| 04/09| 0.5660  | 0.5750  | 0.5676  | +0.002   |
| 07   | 0.6166  | 0.6012  | 0.6112  | -0.005   |
| 08   | 0.1751  | 0.2123  | 0.1878  | +0.013   |
| 10   | 0.5142  | 0.5087  | 0.5128  | -0.001   |
| 13   | 0.5963  | 0.5800  | 0.5906  | -0.006   |
| mean | 0.5468  | 0.5453  | **0.5455** | **-0.0013** |

**Findings — TF CRM tradeoff scales linearly with dose:**

5% gave ~1/3 of the 10% lift on eval_08 (+0.013 vs +0.038) AND
~1/3 of the motif drop on eval_07 (-0.005 vs -0.016) and eval_13
(-0.006 vs -0.017). The dose-response is monotonic — no sweet spot.

Net mean still loses to exp 020 by 0.0013 (outside seed noise).
TF ChIP CRM is **not** a useful library source at any dose I tried;
it trades motif gain for OOD gain with unfavorable ratio.

**Theory v6.9:** eval_08 is hard (always ~0.17-0.21) because the
test distribution is far from cCRE/genomic. TF CRMs help it because
they're an OOD source from the model's perspective, but they pollute
motif learning. Need an eval_08 lifter that doesn't overlap cCRE
PLS territory.

**Plan exp 025:** Try planted-motif synthetic sequences — insert
strong PWM hits (HOCOMOCO/JASPAR top TFs) into random backgrounds.
This is motif-dense WITHOUT being cCRE-redundant: should help
eval_07/13 without crowding cCRE diversity, and the synthetic
background may act as light OOD regularizer.
