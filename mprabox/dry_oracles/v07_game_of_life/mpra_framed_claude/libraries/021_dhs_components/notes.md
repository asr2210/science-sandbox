# Experiment 021 — DHS component-stratified

## Design
3125 DHS summits per component, across 16 DHS components (Primitive,
Neural, Stromal A/B, Lymphoid, Placental, Musculoskeletal, etc).
Maximum cell-type breadth in regulatory windows.

## Result
- eval_01: 0.3920 (Δ -0.0017 vs uniform DHS, within noise of ceiling)
- K562: 0.6038, HepG2: 0.4265, SK-N-SH: 0.1456

DHS cell-type breadth gives no extra lift. The ceiling is set by GC
composition, not by cell-type information.

## Summary of compositional ceiling
The 0.394 ceiling has been reached by all of:
- 4-way mix (cCRE + DHS + natural + mouse)
- 5-way max diversity (+ FANTOM5, Low-DNase)
- pure GC-stratified natural (no reg)
- GC-stratified + reg combo
- GC-stratified human + mouse
- CpG-stratified natural
- DHS-component-stratified

All within ±0.003 of 0.394. **Library design has fully saturated.**

## Plan
Run one more "best mix" seed for noise triangulation (exp 022),
then write the final synthesis and ceiling estimate.
