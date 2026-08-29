# Skill: Parse JASPAR motifs and sample realizations

## Data
- File: `data/jaspar2024_vert.meme` (879 motifs, JASPAR 2024 CORE vertebrates non-redundant).
- Full vertebrate-or-broader file: `data/jaspar2024_core.meme` (2346 motifs).
- Source: `https://jaspar.elixir.no/download/data/2024/CORE/...`.

## MEME format parsing
Each motif begins with `MOTIF MA0004.1 Arnt` and is followed by `letter-probability matrix: alength= 4 w= W nsites=... E=...`, then W rows of 4 floats (A, C, G, T probabilities at each position).

## Reference parser
```python
def parse_meme(path):
    motifs = []
    with open(path) as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("MOTIF "):
            parts = line.split()
            mid, name = parts[1], parts[2] if len(parts) > 2 else parts[1]
            # find the letter-probability matrix
            while i < len(lines) and not lines[i].startswith("letter-probability"):
                i += 1
            header = lines[i].split()
            w = int(header[header.index("w=") + 1])
            i += 1
            pwm = []
            for _ in range(w):
                pwm.append([float(x) for x in lines[i].split()])
                i += 1
            motifs.append((mid, name, pwm))
        else:
            i += 1
    return motifs
```

## Sampling a realization from a PWM
For each row (position), draw a base from the row's probability distribution. To make instances stronger (consensus-like), one can use `argmax` per row. To make instances diverse (representative of weaker binding), draw stochastically.

```python
import numpy as np

def sample_from_pwm(pwm, rng, mode="stochastic"):
    bases = np.array(list("ACGT"))
    out = []
    for row in pwm:
        if mode == "consensus":
            out.append(bases[int(np.argmax(row))])
        else:
            out.append(rng.choice(bases, p=row))
    return "".join(out)
```

## Practical notes
- Motif widths range from ~6 to ~30 bp. Mean ~12.
- 879 vertebrate motifs covers all major TF families.
- For diversity in a library, sample motifs WITHOUT weighting by family — JASPAR has many motifs from highly-studied families (e.g., dozens of bHLH variants).
- For "strong-signal" libraries, use `consensus` mode (the strongest realization).
- For "natural-variance" libraries, use `stochastic` mode (PWM-weighted random draw).
