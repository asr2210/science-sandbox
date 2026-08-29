"""Single-character library: 12500 rows of each char 0/1/2/3."""
N_per = 12500
L = 200

with open("libraries/002_single_char/sequences_0.txt", "w") as f:
    for c in "0123":
        line = c * L + "\n"
        for _ in range(N_per):
            f.write(line)
