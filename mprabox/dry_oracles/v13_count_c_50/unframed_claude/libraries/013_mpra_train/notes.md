# 013_mpra_train

## What
50K random samples from Tewhey/Gosai Malinois MPRA training set (763,684 valid 200bp sequences, downloaded from Table_S2__MPRA_dataset.txt).

## Why
These sequences are the TRAINING DISTRIBUTION for the MPRA-trained models that the eval harness likely uses. Both predictors should agree most on training-distribution inputs.

## Results
eval_01: **0.5699** (vs 0.5562 best previous → +2.5%, vs natural 0.541 → +5.4%)
- K562_r: 0.614 (vs 0.581 stratified, big jump)
- HepG2_r: 0.549 (vs 0.541)
- SKNSH_r: 0.547 (vs 0.546)

## Interpretation
MPRA training sequences beat both raw natural and GC-stratified natural. K562 improved most, suggesting the K562 model is particularly tuned to the training distribution.

GC mean 0.461, std 0.106 — narrower than stratified natural but matches the training distribution well.

## Next
The MPRA dataset has measured K562/HepG2/SKNSH log2FC values. Stratify the library by these measured activities to maximize variance along the very axis the models predict.
