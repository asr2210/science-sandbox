# Exp 011 — TATA box motif at random positions

## Design
50K random uniform 200-char sequences, each with "TATAAA" (= "303000")
overwritten at a random position in [0, 194]. Per-position composition
shifts slightly toward AT.

## Result vs baseline and AT-rich
| eval    | baseline | exp007 AT-iid | exp011 TATA | TATA-base |
|---------|----------|---------------|-------------|-----------|
| eval_01 | 0.4848   | 0.4669        | 0.4401      | -0.045    |
| eval_07 | 0.5200   | 0.7117        | 0.6924      | +0.172    |
| eval_13 | 0.4992   | 0.6900        | 0.6714      | +0.172    |
| eval_04 | 0.4440   | 0.0890        | 0.0729      | -0.371    |
| eval_08 | 0.1613   | 0.0418        | 0.0493      | -0.112    |

## Observations
- TATA insertion is WORSE than AT-iid on eval_01 (0.44 vs 0.47), even
  though TATA shifts AT content LESS (54.5% vs 60%).
- The motif/structure adds ~-0.03 penalty on top of composition effect.
- On eval_07/13, TATA gives smaller lift than pure AT-iid (+0.17 vs
  +0.19). Specific motif doesn't help; if anything mildly worse than
  diffuse AT-bias.

## Interpretation
- The score does NOT seem to recognize TATA box as a special feature.
- Inserting a fixed motif at random positions creates a structural
  artifact the score dislikes.
- Specific positional structure HURTS eval_01.

This is another data point suggesting eval_01 is sharply peaked at
uniform random with no easy improvements.
