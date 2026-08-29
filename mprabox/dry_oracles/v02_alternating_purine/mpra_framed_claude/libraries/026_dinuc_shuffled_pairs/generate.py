"""
Experiment 026 — per-positive dinucleotide-shuffled negatives.

013 ratio positives, but each positive paired with a dinucleotide-
shuffled version of ITSELF as the negative. This removes ALL spatial
structure (position-specific motifs, motif spacing, motif co-occurrence)
while preserving local di-nucleotide composition exactly.

Composition (50K total):
- 15K uniform + 5K CTCF + 5K DNH3 = 25K positives
- 25K dinucleotide-shuffled negatives (one per positive)

Hypothesis: if the model relies primarily on position-specific motif
arrangement (TF binding sites in specific configurations), per-positive
shuffled negatives create the HARDEST possible contrast and the model
should learn very strongly. If the model relies on composition alone
(k-mer frequency), shuffled negatives are too easy.

Predicted:
- best case: 0.175+ (clean per-positive contrast lifts motif evals)
- worst case: 0.13-0.14 (negatives too similar to positives, model
  can't generalize to true random/flank evals)
"""
import os, time, numpy as np

L = 200
HALF = L // 2
SEED = 0

def classify_rare(type_str):
    parts = set(t.strip() for t in type_str.split(","))
    if "DNase-H3K4me3" in parts: return "DNH3"
    if "CTCF-only" in parts: return "CTCF"
    return None

def dinuc_shuffle(seq, rng):
    """Dinucleotide shuffle via Eulerian random walk."""
    n = len(seq)
    if n < 2: return seq
    # build adjacency: dinuc seq[i]seq[i+1] for i in [0,n-1)
    nt = seq
    succ = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        succ[nt[i]].append(nt[i + 1])
    start = nt[0]
    end_nuc = nt[-1]
    # Shuffle each successor list
    for b in succ:
        rng.shuffle(succ[b])
    # Find last-edge per node going to end (per Altschul-Erickson):
    # ensure spanning arborescence to end_nuc — simpler practical method:
    # try multiple shuffles and accept first that walks full length.
    for _ in range(20):
        succ_copy = {b: list(lst) for b, lst in succ.items()}
        for b in succ_copy:
            rng.shuffle(succ_copy[b])
        out = [start]
        cur = start
        ok = True
        for _ in range(n - 1):
            if not succ_copy[cur]:
                ok = False
                break
            nxt = succ_copy[cur].pop()
            out.append(nxt)
            cur = nxt
        if ok and len(out) == n:
            return "".join(out)
    # Fallback: mono-nucleotide shuffle
    arr = list(seq)
    rng.shuffle(arr)
    return "".join(arr)

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    genome, n_prefix = {}, {}
    for f in sorted(os.listdir(cache_dir)):
        if f.endswith(".npy"):
            c = f[:-4]
            mat = np.asarray(np.load(os.path.join(cache_dir, f), mmap_mode="r"))
            genome[c] = mat
            is_n = (mat == ord("N")).astype(np.int32)
            n_prefix[c] = np.concatenate(([0], np.cumsum(is_n)))
    chroms = sorted(genome.keys())
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")
    rng = np.random.default_rng(SEED)
    # Use a deterministic-ish python random for shuffle to use list.shuffle
    import random
    pyrng = random.Random(SEED)

    all_mids, ctcf_mids, dnh3_mids = [], [], []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome: continue
            s, e = int(parts[1]), int(parts[2])
            mid = (s + e) // 2
            all_mids.append((c, mid))
            bk = classify_rare(parts[5])
            if bk == "CTCF": ctcf_mids.append((c, mid))
            elif bk == "DNH3": dnh3_mids.append((c, mid))

    def sample_positives(items, n_need, label):
        order = rng.permutation(len(items))
        out = []
        for j in order:
            c, mid = items[j]
            s = mid - HALF
            if s < 0 or s + L > len(genome[c]): continue
            if n_prefix[c][s + L] - n_prefix[c][s] != 0: continue
            w = genome[c][s:s + L].tobytes().decode("ascii")
            if set(w) <= bases:
                out.append(w)
            if len(out) >= n_need: break
        print(f"  {label}: {len(out)}")
        return out

    positives = []
    positives += sample_positives(all_mids, 15_000, "uniform")
    positives += sample_positives(ctcf_mids, 5_000, "CTCF")
    positives += sample_positives(dnh3_mids, 5_000, "DNH3")
    assert len(positives) == 25_000

    print(f"shuffling {len(positives)} negatives...")
    negatives = [dinuc_shuffle(p, pyrng) for p in positives]
    assert all(len(n) == L for n in negatives)
    assert all(set(n) <= bases for n in negatives)

    all_seqs = positives + negatives
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == 50_000

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote 50000 → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
