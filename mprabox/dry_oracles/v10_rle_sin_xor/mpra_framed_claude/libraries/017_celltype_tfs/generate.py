"""Experiment 017: 1 cell-type-specific TF motif at fixed center.

Filter JASPAR for TFs known to be active in K562 (erythroid leukemia),
HepG2 (hepatocyte), or SK-N-SH (neural). Insert one of these motifs
at fixed center of random uniform background.

Hypothesis: targeted TF coverage helps the model learn cell-type-specific
features. If the eval is sensitive to specific TF binding sites, this should
boost HepG2 and SK-N-SH.
"""
from pathlib import Path
import numpy as np
import re

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
JASPAR = REPO / "data" / "jaspar2024_vert.meme"

# K562 (erythroid): GATA1/2, TAL1, KLF1, MYB, RUNX1, FLI1, NFE2, GFI1B
# HepG2 (hepatocyte): HNF1A, HNF1B, HNF4A, FOXA1, FOXA2, CEBPA, CEBPB, NR1H4, RXRA, PPARG
# SK-N-SH (neural): NEUROD1, NEUROD2, ASCL1, POU3F2, POU3F3, MEF2C, MEF2D, FOXP2, REST, OLIG2, SOX2, NKX2-2
TARGET_TFS = {
    "GATA1", "GATA2", "TAL1", "KLF1", "MYB", "RUNX1", "FLI1", "NFE2", "GFI1B",
    "HNF1A", "HNF1B", "HNF4A", "FOXA1", "FOXA2", "CEBPA", "CEBPB",
    "NR1H4", "RXRA", "PPARG", "PPARA",
    "NEUROD1", "NEUROD2", "ASCL1", "POU3F2", "POU3F3",
    "MEF2C", "MEF2D", "FOXP2", "REST", "OLIG2", "SOX2", "NKX2-2",
}


def parse_meme_named(path: Path) -> list[tuple[str, str]]:
    """Return list of (TF name, consensus) tuples."""
    text = path.read_text()
    blocks = re.split(r"\nMOTIF ", text)
    out = []
    alphabet = "ACGT"
    for b in blocks[1:]:
        header = b.split("\n", 1)[0]
        parts = header.split()
        name = parts[1] if len(parts) > 1 else parts[0]
        # find letter-probability matrix
        m = re.search(r"letter-probability matrix:.*", b)
        if not m:
            continue
        rest = b[m.end():]
        rows = []
        for line in rest.splitlines():
            line = line.strip()
            if not line or line.startswith("URL"):
                if rows:
                    break
                continue
            try:
                vals = [float(x) for x in line.split()]
            except ValueError:
                if rows:
                    break
                continue
            if len(vals) == 4:
                rows.append(vals)
        if rows:
            arr = np.array(rows)
            consensus = "".join(alphabet[i] for i in arr.argmax(axis=1))
            out.append((name, consensus))
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet_arr = np.array(list("ACGT"))

    named = parse_meme_named(JASPAR)
    print(f"loaded {len(named)} motifs total")
    # match by TF name
    filtered = [
        (n, c)
        for n, c in named
        if any(t == n.upper() or t in n.upper() for t in TARGET_TFS)
        and 6 <= len(c) <= 20
    ]
    print(f"filtered to {len(filtered)} cell-type-relevant motifs")
    print("examples:", [f"{n}({c})" for n, c in filtered[:10]])
    if len(filtered) < 5:
        raise RuntimeError("not enough motifs matched")

    motifs = [c for _, c in filtered]

    bg_idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    seqs_arr = alphabet_arr[bg_idx]

    motif_choices = rng.integers(0, len(motifs), size=N_SEQS)
    for i in range(N_SEQS):
        m = motifs[motif_choices[i]]
        L = len(m)
        start = (SEQ_LEN - L) // 2
        for j, c in enumerate(m):
            seqs_arr[i, start + j] = c

    seqs = ["".join(row) for row in seqs_arr]

    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
