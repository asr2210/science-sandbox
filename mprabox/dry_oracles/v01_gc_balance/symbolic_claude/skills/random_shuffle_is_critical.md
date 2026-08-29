# Random shuffle within each row is critical

## Discovery (exp 012)
Imposing structured intra-row arrangement (sorting + cyclic shift) DESTROYS
the score. Composition gradient that was giving eval_01 = 0.601 dropped to
-0.019 when chars were sorted into clusters within each row.

## Why
The eval is highly position-sensitive. When all rows have RANDOM chars at
each position, per-position distribution across the library is what the
model expects. When clustered, certain positions have biased content that
the model interprets differently.

## Rule
After deciding per-row composition counts, **always perform a uniform random
shuffle within each row**. Don't try to add intra-row structure (sorting,
periodicity, etc.) unless you have a very specific reason and have tested
it carefully on a small scale.

## Caveat
Inserting specific MOTIFS at random positions (preserving random-uniform
per-position distribution overall) MIGHT work — that's different from
clustering existing chars.
