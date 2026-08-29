# Skill: fast hg38 loading

## Problem
Parsing `data/hg38.fa` (3.1 GB plain text) line-by-line into a
`dict[chrom] -> str` takes **~9 minutes**. With 30 experiments to run
and many touching the genome, this is prohibitive.

## Solution
Per-chromosome uint8 .npy files in `data/hg38_npy/`. Loaded with
`mmap_mode='r'` → ~6 seconds for all 24 main chromosomes.

## How to use

```python
import numpy as np, os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE_DIR = os.path.join(REPO_ROOT, "data", "hg38_npy")

def load_genome():
    chroms = {}
    for f in os.listdir(CACHE_DIR):
        if f.endswith(".npy"):
            c = f[:-4]
            chroms[c] = np.load(os.path.join(CACHE_DIR, f), mmap_mode="r")
    return chroms

genome = load_genome()
# each chroms[c] is a uint8 numpy array of ASCII bases (uppercase, including 'N')

def get_window(chrom, start, length):
    """Return ASCII string for [start, start+length); None if out of range or has N."""
    arr = genome[chrom]
    if start < 0 or start + length > len(arr):
        return None
    sub = arr[start:start + length]
    if np.any(sub == ord("N")):
        return None
    return sub.tobytes().decode("ascii")
```

## Notes
- Files are mmap-loaded so memory pressure is minimal until you access
  data. Subsequent windowed access is fast.
- For batched random sampling (e.g., 50,000 windows), still cheap because
  windows are tiny (200 bytes each).
- Total disk: 2.9 GB across 24 chromosome files. Gitignored.

## Building the cache (one-time, ~9 min)

See `/tmp/cache_hg38_v2.py` style script. Reads `data/hg38.fa`,
extracts chr1..22, chrX, chrY, saves each as uint8 numpy array.
