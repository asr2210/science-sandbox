# Experiment 013 — minimal regulatory dose

## Design
45K natural + 2.5K cCRE + 2.5K DHS. Test dose-response of regulatory
enrichment.

## Result
- eval_01: 0.3893 (Δ +0.0017 vs nat baseline 0.3876)
- K562: 0.5986, HepG2: 0.4243, SK-N-SH: 0.1451

## Dose-response curve (eval_01)
| reg fraction | design | eval_01 | Δ vs nat |
|---|---|---|---|
| 0% | nat (001) | 0.3876 | — |
| 10% | nat + 5K reg (013) | 0.3893 | +0.0017 |
| 60% | 4-way mix (002) | 0.3937 | +0.0061 |
| ~80% | act contrast (005) | 0.3934 | +0.0058 |
| ~80% | act quintiles (004) | 0.3919 | +0.0043 |
| 100% top-density | TF div (011) | 0.3831 | -0.0045 |

Curve shape:
- 0→10% reg: +0.0017 (gentle slope)
- 10→60% reg: +0.0044 (steeper)
- 60→80% reg: flat / slightly down
- 100% top-density: catastrophic loss

Sweet spot is ~50-70% reg, broadly natural. The "10% regulatory
boost" only captures ~30% of the achievable lift.

## Theory update
T7 refined: it's not purely "distributional breadth," it's
**"natural backbone with moderate regulatory enrichment."** The
optimum is a mix where regulatory windows are ~60% and natural
is ~40%, with natural providing distributional anchor.

## Next direction
Test whether the limit is set by *composition* (GC) or *content*
(motifs/regulatory): exp 014 = GC-stratified natural (no reg, just
uniform GC). If this lifts beyond 0.388, then GC matching is the
mechanism. If not, then it's specifically regulatory content.
