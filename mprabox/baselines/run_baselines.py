"""
run_baselines.py — AR003: Re-run all baselines against extended test set suite.

Runs the same 14 baselines as AR001+AR002 but evaluates against all 9 test sets
and saves model checkpoints so future test sets can be evaluated without retraining.

Baselines (same sequences as AR001/AR002, regenerated deterministically):
  AR001: mpra_oracle, mpra_real, synth_oracle
  AR002: dhs_topic, dhs_random, sei_class, sei_random,
         dhs_sei, dhs_sei_synth, dhs_synth, sei_synth,
         dhs_stratified, dhs_stratified_sei, dhs_stratified_sei_synth

Test sets (all 9 from test_sets_extended.pkl):
  chr7_13_gt        — primary, ground truth (agent-visible metric)
  chr19_21_X_gt     — cross-chromosome, ground truth
  dhs_chr7_13       — DHS generalization probe, oracle-labeled
  sei_chr7_13       — SEI generalization probe, oracle-labeled
  genomic_chr7_13   — genomic background probe, oracle-labeled
  synthetic         — synthetic generalization probe, oracle-labeled
  ukbb_gtex_both    — UKBB+GTEx both alleles, oracle+GT
  ukbb_gtex_one     — UKBB+GTEx one allele, oracle+GT
  ukbb_gtex_gt      — UKBB+GTEx empirical labels

Usage:
    nohup python run_baselines.py --seed 0 --sizes 50000 > ../../logs/ar003_seed0.log 2>&1 &
    python run_baselines.py --merge
"""

import os, sys, time, argparse, warnings, multiprocessing, datetime, gzip, io
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, '..', '..'))
_CKPT_DIR     = os.path.join(_SCRIPT_DIR, 'checkpoints')
_OUTPUT_DIR   = os.path.join(_SCRIPT_DIR, 'output_20260416')

for _p in [_PROJECT_ROOT, os.path.join(_PROJECT_ROOT, 'boda2')]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

DATA_DIR  = os.path.join(_PROJECT_ROOT, 'data')
POOLS_DIR = os.path.join(DATA_DIR, 'pools')
LOGS_DIR  = os.path.join(_PROJECT_ROOT, 'logs')
MPRA_FILE = os.path.join(DATA_DIR, 'Table_S2__MPRA_dataset.txt')

SEEDS = [0, 1, 2, 3, 4]
DEFAULT_SIZES = [50_000]

# Adaptive patience
def patience_for(n): return 10 if n >= 100_000 else 20

# ── Test set loading ──────────────────────────────────────────────────────────
_TEST_SETS_CACHE = None

def load_extended_test_sets():
    global _TEST_SETS_CACHE
    if _TEST_SETS_CACHE is None:
        import pickle
        path = os.path.join(DATA_DIR, 'test_sets_extended.pkl')
        with open(path, 'rb') as f:
            _TEST_SETS_CACHE = pickle.load(f)
    return _TEST_SETS_CACHE


def build_eval_sets(ts):
    """Build the test_sets dict for train_and_eval from the extended test sets pkl."""
    sets = {}
    for name, d in ts.items():
        seqs   = d['sequences']
        # Prefer ground_truth labels if available, else oracle_labels
        labels = d.get('ground_truth', d.get('oracle_labels'))
        sets[name] = (seqs, labels)
        # Also add oracle variant
        if 'oracle_labels' in d and 'ground_truth' in d:
            sets[f'{name}_oracle'] = (seqs, d['oracle_labels'])
    return sets


# ── Baseline sequence generation (mirrors AR001/AR002) ────────────────────────
def make_synthetic(n, seed):
    rng = np.random.RandomState(seed + 9999)
    idx = rng.randint(0, 4, size=(n, 200))
    return [''.join(row) for row in np.array(list('ACGT'))[idx]]


def get_mpra_sequences(n, seed, df=None):
    from prepare_test_sets import get_train_sequences
    return get_train_sequences(n, seed=seed, df=df)


def sample_pool(pool, n, seed, weighted=True):
    rng = np.random.RandomState(seed + 7777)
    if weighted:
        w = pool['sample_weight'].values.astype(np.float64)
        w = np.maximum(w, 0); w /= w.sum()
        idx = rng.choice(len(pool), size=min(n, len(pool)), replace=False, p=w)
    else:
        idx = rng.choice(len(pool), size=min(n, len(pool)), replace=False)
    return pool['sequence'].iloc[idx].tolist()


def sample_dhs_stratified(dhs, n, seed):
    rng = np.random.RandomState(seed + 5555)
    n_per = n // 16; rem = n - n_per * 16
    seqs = []
    for c in range(16):
        pool_c = dhs[dhs['top_component'] == c]['sequence']
        n_c = min(n_per + (1 if c < rem else 0), len(pool_c))
        chosen = rng.choice(len(pool_c), size=n_c, replace=False)
        seqs.extend(pool_c.iloc[chosen].tolist())
    rng.shuffle(seqs)
    return seqs


