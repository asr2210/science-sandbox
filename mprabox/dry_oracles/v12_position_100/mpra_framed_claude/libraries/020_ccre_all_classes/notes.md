# Experiment 020: Pure cCRE all 8 classes

## Design
50K pure cCREs across all 8 V4 Registry classes:
- 17K dELS, 6K pELS, 6K CA, 5K CA-CTCF, 5K TF, 5K CA-H3K4me3, 4K PLS, 2K CA-TF
No peaks, no random. Seed=20.

## Result
eval_01 = **0.0743**. K562=0.0777, HepG2=0.0784, SKNSH=0.0669.
In noise band as expected.

## What I learned
**Even broader cCRE class diversity doesn't break the band.** Previously
my "CA_TF" bucket lumped CA, TF, CA-H3K4me3 together; explicitly sampling
each separately gives the same result. The class labels don't carry
additional learnable structure that the model exploits.
