"""Experiment 011: 6-mer Markov chain trained on hg38.

Conditional model P(next_base | previous 5 bases). 5^4=1024 states.
Trained on full hg38, then generate 50k sequences. Tests whether 5th-order
Markov statistics (6-mer composition) capture the score-relevant content.
"""
import pickle
import numpy as np
from pathlib import Path
import time

N = 50_000
L = 200
K = 5  # condition on last K bases, generate next
SEED = 11

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

valid = set("ACGT")
base2i = {b: i for i, b in enumerate("ACGT")}

t = time.time()
# Build transition counts: counts[kmer_idx, next_base] = #occurrences
# kmer_idx = 0..4^K - 1
n_states = 4 ** K
counts = np.zeros((n_states, 4), dtype=np.int64)

def kmer_to_idx(s):
    idx = 0
    for c in s:
        idx = idx * 4 + base2i[c]
    return idx

for name, seq in chroms.items():
    # Slide a length-(K+1) window, skip any window with N
    # Use numpy for speed: encode the chromosome to int8 with N=-1
    arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8).astype(np.int8)
    # Map ACGT to 0123, others to -1
    enc = np.full_like(arr, -1, dtype=np.int8)
    enc[arr == ord("A")] = 0
    enc[arr == ord("C")] = 1
    enc[arr == ord("G")] = 2
    enc[arr == ord("T")] = 3
    # Build kmer indices using cumulative shifts
    L_chr = len(enc)
    if L_chr < K + 1:
        continue
    # valid_mask[i] = True if enc[i..i+K] all >= 0
    valid_mask = enc >= 0
    # cum_valid[i] - cum_valid[i-K-1] == K+1 means all valid in window
    win = K + 1
    # Build sliding mask using convolution
    from numpy.lib.stride_tricks import sliding_window_view
    valid_win = sliding_window_view(valid_mask, win).all(axis=1)
    enc_win = sliding_window_view(enc, win)
    enc_clean = enc_win[valid_win]
    # Compute kmer_idx and next_base
    kmer = np.zeros(enc_clean.shape[0], dtype=np.int64)
    for j in range(K):
        kmer = kmer * 4 + enc_clean[:, j].astype(np.int64)
    nb = enc_clean[:, K].astype(np.int64)
    np.add.at(counts, (kmer, nb), 1)
    print(f"trained on {name}: total transitions so far {counts.sum():,}")

print(f"training done in {time.time()-t:.1f}s; total counts {counts.sum():,}")

# Normalize → probabilities, smooth with +1 for unseen states
row_sums = counts.sum(axis=1)
probs = (counts + 0.01) / (row_sums[:, None] + 0.04)

# Marginal 5-mer distribution for start
marg = row_sums + 0.01
marg = marg / marg.sum()

rng = np.random.default_rng(SEED)
out = []
bases = np.array(list("ACGT"))
# Vectorized generation: for each of N sequences, pick start 5-mer then walk
# Start: sample start kmer index from marg
start_idxs = rng.choice(n_states, size=N, p=marg)

# Decode start_idx to 5-mer base array
def decode_kmer(idx, K=K):
    out = []
    for _ in range(K):
        out.append(idx % 4)
        idx //= 4
    return list(reversed(out))

t2 = time.time()
# Build sequences
seqs_int = np.zeros((N, L), dtype=np.int8)
for n_i, st in enumerate(start_idxs):
    cur = decode_kmer(int(st))
    seqs_int[n_i, :K] = cur
    cur_idx = int(st)
    for j in range(K, L):
        p = probs[cur_idx]
        nb = int(rng.choice(4, p=p))
        seqs_int[n_i, j] = nb
        # Update kmer index: drop leftmost, append nb
        cur_idx = (cur_idx % (4 ** (K - 1))) * 4 + nb
print(f"generation done in {time.time()-t2:.1f}s")

# Convert to strings
out_strs = ["".join(bases[seqs_int[i]].tolist()) for i in range(N)]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out_strs:
        f.write(s + "\n")

print(f"Wrote {len(out_strs)} sequences of length {L}")
