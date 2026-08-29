# 007 — 50/50 mixture random uniform + cCREs

## Design
25,000 random uniform 200bp + 25,000 stratified cCREs (8 classes). Shuffled.

## Result
- eval_01 mean_r = **0.4927** — between pure cCREs (0.496) and pure random uniform (0.518), but closer to cCREs
- K562 r = 0.9109 (vs random uniform 0.994, cCREs 0.928)
- HepG2 r = 0.5603 — basically unchanged from either pure
- SK-N-SH r = 0.0070 — minimal lift, within noise
- Random uniform half had GC=0.500; cCRE half had GC=0.473

## Reading
The mixture HURT versus random uniform. The cCRE half dragged K562 down without compensating elsewhere. Heterogeneous training data is harmful here — the model seems to do worse when trained on a mixture than on either pure component.

## Implication
Mixing doesn't help. The composition-matching effect is large enough that even 50% off-distribution training data tanks K562. Going forward, modifications that preserve random uniform composition exactly are the only ones with a chance.
