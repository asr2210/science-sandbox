# Exp 006 — Random sequences, 30% GC

## Result

| metric  | random 50% | random 70% | random 30% |
|---------|-----------:|-----------:|-----------:|
| eval_01 | 0.2307     | 0.1448     | 0.2229     |
| k562    | 0.1361     | 0.1187     | -0.0870    |
| hepg2   | -0.0742    | -0.0772    | 0.1934     |
| sknsh   | 0.6302     | 0.3928     | 0.5623     |

HUGE finding: each cell type has its own GC preference:
- **K562**: prefers high GC (positive at 50%, 70%, negative at 30%)
- **HepG2**: prefers LOW GC (negative at 50%/70%, +0.19 at 30%!)
- **SKNSH**: prefers 50% GC (drops at both extremes, badly at 70%)

If we could optimize per cell type independently and then average,
we might get K562~0.20 (high GC + motifs), HepG2~0.30 (low GC + motifs),
SKNSH~0.65 (50% GC). But the SAME library is scored by all three.

Implication: a library of MIXED-GC sequences is one approach; or
per-sequence include both "K562-pro" GC-rich regions AND "HepG2-pro"
AT-rich regions. Architecture matters.
