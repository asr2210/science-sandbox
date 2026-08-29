"""
hp_fold.py — The fixed physics of the sandbox.

A residue chain is a string over {H, P}. It folds as a self-avoiding walk
(SAW) on the 2D square lattice. The energy of a fold is minus the number of
non-consecutive H-H contacts (pairs of H residues on adjacent lattice sites
that are not adjacent in the chain). A chain's fitness is the energy of its
OPTIMAL fold, found by exhaustive enumeration of all SAWs.

This module is world-independent. It never sees a genetic code. It only ever
sees H/P strings. Everything here is exact: no heuristics, no approximation.

Symmetry normalization (standard in the HP-folding literature): the first
step is fixed to a single direction and the first turn is constrained to one
handedness. This removes the 8-fold rotation/reflection redundancy so each
distinct fold is counted once.

Performance note: SAW count grows ~2.6^N. Exact folding is intended for
N up to ~20-25. Walks for a given N are generated once and cached.
"""

from functools import lru_cache
from typing import List, Tuple

# Moves on the square lattice. Order matters only for determinism.
# 0:+x (right), 1:-x (left), 2:+y (up), 3:-y (down)
_DELTAS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _generate_saws(n: int) -> List[Tuple[Tuple[int, int], ...]]:
    """
    Enumerate all self-avoiding walks of n points on the 2D square lattice,
    up to rotation and reflection.

    Normalization to kill the 8 symmetries of the square:
      - First point at origin (0,0).
      - Second point fixed to (1,0): removes the 4 rotations.
      - First turn (the first move that is not straight ahead) must go to
        +y, never -y: removes the remaining reflection.

    Returns a list of coordinate tuples, each of length n.
    """
    if n <= 0:
        return []
    if n == 1:
        return [((0, 0),)]

    results: List[Tuple[Tuple[int, int], ...]] = []
    # Fixed first two points.
    start = [(0, 0), (1, 0)]
    occupied = {(0, 0), (1, 0)}
    # reflection_fixed becomes True once we've seen the first turn and thereby
    # locked the handedness. Until then, a -y turn is disallowed.
    _extend(start, occupied, n, results, reflection_fixed=False)
    return results


def _extend(path, occupied, n, results, reflection_fixed):
    if len(path) == n:
        results.append(tuple(path))
        return
    cx, cy = path[-1]
    px, py = path[-2]
    # Current heading (last move direction).
    hx, hy = cx - px, cy - py
    for dx, dy in _DELTAS:
        # No immediate backtrack (would overlap previous point anyway, but skip early).
        if (dx, dy) == (-hx, -hy):
            continue
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in occupied:
            continue
        is_straight = (dx, dy) == (hx, hy)
        new_reflection_fixed = reflection_fixed
        if not reflection_fixed and not is_straight:
            # This is the first turn. Allow only the +y-ish handedness.
            # The first turn is relative to heading (1,0) initially, but after
            # straight moves the heading is still (1,0) until a turn happens,
            # so the first turn is always from heading (1,0): turns are to
            # (0,1) [up] or (0,-1) [down]. Permit only up.
            if (dx, dy) == (0, -1):
                continue
            new_reflection_fixed = True
        occupied.add((nx, ny))
        path.append((nx, ny))
        _extend(path, occupied, n, results, new_reflection_fixed)
        path.pop()
        occupied.remove((nx, ny))


@lru_cache(maxsize=None)
def _saws_cached(n: int):
    return _generate_saws(n)


def _fold_energy(seq: str, coords: Tuple[Tuple[int, int], ...]) -> int:
    """
    Energy of one specific fold: minus the number of non-consecutive H-H
    contacts. coords[i] is the lattice position of residue i.
    """
    n = len(seq)
    # Map position -> residue index for O(1) neighbor lookup.
    pos_to_idx = {coords[i]: i for i in range(n)}
    contacts = 0
    for i in range(n):
        if seq[i] != 'H':
            continue
        xi, yi = coords[i]
        for dx, dy in _DELTAS:
            j = pos_to_idx.get((xi + dx, yi + dy))
            if j is None:
                continue
            if j <= i:
                continue  # count each pair once
            if j == i + 1:
                continue  # consecutive in chain: not a contact
            if seq[j] == 'H':
                contacts += 1
    return -contacts


def best_energy(seq: str) -> int:
    """
    The fitness of a residue chain: the energy of its optimal fold.
    Lower (more negative) is better. Exact, by exhaustive enumeration.
    """
    n = len(seq)
    if n < 2:
        return 0
    best = 0  # an all-extended chain has 0 contacts; energy can't be positive
    for coords in _saws_cached(n):
        e = _fold_energy(seq, coords)
        if e < best:
            best = e
    return best


def best_energy_and_degeneracy(seq: str) -> Tuple[int, int]:
    """
    Returns (optimal energy, number of distinct optimal folds).
    Degeneracy of 1 means the ground state is unique (a 'designing' sequence
    in the Li-Tang sense). Used for designability analysis.
    """
    n = len(seq)
    if n < 2:
        return 0, 1
    best = 0
    count = 1
    for coords in _saws_cached(n):
        e = _fold_energy(seq, coords)
        if e < best:
            best = e
            count = 1
        elif e == best:
            count += 1
    return best, count


def saw_count(n: int) -> int:
    """Number of symmetry-reduced SAWs of length n. For sizing/timing."""
    return len(_saws_cached(n))
