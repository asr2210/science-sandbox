# 008 — Random background + 25bp real-CRE fragment embedded

**Design.** 50K random 200bp; each sequence gets one 25bp fragment from a random ENCODE cCRE (mixed dELS/pELS/PLS/TF) embedded at a random position. Background is uniform random for 175/200 bases per sequence. Avg library GC = 0.498 (essentially unchanged from random's 0.500).

**Result.** eval_01 = **0.4174** (Δ-0.0018 vs random). K562 = 0.582 (Δ-0.008), HepG2 = 0.610 (Δ-0.013), SK-N-SH = 0.060 (Δ+0.015).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| **008 random + 25bp bio** | **0.582** | **0.610** | **0.060** | **0.4174** |

**Interpretation — much closer to random than any other intervention.** Embedding bio fragments WITHIN sequences (vs mixing whole CREs) is far gentler. K562/HepG2 only dropped ~1.5%, and SK-N-SH lifted +33% relative.

But still net negative — random remains the leader. The lift on SK-N-SH is smaller than the loss on K562/HepG2 in absolute mean_r terms.

**Theory v8.** The "right mechanism" for adding biology is WITHIN-SEQUENCE embedding, not BETWEEN-SEQUENCE mixing. The model can isolate the bio-fragment as a local signal while still benefiting from the broader random background.

Open question: is there a sweet spot fragment length / count / element-type that BEATS random?

**Next.** Test 1x15bp fragment (vs 25bp) per sequence. Smaller insertion should preserve K562/HepG2 better. If SK-N-SH still lifts at 15bp, smaller is better. If not, the SK-N-SH lift requires the larger 25bp+ context, and there's no free lunch.
