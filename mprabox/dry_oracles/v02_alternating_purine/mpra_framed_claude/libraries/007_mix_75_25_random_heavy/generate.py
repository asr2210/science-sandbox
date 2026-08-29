"""
Experiment 007 — 75/25 mix (random-heavy): 37,500 random + 12,500 cCRE.

Maps the random-side of the ratio curve. 005 (50/50) was 0.156.
006 (25/75 cCRE-heavy) was 0.134. If 007 is also < 005, then 50/50 is
the local optimum and we should lock it in. If 007 is > 005, more
random-heavy is even better.
"""
import os
import time
import numpy as np

N_SEQ = 50_000
N_RANDOM = 37_500
N_CCRE = N_SEQ - N_RANDOM
L = 200
HALF = L // 2
SEED = 0

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    genome = {}
    n_prefix = {}
    for f in sorted(os.listdir(cache_dir)):
        if f.endswith(".npy"):
            c = f[:-4]
            mat = np.asarray(np.load(os.path.join(cache_dir, f), mmap_mode="r"))
            genome[c] = mat
            is_n = (mat == ord("N")).astype(np.int32)
            n_prefix[c] = np.concatenate(([0], np.cumsum(is_n)))
    chroms = sorted(genome.keys())
    lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")

    rng = np.random.default_rng(SEED)
    p = lens / lens.sum()

    # random windows
    rand_seqs = []
    while len(rand_seqs) < N_RANDOM:
        need = N_RANDOM - len(rand_seqs)
        bs = need * 2
        chrom_idx = rng.choice(len(chroms), size=bs, p=p)
        chrom_lens_arr = lens[chrom_idx]
        starts = (rng.random(bs) * (chrom_lens_arr - L)).astype(np.int64)
        for i in range(bs):
            if len(rand_seqs) >= N_RANDOM:
                break
            c = chroms[chrom_idx[i]]
            s = int(starts[i])
            if n_prefix[c][s + L] - n_prefix[c][s] != 0:
                continue
            window = genome[c][s:s + L].tobytes().decode("ascii")
            if set(window) <= bases:
                rand_seqs.append(window)

    # cCREs
    chrom_to_idx = {c: i for i, c in enumerate(chroms)}
    cidx, mids = [], []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in chrom_to_idx:
                continue
            mids.append((int(parts[1]) + int(parts[2])) // 2)
            cidx.append(chrom_to_idx[c])
    cidx = np.array(cidx, dtype=np.int32)
    mids = np.array(mids, dtype=np.int64)

    order = rng.permutation(len(mids))
    ccre_seqs = []
    for j in order:
        c = chroms[cidx[j]]
        start = int(mids[j]) - HALF
        if start < 0 or start + L > lens[cidx[j]]:
            continue
        if n_prefix[c][start + L] - n_prefix[c][start] != 0:
            continue
        window = genome[c][start:start + L].tobytes().decode("ascii")
        if set(window) <= bases:
            ccre_seqs.append(window)
        if len(ccre_seqs) >= N_CCRE:
            break

    all_seqs = rand_seqs + ccre_seqs
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == N_SEQ
    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote {N_SEQ} → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
