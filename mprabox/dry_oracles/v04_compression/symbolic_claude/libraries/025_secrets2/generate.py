"""Cryptographic secrets v2. Different entropy snapshot."""
import os, secrets
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    for _ in range(50000):
        f.write("".join(str(secrets.randbelow(4)) for _ in range(200)) + "\n")
print("done")
