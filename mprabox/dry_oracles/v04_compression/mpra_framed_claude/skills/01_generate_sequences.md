# Generating 50k×200bp sequences

## Fast uniform random (used in exp 001)
```python
import numpy as np
rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(50_000, 200), dtype=np.int8)
seqs = alphabet[idx]
with open(out_path, "w") as f:
    f.write("\n".join("".join(row) for row in seqs))
    f.write("\n")
```
Runs in ~1 second.

## Output format requirements
- File: `sequences_0.txt`
- Exactly 50,000 lines
- Each line: exactly 200 characters from {A, C, G, T} (uppercase, no N)
- Trailing newline OK

## Validation
```bash
wc -l sequences_0.txt   # expect 50000
awk '{print length($0)}' sequences_0.txt | sort -u   # expect 200
grep -v '^[ACGT]\{200\}$' sequences_0.txt | head   # expect empty
```

## Composition guidance
- Uniform random ≈ 25% each base, 50% GC.
- Human genome ≈ 41% GC; regulatory regions vary widely (CpG islands
  60-80% GC; many enhancers 40-50%).
