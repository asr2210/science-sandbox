# 004 — cCRE-centered (chr19 + chr22)

## What I tested
50k 200bp windows centered on ENCODE-SCREEN cCREs from chr19 (~26k cCREs)
and chr22 (~17k cCREs). 43,106 unique cCREs → some duplication to reach
50k. Random orientation. Seed=42.

## Result
- eval_01 = **0.1256**  (003=0.134, chr22 random was BETTER)
- mean of evals = 0.1219 (003=0.128)
- K562: 0.029  (vs 003: 0.037)
- HepG2: 0.157  (vs 003: 0.169)
- SK-N-SH: 0.192  (vs 003: 0.196)
- eval_07 K562 jumped to 0.047 (highest yet)
- eval_08 still 0.056

## Surprising negative result
cCRE-focused library is WORSE than random chr22 windows. My theory
predicted enrichment would help; it didn't.

## Possible causes
1. **Library too narrow.** All cCREs share active marks; the model sees a
   compressed slice of CRE space and can't generalize to the eval's
   broader distribution.
2. **Duplicates** (~7k of 50k are duplicate windows) reduce effective
   training-set size.
3. **chr19 GC bias.** chr19 is gene-dense and GC-rich; combining with
   chr22 may skew the composition vs eval distribution.
4. **No inactive examples.** The model lacks negative-class training
   data; it learns "what cCREs look like" but not "what NON-cCREs look
   like" — crippling its discrimination for natural eval sequences
   that span both classes.

## Theory update
Active-CRE enrichment is NOT a free win. Diversity (in both active and
inactive directions) and broad sequence distribution matter at least
as much as activity. This aligns with MPRA-literature reports that
"silencer-lacking" libraries fail at variant direction-of-effect.

## What to try next
Experiment 005: random genomic windows from chr19+chr22 (same regions,
no cCRE focus). Direct comparison to (a) 003 chr22-only random for
"does more genomic diversity help?", and (b) 004 cCRE for "does cCRE
focus help within the same chromosomes?"
