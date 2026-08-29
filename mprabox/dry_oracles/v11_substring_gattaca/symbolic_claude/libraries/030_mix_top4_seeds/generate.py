"""Final: 4-way mix of top seed libraries (12.5k each).

Top seeds for [43,57] uniform-tuples + shuffle, in descending eval_01:
  seed=42 (009): 0.8820
  seed=1  (022): 0.8815
  seed=100(023): 0.8803
  seed=2024(021):0.8782

029 (2-way mix) reached 0.8821, essentially tied with 009.
Hypothesis: averaging the top 4 retains the high score and may smooth
condition-level noise further.
"""
import os

base = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

sources = [
    "009_wider_constrained",
    "022_asymmetric_42_57",
    "023_asymmetric_43_58",
    "021_seed2024",
]
PER = 12500

with open(OUT, "w") as f_out:
    for src in sources:
        path = os.path.join(base, src, "sequences_0.txt")
        with open(path) as f_in:
            for i, line in enumerate(f_in):
                if i >= PER:
                    break
                f_out.write(line)

print(f"wrote 50000 sequences (12.5k each from top-4 seeds)")
