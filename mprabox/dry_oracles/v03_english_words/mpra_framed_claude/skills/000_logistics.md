# Logistics skill

## Environment
- `python3` available; `numpy`, `pandas` installed. **No torch** locally — model training is inside `prepare.py`.
- `prepare.py` interface: `python3 prepare.py libraries/NNN_name/` consumes `sequences_0.txt` (50,000 lines × 200 chars from ACGT) and writes `result.json`.
- Each run takes ~2 minutes wall-clock.
- Each library must be in its own `libraries/NNN_description/` directory.

## File format
`sequences_0.txt`: 50,000 lines, each EXACTLY 200 characters from {A,C,G,T}, plain text. No header.

## Result format
`result.json` contains `eval_01..eval_14` each with `mean_r, k562_r, hepg2_r, sknsh_r`, plus `n_seeds`, `time_s`.

## Per-experiment workflow
1. Create `libraries/NNN_name/`.
2. Write `generate.py` (deterministic seed).
3. Run it: `python3 libraries/NNN_name/generate.py`.
4. Verify: `wc -l libraries/NNN_name/sequences_0.txt` must say 50000; `head -1 ... | awk '{print length}'` must say 200.
5. Run: `python3 prepare.py libraries/NNN_name/`.
6. Write `notes.md`, append entries to root `notebook.md` and `results.tsv`.
7. Commit: `git add -A && git commit -m "NNN_name: mean_r=X.XXX"`; push if remote is configured (don't retry on failure).

## Reference baseline (exp 001, uniform random)
- eval_01 mean_r = **0.4192**
- K562_r ≈ 0.59, HepG2_r ≈ 0.62, SK-N-SH_r ≈ 0.045
- All eval sets clustered 0.385-0.428; eval_08 lowest.
