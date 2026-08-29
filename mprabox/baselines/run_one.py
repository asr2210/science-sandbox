"""Run a single (baseline, size, seed) — patches BASELINES before calling run_seed."""
import sys, os, argparse

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_baselines as rb

parser = argparse.ArgumentParser()
parser.add_argument('--baseline', required=True)
parser.add_argument('--size', type=int, required=True)
parser.add_argument('--seed', type=int, required=True)
args = parser.parse_args()

out_csv = rb.seed_csv(args.seed)
if rb.already_done(out_csv, args.baseline, args.size, args.seed):
    print(f'SKIP {args.baseline} n={args.size:,} seed={args.seed} — already done')
    sys.exit(0)

# Restrict to just this baseline
rb.BASELINES = [args.baseline]
rb.run_seed(args.seed, [args.size])
