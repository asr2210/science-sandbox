# 003_ccre_centered — notes

## Design
50,000 200bp windows centered on high-confidence cCREs (PLS, pELS, dELS,
CA-TF, CA-CTCF) from ENCODE registry V4 (ENCFF286VQG). Skip windows with
N or chromosome-edge.

## Prediction
Regulatory density should help → expected > exp 002 (natural 0.48).

## Result (46s training, 78s wall)
- eval_01: 0.3446 **lower than exp 002** (0.4798) and almost back to random (0.31)
- eval_07 dropped from 0.60 to 0.28 (massive regression)
- eval_13 dropped from 0.59 to 0.35
- eval_04 went 0.50 → 0.42
- eval_08 still ~0.08

## Surprise
**cCRE-only library is significantly WORSE than random genomic.** Strong
negative result against the "regulatory density" hypothesis.

## Hypotheses for why
1. **Activity-range collapse.** cCREs are all "potentially regulatory"
   sequences. Random genomic DNA spans the full range from "boring/inactive"
   to "active enhancer". The model needs negative/low examples to learn the
   activity scale. With cCRE-only training, all training labels likely
   cluster in a narrow range → model can't extrapolate.
2. **Distribution shift.** Eval sequences may be random genomic-like
   (test sets often pull from genome at large). cCRE-trained model sees
   a different distribution → poor generalization.
3. **Loss of negative space.** The model never learns "sequences that do
   nothing", so when shown one in eval, it overpredicts.
4. **Composition bias.** cCREs are GC-rich, CpG-island-enriched. Pure-cCRE
   training overweights this composition.

## Theory update
Library quality is NOT just about regulatory density. It's about **coverage
of the (sequence × activity) space**. Random genomic DNA gives that
coverage because most of the genome is inactive — providing critical
negative examples — while still containing rare functional motifs as
positive examples. Curated cCRE-only library breaks this balance.

## Implication for cross-cell-type generalization
A model that has never seen an "inactive" sequence will overpredict
activity in the unseen cell type — every input looks "regulatory" to it.
This is the worst kind of failure for cross-cell-type transfer.
