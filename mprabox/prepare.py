"""
prepare.py — MPRA evaluation harness.

Usage:
    python prepare.py libraries/NNN_name/

Requires sequences_0.txt, sequences_1.txt, sequences_2.txt in the directory.
Each file must contain exactly 50,000 lines of exactly 200 ACGT characters.

prepare.py:
  - Labels each library with the Malinois oracle (eval/oracle.py)
  - Trains a surrogate model on each labeled library (eval/surrogate.py)
  - Evaluates the surrogate on 14 held-out eval sets (data/eval_sets.pkl)
  - Averages scores across the three seeds
  - Writes result.json to the experiment directory

DO NOT MODIFY THIS FILE.
"""

import sys
import os
import json
import time
import pickle

import numpy as np

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

from eval.oracle    import label_sequences
from eval.surrogate import train_and_eval

_EVAL_PKL = os.path.join(_ROOT, 'data', 'eval_sets.pkl')

# Fixed anonymization mapping — same seed used throughout the paper
# Agents see eval_01..eval_14; the mapping to named sets is fixed but not revealed.
_ANON_SEED = 2026


def _load_eval_sets():
    if not os.path.isfile(_EVAL_PKL):
        raise FileNotFoundError(
            f"eval_sets.pkl not found at {_EVAL_PKL}.\n"
            "Run setup.sh first: bash setup.sh"
        )
    with open(_EVAL_PKL, 'rb') as f:
        raw = pickle.load(f)

    # Replicate original prepare.py logic: split gt vs oracle, preserve insertion order.
    # Sets with both ground_truth and oracle_labels produce two entries.
    named = {}
    for name, d in raw.items():
        labels = d.get('ground_truth', d.get('oracle_labels'))
        named[name] = (d['sequences'], labels)
        if 'oracle_labels' in d and 'ground_truth' in d:
            named[f'{name}_oracle'] = (d['sequences'], d['oracle_labels'])

    # Anonymize using insertion order (NOT sorted) + fixed seed — must match paper.
    names = list(named.keys())
    rng = np.random.RandomState(_ANON_SEED)
    shuffled = names.copy()
    rng.shuffle(shuffled)
    label_map = {f'eval_{i+1:02d}': name for i, name in enumerate(shuffled)}
    anon_sets = {label: named[name] for label, name in label_map.items()}
    return anon_sets


def _validate(seqs_path):
    with open(seqs_path) as f:
        sequences = [line.strip() for line in f if line.strip()]
    if len(sequences) != 50_000:
        raise ValueError(f"expected 50,000 sequences, got {len(sequences)}")
    valid_chars = set('ACGT')
    bad = [i for i, s in enumerate(sequences)
           if len(s) != 200 or not set(s).issubset(valid_chars)]
    if bad:
        raise ValueError(
            f"{len(bad)} sequences have invalid length or non-ACGT characters "
            f"(first bad index: {bad[0]})"
        )
    return sequences


def _evaluate_seed(sequences, eval_sets, seed, ckpt_path):
    print(f"  [seed {seed}] Labeling {len(sequences)} sequences...", flush=True)
    labels = label_sequences(sequences)

    print(f"  [seed {seed}] Training surrogate...", flush=True)
    metrics = train_and_eval(
        sequences, labels, eval_sets,
        seed=seed, save_checkpoint=ckpt_path,
    )

    per_eval = {}
    for label in sorted(eval_sets):
        if label in metrics:
            m = metrics[label]
            per_eval[label] = {
                'mean_r':  round(m['mean_pearson'], 4),
                'k562_r':  round(m['pearson']['K562'], 4),
                'hepg2_r': round(m['pearson']['HepG2'], 4),
                'sknsh_r': round(m['pearson']['SKNSH'], 4),
            }

    print(f"  [seed {seed}] eval_01={per_eval.get('eval_01', {}).get('mean_r', 'N/A'):.4f}", flush=True)
    return per_eval


def run_multi(exp_dir):
    exp_dir = os.path.abspath(exp_dir)
    seed_files = [(i, os.path.join(exp_dir, f'sequences_{i}.txt')) for i in range(3)]
    seed_files = [(i, p) for i, p in seed_files if os.path.isfile(p)]

    if not seed_files:
        print(f"Error: no sequences_N.txt files found in {exp_dir}")
        sys.exit(1)

    print(f"Validating {len(seed_files)} sequence files...", flush=True)
    seed_seqs = []
    for i, p in seed_files:
        try:
            seqs = _validate(p)
            seed_seqs.append((i, seqs))
        except ValueError as e:
            print(f"Error in sequences_{i}.txt: {e}")
            sys.exit(1)
    print("  All files valid.", flush=True)

    print("Loading eval sets...", flush=True)
    eval_sets = _load_eval_sets()
    print(f"  Loaded {len(eval_sets)} eval sets.", flush=True)

    t0 = time.perf_counter()
    all_results = []
    for seed_idx, sequences in seed_seqs:
        ckpt_path = os.path.join(exp_dir, f'model_{seed_idx}.pt')
        per_eval  = _evaluate_seed(sequences, eval_sets, seed_idx, ckpt_path)
        all_results.append(per_eval)

    elapsed = time.perf_counter() - t0

    eval_labels = sorted(eval_sets.keys())
    averaged = {}
    for label in eval_labels:
        averaged[label] = {
            'mean_r':  round(sum(r[label]['mean_r']  for r in all_results) / len(all_results), 4),
            'k562_r':  round(sum(r[label]['k562_r']  for r in all_results) / len(all_results), 4),
            'hepg2_r': round(sum(r[label]['hepg2_r'] for r in all_results) / len(all_results), 4),
            'sknsh_r': round(sum(r[label]['sknsh_r'] for r in all_results) / len(all_results), 4),
        }
    averaged['n_seeds'] = len(all_results)
    averaged['time_s']  = round(elapsed, 1)
    averaged['seeds']   = [{label: r[label] for label in eval_labels} for r in all_results]

    result_path = os.path.join(exp_dir, 'result.json')
    with open(result_path, 'w') as f:
        json.dump(averaged, f, indent=2)

    print(f"\nResults ({elapsed:.0f}s total):")
    for label in eval_labels:
        s = averaged[label]
        print(f"  {label}: mean={s['mean_r']:.4f}  "
              f"K562={s['k562_r']:.4f}  HepG2={s['hepg2_r']:.4f}  SKNSH={s['sknsh_r']:.4f}")
    print(f"\nResult written to {result_path}")


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print("Usage: python prepare.py libraries/NNN_name/")
        print("       (directory must contain sequences_0.txt, sequences_1.txt, sequences_2.txt)")
        sys.exit(1)

    run_multi(sys.argv[1])


if __name__ == '__main__':
    main()
