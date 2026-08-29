# 013 — Random + 3x10bp PLS-only fragments per sequence

**Design.** Combine 011's distribution (3x10bp at random positions) with 012's PLS-only source.

**Result.** eval_01 = **0.4170** vs 012's 0.4248 (Δ-0.0078). K562 = 0.582, HepG2 = 0.609, SK-N-SH = 0.060.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 011 mixed 3x10bp | 0.589 | 0.615 | 0.048 | 0.4177 |
| 012 PLS 1x25bp | 0.591 | 0.619 | 0.065 | **0.4248** |
| 013 PLS 3x10bp | 0.582 | 0.609 | 0.060 | 0.4170 |

**Interpretation — distribution destroys the PLS advantage.** Splitting a 30bp PLS payload into 3x10bp chunks:
- Loses ~3bp of motif span on average per chunk (motifs are 6-15bp, 10bp barely contains one full motif).
- Drops K562 and HepG2 below random (compositional disturbance is worse when spread).
- SK-N-SH lift (0.060) is smaller than 012 (0.065).

**Update to Theory v10:** The right way to add biology is CONCENTRATED at a single locus large enough to span a full PWM hit + a little flanking context. 25bp is the sweet spot because typical TF motifs are 6-12bp and ~7bp flanking on each side captures the spacing rules. 3x10bp fragments are too short to capture full motif+context and the 3 disruptions hurt more than 1.

**Theory v11 — concentrated > distributed for PLS embedding.** Single 25bp PLS fragment captures motif + neighboring base context. Three 10bp fragments split a 30bp payload across three loci where each is below motif length.

**Next directions:**
- 014: Single 30bp PLS fragment (test if 25 vs 30 matters)
- 015: 2x15bp PLS fragments (mid-way between 1x25 and 3x10)
- 016: PLS centered on TSS (more enriched in core promoter motifs)
- 017: 1x25bp PLS but only from "strong" PLS (high signal score)

I'll go with **014: 1x25bp PLS-only but centered ON the cCRE coordinates** (rather than a random 25bp window). PLS coordinates from ENCODE V4 typically span the actual nucleosome-free region around the TSS — sampling random 25bp from a 200bp window can land outside the TF-binding core. A 25bp centered on the cCRE midpoint will more reliably contain core promoter motifs.
