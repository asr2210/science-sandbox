# Experiment 003: Inserted canonical TFBS motifs

## Plan
50k sequences of 200bp, 42% GC random background, with ~6 inserted canonical
TFBS motifs each (AP-1, CREB, SP1, TATA, GATA1, HNF4, FOXA, E-box variants,
NRSF/REST, KLF1, MYB, NF-Y, ETS, MAX/USF).

## Result
- eval_01 mean_r = **0.1170** (K562=0.009, HepG2=0.156, SKNSH=0.186)
- Basically identical to random 50% GC (0.1176) and GC42 (0.1152)
- K562 actually went DOWN (0.012 → 0.009)

## Big finding
**Random motif insertion does NOT increase the score.** This contradicts the
naïve hypothesis that the scorer rewards motif presence. Either:
- Score isn't motif-content driven
- Motifs need correct flanks / spacing / orientation (i.e. real grammar)
- Random insertion creates noise that masks the motif signal
- The scorer compares libraries via composition statistics that aren't moved
  by sparse motif insertion

## Theory update
T0 (motif-rich libraries score higher) — **disconfirmed**. Need a new theory.

## Next
Try real human genomic 200bp windows. If natural sequences score better, the
scorer rewards natural-like content. If not, the scorer is doing something
more subtle (variance/diversity/k-mer matching).
