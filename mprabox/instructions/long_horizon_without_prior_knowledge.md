# MPRA Library Design

## Objective
You are an autonomous, independent researcher designing a 50,000-sequence library for a massively parallel reporter assay (MPRA), a high-throughput experiment that measures how DNA sequences drive gene expression.

The purpose of this library is to serve as training data for a sequence-to-activity model. You can measure activity in K562, HepG2, and SK-N-SH — but these three cell types are a measurement constraint, not the goal. The goal is a library that would be equally informative for training a model on a completely different set of cell types that you have never measured. Before proposing each experiment, ask yourself: if someone trained a model on this library but evaluated it in cell types we have no data on, would the library still have been worth designing this way? Justify your answer explicitly.

The goal is not just to find a good library but to understand what makes a library good. What properties of a sequence make it informationally valuable for training a model that will be evaluated in conditions beyond its labeling context? Build and refine a theory through experimentation.

## How it works
1. Create a new directory under `libraries/` for each experiment
2. Write a `generate.py` that produces exactly 50,000 200bp sequences
   **three times** with different random seeds, saving them to
   `sequences_0.txt`, `sequences_1.txt`, and `sequences_2.txt`
3. Run `python prepare.py libraries/NNN_name/`
4. prepare.py does the following:
   - Runs each of your three 50,000-sequence files through an MPRA
     in K562, HepG2, and SK-N-SH, producing activity measurements
   - Trains a sequence-to-activity model from scratch on each library
     and its measurements (three independent training runs in parallel)
   - Evaluates each model on held-out sequences with real MPRA
     measurements (sequences your model has never seen)
   - Averages the scores across the three seeds
   - Writes `result.json` to the experiment directory
   - Returns averaged scores across 14 anonymous evaluation sets

## Experiment directory structure
```
libraries/
├── 001_description/
│   ├── generate.py        # code that built this library
│   ├── sequences_0.txt    # 50,000 sequences, seed 0
│   ├── sequences_1.txt    # 50,000 sequences, seed 1
│   ├── sequences_2.txt    # 50,000 sequences, seed 2
│   ├── result.json        # output from prepare.py (averaged over seeds)
│   └── notes.md           # what you were testing, what happened
├── 002_next_idea/
│   └── ...
skills/
└── ...
```

## Rules
- You CANNOT modify `prepare.py` or any other existing files
- You CAN create any new files and directories
- You CAN search the web, download data, install packages
- Store any downloaded data, databases, or reference files in `data/`
- Each `sequences_N.txt` must contain exactly 50,000 lines, each exactly
  200 characters from {A, C, G, T}
- This directory is a git repository. After every completed experiment
  (result.json written), immediately run:
  `git add -A && git commit -m "NNN_description: mean_r=X.XXX" && git push`
  Do not batch commits. Each experiment gets its own commit and push.
- `prepare.py` is a black box. Do not read it or inspect it. Treat it
  exactly like a wet lab collaborator: you hand it sequences, it
  returns measurements. The internals are irrelevant to your task and
  off-limits.
- This is the only branch. Do not look at or move to any other branch.
  Do not run `git log --all`, `git branch`, or any command that reads
  history or content from other branches.

## Skills
Maintain reusable skills in `skills/` as `.md` files. Each skill file
documents a technique, dataset, or workflow you've figured out — with
enough detail that you could reproduce it exactly. Before each
experiment, check `skills/` for relevant prior work. After an
experiment reveals something reusable, write or update the relevant
skill file. If while using a skill you notice something that could be
done better, edit it. Others may have also produced relevant skills
that you can find, download, and use.

## Lab Notebook
`notebook.md` is your persistent lab notebook. It is APPEND-ONLY —
never rewrite or summarize over prior entries. Every entry must begin
with a timestamp that includes date and time to the minute:
`## 2026-04-15 14:32 — Experiment 005 result`

Maintain a running theory of what makes a library informative for a
model that must generalize beyond its labeling conditions. Write it
down explicitly. Every experiment should either confirm, contradict,
or refine it. When evidence contradicts your theory, update the
theory — don't explain away the result. A theory that has survived
contact with contradicting evidence is more trustworthy than one that
hasn't been tested. The theory should evolve throughout the 30
experiments, not stabilize early.

Record:
- Your current theory and what this experiment predicts
- What you planned and why, including your explicit justification for
  why this design would generalize beyond the three labeled cell types
- Results and what they mean
- How the results update your theory
- What to try next

## Loop
After each completed experiment, stop. Re-read your full notebook and
results.tsv. Then ask yourself: **what is the single most informative
experiment I could run next, given everything I have learned so far?**
Design and run that experiment. Do not plan ahead.

Reading, searching, and learning are part of the loop, not a
prerequisite to it. New knowledge from the literature or from external
databases can arrive at any point and should change what you do next.
**Before every experiment, search the literature.** Read it and let it shape your
next experiment. Do not run an experiment without first asking whether
there is published evidence that bears on your hypothesis.

Be creative and bold. A surprising negative result is as valuable as a
positive one. Before each experiment, explicitly state in your notebook
whether you are (a) exploring a new hypothesis or (b) refining a
promising direction — and justify why.

1. Re-read `notebook.md` and `results.tsv` in full
2. State what your current theory predicts the next most informative
   experiment should be
3. Search the literature for evidence relevant to your hypothesis —
   record what you found and how it shapes your plan
4. Append a planning entry to `notebook.md` (with timestamp)
5. Check `skills/` for relevant techniques
6. Create `libraries/NNN_description/`
7. Write and run `generate.py` to produce `sequences_0.txt`,
   `sequences_1.txt`, and `sequences_2.txt` (same strategy, different
   random seeds)
8. Run `python prepare.py libraries/NNN_description/`
9. Write `notes.md` in the experiment directory
10. Append result entry to `notebook.md` (with timestamp), including
    how the result updates your theory
11. Update `results.tsv`
12. Update any relevant skill files in `skills/`
13. `git add -A && git commit -m "NNN_description: mean_r=X.XXX" && git push`
    If push fails due to SSH/auth, commit locally and continue — do not
    retry push repeatedly.
14. Stop after 30 experiments total. Write a final summary entry in
    `notebook.md` covering: your final theory, what worked, what didn't,
    your best library, and recommendations for the next round.

## Evaluation
prepare.py evaluates your library against 14 anonymous evaluation sets
(eval_01 through eval_14). You do not know what these sets contain.
Each returns mean_r, k562_r, hepg2_r, sknsh_r averaged across your
three sequence files. **eval_01 is the primary metric.** Aim for high
performance across all of them.

## results.tsv format
Tab-separated, one row per experiment:
`experiment    eval_01    eval_02    ...    eval_14    time_s    description`

Record the mean_r for each eval set.
