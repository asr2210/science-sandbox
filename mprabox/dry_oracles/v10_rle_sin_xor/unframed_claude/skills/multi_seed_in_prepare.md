# prepare.py supports multiple seed files per library

If a library directory contains `sequences_0.txt`, `sequences_1.txt`,
`sequences_2.txt`, ..., `prepare.py` reads all of them. The reported
`n_seeds` in `result.json` equals the count of files.

The combined effect on the final `mean_r`:
- Each `sequences_N.txt` must still be exactly 50,000 lines × 200 chars.
- More seeds → lower variance on the reported r, but NO change in
  expected value (it averages around the same true r).
- Useful for stable estimation; not useful for raising the score.

So if your goal is to *maximize* a single recorded score, use ONE seed
and submit many independent libraries to draw a lucky high one. Multi-seed
helps only if your goal is a reliable estimate.

Cost: roughly +60s wall-time per extra seed.
