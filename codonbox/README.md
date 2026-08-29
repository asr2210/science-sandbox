# CodonBox

A science sandbox for invented biological rule discovery. CodonBox tests whether an agent can infer the rules of an unfamiliar genetic system from experiment alone, using a simplified model of how DNA instructions give rise to three-dimensionally folded proteins.

In each world, genetic instructions are written as a sequence in an alphabet of *j* characters. The sequence is translated into a protein, with consecutive non-overlapping codons of *k* characters each being converted into one of two amino acid types — hydrophobic (H) or polar (P) — according to a hidden codon table. The resulting 16-residue H/P chain folds on a two-dimensional square lattice under Dill's HP model, and fitness is the count of favorable non-consecutive H–H contacts in the optimal fold. No chain can exceed 9 such contacts, so the fitness ceiling is the same in every world.

The agent is told only the alphabet and the sequence length. It is not told that sequences contain codons, how codons might be translated, or that folding exists. It must infer all of this from fitness signal alone. Each run consists of *M*=500 design rounds, one query per round.

## Agent interface

A custom Python harness (`harness.py`) drives the agent through the Anthropic API with exactly two tools:

- **`query(sequence)`** — submit one sequence, receive its fitness. One query per turn, enforced in code.
- **`write_notebook(entry)`** — append to an append-only lab notebook.

The one-query-per-turn constraint forces the agent to deliberate between each experiment rather than batching queries programmatically. Invalid inputs (wrong length, wrong alphabet, non-encoding sequences) silently return fitness 0; no error messages reveal structure.

## Worlds

Eight worlds vary one structural parameter at a time from an Earth-like baseline. Worlds differ along four axes: alphabet size (*j*), codon length (*k*), whether a codon contains silent positions, and whether the informative positions act additively or interact.

| World | *j* | *k* | Codons | Structure |
|-------|-----|-----|--------|-----------|
| `earthlike` | 4 | 3 | 64 | Control: all positions determining, additive |
| `codon2` | 4 | 2 | 16 | Shorter codons |
| `codon4` | 4 | 4 | 256 | Longer codons |
| `alpha6` | 6 | 3 | 216 | Larger alphabet |
| `alpha8` | 8 | 3 | 512 | Larger alphabet |
| `pos1_only` | 4 | 3 | 64 | Only the central codon position determines the residue; outer positions are silent |
| `pos02_interact` | 4 | 3 | 64 | Outer positions jointly determine the residue via non-additive interaction; center is silent |
| `alien` | 6 | 4 | 1,296 | Three positions interact non-additively, one silent (hardest) |

Each world's codon table is built deterministically from its parameters under a fixed seed and balanced so that half the codons map to H and half to P.

## Folding substrate

All worlds share the same folding physics. Fitness is computed by exact enumeration of all self-avoiding walks on a 2D square lattice for 16-residue H/P chains.

- `hp_fold.py` — exact HP folding (Python reference implementation)
- `hpfold.c` — fast C implementation for folding and table enumeration
- `contacts_16.bin` — precomputed symmetry-reduced contact lists for 16-residue chains
- `table_16.bin` — complete fitness lookup for all 2^16 H/P chains

## Running

```bash
# Build the folding substrate (skip if .bin files already exist)
gcc -O3 -march=native -o hpfold hpfold.c
./hpfold build 16 contacts_16.bin
./hpfold enumerate contacts_16.bin 16 table_16.bin

# Install Python dependencies
pip install anthropic

# Run a world (M=500 design rounds, one query per round)
python harness.py earthlike --budget 500
```

## Run results

`runs/<world>/` contains:
- `notebook.md` — the agent's full reasoning trajectory (append-only)
- `queries.jsonl` — every query with hidden ground truth (true residues, energy, degeneracy) for post-hoc grading
- `summary.json` — final fitness, best sequence, fraction-of-optimum
- `GROUND_TRUTH.json` — the world's true codon table and structure (never shown to the agent)
- `transcript.jsonl` — full API message transcript
