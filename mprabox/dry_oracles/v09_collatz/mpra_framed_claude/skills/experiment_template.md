# Experiment template

## Directory layout per experiment
```
libraries/NNN_short_name/
├── generate.py        # produces sequences_0.txt (50,000 × 200bp ACGT)
├── sequences_0.txt
├── result.json        # written by prepare.py
└── notes.md           # design / hypothesis / result / interpretation
```

## generate.py contract
- Write exactly 50,000 lines, each exactly 200 chars from {A,C,G,T}
- Use a fixed seed (typically 0) so the experiment is reproducible
- Save to `sequences_0.txt` in the same directory as `generate.py`
- Reject any sequence containing N
- Reject any sequence not 200 chars long

## After generation
1. `wc -l libraries/NNN/sequences_0.txt` → must equal 50000
2. `head -2 libraries/NNN/sequences_0.txt | awk '{print length}'` → must be 200, 200
3. Run `python3 prepare.py libraries/NNN/`
4. Parse `libraries/NNN/result.json`
5. Append a row to `results.tsv`
6. Write `notes.md` with hypothesis, result, interpretation
7. Append result entry to `notebook.md`
8. `git add -A && git commit -m "NNN_name: mean_r=X.XXX"` (push fails silently — that is OK)

## results.tsv format (tab-separated)
`experiment\teval_01\teval_02\teval_03\teval_04\teval_05\teval_06\teval_07\teval_08\teval_09\teval_10\teval_11\teval_12\teval_13\teval_14\ttime_s\tdescription`

## Eval set clustering observed
These eval sets give nearly identical mean_r in every experiment so far:
- {02, 05, 14} ← tightly linked
- {03, 12}
- {04, 09}
- {06, 11}

Likely related/replicate eval sets. eval_01 is the primary metric.

## Eval set behavior notes (as of experiment 002)
- eval_01 is primary
- eval_07 and eval_13 are the most sensitive to natural regulatory grammar
- eval_08 is the outlier — random baseline 0.089, cCREs 0.076 — NOT measuring grammar lift in the way I first thought; may test composition/synthetic axes
- eval_04 / eval_09 lift LESS from cCREs than the others
