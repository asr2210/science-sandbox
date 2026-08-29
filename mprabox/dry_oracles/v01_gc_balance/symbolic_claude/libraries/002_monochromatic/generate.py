"""
Experiment 002: Monochromatic composition probe.

Four sub-libraries of 12,500 identical strings each:
  - "0"*200
  - "1"*200
  - "2"*200
  - "3"*200
Total 50,000. mean_r reveals whether composition extremes are favored
or penalized vs the uniform random baseline.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
L = 200
PER = 12_500

with open(OUT, "w") as f:
    for ch in "0123":
        line = ch * L + "\n"
        for _ in range(PER):
            f.write(line)

print(f"Wrote {4*PER} sequences of length {L} to {OUT}")
