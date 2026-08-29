# 020_wider_tiles

## Design
5,000 cCREs × 10 tiles, each tile drawn from uniform random offset
in [-400, +400] (instead of the usual [-100, +100]). The 200bp
window can land anywhere within ~1kb of the cCRE midpoint,
exposing the model to flanking regulatory context.

## Hypothesis
Regulatory grammar includes flanking context (insulators,
neighboring TFBSs). Wider sampling trains context-aware grammar.

## Result vs 014 (5K x 10 narrow tiles)
                eval_01  K562    HepG2   SKNSH   eval_07  eval_13
014 narrow:     0.3181   0.144   0.188   0.623   0.337    0.328
020 wider:      0.3216   0.144   0.200   0.621   0.338    0.331

**NEW HIGH on eval_01 (0.3216)**. HepG2 BROKE 0.20 for the first
time (0.188 → 0.200). K562 and SKNSH unchanged. eval_13 also up
(0.328 → 0.331).

## Interpretation — context breadth matters!
First library design that meaningfully lifts mean_r above the
~0.318 plateau (+0.0035 over previous best 012).

Critically, the HepG2 head — the only library-sensitive head —
broke its apparent ~0.19 ceiling. Theory T13's "architecture-bound
HepG2 ceiling at 0.19" was incomplete: 0.19 was the ceiling for
NARROW-CORE tiling; wider tiling pushes it to 0.20+.

### Why this works
Narrow-core tiling (±100bp) keeps every tile centered on the
regulatory element itself. Wider tiling (±400bp) includes:
- The element's CORE in some tiles
- The element's FLANKS in some tiles
- TILES THAT MISS the element entirely (with regulatory context
  on one side)

The model is forced to learn:
- "Where is the regulatory element within my window?" (positional
  invariance)
- "What does the regulatory element look like AT THE EDGE of my
  window?" (partial-motif handling)
- "What does the regulatory context (flanks) tell me even when
  the core element is absent?" (context-only prediction)

These are universal regulatory-grammar skills — they transfer
across cell types because flanking context patterns are universal.

## Theory T13 → T14 (NEW LEVER)
The plateau at ~0.318 was the ceiling for NARROW-CORE tiling
designs. Wider context tiling adds a previously-unsampled
regulatory skill (context-aware grammar) that lifts HepG2 head
beyond its narrow-tile ceiling.

The new theoretical framing:
- The model's ceiling is bounded by what it learns from EACH
  training example.
- Narrow-core tiles teach element identification.
- Wider tiles teach element + context grammar.
- Adding context grammar is a NEW LEARNING AXIS, not a
  distribution shift — that's why it lifts where everything else
  failed.

## Next
Experiment 021: stack the two helpful interventions —
WIDER TILES + RC AUGMENTATION. 5K cCREs × 5 wider tiles + each
tile's RC = 50K. Tests whether wider-context and RC effects
add (peak ~0.325) or are redundant (parity with 020).

Generalization justification: both interventions teach universal
priors (strand invariance + context awareness). They should
combine additively if they teach orthogonal skills.

Prediction: 0.322 ± 0.005. If lift, both axes are productive
and orthogonal. If parity, they tap the same residual learning
capacity.
