# MPRA Library Design Notebook

## Initial framing

I need to design a 50,000 sequence, 200 bp MPRA library without looking at the
black-box evaluator. The goal is not to maximize activity in K562, HepG2, or
SK-N-SH specifically, but to make a compact training set that teaches a model
general regulatory grammar. That changes the design objective from "collect
strong enhancers" to "sample the variables that regulatory sequence models need
to learn": GC content, CpG density, motif identity, motif strength, copy number,
spacing, orientation, syntax, background composition, low-complexity sequence,
and inactive/null sequence.

My working theory is that a high-value MPRA training library should contain both
natural-looking regulatory sequence classes and controlled synthetic
perturbations. Natural-like sequences help the model see realistic base
composition and motif co-occurrence. Synthetic sequences help separate causal
features that are confounded in the genome: a motif can be varied against many
backgrounds, motif pairs can be swept across distance and orientation, and null
backgrounds can establish what the model should ignore. Because the assay size is
fixed, I will allocate the library across diverse sequence families instead of
using one dominant source.

I will not inspect `prepare.py`, per the instructions. Local checks will only
validate that the produced file has exactly 50,000 unique 200 bp A/C/G/T
sequences.

## Library architecture

I implemented `library/generate.py` as a deterministic synthetic library
generator using seed 20260522. The design is a mixture of eight families:

- 6,000 GC-spectrum backgrounds. These are mostly motif-free random backgrounds
  across low to high GC, with neutral, CpG-suppressed, and CpG-island-like
  modes. Purpose: teach baseline sequence composition and prevent the model from
  seeing every sequence as regulatory.
- 6,000 single-motif constructs. These place one to three copies of broad TF
  motifs on varied backgrounds, with exact and weakened versions. Purpose:
  isolate motif identity and motif strength.
- 10,000 motif-pair constructs. These sweep common grammar pairs such as
  AP1-ETS, ETS-RUNX, GATA-E-box, STAT-IRF, NFY-SP1, and CTCF-CTCF across
  orientations and spacings. Purpose: expose cooperative syntax, spacing, and
  order effects.
- 8,000 enhancer-like modules. These have three to eight motifs sampled from
  mixed modules that represent broad regulatory programs rather than one target
  tissue. Purpose: provide realistic combinatorial motif density.
- 6,000 promoter-like constructs. These include CpG-rich backgrounds, TATA/Inr/
  DPE/BRE variants, and SP1/NFY/ETS/NRF1/YY1/KLF motifs. Purpose: cover core
  promoter grammar separately from distal enhancer grammar.
- 5,000 homotypic sweeps. These vary copy number and spacing for repeated motifs.
  Purpose: teach dosage, saturation, and local motif clustering.
- 4,000 repeat and decoy controls. These include tandem repeats, homopolymer
  runs, periodic sequence, shuffled blocks, and damaged motif decoys. Purpose:
  represent low-complexity and nonfunctional-looking DNA that may otherwise be
  under-sampled.
- 5,000 local-composition mosaics. These concatenate segments with different GC
  and CpG tendencies and optionally add sparse motifs. Purpose: give the model
  local background shifts resembling genomic sequence heterogeneity.

The motif list is deliberately broad: AP1, CREB, ETS, SP1/KLF, CTCF, GATA, FOX,
E-box, NFY, NRF1, YY1, TEAD, RUNX, SMAD, STAT, IRF, NFKB, CEBP, SOX/OCT, MEF2,
HOX, P53, REST, and core promoter motifs. I used consensus/IUPAC representations
rather than a tissue-specific motif catalog so that the design stays focused on
general grammar.

## Local validation before assay

I ran `python3 library/generate.py`. The generated `library/sequences.txt` has
50,000 lines. Local format validation found 0 length errors, 0 alphabet errors,
0 duplicates, and 50,000 unique sequences. The family counts match the target
allocation. Mean GC by family ranges from about 0.496 for repeat/decoy controls
to 0.644 for promoter-like constructs; overall mean GC is 0.525 with standard
deviation 0.140. The whole library covers all 4,096 possible 6-mers across
9,750,000 6-mer windows, which is a useful sanity check for sequence-space
coverage even though it is not a substitute for regulatory diversity.

## Assay result

I ran `python3 prepare.py library/sequences.txt`. The black-box evaluation took
589.7 seconds and produced `library/result.json`. The mean_r values across the
14 anonymous evaluations were:

- eval_01: 0.6107
- eval_02: 0.6894
- eval_03: 0.6550
- eval_04: 0.6655
- eval_05: 0.6103
- eval_06: 0.6916
- eval_07: 0.5739
- eval_08: 0.6437
- eval_09: 0.7193
- eval_10: 0.6383
- eval_11: 0.6019
- eval_12: 0.5653
- eval_13: 0.5534
- eval_14: 0.6899

The average of the 14 mean_r values is 0.6363. The strongest results were on
eval_09, eval_06, eval_14, and eval_02; the weakest were eval_13, eval_12, and
eval_07. Without seeing the hidden test sets I cannot know the cause, but my
best interpretation is that the library is doing well where motif grammar and
composition diversity are rewarded and less well where the hidden test sets
depend on natural genomic sequence features I did not explicitly sample from
real genomes.

## What I would try next

With another shot, I would add a real-sequence component while keeping the
synthetic perturbation backbone. In particular, I would sample fixed-length
windows from multiple mammalian genomes or accessible regulatory catalogs,
dinucleotide-shuffle matched controls, and tiled perturbations around natural
promoters/enhancers. I would also reduce the most extreme low/high-GC repeat
tail unless it proved useful, because those controls are valuable but may be
over-represented relative to likely anonymous regulatory test sets. Finally, I
would make the pair and module grammar sweeps more systematic, with explicit
balanced factorial coverage of motif identity, orientation, spacing, strength,
background GC, and copy number.
