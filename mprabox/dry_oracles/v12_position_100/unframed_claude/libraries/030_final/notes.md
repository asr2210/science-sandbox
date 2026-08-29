# 030 final

**Design (FINAL):** proven 020 recipe. Top 12.5k cCREs by TFBS-cluster density (in 400bp context) × 4 sliding 200bp windows at offsets {-75, -25, +25, +75}. SEED=350.

**Result:** eval_01 = 0.0764. eval_03 = 0.0962 (NEW BEST across all 30 libraries).

**Why this recipe won across 30 experiments:**
1. cCRE substrate (~2.35M ENCODE regulatory elements) provides the basic regulatory grammar.
2. Filtering to high TFBS density picks "regulatory hub" regions packed with information.
3. Sliding-window augmentation (4 views per region) acts like translation-invariant data aug — model learns motifs are position-invariant within the 150bp envelope around the cCRE center.
4. 4 views × 12.5k regions is the sweet spot: enough unique biological regions for diversity, enough aug for invariance learning.

**Key negative results that shaped this:**
- Pure random / dinuc-Markov / random-intergenic: cap at 0.065-0.075
- Oversampling with replacement (013): kills the model (0.0458)
- Mixed/hybrid libraries (007, 019): no benefit from substrate union
- Wider augmentation offsets (025): hurts; flanking sequence is less informative
- Fewer regions with more aug (026): hurts; diversity dominates
- RC augmentation (018): neutral
- Joint TFBS×DHS scoring (024): no benefit over TFBS-only
- Activity contrast with intergenic deserts (015): hurts

**Variance:** Noise floor ~0.003 on eval_01 between replicates (e.g., 011 vs 016 same recipe diff seed: 0.0760 vs 0.0734). Three 020-recipe replicates: 0.0764/0.0766/0.0764 — exceptionally stable because TFBS-density ranking is mostly deterministic.
