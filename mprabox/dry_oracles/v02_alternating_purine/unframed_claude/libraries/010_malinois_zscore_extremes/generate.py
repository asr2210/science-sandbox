"""Z-score-style extremes for max signal/noise.

Per cell line, rank sequences by |log2FC| / lfcSE (Z-magnitude).
Pick top ~8334 per cell line, dedup, top up to 50k randomly.

Goal: bias toward high-confidence active sequences. Should give
cleaner training signal for the oracle.
"""
import os, random

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
random.seed(10)
each = 16670  # per cell line top by |z|, ~50k after dedup hopefully

records = []  # (k_lfc, k_se, h_lfc, h_se, sn_lfc, sn_se, seq)
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12:
            continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s):
            continue
        try:
            k_l = float(cols[5]); h_l = float(cols[6]); sn_l = float(cols[7])
            k_s = float(cols[8]); h_s = float(cols[9]); sn_s = float(cols[10])
        except ValueError:
            continue
        if k_s <= 0 or h_s <= 0 or sn_s <= 0:
            continue
        records.append((k_l, k_s, h_l, h_s, sn_l, sn_s, s))

print(f"Got {len(records)} records")

def zmag(lfc, se): return abs(lfc) / max(se, 1e-6)

chosen = set()
for i_lfc, i_se, name in [(0,1,"K562"), (2,3,"HepG2"), (4,5,"SKNSH")]:
    ranked = sorted(records, key=lambda r: -zmag(r[i_lfc], r[i_se]))
    for r in ranked[:each]:
        chosen.add(r[6])
print(f"After dedup: {len(chosen)}")

if len(chosen) < N_SEQS:
    pool = [r[6] for r in records if r[6] not in chosen]
    random.shuffle(pool)
    chosen.update(pool[:N_SEQS - len(chosen)])
elif len(chosen) > N_SEQS:
    chosen = set(list(chosen)[:N_SEQS])

chosen_list = list(chosen)
random.shuffle(chosen_list)
chosen_list = chosen_list[:N_SEQS]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen_list:
        f.write(s + "\n")
print(f"Wrote {len(chosen_list)}")
