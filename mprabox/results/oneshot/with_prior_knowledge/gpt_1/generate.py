#!/usr/bin/env python3
import json
import hashlib
import math
import random
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ucsc_tiles"
OUT = ROOT / "library" / "sequences.txt"
NOTEBOOK = ROOT / "notebook.md"

BASES = "ACGT"
RNG = random.Random(20260527)

CHROM_SIZES = {
    "chr1": 248956422,
    "chr2": 242193529,
    "chr3": 198295559,
    "chr4": 190214555,
    "chr5": 181538259,
    "chr6": 170805979,
    "chr7": 159345973,
    "chr8": 145138636,
    "chr9": 138394717,
    "chr10": 133797422,
    "chr11": 135086622,
    "chr12": 133275309,
    "chr13": 114364328,
    "chr14": 107043718,
    "chr15": 101991189,
    "chr16": 90338345,
    "chr17": 83257441,
    "chr18": 80373285,
    "chr19": 58617616,
    "chr20": 64444167,
    "chr21": 46709983,
    "chr22": 50818468,
    "chrX": 156040895,
}

TARGETS = {
    "PLS": 3500,
    "pELS": 10000,
    "dELS": 22000,
    "CTCF": 5000,
    "H3K4me3": 1500,
}

MOTIFS = [
    "TGACTCA",      # AP-1
    "GGAAGT",       # ETS
    "GGGCGG",       # GC box / SP/KLF
    "CCACC",        # KLF-like
    "CACGTG",       # E-box
    "GATAAG",       # GATA
    "TGACGTCA",     # CRE
    "TGAATCA",      # TEAD-like
    "TGTGGC",       # RUNX-like
    "TTGCGCATGCGCAA",  # CTCF core-like
    "GCCATNTTGG".replace("N", "A"),  # NF-Y-like
    "TAATTA",       # homeobox-like
    "GCGCATGCGC",   # NRF/GC-rich
    "TATAAA",       # TATA
]


def log_note(text):
    with NOTEBOOK.open("a") as handle:
        handle.write("\n" + text.rstrip() + "\n")


def fetch_json(url, cache_path, retries=5):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                text = response.read().decode("utf-8")
            cache_path.write_text(text)
            return json.loads(text)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(1.5 * (attempt + 1))


def ucsc_url(endpoint, **params):
    query = urllib.parse.urlencode(params, safe=":,;")
    return f"https://api.genome.ucsc.edu/getData/{endpoint}?{query}"


def clean(seq):
    seq = seq.upper()
    return seq if len(seq) == 200 and set(seq) <= set(BASES) else None


def revcomp(seq):
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def acceptable(seq):
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    if not 0.22 <= gc <= 0.82:
        return False
    for base in BASES:
        if base * 13 in seq:
            return False
    return True


def label_group(item):
    label = item.get("encodeLabel", "") or item.get("ccre", "")
    ccre = item.get("ccre", "")
    if label == "PLS":
        return "PLS"
    if label == "pELS":
        return "pELS"
    if label == "dELS":
        return "dELS"
    if "CTCF" in label or "CTCF" in ccre:
        return "CTCF"
    if "H3K4me3" in label or "H3K4me3" in ccre:
        return "H3K4me3"
    return "DNase"


def tile_plan(tile_size=1_000_000, desired_tiles=330):
    total = sum(CHROM_SIZES.values())
    plan = []
    phi = 0.6180339887498949
    for chrom, size in CHROM_SIZES.items():
        n = max(3, round(desired_tiles * size / total))
        usable = max(1, size - tile_size - 1)
        for i in range(n):
            frac = (i * phi + 0.137 * (len(chrom) + ord(chrom[-1]))) % 1.0
            start = int(frac * usable)
            start = max(0, min(start, size - tile_size))
            plan.append((chrom, start, start + tile_size))
    RNG.shuffle(plan)
    return plan


def gather_candidates():
    candidates = defaultdict(list)
    seen_coords = set()

    for chrom, start, end in tile_plan():
        key = f"{chrom}_{start}_{end}"
        track_url = ucsc_url(
            "track",
            genome="hg38",
            track="encodeCcreCombined",
            chrom=chrom,
            start=start,
            end=end,
        )
        seq_url = ucsc_url(
            "sequence",
            genome="hg38",
            chrom=chrom,
            start=start,
            end=end,
        )
        track = fetch_json(track_url, DATA / f"{key}.ccre.json")
        sequence = fetch_json(seq_url, DATA / f"{key}.seq.json").get("dna", "").upper()
        if len(sequence) != end - start:
            continue

        for item in track.get("encodeCcreCombined", []):
            cstart = int(item["chromStart"])
            cend = int(item["chromEnd"])
            center = (cstart + cend) // 2
            # Use small deterministic jitter so similar nearby cCREs do not all
            # place the annotation at the exact same 100 bp position.
            seed_material = f"{item.get('name', '')}:{chrom}:{cstart}:{cend}".encode()
            jitter_seed = int(hashlib.sha1(seed_material).hexdigest()[:8], 16)
            jitter = (jitter_seed % 61) - 30
            wstart = center - 100 + jitter
            wend = wstart + 200
            if wstart < start or wend > end:
                continue
            seq = clean(sequence[wstart - start : wend - start])
            if not seq or not acceptable(seq):
                continue
            coord = (chrom, wstart, wend)
            if coord in seen_coords:
                continue
            seen_coords.add(coord)
            group = label_group(item)
            score = float(item.get("score", 0))
            z = float(item.get("zScore", 0))
            candidates[group].append((score, z, seq))

    for group in list(candidates):
        candidates[group].sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidates


