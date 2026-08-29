# Exp 012: per-sequence mono-shuffled natural

**Hypothesis**: Tests whether natural's SKNSH boost is from (a) per-
sequence GC variation, (b) actual motifs, or (c) both.

**Method**: Take Exp 006 natural sequences, mono-shuffle each in place.
Preserves per-seq base composition (including natural per-seq GC variance
from ~30 to ~70%) but destroys motifs and di-frequencies.

**Results vs comparators**:
| Lib | eval_01 | K562 | HepG2 | SKNSH |
|-----|---------|------|-------|-------|
| 001 random uniform | 0.4203 | 0.585 | 0.618 | 0.059 |
| 006 natural | 0.3975 | 0.541 | 0.552 | 0.099 |
| 008 Markov-1 nat | 0.4094 | 0.571 | 0.595 | 0.062 |
| 012 shuffled nat | 0.3632 | 0.498 | 0.523 | 0.068 |

**Interpretation**: 
- mono-shuffled is WORSE than Markov-1 on K562/HepG2. The per-sequence GC
  *variation* (each seq has its own GC) drags K562/HepG2 down severely.
- mono-shuffled SKNSH (0.068) is between Markov-1 (0.062) and natural
  (0.099). So natural's SKNSH gain has both a per-seq-GC component
  (~+0.006) and a motif component (~+0.031).

**Key takeaway**: K562 and HepG2 score depends sensitively on per-sequence
GC UNIFORMITY. Random's per-seq GC is tightly distributed around 50%
(binomial std ~3.5%). Natural's varies 30-70%. The K562/HepG2 model heads
expect uniform-GC inputs.

**Implication for design**: Try a library with even MORE uniform per-seq
composition than random (e.g., enforce exactly 50:50 GC per seq). Could
nudge K562/HepG2 marginally above random baseline.
