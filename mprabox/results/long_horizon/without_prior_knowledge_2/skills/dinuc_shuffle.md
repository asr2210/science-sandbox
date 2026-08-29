# Skill: dinucleotide-preserving sequence shuffle

When you need to control for compositional/dinucleotide bias while
destroying motifs (the classic motif-vs-composition test).

## Algorithm
Hierholzer's randomized Eulerian-walk on the de Bruijn dinucleotide graph:

```python
from collections import defaultdict
def dinuc_shuffle(seq, rng):
    n = len(seq)
    if n < 2: return seq
    adj = defaultdict(list)
    for i in range(n - 1):
        adj[seq[i]].append(seq[i+1])
    for u in adj:
        rng.shuffle(adj[u])           # randomize edge order
    stack, path = [seq[0]], []
    while stack:
        u = stack[-1]
        if adj[u]:
            stack.append(adj[u].pop())
        else:
            path.append(stack.pop())
    path.reverse()
    return ''.join(path)
```

## Properties
- **Exact** dinucleotide and mononucleotide preservation (every edge
  used exactly once).
- Same start and end character as input.
- Same length as input.
- NOT uniform over all valid Eulerian paths (use Altschul-Erickson with
  random arborescence for that), but close enough for biological
  shuffling controls.
- Fast: O(n) per sequence.

## When to use
- Motif-vs-composition mechanism tests
- Background null models for motif enrichment
- Negative controls when training models on regulatory sequences

## Empirical finding (003)
On 50K x 200bp cCRE-derived sequences, dinuc shuffling DROPPED the
sequence-to-activity model's eval performance below uniform random
(mean 0.660 vs 0.732). Take-home: **natural compositional bias is
actively harmful for ML generalization without motifs**, because it
narrows coverage without providing compensating signal. Real motifs
in 002 were doing all the work of cCRE's gain over random.

## Use rng with numpy
`rng.shuffle()` works on lists in-place. Seed deterministically per
sequence with `np.random.default_rng(int(seed * 10**9 + idx))`.
