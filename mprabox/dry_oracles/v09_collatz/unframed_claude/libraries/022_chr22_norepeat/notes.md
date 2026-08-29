# Exp 022 — chr22 NON-REPEAT (≥80% uppercase) windows

chr22 is 41% soft-masked (lowercase = Alu/LINE/SINE/etc). Filter to
windows that are ≥80% uppercase (non-repeat). 28% of random windows
pass. Resulting GC mean=0.511 (vs 0.47 for full chr22 — non-repeat
DNA is GC-richer).

## Result

| metric  | chr22 random | non-repeat chr22 |
|---------|-------------:|-----------------:|
| eval_01 | 0.3202       | 0.3146           |
| k562    | 0.1443       | **0.1307** (-0.014) |
| hepg2   | 0.1990       | 0.1918           |
| sknsh   | 0.6173       | 0.6212           |

Surprising: K562 DROPPED when repeats removed. SKNSH only gained
+0.004 (much less than Markov's +0.036). HepG2 barely moved.

**Lesson**: K562 actively rewards genomic repeats (Alu elements
contain TF binding sites that boost K562 model). Removing them costs
more than it gains.

The Markov SKNSH gain (+0.036) was NOT from removing repeats — it
was from the simpler statistical structure of synthetic sequences.
SKNSH's score isn't easily pushed by tweaking real genomic regions.

**Conclusion**: chr22 RANDOM (incl repeats) remains the optimum
because each cell type's preference is partly satisfied by different
parts of the natural composition:
- HepG2: needs natural higher-order structure (not synthetic)
- K562: needs the repetitive elements (Alu etc)
- SKNSH: needs ~50% GC, tolerant of either

Hard to improve all three simultaneously with real DNA filtering.
