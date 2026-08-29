# Exp 005 — Random sequences, 70% GC

50k random 200bp at 70% GC (P(G)=P(C)=0.35, P(A)=P(T)=0.15).

## Result

| metric  | random 50% | random 70% | delta   |
|---------|-----------:|-----------:|--------:|
| eval_01 | 0.2307     | 0.1448     | -0.0859 |
| k562    | 0.1361     | 0.1187     | -0.0174 |
| hepg2   | -0.0742    | -0.0772    | -0.0030 |
| sknsh   | 0.6302     | 0.3928     | -0.2374 |

SKNSH dropped by 0.24 — it strongly prefers ~50% GC. HepG2 unchanged.
K562 slightly worse.
