# 008_ccre_plus_random

## Design
50,000 = 25,000 cCRE 200bp windows + 25,000 uniform random 200bp.

## Hypothesis
Random adds compositional spread that SKNSH responds to; cCRE
provides regulatory grammar that HepG2 responds to. If additive,
mix gives best of both. If model "averages" signals, mix hurts.

## Result vs 002 and 001
                eval_01  K562    HepG2   SKNSH   eval_08
001 random:     0.2307   0.139   -0.089  0.642   0.089
002 cCRE pure:  0.3154   0.145   +0.177  0.625   0.076
008 cCRE+rand:  0.3091   0.141   +0.168  0.619   0.084

Mix is WORSE than pure cCRE on every cell type. eval_08 lifted a bit
(more random-like contribution).

## Interpretation
The model treats random sequences as TRAINING NOISE, not as
compositional-diversity reinforcement. Halving cCRE content loses
HepG2 grammar; the random half doesn't pay back the loss anywhere.

This is a stronger statement than I expected: **at 50K library size,
the model gets MORE bang from concentrating on regulatory grammar
than from spreading across diverse content.** Diluting with random
sequences uniformly hurts.

Implication: the model's effective training budget per cell-type
predictability ceiling is small. Each "wasted" training sample on
non-regulatory content reduces the cell-type-grammar signal.

## Theory T5 → T6
Wasted training samples (random, shuffled) HURT. Adding LOW-INFO
content to a library reduces effective training. Only HIGH-INFO
regulatory content adds useful signal.

This implies: the lever to break the plateau is HIGHER-INFO cCRE
sequences. Candidates:
- Peak quality filter (sort by signalValue, take top)
- Cross-species conserved cCREs (phyloP > 2)
- Multi-evidence convergent cCREs (DNase + H3K27ac + TF ChIP)
- STARR-seq validated active elements

## Next
Experiment 009: HepG2 DNase peaks sorted by signalValue, top 10K
regions × 5 tiles. Tests peak-quality hypothesis directly.