def take_balanced(candidates):
    seqs = []
    used = set()
    summary = {}
    for group, target in TARGETS.items():
        pool = candidates.get(group, [])
        # Blend higher-confidence cCREs with broad random coverage from the
        # sampled tiles. Confidence gets priority, but not monopoly.
        top_n = min(len(pool), math.ceil(target * 0.65))
        chosen = [seq for _, _, seq in pool[:top_n]]
        rest = [seq for _, _, seq in pool[top_n:]]
        RNG.shuffle(rest)
        chosen.extend(rest[: max(0, target - len(chosen))])
        for seq in chosen:
            if seq not in used:
                used.add(seq)
                seqs.append(seq)
        summary[group] = len(chosen)
    return seqs, used, summary


def markov_shuffle(seq):
    starts = list(seq[:-1])
    transitions = defaultdict(list)
    for a, b in zip(seq[:-1], seq[1:]):
        transitions[a].append(b)
    for base in BASES:
        RNG.shuffle(transitions[base])

    out = [RNG.choice(starts)]
    for _ in range(199):
        opts = transitions.get(out[-1])
        if opts:
            out.append(opts.pop())
        else:
            out.append(RNG.choice(BASES))
    return "".join(out)


def random_background(gc):
    weights = {
        "A": (1 - gc) / 2,
        "T": (1 - gc) / 2,
        "G": gc / 2,
        "C": gc / 2,
    }
    bases = list(weights)
    cum = []
    running = 0.0
    for base in bases:
        running += weights[base]
        cum.append(running)
    out = []
    for _ in range(200):
        x = RNG.random()
        for base, cutoff in zip(bases, cum):
            if x <= cutoff:
                out.append(base)
                break
    return out


def synth_sequence():
    gc = RNG.choice([0.36, 0.43, 0.50, 0.57, 0.66])
    seq = random_background(gc)
    n_motifs = RNG.choice([1, 2, 2, 3, 4])
    occupied = []
    for _ in range(n_motifs):
        motif = RNG.choice(MOTIFS)
        if RNG.random() < 0.5:
            motif = revcomp(motif)
        for _try in range(50):
            pos = RNG.randrange(10, 190 - len(motif))
            if all(pos + len(motif) < a or pos > b for a, b in occupied):
                seq[pos : pos + len(motif)] = motif
                occupied.append((pos, pos + len(motif)))
                break
    return "".join(seq)


def fill_library(real_seqs, used):
    seqs = list(real_seqs)
    source = list(real_seqs)
    RNG.shuffle(source)

    shuffled_added = 0
    for template in source:
        if shuffled_added >= 4000:
            break
        seq = markov_shuffle(template)
        if clean(seq) and acceptable(seq) and seq not in used:
            used.add(seq)
            seqs.append(seq)
            shuffled_added += 1

    synth_added = 0
    while synth_added < 2500:
        seq = synth_sequence()
        if acceptable(seq) and seq not in used:
            used.add(seq)
            seqs.append(seq)
            synth_added += 1

    random_added = 0
    while len(seqs) < 50000:
        seq = "".join(random_background(RNG.choice([0.33, 0.45, 0.55, 0.68])))
        if acceptable(seq) and seq not in used:
            used.add(seq)
            seqs.append(seq)
            random_added += 1

    return seqs[:50000], {
        "dinuc_markov_shuffled": shuffled_added,
        "motif_synthetic": synth_added,
        "composition_random": random_added,
    }


def validate(seqs):
    assert len(seqs) == 50000, len(seqs)
    assert len(set(seqs)) == 50000, "duplicate sequences"
    for seq in seqs:
        assert len(seq) == 200, len(seq)
        assert set(seq) <= set(BASES), seq


def main():
    candidates = gather_candidates()
    real, used, class_summary = take_balanced(candidates)
    seqs, extra_summary = fill_library(real, used)
    RNG.shuffle(seqs)
    validate(seqs)
    OUT.write_text("\n".join(seqs) + "\n")

    gc_values = [(s.count("G") + s.count("C")) / 200 for s in seqs]
    summary = {
        "n": len(seqs),
        "unique": len(set(seqs)),
        "class_targets": TARGETS,
        "real_selected_by_class": class_summary,
        "extra_components": extra_summary,
        "candidate_counts": {k: len(v) for k, v in candidates.items()},
        "gc_mean": round(sum(gc_values) / len(gc_values), 4),
        "gc_min": round(min(gc_values), 4),
        "gc_max": round(max(gc_values), 4),
    }
    (ROOT / "library" / "design_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    log_note(
        "## Generated library\n"
        f"I generated `library/sequences.txt` with {summary['n']} unique 200 bp sequences. "
        f"Real cCRE selected by class: {class_summary}. Extra components: {extra_summary}. "
        f"GC mean/min/max: {summary['gc_mean']}/{summary['gc_min']}/{summary['gc_max']}. "
        "The final ordering is shuffled so components are not block-structured."
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
