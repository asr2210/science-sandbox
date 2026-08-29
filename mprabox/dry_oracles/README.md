# Dry Oracles

14 synthetic scoring functions that replace the real Malinois oracle with rules of increasing difficulty. Each oracle defines a deterministic scoring function over 200bp sequences, replacing the biological signal with a synthetic one while keeping the rest of the evaluation pipeline identical.

## Oracles

| # | Oracle | What it rewards |
|---|--------|----------------|
| 01 | gc_balance | 50% GC content, equal base counts |
| 02 | alternating_purine | Alternating purine/pyrimidine pattern |
| 03 | english_words | English words via dinucleotide-letter encoding |
| 04 | compression | zlib compressibility |
| 05 | prime_counts | Nucleotide counts that are prime numbers |
| 06 | fibonacci_spell | Specific bases at Fibonacci-indexed positions |
| 07 | game_of_life | Conway's Game of Life on a 10×20 grid |
| 08 | modular_cross | Cross-products of counts under modular arithmetic |
| 09 | collatz | Collatz stopping time of derived properties |
| 10 | rle_sin_xor | RLE compressibility × sin(prime-position sums) × XOR-fold |
| 11 | substring_gattaca | Occurrences of specific 6-7mer substrings |
| 12 | position_100 | Score depends on the base at position 100 |
| 13 | count_c_50 | Reward sequences with exactly 50 C's |
| 14 | parity_g | Reward even number of G's |

## Framings

Each oracle was tested under three instruction conditions:

| Framing | Description |
|---------|-------------|
| **MPRA-framed** | Agent believes it is designing an MPRA library. No baselines. |
| **Unframed** | Black-box optimisation. No biological context. |
| **Symbolic** | Alphabet is {0,1,2,3}. No biological connotation. |

## Running

```bash
cd dry_oracles/v07_game_of_life
cp ../instructions/mpra_framed.md instructions.md
# Point your agent at instructions.md
```

## Structure

```
dry_oracles/
├── instructions/           # Framing variants
│   ├── mpra_framed.md
│   ├── unframed.md
│   └── symbolic.md
├── strategies/             # Per-oracle baseline results
├── eval/                   # Shared evaluation harness
├── baselines/              # Baseline computation code
└── v{01..14}_{name}/
    ├── oracle.py           # Scoring function
    ├── prepare.py          # Sealed evaluation harness
    ├── strategies.md       # Baseline results for this oracle
    ├── mpra_framed_claude/ # Run results
    ├── unframed_claude/
    └── symbolic_claude/
```
