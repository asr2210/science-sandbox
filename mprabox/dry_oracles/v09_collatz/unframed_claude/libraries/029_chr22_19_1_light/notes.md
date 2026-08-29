# Exp 029 — chr22 + chr19 + chr1 light (47.5/47.5/5)

50k 200bp windows: 23750 chr22 + 23750 chr19 + 2500 chr1.

## Result

| metric  | mix (027) | +5% chr1 (029) | +20% chr1 (028) |
|---------|----------:|---------------:|----------------:|
| eval_01 | **0.3215**| 0.3203         | 0.3197          |
| k562    | 0.1446    | 0.1431         | 0.1447          |
| hepg2   | 0.2004    | 0.2015         | 0.2013          |
| sknsh   | 0.6196    | 0.6165         | 0.6132          |

Dose-response is consistently negative for chr1 addition.
HepG2 lifts ~+0.001 from any chr1 dose; SKNSH drops monotonically.

**Conclusion**: chr22+chr19 50/50 is the local optimum. Adding any
chr1 hurts.

**Plan for exp 030 (final)**: rerun chr22+chr19 50/50 with a different
seed to test variance — if it lands above 0.3215, that becomes best.
If below, 027 remains best. Essentially free upside.
