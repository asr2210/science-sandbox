# Skill: writing generate.py for the 3-seed protocol

## Goal
Each `generate.py` must produce three files (`sequences_0.txt`,
`sequences_1.txt`, `sequences_2.txt`) where each file contains exactly
50,000 lines of 200 ACGT chars. Same design strategy, different RNG seed.

## Validated template
```python
import os, numpy as np

N_SEQS, SEQ_LEN = 50_000, 200
ALPHABET = np.array(list("ACGT"))
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate(seed: int) -> list[str]:
    rng = np.random.default_rng(seed)
    # ... your design here, must use `rng` for any randomness so the seed
    #     fully determines the output ...
    # always assert at write time:

def write_seqs(seqs, path):
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= {"A", "C", "G", "T"} for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")

if __name__ == "__main__":
    for seed in (0, 1, 2):
        seqs = generate(seed)
        write_seqs(seqs, os.path.join(OUT_DIR, f"sequences_{seed}.txt"))
```

## Run
```
python3 libraries/NNN_name/generate.py
python3 prepare.py libraries/NNN_name/
```

(Note: the python on this system is `python3`, not `python`.)

## prepare.py timing
- Uniform random 50K seqs × 3 seeds: ~15 min wall time on the cluster
  (`spark01..03`, parallel across seeds).
- Each seed produces a `model_<seed>.pt` (~16 MB) inside the library dir
  during training. Don't commit the .pt files — but they're not in any
  .gitignore yet, so check before `git add -A`.

## Invariants enforced by prepare.py validator
- exactly 50,000 lines per file
- exactly 200 chars per line
- only A/C/G/T
- three files (`sequences_0.txt`, `sequences_1.txt`, `sequences_2.txt`)

## Output
`result.json` in the experiment directory: per-eval mean_r and per-cell
breakdowns (k562, hepg2, sknsh) averaged across the three seeds. Stdout
also prints the same numbers.
