# Exp 007 — Bipartite GC architecture

100bp AT-rich (30% GC) + 100bp GC-rich (70% GC) halves with cell-type
motifs in matching halves.

## Result

| metric  | exp 002 | exp 006 30%GC | exp 007 bipartite |
|---------|--------:|--------------:|------------------:|
| eval_01 | 0.2541  | 0.2229        | 0.1937            |
| k562    | 0.1262  | -0.0870       | 0.1233            |
| hepg2   | 0.0186  | 0.1934        | -0.0610           |
| sknsh   | 0.6174  | 0.5623        | 0.5188            |

Bipartite STRUCTURE itself hurts SKNSH (0.52, down from 0.63 random).
HepG2 did NOT inherit the 30%-GC gain — needs uniform AT bias, not local.
K562 about same as exp 002. SKNSH drop dominates.

Lesson: Sharp internal GC architecture is penalized (looks synthetic to
SKNSH model). HepG2 wants GLOBAL low-GC, not local.
