#!/usr/bin/env bash
# setup.sh — One-time setup: clone boda2, download Malinois weights, build eval_sets.pkl.
# Run once after copying/cloning: bash setup.sh

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# ── 1. boda2 (BassetBranched architecture) ────────────────────────────────────
if [ -d "boda2" ] && [ -f "boda2/boda/__init__.py" ]; then
    echo "[setup] boda2 already present."
else
    echo "[setup] Cloning boda2..."
    git clone https://github.com/sjgosai/boda2.git boda2
    echo "[setup] boda2 cloned."
fi

# ── 2. Malinois checkpoint ────────────────────────────────────────────────────
ARTIFACT_DIR="$REPO_ROOT/data/malinois/artifacts"
CKPT="$ARTIFACT_DIR/torch_checkpoint.pt"

if [ -f "$CKPT" ]; then
    echo "[setup] Malinois checkpoint already present."
else
    mkdir -p "$ARTIFACT_DIR"
    TARBALL="$REPO_ROOT/data/malinois_artifacts.tar.gz"
    URL="https://storage.googleapis.com/tewhey-public-data/CODA_resources/malinois_artifacts__20211113_021200__287348.tar.gz"

    echo "[setup] Downloading Malinois checkpoint (~700 MB)..."
    if command -v gsutil &>/dev/null; then
        gsutil -q cp gs://tewhey-public-data/CODA_resources/malinois_artifacts__20211113_021200__287348.tar.gz "$TARBALL"
    elif command -v curl &>/dev/null; then
        curl -L --progress-bar "$URL" -o "$TARBALL"
    elif command -v wget &>/dev/null; then
        wget -q --show-progress "$URL" -O "$TARBALL"
    else
        echo "ERROR: need gsutil, curl, or wget to download the Malinois checkpoint."
        echo "  URL: $URL"
        exit 1
    fi

    echo "[setup] Extracting..."
    tar -xzf "$TARBALL" -C "$ARTIFACT_DIR" --strip-components=2
    rm -f "$TARBALL"
    echo "[setup] Checkpoint saved to $CKPT"
fi

# ── 3. Build eval_sets.pkl from plain-text files ──────────────────────────────
PKL="$REPO_ROOT/data/eval_sets.pkl"

if [ -f "$PKL" ]; then
    echo "[setup] eval_sets.pkl already present."
else
    echo "[setup] Building eval_sets.pkl from data/eval_sets/ ..."
    python3 - << 'PYEOF'
import os, pickle
import numpy as np

REPO_ROOT = os.getcwd()
eval_dir  = os.path.join(REPO_ROOT, 'data', 'eval_sets')
out_path  = os.path.join(REPO_ROOT, 'data', 'eval_sets.pkl')

# Insertion order must match the original pkl — determines eval_01..eval_14 mapping.
ORDERED_NAMES = [
    'chr7_13_gt',
    'chr19_21_X_gt',
    'dhs_chr7_13',
    'sei_chr7_13',
    'genomic_chr7_13',
    'synthetic',
    'ukbb_gtex_both',
    'ukbb_gtex_one',
    'ukbb_gtex_gt',
]

eval_sets = {}
for name in ORDERED_NAMES:
    seq_path = os.path.join(eval_dir, f'{name}_sequences.txt')
    gt_path  = os.path.join(eval_dir, f'{name}_labels_gt.tsv')
    orc_path = os.path.join(eval_dir, f'{name}_labels_oracle.tsv')

    with open(seq_path) as f:
        seqs = [l.strip() for l in f if l.strip()]

    entry = {'sequences': seqs}
    if os.path.isfile(gt_path):
        entry['ground_truth'] = np.loadtxt(gt_path, delimiter='\t',
                                            skiprows=1, dtype=np.float32)
    if os.path.isfile(orc_path):
        entry['oracle_labels'] = np.loadtxt(orc_path, delimiter='\t',
                                             skiprows=1, dtype=np.float32)

    eval_sets[name] = entry
    print(f'  {name}: {len(seqs)} sequences')

with open(out_path, 'wb') as f:
    pickle.dump(eval_sets, f)
print(f'[setup] Written: {out_path}')
PYEOF
fi

# ── 4. Sanity check ───────────────────────────────────────────────────────────
echo "[setup] Running oracle sanity check (expect r ≈ 0.88 on chr7+13)..."
python3 - << 'PYEOF'
import sys, os, pickle
sys.path.insert(0, os.getcwd())
import numpy as np
from eval.oracle import label_sequences
from scipy.stats import pearsonr

with open('data/eval_sets.pkl', 'rb') as f:
    es = pickle.load(f)

d = es['chr7_13_gt']
seqs = d['sequences'][:500]
gt   = d['ground_truth'][:500]
preds = label_sequences(seqs)
rs = [pearsonr(gt[:, i], preds[:, i])[0] for i in range(3)]
print(f'  K562={rs[0]:.3f}  HepG2={rs[1]:.3f}  SKNSH={rs[2]:.3f}  mean={np.mean(rs):.3f}')
if np.mean(rs) < 0.80:
    print('  WARNING: r lower than expected.')
else:
    print('  OK.')
PYEOF

echo "[setup] All done. Run: python prepare.py libraries/NNN_name/"
