"""Cryptographic random via secrets module."""
import os, secrets
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write("".join(str(secrets.randbelow(4)) for _ in range(200)) + "\n")
print("done secrets cryptographic random")
