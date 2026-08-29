50/50 mix random uniform + chr22. eval_01 mean=0.3966.
K562 0.540, HepG2 0.554, SKNSH 0.096.
The chr22 SKNSH boost is preserved in the mix, but the K562/HepG2 hit
from chr22 also propagates. Net mean (0.40) is worse than pure random (0.42).
Linear mixing alone doesn't separate the two effects.
The path to >0.42 mean is to find a sequence type that boosts SKNSH
WITHOUT hurting K562/HepG2. Real chr22 fails this — its drag on the
trained-on-MPRA predictors offsets any SKNSH gain.
