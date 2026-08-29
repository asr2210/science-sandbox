# Exp 011 — Real chr22 DNA + light motif augmentation

Real chr22 windows (same as exp 009) + 3 strong universal activator
motifs (AP-1, SP1, NFY, CRE, E-box) inserted per sequence.

## Result

| metric  | real chr22 alone | + 3 motifs |
|---------|-----------------:|-----------:|
| eval_01 | 0.3202           | 0.3152     |
| k562    | 0.1443           | 0.1443     |
| hepg2   | 0.1990           | 0.1911     |
| sknsh   | 0.6173           | 0.6102     |

Motif insertion mildly displaces useful natural content. HepG2 -0.008,
SKNSH -0.007, K562 unchanged. Real DNA is already near-optimal for the
features the model rewards; injecting synthetic motifs is a small net
negative.

Conclusion: don't disturb natural sequences. Look for BETTER natural
sequences instead.