def get_baseline_seqs_labels(baseline, n, seed, df_mpra, dhs, sei, mpra_oracle_cache):
    """Return (sequences, labels) for a given baseline."""
    from oracle import label_sequences

    if baseline == 'mpra_oracle':
        seqs, _ = get_mpra_sequences(n, seed, df=df_mpra)
        # Cache oracle labels for mpra_real reuse
        labels = mpra_oracle_cache.get((n, seed))
        if labels is None:
            labels = label_sequences(seqs, batch_size=512)
            mpra_oracle_cache[(n, seed)] = (seqs, labels)
        else:
            seqs, labels = mpra_oracle_cache[(n, seed)]
        return seqs, labels

    elif baseline == 'mpra_real':
        # Same sequences as mpra_oracle, real labels
        if (n, seed) in mpra_oracle_cache:
            seqs, _ = mpra_oracle_cache[(n, seed)]
        else:
            seqs, _ = get_mpra_sequences(n, seed, df=df_mpra)
        _, gt = get_mpra_sequences(n, seed, df=df_mpra)
        return seqs, gt

    elif baseline == 'synth_oracle':
        seqs = make_synthetic(n, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_topic':
        seqs = sample_pool(dhs, n, seed, weighted=True)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_random':
        seqs = sample_pool(dhs, n, seed, weighted=False)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'sei_class':
        seqs = sample_pool(sei, n, seed, weighted=True)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'sei_random':
        seqs = sample_pool(sei, n, seed, weighted=False)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_sei':
        seqs = sample_pool(dhs, n//2, seed, weighted=True) + sample_pool(sei, n-n//2, seed, weighted=True)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_sei_synth':
        n3 = n//3
        seqs = sample_pool(dhs, n3, seed, True) + sample_pool(sei, n3, seed, True) + make_synthetic(n-2*n3, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_synth':
        seqs = sample_pool(dhs, n//2, seed, True) + make_synthetic(n-n//2, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'sei_synth':
        seqs = sample_pool(sei, n//2, seed, True) + make_synthetic(n-n//2, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_stratified':
        seqs = sample_dhs_stratified(dhs, n, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_stratified_sei':
        seqs = sample_dhs_stratified(dhs, n//2, seed) + sample_pool(sei, n-n//2, seed, True)
        return seqs, label_sequences(seqs, batch_size=512)

    elif baseline == 'dhs_stratified_sei_synth':
        n3 = n//3
        seqs = sample_dhs_stratified(dhs, n3, seed) + sample_pool(sei, n3, seed, True) + make_synthetic(n-2*n3, seed)
        return seqs, label_sequences(seqs, batch_size=512)

    else:
        raise ValueError(f"Unknown baseline: {baseline}")


BASELINES = [
    'mpra_oracle', 'mpra_real', 'synth_oracle',
    'dhs_topic', 'dhs_random', 'sei_class', 'sei_random',
    'dhs_sei', 'dhs_sei_synth', 'dhs_synth', 'sei_synth',
    'dhs_stratified', 'dhs_stratified_sei', 'dhs_stratified_sei_synth',
]

# ── CSV helpers ───────────────────────────────────────────────────────────────
def seed_csv(seed):
    return os.path.join(_OUTPUT_DIR, f'baselines_seed{seed}.csv')

def merged_csv():
    return os.path.join(_OUTPUT_DIR, 'baselines.csv')

def ckpt_path(baseline, size, seed):
    return os.path.join(_CKPT_DIR, f'{baseline}_{size}_seed{seed}.pt')

def already_done(path, baseline, size, seed):
    if not os.path.isfile(path): return False
    try:
        df = pd.read_csv(path)
        return bool(((df['baseline']==baseline)&(df['size']==size)&(df['seed']==seed)).any())
    except: return False

def append_row(path, row):
    new = pd.DataFrame([row])
    if os.path.isfile(path): new.to_csv(path, mode='a', header=False, index=False)
    else: new.to_csv(path, index=False)

def log(msg, seed=None):
    ts  = time.strftime('%H:%M:%S')
    pfx = f"[seed{seed}]" if seed is not None else "[main]  "
    print(f"{ts} {pfx} {msg}", flush=True)

# ── Per-seed worker ───────────────────────────────────────────────────────────
def run_seed(seed, sizes):
    import warnings; warnings.filterwarnings('ignore')
    import socket, numpy as np, pandas as pd, time, os, sys, pickle

    for _p in [_PROJECT_ROOT, os.path.join(_PROJECT_ROOT, 'boda2')]:
        if _p not in sys.path: sys.path.insert(0, _p)

    from surrogate import train_and_eval

    os.makedirs(_CKPT_DIR, exist_ok=True)
    os.makedirs(_OUTPUT_DIR, exist_ok=True)

    out_csv = seed_csv(seed)
    log(f"Worker started  pid={os.getpid()}  node={socket.gethostname()}", seed)

    # Load test sets once
    log("Loading extended test sets...", seed)
    ts = load_extended_test_sets()
    eval_sets = build_eval_sets(ts)
    log(f"  {len(eval_sets)} evaluation sets", seed)

    # Load pools
    log("Loading sequence pools...", seed)
    df_mpra = pd.read_table(MPRA_FILE)
    dhs = pd.read_parquet(os.path.join(POOLS_DIR, 'dhs_pool.parquet'),
                          columns=['sequence','sample_weight','top_component'])
    sei = pd.read_parquet(os.path.join(POOLS_DIR, 'sei_pool.parquet'),
                          columns=['sequence','sample_weight'])
    log(f"  MPRA: {len(df_mpra):,}  DHS: {len(dhs):,}  SEI: {len(sei):,}", seed)

    mpra_cache = {}  # (n, seed) -> (seqs, oracle_labels) for mpra_oracle/mpra_real sharing

    total = len(sizes) * len(BASELINES)
    done  = 0

    for size in sizes:
        for baseline in BASELINES:
            done += 1
            if already_done(out_csv, baseline, size, seed):
                log(f"SKIP {baseline} n={size:,} [{done}/{total}]", seed)
                continue

            pat = patience_for(size)
            log(f"START {baseline} n={size:,} patience={pat} [{done}/{total}]", seed)

            t0 = time.perf_counter()
            try:
                seqs, labels = get_baseline_seqs_labels(
                    baseline, size, seed, df_mpra, dhs, sei, mpra_cache)
                ckpt = ckpt_path(baseline, size, seed)
                m = train_and_eval(
                    seqs, labels, eval_sets,
                    seed=seed,
                    conv_warm_start=False,
                    early_stop_patience=pat,
                    save_checkpoint=ckpt,
                )
            except Exception as e:
                log(f"ERROR {baseline} n={size:,}: {e}", seed)
                import traceback; traceback.print_exc()
                continue

            elapsed = time.perf_counter() - t0

            # Build row: one column per test set per metric
            row = {'baseline': baseline, 'size': size, 'seed': seed,
                   'n_epochs': m['n_epochs'], 'val_loss': m['val_loss'],
                   'train_time_s': elapsed}
            for ts_name in eval_sets:
                if ts_name in m:
                    row[f'{ts_name}_mean'] = m[ts_name]['mean_pearson']
                    for ct in ['K562','HepG2','SKNSH']:
                        row[f'{ts_name}_{ct.lower()}'] = m[ts_name]['pearson'][ct]

            append_row(out_csv, row)
            primary = row.get('chr7_13_gt_mean', float('nan'))
            log(f"DONE  {baseline} n={size:,}  {elapsed:.0f}s  "
                f"{m['n_epochs']}ep  chr7_13_gt={primary:.4f}", seed)

    log(f"Seed complete → {out_csv}", seed)


# ── Merge ─────────────────────────────────────────────────────────────────────
def merge():
    parts = []
    for s in SEEDS:
        p = seed_csv(s)
        if os.path.isfile(p):
            try: parts.append(pd.read_csv(p))
            except: pass
    if not parts:
        print("No seed CSVs found.")
        return pd.DataFrame()
    df = pd.concat(parts, ignore_index=True).sort_values(['baseline','size','seed']).reset_index(drop=True)
    df.to_csv(merged_csv(), index=False)
    print(f"Merged {len(df)} rows → {merged_csv()}")
    return df


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today = datetime.date.today().strftime('%Y%m%d')
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed',  type=int, default=None)
    parser.add_argument('--sizes', type=int, nargs='+', default=DEFAULT_SIZES)
    parser.add_argument('--merge', action='store_true')
    args = parser.parse_args()

    os.makedirs(LOGS_DIR,    exist_ok=True)
    os.makedirs(_CKPT_DIR,   exist_ok=True)
    os.makedirs(_OUTPUT_DIR, exist_ok=True)

    if args.merge:
        merge()
        return

    if args.seed is not None:
        import socket
        print(f"{'='*68}")
        print(f"AR003 EXTENDED BASELINES — single-seed mode")
        print(f"  Node:  {socket.gethostname()}")
        print(f"  Seed:  {args.seed}  Sizes: {args.sizes}")
        print(f"  Baselines: {len(BASELINES)}")
        print(f"  Test sets: 9 (all from test_sets_extended.pkl)")
        print(f"  Checkpoints → {_CKPT_DIR}")
        print(f"{'='*68}")
        run_seed(args.seed, args.sizes)
        print(f"\nDone. Merge: python run_baselines.py --merge")
        return

    # Multi-seed local
    seeds = SEEDS
    multiprocessing.set_start_method('spawn', force=True)
    procs = []
    for s in seeds:
        p = multiprocessing.Process(target=run_seed, args=(s, args.sizes), name=f"seed{s}")
        p.start(); procs.append(p)
        print(f"Launched seed={s} pid={p.pid}")
        time.sleep(2)
    for p in procs:
        p.join()
    merge()


if __name__ == '__main__':
    main()
