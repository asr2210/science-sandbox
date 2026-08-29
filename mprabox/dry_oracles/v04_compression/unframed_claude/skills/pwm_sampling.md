# Skill: PWM-sampled motif insertion

## When to use
Generating MPRA-style libraries where you want to add real TF binding-site
content WITHOUT homogenizing the library. Beats hardcoded consensus strings.

## Why it works
The black-box scorer rewards FUZZY PWM-shaped motifs (consistent with a
predictor trained on real ChIP-seq / MPRA data). Rigid consensus strings
were flat or slightly hurt (exp 003); PWM-sampled motifs gave +0.05 on
eval_01 (exp 010).

## How

```python
from pyjaspar import jaspardb
import numpy as np
ALPHABET = list("ACGT")

j = jaspardb(release="JASPAR2024")
motifs = []
for name in ["SP1", "MYC", "MAX", "USF1", "CREB1", "JUN", "GATA1", "ELK1",
             "NRF1", "YY1", "NFYA", "KLF4", "EGR1"]:
    ms = j.fetch_motifs(species="9606", collection="CORE", tf_name=name)
    if ms:
        m = ms[0]
        counts = np.array([m.counts[b] for b in ALPHABET], dtype=float)
        probs = counts / counts.sum(axis=0, keepdims=True)
        motifs.append((name, probs))

def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))
```

## Tuning knobs to try
- Number of motifs per sequence (3 worked; try 5, 8)
- Number of TFs in the bank (17 worked; try all 720)
- Whether to RC half the motifs (yes seems fine)
- Position constraints (random vs centered)
- Larger TF bank means lower duplication, more "natural" coverage

## Caveat
Don't pack so densely that library composition drifts off uniform random
(exp 004 packed ~20 motifs/seq and scored 0.17 — too far).
