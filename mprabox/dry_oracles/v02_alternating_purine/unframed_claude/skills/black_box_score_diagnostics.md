# Skill: Diagnosing a black-box MPRA scoring function

When you can submit sequences to a black-box scorer and only see numbers
back, run these probes early to learn what the scorer measures:

## 1. Random baseline first
Submit 50k uniformly random ACGT sequences. The shape of the result
tells you most of what you need:
- Score type (correlation? regression? classification?)
- Per-cell-line breakdown
- Magnitude floor (random isn't necessarily 0!)

## 2. Look for "duplicate" outputs
Compare across cell lines and across eval sets. If two columns return
**identical numbers to 4 decimals on every input**, they share an oracle.
In our run, K562 and HepG2 always matched exactly — they're the same
oracle reported twice. This saves you from trying to optimize them
separately.

Also check for paired eval sets: in our run, eval_01 = eval_14,
eval_02 = eval_05, eval_03 = eval_12, eval_06 = eval_11. That meant
only ~9 unique oracle outputs hidden in 14 columns.

## 3. Composition probes (cheap, fast)
- All-A, all-N? Probably rejected (non-ACGT) — confirms validation.
- High-GC random (60%), low-GC random (40%): does score shift?
- Sequences padded with TATA boxes or NRSF sites: does any motif move it?
For our scorer, NONE of these substantially helped — the oracle was
not GC-sensitive in the relevant range and didn't reward isolated
consensus motifs.

## 4. Real biological reference
The single biggest jump was substituting real Malinois MPRA sequences
for synthetic ones (+0.02). Always try a published dataset matching
the cell lines before designing sequences from scratch.

## 5. Variance probe
Run the same generator twice with different seeds. Difference indicates
noise floor. In our run: ~0.005 between seeds on the same 4×4×4 strategy.

## 6. Confirm "training-set" hypothesis
If a stratified sample with uniform activity coverage beats the same
data with extreme-only coverage, the scorer is plausibly training a
downstream model on your library (it needs gradient information, not
just label spread). In our run, 3D stratification (0.19) beat extremes
(0.17) — confirming "submit-as-training-data" semantics.

## 7. Cost-conscious experimentation
Each call costs ~30-45s plus an experiment slot. Batch generator
writes locally, run prepare.py one at a time. Keep results in a
TSV so you can diff strategies quickly.
