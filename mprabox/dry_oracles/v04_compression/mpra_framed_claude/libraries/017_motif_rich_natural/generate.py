"""Experiment 017: motif-rich natural (PWM-scored window curation).

Substitutes exp 011's 20K random natural with 20K natural windows
selected for highest JASPAR PWM motif content. Other components
unchanged.

Final library: 20K motif-rich natural + 15K cCRE off + 10K DHS + 5K mouse.

Hypothesis: per-sequence motif density is higher (more learning signal
per training step) while preserving natural context. If > 0.508 (>2σ
above plateau), within-class curation works and the plateau is
content-limited. If equal, random natural already provides enough motif
coverage.

Implementation: parse a small curated set of ~20 diverse JASPAR PWMs,
convert to log-odds (pseudocount 1, uniform background), score each
candidate window by sum of per-PWM max scores (forward+RC), pick top N.

Candidate pool: 100K random natural windows.
"""
import gzip
import os
import re

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CCRE = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_CCRE - N_DHS
L = 200
SEED = 0
N_CANDIDATES = 100_000

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")
JASPAR = os.path.join(REPO_ROOT, "data", "jaspar2024_core.jaspar")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HUMAN_SET = set(HUMAN_CHROMS)
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}

# Hand-curated set of diverse, well-known TF PWMs (JASPAR IDs).
CURATED_IDS = {
    "MA0139.1",  # CTCF
    "MA0079.5",  # SP1 (extended) — match prefix MA0079
    "MA0036.4",  # GATA2
    "MA0099.3",  # FOS::JUN (AP-1)
    "MA0083.3",  # SRF
    "MA0080.5",  # SPI1
    "MA0102.4",  # CEBPA
    "MA0148.4",  # FOXA1
    "MA0144.2",  # STAT3
    "MA0258.2",  # ESR2
    "MA0093.3",  # USF1
    "MA0506.1",  # NRF1
    "MA0259.1",  # ARNT::HIF1A
    "MA0035.4",  # GATA1
    "MA0014.3",  # PAX5
    "MA0152.1",  # NFATC2
    "MA0498.2",  # MEIS1
    "MA0498.3",
    "MA0140.2",  # GATA1::TAL1
    "MA0019.1",  # DDIT3::CEBPA
}
PWM_PREFIX_MATCH = {x.rsplit(".", 1)[0] for x in CURATED_IDS}

BASE_TO_IDX = {"A": 0, "C": 1, "G": 2, "T": 3}


def parse_jaspar():
    """Yield (id, name, count_matrix [4×W])."""
    pwms = []
    with open(JASPAR) as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(">"):
            header = line[1:].split("\t")
            mid = header[0]
            name = header[1] if len(header) > 1 else ""
            mat = np.zeros((4, 0), dtype=np.float64)
            rows = []
            for j in range(4):
                row_line = lines[i + 1 + j]
                nums = re.findall(r"-?\d+\.?\d*", row_line)
                rows.append([float(x) for x in nums])
            W = len(rows[0])
            mat = np.array(rows, dtype=np.float64)
            pwms.append((mid, name, mat))
            i += 5
        else:
            i += 1
    return pwms


def counts_to_logodds(mat, pseudocount=1.0):
    """Convert 4×W count matrix to log2-odds vs uniform background."""
    total = mat.sum(axis=0, keepdims=True) + 4 * pseudocount
    freqs = (mat + pseudocount) / total
    bg = 0.25
    return np.log2(freqs / bg)


def reverse_complement_pwm(lo):
    """Reverse columns and swap rows (A↔T, C↔G)."""
    return lo[[3, 2, 1, 0], ::-1]


def encode_seqs(seqs):
    """Encode list of L-length strings to N×4×L array (no N expected)."""
    N = len(seqs)
    arr = np.zeros((N, 4, len(seqs[0])), dtype=np.float32)
    for n, s in enumerate(seqs):
        for i, b in enumerate(s):
            arr[n, BASE_TO_IDX[b], i] = 1.0
    return arr


def conv1d_max(seqs_arr, lo):
    """For each sequence in seqs_arr (N×4×L), compute max sliding score
    using log-odds matrix lo (4×W). Returns N array of max scores."""
    N, _, Lseq = seqs_arr.shape
    W = lo.shape[1]
    lo_f = lo.astype(np.float32)
    scores = np.zeros((N, Lseq - W + 1), dtype=np.float32)
    for w in range(W):
        # seqs_arr[:, :, w:Lseq-W+1+w] is N×4×(L-W+1); lo_f[:, w] is 4
        scores += np.einsum("nca,c->na", seqs_arr[:, :, w:Lseq - W + 1 + w], lo_f[:, w])
    return scores.max(axis=1)


def score_seqs(seqs, pwms_lo):
    """Return per-sequence total motif score (sum over PWMs of max(fwd, rc))."""
    arr = encode_seqs(seqs)
    total = np.zeros(len(seqs), dtype=np.float32)
    for lo in pwms_lo:
        s_fwd = conv1d_max(arr, lo)
        s_rc = conv1d_max(arr, reverse_complement_pwm(lo))
        total += np.maximum(s_fwd, s_rc)
    return total


def sample_natural_pool(fa, chroms, n, rng):
    chrom_lens = {c: len(fa[c]) for c in chroms}
    arr = np.array(chroms)
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(arr, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def sample_natural(fa, chroms, n, rng):
    return sample_natural_pool(fa, chroms, n, rng)


def sample_offcenter_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET or parts[9] not in HIGH_CONF:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((parts[0], mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        offset = int(rng.integers(25, 176))
        start = mid - offset
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def sample_dhs(fa, n, rng):
    summits = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET:
                continue
            summits.append((parts[0], int(parts[6])))
    idx = rng.permutation(len(summits))
    out = []
    for i in idx:
        chrom, mid = summits[i]
        start = mid - L // 2
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def main():
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)

    # Parse PWMs, keep curated ones
    all_pwms = parse_jaspar()
    print(f"Total JASPAR PWMs: {len(all_pwms)}")
    kept = []
    for mid, name, mat in all_pwms:
        prefix = mid.rsplit(".", 1)[0]
        if mid in CURATED_IDS or prefix in PWM_PREFIX_MATCH:
            kept.append((mid, name, mat))
    print(f"Curated PWMs matched: {len(kept)} ({[m[0] for m in kept]})")
    pwms_lo = [counts_to_logodds(mat) for _, _, mat in kept]

    # Candidate pool of natural windows
    print(f"Sampling {N_CANDIDATES} candidate natural windows...")
    candidates = sample_natural_pool(hg, HUMAN_CHROMS, N_CANDIDATES, rng)

    # Score candidates in batches
    print("Scoring candidates...")
    batch = 5000
    scores = np.empty(len(candidates), dtype=np.float32)
    for i in range(0, len(candidates), batch):
        scores[i:i + batch] = score_seqs(candidates[i:i + batch], pwms_lo)

    # Pick top N_NATURAL
    top_idx = np.argsort(-scores)[:N_NATURAL]
    natural = [candidates[i] for i in top_idx]
    print(f"Top-scored natural: score range [{scores[top_idx].min():.2f}, "
          f"{scores[top_idx].max():.2f}], median {np.median(scores[top_idx]):.2f}")
    print(f"All candidates: score range [{scores.min():.2f}, {scores.max():.2f}], "
          f"median {np.median(scores):.2f}")

    ccre = sample_offcenter_ccre(hg, N_CCRE, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + ccre + dhs + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} ccre={len(ccre)} dhs={len(dhs)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
