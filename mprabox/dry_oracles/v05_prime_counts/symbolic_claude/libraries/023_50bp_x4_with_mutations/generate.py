"""50bp x 4 repeat with 10% mutation rate per copy.
Tests whether exact periodicity matters or just approximate similarity."""
import random, os
random.seed(42)
N, L = 50_000, 200
UNIT = 50
MUT = 0.10
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        seq_parts = [unit]
        for _ in range(L // UNIT - 1):
            mutated = []
            for c in unit:
                if random.random() < MUT:
                    mutated.append(random.choice([x for x in ALPHA if x != c]))
                else:
                    mutated.append(c)
            seq_parts.append("".join(mutated))
        f.write("".join(seq_parts) + "\n")
print(f"Wrote {N} 50bpx4 with 10% mutations")
