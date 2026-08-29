""

import os
import sys
import json
import time
import pickle
from itertools import product

import numpy as np
from scipy.stats import pearsonr
from sklearn.linear_model import Ridge

_ROOT = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_ROOT)

from eval.oracles import get_oracle

_EVAL_PKL = os.path.join(_PARENT, 'data', 'eval_sets.pkl')
_ANON_SEED = 2026

_K = 6
_KMERS = [''.join(p) for p in product('ACGT', repeat=_K)]
_KMER_TO_IDX = {km: i for i, km in enumerate(_KMERS)}
_N_FEATURES = len(_KMERS)  # 4096

CELL_TYPES = ['K562', 'HepG2', 'SKNSH']


def _kmer_features(sequences):
    n = len(sequences)
    X = np.zeros((n, _N_FEATURES), dtype=np.float32)
    for i, seq in enumerate(sequences):
        for j in range(len(seq) - _K + 1):
            kmer = seq[j:j + _K]
            idx = _KMER_TO_IDX.get(kmer)
            if idx is not None:
                X[i, idx] += 1
        total = len(seq) - _K + 1
        if total > 0:
            X[i] /= total
    return X


def _load_and_relabel_eval_sets(label_fn):
    if not os.path.isfile(_EVAL_PKL):
        raise FileNotFoundError(
            f"eval_sets.pkl not found at {_EVAL_PKL}.\n"
            "Symlink to MPRAgent/data/eval_sets.pkl required."
        )
    with open(_EVAL_PKL, 'rb') as f:
        raw = pickle.load(f)

    named = {}
    for name, d in raw.items():
        seqs = d['sequences']
        named[name] = seqs
        if 'oracle_labels' in d and 'ground_truth' in d:
            named[f'{name}_oracle'] = seqs

    names = list(named.keys())
    rng = np.random.RandomState(_ANON_SEED)
    shuffled = names.copy()
    rng.shuffle(shuffled)
    label_map = {f'eval_{i+1:02d}': name for i, name in enumerate(shuffled)}

    anon_sets = {}
    for label, name in label_map.items():
        seqs = named[name]
        labels = label_fn(seqs)
        anon_sets[label] = (seqs, labels)

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


def _train_and_eval(X_train, Y_train, eval_sets_featurized, alpha=1.0):
    results = {}
    models = []
    for col in range(3):
        y = Y_train[:, col]
        mask = np.isfinite(y)
        reg = Ridge(alpha=alpha)
        reg.fit(X_train[mask], y[mask])
        models.append(reg)

    for label, (X_eval, Y_eval) in eval_sets_featurized.items():
        pearson_r = {}
        for col, ct in enumerate(CELL_TYPES):
            preds = models[col].predict(X_eval)
            y_true = Y_eval[:, col]
            mask = np.isfinite(y_true) & np.isfinite(preds)
            if mask.sum() < 3:
                pearson_r[ct] = 0.0
            else:
                r, _ = pearsonr(y_true[mask], preds[mask])
                pearson_r[ct] = float(r)
        results[label] = {
            'mean_r':  round(float(np.mean(list(pearson_r.values()))), 4),
            'k562_r':  round(pearson_r['K562'], 4),
            'hepg2_r': round(pearson_r['HepG2'], 4),
            'sknsh_r': round(pearson_r['SKNSH'], 4),
        }
    return results


def run(exp_dir, oracle_name):
    exp_dir = os.path.abspath(exp_dir)
    label_fn = get_oracle(oracle_name)

    seed_files = [(i, os.path.join(exp_dir, f'sequences_{i}.txt')) for i in range(3)]
    seed_files = [(i, p) for i, p in seed_files if os.path.isfile(p)]

    if not seed_files:
        print(f"Error: no sequences_N.txt files found in {exp_dir}")
        sys.exit(1)

    seed_seqs = []
    for i, p in seed_files:
        try:
            seqs = _validate(p)
            seed_seqs.append((i, seqs))
        except ValueError as e:
            print(f"Error in sequences_{i}.txt: {e}")
            sys.exit(1)

    print("Evaluating...", flush=True)
    eval_sets = _load_and_relabel_eval_sets(label_fn)

    eval_featurized = {}
    for label in sorted(eval_sets):
        seqs, labels = eval_sets[label]
        X = _kmer_features(seqs)
        eval_featurized[label] = (X, labels)

    t0 = time.perf_counter()
    all_results = []
    for seed_idx, sequences in seed_seqs:
        labels = label_fn(sequences)
        X_train = _kmer_features(sequences)
        per_eval = _train_and_eval(X_train, labels, eval_featurized)
        all_results.append(per_eval)

    elapsed = time.perf_counter() - t0

    eval_labels = sorted(eval_featurized.keys())
    if len(all_results) == 1:
        averaged = {label: all_results[0][label] for label in eval_labels}
    else:
        averaged = {}
        for label in eval_labels:
            averaged[label] = {
                'mean_r':  round(sum(r[label]['mean_r']  for r in all_results) / len(all_results), 4),
                'k562_r':  round(sum(r[label]['k562_r']  for r in all_results) / len(all_results), 4),
                'hepg2_r': round(sum(r[label]['hepg2_r'] for r in all_results) / len(all_results), 4),
                'sknsh_r': round(sum(r[label]['sknsh_r'] for r in all_results) / len(all_results), 4),
            }
    averaged['n_seeds'] = len(all_results)
    averaged['time_s'] = round(elapsed, 1)
    if len(all_results) > 1:
        averaged['seeds'] = [{label: r[label] for label in eval_labels} for r in all_results]

    result_path = os.path.join(exp_dir, 'result.json')
    with open(result_path, 'w') as f:
        json.dump(averaged, f, indent=2)

    print(f"\nResults ({elapsed:.0f}s total):")
    for label in eval_labels:
        s = averaged[label]
        print(f"  {label}: mean={s['mean_r']:.4f}  "
              f"K562={s['k562_r']:.4f}  HepG2={s['hepg2_r']:.4f}  SKNSH={s['sknsh_r']:.4f}")
    print(f"\nResult written to {result_path}")
