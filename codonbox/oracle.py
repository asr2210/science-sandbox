"""
oracle.py — The sealed oracle the agent queries. PURELY QUANTITATIVE.

The agent never sees inside this. It submits a DNA string; the oracle returns
ONLY {ok, fitness, query_index}. Whether the agent understood the organism's
biology is judged post hoc by a human reading notebook.md against the known
ground truth (world.code_summary) — there is no automated qualitative grader.

COLD START: the oracle reveals no structure through errors. ANY string is
accepted and returns a fitness. It returns 0 unless the string is composed
entirely of the organism's alphabet AND cleanly encodes a product of exactly
the right length under the hidden codon size. Only then does a real fitness
appear. The agent must infer the alphabet, the codon size, and the product
length from WHERE nonzero fitness emerges — never from a message.

Every query is logged with the returned fitness AND, in a hidden channel the
agent never sees, the true residues / energy / degeneracy, so the human reading
the notebook afterward has the true trajectory to compare against.
"""

import json
import os
import struct
import subprocess
import time
from typing import Optional

from world import World


class FoldTable:
    """Loads the enumerated N-residue fitness/degeneracy table.
    Entry format (hpfold.c 'enumerate'): int8 energy + uint32 degeneracy,
    indexed by residue H-bitmask 0..2^N-1."""

    ENTRY = struct.Struct("<bI")

    def __init__(self, path: str, n_residues: int):
        self.n = n_residues
        self.energy = None
        self.degen = None
        if path and os.path.isfile(path) and os.path.getsize(path) > 0:
            self._load(path)

    def _load(self, path: str):
        total = 1 << self.n
        if os.path.getsize(path) != total * self.ENTRY.size:
            return  # incomplete -> unavailable, fall back to on-demand
        with open(path, "rb") as f:
            data = f.read()
        energy = bytearray(total)
        degen = [0] * total
        for m in range(total):
            e, d = self.ENTRY.unpack_from(data, m * self.ENTRY.size)
            energy[m] = e & 0xFF
            degen[m] = d
        self.energy = energy
        self.degen = degen

    @property
    def loaded(self) -> bool:
        return self.energy is not None

    @staticmethod
    def _signed(b):
        return b - 256 if b >= 128 else b

    def lookup(self, hmask: int):
        return self._signed(self.energy[hmask]), self.degen[hmask]

    def true_optimum(self):
        """Best (most negative) energy over all residue chains -> the
        performance ceiling for grading. Returns (best_energy, best_fitness)."""
        best = min(self._signed(self.energy[m]) for m in range(1 << self.n))
        return best, -best


def residue_to_hmask(residues: str) -> int:
    m = 0
    for i, r in enumerate(residues):
        if r == 'H':
            m |= (1 << i)
    return m


class Oracle:
    def __init__(
        self,
        world: World,
        n_residues: int,
        table_path: Optional[str] = None,
        contacts_path: Optional[str] = None,
        folder_bin: str = "./hpfold",
        log_path: Optional[str] = None,
        resume: bool = False,
    ):
        self.world = world
        self.n_residues = n_residues
        self.table = FoldTable(table_path, n_residues) if table_path else None
        self.contacts_path = contacts_path
        self.folder_bin = folder_bin
        self.log_path = log_path
        self.n_queries = 0
        self.best_fitness = None
        self.best_dna = None
        # Only truncate the queries log on a fresh start; on resume the prior
        # rows are authoritative and must be kept.
        if self.log_path and not resume:
            open(self.log_path, "w").close()

    def _fold_on_demand(self, residues: str):
        r = subprocess.run(
            [self.folder_bin, "score", self.contacts_path, residues],
            capture_output=True, text=True,
        )
        e, d = r.stdout.strip().split()
        return int(e), int(d)

    def _try_translate(self, dna: str):
        """Residue chain iff the string is all-alphabet and encodes exactly
        n_residues residues under the world's codon size; else None (scored 0,
        silently). No error is ever surfaced."""
        if not dna:
            return None
        if set(dna) - set(self.world.alphabet):
            return None
        L = self.world.codon_length
        if len(dna) % L != 0:
            return None
        if len(dna) // L != self.n_residues:
            return None
        return self.world.translate(dna)

    def query(self, dna: str) -> dict:
        """The agent's single action. Cold start: structure never leaks via
        errors; non-conforming input simply scores 0."""
        self.n_queries += 1
        residues = self._try_translate(dna)
        if residues is None:
            res = {"ok": True, "fitness": 0, "query_index": self.n_queries}
            self._log(dna, res, residues=None, energy=0, degeneracy=None)
            return res

        hmask = residue_to_hmask(residues)
        if self.table and self.table.loaded:
            energy, degen = self.table.lookup(hmask)
        else:
            energy, degen = self._fold_on_demand(residues)

        fitness = -energy
        if self.best_fitness is None or fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_dna = dna

        res = {"ok": True, "fitness": fitness, "query_index": self.n_queries}
        self._log(dna, res, residues=residues, energy=energy, degeneracy=degen)
        return res

    def _log(self, dna, result, residues=None, energy=None, degeneracy=None):
        if not self.log_path:
            return
        entry = {
            "t": round(time.time(), 3),
            "query_index": result.get("query_index"),
            "dna": dna,
            "returned": {k: v for k, v in result.items() if k != "query_index"},
            "_hidden": {"residues": residues, "energy": energy,
                        "degeneracy": degeneracy},
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
