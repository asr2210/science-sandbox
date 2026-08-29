# 003 cCRE pan-tissue 200bp windows

50,000 windows centered on ENCODE V4 cCREs sampled uniformly from chr1/11/19/22
(~424k available). Type mix: 62% dELS, 14% pELS, 8% CA, 5% TF, 4% CA-CTCF,
3% CA-H3K4me3, 3% PLS, 1% CA-TF.

## Result
- mean_r = 0.694 (eval_01 = 0.702)
- Worse than random uniform (0.852), similar to random genomic (0.682)
- SK-N-SH still bottlenecked at 0.50–0.60
- Training time 40s — much slower than random uniform (11s), suggests cCRE
  sequences trigger more learnable structure but model still under-extracts it

## Key takeaway
**Enriching for known regulatory function did not help.** Random uniform >
cCREs > random genomic, but only by a small margin (cCRE > genomic by 0.012).

This argues against "label dynamic range" as the SOLE issue — cCREs should
have wider activity than random genomic but they performed nearly the same.
More likely the model is dominated by k-mer / composition features and
random uniform's flat k-mer distribution covers eval-set k-mer space best.

## Implication for next steps
The library that wins should combine random uniform's broad k-mer coverage
with explicit motif signal. Test motif-injection on random uniform background
in exp 004.
