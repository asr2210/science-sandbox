# String Optimization

## Objective
You have access to a black-box scoring function that takes 50,000
strings of length 200 over the alphabet {0, 1, 2, 3} and returns
scores. Your goal is to maximize those scores.

You have 30 submissions. Use them wisely.

## How it works
1. Create a new directory under `libraries/` for each experiment
2. Write a `generate.py` that produces exactly 50,000 strings
   and saves them to `sequences_0.txt`
3. Run `python prepare.py libraries/NNN_name/`
4. prepare.py scores your submission and writes `result.json`

## Format
`sequences_0.txt` must contain exactly 50,000 lines, each exactly
200 characters from {0, 1, 2, 3}. Example line:
`01230123012301230123...` (200 characters)

## Experiment directory structure
```
libraries/
├── 001_description/
│   ├── generate.py
│   ├── sequences_0.txt
│   ├── result.json
│   └── notes.md
├── 002_next_idea/
│   └── ...
skills/
└── ...
```

## Rules
- You CANNOT modify `prepare.py` or any other existing files
- You CAN create any new files and directories
- You CAN install packages, write any code
- `prepare.py` is a black box. Do not read it or inspect it.
- This directory is a git repository. After every completed experiment
  (result.json written), immediately run:
  `git add -A && git commit -m "NNN_description: mean_r=X.XXX" && git push`
- This is the only branch. Do not look at or move to any other branch.

## Skills
Maintain reusable skills in `skills/` as `.md` files. Document
techniques you figure out with enough detail to reproduce them.

## Lab Notebook
`notebook.md` is your persistent lab notebook. It is APPEND-ONLY.
Every entry must begin with a timestamp:
`## 2026-04-15 14:32 — Experiment 005 result`

Maintain a running theory of what the scoring function rewards.
Write it down explicitly. Every experiment should either confirm,
contradict, or refine it. When evidence contradicts your theory,
update the theory — don't explain away the result. A theory that
has survived contact with contradicting evidence is more trustworthy
than one that hasn't been tested. The theory should evolve throughout
the 30 experiments, not stabilize early.

Record:
- Your current theory and what this experiment predicts
- What you planned and why
- Results and what they mean
- How the results update your theory
- What to try next

## Loop
1. Re-read `notebook.md` and `results.tsv` in full
2. Plan your next experiment based on everything you've learned
3. Append a planning entry to `notebook.md` (with timestamp)
4. Check `skills/` for relevant techniques
5. Create `libraries/NNN_description/`
6. Write and run `generate.py` to produce `sequences_0.txt`
7. Run `python prepare.py libraries/NNN_description/`
8. Write `notes.md` in the experiment directory
9. Append result entry to `notebook.md` (with timestamp)
10. Update `results.tsv`
11. Update any relevant skill files in `skills/`
12. `git add -A && git commit -m "NNN_description: mean_r=X.XXX" && git push`
    If push fails, commit locally and continue.
13. Stop after 30 experiments total. Write a final summary in
    `notebook.md`.

## Evaluation
prepare.py evaluates your submission across 14 anonymous test sets
(eval_01 through eval_14). Each returns mean_r, k562_r, hepg2_r,
sknsh_r. **eval_01 is the primary metric.** The column names are
arbitrary labels.

## results.tsv format
Tab-separated, one row per experiment:
`experiment	eval_01	eval_02	...	eval_14	time_s	description`

Record the mean_r for each eval set.
