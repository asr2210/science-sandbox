# 017_chipseq_k562_hepg2_sknsh

## Setup
50k TF ChIP-seq peaks from ENCODE TFBS clusters
(encRegTfbsClusteredWithCells.hg38.bed.gz, 10.5M entries). Filtered to
peaks observed in K562 (17k), HepG2 (17k), SK-N-SH (16k). Deduped by
200bp genomic bin so co-bound clusters don't oversample.

After dedupe per cell:
- K562: 961k unique 200bp bins
- HepG2: 711k unique 200bp bins
- SK-N-SH: 215k unique 200bp bins

## Result
- eval_01 = 0.6900 vs cCRE 0.6921 (tied, −0.002)
- eval_04 = 0.6012 vs cCRE 0.5977 (+0.004, tiny lift)
- eval_07 = 0.7483 vs cCRE 0.7562 (−0.008)
- eval_08 = 0.1266 vs cCRE 0.1248 (+0.002)
- eval_10 = 0.6634 vs cCRE 0.6673 (~tied)
- eval_13 = 0.7363 vs cCRE 0.7466 (−0.010)

## Interpretation
ChIP-seq peaks — direct evidence of TF binding in the exact target
cell types — give the same eval_01 as cCREs. This is striking.

The 0.69 ceiling now holds across **3 qualitatively different data
sources**:
1. cCREs (biochemical regulatory annotation): 0.6921
2. Random Malinois MPRA (measured oligos in target CTs): 0.6856
3. K562/HepG2/SK-N-SH ChIP-seq peaks (direct TF binding): 0.6900

## Theory update → T9 — STRONG ceiling
The ~0.69 eval_01 ceiling is not about training-data *source* — it's
intrinsic. Likely cause:
1. **Model capacity / training time bottleneck**: 30s training saturates
   the model regardless of input quality
2. **Eval intrinsic noise floor** at ~0.69 (e.g., measurement noise in
   the eval set caps achievable correlation)

Either way, no library-design lever within biological regulatory
sequences will move eval_01 above ~0.70. Need to either:
- find a *qualitatively different* signal type the model isn't getting
  (synthetic curriculum? motif-enriched composites?)
- accept the ceiling and optimize other evals

## Takeaway
Pivot strategy: stop searching for the eval_01 lever. Either it
doesn't exist or it's outside my design space. Instead, focus on
*not regressing* eval_01 while studying the other axes (eval_04,
eval_08) that DO respond to library choice. The cCRE library at 0.6921
is the practical winner.
