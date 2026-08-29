# Exp 006: real human genomic windows

**Hypothesis**: Natural DNA sequences will outperform random because the
underlying model is trained on natural data.

**Method**: 12 Mb of hg38 from 12 chromosomes (1 Mb each), sliced into
50k random 200bp windows (N-free).

**Results**:
- eval_01 mean=0.3975 (vs 0.4203 random) → -0.023 worse on mean
- K562=0.5414 (vs 0.5847) → -0.043
- HepG2=0.5520 (vs 0.6175) → -0.066
- SKNSH=0.0991 (vs 0.0587) → **+0.040** ✨ huge improvement

**Big finding**: K562/HepG2 prefer random; SKNSH prefers natural. The three
cell types have DIFFERENT optimal compositions. Random's natural ~50% GC
seems to mimic K562/HepG2 enhancer composition (myeloid/liver enhancers
tend to be balanced or slightly GC-rich), while SKNSH (neural) loves
natural sequences which are AT-rich and contain homeobox/E-box motifs.

**Implications**: A MIXTURE library — part random, part natural — could
provide preferred inputs to all three cell types simultaneously and lift
the aggregate mean_r above either component alone. Will test in Exp 007.
