# Sampling patterns I've found useful for 200bp libraries

## Length-weighted chromosome sampling
```python
chroms = np.array([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
chrom_lens = {c: len(fa[c]) for c in chroms}
weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
weights /= weights.sum()
c = rng.choice(chroms, p=weights)
start = rng.integers(0, chrom_lens[c] - L)
seq = str(fa[c][start:start+L]).upper()
if "N" in seq: skip
```
Rejection rate for N-windows on hg38 primary: ~5%.

## cCRE-centered windows
For each cCRE row, take `mid = (start+end)//2`, then window
`[mid-L//2, mid+L//2]`. Verify within chromosome bounds.

## Use `pyfaidx.Fasta(path, sequence_always_upper=True)` for fast random access.
First call builds `.fai` index (~10s for hg38). Subsequent calls instant.

## Random read order — fasta indexing is random-access, no need to scan.

## Skip these in samples
- N-containing windows (heterochromatin)
- Soft-masked DNA: I uppercase but keep — repeats are real DNA.
- Optionally: blacklist regions (ENCFF356LFX).

## Performance tips
- Loading hg38 with pyfaidx: ~3 sec
- Building .fai index: ~10 sec one-time
- Sampling 50K random windows: <1 sec after index built
- Loading cCRE bed.gz (filter to high-conf): ~3 sec
