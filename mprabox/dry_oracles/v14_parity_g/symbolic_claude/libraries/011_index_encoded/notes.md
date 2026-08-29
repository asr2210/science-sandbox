# 011 Index encoding (first 9 chars = base-4 of i)

eval_01 = -0.0034 (WORSE). But:
- eval_07 = +0.0078 (BIG, a=0.0053, b=0.0122, c=0.0058)
- eval_13 = +0.0068 (a=0.0044, b=0.0120, c=0.0041)

So index encoding helps eval_07 and eval_13 specifically. Maybe these evals
reward sequences with high mutual info between content and order.

Not the way for eval_01. Going back to HEAVY=0.7-0.85 bucket approach.
