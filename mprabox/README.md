# MPRAbox

A science sandbox for regulatory sequence design. MPRAbox asks whether an autonomous agent can design maximally informative libraries of regulatory DNA sequences for training predictive sequence-to-activity models.

In each of *M* design rounds, the agent designs a library of 50,000 200bp DNA sequences. A sealed in silico MPRA oracle (Malinois) labels the sequences, a surrogate model is trained from scratch on those labels, and performance is evaluated on 14 hidden held-out test sets spanning empirical MPRA measurements, human genetic variants, annotated regulatory elements, genomic background, and synthetic DNA. The agent receives only the Pearson correlation for each evaluation set and their mean — no sequence-level predictions, evaluation set identities, or oracle internals.

## Agent interface

Agents operate within a general-purpose coding environment (Claude Code, Codex CLI, or Gemini CLI) with access to the file system, shell, web search, and package management. The agent reads an `instructions.md` file, then autonomously designs and executes experiments by writing Python scripts and calling a sealed evaluation harness (`prepare.py`). The agent treats `prepare.py` as a wet-lab collaborator: it hands in sequences and gets back measurements.

## Setup

```bash
cd mprabox
python3.12 -m venv venv
source venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install numpy scipy pandas matplotlib lightning
bash setup.sh
```

`setup.sh` clones `boda2`, downloads pretrained Malinois weights (~700 MB), and builds the eval set index.

## Running an agent

1. Copy the desired instruction variant:

```bash
# Long-horizon, without prior knowledge (M=30):
cp instructions/long_horizon_without_prior_knowledge.md instructions.md

# One-shot, with prior knowledge (single library):
cp instructions/oneshot_with_prior_knowledge.md instructions.md
```

2. Point your agent at the task: **"Read `instructions.md` and get started."**

## Conditions

| Condition | Description |
|-----------|-------------|
| **Without prior knowledge** | Agent receives only the task specification and submission interface |
| **With prior knowledge** | Agent additionally receives descriptions of human-designed strategies and their performance scores |

## Experiment regimes

**One-shot (M=1):** The agent designs and submits a single library. Five independent replicates per model per condition (3 models × 2 conditions × 5 replicates = 30 runs).

**Long-horizon (M=30):** The agent submits *M*=30 successive libraries, receiving the evaluation report after each round before designing the next. Four independent runs (2 without prior knowledge, 2 with prior knowledge), Claude Opus 4.7 only.

## Evaluation suite

Models are evaluated on 14 held-out evaluation sets derived from nine source distributions. Evaluation set identities are hidden from the agent.

| Source | Labels | Sequences |
|--------|--------|-----------|
| MPRA holdout, chr7/13 | Experimental + Malinois | 60,055 |
| MPRA holdout, chr19/21/X | Experimental + Malinois | 56,340 |
| UKBB/GTEx fine-mapped variants | Experimental + Malinois | 59,084 |
| UKBB/GTEx, both alleles | Experimental + Malinois | 62,966 |
| UKBB/GTEx, one allele | Experimental + Malinois | 30,505 |
| Sei regulatory classes | Malinois | 20,000 |
| DHS index | Malinois | 20,000 |
| Genomic windows | Malinois | 20,000 |
| Synthetic DNA | Malinois | 20,000 |

## Human-designed reference panel

14 human-designed strategies provide a reproducible baseline, each evaluated at 7 library sizes (10k–300k) × 5 seeds. Strategies span DHS topic-weighted sampling, Sei class-balanced sampling, synthetic DNA, prior MPRA sequences, and multi-source mixtures. Results in `baselines/results/baselines.csv`.

## Oracle and surrogate

**In silico MPRA oracle** (`eval/oracle.py`): Malinois, a deep CNN trained on 776,474 MPRA measurements across K562, HepG2, and SK-N-SH. Returns predicted log2 fold-change for each submitted sequence.

**Surrogate model** (`eval/surrogate.py`): A fresh CNN trained from scratch on oracle-labeled sequences with locked hyperparameters. Same architecture as Malinois, no shared weights. Generalisation must come entirely from the submitted training library.

## Dry oracles

14 invented scoring rules that replace the Malinois oracle while preserving the same library-design task. Each dry oracle assigns synthetic activity values via a hidden rule (nucleotide composition, positional patterns, compressibility, number theory, cellular automata, or a hidden cipher). Libraries are scored using 6-mer Ridge regression rather than a CNN surrogate.

Three task framings:
- **MPRA-framed** — agent believes it is designing regulatory DNA
- **Unframed** — black-box optimisation over {A,C,G,T}, no biological context
- **Symbolic** — alphabet replaced with {0,1,2,3}, no biological connotation

See `dry_oracles/README.md` for the 14 rules and per-oracle results.

## Results

### One-shot

`results/oneshot/{without_prior_knowledge,with_prior_knowledge}/{claude,gpt,gemini}_{1..5}/`

Each run contains: `generate.py`, `library/result.json`, `notebook.md`, `session.jsonl`.

### Long-horizon

`results/long_horizon/{without,with}_prior_knowledge_{1,2}/`

Each run contains: `notebook.md`, `results.tsv`, `libraries/`, `skills/`, `session.jsonl`.
