"""
Compute strategies.md for each adversarial oracle by running simple baseline
strategies through each oracle's evaluation pipeline.
"""

import sys
import os
import time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = '/data/users/arao/.cache/.e'
sys.path.insert(0, ENGINE)

from eval.harness import _load_and_relabel_eval_sets, _kmer_features, _train_and_eval
from eval.oracles import get_oracle

N = 50_000
SEQ_LEN = 200

ORACLES = [
    'v01_gc_balance', 'v02_alternating_purine', 'v03_english_words',
    'v04_compression', 'v05_prime_counts', 'v06_fibonacci_spell',
    'v07_game_of_life', 'v08_modular_cross', 'v09_collatz', 'v10_rle_sin_xor',
]

BASES = list('ACGT')


def make_random_uniform(n, seed):
    rng = np.random.RandomState(seed)
    idx = rng.randint(0, 4, size=(n, SEQ_LEN))
    return [''.join(BASES[j] for j in row) for row in idx]


def make_gc_sweep(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for i in range(n):
        gc_frac = i / n
        seq = []
        for _ in range(SEQ_LEN):
            if rng.random() < gc_frac:
                seq.append('G' if rng.random() < 0.5 else 'C')
            else:
                seq.append('A' if rng.random() < 0.5 else 'T')
        seqs.append(''.join(seq))
    return seqs


def make_gc_50(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        seq = []
        for _ in range(SEQ_LEN):
            if rng.random() < 0.5:
                seq.append('G' if rng.random() < 0.5 else 'C')
            else:
                seq.append('A' if rng.random() < 0.5 else 'T')
        seqs.append(''.join(seq))
    return seqs


def make_at_rich(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        seq = []
        for _ in range(SEQ_LEN):
            if rng.random() < 0.8:
                seq.append('A' if rng.random() < 0.5 else 'T')
            else:
                seq.append('G' if rng.random() < 0.5 else 'C')
        seqs.append(''.join(seq))
    return seqs


def make_gc_rich(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        seq = []
        for _ in range(SEQ_LEN):
            if rng.random() < 0.8:
                seq.append('G' if rng.random() < 0.5 else 'C')
            else:
                seq.append('A' if rng.random() < 0.5 else 'T')
        seqs.append(''.join(seq))
    return seqs


def make_homopolymer_rich(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        seq = []
        pos = 0
        while pos < SEQ_LEN:
            base = BASES[rng.randint(4)]
            run_len = rng.geometric(0.1)
            run_len = min(run_len, SEQ_LEN - pos)
            seq.extend([base] * run_len)
            pos += run_len
        seqs.append(''.join(seq[:SEQ_LEN]))
    return seqs


def make_alternating_ry(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        seq = []
        for j in range(SEQ_LEN):
            if j % 2 == 0:
                seq.append('A' if rng.random() < 0.5 else 'G')
            else:
                seq.append('C' if rng.random() < 0.5 else 'T')
        seqs.append(''.join(seq))
    return seqs


def make_dinuc_repeat(n, seed):
    rng = np.random.RandomState(seed)
    dinucs = ['AC', 'AG', 'AT', 'CA', 'CG', 'CT', 'GA', 'GC', 'GT', 'TA', 'TC', 'TG']
    seqs = []
    for _ in range(n):
        d = dinucs[rng.randint(len(dinucs))]
        seq = (d * 100)[:SEQ_LEN]
        pos = rng.randint(0, SEQ_LEN - 10)
        noise_len = rng.randint(5, 20)
        noise = ''.join(BASES[rng.randint(4)] for _ in range(noise_len))
        seq = seq[:pos] + noise + seq[pos + noise_len:]
        seqs.append(seq[:SEQ_LEN])
    return seqs


def make_dirichlet_composition(n, seed):
    rng = np.random.RandomState(seed)
    seqs = []
    for _ in range(n):
        probs = rng.dirichlet([0.5, 0.5, 0.5, 0.5])
        idx = rng.choice(4, size=SEQ_LEN, p=probs)
        seqs.append(''.join(BASES[j] for j in idx))
    return seqs


STRATEGIES = {
    'random_uniform': (make_random_uniform, 'Fully random sequences, each base equally likely.'),
    'gc_sweep': (make_gc_sweep, 'GC content linearly swept from 0% to 100% across sequences.'),
    'gc_50': (make_gc_50, 'All sequences at 50% GC content.'),
    'at_rich': (make_at_rich, '80% AT, 20% GC — biased toward A and T.'),
    'gc_rich': (make_gc_rich, '80% GC, 20% AT — biased toward G and C.'),
    'homopolymer_rich': (make_homopolymer_rich, 'Sequences with long runs of the same base (geometric run lengths).'),
    'alternating_ry': (make_alternating_ry, 'Strict alternation of purines and pyrimidines (RYRYRY...).'),
    'dinuc_repeat': (make_dinuc_repeat, 'Dinucleotide repeats (e.g., ACACAC...) with small random patches.'),
    'dirichlet_composition': (make_dirichlet_composition, 'Each sequence draws base frequencies from a Dirichlet prior — diverse compositions.'),
}


def evaluate_against_oracle(all_seqs, oracle_name):
    label_fn = get_oracle(oracle_name)
    print(f"  Loading + relabeling eval sets...", flush=True)
    eval_sets = _load_and_relabel_eval_sets(label_fn)
    print(f"  Featurizing eval sets...", flush=True)
    eval_feat = {}
    for label in sorted(eval_sets):
        seqs, labels = eval_sets[label]
        eval_feat[label] = (_kmer_features(seqs), labels)

    results = {}
    for name, seqs in all_seqs.items():
        print(f"    {name}...", flush=True)
        labels = label_fn(seqs)
        X = _kmer_features(seqs)
        results[name] = _train_and_eval(X, labels, eval_feat)
    return results


def write_strategies_md(oracle_name, results):
    eval_labels = sorted(next(iter(results.values())).keys())
    lines = [
        "# Baseline Strategies\n",
        "",
        "Performance of systematic baseline strategies evaluated before your run.",
        "All used exactly 50,000 sequences. Performance is Pearson r (mean_r).\n",
        "",
        "## Strategy Descriptions\n",
    ]
    for name, (_, desc) in STRATEGIES.items():
        lines.append(f"**{name}** — {desc}\n")

    lines.extend(["", "---\n", "", "## Results\n", ""])

    header = "| strategy | " + " | ".join(eval_labels) + " |"
    sep = "|" + "|".join(["--------"] * (len(eval_labels) + 1)) + "|"
    lines.extend([header, sep])

    sorted_b = sorted(results.keys(),
                       key=lambda b: results[b].get('eval_01', {}).get('mean_r', 0),
                       reverse=True)
    for b in sorted_b:
        vals = [f"{results[b].get(ev, {}).get('mean_r', 0):.4f}" for ev in eval_labels]
        lines.append(f"| {b:30s} | " + " | ".join(vals) + " |")

    out_path = os.path.join(_HERE, 'strategies', f'{oracle_name}.md')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_path}", flush=True)


def main():
    print("=== Generating baseline sequences ===", flush=True)
    all_seqs = {}
    for name, (gen_fn, _) in STRATEGIES.items():
        print(f"  {name}...", flush=True)
        all_seqs[name] = gen_fn(N, seed=0)

    print(f"\n=== Evaluating against {len(ORACLES)} oracles ===", flush=True)
    for oracle_name in ORACLES:
        t0 = time.time()
        print(f"\nOracle: {oracle_name}", flush=True)
        results = evaluate_against_oracle(all_seqs, oracle_name)
        write_strategies_md(oracle_name, results)
        print(f"  Done in {time.time()-t0:.0f}s", flush=True)

    print("\n=== All done ===", flush=True)


if __name__ == '__main__':
    main()
