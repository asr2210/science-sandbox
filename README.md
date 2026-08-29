# Science Sandboxes

Code and results for **"Science sandboxes measure the scientific capability of AI agents"**.

This repository contains two sandboxes — sealed experimental environments where AI agents conduct autonomous scientific research against ground-truth oracles:

- **MPRAbox** — regulatory sequence design for massively parallel reporter assays (MPRA)
- **CodonBox** — protein fitness prediction in invented biological worlds

## Repository structure

```
science-sandbox/
├── mprabox/                    # Regulatory sequence design sandbox
│   ├── prepare.py              # Sealed evaluation harness
│   ├── eval/                   # Malinois oracle + surrogate model trainer
│   ├── data/                   # Model weights + 14 held-out eval sets
│   ├── instructions/           # Agent task prompts (all conditions)
│   ├── baselines/              # Human-designed strategies
│   ├── results/
│   │   ├── oneshot/            # M=1
│   │   └── long_horizon/       # M=30
│   └── dry_oracles/            # Invented rules
│
└── codonbox/                   # Protein fitness prediction sandbox
    ├── oracle.py               # Sealed oracle interface
    ├── harness.py              # Agent loop driver
    ├── world.py                # 8 world definitions
    └── runs/                   # Agent trajectories for all 8 worlds
```

## MPRAbox

Agents design 50,000-sequence DNA libraries evaluated by a pretrained Malinois model (oracle). A surrogate CNN is trained from scratch on oracle-labeled sequences and evaluated on 14 held-out genomic test sets. The agent never sees the eval set identities.

**Conditions:**
- *Without prior knowledge* — no information about baselines or strategies
- *With prior knowledge* — summary of human-designed strategies provided

**Dry oracles:** 14 synthetic scoring functions of increasing difficulty, tested under three framings:
- *MPRA-framed* — agent believes it is designing a real MPRA library
- *Unframed* — black-box optimization, no biological context
- *Symbolic* — alphabet is {0,1,2,3}, no biological connotation

See [`mprabox/README.md`](mprabox/README.md) for setup and usage.

## CodonBox

An agent explores a counterfactual world with a single tool: submit a DNA-like sequence, get a fitness score of the resulting protein. The world has a hidden codon table, folding physics, and position structure. The agent must discover how the world works from fitness signal alone.

8 worlds of increasing complexity, from DNA-like (`earthlike`) to alien biologies (`alien`).

See [`codonbox/README.md`](codonbox/README.md) for setup and usage.

## Citation

```bibtex
@article{rao2026science,
  title={Science sandboxes measure the scientific capability of AI agents},
  author={Rao, Arya},
  year={2026}
}
```

## License

MIT. See [LICENSE](LICENSE). Malinois model weights are subject to the [boda2 license](https://github.com/sjgosai/boda2).
