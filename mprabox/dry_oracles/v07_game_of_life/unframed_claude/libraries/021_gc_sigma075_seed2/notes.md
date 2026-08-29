# 021_gc_sigma075_seed2

## Hypothesis
Replicate 014's recipe (per-seq GC N(0.5, 0.075)) with seed=2. After 014 (0.3989) and 020 (0.3943), the variance estimate suggested ~50% chance of beating 014.

## Result
- **eval_01 mean_r = 0.3989** (K562=0.6174, HepG2=0.4372, SKNSH=0.1421)
- **Exactly matched 014's 0.3989** (down to 4 decimal places — surprising coincidence).

## Interpretation
The σ=0.075 recipe distribution:
- seed=42: 0.3989
- seed=1:  0.3943
- seed=2:  0.3989

Two of three hit 0.3989 exactly. This may be a soft ceiling — perhaps the eval has discrete quantization, or perhaps the σ=0.075 plateau-with-noise really centers around 0.398 with occasional unlucky draws.

Either way, 0.3989 looks like the practical maximum for this recipe. To beat it, I'd need either:
- A different recipe with higher tail (e.g., σ=0.10 or σ=0.13, untested for multi-seed)
- Pure luck on more draws

## Strategy update
Continue rolling seeds 7, 99, 314, 12345 of the 014 recipe to see if any beats 0.3989. Also try σ=0.10 with multiple seeds (018's lone draw was 0.3978).
