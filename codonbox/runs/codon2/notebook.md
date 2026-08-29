
## 2026-06-28 15:06 — query 0

Initial assumptions: 32-char sequences over {A,B,C,D}. Unknown scoring function. Higher = better.

Plan:
1. Test homogeneous sequences (all A, all B, all C, all D) to see if any single character dominates.
2. Test simple alternating patterns to detect positional/pairing effects.
3. Test random sequences to gauge typical scores.
4. From there, build hypotheses about composition, position, motifs, or interactions.

First experiment: all-A sequence as baseline.

## 2026-06-28 15:06 — query 4

Results: A=0, B=9, C=9, D=0. B and C give 9, A and D give 0.
Hypotheses:
- Each B or C contributes ~0.28 each? 32*0.28=9. Or maybe count adjacent B-B pairs (31 of them) = 9 seems off.
- Maybe count B's only above threshold? 32 B's → 9; perhaps log or sqrt? sqrt(32)≈5.6, log2(32)=5. Neither matches 9.
- Maybe count number of distinct runs or some motif count.
- Could be number of specific motifs. With 32 of same char, count of "BB" overlapping pairs = 31. count of "BBB"=30. None equals 9.
- Maybe positional: certain positions favor B/C; 9 of 32 positions reward.

Next: test alternating BC to see if mixing B and C is better or worse than pure.

## 2026-06-28 15:06 — query 6

BCBC...=9, BABA...=0. Surprising: pure B = 9, but BA alternating = 0. So A actively disrupts.
Maybe scoring uses pairs/motifs and any A or D breaks it.
- Pure B: 9. Pure C: 9. BCBC: 9. So B and C are interchangeable in terms of scoring.
- BABA: 0 → A kills it.
Try: many B's with one A, or partial substitution to see if A is destructive or just neutral.

## 2026-06-28 15:07 — query 10

Key data:
- 32 B's = 9
- 31 B's + 1 A = 9 (one A doesn't hurt)
- 31 B's + 1 D = 9 
- 32 A's = 0
- 31 A's + 1 B = 0 (one B doesn't help)
- 16 B's + 16 A's = 3

So scoring is non-linear. Could be counting maximal runs of B/C.
- 32 B's: one run of 32 → 9
- 16B+16A: one run of 16 → 3
- BBBB...AB...: run of 16, A, run of 15 → 9?

Wait, BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBB has runs: 16 B's + A + 15 B's = max run 16, gave 9. But pure 32 B's also gave 9!

So 32 B's=9, 16 B's=3, max-run-16 case=9. Maybe sum of (run_length contribution)?
If contribution(L) for run of B/C of length L: 
- L=32 alone → 9
- L=16 alone → 3
- L=16 + L=15 (separated by A) → 9
So 16+15=31 B's giving 9 is similar to 32 B's giving 9. Maybe sum f(L) where f(16)+f(15) = 9 = f(32). Or maybe count of "good" positions/patterns.

Could be: number of substrings of length k that are all in {B,C}? 
- Length 32 all B: count of substrings of length k all-good. If k=24, count = 32-24+1 = 9! 
- Pure 32 B: 9 substrings of length 24.
- 16+15 with one A: longest run 16, so 0 substrings of length 24. But still 9...

Maybe count of "good" characters minus penalty? 32 B = 32, but reported 9...

Try: log scoring? floor(log2(L)) summed? log2(32)=5, not 9.

Let me try: count of B's where surrounding chars are also B (no A/D within window). Or: number of positions i such that s[i..i+w-1] are all B/C.

For pure 32 B's: # of length-w windows fully B/C = 33-w. 33-w=9 → w=24.
For 16 B + 16 A: length-w windows starting in first 16-w+1=... if w=24, none. But got 3 not 0.

Maybe non-overlapping count: 32/k = 9... 32/floor: no.

Let me test more lengths of pure B runs.

## 2026-06-28 15:07 — query 13

Run-length data:
- L=4: 0
- L=8: 1
- L=16: 3
- L=24: 6
- L=32: 9

Differences: 4→8: +1, 8→16: +2, 16→24: +3, 24→32: +3.
Try: floor((L-4)/?) something.
L=4: 0, L=8:1, L=16:3, L=24:6, L=32:9. 
Could be: ceil((L-5)/3)? L=8:(3/3)=1 ✓, L=16:11/3=3.67→4 ✗
Try floor((L-5)/3): L=8:1 ✓, L=16:3 (11/3=3.67→3) ✓, L=24:6 (19/3=6.33→6) ✓, L=32:9 (27/3=9) ✓, L=4: -1/3→? probably max 0.
So maybe score per run = max(0, floor((L-5)/3)) — but need to test boundaries.

L=5: floor(0/3)=0
L=6: floor(1/3)=0
L=7: floor(2/3)=0
L=8: 1 ✓
L=11: floor(6/3)=2
L=14: floor(9/3)=3

Also test 16+15 case (one A in middle of 32 B's):
two runs: 16 and 15. Score = floor(11/3) + floor(10/3) = 3 + 3 = 6. But measured 9!
So total isn't sum of independent runs. Hmm.

Unless A doesn't actually separate runs - check: BBBBBBBBBBBBBBBB(A)BBBBBBBBBBBBBBB gave 9. Same as pure 32 B. So one A might be "ignored"/treated as null. Or only D separates? And BBBB...DBBBB... also gave 9!

So both A and D in middle didn't reduce score. Maybe both are "neutral" — only counted is length of total B/C content?
Pure 32 B = 9, 31 B + 1 A = 9. Both have B-count of 32 or 31. Maybe formula uses B+C count?

B-count formula: 
L=32 B's, count=32, score=9
count=31, score=9
count=24, score=6
count=16, score=3
count=8, score=1
count=4, score=0
count=0, score=0

floor((count-5)/3): 32→9, 31→8.67→8 (not 9). Doesn't fit.
floor(count/3.5): 32→9.14→9, 31→8.86→8. No.
floor((count-2)/3.33)? 

Let me try ceil((count-4)/3): 32→28/3=9.33→10. No.
floor((count+1)/3.6): 32→33/3.6=9.16. 31→8.88→8.
floor((count-3)/3.2): 32→9.06, 31→8.75. 

Both 31 and 32 → 9. And 24→6, 16→3, 8→1, 4→0.
Could it be floor(count/3) - some const? 32/3=10.67. 

Could it be floor((count-2)/3)? 32→10, no.

Maybe NOT pure count. 16 B + 16 A gave 3. count=16. Same as L=16 pure. ✓
Yet 31 B + 1 A (in middle) gave 9 = same as L=32 pure. count=31 vs 32. Maybe both give 9?

Let me hypothesize: score = floor(count/3) with cap of 9? 
- 32/3=10.67→10 (but 9). Cap at 9 fits! 
- 31/3=10.33→10 → capped 9? 
- 24/3=8. But measured 6. ✗

Hmm. Try floor((count-4)/3): 
- 32: 28/3=9.33→9 ✓
- 31: 27/3=9 ✓
- 24: 20/3=6.67→6 ✓
- 16: 12/3=4 ✗ (got 3)
- 8: 4/3=1.33→1 ✓
- 4: 0/3=0 ✓

Close but 16 doesn't fit. Maybe position matters? Or (count-5)/3?
- 32:27/3=9 ✓
- 31:26/3=8.67→8 ✗

What about floor((count-1)/3.5)?
- 32: 31/3.5=8.86→8 ✗

Let me get more data: try L=16 in different positions, L=12, L=20.

## 2026-06-28 15:07 — query 16

More data, run of B's at start, rest A:
- L=0: 0
- L=4: 0
- L=8: 1
- L=12: 2
- L=16: 3
- L=20: 4
- L=24: 6
- L=28: 7
- L=32: 9

Differences: 4,1,1,1,1,2,1,2 → so per +4 chars: +1,+1,+1,+1,+2,+1,+2.
Cumulative: 0,0,1,2,3,4,6,7,9. 

It almost looks like floor(L*?/?). Let's see fractions per L:
8→1: 0.125, 12→2: 0.167, 16→3: 0.188, 20→4: 0.2, 24→6: 0.25, 28→7: 0.25, 32→9: 0.281

Could be: floor(L²/something)? 
- 8²/64=1, 12²/72=2, 16²/85.3=3 ... not clean.
- L² values: 64,144,256,400,576,784,1024
- divided by score: 64, 72, 85, 100, 96, 112, 113.7. Not constant.

Try L*(L-1)/2 = pairs:
- L=8: 28
- L=12: 66
- L=16: 120
- L=20: 190
- L=24: 276
- L=28: 378
- L=32: 496
Divided by score: 28, 33, 40, 47.5, 46, 54, 55.1. No.

Try cumulative # of substrings of length k that are all B. For pure run of L at start:
- # substrings of length k all-B = max(0, L-k+1) if length-k substr fits in run.
- Score for L=32 = 9 → if k=24: 32-24+1=9 ✓
- Score for L=8 should be 8-24+1<0. So 0, but measured 1.

Maybe sum over k? Or count of substrings of B/C of varying length?

Total number of substrings (i,j) of all-B/C content within string:
For pure run of L: L*(L+1)/2.
- L=8: 36, but score 1. /36? 

What if score = floor(L/4) * something? 
floor(L/4): 0,1,2,3,4,5,6,7,8. Doesn't match.

Look at the actual sequence:
L: 0 4 8 12 16 20 24 28 32
S: 0 0 1 2  3  4  6  7  9

Notice S(L) ≈ floor(L²/100)? 
- 64/100=0 ✗ (need 1)
- 144/100=1 ✗ (need 2)
Doesn't fit.

Try S(L) = floor((L-4)*(L+4)/something):
(L²-16): 48, 128, 240, 384, 560, 768, 1008. 
Divided by score: 48, 64, 80, 96, 93, 110, 112. Not clean.

Try counting non-overlapping length-3 motifs of BBB or CCC: floor(L/3):
L=8:2, L=12:4. Doesn't match.

Maybe count of length-k substrings of B's, where k varies?
Substrings BBB (length 3, overlapping): L-2. L=8→6. ✗

Hmm. Let me try a recursive read: score(L) = score(L-4) + Δ
4→8: +1; 8→12: +1; 12→16: +1; 16→20: +1; 20→24: +2; 24→28: +1; 28→32: +2.

Looks noisy but could be threshold-based. Or maybe involves position.

Let me try same B-count but different positions to test position-dependence.

## 2026-06-28 15:08 — query 19

Position invariance: L=16 at start, middle, end all give 3.
Splitting: 8+8 B's split by 16 A's = 4 (vs single L=16 = 3). So split helps slightly!

Two runs of 8: each "alone" gives 1; two of them gives 4, not 2. So runs interact non-linearly? Or formula isn't sum of run scores.

Maybe score is computed by sliding window/motif counting independent of run boundaries when separator is A.

Hypothesis: Score counts substrings of length k where the count of B/C ≥ some threshold, sliding window.

Let me consider: score = # of windows of size W where ≥ T of them are B/C.
For L=32 of B: every window is all B → score depends on W. 33-W = ? gives 9 → W=24.
But 16 B + 16 A: count of length-24 windows that are all B/C. None fit (max run is 16). But score = 3. ✗

Maybe score = # of length-k windows where ≥ ⌈k/2⌉ are B/C?
- Pure 32 B: 33-k = 9 → k=24. 
- L=16 at start (16 B + 16 A): windows of size 24; each window contains positions [i, i+23]. # of B's in window depends on overlap with the B-run. Window starting at i (0-indexed) covers 24 positions; B's in it = max(0, min(16,i+24)-max(0,i)). For i=0: 16 B's. Need ≥12 → yes. i=1: 15. ✓. ... i=4: 12. i=5: 11. ✗.
  So # windows with ≥12 B's: i=0..4, that's 5. But score 3. ✗

What about T=16? i=0 only → 1. ✗

Let me try a different angle: maybe score = number of substrings (start, length) that are entirely B/C and length ≥ some min.

For pure L=32: # substrings of length ≥M all B/C = sum_{k=M}^{32}(33-k).
- M=24: 9+8+7+...+1 = 45. ✗
- M=30: 3+2+1=6. M=29: 4+3+2+1=10.

Maybe just floor(L/k):
L=32, k=4: 8. L=32, k=3: 10. L=32, k=3.5: 9. Hmm.

Maybe ceil(L/4) - 0? 32→8. No.

Hmm what if score counts max # disjoint copies of pattern "BBBB" or similar.
Pure 32 B's, max disjoint BBBB = 8. Not 9.

Or count of length-k substrings with overlap, k=4: 32-4+1=29 for pure. Not 9.

Let me check very small B counts:
- 1 B (rest A): need data
- 2 B's
- 3 B's

## 2026-06-28 15:08 — query 23

BCBC=9, BBCC=9 confirms B and C interchangeable.
AABB pattern (16 B's, 16 A's): 0! But contiguous 16 B's=3.
So position/contiguity DOES matter, but in a discrete threshold way.

AABB: max run of B/C = 2 → 0
BBBAAA...x4 with runs of 3 each: 0
8+8 split by 16 A's: 4

So minimum run length matters. Hypothesis: only runs of length ≥ some min L_min contribute. 
Runs of length < ~5 contribute 0. Run of 8 contributes 1.

Test split 4+4 gave 0 (presumably; AABB), but 8+8 gave 4.

What about specific: score = sum over runs of f(run_length) where f(L)=max(0, floor((L-5)/3))?
- Run 8: 1, Run 16: 3, Run 24: 6, Run 32: 9. 
  L=8: (8-5)/3=1 ✓
  L=12: (12-5)/3=2.33→2 ✓
  L=16: (16-5)/3=3.67→3 ✓
  L=20: (20-5)/3=5 ✓ But got 4 ✗
  
Doesn't fit L=20.

Try f(L) = max(0, ⌊(L-4)/3⌋):
L=8: (4)/3=1 ✓
L=12: 8/3=2 ✓
L=16: 12/3=4 ✗ (got 3)

Try f(L) = max(0, ⌊L/4⌋ - 1):
L=8: 1 ✓
L=12: 2 ✓
L=16: 3 ✓
L=20: 4 ✓
L=24: 5 ✗ (got 6)
L=28: 6 ✗ (got 7)
L=32: 7 ✗ (got 9)

Close for small L but breaks for large L. 

Maybe there's a bonus for being at a special position? L=24 at start gave 6, L=24 elsewhere?
Let me check whether L=24 elsewhere differs.

## 2026-06-28 15:08 — query 26

Position-invariant. L=20→4 anywhere. L=24→6 anywhere.

8+8 B's: 4. (one of 1+1=2 doesn't fit; 4 is much more)
8+8+8 B's: 8. Way more than 3+1+1+1=3.

Hmm, three runs of 8 = 8. Two runs of 8 = 4. One run of 8 = 1.
1, 4, 8 for n=1,2,3 runs of 8. Pattern: n²: 1, 4, 9. Hits 1, 4 but 8 not 9.
Actually 8 might be off — let me see if 3 runs of 8 in 32 chars is even possible: 8+1+8+1+8 = 26... need separators of ≥1 between. With 4-char separators: 8+4+8+4+8 = 32 yes.

If formula is (sum of B/C - constant_per_break)² or similar:
2 runs of 8: 16 B's. one run of 16 → 3.
But 2 separated runs of 8 = 4.

So splitting does help! Single run of 16 = 3; two runs of 8 = 4.

Three runs of 8: 24 B's. Single run of 24 = 6. Three runs = 8.

Maybe score = (# of runs of length ≥ T)² or similar?
- 1 run of 8: 1=1²
- 2 runs of 8: 4=2²
- 3 runs of 8: 9=3²? But we got 8, not 9.

Close to n² but not exact. Could be n² - constant_or_correction.
Or could relate to number of distinct B-segments + their lengths.

Let me try 4 runs of any length.

## 2026-06-28 15:09 — query 30

More data:
- 1 run of 4 = 0
- 1 run of 8 = 1
- 1 run of 16 = 3
- 1 run of 24 = 6
- 1 run of 32 = 9
- 2 runs of 8 (16 B's) = 4
- 3 runs of 8 (24 B's) = 8
- 4 runs of 4 (16 B's) = 6
- 4 runs of 5 (20 B's) = 6
- 4 runs of 6 (24 B's) = 7
- 8 runs of 2 = 0

Interesting: 4 runs of 4 = 6, but 1 run of 4 = 0. So when there are MANY short runs, they contribute. So it's not "min run length to contribute".

4 runs of 4 (16 B's) > 1 run of 16 (3) ← yes, 6 > 3.
4 runs of 5 (20 B's) = 6 > 4 (1 run of 20)
4 runs of 6 (24 B's) = 7 > 6 (1 run of 24)

3 runs of 8 (24 B's) = 8, which is more than 4 runs of 6 (24) = 7.
2 runs of 8 (16 B's) = 4 < 4 runs of 4 (16 B's) = 6.

Maybe scoring is: number of "BB" pairs (adjacent B/C positions)?
Count of BB or CC or BC or CB adjacent pairs:
- Pure 32 B: 31 adjacent pairs all B → 31. But score 9.
- 1 run of 8: 7 pairs → 7. Score 1.
- 1 run of 16: 15 pairs → 15. Score 3.
- 2 runs of 8: 14 pairs → 14. Score 4.
- 4 runs of 4: 12 pairs → 12. Score 6. 

Ratio score/pairs: 9/31≈0.29, 1/7≈0.14, 3/15=0.2, 4/14≈0.29, 6/12=0.5. Not constant.

What about count of "good" triples?
1 run of 8: 6 triples → 1. 
1 run of 16: 14 → 3. 
1 run of 32: 30 → 9.
Ratios: 1/6, 3/14, 9/30=0.3. Hmm not clean.

What about: # of length-4 substrings that are all B/C?
Pure 32 B: 29 substrings. Score 9.
1 run of 8: 5. Score 1.
1 run of 16: 13. Score 3.
2 runs of 8: 10. Score 4.
4 runs of 4: 4 substrings (one per run, only the full run). Score 6.
4 runs of 6: each contributes 3 length-4 substrings = 12. Score 7.
3 runs of 8: each contributes 5 = 15. Score 8.

Not a clean ratio.

What about length-2 (BB) substrings (overlapping)?
1 run of L: L-1 pairs.
Score(L)*?: L=8→7→1, L=12→11→2, L=16→15→3, L=20→19→4, L=24→23→6, L=28→27→7, L=32→31→9.
Pairs/score: 7, 5.5, 5, 4.75, 3.83, 3.86, 3.44.
Score ≈ pairs / 4? 7/4=1.75→1, 15/4=3.75→3, 31/4=7.75 ≠9.

Try length-3 (BBB) substrings:
L=8→6→1, L=12→10→2, L=16→14→3, L=20→18→4, L=24→22→6, L=28→26→7, L=32→30→9.
Triples/score: 6, 5, 4.67, 4.5, 3.67, 3.71, 3.33.

# of length-4 (BBBB) substrings:
L=8→5→1, L=12→9→2, L=16→13→3, L=20→17→4, L=24→21→6, L=28→25→7, L=32→29→9.
4-tuples/score: 5, 4.5, 4.33, 4.25, 3.5, 3.57, 3.22.

L=32: 29/9≈3.22. L=24: 21/6=3.5. L=20: 17/4=4.25. Not a power law.

Let me try a different idea: score might be number of pairs of B's separated by some specific distance.

Pure run of L: # pairs (i,j) with j-i=d and both B = L-d. Sum over d=1..D: sum_{d=1}^{D}(L-d) = D*L - D(D+1)/2.

For D=1, L=32: 32-1=31. /9=3.44.

Or count of pattern "BB" non-overlapping? L=32: 16.

Let me try: count of B's at specific positions (positional fitness landscape). If certain positions are "active".

If 9 positions are good, all-B = 9 (each contributes 1). 
- 16 B's at start (pos 0-15) = 3 → so 3 good positions in 0-15.
- 16 B's at middle (pos 8-23) = 3 → 3 good in 8-23.
- 16 B's at end (16-31) = 3 → 3 in 16-31.

If 3 good in 0-15, 3 in 8-23, 3 in 16-31: overlap matters. 0-15∩8-23 = 8-15. 8-23∩16-31=16-23. 
Need: |good ∩ [0,15]|=3, |good ∩ [8,23]|=3, |good ∩ [16,31]|=3, total = 9.
Could be 3 in [0,7], 3 in [12,15] no wait... Need exactly 3 each.

Let's say good positions split: a in [0,7], b in [8,15], c in [16,23], d in [24,31]. Total a+b+c+d=9.
[0,15] = a+b=3. [16,31]=c+d=3. [8,23]=b+c=3. So a+b=3, c+d=3, b+c=3, a+b+c+d=9? But a+b+c+d=3+3=6, not 9!

Contradiction! So can't be simple positional.

Unless count is non-linear in # of good positions covered. E.g., good positions = 9 specific positions; the score is # of good positions where the char is B/C, BUT non-linear.

If 9 good positions: all-B → all 9 active → 9.
16-B run covering 3 → 3.
8+8 split covering 4 → 4.
4 runs of 8 covering 8 → 8.

Actually 8+8 covered 4 good positions, but 16 covered only 3. 32 covered 9, 24 covered 6. 

Positional hypothesis works IF score = # of good positions activated. Let me derive:
Assume 9 specific positions are "good". S = sum over good pos of [s[i] ∈ {B,C}].

For run [0,L-1]: count of good positions in [0,L-1].
- L=4: 0 good
- L=8: 1 good
- L=12: 2 good
- L=16: 3 good
- L=20: 4 good
- L=24: 6 good (jump of 2 in [20,23])
- L=28: 7 good
- L=32: 9 good (jump of 2 in [28,31])

So good positions count by prefix [0,L-1]:
L=4: 0 → no good in [0,3]
L=8: 1 → 1 good in [4,7]
L=12: 2 → 1 good in [8,11]
L=16: 3 → 1 good in [12,15]
L=20: 4 → 1 good in [16,19]
L=24: 6 → 2 good in [20,23]
L=28: 7 → 1 good in [24,27]
L=32: 9 → 2 good in [28,31]

Total 9 good positions in regions: 0 in [0,3], 1 each in [4,7],[8,11],[12,15],[16,19],[24,27], 2 each in [20,23],[28,31].

Test with L=16 in middle (pos 8-23): good in [8,23] should = 1+1+1+2=5. But measured 3. ✗

So position invariance contradicts this — moving the run gives different counts unless symmetric.

Unless score isn't position-dependent at all, but depends on prefix-length somehow? L=16 at start, middle, end all gave 3. So it's symmetric.

That means good positions hypothesis only works if good positions are translation-invariant within string — that's not possible for fixed positions.

So position doesn't matter. Run-length structure does. Reformulate.

Compositional features that are translation-invariant (only run-length matters):
- multiset of run-lengths of B/C-runs

Let me tabulate score as function of multiset of run lengths:
{4}: 0
{8}: 1
{12}: 2
{16}: 3
{20}: 4
{24}: 6
{28}: 7
{32}: 9
{8,8}: 4
{8,8,8}: 8
{4,4,4,4}: 6
{5,5,5,5}: 6
{6,6,6,6}: 7
{2,2,2,2,2,2,2,2}: 0
{3,3,3,3}: 0 (from earlier BBBAAAAA*4)
{16,15}: 9 (the BBBB...B(A)BBBB...B case)
{16,0}: equivalent to {16}=3, but I had BBBB(16 B)+16A=3, also BBBB(A)BBBB...=9 → that was 16+15 not just 16.

Now if score is f(multiset), what formula works?

{8}=1, {8,8}=4, {8,8,8}=8. 
With 1 run: 1, 2 runs: 4, 3 runs: 8. 
Ratios: 1, 4, 8. Diffs: 3, 4. Not n².

{4,4,4,4}=6. 4 runs of 4.
{2*8}={6,6,6,6}=7, similar.

Try: total B/C count + bonus for # runs?
{4,4,4,4}: 16 B's, 4 runs. Score 6. 
{8,8}: 16 B's, 2 runs. Score 4. 
{16}: 16 B's, 1 run. Score 3.
For 16 B's: 16/2 + #runs = ?: 8+1=9, 8+2=10, 8+4=12. No.
Score - 16: -13, -12, -10. No.
3, 4, 6 → diff 1, 2. Like # runs - 1? 
score = base + (#runs - 1)? With 16 B's base=3, +0,+1,+3? Diff for #runs=4 is 3 vs 2 for #runs=2, so +(#runs-1)? 1 run=3+0=3 ✓, 2 runs=3+1=4 ✓, 4 runs=3+3=6 ✓.

Let me check 24 B's:
- {24}: 6
- {8,8,8}: 8
- {6,6,6,6}: 7

For 24 B's, base=6. With #runs=1: 6, #runs=3: 8, #runs=4: 7?? Doesn't follow (#runs-1) pattern strictly.

Maybe (#runs-1) with diminishing returns or capped.

Actually: 1 run=6, 3 runs=8, 4 runs=7. 4 runs gave less than 3 runs!
Sequence was BBBBBBAA*4. Note runs of 6 each. While 3 runs of 8 each.

So shorter runs are penalized? Maybe score combines: f(L) per run, but with bonus.

Let me try a totally different angle. Maybe score depends on having particular MOTIFS, e.g., specific length-k substrings.

Let me brute force test: try multiplying motifs.

## 2026-06-28 15:09 — query 35

More data:
- 15+15 split by AA: 9 (same as 30 contiguous)
- 10+10+10 split by A's: 9 
- 7+7+7+7 split by A's: 7
- 15+15 split by DD: 9
- 4 runs of 5 (BBBBB AAA *4): 6
- 4 runs of 6 (BBBBBB AA *4): 7
- 4 runs of 7 (BBBBBBB A *4): 7
- 4 runs of 8 (BBBBBBBB AAAA *4): wait, didn't test this — actually had 3 runs of 8.

Total B counts:
- 15+15=30 B's: 9
- 10+10+10=30 B's: 9
- 7+7+7+7=28 B's: 7
- 6+6+6+6=24 B's: 7
- 5+5+5+5=20 B's: 6
- 4+4+4+4=16 B's: 6
- single 32 B's: 9
- single 28 B's: 7

Wait! 4 runs of 7 (28 B's) = 7 = single 28-run!
4 runs of 8 (24 B's) — actually I tested 3 runs of 8 (24 B's) = 8 but single 24 = 6.

Let me check: maybe score = total # B's minus penalty(non-B/C) or just function of B-count + small structural?

B-counts and scores:
- 0: 0
- 4: 0
- 8: 1
- 12: 2
- 16: 3 (single) or 4 (8+8) or 6 (4+4+4+4)
- 20: 4 (single) or 6 (5*4)
- 24: 6 (single) or 7 (6*4) or 8 (8*3)
- 28: 7 (single) or 7 (7*4)
- 30: 9 (15+15) or 9 (10+10+10)
- 31: 9 (with one A in middle)
- 32: 9

Hmm. 

Hypothesis: score = (# B's) - (# A's or D's in B-region)? Or maybe pairs of (B/C adjacent to other B/C)?

Try: score = # of adjacent B/C-B/C pairs (i,i+1) both in {B,C} - some penalty? OR ceil((# such pairs)/something)?

Pairs of consecutive B/C:
- 32 B's: 31 pairs → 9
- 30 B's (15+15 with AA gap): 14+14=28 pairs → 9
- 30 B's (10+10+10): 9+9+9=27 pairs → 9
- 28 B's (single): 27 → 7
- 28 B's (4 runs of 7): 6*4=24 → 7
- 24 B's (single): 23 → 6
- 24 B's (3 of 8): 7*3=21 → 8 ← Wait, less pairs but higher score!
- 24 B's (4 of 6): 5*4=20 → 7
- 20 B's (single): 19 → 4
- 20 B's (4 of 5): 4*4=16 → 6 ← Less pairs, more score!
- 16 B's (single): 15 → 3
- 16 B's (8+8): 7+7=14 → 4
- 16 B's (4 of 4): 3*4=12 → 6 ← Less pairs, more score!
- 12: 11 → 2
- 8: 7 → 1

So #pairs alone doesn't explain. Splitting into more runs INCREASES score despite fewer pairs.

Maybe the score rewards "structure" — # of runs?
For 16 B's: 1 run=3, 2 runs=4, 4 runs=6. So +1 per extra run? Roughly.
For 24 B's: 1 run=6, 3 runs=8, 4 runs=7. So 3 runs gives +2 vs 1 run.
For 20 B's: 1 run=4, 4 runs=6. +2.

Maybe formula: score = total_B_count / 4 + something? 
- 32/4 = 8, score 9.
- 16/4 = 4, +0 runs(1)=3, +1run(2)=4, +3runs(4)=6. So 4+(#runs-1) for 16 B's? 1run:4+(-1)=3 ✓, 2runs:4+0=4 ✓, 4runs:4+2=6 ✓. So 16 fits "total/4 + #runs - 1".
- 32/4=8 + 0 = 8, not 9. ✗

Try total_BC // 4 + #runs - 1:
- 32: 8+0=8 ≠ 9
- 24 single: 6+0=6 ✓
- 24 (3 runs): 6+2=8 ✓!
- 24 (4 runs): 6+3=9 ≠ 7. ✗

Doesn't fit 4 runs of 6.

Maybe runs of length < some threshold don't fully count, and a run of L contributes f(L) ≈ floor(L/4):
floor(L/4) values: L=4→1, L=5→1, L=6→1, L=7→1, L=8→2, L=12→3, L=16→4, L=20→5, L=24→6, L=28→7, L=32→8.

Run scores:
{4}=0; floor(4/4)=1, but score 0. ✗
{8}=1; floor(8/4)=2, but 1. 
{32}=9; floor=8, but 9.

Try floor((L-?)/?)+? Let's regress.

Let me try: f(L) = floor((L-1)/4):
L=4: 0 ✓
L=8: 1 ✓
L=12: 2 ✓
L=16: 3 ✓
L=20: 4 ✓
L=24: 5 (should be 6) ✗
L=28: 6 (should be 7) ✗
L=32: 7 (should be 9) ✗

Hmm. For L≥24 it deviates upward.

Sum f(L) across runs:
{4,4,4,4}: 4*0=0 (need 6) ✗
{6,6,6,6}: 4*1=4 (need 7) 

So single-run f(L) = floor((L-1)/4) for L ≤ 20. But for combined runs we need MORE.

Let me try: score = sum_{i} something - 1, where each "B unit" gets fractional contribution?

Actually, look at the {16,15} case: 31 B's, score 9. {16}=3, {15}=? Probably 3 (since {16}=3, {12}=2, expect {15}=3). Sum 3+3=6 ≠ 9.

So merging or proximity matters. {16,15} with AA separator effectively = 30 B's, contiguous-ish = 9, like 32 alone (also 9).

Key insight: gaps of 1-2 A's don't separate runs effectively. Let me explore.

## 2026-06-28 15:09 — query 37

{4,4} far apart = 2. {4,4,4} = 4. {4,4,4,4}=6. {4}=0.
Pattern: 0, 2, 4, 6. So 2*(n-1) for n runs of 4? Or 2*n - 2?
n=1: 0, n=2: 2, n=3: 4, n=4: 6. → score = 2(n-1).

For runs of 8:
n=1: 1, n=2: 4, n=3: 8.
Not arithmetic. Diffs: 3, 4.

For runs of 6:
n=4: 7.

For runs of 5:
n=4: 6.

For runs of 7:
n=4: 7.

Let me think about it differently. Maybe score = total_BC - 2*(# runs) or something nonlinear.

{4,4,4,4}: 16 - 4*? = 6. 16-10=6, so penalty 10? Doesn't simplify.

Maybe score = (sum of (L-2)+) over runs?
{4}: 2 (need 0)
{4,4,4,4}: 8 (need 6)
{8}: 6 (need 1)
Doesn't match.

Maybe each run is a "unit" with score depending on length AND total runs.

I'm spending too many experiments. Let me change strategy and think about whether D matters differently than A.

Tests so far don't differ for A vs D in middle positions. Let me check if D in run / replacement of B affects.

## 2026-06-28 15:10 — query 40

A and D both give same results as separators. So {B,C} are "good" and {A,D} are "bad/neutral". 
3 runs of 8 split by 4 D's: 8. Same as separated by 4 A's: 8. ✓

So effectively 2-letter biology: {B,C}=1, {A,D}=0. Now score depends on structure of 1's.

Let me compile run-length-only data (B/C contig runs):
{}: 0
{4}: 0
{8}: 1
{12}: 2
{16}: 3
{20}: 4
{24}: 6
{28}: 7
{32}: 9
{4,4}: 2
{4,4,4}: 4
{4,4,4,4}: 6
{5,5,5,5}: 6
{6,6,6,6}: 7
{7,7,7,7}: 7
{8,8}: 4
{8,8,8}: 8
{10,10,10}: 9
{15,15}: 9
{16,15}: 9 (effectively 31 B's)
{2,2,2,2,2,2,2,2}: 0
{3,3,3,3}: 0

What works? Let's try score = sum f(L) where f(L) = max(0, L-3) - something?
f(L) = max(0, L-3): {4}=1 (need 0); ✗
f(L) = max(0, L-4): {4}=0 ✓, {8}=4 (need 1) ✗

What about a quadratic-like formula?
For runs of 4:
n=1: 0, n=2: 2, n=3: 4, n=4: 6 → 2(n-1) = 2n-2.

For runs of L (all same), n copies in 32:
n*L + (n-1)*gap = 32 → gap = (32-nL)/(n-1).
Could score depend on total content + spacing?

For runs of L, in n copies:
- L=4, n=1: 0
- L=4, n=2: 2
- L=4, n=3: 4
- L=4, n=4: 6
- L=5, n=4: 6
- L=6, n=4: 7
- L=7, n=4: 7
- L=8, n=1: 1
- L=8, n=2: 4
- L=8, n=3: 8
- L=10, n=3: 9
- L=15, n=2: 9
- L=16, n=1: 3

Let me consider: maybe each position contributes if it's part of B/C with another B/C nearby (within window k).

Try: score = # of B/C characters that have at least one B/C within distance 2.

For {4}: 4 B's, each has neighbors within 2. Each contributes? = 4. But score 0.

Try: # of B/C characters with at least one B/C exactly at distance d (some specific d)?

Try: # of pairs (i, j) such that s[i], s[j] ∈ {B,C}, in some relation.

Let's count # of pairs (i, j), i<j, both B/C, with j-i in some set:
- Pure 32: pair count = C(32,2) = 496. Need 9.
- 16: C(16,2)=120. Need 3.
- 32/120/496 vs 9/3 — 496/9 ≈ 55, 120/3=40. Not constant.

# of B/C-pairs at distance EXACTLY d:
For pure 32: 32-d pairs at distance d. Sum d=1..D = sum.
- D=4: 31+30+29+28=118. No.

Score 9 for pure 32, 3 for pure 16, suggests something near L*0.28 or L²/120. L²/120: 8.5 for L=32, 2.13 for L=16. ~Close but not exact.

Try cube root or some function:
- floor(L*0.28): 0,1,2,3,4,5,6,7,8 for L=4,...,32. Doesn't match.

Hmm OK let me look at the gap between (1 run of L) and (k runs summing to total):
n*L Single (sum) = ?
- 16 single: 3 = 3
- 16 (4 runs of 4): 6 = 2*3
- 16 (2 runs of 8): 4 ≈ 1+3?
- 20 single: 4
- 20 (4 runs of 5): 6
- 24 single: 6
- 24 (3 runs of 8): 8
- 24 (4 runs of 6): 7

It's interesting that {8,8,8}=8 > {4,4,4,4}=6 even though total B = 24 vs 16. But {8,8,8}=8 < {32}=9.

Try total contribution where each B/C contributes 1 if in "long enough" run, but with bonus for # of runs:

Actually let me think: maybe the score is # of length-3 substrings of B/C, with diminishing returns or capped?
# of BBB-type substrings (any 3 consecutive B/C):
{4}: 2, {8}: 6, {12}: 10, {16}: 14, {20}: 18, {24}: 22, {28}: 26, {32}: 30.
Scores: 0, 1, 2, 3, 4, 6, 7, 9.
Ratio: -, 1/6, 2/10, 3/14, 4/18, 6/22, 7/26, 9/30. Not clean.

Let me try score = floor(triples/4):
2/4=0 ✓; 6/4=1 ✓; 10/4=2 ✓; 14/4=3 ✓; 18/4=4 ✓; 22/4=5 (need 6) ✗

Try score = floor((triples+2)/4):
{4}:(4)/4=1 ✗

Try # of length-2 (pairs):
{4}: 3, {8}: 7, {16}: 15, {24}: 23, {32}: 31.
floor((pairs-1)/3)? 2/3=0, 6/3=2 (need 1), no.

Let me try # of length-4 substrings:
{4}: 1, {8}: 5, {12}: 9, {16}: 13, {20}: 17, {24}: 21, {28}: 25, {32}: 29.
Scores: 0, 1, 2, 3, 4, 6, 7, 9.

Hmm: 0,1,2,3,4,6,7,9 - jumps at L=24 (+2) and L=32 (+2). 

L=24: 21 → 6.
L=32: 29 → 9.
Ratio 21/6=3.5, 29/9=3.22.

Try floor((length-4-substr-count + 1)/3.something):
(1+2)/3=1 (need 0), nope.

Look more carefully: 0,1,2,3,4,6,7,9.
Diffs at L: 4(0→0)0; 8:+1; 12:+1; 16:+1; 20:+1; 24:+2; 28:+1; 32:+2.

Could there be a 0/1 indicator that adds when L hits 24 and 32?

Wait, score(24)=6, score(20)=4. Diff 2. score(24+4=28)=7, score(28+4=32)=9, diff 2.

Maybe the formula counts:
- # of complete "chunks" of size 4 OR # of complete chunks of size 8, OR similar?

For run L, # chunks of size 4: floor(L/4): 1,2,3,4,5,6,7,8 for L=4..32.
For run L, # chunks of size 8: floor(L/8): 0,1,1,2,2,3,3,4.
Sum: 1,3,4,6,7,9,10,12. Doesn't match (0,1,2,3,4,6,7,9).

Try # chunks of size 4 + # chunks of size 8 - 1:
L=4: 1+0-1=0 ✓
L=8: 2+1-1=2 (need 1) ✗

Try # of complete chunks of size 4 in run, minus # runs:
{4}: 1-1=0 ✓
{8}: 2-1=1 ✓
{12}: 3-1=2 ✓
{16}: 4-1=3 ✓
{20}: 5-1=4 ✓
{24}: 6-1=5 (need 6) ✗
{28}: 7-1=6 (need 7) ✗  - wait this WORKS as -1 for 28!  no, 7-1=6, need 7.

Hmm so the formula works for L=4..20 then breaks.

Try: floor(L/4)*1 + floor(L/16): 
L=4: 1+0=1 (need 0)
L=24: 6+1=7 (need 6)
Nope.

Try: floor((L*L)/N):
L=32: 1024/N=9 → N≈114
L=16: 256/114=2.24→2 (need 3) ✗

Or (L-3)*(L)/100:
32: 29*32/100=9.28→9 ✓
28: 25*28/100=7 ✓
24: 21*24/100=5.04→5 ✗ (need 6)

Hmm. Let me re-test L=24 to verify.

## 2026-06-28 15:11 — query 49

Full single-run table:
L: 4, 5, 6, 7, 8, 12, 16, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
S: 0, ?, ?, ?, 1, 2, 3, 4, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9

Note: pure 31 B's then A vs B(A in middle B*15) — we tested {16,15}=31 B's split → score 9. But single 31 = 8. So splitting helps!

S(L) for single run:
L=4: 0
L=8: 1
L=12: 2
L=16: 3
L=20: 4
L=22-23: 5
L=24-27: 6
L=28-29: 7
L=30-31: 8
L=32: 9

Looks like Score increases each ~4 chars but irregularly past L=20.
Cumulative thresholds: ~L=8 for 1, L=12 for 2, L=16 for 3, L=20 for 4, L=22 for 5, L=24 for 6, L=28 for 7, L=30 for 8, L=32 for 9.

Threshold jumps: 8,12,16,20,22,24,28,30,32. Gaps: 4,4,4,2,2,4,2,2.

Could be related to integer multiples. Let me try formula floor(L/4) + extra:
L=4:1; L=8:2; L=12:3; L=16:4; L=20:5; L=22:5; L=24:6; L=28:7; L=32:8. Score = floor(L/4) - 1? L=4:0 ✓, L=8:1 ✓, L=12:2 ✓, L=16:3 ✓, L=20:4 ✓, L=24:5 (need 6) ✗.

So floor(L/4)-1 works through L=20.

Beyond L=20 something else adds:
L=22: 5 = 4 + 1; L=24: 6 = 5 + 1; L=28: 7 = 6 + 1; L=30: 8 = 6 + 2; L=32: 9 = 7 + 2.

Maybe: score = floor(L/4)-1 + max(0, floor((L-20)/something))?
L=20: +0
L=22: +1: floor(2/2)=1
L=24: +1: floor(4/4)=1
L=28: +1
L=30: +2
L=32: +2

floor((L-20)/4)+ floor((L-22)/something)? Complicated.

OR maybe it's: score = floor(L/4) - 1 + floor(L*(L-20)/N)? 

Let me try another approach: score = # of B/C - # singletons or some other count.

Actually, let me see if score follows floor(L^2/something):
L=4: 16/X=0 → X≥17.
L=8: 64/X=1 → X∈[33,64].
L=32: 1024/X=9 → X∈[103,114].
Not consistent.

Try score = floor((L-3)(L+4)/120) or similar quadratic:
L=4: 1*8/120=0 ✓
L=8: 5*12/120=0.5→0 ✗

Or floor(L*(L-3)/120):
L=8: 40/120=0 ✗

Hmm. Let me just see the data as floor(L/k) for varying k:
L=8: 1; if score=floor((L-7)/c): L=8:1/c=1→c=1: but then L=12 → 5 not 2.

Look at the sequence 0,1,2,3,4,5,6,7,8,9. The score jumps from k to k+1 at L = 4,8,12,16,20,22,24,28,30,32.

Differences in L at score jumps: 4,4,4,4,2,2,4,2,2.

What if score = number of "milestones" passed where milestones are at specific L values?
Milestones: 5(→1?), 9,13,17,21,23,25,29,31, ??

Or: each B adds something, and there's a baseline subtraction.

Let me try: score = sum_{i=1}^{L} c_i where c_i depends on i (the i-th B/C in the run)?
S(L)-S(L-1) for L→L+1:
L=4→5: ?
L=7→8: 0→1: c_8=1
L=11→12: 1→2: c_12=1
L=15→16: 2→3: c_16=1
L=19→20: 3→4: c_20=1
L=21→22: 4→5: c_22=1
L=23→24: 5→6: c_24=1
L=27→28: 6→7: c_28=1
L=29→30: 7→8: c_30=1
L=31→32: 8→9: c_32=1

So contributing positions when added: 8, 12, 16, 20, 22, 24, 28, 30, 32.
These match the "milestones" I noted.

Maybe it's positional after all but somehow length-invariant via right-anchoring? Let me test L=20 in the middle/end again - we got L=20 middle: 4 ✓; L=24 end: 6 ✓. So it's NOT positional.

So formula depends on L only. Let's predict and verify:
- L=21: should be 4 or 5? Gap was 20→22, so probably L=21→4.
Let me check L=21 to be sure.

Actually I realize the threshold pattern 8,12,16,20,22,24,28,30,32 looks like multiples-related.
8=8, 12=8+4, 16=8+8, 20=8+12, 22=8+14, 24=8+16, 28=8+20, 30=8+22, 32=8+24.
Hmm.

Equivalent: needed L for score k:
k=1: L≥8
k=2: L≥12
k=3: L≥16
k=4: L≥20
k=5: L≥22
k=6: L≥24
k=7: L≥28
k=8: L≥30
k=9: L≥32

Differences in min L: 4,4,4,2,2,4,2,2. Odd.

Maybe it's # of "B/C-pairs at distance d" for various d:
Pair at distance 1: L-1. So # ≥ k pairs needs L ≥ k+1.
Hmm.

Maybe score = sum of floor((L-d_i)/c) for some set of d's?
Or count of pairs at distances in some set.

Let me try: score = # of length-2 substrings + # of length-4 substrings + ...?

Let me compute predicted score(L) = floor(L/4) + floor(L/8) - 1:
L=4: 1+0-1=0 ✓
L=8: 2+1-1=2 (need 1) ✗

Try floor(L/4) + floor(L/16) - 1:
L=4: 1+0-1=0 ✓
L=8: 2+0-1=1 ✓
L=12: 3+0-1=2 ✓
L=16: 4+1-1=4 (need 3) ✗

Try floor((L-1)/4) + floor((L-1)/16):
L=4: 0+0=0 ✓
L=8: 1+0=1 ✓
L=12: 2+0=2 ✓
L=16: 3+0=3 ✓
L=20: 4+1=5 (need 4) ✗

Try floor(L/4)-1 + floor((L-1)/11): ad hoc.

Let me try floor((L-1)/4) for L≤20, then incremental:
L=20:4, L=24:6 → +2 over 4 extra. Avg 0.5 per char.
L=24:6, L=28:7 → +1 over 4.
L=28:7, L=32:9 → +2 over 4.

What if score = round(L * 9/32)?
L=32: 9 ✓
L=28: 7.875→8 (need 7) ✗

Try score = floor((L^2 - something)/100):
L=32: 1024/100=10.24→10. Need 9.

OK, let me try a completely different approach: simulation. The pattern is consistent with: for each i in 1..32, if i ≤ L there's contribution; specific i's count.

Looking at "contributing positions": when you add the L-th B/C, score goes up by 1 if L ∈ {8, 12, 16, 20, 22, 24, 28, 30, 32}.

These are: 8, 12, 16, 20, 22, 24, 28, 30, 32.
Or: 32 - {0, 2, 4, 8, 10, 12, 16, 20, 24} = {32, 30, 28, 24, 22, 20, 16, 12, 8}.

Differences in "good" L: 4,4,4,2,2,4,2,2. 

Wait, maybe scores are off-by-one and actually score jumps at L=5,9,13,17,21,23,25,29,31? Let me check more boundaries.

## 2026-06-28 15:11 — query 52

Confirmed: L=5,6,7 all give 0. L=8 gives 1. So threshold is exactly L=8 for score 1.

Updated single-run thresholds (L for score k):
k=1: L=8
k=2: L=12
k=3: L=16
k=4: L=20
k=5: L=22
k=6: L=24
k=7: L=28
k=8: L=30
k=9: L=32

I wonder if maybe the score is the number of non-overlapping substrings of length ≥ 8 that can be carved out of the B/C content?

Single run of L: # non-overlapping length-8 substrings = floor(L/8).
L=8:1, L=16:2, L=24:3, L=32:4. Doesn't match.

What about # of length-k substrings (overlapping) with k chosen as min(8, ...)?

How about: # of pairs of positions (i,j) with i<j, both B/C, AND j-i is in some specific set?

Or, # of B/C positions p such that some condition (like "BBBBBBBB" — length 8 window — exists containing p)?

For run of L, # of positions in length-8 windows of B/C: if L≥8, every position in run is in some window. So = L if L≥8.
L=8:8 (need 1), no.

Try: # of length-8 windows of all B/C = max(0, L-7).
L=8:1 ✓; L=12:5 (need 2) ✗

What about a "logarithmic" score? floor(log2(L-X))?

Hmm let's count for single-run scores differently:
(L, score): (8,1), (12,2), (16,3), (20,4), (22,5), (24,6), (28,7), (30,8), (32,9).

Score-L correspondence:
At score k, min L = ?
k=1: 8 
k=2: 12 (diff 4)
k=3: 16 (diff 4)
k=4: 20 (diff 4)
k=5: 22 (diff 2)
k=6: 24 (diff 2)
k=7: 28 (diff 4)
k=8: 30 (diff 2)
k=9: 32 (diff 2)

OR: each additional B/C beyond L=7 adds 1/4 to score, plus there are bonus jumps. What if there are TWO components: one based on consecutive B/C count, and another based on number of "BBBBBBBB" (8-letter) motifs?

Component A: floor((L-4)/4) for run of L (or 0 if L<8)?
L=8:1; L=12:2; L=16:3; L=20:4; L=24:5; L=28:6; L=32:7. Need: 1,2,3,4,6,7,9.
Component B (bonus): L=8:0; L=12:0; L=16:0; L=20:0; L=24:1; L=28:1; L=32:2.

Component B looks like: floor((L-16)/8)?
L=24: 8/8=1 ✓; L=32: 16/8=2 ✓; L=20: 4/8=0 ✓; L=28: 12/8=1 ✓; L=22: 6/8=0; L=30: 14/8=1.

So score(L) = floor((L-4)/4) + floor((L-16)/8) for L ≥ 8?
L=8: 1+0=1 ✓
L=12: 2+0=2 ✓
L=16: 3+0=3 ✓
L=20: 4+0=4 ✓
L=22: floor(18/4)=4 + floor(6/8)=0 = 4. Need 5! ✗

Close but L=22 needs +1. Hmm.

Actually wait: floor((22-4)/4) = floor(18/4) = 4. So predicted 4. Got 5.

Maybe the formula is floor((L-4)/4) + floor((L-?)/?) for another threshold.

L=22 +1 from somewhere; L=24 same.
L=22: 5. (L-4)/4 = 4.5. round? round(4.5)=4 or 5 depending. 
L=30: 8. (L-4)/4=6.5. round to nearest = 6 or 7. Doesn't fit 8 either.

Let me actually test if my data is correct - re-test L=22.

## 2026-06-28 15:11 — query 53

!! Re-test: L=22 in middle gave 4. Earlier L=22 at start gave 5. POSITION MATTERS after all!

Let me re-verify with original sequence.

## 2026-06-28 15:11 — query 57

Interesting! L=22 middle with C's instead of B's gave 4, but L=22 anywhere with B's gave 5. So B and C ARE different!

Let me verify: pure 32 C's gave 9 (same as 32 B's). But L=22 of C gave 4 (vs 5 for B). 

Or maybe the diff is the surrounding chars. Let me retest the C case with B's around.

## 2026-06-28 15:12 — query 60

!!! REPRODUCED CLEARLY:
- L=22 C's, positions 5-26: 4
- L=22 B's, positions 5-26: 5

Same position, different character → different score! So B and C are NOT identical.

But pure 32 B = 9 = pure 32 C. So in some configs they tie, in others they differ.

Maybe scoring is more subtle. Perhaps score = f(B) + g(C) where each is computed separately?

Let's check: pure 32 B = 9. Pure 32 C = 9. So f(32 B's) = 9 = g(32 C's).
Pure 16 B (in 32) = 3. What about pure 16 C?

## 2026-06-28 15:12 — query 63

L=22 C's at start = 5. L=22 C's at center = 4. Same character C, position matters!
L=22 B's at center = 5. So C at center=4, B at center=5. Difference.

But L=16 C's at start = 3, same as L=16 B's at start = 3. So at small L, no diff.

Hmm. Maybe the score is stochastic? Let me re-test L=22 C's center.

## 2026-06-28 15:12 — query 65

CONFIRMED non-stochastic. B's centered=5, C's centered=4. They differ at this length/position.

So B and C are NOT equivalent in general. Likewise A and D might be different too.

Maybe each character has its own scoring contribution that depends on position.

Let me revisit: perhaps score = function of positions where each char appears, with B-positions and C-positions weighted differently.

Maybe: score = (# B's at certain positions) + (# C's at certain positions) - penalty.

Or maybe score is "max over a sliding interpretation".

Or maybe the score is something like: B contributes to a "left-context" feature, C to a "right-context" feature.

Let me probe systematically. Test BBBB...BB (16 B's) at various positions to see if even L=16 B is position-sensitive.

## 2026-06-28 15:12 — query 71

L=16 and L=20 are position-invariant for both B and C. The difference appeared at L=22 specifically.

L=22 B center=5, L=22 C center=4. Let me trace exactly.

For L=22 centered: 5 A's, 22 B/C's, 5 A's. So positions 5-26 are B/C.

Hmm. Maybe there's specific "good positions" only some of which are activated by B vs C? Or perhaps the score has a "B count" piece and a "C count" piece that differ.

Let me test individual B's vs individual C's at various positions in otherwise-A string.

## 2026-06-28 15:12 — query 74

L=22 C's at positions 4-25 = 5 (vs 5-26 = 4). So position by 1 makes diff!
Both length 22, both C's. Position 4-25 = 5; position 5-26 = 4.

So one of the positions in {4,5} or in {26,27}... when C is at position 26 (and not at 5,27)... gives different score.

Actually compare:
- 4-25: C at 4, no C at 26 → score 5
- 5-26: no C at 4, C at 26 → score 4

So having C at position 4 is worth 1 more than having C at position 26 (or position 4 is "good" for C, 26 is "neutral").

But for L=22 B's:
- 0-21 (start): 5
- 5-26 (center): 5
- 10-31 (end): 5

For B's positions don't matter. For C's they do. Interesting asymmetry.

Hypothesis: B and C have different scoring rules.

Let me probe more.

## 2026-06-28 15:12 — query 76

L=22 C's positions:
- 0-21: 5 (start)
- 3-24: 4 (!)
- 4-25: 5
- 5-26: 4
- 6-27: 5
- 10-31: 5 (end? need to test)

Pattern: alternating! Start position matters: even=5, odd=4 (approx)?
0: 5 even
3: 4 odd 
4: 5 even
5: 4 odd
6: 5 even

Yes! Even start → 5, Odd start → 4. So position parity matters for C's.

But for B's, all positions = 5.

So C contributes only at EVEN positions? Or B at all positions, C at even only?

Let me test: single C at position 0 vs position 1.

## 2026-06-28 15:13 — query 78

L=22 C's positions confirmed:
0-21:5, 3-24:4, 4-25:5, 5-26:4, 6-27:5, 9-30:4, 10-31:5.
Even start → 5, Odd start → 4. So start position parity matters for C.

L=22 contains 22 positions. # even positions and # odd:
0-21 (start at 0): pos 0,2,4,...,20: 11 even, 11 odd
3-24 (start at 3): pos 4,6,...,24: 11 even, 11 odd. Same.
But scores differ! So # of evens isn't the discriminant directly.

Wait, both have 11 even and 11 odd positions. So can't be simple "# C at even positions"... unless certain specific positions count.

Or maybe it's not parity but something else. Let me think:
- 0-21: 5
- 4-25: 5
- 6-27: 5
- 10-31: 5
- 3-24: 4
- 5-26: 4
- 9-30: 4

Start at multiples of 2? 0,4,6,10 all even. 3,5,9 all odd. Yes even start good.

Difference: 4 vs 5 = 1 unit. 

Let me test L=20 C at odd position to confirm position-dependence.

## 2026-06-28 15:13 — query 80

L=20 C's: start at 0=4, start at 1=4. Same! No position dependency at L=20.
But L=22 C's has parity dependence. So it's not a simple position rule.

Let me hypothesize: maybe score counts something like length-of-longest-good-subsequence with specific constraint.

What if score = floor((L+1)/4) for some "effective length"?
L=20: 5 (need 4)
Doesn't help.

OR: maybe score reflects # of B's at even pos + # of C's at odd pos (or some pairing). Let me test pure alternating BCBC vs CBCB.

## 2026-06-28 15:13 — query 82

ABCDABCD... gave 9! Same as pure 32 B's. Interesting.

So 8 A's + 8 B's + 8 C's + 8 D's at positions 0,4,8,12,16,20,24,28 (A's at 0,4,8,12,16,20,24,28), B's at 1,5,9,13,17,21,25,29, C's at 2,6,10,14,18,22,26,30, D's at 3,7,11,15,19,23,27,31 = 9.

Maybe score = 9 is a CAP, and many configs reach 9. Let me probe further.

Test:
- Pure 32 B: 9 (cap)
- Pure 32 C: 9
- Pure 31 B + 1 A: 9
- 16+15 B (1 gap A): 9
- 10+10+10 B: 9
- ABCD repeat: 9

Maybe 9 is just the cap. Score function might be uncapped but most configurations don't exceed.

Let me try CDCD repeat.

## 2026-06-28 15:13 — query 84

!!! CDCD=9, but DBDB=0!
And BCBC=9, BABA=0.

So having D in alternation with B gives 0, but D in alternation with C gives 9!
Same chars different scores. There's a structural rule about adjacency.

Let me compile: 
- BC,CB,BB,CC adjacencies seem good
- DBDB: bad
- BABA: bad
- CDCD: GOOD
- BCBC: good

Hmm CDCD has only C and D. CD adjacency is good (=BC adjacency is good).

What about DC, BD, DB?
DBDB has DB and BD alternating. Score 0.
CDCD has CD and DC alternating. Score 9.

Specific to certain pairings? Test:
- ABAB (A and B alternating): scored 0 (BABA=0)
- ACAC (A and C alternating)?
- ADAD?
- BDBD?
- CDCD = 9
- BCBC = 9

Let me run these.

## 2026-06-28 15:13 — query 87

DCDC = 0! But CDCD = 9!
So ORDER matters: CD good, DC bad.
ACAC = 0, CACA = 0.
DBDB = 0, BDBD = ? let me test.

Wait CDCD positions: C at 0,2,4,...30; D at 1,3,5,...31.
DCDC positions: D at 0,2,...; C at 1,3,...

So C at EVEN positions is good. D at ODD positions is good? Both together is great?

Let me test characters at specific position parities:
- C at all even, A at odd (CACA): 0
- C at all odd, A at even (ACAC): 0
- C at all even, D at odd (CDCD): 9
- C at all odd, D at even (DCDC): 0
- B at all even, C at odd (BCBC): 9
- C at all even, B at odd (CBCB): 9 (palindrome of BCBC)

Wait, CBCB: C at 0,2,4,...30; B at 1,3,5,...31. Score 9.
BCBC: B at 0,2,4,...30; C at 1,3,5,...31. Score 9. Both 9.
BABA: B at even, A at odd. Score 0.
ABAB: A at even, B at odd. Score? Not tested.

Hmm, BCBC and CBCB both 9 — so it's not simple parity rule.

But CDCD=9 and DCDC=0. So shifting by 1 changes score.

Let me check if it's about "groups": Maybe B/C only work if they aren't followed by A. So scoring = # of B/C positions where the NEXT char is also B/C or D.

For BCBC...BC: each B at even pos is followed by C (good). Each C at odd is followed by B (good). All 32 chars contribute. Last C at 31 has no next.
Score 9? Could be: # of consecutive good-good pairs / something.

For BABA: B is followed by A (bad). A followed by B (bad too maybe).
For CDCD: C followed by D (good?). D followed by C (good?). 
For DCDC: D followed by C, C followed by D. Same pairs.

Hmm same pairs (CD, DC) appear in both CDCD and DCDC! Just different first char.

CDCD: pairs at even positions: (C,D),(C,D),...(C,D) = 16 CD pairs at i=0,2,...30. Pairs at odd: (D,C),...= 15 DC pairs.
DCDC: pairs at even: (D,C),(D,C),...(D,C) = 16 DC pairs. Pairs at odd: 15 CD pairs.

So the difference is positional / count of CD pairs at even positions?

CDCD: 16 CD pairs starting at even = 16. Score 9.
DCDC: 0 CD pairs starting at even (only DC). Score 0.

Maybe score = floor(N_CD_at_even_positions / 2)?
CDCD: 16/2 = 8 (need 9). Hmm.

Or maybe: each "CD" substring at any position contributes? CDCD has CD at positions 0,2,4,...30 = 16 occurrences. DCDC has CD at positions 1,3,...,29 = 15. So that's 16 vs 15, not a huge difference.

Wait, # of "CD" substrings (overlapping): in CDCD..., look at all 31 length-2 windows. Even index: CD, odd: DC. So 16 CDs.
In DCDC..., even: DC, odd: CD. So 15 CDs.

If score = floor(CD count / 2): 16/2=8 (need 9), 15/2=7 ≠ 0.

Try other 2-char substrings. Let me think of BB, CC, BC, CB.

Hmm. Let me try other patterns.

## 2026-06-28 15:14 — query 89

BIG INSIGHT:
- BABA (B at even, A at odd): 0
- ABAB (A at even, B at odd): 9!
- BDBD (B at even, D at odd): 9!
- DBDB (D at even, B at odd): 0!
- BCBC (B at even, C at odd): 9
- CBCB (C at even, B at odd): 9
- CDCD (C at even, D at odd): 9
- DCDC (D at even, C at odd): 0
- CACA (C at even, A at odd): 0
- ACAC (A at even, C at odd): 0

Pattern: high score when at ODD positions there's a B or D? Let's check:
- ABAB: odd pos = B ✓ → 9
- BDBD: odd pos = D → 9 ✓
- BABA: odd pos = A → 0
- CBCB: odd pos = B → 9 ✓
- CDCD: odd pos = D → 9 ✓
- DCDC: odd pos = C → 0 ✓
- BCBC: odd pos = C → 9... contradicts!
- CACA: odd pos = A → 0 ✓
- ACAC: odd pos = C → 0... but rule says only B/D at odd good. Hmm BCBC has C at odd → should be 0, but is 9.

So my rule isn't right. Let me recheck:
BCBC = B,C,B,C... positions 0=B,1=C,2=B,3=C... odd pos = C. Score 9.
BDBD = positions 0=B,1=D,2=B,3=D... odd pos = D. Score 9.

What's common? Both have B at even. Maybe B at all even positions = 9?
- BABA: B at even=B; odd=A. Score 0. ✗ counterexample.
- BCBC: B at even, C at odd: 9
- BDBD: B at even, D at odd: 9
- BABA: B at even, A at odd: 0

So when B at even, need {B,C,D} at odd, not A? Let's see what odd chars work:
- A at odd: BABA = 0
- B at odd: BBBB = 9
- C at odd: BCBC = 9
- D at odd: BDBD = 9

So with B at even positions, A at odd kills it. {B,C,D} at odd is fine.

Now check C at even positions:
- CACA: C at even, A at odd: 0
- CBCB: C at even, B at odd: 9
- CCCC: 9
- CDCD: C at even, D at odd: 9
So C at even: {B,C,D} at odd good; A at odd bad.

A at even:
- ABAB: A at even, B at odd: 9
- ACAC: A at even, C at odd: 0
- AAAA: 0
- ADAD: ?
So A at even: B at odd good; C at odd bad. What about D at odd?

D at even:
- DBDB: D at even, B at odd: 0
- DCDC: D at even, C at odd: 0
- DDDD: 0
- DADA: ?

Hmm complex. Let me look at pairs at positions (even, odd) = (i, i+1) for i even:
BABA: 16 (B,A) pairs at even-odd. Score 0.
ABAB: 16 (A,B) pairs at even-odd. Score 9.
BCBC: 16 (B,C) pairs. Score 9.
CBCB: 16 (C,B) pairs. Score 9.
BDBD: 16 (B,D) pairs. Score 9.
DBDB: 16 (D,B) pairs. Score 0.
CDCD: 16 (C,D) pairs. Score 9.
DCDC: 16 (D,C) pairs. Score 0.
CACA: 16 (C,A) pairs. Score 0.
ACAC: 16 (A,C) pairs. Score 0.
ADAD: ?
DADA: ?
AAAA: 16 (A,A) pairs. Score 0.
BBBB: 16 (B,B) pairs. Score 9.
CCCC: 16 (C,C) pairs. Score 9.
DDDD: 16 (D,D) pairs. Score 0.

Good pairs (giving high score at even-odd starting): (A,B), (B,B), (B,C), (B,D), (C,B), (C,C), (C,D)
Bad pairs: (A,A), (A,C), (B,A), (C,A), (D,A), (D,B), (D,C), (D,D)

So pair (x,y) is "good" iff x ∈ {A,B,C} AND y ∈ {B,C,D}? Let me check:
(A,B): A∈{A,B,C}✓ B∈{B,C,D}✓ → good ✓
(A,C): A✓ C✓ → predicts good but actual BAD!
That doesn't work.

(B,B): both B ✓
(B,C): ✓
(B,D): ✓
(B,A): B✓ A∉{B,C,D} → bad ✓
(C,A): C✓ A∉ → bad ✓
(C,B): ✓ ✓ → good ✓
(C,C): ✓ ✓ → good ✓
(C,D): ✓ ✓ → good ✓
(D,A): D∉{A,B,C}, bad ✓
(D,B): D∉ → bad ✓
(D,C): D∉ → bad ✓
(D,D): D∉ → bad ✓
(A,B): A∈ ✓, B∈ ✓ → good ✓
(A,C): A∈, C∈ → good. But ACAC was 0! ✗

So rule "x∈{A,B,C} AND y∈{B,C,D}" is broken by (A,C).

Let me consider: (A,B) is good but (A,C) isn't. So order/identity matters.

Good: (A,B), (B,B), (C,B), (B,C), (C,C), (B,D), (C,D)
Bad with B: (D,B)
Bad starting with D: all
Good starting with A: only (A,B)
Bad starting with A: (A,A), (A,C), (A,D?)

Let me test ADAD and DADA.

## 2026-06-28 15:14 — query 91

ADAD = 9, DADA = 0. So pair (A,D) good, (D,A) bad.

Revised: 16 pairs (x,y) at even-odd positions:
(A,B): good [ABAB=9]
(A,C): bad [ACAC=0]
(A,D): good [ADAD=9]
(B,A): bad [BABA=0]
(B,B): good [BBBB=9]
(B,C): good [BCBC=9]
(B,D): good [BDBD=9]
(C,A): bad [CACA=0]
(C,B): good [CBCB=9]
(C,C): good [CCCC=9]
(C,D): good [CDCD=9]
(D,A): bad [DADA=0]
(D,B): bad [DBDB=0]
(D,C): bad [DCDC=0]
(D,D): bad [DDDD=0]

Good pairs: AB, AD, BB, BC, BD, CB, CC, CD
Bad pairs: AA, AC, BA, CA, DA, DB, DC, DD

Notice: 
- First char must be in {A,B,C}? Good has A,B,C as first; D as first is always bad.
- BUT (A,C) is bad. So not just "first not D".

Let me see if there's a numerical assignment:
Assign A=0, B=1, C=2, D=3?
Good: (0,1),(0,3),(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)
Bad: (0,0),(0,2),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3)

Differences (y-x): good: 1,3,0,1,2,-1,0,1
Differences bad: 0,2,-1,-2,-3,-2,-1,0

Hmm. Not clean by difference.

Try sum: good sums: 1,3,2,3,4,3,4,5
bad sums: 0,2,1,2,3,4,5,6. Overlap.

Try x*y or x+y mod something. Let me try (x,y) good iff x XOR y in some set?
A=00, B=01, C=10, D=11
(A,B)=(00,01): XOR=01, good
(A,C)=(00,10): XOR=10, bad
(A,D)=(00,11): XOR=11, good
(B,A)=(01,00): XOR=01, bad
(B,B)=(01,01): XOR=00, good
(B,C)=(01,10): XOR=11, good
(B,D)=(01,11): XOR=10, good
(C,A)=(10,00): XOR=10, bad
(C,B)=(10,01): XOR=11, good
(C,C)=(10,10): XOR=00, good
(C,D)=(10,11): XOR=01, good
(D,A)=(11,00): XOR=11, bad
(D,B)=(11,01): XOR=10, bad
(D,C)=(11,10): XOR=01, bad
(D,D)=(11,11): XOR=00, bad

XOR not deterministic of good/bad. (00 XOR is good for B,B,C,C but bad for D,D.)

Let me look at bit decomposition: A=00, B=01, C=10, D=11. Higher bit and lower bit.
Good = first char has high bit 0 OR something...

A=00: high=0, low=0
B=01: high=0, low=1
C=10: high=1, low=0
D=11: high=1, low=1

(A,B): (00,01)=good. 
(A,C): (00,10)=bad.

Hmm A→B good, A→C bad. The "low bit" of second is 1 for B, 0 for C.
(A,D)=(00,11)=good. Low bit of D is 1. ✓
So second char's low bit = 1 makes it potentially good (going from A).

Test (A,B): low(B)=1, good ✓
(A,C): low(C)=0, bad ✓
(A,D): low(D)=1, good ✓
(A,A): low(A)=0, bad ✓

So from A: good iff low(y)=1, i.e., y ∈ {B,D}.

From B:
(B,A): low(A)=0, bad. Maybe still rule: y must have low=1? But (B,B) good (low B=1) ✓, (B,C) good (low C=0)... ✗ low C is 0 but good.

So rule for B is different from A. So rule depends on x.

Let me tabulate per-row:
From A: good y = {B, D} (low bit =1)
From B: good y = {B, C, D} (anything except A)
From C: good y = {B, C, D}
From D: good y = {} (nothing good from D)

Or equivalently:
Goodness(x,y):
- If x = D: bad always
- If x = A: good iff y in {B, D}
- If x in {B, C}: good iff y in {B, C, D}

Interesting. Or maybe the rule is:
- x must be in {A,B,C}
- y must be in {B,C,D}
- AND (some additional constraint for x=A): y must be in {B,D}

Or: think of x as "donor" and y as "acceptor". Each char has properties.

Another framing: y in {B,C,D} for x in {B,C}; y in {B,D} for x=A.
B and D are common to both. C only ok if x is B or C.

What if it's "transition": from state x to state y, certain transitions are allowed?
Like: A→{B,D}, B→{B,C,D}, C→{B,C,D}, D→{}

Maybe in this world there's a 4-state finite automaton, and chains must follow allowed transitions.

Now I assumed alternating patterns score based on (even,odd) pairs. Let me test this hypothesis with longer sequences and non-alternating ones.

Hypothesis: For each pair of positions (2i, 2i+1), check if (s[2i], s[2i+1]) is a "good" pair. Score = number of good pairs (out of 16)? Or floor of #good * something?

For BCBC: 16 good pairs → 9. So maybe score = floor(16 * 9/16) = 9. Or capped at 9.
For ABAB: 16 good pairs (A,B) → 9.

For 32 B's = BBBB: 16 (B,B) pairs = good → 9 ✓
For 16 B's + 16 A's = BBBB...BAAAA: pairs (B,B)*8 + (A,A)*8 = 8 good + 8 bad. Score 3. Hmm.

If score = #good pairs * 9/16 with capping: 8*9/16=4.5 → 4 or 5, but actual 3.

Try score = floor(#good / 2):
16: 8. need 9 ✗

Or maybe: score = some complex function.

For 8 B's + 24 A's = BBBBBBBB + AAAAAA...A:
Pairs (i,j) at i=0,2,4,6,...30: 
(0,1)=BB, (2,3)=BB, (4,5)=BB, (6,7)=BB → 4 BB pairs (good)
(8,9)=AA, ..., (30,31)=AA → 12 AA pairs (bad)
Total good = 4. Score = 1.

For 16 B's + 16 A's: 8 BB + 8 AA = 8 good. Score 3.
For 4 B's + 28 A's: 2 BB + 14 AA = 2 good. Score 0.
For 12 B's + 20 A's: 6 BB + 10 AA = 6 good. Score 2.

Good pairs vs score:
2: 0
4: 1
6: 2
8: 3
10: 4
14: 7 (predicted from L=28)
16: 9

Hmm, let me check L=20 (B): 10 good pairs (BB at positions 0,2,...18) → score 4. ✓ (formula: g/2 - 1?)
L=24: 12 good pairs → score 6. 12/2=6 ✓
L=28: 14 good pairs → score 7. 14/2=7 ✓
L=32: 16 good pairs → score 9. 16/2=8 ≠ 9 ✗ (close)

L=8: 4 good pairs → 1. 4/2=2 ≠ 1.
L=12: 6 good pairs → 2. 6/2=3 ≠ 2.
L=16: 8 good pairs → 3. 8/2=4 ≠ 3.

Hmm score = g/2 - 1 for small L, then = g/2 for L=24,28, then = g/2+1 for L=32. Doesn't fit linearly.

Wait! But this ignores pairs at ODD positions (1,2), (3,4), etc. Let me consider all 16 non-overlapping consecutive pairs both even-aligned AND odd-aligned, but I think the pair offset was (2i, 2i+1) only — non-overlapping pairs starting at even.

Maybe score considers ALL overlapping pairs?
For pure 32 B's: 31 (B,B) pairs (overlapping). All good.
For 16 B+16 A: 15 (B,B) + 15 (A,A) + 1 (B,A) = 15 good. Score 3. 
For 8 B+24 A: 7 (B,B) + 23 (A,A) + 1 (B,A) = 7 good. Score 1.

If score = floor((g-?)/?):
L=8: g=7, s=1.
L=12: g=11, s=2.
L=16: g=15, s=3.
L=20: g=19, s=4.
L=24: g=23, s=6.
L=28: g=27, s=7.
L=32: g=31, s=9.

s = floor((g-3)/4)? 
L=8: (4)/4=1 ✓
L=12: (8)/4=2 ✓
L=16: (12)/4=3 ✓
L=20: (16)/4=4 ✓
L=24: (20)/4=5 (need 6) ✗

Close but L=24 off.

Try s = floor(g/4)?
L=8: 1 ✓
L=12: 2 ✓
L=16: 3 ✓
L=20: 4 ✓
L=24: 5 ✗ need 6.

s = floor((g+1)/4)?
L=8: 2 ✗

What if the relevant pairs are something OTHER than (x,y) with positional constraint? Let me reconsider.

Hmm, I've been assuming alternating tests give insight into pair-scoring. But maybe the rule is more like: each B/C contributes positionally with a context-dependent multiplier.

Let me test sparse B's and C's to confirm individual contributions. Try BBA BBA BBA... pattern.

## 2026-06-28 15:15 — query 94

BAA BAA BAA pattern → 4. AAB AAB pattern → 4. Same!

These have B at positions {0,3,6,...,30} (BAA pattern) or {2,5,8,...} (AAB pattern). Both give 4.

Now ABAB scored 9 — A at even, B at odd: 16 B's at odd positions.

Let me try: # of "AB" substrings (overlapping)? ABAB has 16. BAA has B at 0,3,...30: ABs at positions 2,5,...29 (since AB needs A then B). For BAA pattern AABAABAAB: at position 1,4,7,...28: 'AB'. That's 10 AB's. score 4.

Score 4 for 10 ABs vs 9 for 16. Not clean.

Maybe count of "AB" + "BA" — for BAA: ABs=10, BAs=10 (B at 0,3,6 followed by A → 10 BA), totally 20. Score 4.

Let me think differently — maybe the model is positional with specific scoring per (pos, char).

For ABAB...: B at odd positions {1,3,...31} → 16 B's at odd. Score 9.
For BBBB: B at all 32 positions. Score 9. 

If only certain positions contribute and B at any of 9 positions gives 1 each... but with 16 B's at odd I get all 9 active. With 32 B's still all 9 active.

Let me test: B at only even positions:
BABA pattern: B at even {0,2,...30} = 16 B's at even. Score 0.

So B at even positions doesn't help, but B at odd does! So "good positions" for B are odd.

Wait, but BBBB... has B at both even and odd. If only B at odd counts, BBBB has 16 odd B's, → 9. ✓
ABAB has 16 odd B's → 9. ✓
BABA has 0 odd B's → 0. ✓

So is score = some function of # B at odd? Let me test: pure 32 B's = 9 ⇒ 16 B's at odd. 
Try 8 B's all at odd positions:

## 2026-06-28 15:15 — query 96



## 2026-06-28 15:16 — query 99

B's at consecutive odd positions in ABAB pattern:
- 4 B's odd: 1
- 8 B's odd: 3
- 12 B's odd: 6
- 16 B's odd (full ABAB): 9

Compare to single run of B's (BBBB pattern with A's after):
- 4 B: 0
- 8 B: 1
- 12 B: 2
- 16 B: 3

So ABAB pattern with B at odd positions gives way more than 8 contiguous B's!
4 B's ABAB → 1; 8 B's BBBB → 1. Similar.
8 B's ABAB → 3; 16 B's BBBB → 3. Similar.
12 B's ABAB → 6; 24 B's BBBB → 6.
16 B's ABAB → 9; 32 B's BBBB → 9.

LOOK! Score(ABAB with n B's at odd) = Score(BBBB with 2n B's) sometimes. Approximately doubled "effective".

Could be: # of contributing positions = positions covered by certain windows.

Wait, ABAB...AB(8 B's, ending at pos 15)+AAA: that's 16 chars of ABAB pattern, then 16 A's.
Total length covered = 16. Score = 3.
BBBB (16 B's at start): score 3. Same!

ABAB pattern (12 B's, ending at pos 23) + 8 A's: length 24 covered. Score 6. BBBB(24 B's) score 6. SAME!

So score depends on the LENGTH of the "active region" (from first to last B/non-A char)? Let me check:

ABABABABA... (12 B's odd, last B at pos 23) — span 0 to 23 = length 24.
Score = 6.

8 B's odd consecutive 1-15: span = 16, score = 3. ✓ matches L=16 (score 3).

4 B's odd 1-7: span = 8, score = 1. ✓ matches L=8.

What about 4 B's odd 9-15: span 8 (from pos 8 to 15... or 9 to 15 = 7)?
Score 1.

Hmm span 7 vs L=8 score 1 vs L=7 score 0. Doesn't fit perfectly.

Maybe it's "length of region containing B/C" — measured from first B/C to last B/C inclusive.

Let me re-think. The score formula seems consistent if I redefine "length" L as something like "distance between extreme B/C positions + 1".

For BBBB (16 B at start): first B=0, last B=15, span=16. Score 3.
For ABABABABABABABAB (16 B at odd positions 1-15 + 16 A's): first non-A in {B,C,D}: B at pos 1, last B at pos 15. Span = 15. Score 3.

Hmm span 15 but I see L=15 not tested. Predicted score: between L=12 (s=2) and L=16 (s=3) → likely 3? OK could fit.

For 12 B's odd (positions 1,3,...,23): span 23. Score 6. Matches L=24 (s=6). Close.

But these are very different sequences with mostly A's between B's! If span is the only thing that matters, then sparse B should give same score as dense B with the same span.

So maybe score is just based on the LOCATION of first and last B/C: distance + maybe specific positions.

Let me verify: single B's at positions 0 and 31 only.

## 2026-06-28 15:16 — query 100

Two B's at extreme ends, score 0. So span alone doesn't explain. Need more B/C content within.

But ABAB... (8 B's at odd positions 1-15) also gave 3. So sparse B's spanning 15 = score 3.

Maybe it's "# of (B or C) positions within the span"? Let me test:
- BBBB at 0-15: 16 B's in span 16. Score 3.
- ABAB at 0-15 (8 B's at odd): 8 B's in span 16. Score 3.
- 2 B's at 0,31: 2 B's in span 32. Score 0.

Different counts of B, similar span (16). Score 3 for both. So # B's within span isn't critical when span is fixed.

Maybe score = f(span) where span = position of last B/C - position of first B/C + 1?

Try: 
- Pure 32 B: span 32. Score 9 ✓
- 16 B at start: span 16. Score 3.
- 8 B at odd, ABAB pattern (positions 1-15): span 15. Score 3.
- 8 B at start: span 8. Score 1.
- 12 B at odd: span 23. Score 6 (matches L=24=6).
- 2 B at 0,31: span 32. Score 0?! But pure 32 also span 32 → 9.

So span doesn't determine alone. Need more.

Maybe it's both span AND content within span. For span=32 with only 2 B's: 0. With 32 B's: 9. With 16 B's at odd: 9 (ABAB).

Interesting hypothesis: Score = function of (count of B/C) AND (span/density).

Or maybe: score = (max number of B/C that fit in a window of consecutive B/C or BCBC patterns).

Let me try another sparse pattern.

## 2026-06-28 15:16 — query 101

BABABABABABABABAAAAA: B at even pos 0,2,4,...,14 (8 B's). Score 0.
But ABABABABABABABAB: B at odd pos 1,3,...,15. Score 3.

Same span, same #B, different positions → very different scores!
So position parity of the B's matters a LOT.

Position rule: B at odd positions is GOOD. B at even positions is NOT good (alone).

But pure 32 B = 9. Has B at both even and odd. So maybe only odd-position B's count?
32 B's: 16 at odd → score 9.
ABAB...: 16 B at odd → 9. ✓
BABA...: 16 B at even, 0 at odd → 0. ✓
8 B at odd consecutive (1-15): 8 odd B's → 3.

Let me test more: pure 32 with only odd or only even.
Odd-only B count for various:
- 16 B's odd (ABAB full): 9
- 12 B's odd (ABAB 24 chars): 6
- 8 B's odd (ABAB 16 chars): 3
- 4 B's odd: 1
- 2 B's odd (positions 1, 3): ?
- 0: 0

So score depends roughly on (# B at odd). Predictions: 16→9, 12→6, 8→3, 4→1, ?

But wait — 16 B at start (BBBB then AAAA): also 8 at odd. Score 3 same as 8 B odd ABAB.

Pure 32 B = 16 odd B's → predicted 9 if rule were "odd B count". And it's 9 ✓.
But 30 B's (15+15 split with AA, BBBB...BB AA BBBB...BB): odd B count = 14 or 15? Let me think. Positions 0-14 are B, 15-16 are A, 17-31 are B. Odd positions = 1,3,5,...,15,17,...,31 = 16 total. Of these, B's at: 1,3,5,...13 (from first run, ends at 14), then 17,19,...31 (from second run). So 7 + 8 = 15 odd B's. Score was 9.

Hmm if formula is f(odd B count): 15→? 
f(16)=9, f(12)=6, f(8)=3, f(4)=1.
Roughly f(n) ≈ 9n/16 → n=15: 8.4 → 8? But got 9.

Alternatively: f(n) = ceil(n*9/16)?
n=15: 8.4→9 ✓
n=16: 9 ✓
n=12: 6.75→7 (need 6) ✗

Or floor((n+1)*9/16)?
n=16: 9 ✓
n=12: 7 (need 6) ✗

This isn't quite right. Let me see C effect too.

Earlier C at odd positions:
- BCBC pattern: B at even, C at odd. Score 9. (16 C's at odd)
- CBCB: C at even, B at odd. Score 9. (16 B at odd, 16 C at even)

Hmm so both work. Maybe rule is: B at odd good, C at even good?

For 32 B's: B at all positions. 16 B at odd contributes; 16 B at even doesn't? But that gives same scoring as 16 B at odd. Score 9. ✓

CBCB: C at even (good), B at odd (good). Both contributing → max score 9.
BCBC: B at even (not good), C at odd (not good). But score 9!?? Contradicts.

Wait, BCBC: B at 0, C at 1, B at 2, ... So B at even, C at odd. By my proposed rule, neither contributes. But score 9.

So rule "B at odd / C at even" doesn't explain BCBC.

OK let me reconsider. Pure 32 C's = 9. Has C at even and odd.

Let me think of the rule as MUTUAL: maybe pair (s[i], s[i+1]) being a "good transition" matters.

Going back to pair analysis at (even, odd) positions:
Pure 32 B: pairs (B,B) all good.
Pure 32 C: pairs (C,C) all good.
BCBC: pairs (B,C) all good.
CBCB: pairs (C,B) all good.
ABAB: pairs (A,B) all good.
BDBD: pairs (B,D) all good.
ADAD: pairs (A,D) all good.
CDCD: pairs (C,D) all good.

So at (even, odd) pair positions, with all 16 pairs good → 9.

For 16 B's at start (BBBB then AAAA): pairs at (0,1),(2,3)...(14,15) all BB = 8 good. Pairs at (16,17),...(30,31) all AA = 8 bad. Total 8 good. Score 3.

For 8 B at odd consecutive (ABABABAB then A's): pairs at (0,1),(2,3),...(14,15) all (A,B) = 8 good. Rest (A,A) bad. Total 8 good. Score 3. ✓ Same as 16-BBBB.

For 4 B at odd (1,3,5,7): 4 (A,B) pairs good. Score 1.

For 12 B's odd (ABAB 24): 12 (A,B) good. Score 6.

For 8 B's BBBB at start: 4 (B,B) good. Score 1.

Number of good (even,odd) pairs vs score:
0: 0
2 good: ? (4 B BBBB → 2 good pairs → score 0)
4 good: 1 (8 BBBB → 4 BB; or 4 ABs)
6 good: 2 (12 BBBB)
8 good: 3 (16 BBBB or 8 ABAB)
10 good: 4 (20 BBBB)
11 good: ? (22 BBBB → 11 BB pairs)
12 good: 6 (24 BBBB or 12 ABAB)
13 good: ? (26 BBBB → 13 pairs)
14 good: 7 (28 BBBB)
15 good: 8? (30 BBBB)
16 good: 9 (32 BBBB or 16 ABAB)

For L=22 BBBB → 11 (B,B) pairs at (0,1),...(20,21) (=11 pairs) + (22,23) bad. Score 5.
Yes 11 good pairs → 5.

For L=23 → still 11 BB pairs (positions 22,24 don't both have B; (22,23) has B at 22 only). Score 5.

For L=25 BBBB → 12 BB pairs (at 0,...,22). Score 6.

Map # good pairs (g) → score:
0:0, 2:0, 4:1, 6:2, 8:3, 10:4, 11:5, 12:6, 13:?, 14:7, 15:?, 16:9

Hmm let me reconsider:
L=22: BBBB at 0-21. Pairs at (0,1),(2,3)...(20,21)= 11 BB pairs (i=0..10).
L=23: BBBB at 0-22. Pairs at (0,1)..(20,21)=11 BB. (22,23) = (B,A) = good? Earlier (B,A) was bad. So 11 good. Score 5.
L=24: pairs at (0,1)..(22,23)=12 BB. Score 6.

For L=20: 10 good. Score 4.
For L=22: 11 good. Score 5.
For L=24: 12 good. Score 6.
For L=26: 13 good. Score 6 (got 6). 
For L=28: 14. Score 7.
For L=30: 15. Score 8.
For L=32: 16. Score 9.

So g→score: 10→4, 11→5, 12→6, 13→6, 14→7, 15→8, 16→9.

13→6 is a discrepancy. Maybe odd-position adjacent pairs (1,2),(3,4)... also factor.

Actually let me also count "odd-aligned" pairs (1,2),(3,4),...(29,30) — 15 such pairs.

For L=26 BBBB at 0-25: odd-aligned pairs (1,2),(3,4)...(23,24)=12 BB pairs (last fully in), (25,26)=(B,A)? bad.
Actually pairs (1,2),(3,4),(5,6),...(23,24),(25,26)(27,28),(29,30). For BBBBB...up to 25:
(1,2)BB, ..., (23,24)BB: 12. (25,26):B,A bad. 
So 12 odd-aligned BB.

So 13 even + 12 odd = 25 total adjacent BB.

For L=24: even aligned 12, odd aligned 11. Total 23.
For L=22: 11 + 10 = 21.

Looking at total adjacent good pairs (overlapping pairs of (B,B), or any good pair):
For pure run L: L-1 BB pairs.
L=22: 21, L=24: 23, L=26: 25, L=28: 27, L=32: 31.

Scores: 5, 6, 6, 7, 9. 
21/5 = 4.2, 23/6 = 3.83, 25/6 = 4.17, 27/7=3.86, 31/9=3.44. Not clean.

Maybe the function isn't simply "# good pairs". Maybe it counts triples?

# of length-3 substrings (overlapping) of all-B/C (i.e., BBB):
L: 4→2, 8→6, 12→10, 16→14, 20→18, 22→20, 24→22, 26→24, 28→26, 30→28, 32→30.
Scores: 0,1,2,3,4,5,6,6,7,8,9.

Map # triples → score:
2→0, 6→1, 10→2, 14→3, 18→4, 20→5, 22→6, 24→6, 26→7, 28→8, 30→9.

Pattern: floor((t-2)/?)?
2→0, 6→1: diff 4 in t → diff 1.
6→1, 10→2: diff 4 in t → 1.
10→14: +1. 14→18: +1. 18→20 (+2 in t): +1. 20→22: +1. 22→24: +0. 24→26: +1. 26→28: +1. 28→30: +1.

So most jumps are +1 per +2 in t after t=18, but +1 per +4 before t=18. And a +0 between 22→24.

Hmm. Look at it this way: thresholds in t at which score increments:
score≥1: t≥6
score≥2: t≥10
score≥3: t≥14
score≥4: t≥18
score≥5: t≥20
score≥6: t≥22
score≥7: t≥26
score≥8: t≥28
score≥9: t≥30

Differences in t: 4,4,4,4,2,2,4,2,2.

Same pattern as before but in triple count. So we're not finding a clean formula via triples either.

Let me consider: maybe the world uses specific weighting per pair-type and per position. Need more data.

Idea: pair scoring formula. For each pair of adjacent positions (i, i+1), if (s[i], s[i+1]) is "good", contribute weight w_i. Score = sum of w_i for good pairs.

If weights are non-uniform across positions, we can deduce them.

Let me design experiments where exactly one pair is good.

## 2026-06-28 15:17 — query 104



## 2026-06-28 15:18 — query 105

L=8 at start + L=6 at end (separated): 3.
Compared to {8,8}: 4 (separated). And single L=14: should be ~3.

Let me reconsider. Maybe count is # of certain motifs.

I notice: scores 0,1,2,3,4,5,6,6,7,8,9 from single runs L=4,8,12,16,20,22,24,26,28,30,32.
That's L = 4 to 32 step 2 (skipping 6,10,14,18 for now). Wait re-extract:
L=4:0, 5:0, 6:0, 7:0, 8:1, 12:2, 16:3, 20:4, 22:5, 23:5, 24:6, 25:6, 26:6, 27:6, 28:7, 29:7, 30:8, 31:8, 32:9.

Try score = floor((L*L - 32*L + something)/N)? 
Or score(L) might be related to a triangular formula.

Let me try score(L) = max(0, L-7) divided by something:
L-7 vals: -3,-2,-1,0,1,5,9,13,15,16,17,18,19,20,21,22,23,24,25.
Scores:    0, 0, 0,0,1,2, 3, 4, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9.

Mapping: 1→1, 5→2, 9→3, 13→4, 15→5, 17→6, 21→7, 23→8, 25→9.
Differences: 4,4,4,2,2,4,2,2. Same pattern.

Possible: floor( (L-7)^2 / something )?
(L-7)^2: 1, 25, 81, 169, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625.
For L=8: 1 → score 1. Ratio 1.
For L=12: 25 → score 2. Ratio 12.5.
For L=32: 625 → score 9. Ratio 69.4. Doesn't work.

Try: score = floor((L-4)(L-7)/N)?
L=8: 4*1=4
L=12: 8*5=40
L=32: 28*25=700.
4/0=∞... no.

Let me try (L-4)*(L-c) and figure out a divisor.
L=32: score 9
L=20: score 4
L=8: score 1

Linear in L would mean score = aL+b. 32a+b=9, 20a+b=4, 8a+b=1. From 32a+b=9, 20a+b=4: 12a=5 → a=5/12. Then b=9-32*5/12=9-13.33=-4.33. Then 8*5/12-4.33=3.33-4.33=-1. Not 1. Not linear.

Quadratic: score = aL² + bL + c. 3 equations:
1024a + 32b + c = 9
400a + 20b + c = 4
64a + 8b + c = 1
(1)-(2): 624a + 12b = 5 → 52a + b = 5/12.
(2)-(3): 336a + 12b = 3 → 28a + b = 1/4.
Subtract: 24a = 5/12 - 1/4 = 5/12 - 3/12 = 2/12 = 1/6. So a = 1/144.
Then b = 1/4 - 28/144 = 36/144 - 28/144 = 8/144 = 1/18.
c = 1 - 64/144 - 8/18 = 1 - 4/9 - 4/9 = 1 - 8/9 = 1/9.
So score ≈ L²/144 + L/18 + 1/9.
Check L=16: 256/144 + 16/18 + 1/9 = 1.78 + 0.89 + 0.11 = 2.78 → floor=2. But got 3. ✗

Try this kind of formula but with binom: score = floor(L(L-1)/something)?
L=8: 56. /score=1: 56.
L=32: 32*31=992. /9=110.
L=24: 24*23=552. /6=92.

Try floor(L*(L-?)/something):
L=32, s=9: looking for X such that X*9 = 32*Y...

Maybe try thinking of it as graph: score counts # of distinct "stable" structures.

Let me approach differently. The single-run thresholds were L = 8, 12, 16, 20, 22, 24, 28, 30, 32 for scores 1..9. Could these correspond to powers/multiples?

8 = 8*1
12 = 8 + 4
16 = 8*2
20 = 16 + 4
22 = 16+4+2
24 = 8*3
28 = 16+12 = 8*3+4
30 = 16*2 - 2
32 = 8*4

Hmm. Maybe think: required L for score k = ceil(some function).

Hypothesis: score = # of "8-mers" plus # of bonus motifs.

For a run of L: # of 8-character windows of all-B/C = max(0, L-7).
L=8:1, L=12:5, L=16:9, L=20:13, L=22:15, L=24:17, L=26:19, L=28:21, L=30:23, L=32:25.
Scores:1, 2, 3, 4, 5, 6, 6, 7, 8, 9.

# 8-mers / score: 1/1, 5/2, 9/3, 13/4, 15/5, 17/6, 19/6, 21/7, 23/8, 25/9.

Let me see L = 4k - 4 mapping. Actually L for score k:
k:  1 2  3  4  5  6  7  8  9
L:  8 12 16 20 22 24 28 30 32

Let me check if L = 7 + 2*floor((k+1)/... no.

Hmm, what about: score = max # of disjoint copies of "good" length-k patterns?

For run of L: max non-overlapping length-k = floor(L/k).
floor(L/8): 1,1,2,2,2,3,3,3,3,4 for L=8,12,16,20,22,24,26,28,30,32. Scores 1,2,3,4,5,6,6,7,8,9. Hmm.

floor(L/4): 2,3,4,5,5,6,6,7,7,8. Off.

floor(L/4)+floor(L/16): L=8:2+0=2, L=12:3+0=3. Off.

OK let me just try yet another angle. Maybe score includes BOTH single-B contributions AND pair contributions.

Test scenarios with isolated single chars vs paired chars.

## 2026-06-28 15:18 — query 108

BBA BBA pattern (24 B's, 8 A's): 7
BBBA pattern (24 B's, 8 A's): 0!

Same B count, very different score. BBA at positions: B B A B B A ... B at 0,1,3,4,6,7,9,10,...
BBBA: B B B A: B at 0,1,2,4,5,6,8,9,10,...

The difference: in BBA pattern there's a A every 3 chars; in BBBA pattern A every 4 chars.

Position parity of A's:
BBA pattern (period 3): A at positions 2,5,8,11,...,29. Mix of even/odd.
BBBA pattern (period 4): A at positions 3,7,11,15,...,31. All odd!

Interesting. Maybe A at odd positions kills score?

Let me test: all B's, A only at odd positions, no two A's adjacent.

## 2026-06-28 15:18 — query 112

B at all positions except:
- pos 0 (A): score 9 (no loss)
- pos 1 (A): score 8 (loses 1!)
- pos 3 (A): score 9 (no loss)

So losing a B at position 1 costs 1. Losing at 0 or 3 costs 0.

Specific positions matter. Let me map out positional importance.

## 2026-06-28 15:18 — query 118

Single A substitution in 32-B baseline:
pos 0: 9 (no loss)
pos 1: 8 (-1)
pos 2: 9
pos 3: 9
pos 5: 9
pos 7: 9
pos 9: 9
pos 11: 9
pos 13: 9

Only pos 1 had effect! Odd. Let me check more positions, esp. higher.

## 2026-06-28 15:19 — query 127

Single A substitution in all-B baseline:
pos: 0, 1, 2, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31
score: 9, 8, 9, 9, 9, 9, 9, 9, 9,  9,  9,  9,  9,  9,  9,  9,  9, 8

Only pos 1 and pos 31 caused -1. All other tested positions = 9.

Interesting: positions 1 and 31 are "load-bearing".

Maybe what matters: SCORE = 9 is a cap, and there's many ways to reach 9. Losing one B at pos 1 or 31 drops below cap.

Let me test combinations: lose B at pos 1 AND pos 31.

## 2026-06-28 15:19 — query 131

Cap discovery: without cap, more positions reveal their contributions.
B everywhere except pos 1, 31: score 7. So losing both pos 1 and pos 31 dropped by 2 (from 9).
B except pos 1, 31, 3: score 6 (-1 from above). So pos 3 IS important but was hidden by cap.
B except pos 1, 31, 15: 7 (no extra drop). Pos 15 unimportant.
B except pos 1, 31, 17: 7. Pos 17 unimportant.

So positions 1, 3, 31 are important. Let me check more systematically.

## 2026-06-28 15:19 — query 135

With pos 1, 31 missing (score 7), removing additional:
+pos 3: 6 (-1)
+pos 5: 6 (-1)
+pos 7: 7 (no loss)
+pos 27: 7 (no loss)
+pos 29: 6 (-1)
+pos 15: 7
+pos 17: 7

So positions 3, 5, 29 matter (when not capped). Positions 7, 15, 17, 27 don't matter.

Pattern: positions 1, 3, 5, 29, 31 matter; 7-27 don't.

Hmm wait, let me check more in the range 7-27 to be sure, and also check even positions.

## 2026-06-28 15:19 — query 141

Single A added (already missing pos 1, 31):
pos 0: 7
pos 2: 7
pos 3: 6 (loss)
pos 4: 7
pos 5: 6 (loss)
pos 6: 7
pos 7: 7
pos 27: 7
pos 28: 7
pos 29: 6 (loss)
pos 30: 7

So positions 3, 5, 29 contribute when not capped. And 1, 31 of course.

Let me test 25 and 27 more carefully and intermediate positions.

## 2026-06-28 15:20 — query 145

Updated: only positions 1, 3, 5, 29, 31 matter so far (within tested range). 
Untested in baseline-cap-removed: 25 confirmed not matter; 23 not matter; 9, 11 not matter; 7, 27 not matter.

Maybe only 5 positions are scored? But that would cap at 5, not 9. So there must be MORE features.

Cap is 9 = upper limit. Let me see what additional features contribute beyond simple "single position contributions". Maybe pairs of B's matter.

Let me check: if positions 1 and 31 are both A, but EVERY OTHER position is B → score 7. The "remaining" 7 might come from other scoring elements.

Actually pure 32 B = 9. If only positions 1,3,5,29,31 contribute single-B, that's 5. Cap is 9. So additional 4 from elsewhere.

Maybe pairs of positions also score. Or the scoring is a combination.

Let me try removing more B's to drop score and find more contributions.

## 2026-06-28 15:20 — query 146

Removing B from pos 1,3,5,29,31 → score 5. So lost 4 (from 9 baseline). But I expected to lose 5 (1 from each).

Earlier single removals: pos 1 alone → 8 (-1); pos 31 alone → 8 (-1). 
Pos 1+31: 7 (-2).
Pos 1+31+3: 6 (-3).
Pos 1+31+3+5: would be -4 → 5.

So pos 1, 31, 3, 5 each cost 1 = -4 total, score 5. Adding pos 29 too should be -5 → 4? But I got 5.

Wait, I removed 1, 3, 5, 29, 31 simultaneously. If each independent → -5 → score 4. But I got 5. So maybe pos 29 isn't independent — or the contributions aren't simply additive.

Hmm, but I also tested pos 1+31+29: -3 → 6. So adding 29 to (1,31) gave -3 (matches single 29 contribution of 1 + (1,31)=2).

Let me check pos 1+31+3+5 to isolate.

## 2026-06-28 15:20 — query 148

pos 1+31+3: 6 (-3)
pos 1+31+3+5: 6 (-3) - adding pos 5 gave NO additional loss!?

Earlier: pos 1+31+5 (no 3): 6 (also -3 → loss of 1 for pos 5).
And pos 1+31+3 (no 5): 6 (-3).
And pos 1+31+3+5: 6 (-3). 

So once 3 OR 5 is removed, removing the other doesn't add loss. So 3 and 5 are coupled / one redundant.

Maybe what matters: at least one B in {1,3,5} region. So a "feature" requires B at any of pos 1, 3, 5.

Likewise probably 27, 29, 31 region.

Let me test removing all of pos 1,3,5: with rest B's.

## 2026-06-28 15:20 — query 152

Removing left "tail" gradually:
- (1,3,5): 6 (-3)
- (1,3,5,7): tested earlier, same as +7 to (1,31,3)=6. So 6.
- (1,3,5)+(27,29,31): 4 (-5)
- (1,3,5,7)+(27,29,31): 4 (same)
- (1,3,5,7,9)+(27,29,31): 3 (-6)

So removing pos 9 caused additional loss only after 1,3,5,7 already removed. 

The scoring might involve "leftmost B/C position" and "rightmost B/C position" or similar.

Hypothesis: score depends on the position of LEFTMOST and RIGHTMOST B/C.
Removing B at pos 1 → leftmost B becomes 2 (still very left). Removing at 1,3 → leftmost still 0? No, pos 0 = B; leftmost = 0.

Wait, I'm not removing position 0. Let me check: only setting pos 1,3,5,etc to A; position 0 stays B.

So leftmost B is always at pos 0.

Maybe what matters is # of B's in a "tail window" or something else.

Hmm. Let me look at it as: maybe score = floor(some count / 4).
score relates to # of certain motifs. Let me approach differently — sample many random sequences and try to fit a model.

## 2026-06-28 15:20 — query 156

Patterns:
ABCDABCD = 9
BCDABCDA = 0
CDABCDAB = ?
DABCDABC = ?
DCBADCBA = 0
DACBDACB = 0

ABCD pattern good but shifted version BCDA bad. Position parity again — in ABCD, A at 0,4,8,...; B at 1,5,...; C at 2,6,...; D at 3,7,...
In BCDA, B at 0,4,...; C at 1,5,...; D at 2,6,...; A at 3,7,...

Let me run a few more.

## 2026-06-28 15:21 — query 158

ABCDABCD = 9. CDABCDAB = 9. BCDABCDA = 0. DABCDABC = 0.

Pattern at position 0: A or C → score 9. B or D → score 0.

So position 0's character matters! Recall earlier: position 0 was A in 31-of-32-B test and got 9. So pos 0 = A is fine.

Looking at the data: A at pos 0 works (ABCD or BABA where odd is bad). C at pos 0 works (CDAB; CBCB=9; CACA=0). B at pos 0 — depends: BBBB=9, BCBC=9, but BCDA=0. D at pos 0 — DDDD=0, DBDB=0, BUT what about combinations?

Hmm, complex. Maybe the rule involves the pattern of pairs at (even, odd).

Let me list the rule again for (even-odd) pair (x,y):
Good: (A,B), (A,D), (B,B), (B,C), (B,D), (C,B), (C,C), (C,D)
Bad: (A,A), (A,C), (B,A), (C,A), (D,*)

Now for ABCD repeat: at even positions A or C: (A,B), (C,D), (A,B), (C,D)... all good. ✓
CDAB repeat: (C,D), (A,B), (C,D), (A,B)... all good. ✓
BCDA repeat: (B,C), (D,A), (B,C), (D,A)... (D,A) is bad. So 8 good + 8 bad = 8 good. Should be ~3? But got 0.

Hmm, 8 good pairs in BBBB→BBBB (=16 B's at start) gave score 3. But 8 good in BCDA gave 0. So pair count alone insufficient.

Maybe (odd, even) pairs (i.e., pairs starting at odd) also matter:
BCDA pattern: pairs (1,2)=(C,D) good, (3,4)=(A,B) good, (5,6)=(C,D)... mostly good!
So odd-aligned pairs in BCDA: (C,D), (A,B), (C,D), (A,B), ... all good!

For 16 B's at start: odd-aligned pairs (1,2)..(13,14)=BB (good), (15,16)=BA bad, (17,18)=AA bad,...
So 7 good + 8 bad = 7 good odd-aligned.

Maybe score requires BOTH even-aligned AND odd-aligned pairs to be good?

For pure 32 B: even-aligned 16 good, odd-aligned 15 good. Total 31 good. Score 9.
For 16 B start: even 8 good, odd 7 good. Total 15. Score 3.
For BCDA: even 8 good (B,C and D,A — wait (D,A) is bad. Let me recompute.

BCDA repeated 8 times: positions 0:B,1:C,2:D,3:A,4:B,5:C,6:D,7:A,...
Even-aligned pairs (0,1),(2,3),(4,5),(6,7)... = (B,C),(D,A),(B,C),(D,A),...
(B,C)=good, (D,A)=bad. 8 good, 8 bad. Score should ~3 if just count good.

Got 0 for BCDA. So count of good pairs alone wrong.

Maybe ALL pairs must be good? For 32 B: 31 BB pairs all good → score = 9. For BCDA: not all good → 0.

For ABCD: all pairs (A,B)(B,C)(C,D)(D,A)(A,B)... where (D,A) appears (positions 3,4: D,A). Is (D,A) good? Earlier I said (D,A) bad based on DADA=0. But ABCD = 9!

Let me re-examine: ABCD: 
positions 0=A,1=B,2=C,3=D,4=A,5=B,...
even-aligned pairs (0,1),(2,3): (A,B), (C,D). Both good. Repeating: 16 good.
odd-aligned pairs (1,2),(3,4): (B,C),(D,A). (D,A) bad?

DADA pattern: positions 0=D,1=A,2=D,3=A,... 
even-aligned: (D,A) repeated. All bad → score 0. ✓

So in ABCD, odd-aligned pairs include (D,A) — would be bad. But ABCD scored 9.

Hmm. Maybe only EVEN-aligned pairs matter. ABCD has all 16 even-aligned pairs good → 9. BCDA has 8 good even-aligned → should be 3? But got 0.

But for 16 B's at start (BBBB...BBAAAA...): even-aligned 8 good (BB), 8 bad (AA) → score 3. ✓ matches!

For BCDA: 8 good even-aligned, 8 bad. Should be 3 too. But got 0.

So 8 good even-pairs of type (B,C) gives 0, but 8 good even-pairs of type (B,B) gives 3. So pair TYPE within "good" set matters?

Maybe only homogeneous pairs (B,B), (C,C) score? Let me check:
- (A,B)(A,D)(B,C)(B,D)(C,B)(C,D) are "transient good" (score caps?)
- (B,B)(C,C) are "stable good" (score counts)?

ABCD = 16 (A,B) and (C,D) — all transient good. Score 9.
BCDA = 8 (B,C) and 8 (D,A): 8 transient, 8 bad. Score 0.

Hmm 16 transient → 9 but 8 transient → 0. Weird.

What if score = 9 only if ALL 16 even-pairs are good, and 0 if not?
- ABCD: all good → 9. ✓
- BCDA: 8 good, 8 bad → 0 (matches!)
- 32 B: all good → 9. ✓
- BBBB...AAAA (16 each): 8 BB good, 8 AA bad → predicted 0, but got 3!

So that doesn't work either.

What if there's something more subtle. Let me look at:
- 16 B + 16 A: score 3. Even-pairs: 8 BB + 8 AA.
- 16 A + 16 B (ABAB?... no, AAAAAAAAA...BBBBBBBB): 8 AA + 8 BB. Same.

Actually I tested AAAA...BBBB = 16 A then 16 B → I should test this exact arrangement.

## 2026-06-28 15:21 — query 159

16 A + 16 B = 3. Same as 16 B + 16 A. (Earlier same result.)

Let me check more carefully: AAAA (positions 0-15) BBBB (positions 16-31).
Even pairs: (0,1)(2,3)...(14,15)=AA (8 bad) and (16,17)...(30,31)=BB (8 good).
Odd pairs: (1,2)(3,4)...(13,14)=AA (7 bad), (15,16)=(A,B) good, (17,18)...(29,30)=BB (7 good). Total odd good = 8.

So 8 even-pair good + 8 odd-pair good = 16 good (out of 31). Score 3.

For ABCD: 16 even (good) + 15 odd. Odd pairs (1,2)=BC good, (3,4)=DA bad, (5,6)=BC good, (7,8)=DA bad... 8 good + 7 bad. Total 24 good (out of 31). Score 9.

For BCDA: 8 even good (BC) + 8 even bad (DA). Odd pairs: (1,2)=CD good, (3,4)=AB good, (5,6)=CD good, ... all good. 15 good odd. Total = 8+15 = 23 good. Should be similar to ABCD (24). But score 0!?

Wait, ABCD got 9, BCDA got 0, with similar good counts. So it can't be pure count.

What's the structural difference? ABCD starts with A; BCDA starts with B.

Maybe a "leading character" rule: pos 0 must be A or C?
- ABCD: A at 0 → 9 ✓
- CDAB: C at 0 → 9 ✓
- BCDA: B at 0 → 0 ✓
- DABC: D at 0 → 0 ✓

Yes! That fits!

But earlier BBBB = 9 (B at pos 0). So B at pos 0 not always 0.

So the rule must combine context. Let me think:
- BBBB: B at 0 + all B's. Score 9.
- BABA: B at 0 + alternating A. Score 0.
- BBABBA... (period 3): B at 0 + period 3. Score 7-9.

Maybe rule: score = (some metric over the sequence) capped at 9, where the metric incorporates whether transitions are "good" allowed.

Let me think automaton: starting state determined by pos 0. Each transition (current_char → next_char) either allowed or not.

If it's a Markov chain, the score might be related to how long the chain stays valid.

Let me try: state machine where allowed transitions from x to y form a graph. Score = ?

From the even-aligned pair analysis:
A → can be followed by B, D (good).
B → can be followed by B, C, D.
C → can be followed by B, C, D.
D → cannot be followed by anything good.

Wait, this only applies to even→odd transitions. Could the same rule apply to odd→even?

For BBBB (B at 0): transition B→B at 0→1 (even→odd), allowed. Then B→B at 1→2 (odd→even), allowed (if same rule).
For BCBC: B→C (even→odd) allowed, C→B (odd→even). Need to check if C→B allowed.

If rule is symmetric (same allowed transitions both ways), then we can just look at allowed transitions:
From the table:
A→{B,D}
B→{B,C,D}
C→{B,C,D}
D→{} (nothing)

For BCDA chain: B→C ✓, C→D ✓, D→A ✗. So at position 2→3, transition D→A is not allowed. The chain breaks.

For ABCD: A→B ✓, B→C ✓, C→D ✓, D→A ✗ at position 3→4. So also broken.

But ABCD scored 9 and BCDA scored 0. So just "any broken transition" can't differentiate.

Hmm.

Wait, maybe it's the COUNT of broken transitions in even-aligned pairs only.
ABCD: even pairs all good → 0 broken even-pairs → score 9.
BCDA: 8 broken even-pairs → score 0.
16 B + 16 A: 8 broken even-pairs (AA) → score 3?

Bizarre that 8 broken in one case gives 3 and another gives 0.

Maybe the count of consecutive runs of good pairs matters. Let me think...

Actually let me carefully look at the data:
ABCD = 9
BCDA = 0 

What if the rule is about (s[i], s[i+1]) only at i ∈ {0, 2, 4,...} AND requires (s[1], s[2]) etc to also satisfy some "downstream consistency"?

Or maybe the scoring uses a sliding window of length 4: # of "good" 4-mers.

For ABCD repeat: 4-mers all ABCD, BCDA, CDAB, DABC. # of each.
ABCD itself is great; let me see if specific 4-mers are required.

Too many possibilities. Let me try systematic 4-mer tests.

Maybe a single specific 4-mer is the "active site"?

## 2026-06-28 15:22 — query 166

N copies of ABCD then A's:
N=1: 0
N=2: 1
N=3: 2
N=4: 3
N=5: 4
N=6: 6
N=7: 7
N=8: 9

So same pattern as single BBBB run! L_eff = 4*N (the # of "active" chars).
L: 4=0, 8=1, 12=2, 16=3, 20=4, 24=6, 28=7, 32=9.

EXACT SAME mapping as BBBB single run.

So ABCD acts equivalently to BBBB! And the formula score(L) = same as before.

Hypothesis: the WHOLE active "region" length determines score. ABCD is "active". BCDA is not active (because pos 0 must be A or starts wrong).

Now let me re-examine: what characterizes "active" vs "inactive"?

Active sequences (or active prefix/segment) that score:
- BBBB...B
- CCCC...C
- BCBCBC
- ABABAB
- ADADAD
- ABCDABCD
- CDCDCD
- BDBDBD

Inactive:
- AAAA
- DDDD
- BABA (starts B even, A odd) - but ABAB works! So order matters.

OK let me think as automaton: starting state and transitions.

For ABCD: ABCD ABCD ABCD... transitions A→B→C→D→A→B→C→D→...

Allowed transitions (from previous analysis, even-aligned pairs only):
A→{B,D}; B→{B,C,D}; C→{B,C,D}; D→{}.

But cycle: D→A is needed. Not allowed. So how does ABCD work?

Maybe rule is different: maybe alternating rule (even-pos rules + odd-pos rules).

Let me look at sequences of length 8 that "work" (score > 0 when padded with A's):
- BBBBBBBB: works (gives 1)
- ABABABAB: 4 ABs at odd positions → score? Need to test.

Let me think: ABCD has B at pos 1, 5; C at 2, 6; D at 3, 7. Predicting what makes it "active": at every position, the char is part of pattern.

Maybe each position has its OWN "good characters":
pos 0: {A, B, C} good (D bad)
pos 1: {B, C, D} good (A bad)
pos 2: {?, ?, ?, ?} 
pos 3: {?, ?, ?, ?}
...

For BBBB...: B good at all positions. So B ∈ good set for every pos.
For CCCC: C good at all positions.
For DDDD: D bad → D not in good set at some pos.
For AAAA: A bad → A not in good set at some pos.

For ABCDABCD: alternates - A at even, B at 1,5..., C at 2,6..., D at 3,7,..., A at 4,8,...

If position-good rules are:
pos 0: {A,B,C}; pos 1: {B,C,D}; pos 2: {?}; pos 3: {?}; pos 4: {A,?}; pos 5: {B,?}...

For ABCD repeat to be active at all positions:
pos 0=A: A good at 0 ✓
pos 1=B: B good at 1 ✓
pos 2=C: C good at 2
pos 3=D: D good at 3
pos 4=A: A good at 4
pos 5=B: B good at 5
... etc.

For BBBB...B active: B good at every position.
For CCCC...C active: C good at every position.
For ABAB...AB active: A good at even, B good at odd.
For CDCD...CD active: C good at even, D good at odd.
For BCBC active: B good at even, C good at odd.
For ADAD active: A good at even, D good at odd.

If a sequence is "fully active" (every position has good char), score is the maximum (9 for length 32 or relates to length).

Let me see which characters are "good" at each position:
From pure runs working: B and C are good at all positions, A and D are NOT good at all positions.

From ABAB works (A at even, B at odd): A good at even positions, B good at odd positions. 
From BABA (=0): B good at even? But BBBB=9 means B good at even (since BBBB has B at even pos). So contradiction.

Hmm unless the rule is: a position needs to be "compatible" with neighbors.

Or maybe the score = LONGEST RUN of "good" transitions.

Let me hypothesize: there's a finite automaton; the score = LENGTH of the longest valid path starting from position 0.

If pos 0 must satisfy some condition. Let me hypothesize transitions allowed (i, char) → (i+1, char'):
- B can follow B, C
- C can follow B, C
- A can follow ??
- D can follow ??

Hmm. Let me try a different framing.

For ABCD pattern: maybe internal "compatibility" rule like (s[i], s[i+1]) must satisfy some constraint.
- A→B ✓
- B→C ✓
- C→D ✓
- D→A: needed for cycle.

For BCDA: B→C ✓, C→D ✓, D→A. Same transitions, just starting later.

Difference: ABCD scoring at position 0 has different "starting state".

Maybe maybe what's important is whether the sequence starts in a "valid" state. Perhaps state 0 must be {A, B, C} (not D).
But that doesn't explain BCDA = 0 (starts with B).

Wait, let me check that L=8 BBBB...B score 1 result more carefully. Maybe the score is not really "length-based" but rather "the length of the prefix that matches a valid template".

For BBBBBBBB + 24 A's = score 1.
For ABCDABCD + 24 A's = score 1 (tested).
For BBBBBBBBBBBBBBBB + 16 A's = 3.
For ABCDABCDABCDABCD + 16 A's = 3.

For BCDA + ... : BCDABCDA + 24 A's = ? need to test. If score 0, then BCDA isn't a valid start.

Let me check.

## 2026-06-28 15:22 — query 170

BCDA-based always 0. So pattern matters intrinsically.

Now let me revisit my data: maybe the rule is positional. Let me see what's "good" at each position by testing single characters.

For position 0: B works (BBBB=9), A works (ABAB=9), C works (CBCB=9), D doesn't seem to (DDDD=0, DBDB=0, DCDC=0, DABC=0, DADA=0).

For position 1: B works (BBBB,ABAB), C works (BCBC), D works (BDBD,ADAD,CDCD), A doesn't (BABA, CACA, DADA, AAAA, BCDA — A at pos 3, DABC — A at pos 1!).

DABC: D at 0, A at 1, B at 2, C at 3. A at pos 1 → bad.

For position 2: C works (BCBC: C at even=0,2,4,... yes 2 has C; ABCD: 2=C), D works (CDCD: 2=C/D ?). Let me check CDCD: pos 0=C,1=D,2=C,3=D. So 2=C. Hmm CDCD never tests D at pos 2.

Let me test more directly.

## 2026-06-28 15:22 — query 173

D at pos 1 in all-B baseline: 9 (no loss). 
A at pos 1: 8 (-1). So D is "different" from A here.

So A and D are NOT equivalent universally. Let me try D at pos 1, 31.

## 2026-06-28 15:22 — query 176

D at pos 0 in all-B: 8 (-1). So D is "bad" at pos 0.
D at every even position (alternating DBDB): 0. So D is bad at many even positions.

What if the rule is: at each position, certain chars are "good" and certain are "bad". Bad chars cost some score, with caps.

Let me probe more systematically: replace single B with D at various positions.

## 2026-06-28 15:22 — query 179

D substitutions in all-B (baseline 9):
pos 0: 8
pos 1: 9
pos 2: 9
pos 4: 9
pos 30: 8
pos 31: 9 (tested earlier)

So D is bad at pos 0, 30. Not bad at 1, 2, 4, 31.

Interesting: A was bad at 1, 31. D is bad at 0, 30.
This is consistent with: A is bad at odd positions (near boundary), D is bad at even (near boundary)? Or specifically:
- A bad at pos 1 (odd)
- D bad at pos 0 (even)
- A bad at pos 31 (odd) 
- D bad at pos 30 (even)

So the "important" positions are 0/1 (start) and 30/31 (end). At those positions:
- pos 0: A or D bad? Let me check A at pos 0.
- pos 1: A bad, D ok.
- pos 30: D bad, A ?
- pos 31: A bad, D ?

## 2026-06-28 15:23 — query 182

Summary:
pos 0: A=9, B=9, D=8 (A and B good, D bad)
pos 1: A=8, B=9, D=9 (A bad, B and D good)
pos 30: A=9, B=9, D=8 (D bad)
pos 31: A=8, B=9, D=9 (A bad)

So the "important" position rules near edges (likely also for C):
- At even positions (0, 30): A and B and C good; D bad.
- At odd positions (1, 31): B, C, D good; A bad.

This matches the pair rules I derived earlier!
Even-aligned pair (s[2i], s[2i+1]) good iff:
- s[2i] ∈ {A,B,C} (no D)
- s[2i+1] ∈ {B,C,D} (no A)
EXCEPT (A,C) which was bad.

Recheck: at pos 2 (even), is C also restricted? We saw pos 2 with A or B both work in all-B baseline.

Maybe the rule is per-position: at even pos, char shouldn't be D; at odd pos, char shouldn't be A. And there's a "penalty" of some sort for violations near pos 0/1 and 30/31, but elsewhere ignored due to cap.

Now consider 16 B's + 16 A's: 
Even positions 16-30 have A → all A at even positions in second half.
Odd positions 17-31 have A → all A at odd positions in second half.

Pos 31 has A → bad (counts -1).
Pos 30 has A → ? In all-B test, A at pos 30 gave 9 (not bad). So pos 30 A might not be bad?

Hmm but 16 B + 16 A gives score 3 (not 8). So many things wrong.

Maybe constraint per pair-position: pair (s[2i], s[2i+1]) needs to be "good".

For all-B: 16 good pairs (B,B) → 9 (cap).
For 16 B + 16 A: 8 good pairs (B,B), 8 bad pairs (A,A).
For ABCD: 16 good pairs (A,B) and (C,D) — predict good. → score 9. ✓
For BCDA: 8 good pairs (B,C) + 8 bad pairs (D,A) → 8 good.

For ABCD score 9, but 16 B + 16 A also has different score (3). So # good pairs isn't enough.

Important: good pairs are at specific positions. Maybe pairs at pos 0 and pos 30 are "the only ones that matter individually" and cap at 9 with everything else? No.

Let me see: 16 B then 16 A. Has good pairs at positions (0,1)(2,3)...(14,15). 8 good. Score 3.
ABCDABCDABCDABCD then AAAAAAAAAAAAAAAA (16 A): 8 good pairs at (0,1)...(14,15) being (A,B) good, (C,D) good. Score?

I haven't tested ABCD x4 + 16 A's. Let me extrapolate: from earlier I tested N=4 copies → ABCDABCDABCDABCD then 16 A's = 3. Yes!

So ABCDABCDABCDABCD + AAAA...A = 3. Same as 16 B's + 16 A's!

So 8 good pairs at positions 0,2,4,...14 → 3.
16 good pairs at positions 0..30 → 9.

What about 12 good pairs?
For pure B's: L=24 → 12 BB pairs at positions 0,2,...22. Score 6.
For ABCD x6 + 8 A's: 12 good pairs at 0,2,...22. Score 6. ✓

For 14 good pairs:
L=28 → 14 pairs → 7.
ABCD x7 + 4 A's → 7.
Test gave 7. ✓

For 10 good pairs:
L=20 → 10 pairs → 4.
ABCD x5 + 12 A's → 4.
Test gave 4. ✓

For 11 good pairs:
L=22 → 11 pairs → 5.
ABCD x5.5 (impossible). Try a mixed.

But what about FRACTIONAL pairs or non-aligned good?

Actually I think: score = function of # even-aligned good pairs, where the function matches my earlier table:
0 good→0, 1→0, 2→0, 4→1, 6→2, 8→3, 10→4, 11→5, 12→6, 13→6, 14→7, 15→8, 16→9.

But wait, 11 good only happens with non-uniform patterns. Let me test by removing one pair from the cap=16 case.

## 2026-06-28 15:23 — query 186

Pair-kills:
0 killed → 16 good pairs → 9
1 killed (pos 0,1=AA): 15 → 8
1 killed (pos 30,31=AA): 15 → 8
2 killed (pos 0,1 and 30,31): 14 → 7
3 killed (pos 0,1; 16,17; 30,31): 13 → 7

Mapping confirmed: # good even-aligned pairs → score:
16→9
15→8
14→7
13→7 (?)
12→6
11→5
10→4
8→3
6→2
4→1

But the mapping is not monotonic +1 per pair! 13→7 but 14→7 too. So when 13 vs 14 pairs are good gives same score 7.

Also let me check: # bad pairs:
16 good = 0 bad → 9
15 good = 1 bad → 8
14 good = 2 bad → 7
13 good = 3 bad → 7
12 good = 4 bad → 6
11 good = 5 bad → 5
10 good = 6 bad → 4
8 good = 8 bad → 3
6 good = 10 bad → 2
4 good = 12 bad → 1
0 good = 16 bad → 0

Sequence: 9,8,7,7,6,5,4,?,3,?,2,?,1,?,?,?,0
With 16-(# bad) ≈ score for low bad. Let me see #bad → score:
0→9, 1→8, 2→7, 3→7, 4→6, 5→5, 6→4, 8→3, 10→2, 12→1, 16→0.

Hmm: 9 = 16 - 7? Try score = max(0, 16 - 2*bad - something):
score = 9 - bad for bad ≤ 3? 9-0=9, 9-1=8, 9-2=7, 9-3=6 (but got 7). 
score = 16 - bad for bad ≤ ?: 16-0=16 (need 9). No.

Maybe score = floor((16-bad) * 9 / 16) approximately:
bad=0: 9
bad=1: 15*9/16 = 8.4 → 8 ✓
bad=2: 14*9/16 = 7.875 → 7 ✓
bad=3: 13*9/16 = 7.3 → 7 ✓
bad=4: 12*9/16 = 6.75 → 6 ✓
bad=5: 11*9/16 = 6.19 → 6 (need 5) ✗

Close but bad=5 fails. 

Try: floor(good * 9 / 16)?
good=16: 9 ✓
good=15: 8.4 → 8 ✓
good=14: 7.87 → 7 ✓
good=13: 7.3 → 7 ✓
good=12: 6.75 → 6 ✓
good=11: 6.19 → 6 (need 5) ✗
good=10: 5.6 → 5 (need 4) ✗

Close but breaks.

Maybe: floor(good²/something) or piecewise.

Actually looking at the table again:
good=4: 1; good=6: 2; good=8: 3; good=10: 4; good=11: 5; good=12: 6; good=14: 7; good=16: 9.

The jumps are at good=4,6,8,10,11,12,14,16. Increments of 2, but then 1 at 11, then 2,2,2.

Hmm: good=8,10,12,14,16 give scores 3,4,6,7,9. Diffs 1,2,1,2. Same pattern.

Maybe score = (good-3)/(some piecewise function).

Try score = floor((good)/2) - 1 + bonus:
good=4: 1 ✓
good=6: 2 ✓
good=8: 3 ✓
good=10: 4 ✓
good=12: 5 (need 6) ✗

floor((good-2)/2):
good=4: 1 ✓
good=6: 2 ✓
good=8: 3 ✓
good=10: 4 ✓
good=12: 5 (need 6) ✗

floor((good-2)/2) + max(0, good-10):
good=10: 4+0=4 ✓
good=11: 4+1=5 ✓
good=12: 5+2=7 (need 6) ✗

floor((good-2)/2) + floor((good-10)/X):
good=12: 5 + ? = 6 → +1
good=14: 6 + ? = 7 → +1
good=16: 7 + ? = 9 → +2

Hmm.

Wait I think I conflated good-pair count with something. Let me actually carefully tabulate from my L-tests:

For single run of B at start, L B's then (32-L) A's:
even-aligned pairs at (0,1)(2,3)...(2i, 2i+1)... = (B,B) if both i ≤ floor((L-1)/2)... actually:
Pair (2i, 2i+1) is BB iff 2i+1 < L, i.e., i ≤ (L-1)/2, i.e., i ≤ floor((L-1)/2). So # BB pairs = floor((L-1)/2)+1 if L ≥ 1 and 2i ≥ 0 ... = ceil(L/2).

Wait, # of full BB pairs at even positions = floor(L/2) if L even. For L=20: 10 pairs. ✓

L=8: 4 BB pairs. Score 1.
L=12: 6 → 2.
L=16: 8 → 3.
L=20: 10 → 4.
L=22: 11 → 5.
L=24: 12 → 6.
L=26: 13 → 6.
L=28: 14 → 7.
L=30: 15 → 8.
L=32: 16 → 9.

But the AA bad pairs also matter (or not).
L=8: 4 BB + 12 AA pairs. Total 16. 
L=12: 6 BB + 10 AA.
L=32: 16 BB + 0 AA.

What if bad-pair count subtracts? Let's see:
score = func(good=4 BB, bad=12 AA) = 1.
score = func(good=16, bad=0) = 9.

Maybe score = good - bad/3? L=8: 4-4=0. Need 1.
score = (good - bad)/2? 8: (4-12)/2 = -4. No.

OK let me look in detail. Maybe the good pairs aren't just BB/AB/CD/etc but specific.

Different "good" pair types contribute differently? Maybe BB is "1-good" and AB or CD is "0-good"? No, ABCD has 16 AB/CD pairs and scores 9.

Actually I realize: 16 good even pairs always gives 9 (cap). Even if it includes (A,B) or (C,D) types. And only the COUNT matters.

For 16 B's + 16 A's: 8 good even pairs (BB) + 8 bad (AA). Score 3.
For ABCD x4 + 16 A's: 8 good (AB/CD) + 8 bad (AA). Score 3. ✓ Both 8 good, both 3.

But what about specific positions of good pairs?

Position of good even pairs:
For 16 B at start: pairs at i=0,1,2,3,4,5,6,7 are good (positions 0-1, 2-3, ..., 14-15).
For ABCD x4: same positions are good.

What if the good pairs are at non-contiguous positions? Let me test.

## 2026-06-28 15:24 — query 187

8 BB + 8 BB split with 16 A in middle = 4. Different from contiguous 8 BB at start = 3.

Even-pair positions:
At start 8 BBs: pairs at 0,1,2,3 are BB (i.e., positions 0-1, 2-3, 4-5, 6-7).
Then 16 As: pairs at 4,5,6,7,8,9,10,11 are AA (positions 8-9 to 22-23).
At end 8 BBs: pairs at 12,13,14,15 are BB (positions 24-25 to 30-31).
Total good even pairs: 8 (4+4). Score 4.

For BBBBBBBB...AAAAAAAA (16 B then 16 A): 8 good even pairs at indices 0-7. Score 3.
For 8 BB at start + 8 BB at end split: 8 good even pairs at indices 0-3, 12-15. Score 4.

So same # of good pairs, different positions, different scores! Position of good pairs matters.

Insight: more "spread out" good pairs score higher. Maybe a "diversity" or "extent" bonus.

Let me think: maybe score depends on EXTENT (last good pair index - first good pair index + 1) and # of good pairs?

For 8 BBs at start: indices 0-7. extent 8. # good = 8. Score 3.
For 4+4 split: indices {0,1,2,3,12,13,14,15}. extent 16. # good 8. Score 4.

For 16 good: extent 16. # = 16. Score 9.

For 12 good (e.g., L=24 single): indices 0-11. extent 12. # = 12. Score 6.

What if score = max # good pairs in any "window" of certain size, or extent / 2 + adjustment?

Try score = floor((extent + #good)/something):
8 start: (8+8)/X=3 → X=5.3
4+4 split: (16+8)/X=4 → X=6.
Not clean.

Maybe score = floor((sum of pair indices weights)/N)?

Let me think of it as: score = MAX over all even-aligned starting positions p, of (# consecutive good pairs starting from index p)? No, that's just run length again.

Actually for the splits: 8 BBs split (4 at start, 4 at end). The longest "run of good pairs" is 4. Score 4.
For 8 BBs at start: longest run is 8. Score 3.

So they're not consistent with "longest run of good pairs" either.

Maybe score relates to # of good even pairs AND # of good odd pairs?

ABCDABCD repeat: odd pairs (1,2)=(B,C) good, (3,4)=(D,A) bad, (5,6)=(B,C) good, (7,8)=(D,A) bad,... 8 good odd + 7 bad odd = 8 good odd.
Hmm but it was 9 score. 16 good even + 8 good odd = 24 total. 

For BCDA: 8 good even (BC) + 15 good odd (CD, AB)? Let me check.
BCDA repeat: positions 0:B,1:C,2:D,3:A,4:B,5:C,6:D,7:A,...
Odd pairs (1,2)=(C,D) good, (3,4)=(A,B) good, (5,6)=(C,D) good, (7,8)=(A,B) good,... all good. 15 good odd!
Even pairs (0,1)=(B,C) good, (2,3)=(D,A) bad, repeating. 8 good + 8 bad.

So total good = 8+15 = 23. But BCDA scored 0!

So total good pairs isn't the score. Position matters.

Let me think: maybe the rule is based on (s[i], s[i+1]) ONLY at certain positions, like only even pairs?

For BCDA: 8 even good. Score 0.
For 16 B + 16 A: 8 even good. Score 3.

Both 8 even good but different scores. So even count alone not enough either.

What distinguishes them?
16 B + 16 A: contiguous block of good pairs.
BCDA: alternating good/bad pairs.

What if score requires CONSECUTIVE good pairs starting from index 0?

For 16 B + 16 A: pairs 0,1,2,3,4,5,6,7 good (8 consecutive). Score 3.
For BCDA: pair 0 good, pair 1 bad. Only 1 consecutive from start. Score 0.

For ABCD: 16 consecutive good. Score 9.
For 16 B start: 8 consecutive. Score 3.
For 8 BBs at start: 4 consecutive. Score 1? But measured 1 actually. Let me check.

Wait, 8 B's at start (L=8 BBBB then 24 A's): even pairs are (B,B)x4 then (A,A)x12. 4 consecutive good. Score 1. ✓ Yes 1.

For 4+4 split (4 BB at start, then 16 A, then 8 BBs at end... wait original test was 8 BBs at start + 16 A + 8 BBs at end):
Even pair seq: 4 good, 8 bad, 4 good. First 4 consecutive good. Score 4.

Hmm, predicted 1 if formula is "consecutive from start", but got 4. So not that.

Maybe score = sum over RUNS of consecutive good pairs?

For 8 BB at start: 1 run of 4 → ?
For 4+4 split: 2 runs of 4 each.
For 16 B start: 1 run of 8.
For pure 32 B: 1 run of 16.

For BCDA: 8 isolated good pairs (alternating bad).
For ABCD: 1 run of 16.

Run lengths:
{4}: score 1
{8}: score 3
{16}: score 9
{4, 4}: score 4
{1,1,1,1,1,1,1,1}: score 0 (BCDA)

So 8 isolated runs of 1 = 0. 1 run of 8 = 3. 2 runs of 4 = 4. 1 run of 16 = 9.

This is interesting! Sum f(R) over runs of good-pair runs:
f(1)=0, f(4)=1 or 2 (4+4=4 means f(4)=2 if linear, or f(4)=1 and there's a bonus)
f(8)=3, f(16)=9.

If 2 runs of 4 gives 4 and 1 run of 8 gives 3, then 4 + 4 > 8 (4*2 vs 3). Weird.

f(4)=2 (from 4+4=4 implies 2+2=4); but then 1 run of 4 should give 2, not 1.

f(4)=1, but 2*f(4)+bonus(2 runs)=4. So bonus(2 runs)=2. 

Or score = sum f(R) + g(# runs)?
1 run of 16: f(16) + g(1) = 9
1 run of 8: f(8) + g(1) = 3 → f(8)=3-g(1)
2 runs of 4: 2 f(4) + g(2) = 4
1 run of 4: f(4) + g(1) = 1
8 runs of 1: 8 f(1) + g(8) = 0

This is getting too many unknowns. Let me just gather more data.

Actually before getting lost: re-derived idea. The pairing analysis gave me confused results. Let me step back and just look at what makes sequences score high. The basic theory seems to be: there's a "good pattern" that must be matched, position-aware.

ABCD repeat scoring like BBBB suggests: each character at each position has a "score allotment" based on local context.

Let me try a really simple test: BABA BABA where every pair is "(BA)" — bad. What scores?

## 2026-06-28 15:24 — query 189

BBAA BBAA pattern: 16 BB pairs ... wait no.
BBAABBAABBAA... positions: B B A A B B A A...
Even pairs (0,1)=BB good, (2,3)=AA bad, (4,5)=BB good, (6,7)=AA bad,...
8 BB good + 8 AA bad = 8 good. Score 0!

But 16 BB good (pure) = 9.
16 B's + 16 A's = 8 BB + 8 AA = score 3.
BBAA BBAA = 8 BB + 8 AA = score 0!?

Both have 8 good even pairs but different scores.

In 16 B + 16 A: good pairs at indices 0-7 contiguous.
In BBAA BBAA: good pairs at indices 0,2,4,6,8,10,12,14 alternating.

So same # good pairs but completely different layout: contiguous = 3, alternating = 0.

The "run length" of good even-pairs matters:
- 16 B + 16 A: 1 run of 8 good pairs.
- BBAA BBAA: 8 runs of 1 good pair each.

And BBBB AAAA BBBB AAAA: 4 alternating blocks of BBBB and AAAA.
Even pairs: BB BB AA AA BB BB AA AA BB BB AA AA BB BB AA AA → 2 BB, 2 AA, ...
So 4 runs of 2 good pairs each = {2,2,2,2}. Score 6.

Comparison:
- {16} good pairs: 9 (max)
- {8}: 3
- {4,4}: 4
- {4}: 1
- {2,2,2,2}: 6
- {1,1,1,1,1,1,1,1}: 0
- BCDA was 1 good pair contiguous? Let me recount BCDA: even pairs at (0,1)=(B,C) good, (2,3)=(D,A) bad, repeating. So 8 isolated good pairs. = {1,1,1,1,1,1,1,1}. Score 0.

So {2,2,2,2} = 6 (highest of partitions of 8 we've seen!).
{1*8} = 0.
{8} = 3.
{4,4} = 4.

Strange — splitting helps but at extremes hurts. Let me think:
- {2*n} for n=4, 8 = 16 good pairs total, 6 score. 16 good = 9 only when single big run.

Hmm wait {2,2,2,2} only has 8 good pairs total (2*4). Not 16. Score 6.
{8} = 8 good pairs in 1 run. Score 3.
{4,4} = 8 good pairs in 2 runs. Score 4.
{2,2,2,2} = 8 good pairs in 4 runs. Score 6.
{1,1,1,1,1,1,1,1} = 8 good pairs in 8 runs. Score 0.

So sweet spot at ~4 runs. Quadratic-like.

What about {1,2,1,2,1,1}? Need to test other configurations.

Actually maybe the metric is: maximum # of good pairs in a periodic-2 substructure?

Or maybe: # of "BBBB" or "BBBC" type 4-mers (4 consecutive B/C). 

Re-examine via 4-mers (length 4 windows of all B/C):
BBBBAAAA repeating: BBBB at position 0-3, 8-11, 16-19, 24-27 = 4 occurrences of BBBB. # 4-mers all B/C = 4 (one per block). Score 6.
BBAABBAA: no 4-mers of all B/C. Score 0.
16 B's contiguous: 4-mers at 0,1,2,3,4,5,6,7,8,9,10,11,12,13 = 13 occurrences (all 4-mers within the 16 block, that's 16-4+1=13). Score 3.

Hmm 4 4-mers → 6 score. 13 4-mers → 3.

Maybe the right pattern is something more specific. Let me note: BBBBAAAA BBBB AAAA BBBB AAAA BBBB AAAA = period-8 with 4 BBBB's. 4 BBBB's gave 6.

What if score = # of "good 4-blocks" at position 4k? Like, position 0-3 either all B/C or what?
Test: pairs at position 4k:
8 B's at 0-7: positions 0-3 all B, 4-7 all B → 2 "good 4-blocks".
16 B's: 4 blocks.
BBBBAAAA repeating: blocks at 0-3 (BBBB), 4-7 (AAAA), 8-11 (BBBB), ... 4 BBBB blocks (at 0,8,16,24).

For 16 B's contiguous → 4 BBBB blocks → score 3.
For BBBBAAAA*4 → 4 BBBB blocks → score 6.

Same block count, different scores. Position matters.

OK this is getting complex. Let me try yet another angle: brute force gather more data systematically and look for patterns.

## 2026-06-28 15:24 — query 191

BBABBABBA... period 3. Same as earlier test (gave 7).

Let me think about this very differently. We have many data points. Let me focus on the observation that score(seq) up to 9 corresponds to something countable.

ABCDABCDABCDABCDABCDABCDABCDABCD = 9. This sequence has nothing special — but treats {A,B,C,D} as all useful.

Let me revisit: when ALL chars are not A and not D-only.

Maybe the rule is: at position i, character c is "valid" iff (i mod 4) is allowed for c?

Let me see which (i mod 4, c) are good. In ABCD repeat:
i mod 4 = 0: A — good (since ABCD=9)
i mod 4 = 1: B — good
i mod 4 = 2: C — good
i mod 4 = 3: D — good

In BCDA:
i mod 4 = 0: B
i mod 4 = 1: C
i mod 4 = 2: D
i mod 4 = 3: A
→ score 0, so something here is invalid.

In CDAB:
i mod 4 = 0: C
i mod 4 = 1: D
i mod 4 = 2: A
i mod 4 = 3: B
→ score 9.

DABC: D at 0, A at 1, B at 2, C at 3 → 0.

So good (i mod 4, c) sets:
i%4=0: from ABCD: A, from CDAB: C → A, C definitely good at 0%4. Also tested: B works (BBBB=9), so B at 0%4 also good. What about D? DDDD=0 implies D not good at all positions but maybe ok at some. D at pos 0 in all-B: 8 (almost OK). 

Let me check BBBB more carefully via pos: i%4=0 → B; i%4=1 → B; i%4=2 → B; i%4=3 → B. All B. Score 9.

So B is good at every i%4.

CCCC: C is good at every i%4 (score 9).

ABCDABCD: pos-rule satisfied: A@0, B@1, C@2, D@3. Score 9.

What if the rule is: a sequence is "alive" if its content matches a valid periodic pattern. Valid period-1 patterns: BBBB, CCCC. Valid period-4: ABCD, CDAB (and ?). Valid period-2: ABAB, ADAD, BCBC, CBCB, CDCD, BDBD, BBBB, CCCC.

Let me try other period 4 patterns.

## 2026-06-28 15:25 — query 196



## 2026-06-28 15:26 — query 199



## 2026-06-28 15:27 — query 207



## 2026-06-28 15:28 — query 216

Updated period-4 results:
Good (score 9): ABCD, CDAB, ABCB, CBCD, CDBC, BCCD, BBAB, ABBB, CCCB, CCBC, CCCD, CDCC, ABCC
Bad (score 0): DABC, BCDA, ABDC, CBDA, ACBD, BCBA, ACDB, DCBC, BAAB, ABBA, BABB, BBBA, AABB, DCCC, BABC, CABC

Looking at the GOOD set characters at each position (mod 4):
ABCD: A,B,C,D
CDAB: C,D,A,B
ABCB: A,B,C,B
CBCD: C,B,C,D
CDBC: C,D,B,C
BCCD: B,C,C,D
BBAB: B,B,A,B
ABBB: A,B,B,B
CCCB: C,C,C,B
CCBC: C,C,B,C
CCCD: C,C,C,D
CDCC: C,D,C,C
ABCC: A,B,C,C

Pos 0 (=0%4) chars in good patterns: A,C,A,C,C,B,B,A,C,C,C,C,A → {A,B,C}
Pos 1 (=1%4): B,D,B,B,D,C,B,B,C,C,C,D,B → {B,C,D}
Pos 2 (=2%4): C,A,C,C,B,C,A,B,C,B,C,C,C → {A,B,C}
Pos 3 (=3%4): D,B,B,D,C,D,B,B,B,C,D,C,C → {B,C,D}

So pattern: pos%2=0 → {A,B,C}; pos%2=1 → {B,C,D}.

This confirms my earlier (s[even], s[odd]) pair rule's constraints!

EXCEPT for the (A,C) bad pair: I have ABCC good which has (A,B) at pos 0-1 and (C,C) at pos 2-3. Both good per my rule.

But ACAC was 0 — that's (A,C) at (0,1), (A,C) at (2,3),... All (A,C) which is bad pair.

So at the per-pair level: (even, odd) = (A,C) is BAD.

Let me re-verify my pair table:
At (even, odd) position pair (x,y), the pair is "good" if specific conditions. Let me re-derive from period-2 patterns:
AAAA: (A,A) bad - all (A,A) pairs.
BBBB: (B,B) good
CCCC: (C,C) good
DDDD: (D,D) bad
ABAB: (A,B) good
BABA: (B,A) bad
ACAC: (A,C) bad
CACA: (C,A) bad
ADAD: (A,D) good
DADA: (D,A) bad
BCBC: (B,C) good
CBCB: (C,B) good
BDBD: (B,D) good
DBDB: (D,B) bad
CDCD: (C,D) good
DCDC: (D,C) bad

GOOD even-odd pairs: BB, CC, AB, AD, BC, CB, BD, CD = 8 good
BAD even-odd pairs: AA, DD, BA, AC, CA, DA, DB, DC = 8 bad

Constraint: pair (x,y) is GOOD iff:
- x in {A,B,C} (not D), AND
- y in {B,C,D} (not A), AND
- NOT (x=A AND y=C)

Verify: 
- (A,B): A∈ABC, B∈BCD, not (A,C) → good ✓
- (A,C): A∈ABC, C∈BCD, IS (A,C) → bad ✓
- (A,D): A,D allowed, not (A,C) → good ✓
- (B,B)(B,C)(B,D): all good ✓
- (C,B)(C,C)(C,D): all good ✓
- (D,*): D not in {A,B,C} → bad ✓
- (B,A)(C,A): A not in {B,C,D} → bad ✓
- (A,A): A not in {B,C,D} → bad ✓

So 8 good pair types, all symmetrically structured.

Now the question is: what's the scoring function?

I have data:
- # good even-pairs g, distribution of runs r1,r2,...
- score

Let me organize:
{16}: 9 [pure 32 B etc.]
{15}: 8 [31 B + 1 A at pos 0 or 1, ...]
{14}: 7 [some configs]
{13}: 7
{12}: 6
{11}: 5
{10}: 4
{8}: 3
{4,4}: 4 [8 B's at start + 8 B's at end split]
{2,2,2,2}: 6 [BBBB AAAA repeating]
{1,1,...1}(8x): 0 [BBAA BBAA or BCDA pattern]
{4}: 1 [8 B's]
{6}: 2
{4,4} via 8 BBs + 16 A + 8 BBs (with longer gap): different positions? wait result was 4.

Maybe the scoring function isn't just g but g + bonus for "spacing".

Wait, I notice: {2,2,2,2} gave 6. Same as {12} (single run of 12 good pairs).
{4,4} gave 4 - same as {10}.

Could it be: score = some function of multiset of run lengths considering "effective length"?

Let me look at:
{16} → 9
{2,2,2,2} → 6 (=score of {12} single)
{4,4} → 4 (=score of {10} single)
{1,1,1,1,1,1,1,1} → 0

Maybe: score = score(L_effective) where L_effective is determined by the run structure?

For BBBBAAAA BBBBAAAA...: 4 BBBB blocks. Each "good even pair run" of length 2. Total good pairs = 8. But score = 6 = single-run score for 12 pairs.

Hmm, total good g = 8, but score corresponds to "effective" g = 12.

Maybe: spreading pairs out makes them count for more? Maybe score = something like sum of position-weighted good pairs?

Let me compute "extent" of good pairs:
{16}: positions 0-15, extent 16. Score 9.
{2,2,2,2}: positions {0,1,4,5,8,9,12,13} or similar. Extent ~14. Score 6.
{4,4}: positions {0,1,2,3,12,13,14,15}. Extent 16. Score 4.

Doesn't seem to match.

Maybe score = floor((# good 4-mers BB+CC+...)/something):
Let me count "good 4-mers": 4 consecutive chars all in valid pattern.
BBBB sub: ABCD has these? ABCD has length 4, just one ABCD 4-mer. Not BBBB.

Hmm.

Let me try: maybe score = # of i in {0,1,...,29} such that (s[i], s[i+1]), (s[i+2], s[i+3]) are both good pairs and certain alignment.

Actually let me re-test the # of good pairs hypothesis with more data, specifically with split patterns.

## 2026-06-28 15:29 — query 220



## 2026-06-28 15:30 — query 225

Updated data on good-pair run distributions (showing pair-runs):
{} or {1,1,...}: 0
{2}: 0
{3,3}: 2
{4}: 1
{2,2}: 2
{4,4}: 4
{3,3,3}: 4
{2,2,2}: 4
{2,2,2,2}: 6
{3,3,3,3}: 7
{4,4,4}: 8 (from BBBBBBBB AAAA BBBBBBBB AAAA BBBBBBBB AAAA... 3 runs of 8 B)
{8}: 3
{6}: 2
{10}: 4
{11}: 5
{12}: 6
{14}: 7
{15}: 8
{16}: 9

Let me think about this. It looks like a quadratic function of the configuration.

Looking at uniform runs {k,k,k,k} with n=4 runs:
n=4, k=2: 6
n=4, k=3: 7
n=4, k=4: 6
n=3, k=4: 8
n=3, k=3: 4
n=2, k=4: 4
n=2, k=3: 2
n=1, k=16: 9

For n=1, score(k) = sequence I derived earlier.

Maybe the score formula is # of length-4 contiguous good-pair runs?

For {16}: 13 length-4 windows. Score 9. 13/score ≠ const.

Let me think bigger picture. Maybe score = (# of "good 4-cell blocks at aligned positions") or similar.

The pairs are pair-positions 0..15. A "4-block" might be 4 consecutive pair positions that are all good.

For {16}: 13 4-blocks. Score 9.
For {12} single: 9 4-blocks. Score 6. 
For {8} single: 5 4-blocks. Score 3.
For {4}: 1 4-block. Score 1.
For {4,4}: 1+1 = 2 4-blocks. Score 4.
For {2,2,2,2}: 0 4-blocks (each is size 2). Score 6.
For {16} ABCD type: 13 4-blocks. Score 9.

{2,2,2,2} = 0 4-blocks but score 6 > {4} = 1 4-block score 1. So not 4-block count.

OK maybe count BB pairs at every position (overlapping good pairs)? Let me count differently.

Actually let me try this hypothesis: score = # of (i, i+1) such that BOTH the even-pair starting at i (if i even) and the odd-pair starting at i are good?

Or: score = # of pairs (i, i+1) where (s[i], s[i+1]) is a "good" pair AND (s[i+2], s[i+3]) is also good?

For {16} pure B: every BB is good → all consecutive pairs satisfied → max score 9.

Let me focus on counts: total "good adjacent pairs" (not just even-aligned) for varying patterns:

BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA = 4 runs of 4 B's.
Adjacent pairs (i, i+1) overlap:
within each BBBB: 3 BB pairs. 4 runs → 12 BB pairs.
At boundaries: pairs (BB-AA): 4 of (B,A) at positions 3-4, 11-12, 19-20, 27-28. And 3 (A,B) at positions 7-8, 15-16, 23-24. Plus (A,A) within AAAA: 3 per group * 4 = 12.

Good adjacent pairs in this sequence: where is the rule? Adjacent pair (x,y) is "good" iff... same rule? Let me confirm.

Actually I derived "good even pairs". Whether the same rule applies to odd pairs is unknown. Let me look at the BBAA pattern: BBAA BBAA = score 0. Adjacent pairs: (0,1)=BB, (1,2)=BA, (2,3)=AA, (3,4)=AB, (4,5)=BB, etc.
even pairs (0,1)(2,3)... = BB AA BB AA. 8 good even.
odd pairs (1,2)(3,4)... = BA AB BA AB. 0 good odd (BA is bad, AB is good actually!). Let me recount.

Earlier: (A,B) good, (B,A) bad. So in BBAA BBAA: 
Odd pairs (1,2),(3,4),(5,6),(7,8),...: 
(B,A), (A,B), (B,A), (A,B), ... 
8 AB good (at odd-indexed pairs), 8 BA bad.

So total good pairs (even or odd): 8 even good + 8 odd good = 16.

For 16 B pure: 16+15 = 31 good pairs.
For BBAA pattern: 16 good pairs.
For {2,2,2,2}: same as BBBBAAAA BBBBAAAA pattern. Let me count: BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA.
Even pairs: 8 good (BB) + 8 bad (AA).
Odd pairs: (1,2)=BB, (3,4)=BA, (5,6)=AA, (7,8)=AB, (9,10)=BB, (11,12)=BA, (13,14)=AA, (15,16)=AB,...
Pattern repeats every 8 positions. Per period: BB, BA, AA, AB. BB good, BA bad, AA bad, AB good. 2 good per 4 odd pairs. Total odd pairs = 15. 4 periods × 2 = 8 good odd in 16 pairs but odd has 15 → ~7-8.

Hmm complicated. Maybe I should just try to fit a model.

Let me hypothesize: score = floor((# total good pairs (overlapping))/4) - some adjustment.

For 32 B: total good = 31. /4 = 7.75. Need 9. ✗

Or: score = max over k of (# 4-consecutive-good-pairs windows)? Too vague.

OK I'll take a different approach: hypothesize that the score function is the COUNT of some specific motif. Let me look at small examples and try to deduce.

CDCD repeating: score 9. Has CDCD motif 16 times (overlapping CD pairs at every even pos). 
CDABCDAB: score 9. Has CD at positions 0,4,8,...28 = 8 of them. AB at 2,6,...30 = 8. 

Maybe score = floor((# good even pairs + # good odd pairs)/something)?

For {16} pure B (BBBB...): 16 good even + 15 good odd = 31. 31/X = 9 → X≈3.4.
For 16 B + 16 A: 8 good even + 8 good odd? Let me count.
16 B at start, then 16 A. 
Even pairs: 8 BB + 8 AA.
Odd pairs: (1,2)(3,4)...(13,14)= 7 BB. (15,16)=(B,A) bad. (17,18)...(29,30)= 7 AA bad.
Total good odd = 7.
Total good = 8 + 7 = 15. /X = 3 → X=5.

For ABCD x8: 16 even + 8 odd = 24. /X = 9 → X = 2.67.
For ABCD x4 + 16 A: 8 even + ? odd. Odd pairs (1,2)=(B,C) good, (3,4)=(D,A) bad, (5,6)=(B,C) good, ... in first half. Then in 16 A's: bad.

Stop, too messy. Let me think differently.

I notice ABCD * N gives same as BBBB * 4N in many cases. Like ABCD repeat with N "blocks" gives same score as 4N B's. Maybe score depends on TOTAL number of positions that are part of a "valid" period?

ABCD has period-4 pattern matching. BBBB has period-1 (just B). Both are "valid templates". Once the sequence breaks from the template, it stops contributing.

For BBBB at start length L, then A's: contributing length = L. Score = f(L).
For ABCD x N at start, then A's: contributing length = 4N. Score = f(4N).
For BBBB AAAA BBBB AAAA: contributing length = ? 

Hmm but ABCD AAAA ABCD AAAA = should give 4 contributing chars * 2 = 8 contributing chars, score?
And BBBB AAAA BBBB AAAA = 8 contributing. Score = 4 (=score of L=8 contiguous + maybe more for splitting).

Maybe the rule: each "good template block" contributes some score, and they combine. Hmm.

Let me explicitly test: does the structure matter mostly through pair count of valid even pairs OR something else.

## 2026-06-28 15:30 — query 229

More pair-run data:
{6,6} (each from 12 B): 7. Total good pairs = 12.
{5,5}: 5. Total = 10.
{4,4}: 4. Total = 8.
{3,3}: 2. Total = 6.
{2,2}: 2. Total = 4.

For uniform pairs of equal size {k, k}:
k=2: 2
k=3: 2
k=4: 4
k=5: 5
k=6: 7

Vs single runs:
{4}: 1; {6}: 2; {8}: 3; {10}: 4; {12}: 6.

So {k,k} is roughly comparable to {2k} but with bonus:
{2,2}=2 vs {4}=1 (+1)
{3,3}=2 vs {6}=2 (=)
{4,4}=4 vs {8}=3 (+1)
{5,5}=5 vs {10}=4 (+1)
{6,6}=7 vs {12}=6 (+1)

Roughly +1 for splitting. Makes sense — more "starts/ends" might add up.

Let me revisit: maybe the score is total good pairs + bonus for each gap of A/D? Or each separation.

Single run length L pair-good = floor(L/2). For L=20, 10 pairs, score 4. For L=10 in two runs (10+10), 10 pairs, score 5.

Maybe score = floor((# good pairs + # gaps)/?) where gap is between active blocks. 

Or maybe: there's a base unit "BBC", "ABCC" etc and the score counts complete coverage.

Actually let me try one more theory: maybe score = sum over each maximal "active" block of f(block_length), where f(L) computed appropriately.

Block lengths (in chars, not pairs) for {2,2,2,2}: each B-block is 4 chars → block length 4. 4 blocks of 4 chars each. Score 6.
For BBBB AAAA repeating: block sizes [4,4,4,4]. Score 6.

For BBBBBBBB AAAA BBBBBBBB AAAA BBBBBBBB AAAA (3 blocks of 8): score 8.
For 8 BBBB AAAA = 1 block of 8 → score 1.
2 blocks of 8 → 4.
3 blocks of 8 → 8.
4 blocks of 8 doesn't fit in 32 chars.

So # blocks counts strongly:
1 block of 8: 1.
2 blocks of 8: 4.
3 blocks of 8: 8.

Hmm 1, 4, 8 — almost n² but 8 not 9.

For blocks of 4:
1 block: 0.
2 blocks: 2 [{4,4} = BBBB AAAA BBBB pattern with 8 A's between gives 2; 4 B+8A+4B → tested]. 
3 blocks: 4. [BBBB AAAA BBBB AAAA BBBB + A's = {3,3,3} reported 4]
4 blocks: 6. [{4 of 4} = BBBBAAAA BBBBAAAA BBBBAAAA BBBBAAAA tested 6]

1, 2, 4, 6 for n blocks of 4. Diffs 1, 2, 2.

For blocks of 5 (10-B in run):
Tested {5,5} = 5, {5,5,5,5} = 6 (=24 chars, 4 runs of 5 with 3-char A gaps).
{5}: predicted 1 or 2 (between {4}=1 and {6}=2).

For blocks of 6:
{6}: 2. {6,6}: 7. {6,6,6,6}: 7.
1: 2; 2: 7; 4: 7.

For blocks of 7:
{7}: ? (between 6 and 8 → ~3 maybe). Test wasn't done explicitly.
{7,7,7,7}: 7.

For blocks of 8:
{8}: 1, no wait it's a block of 8 chars = 4 good pair pairs. Hmm I'm conflating.

Wait, I think I confused two things. Let me clarify: by "block" I mean a contiguous run of B/C characters. A B-block of length L_char has floor(L_char/2) "good even pairs" if it's aligned to even positions, otherwise it could be more or less.

Let me re-examine: for B-block at start of length L_char:
# good even pairs = ceil(L_char/2) (last pair (L_char-1, L_char) if L_char odd is B,A=bad).
Actually: even pairs at indices 0, 2, 4, ..., 2*(L_char/2 - 1). If L_char even, # = L_char/2.
If L_char odd, # = (L_char-1)/2.
So floor(L_char/2).

For L_char=8: 4 good even pairs. Score 1.
For L_char=4 (single block at start): 2 good even pairs. Score 0.
For L_char=16: 8. Score 3.

For 4 blocks of 4 (BBBBAAAA repeating): each block has 2 good even pairs. Total 8 good even pairs distributed. Score 6.

So score(8 contiguous good even pairs at start) = 3.
score(8 even pairs spread out as 4 runs of 2) = 6.

Even though same total good even pairs, distribution makes big difference.

Maybe what the score really measures is some structural count. Let me try: # of maximal good-pair runs WHOSE total pair count is at least 1? 

# of nonzero pair-runs:
{16}: 1. Score 9.
{8}: 1. Score 3.
{4}: 1. Score 1.
{4,4}: 2. Score 4.
{2,2,2,2}: 4. Score 6.
{2,2,2,2,2,2,2,2}: 8. Score 0!!!

Wait, {2*8} should be 8 runs but score 0. Let me recompute: BBAA BBAA BBAA... is BBAABBAA... So even pairs: BB at 0-1, AA at 2-3, BB at 4-5, AA at 6-7, ... So good even pairs at indices 0, 2, 4, 6, ... 14 (every other index). Eight good even pairs in 8 isolated 1-runs.
Hmm "runs of consecutive good pairs": each isolated good pair is a run of 1.
{1,1,1,1,1,1,1,1}: 8 runs of 1. Score 0.

So pair runs of 1 count for 0. Pair runs of 2+ count for something positive.

Let me hypothesize: score = sum over pair-runs of f(R), where f(R) = R*(R-1)/2 or similar (rewards LONGER runs more).

f(1) = 0.
f(2) = 1. {2,2,2,2} = 4. Score 6. Diff +2. Maybe + bonus for # runs?
f(R) = R-1? {16}: 15. Score 9. Off.
f(R) = floor(R/2)+something. 

Actually let me fit:
{16}: 9
{8}: 3
{4}: 1
{2}: 0
{4,4}: 4
{2,2}: 2
{2,2,2,2}: 6
{2,2,2}: 4
{3,3}: 2
{3,3,3}: 4
{3,3,3,3}: 7
{4,4,4}: 8
{4,4,4,4}: 6
{6,6}: 7
{5,5}: 5
{5,5,5,5}: 6
{6,6,6,6}: 7
{7,7,7,7}: 7
{8,8}: 4 (from {4,4} BBBBBBBB AAAA BBBBBBBB AAAA... wait, length).

Wait I conflated again. Let me clarify: my pair-run lengths.

{8,8} pair-runs: each from 16 B's. 2 runs of 16 B's would be 32 chars, no gap possible. {8,8} good pair runs needs 8+8 = 16 good pairs distributed in 2 runs.

Actually I'm confusing myself. Let me just compute the # of good even pairs each test had.

Wait — I think there's a simpler explanation. Let me hypothesize: score = COUNT of "good even pairs" that are FOLLOWED (or preceded) by another good even pair within distance d. 

Or: score = # of good even pairs that are part of a run of length ≥ 2.

For {16}: 16 good in a run of 16. All ≥2. Count 16. /2 = 8. Need 9.
For {8}: 8 in run of 8. /2 = 4. Need 3.

Doesn't fit.

Let me really focus: I'll guess that score might be:
score = floor( sum_{runs} (R*(R+1)/2) / X )

For {16}: 16*17/2 = 136. /X = 9 → X≈15.
For {8}: 36. /15 ≈ 2.4 → 2. Need 3. Close.
For {4}: 10. /15 = 0.67 → 0. Need 1.

Hmm. Try X=12:
{16}: 11.3 → 11.
{8}: 3 ✓
{4}: 0.83 → 0. Need 1.

Try sum R^2:
{16}: 256. /X = 9 → X≈28.
{8}: 64. /28 = 2.3 → 2.
{4}: 16. /28 = 0.57 → 0.
{4,4}: 16+16=32. /28 = 1.14 → 1.
{2,2,2,2}: 4*4=16. /28 → 0. Need 6.
No.

Try sum R:
{16}: 16. Need 9. /2 = 8. Need 9.
{4,4}: 8. /2 = 4. ✓
{2,2,2,2}: 8. /2 = 4. Need 6. ✗

Hmm. Let me hypothesize score = (# runs)² when uniform-ish:
{16}: 1 run. Score 9. 1² = 1.
{4,4}: 2 runs. Score 4. 2² = 4. ✓!!
{2,2,2,2}: 4 runs. Score 6. 4² = 16. ✗

Almost! For 2 runs got 4 = 2². For 4 runs got 6 not 16.

Or # runs * something:
{4,4}: 2 → 4. Score/runs=2.
{2,2,2,2}: 4 → 6. Score/runs=1.5.
{8,8,8}: 3 → 8. Score/runs=2.67.

Nothing obvious.

Maybe: score = floor((sum_runs / max_pair_run_in_sequence) * something)?

For {16}: max_run=16. sum=16. ratio 1. *9 = 9.
For {8}: max=8. sum=8. ratio 1. *9 = 9. But score 3.

No.

Honestly let me just try to fit a simple regression by gathering more data points. I'll test many configurations.

## 2026-06-28 15:31 — query 234



## 2026-06-28 15:32 — query 240



## 2026-06-28 15:34 — query 249



## 2026-06-28 15:34 — query 252

Interesting! Replacing pos 14,15 with DA in ADAD pattern gave 9, not less.
But (D,A) was supposed to be a bad pair!

Let me reconsider. Position 14 is even, position 15 is odd.
- (D, A) at (14, 15): D is even-pos, A is odd-pos.
- The pair test: x at even ∈ {A,B,C} for good. D is not. So pair (D,A) should be bad.
- Yet score = 9. So bad pair at this position doesn't hurt.

Maybe the bad-pair rule applies only at certain positions (like position 0 only)?

Let me re-test ADAD with breaking at start.

## 2026-06-28 15:34 — query 256

Cap = 9 is masking interior effects. To probe, I need to break enough good pairs to drop below cap.

Key insight remains: position 0,1 matter (one bad pair → -1 from cap). Position 30,31 matter. Other interior positions cap-protected.

Now testing 2 simultaneous breaks: pos 0-1 and 30-31 → score 7 (-2 from cap). So each contributes 1.

Let me check 3 bad pairs (interior + end): pos 0-1, 30-31, 16-17:
DAADADADADADADADDAADADADADADADDA — need to construct this. Pos 0-1 DA, 16-17 DA, 30-31 DA, rest ADAD.

## 2026-06-28 15:35 — query 260

Hmm, mixed results. Let me focus on testing strict configurations.

Key claim to verify: score is determined by a function of (a) total good even pairs, and (b) their distribution.

Let me dump my pair-distribution data:
{16}: 9
{15}: 8 (test had 14 good, 1 bad)
{14}: 7
{13}: 7
{12}: 6 (could be 1 run or 1 bad)
{11}: 5
{10}: 4
{8}: 3 (1 run)
{6}: 2
{4}: 1
{2}: 0
{1}: 0
{0}: 0
{4,4}: 4
{8,8}: ? 
{2,2}: 2
{3,3}: 2
{5,5}: 5
{6,6}: 7
{4,4,4}: 8
{3,3,3}: 4
{2,2,2}: 4
{2,2,2,2}: 6
{3,3,3,3}: 7
{4,4,4,4}: 6
{5,5,5,5}: 6
{6,6,6,6}: 7
{7,7,7,7}: 7
{1,1,1,1,1,1,1,1}: 0
{1,1}: 0
{1,1,1,1}: 0

I notice some "tricky" results. Let me try one approach: maybe each "good pair" contributes positionally, like 9 specific "active" pair-positions. But that's not enough (interior breaks ignored due to cap).

Actually wait — maybe the formula is much simpler than I thought.

Hypothesis: score = max number of NON-OVERLAPPING blocks of 4 chars that are "good 4-mers" of certain type. And max is 9. 

For pure 32 B: floor(32/?) = 9. 32/3.55 = 9.
For ADAD: 32 chars / something.

Or maybe: it's the number of unique 4-mer types? No, BBBB has only one type.

Maybe COUNTING: score = # of "active 4-mer windows" along the sequence?

Let me try: a 4-mer (s[i], s[i+1], s[i+2], s[i+3]) is "active" iff both even-aligned pairs (s[i], s[i+1]) and (s[i+2], s[i+3]) are good, AND aligned (i even).

For BBBB: 4-mer at i=0,4,8,...,28 (8 places). All active. → 8. But score 9.
Hmm 8 ≠ 9.

If aligned at i=0,2,4,...28: 15 positions. For BBBB all good 4-mers. 15? Need 9.

Maybe count 4-mers AT ALL i (overlapping): 29 4-mers. Need 9.

Or maybe specific motif: 4-mer "BBBB" or alike. Hmm.

Let me try: # of i ∈ {0,4,8,...28} (so i = 4k) such that (s[i], s[i+1], s[i+2], s[i+3]) is "active". That's 8 positions. For BBBB all 8 active. Score 9 (>8). Doesn't work.

Hmm. Try score = floor(9 * # active / 16) or similar.

Actually score caps at 9. The cap suggests max = 9, achieved when the sequence has some specific completeness.

For pure 32 B: 9 specific things complete.

Let me try: score = # of "active" 2-character motifs at even positions out of 9 specific motif-positions...

Actually let me make a fitting model. Score is determined by the configuration of good even pairs (positions 0-15 each can be good or bad), so 2^16 possible configs.

For uniform configs:
{16}: 9
{15}: 8 (1 bad anywhere except interior gives 8 — at pos 0 or pos 15 of pair-positions = string positions 0-1 or 30-31)

Let me look at the score as a function of which pair-positions are good vs bad.

Let g_i ∈ {0,1} for i=0..15. Score = f(g_0, g_1, ..., g_15).

From data:
g all 1: 9
g_0=0 rest 1 OR g_15=0 rest 1: 8
g_0=0, g_15=0 rest 1: 7
g_0=0, g_15=0, g_8=0 rest 1: 7

For g all 0: 0.

Let me hypothesize: score = (16 - # bad pairs) / X for some adjustments.

Actually maybe: score = number of good even pairs minus distinct "gap penalties".

Or: score is dictated by the LONGEST RUN of good pairs plus some bonus.

For {16}: longest run = 16, score 9.
For {8}: longest = 8, score 3.
For {4}: 4, score 1.
For {12}: 12, score 6.
For {4,4}: longest = 4, score 4 (longer than {4} alone). So has bonus from second run.
For {8,8}: longest = 8, score should be more than {8}=3.

Let me check the formula:
Score(longest run) (from my data on single runs): R=2:0; R=4:1; R=6:2; R=8:3; R=10:4; R=11:5; R=12:6; R=14:7; R=15:8; R=16:9.

Hmm thresholds: 4→1, 6→2, 8→3, 10→4, 11→5, 12→6, 14→7, 15→8, 16→9. Increment of 2 per +1 score, then 1 per +1 after R=10.

These thresholds look like: R for score s = 2s+2 for s≤4, then thresholds 11,12,14,15,16.

Actually: thresholds 4,6,8,10,11,12,14,15,16. 
For s 1..9: R_s = 4,6,8,10,11,12,14,15,16.
Diff: 2,2,2,1,1,2,1,1.

I want to fit thresholds. Pattern: R_s where s ≤ 4: 2s+2. After that?

OK let me hypothesize: score = sum over runs of some function:
- f(1)=0
- f(2)=0
- f(3)=1 (from {3,3}=2 → 2*f(3)=2, so f(3)=1)
- f(4)=1 or 2 ({4,4}=4 → 2*f(4)=4, f(4)=2; but {4}=1)

So splitting matters. Maybe score = sum f(R_i) + bonus(# runs)?

Linear: f(R)+g(n)
n=1: f(R)+g(1)
n=2 with equal R: 2f(R)+g(2)

For R=4: n=1 → 1 = f(4)+g(1). n=2 → 4 = 2f(4)+g(2). n=3 → 4 = 3f(4)+g(3). n=4 → 6 = 4f(4)+g(4).
Subtract: g(2)-g(1) = 4-1-f(4) = 3-f(4). g(3)-g(1) = 4-1-2f(4) = 3-2f(4). g(4)-g(1) = 5-3f(4).

For R=8: n=1 → 3. n=2 → ? haven't tested. n=3 → 8.
For R=2: n=1 → 0. n=2 → 2. n=3 → 4. n=4 → 6. n=8 → 0!
Linear (n-1): n=1:0, n=2:2, n=3:4, n=4:6. Then n=8:0 breaks.

n=8 R=2 case gave 0. So clearly not linear in n forever.

Maybe there's a "spacing" constraint: too many runs squished together → fewer scores.

Let me check {1,1,1,1,1,1,1,1} also = 0. 8 runs of 1. If 1-runs always contribute 0, then sum = 0 regardless. So f(1)=0 cleanly.

{2,2,2,2}: 4 runs of 2, total 8 pairs. Score 6.
{2,2,2,2,2,2,2,2}: 8 runs of 2, total 16 pairs. Score 0!!

But total pairs same as {16}=9. Hmm.

Wait this needs verification — {2,2,...} with 8 runs would need spacing. Let me think: 8 runs of pair-length 2 = 8 BB-pair blocks = 8 BBBB chunks = 32 B chars with no separators. That's just pure 32 B = {16}. Not {2*8}.

To have 8 distinct pair-runs of 2 each, I need separators between them. Separator = at least 1 bad pair = ≥2 chars. 8 runs of 4 chars each + 7 separators of 2 chars = 32+14 = 46. Doesn't fit.

{2*4} = 4 runs of 2 = 4 BBBB blocks of 4 chars = 16 chars + need separators. 16 + 3*2 (min) = 22 chars + 10 extra. With 4 separators between/around runs of 2 (=4 chars each), filling 32 chars with 16 B chars + 16 A chars in 4 BBBB + 4 AAAA blocks. = BBBBAAAA × 4 = 32. ✓ score 6.

So {2*4} fits exactly. {2*5} needs 20 chars B + ≥4 chars A = ≥24, possible with extras.

Wait, {2*8} would need 32 chars + 14 separator chars = 46. Impossible in 32 chars. So we can't have 8 pair-runs of 2.

But {1*8} is what I tested: BBAA BBAA BBAA... each B-block is 2 chars = 1 pair. 8 BB pairs = 8*1 = 8 pair-runs of 1. Total pairs = 8.

I conflated. {2*8} can't exist. The "BBAABBAA" pattern has pair-runs of 1, not 2.

OK so realistic configs:
- pair-runs of 1: 1 chunk = 4 chars (BBAA or similar). 
- pair-runs of 2: 1 chunk = 8 chars (BBBBAAAA).
- pair-runs of 4: 1 chunk = 16 chars (BBBBBBBBAAAAAAAA).

Wait that's wrong. A "pair-run of length 2" = 2 consecutive good even pairs = 4 chars of B + 0 chars of A. But to be isolated, need bad pairs around.

A B-block of length 4 (4 chars B) → 2 good even pairs at (0,1)(2,3) — if aligned to even start. Pair-run of 2.

Adjacent A-block of length 4 → 2 bad even pairs.

So BBBBAAAA = 4 B + 4 A = 8 chars = 4 even pairs total (2 good + 2 bad).

BBBBAAAA × 4 = 32 chars = 16 even pairs (8 good + 8 bad), in 4 pair-runs of 2.

OK so {2*4} = 4 pair-runs each of length 2 = scores 6.

Now {2*3} would be BBBBAAAA × 3 = 24 chars + 8 A's = 6 good pair-runs of 2... wait BBBBAAAA × 3 = 3 pair-runs of 2.

OK my notation is consistent. Let me get more data.

## 2026-06-28 15:36 — query 263



## 2026-06-28 15:38 — query 275

Symmetric (k B + (32-2k) A + k B):
- 16 B + 0 A + 16 B = 32 B = 9
- 15 B + 2 A + 15 B = 9
- 14 B + 4 A + 14 B = 8
- 13 B + 6 A + 13 B = 7
- 12 B + 8 A + 12 B = 7
- 11 B + 10 A + 11 B = 6
- 10 B + 12 A + 10 B = 5
- 8 B + 16 A + 8 B = 4
- 4 B + 24 A + 4 B = 2 (from earlier)

So even with 16 A's in middle, the score for 8+0+8 = 4 (compare to single L=16 = 3 and L=8 = 1). Splitting boosted from 3 to 4 (and single 8 boosted from 1 to 4).

Pattern of scores for k_B chars on each side:
k=4: 2
k=8: 4
k=10: 5
k=11: 6
k=12: 7
k=13: 7
k=14: 8
k=15: 9
k=16: 9

Score thresholds for 2-symmetric (need k each side):
score≥1: k=? 
score≥2: k=4
score≥3: k=? 
score≥4: k=8
score≥5: k=10
score≥6: k=11
score≥7: k=12
score≥8: k=14
score≥9: k=15

Now compare to single run thresholds for score s:
single: L=8 for 1, L=12 for 2, L=16 for 3, L=20 for 4, L=22 for 5, L=24 for 6, L=28 for 7, L=30 for 8, L=32 for 9.

If we equate L_single = 2*k (since split 2k chars total):
2k=8: k=4 → single score 1, split score (k=4) = 2.
2k=12: k=6 → single 2, split (need to test) = ?
2k=16: k=8 → single 3, split = 4.
2k=20: k=10 → single 4, split = 5.
2k=22: k=11 → single 5, split = 6.
2k=24: k=12 → single 6, split = 7.
2k=28: k=14 → single 7, split = 8.
2k=30: k=15 → single 8, split = 9.

So split=single+1 (mostly)! Splitting gives +1 bonus.

Now 3 blocks vs 1 block of same total:
L=24 single = 6.
3 of L=8 = {4,4,4} pair-runs = 8 (from data).
Diff +2.

Could there be a "bonus per split"? Each additional block contributes +1?
- 1 block of L: score(L)
- 2 blocks of L/2 each: score(L) + 1
- 3 blocks of L/3 each: score(L) + 2?
- 4 blocks of L/4 each: score(L) + 3?

Check 3*8 = 24 → score 8. Single 24 → 6. Diff +2. ✓
Check 4*6 = 24 → score 7. Diff +1. (Not +3 as predicted.)
Check 4*5 = 20 → 6. Single 20 → 4. Diff +2. (Not +3.)
Check 4*4 = 16 → 6. Single 16 → 3. Diff +3. ✓
Check 4*7 = 28 → 7. Single 28 → 7. Diff 0!

So +bonus depends on block size too. Smaller blocks → bigger bonus? Larger blocks → smaller bonus.

For 4 blocks:
size 4: +3 (6 vs 3)
size 5: +2 (6 vs 4)
size 6: +1 (7 vs 6) — wait diff is 7-6=1.
size 7: 0 (7 vs 7)

For 3 blocks:
size 4: 4 blocks total 12 not 12 single = 2. 3 blocks of 4: {3,3,3} → from data = 4. Diff +2.
size 5: 3*5=15 total. {3,3} ... actually pair counts. Let me compute pair runs.
size 6 (12 B chars): 3 blocks of 12 B = not possible in 32 chars (36 needed). 
size 8: 3 blocks of 8 = 24 B total. Single 24 = 6. 3*8 = {4,4,4} pair-runs → 8. Diff +2.

For 2 blocks:
size 4 (8 B total): {2,2} = 2. Single 8 = 3. Diff -1?? wait. {2,2} pair-runs from 2 B-blocks of 4 chars each = 2 pair-runs of 2 each. score 2. Single 8 (=1 B-block of 16 chars = 1 pair-run of 8) = 3.
Hmm wait, "single 8" might mean total 8 B chars vs total 16. Need to compare equal total.
Same total 8 B = 8 chars:
1 B-block of 8 = pair-run {4}: score 1.
2 B-blocks of 4 = pair-runs {2,2}: score 2.
Diff +1.

Same total 16 B:
1 block of 16 chars = {8}: score 3.
2 blocks of 8 chars: ... was tested earlier? Two BBBBBBBB blocks split by A's. With min separator of 1 char A (BBBBBBBB A BBBBBBBB...= 17 chars). To make {4,4} pair-runs we need clear separation.
Hmm I tested 16 B + ... + 16 B which is bunched. Earlier {4,4} from 8 BBs (16 chars total). Wait need to recompute.

Actually I'm confusing notation. Let me reset:
- B-block-length L_B (in chars).
- pair-run-length: number of consecutive good even-pairs from this block.
- For a B-block of length L_B starting at even position, pair-run = floor(L_B/2) if it ends at any position, but if it ends at odd position then the last pair is (B,A) which is bad. So pair-run = floor(L_B/2).

For B-block of length 4 at even start: pair-run = 2.
For B-block of length 8 at even start: pair-run = 4.

So {2,2,2,2} from 4 B-blocks of length 4 each = score 6.
{4} from 1 B-block of length 8 = score 1.

But these have different TOTAL good pairs: {2,2,2,2} has 8 pairs; {4} has 4 pairs. Not equal.

Let me redo comparison:
8 good pairs:
- {8}: 1 block of length 16 chars → score 3.
- {4,4}: 2 blocks of 8 chars each → ? need to test.
- {2,2,2,2}: 4 blocks of 4 chars each → score 6.
- {1,1,...8 times}: 8 blocks of 2 chars each → score 0.

So with same 8 good pairs, score varies 0-6 depending on structure!

That's a huge dispersion. The score is not monotonic in # good pairs.

The sweet spot seems to be ~4 blocks. Let me focus: maybe score directly depends on # of B-BLOCKS (regardless of size, up to a point)?

For uniform N blocks of equal size, score(N, L) data:
N=1: L=4:0, L=8:1, L=12:2, L=16:3, L=20:4, L=24:6, L=28:7, L=32:9.
N=2: L=4 each (total 8 B): need test; L=8 each (16 B): need test ({4,4} from BBBBBBBB + ... + BBBBBBBB); L=12 each (24 B): tested as 7; L=14 each (28 B): tested 8; L=10 each (20 B): tested 5; L=15 each (30 B): tested 9 (15+15 with AA).

Actually I tested 15+15 = 9. And 14+14 (with 4 A's) = 8. 12+12+8 A's between = 7. 10+10 = 5. 

Let me just see N=2 scores vs total B:
2*4 = 8 B: ? 
2*8 = 16 B: ?
2*10 = 20 B: 5
2*12 = 24 B: 7
2*14 = 28 B: 8
2*15 = 30 B: 9

vs N=1 scores at same total:
1*8 = 8 B: 1
1*16 = 16 B: 3
1*20 = 20 B: 4
1*24 = 24 B: 6
1*28 = 28 B: 7
1*30 = 30 B: 8

So N=2 - N=1: 1, 1, 1, 1 (for L=20,24,28,30). Splitting gives +1.

For N=3:
3*8 = 24 B: 8
3*10 = 30 B: 9

vs N=1 at same total:
24: 6 → N=3 gives +2.
30: 8 → N=3 gives +1.

For N=4:
4*4 = 16 B: 6 vs N=1=3 → +3
4*5 = 20 B: 6 vs N=1=4 → +2
4*6 = 24 B: 7 vs N=1=6 → +1
4*7 = 28 B: 7 vs N=1=7 → 0

So bonus = max(0, c - (size - 4)) where c depends on N?

Let me see: bonus(N=4, L=4)=3; L=5: 2; L=6: 1; L=7: 0. Linear in L: bonus = 7-L = 4 - (L-3).
bonus(N=3, L=8)=2; L=10: 1. bonus = 4-(L-6)? 4-2=2; 4-4=0; no.

Hmm. Let me try: total contribution = (# pair-good blocks * some factor) + (# of good pairs).

For total B = T, in N blocks of equal size L = T/N:
# pair good = T/2 (if blocks at even positions and L even).
For N=1, T=32: pair good = 16, score 9.

Maybe score = min(9, (pair_good + N - 1)) ?
N=1, T=32: 16+0=16 → min(9,16)=9 ✓
N=2, T=30: 15+1=16 → 9 ✓
N=2, T=24: 12+1=13 → min 9 vs 13 = 9 (but score 7) ✗

Not.

Maybe score = floor((pair_good + bonus*N)/k):
Too many free parameters.

Let me try once more: score might simply be COUNT of some specific motif. Maybe motif of length 4 at certain positions.

Let me count "BBBB" (4 consecutive B's or any 4 chars all in {B,C}) at positions divisible by 4:
For 32 B: positions 0,4,8,...28 — 8 blocks of BBBB. Score 9. Doesn't match.

What if score = # of positions i ∈ {0..31} such that s[i] AND s[i-1] AND s[i+1] form a "good triple"?

Let me give up on cracking the exact formula and move to gathering more diverse data, then make my best guess at structure.

## 2026-06-28 15:39 — query 286

Complete single-run B table at start:
L: 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32
S: 0 0 0 0 1 ? 1  1  2  ?  2  2  3  3  4  4  4  4  5  5  6  6  6  6  7  7  8  8  9

Predicted L=9: between 8 and 10. Likely 1. L=13: 2.

So thresholds:
score s ≥ 1: L=8
score s ≥ 2: L=12
score s ≥ 3: L=16 (or 17?)
score s ≥ 4: L=18
score s ≥ 5: L=22
score s ≥ 6: L=24
score s ≥ 7: L=28
score s ≥ 8: L=30
score s ≥ 9: L=32

Hmm wait L=17 gave 3 and L=18 gave 4. So threshold for 4 is L=18, not 20!
And L=16 = 3, L=17 = 3, L=18 = 4.

Updated thresholds:
s ≥ 1: L=8
s ≥ 2: L=12
s ≥ 3: L=16
s ≥ 4: L=18
s ≥ 5: L=22
s ≥ 6: L=24
s ≥ 7: L=28
s ≥ 8: L=30
s ≥ 9: L=32

Differences: 4,4,4,2,4,2,4,2,2. Mostly +4 or +2.

Hmm new data L=18 = 4 conflicts with my earlier hypothesis. Let me test more around 17-19 to be sure.

Actually I tested L=20 earlier multiple times = 4. Now L=18 = 4. So L=18,19,20,21 all = 4. Threshold for 4 is L=18.

Let me re-examine L=17 = 3. 17 chars of B at start, then 15 A's.
Even pairs: (0,1)BB ... (16,17)=(B,A) bad. Good even pairs = 8 (positions 0,2,4,6,8,10,12,14). 8 pairs → score 3 (matches earlier {8}=3).

L=18: even pairs (0,1)BB...(16,17)BB, (18,19)=AA. Good even = 9 pairs at positions 0,2,4,6,8,10,12,14,16. 9 pairs → score 4 (per single-run table).

So good even pairs vs score for single B-run at even start:
1 pair (L=2-3): 0
2 (L=4-5): 0
3 (L=6-7): 0
4 (L=8-9): 1
5 (L=10-11): 1
6 (L=12-13): 2
7 (L=14-15): 2
8 (L=16-17): 3
9 (L=18-19): 4
10 (L=20-21): 4
11 (L=22-23): 5
12 (L=24-25): 6
13 (L=26-27): 6
14 (L=28-29): 7
15 (L=30-31): 8
16 (L=32): 9

So pair count → score:
1: 0
2: 0
3: 0
4: 1
5: 1
6: 2
7: 2
8: 3
9: 4
10: 4
11: 5
12: 6
13: 6
14: 7
15: 8
16: 9

This is now cleaner. Maps roughly to:
score = floor((2k-?)/3) — let me check:
k=4: (8-?)/3=1 → ?=5. (8-5)/3=1 ✓
k=8: (16-5)/3=3.67→3 ✓
k=12: (24-5)/3=6.33→6 ✓
k=16: (32-5)/3=9 ✓
k=10: (20-5)/3=5 (need 4) ✗

Try floor((2k)/3) - 1 or similar:
k=4: 8/3-1 = 1.67 → 1 ✓
k=8: 16/3-1 = 4.33 → 4 (need 3) ✗

Hmm. Look at it as 2-row pattern:
k: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
s: 0 0 0 1 1 2 2 3 4  4  5  6  6  7  8  9

Differences: 0,0,1,0,1,0,1,1,0,1,1,0,1,1,1. Mostly +1 per +1 but with 0's.

The 0's are at k=2,5,7,10,13. Differences: 3, 2, 3, 3.

Hmm let me check increments:
k→k+1: 0,0,1,0,1,0,1,1,0,1,1,0,1,1,1
Skip k=1,2,3: from 4 onward: 0,1,0,1,0,1,1,0,1,1,0,1,1,1.

Looks like alternating "incr/no-incr" pattern. Around k=8 the rate increases.

Actually maybe it's score = round(k * 9/16)?
k=4: 4*9/16 = 2.25 → 2 (need 1) ✗

Try floor((k-1)*9/15)?
k=4: 3*9/15 = 1.8 → 1 ✓
k=8: 7*9/15 = 4.2 → 4 (need 3) ✗

Try floor(k * (k+1) / N):
k=16: 16*17 = 272. /N=9 → N≈30.
k=8: 72/30 = 2.4 → 2 (need 3) ✗

Triangular subset...

Actually let me look: score pattern: 0,0,0,1,1,2,2,3,4,4,5,6,6,7,8,9. Score is non-decreasing. Total = 56 sum.

Differences between successive scores: 0,0,1,0,1,0,1,1,0,1,1,0,1,1,1 (15 diffs).

The 1's appear at positions (k transitions to k+1): k=3→4, 5→6, 7→8, 8→9, 10→11, 11→12, 13→14, 14→15, 15→16.

Positions of 1's: 3,5,7,8,10,11,13,14,15 (9 positions).
Positions of 0's: 1,2,4,6,9,12 (6 positions).

Look at 1's positions: k = 3,5,7,8,10,11,13,14,15.
Look at 0's positions: k = 1,2,4,6,9,12.

Hmm. Let me see the score as floor(k(k+1)/(some count))?

Hmm, k → s mapping:
4→1: ratio 0.25
8→3: 0.375
12→6: 0.5
16→9: 0.5625

Looks like s ≈ k²/something:
k²/16: 1, 4, 9, 16. Vs s: 1,3,6,9. Close — s ≈ k²/16 - small.
floor(k²/16 - 1)?
k=4: 0 ✗
k=8: 3 ✓
k=12: 8 ✗ (need 6)

floor((k²-k)/something):
k=4: 12. k=8: 56. k=12: 132. k=16: 240.
Vs s 1, 3, 6, 9. Ratios: 12, 18.67, 22, 26.67. Not.

Maybe rule is just complicated. Let me see if score is well-fit by floor((k-3)/(some piecewise)).

Actually score s(k) for single run:
k: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
s: 0 0 0 1 1 2 2 3 4  4  5  6  6  7  8  9

Hmm... let me check: s(k) = floor((k-1)*9/15)?
k=4: 1.8 → 1 ✓
k=8: 4.2 → 4 (need 3) ✗

Or s(k) = round((k-?)*9/?):
Wanted (1,4),(2,8),(3,12),(4,18),(5,22),(6,24),(7,28),(8,30),(9,32).
Or rather min k for score s:
s: 1 2 3 4 5 6 7 8 9
k: 4 6 8 9 11 12 14 15 16

Differences in k: 2,2,1,2,1,2,1,1.

Hmm. k_min(s) = ?

s + (s-1)/2 something? 
s=1: 4 = 1+3? = 1*4.
s=2: 6 = 2*3.
s=3: 8 = 3+5? = 2*4? = 8.
s=4: 9 = 2*4.5 = 9.
s=5: 11.
s=6: 12 = 2*6.

Look at k for s: 4,6,8,9,11,12,14,15,16.

s=1: 4
s=2: 6 = 4+2
s=3: 8 = 6+2
s=4: 9 = 8+1
s=5: 11 = 9+2
s=6: 12 = 11+1
s=7: 14 = 12+2
s=8: 15 = 14+1
s=9: 16 = 15+1

Pattern of increments: 2, 2, 1, 2, 1, 2, 1, 1.
Or: 2,2,1,2,1,2,1,1.

Maybe k_min(s) = ceil((s + 9) * c)?
s=1: ceil(10c). For k=4 → c=0.4.
s=9: ceil(18*0.4)=8. Need 16. No.

Or k_min(s) = ceil(s*c + d):
s=1: 4 = c+d.
s=9: 16 = 9c+d.
Solve: 8c=12, c=1.5, d=2.5. So k_min(s)=ceil(1.5s+2.5)=ceil((3s+5)/2).
s=1: ceil(4)=4 ✓
s=2: ceil(5.5)=6 ✓
s=3: ceil(7)=7 (need 8) ✗

Try (3s+7)/2:
s=1: 5 (need 4) ✗

Doesn't work cleanly.

What if it's a sum: s = max{m : sum_{i=1}^{m} a_i ≤ k} where a_i values are 4,2,2,1,2,1,2,1,1?

OK let me just accept that the score function is positional and complex, and move on.

Key learnings:
1. Cap at 9. So max achievable is 9.
2. Many sequences score 9: any "regular" pattern with valid pair structure throughout.
3. There seems to be a specific scoring that involves "good even-aligned pairs".
4. Good even pairs: x ∈ {A,B,C}, y ∈ {B,C,D}, except (A,C) is bad. So 8 of 16 pair types are good.

I'll focus remaining experiments on confirming the model and exploring edge cases of D vs A and B vs C.

## 2026-06-28 15:39 — query 295

All "bad pair" types at pos 0,1 give -1 from cap of 9: score 8.
Good pair types at pos 0,1 give 9 (no loss).

So pair-rule confirmed: each "bad" pair at position 0,1 costs 1.

Let me verify the same at pos 30,31 (already tested some).

I've gathered enough data. My BEST theory:
- Sequences are evaluated by pair-structure on even-aligned positions.
- Good pair (x,y) at positions (2i, 2i+1):
  - x ∈ {A, B, C}
  - y ∈ {B, C, D}
  - (x, y) ≠ (A, C)
- 8 good pair types, 8 bad pair types.
- Score = some function of the configuration of 16 pair slots (good vs bad), CAPPED at 9.
- Cap of 9: many configurations reach the cap; below the cap, position and run structure of good pairs matters in complex ways.

The exact below-cap formula is complex; my best fit involves:
- Sum of good pair contributions
- Bonus for splitting into multiple blocks
- Particular weighting for edge positions (0-1 and 30-31)

For the rest of the experiments, let me probe specific predictions and refine.

## 2026-06-28 15:40 — query 303

CDCD x6 (12 good pair-positions) + DCDC x2 (4 bad pair-positions) = 6.
Matches single-run table for 12 good pairs = 6. So when good pairs are contiguous from start, score follows that table.

Let me commit to the model:
- Pair-positions 0..15 are each independently "good" or "bad" based on (s[2i], s[2i+1]).
- Score is a function f({good_0, good_1, ..., good_15}) capped at 9.

Now I want to test: when all 16 good, score = 9. When 0 good, score = 0.

For uniform contiguous good runs starting at pair-pos 0:
1 good → 0
2 → 0
3 → 0
4 → 1
5 → 1
6 → 2
7 → 2
8 → 3
9 → 4
10 → 4
11 → 5
12 → 6
13 → 6
14 → 7
15 → 8
16 → 9

For uniform contiguous good runs NOT at pos 0 (need to check positional effect).

## 2026-06-28 15:41 — query 320

ABCD with (A,C) at pos 0-1 (bad pair) = 8. Confirms pair rule for pos 0-1.

I'm running low. Let me synthesize my final theory and run remaining experiments to confirm.

FINAL THEORY (best guess):
1. Each consecutive even-aligned pair (s[2i], s[2i+1]) for i=0..15 is classified as good or bad.
2. Good pair (x,y): x ∈ {A,B,C}, y ∈ {B,C,D}, and (x,y) ≠ (A,C). 8 of 16 possible pairs are good.
3. Score function f(g_0, ..., g_15) is capped at 9.
4. Below cap, score depends on distribution: contiguous good pairs from start of pair-sequence map to the threshold table 1→4 pairs, 2→6, etc.
5. Splitting good pairs into multiple runs gives bonus that depends on # runs and average size.

The exact function below cap is complex but probably involves:
- score = min(9, sum over pair-runs of f(R)) where f(R) approximates floor((R-1)/something) plus a positional bonus.

Or maybe: score = #(good pair-runs of length ≥ 2) * 2 + ... — let me check.

{2,2,2,2}: 4 runs of 2 each (all ≥ 2). 4*2 = 8? Score 6.

How about: score = (sum over runs of R) - (sum over BAD-runs of B), with some weights?

Actually, let me try: maybe score = (# pair-positions that are good AND have a good neighbor pair-position).

For {16}: every pair has 2 good neighbors. # = 16. Score 9.
For {8} at start (pair-pos 0-7 good, 8-15 bad): 
- pair 0: 1 good neighbor (pair 1)
- pair 1-6: 2 good neighbors each (except pair 7 has only 1)
- pair 7: 1 good neighbor
- pairs 8-15: 0 good neighbors (themselves bad)
Total positions with ≥1 good neighbor: 8 (the good ones, since each has at least 1 good neighbor except isolated). Score 3.

For {2,2,2,2}: each good pair has 1 good neighbor. # = 8. Score 6. So count of good pairs with ≥1 good neighbor = 8, but score 6 ≠ 8.

For {1,1,...}: 0 with neighbors. Score 0. ✓

This is the # good pair-positions that aren't isolated. Doesn't quite match.

Let me look at:
{16}: max(s) = 9, all 16 good, very long chain.
{8}: 8 good pairs in 1 chain. Score 3.
{4}: 4 good, 1 chain. Score 1.
{2}: 2 good. Score 0.
{4,4}: 8 good, 2 chains. Score 4.
{2,2}: 4 good, 2 chains. Score 2.
{2,2,2}: 6 good, 3 chains. Score 4.
{2,2,2,2}: 8 good, 4 chains. Score 6.
{3,3,3}: 9 good, 3 chains. Score 4.
{3,3,3,3}: 12 good, 4 chains. Score 7.
{4,4,4}: 12 good, 3 chains. Score 8.
{4,4,4,4}: 16 good, 4 chains. Score 6.
{6,6}: 12 good, 2 chains. Score 7.

Hmm note: {4,4,4,4} = 16 good but only score 6. While {16} = 16 good = 9. So # good can't determine.

What's different? {16}: one continuous chain. {4,4,4,4}: 4 chains of 4.

For {4,4,4,4}: pair pos 0-3, 4-7, 8-11, 12-15. Wait that's contiguous! That IS {16}!

Wait {4,4,4,4} means 4 separate chains of 4 good pairs each. They need bad pair separators. So minimum pair positions used: 4*4 + 3*1 = 19 > 16. Impossible.

So {4,4,4,4} can't actually exist in 16 pair positions. My data above was for 4 blocks of 4 B-chars each (BBBB AAAA × 4 = 32 chars), which gives {2,2,2,2} in pair terms.

So {4,4,4,4} in pair terms is impossible! My earlier description was wrong.

Let me re-derive pair-runs for {4*4 B-blocks}:
BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA = 4 B-blocks of 4 chars each. 
Pair structure: pair 0 (chars 0-1) = BB good. pair 1 (chars 2-3) = BB good. pair 2 (chars 4-5) = AA bad. pair 3 (chars 6-7) = AA bad. Then repeat: pair 4 = BB good, pair 5 BB good, pair 6 AA bad, pair 7 AA bad. ...
So good pair-positions: 0,1,4,5,8,9,12,13. Bad: 2,3,6,7,10,11,14,15.
Pair-runs: {2,2,2,2} (4 runs of 2 each, separated by bad pairs of run-length 2 each).
Total good = 8. Score 6.

OK so {2,2,2,2} = 4 B-blocks of length 4 chars each.

Re-check my data with proper notation:
B-block-lengths → pair structure:
- {16 B} = single B-block of length 32 = pair-runs {16}. Score 9.
- {16 chars B at start} = single B-block length 16 = pair-runs {8}. Score 3.
- 4 B-blocks length 8 each = need 32+3*≥1 chars = at least 35. Impossible.
- 3 B-blocks length 8 each = 24+2*4 = 32. Pair-runs: B-block 0-7 → pairs 0-3 good. Then AAAA pos 8-11 → pairs 4-5 bad. B-block 12-19 → pairs 6-9 good. Then AAAA pos 20-23 → pairs 10-11 bad. B-block 24-31 → pairs 12-15 good.
  Good pair-positions: 0,1,2,3,6,7,8,9,12,13,14,15. Bad: 4,5,10,11.
  Pair-runs: {4,4,4} (run lengths). Total good = 12. Score 8.

So {4,4,4} = 12 good in 3 runs of 4 each → score 8.

Now we have for total good = 12:
{12}: 1 run = score 6.
{6,6}: 2 runs of 6 = score 7.
{4,4,4}: 3 runs of 4 = score 8.
{3,3,3,3}: 4 runs of 3 = score 7.

Score vs # runs (n) for 12 good pairs:
n=1: 6
n=2: 7
n=3: 8
n=4: 7

For 8 good pairs:
{8}: 3
{4,4}: 4
{2,2,2,2}: 6

n=1: 3
n=2: 4
n=4: 6

For 16 good pairs:
n=1: 9 (cap)

For 24 good pairs — impossible (only 16 pair-positions).

Hmm but cap... let me hypothesize: score = (sum over runs of f(R)) + g(# runs).

But for n=4 (12 good): {3,3,3,3} = 7. {4,4,4}=8. So fewer but bigger runs help. n affects but R distribution too.

Let me consider: score = min(9, sum_{runs} (R + n - 1))? For {12}: 12 + 0 = 12, cap 9. ✓ score 9. But actual 6.

OK, this isn't fitting cleanly. Let me just empirically test more configurations to fill in the table for systematic study.

## 2026-06-28 15:43 — query 336

Wait this sequence has 5 BBBB runs! Let me recount.

BBBBBBBB ACAC BBBB ACAC BBBB ACAC BBBB.
Positions: 0-7 B, 8-11 AC, 12-15 B, 16-19 AC, 20-23 B, 24-27 AC, 28-31 B.

Pairs: 0-1 BB G, 2-3 BB G, 4-5 BB G, 6-7 BB G, 8-9 AC BAD, 10-11 AC BAD, 12-13 BB G, 14-15 BB G, 16-17 AC BAD, 18-19 AC BAD, 20-21 BB G, 22-23 BB G, 24-25 AC BAD, 26-27 AC BAD, 28-29 BB G, 30-31 BB G.

Good: 0,1,2,3,12,13,20,21,28,29 → wait 10 good positions in {4, 2, 2, 2} = 10 good in 4 runs. Score 7.

Wait actually runs are {4 (pair-pos 0-3), 2 (pair-pos 6-7), 2 (pair-pos 10-11), 2 (pair-pos 14-15)}. = {4,2,2,2}. Score 7.

OK so {4,2,2,2} = 7.
{2,2,2,2}: 6.
{6,2,2}: 6.
{5,5}: 5.
{6,4}: 5.
{10}: 4.

So 4 runs with mix > 3 runs > 2 runs > 1 run. More runs = better, but R distribution matters.

I think the score is approximated by: # of pair-runs + (sum of run lengths)/something.

Let me hypothesize: score = floor((# runs + total_good)/k) for some k.

{10}: 1 + 10 = 11. /X = 4. X = 2.75.
{5,5}: 2 + 10 = 12. /2.75 = 4.36 → 4. But got 5. ✗

Or: score = # runs + sum f(R) for f(R) = floor((R-2)/2) or similar:
{10}: 1 + (10-2)/2 = 1+4 = 5. Need 4. Off.
{5,5}: 2 + 2*1.5 = 5. ✓
{4,4}: 2 + 2*1 = 4. ✓
{2,2,2,2}: 4 + 0 = 4. Need 6. ✗

Try: score = #runs + sum floor(R/2):
{10}: 1+5=6. Need 4. ✗

score = sum (R+1) capped: 
{10}: 11. Cap 9. ✓ for >=9 cases.
{5,5}: 12. Need 5. ✗

score = max(0, sum R - max_R) + ?:
{10}: 0. ✗
{5,5}: 5. ✓
{4,4}: 4. ✓
{2,2,2,2}: 6. ✓ (8 - 2 = 6)
{6,6}: 6. Got 7. Close.
{3,3,3,3}: 9 (12-3). Got 7. ✗

So {2,2,2,2} (4 runs): total 8 - max 2 = 6 ✓ but {3,3,3,3}: 12-3=9, score 7.

What about sum R - (max R OR something else)?
For {2,2,2,2} = 8-2 = 6 ✓
For {3,3,3,3} = 12-3 = 9, but got 7.

Maybe score = sum (R - 1) + (#runs ≥ something)?
{4,4,4,4} pair-runs (12 good total) = no wait {4,4,4} = 12.
{4,4,4}: sum(R-1) = 3*3 = 9. Got 8.
{6,6}: 5*2 = 10. Got 7.
{3,3,3,3}: 2*4 = 8. Got 7.
{2,2,2,2}: 1*4 = 4. Got 6.

Doesn't fit linearly.

OK I'll commit my best model: it's a complex piecewise function. The big-picture rules I'm confident in:
1. Pair-positions on even alignment.
2. Good pair rule: x ∈ {A,B,C}, y ∈ {B,C,D}, except (A,C).
3. Score caps at 9.
4. Below cap, structure matters: # of runs and run lengths.

Let me use remaining experiments to verify edge cases and explore.

## 2026-06-28 15:48 — query 387

3-letter cycle permutations scores:
ABC: 7
BCA: 7
CAB: 6
ACB: 4
BAC: 4
CBA: 6

Looking at these:
- ABC, BCA: 7 (these are cyclic shifts of "ABC" forward)
- CAB: 6 (other cyclic shift of "ABC" forward)
- ACB: 4 (cyclic shift of "ACB" forward)
- BAC, CBA: 4, 6 (cyclic shifts of "ACB" backward = ABC reversed)

Hmm.

Now let me apply my "good even pair" rule:
ABC repeat: pos 0=A,1=B,2=C,3=A,4=B,5=C,...
Even pairs: (0,1)AB G, (2,3)CA bad, (4,5)BC G, (6,7)AB G, (8,9)CA bad, ...
Pattern G B G G B G G B G G B G G B G G. 
Pair pos 0,2,3,5,6,8,9,11,12,14,15 good. 11 good. 
Pair-runs: 1, 2, 2, 2, 2, 2. = {1,2,2,2,2,2}. Score 7. ✓ matches earlier ABC result.

BCA repeat: pos 0=B,1=C,2=A,3=B,4=C,5=A,6=B,...
Even pairs: (0,1)BC G, (2,3)AB G, (4,5)CA bad, (6,7)BC G, (8,9)AB G, (10,11)CA bad,...
Pattern G G B G G B G G B G G B G G B G.
Good at pair pos 0,1,3,4,6,7,9,10,12,13,15. 11 good.
Pair-runs: 2,2,2,2,2,1. = {2,2,2,2,2,1} ~ same as {1,2,2,2,2,2}. Score 7. ✓

CAB repeat: pos 0=C,1=A,2=B,3=C,4=A,5=B,6=C,...
Even pairs: (0,1)CA bad, (2,3)BC G, (4,5)AB G, (6,7)CA bad, (8,9)BC G, (10,11)AB G,...
Pattern B G G B G G B G G B G G B G G B.
Good at pair pos 1,2,4,5,7,8,10,11,13,14. 10 good.
Pair-runs: 2,2,2,2,2 = {2,2,2,2,2}. Score 6. ✓ (less than 11 good versions).

ACB repeat: pos 0=A,1=C,2=B,3=A,4=C,5=B,6=A,...
Even pairs: (0,1)AC bad, (2,3)BA bad, (4,5)CB G, (6,7)AC bad, (8,9)BA bad, (10,11)CB G,...
Pattern B B G B B G B B G B B G B B G B.
Good at pair pos 2,5,8,11,14. 5 isolated. Score 4.

BAC repeat: pos 0=B,1=A,2=C,3=B,4=A,5=C,6=B,...
Even pairs: (0,1)BA bad, (2,3)CB G, (4,5)AC bad, (6,7)BA bad, (8,9)CB G, (10,11)AC bad,...
Pattern B G B B G B B G B B G B B G B B.
Good at pair pos 1,4,7,10,13. 5 isolated. Score 4.

CBA repeat: pos 0=C,1=B,2=A,3=C,4=B,5=A,6=C,...
Even pairs: (0,1)CB G, (2,3)AC bad, (4,5)BA bad, (6,7)CB G,...
Pattern G B B G B B G B B G B B G B B G.
Good at pair pos 0,3,6,9,12,15. 6 isolated. Score 6.

Now compare same {1*6} pattern:
- CBA: 6 isolated good (positions 0,3,6,9,12,15). Score 6.
- BBAABB pattern: 8 isolated 1's at positions 0,2,4,6,8,10,12,14. Score 0.

Difference: CBA has gap-of-2 between good (positions 0→3 is distance 3, so gap of 2 bad pairs). BBAA has gap-of-1 between good (positions 0→2 is distance 2, gap 1).

Maybe isolated 1-runs CONTRIBUTE if the GAP between them is large enough?

For CBA: gap = 2 bad pairs between good 1-runs → 6 good positions → score 6.
For BBAA: gap = 1 bad pair → 0 score.

Test: try gap of 2 with B's. Sequence: BB AAAA BB AAAA ... = pair (0,1)BB G, (2,3)AA bad, (4,5)AA bad, (6,7)BB G, (8,9)AA bad, (10,11)AA bad, (12,13)BB G,...
That's gap of 2 bad pairs between good 1-runs. Period 6 = BBAAAA. In 32 chars: BBAAAA BBAAAA BBAAAA BBAAAA BBAAAA BB. = 30 + 2 = ah 5 full periods = 30 chars + 2 extra. 

Good pair-positions in BBAAAA repeat: 0, 3, 6, 9, 12, 15. 6 isolated 1-runs. Same as CBA pattern in pair positions!

Predicted score: 6 (same as CBA).

## 2026-06-28 15:49 — query 395

n isolated good pairs (gap 2 between):
n=2: 1
n=3: 2
n=4: 4
n=5: 4
n=6: 6

Jumps at n=4 (+2) and n=6 (+2). Increments 1, 1, 2, 0, 2.

Interesting irregular pattern.

OK I clearly don't have the formula. Let me commit my final summary to the notebook.

FINAL THEORY:
The biology of this world rewards structured chemical patterns built from 4 monomers {A, B, C, D}, with the following key rules I've inferred:

1. Sequences are 32 characters long. Max achievable score = 9.

2. Score depends on "good even-aligned pairs" — pairs of adjacent characters at positions (2i, 2i+1):
   - A pair (x, y) is "good" iff: x ∈ {A,B,C}, y ∈ {B,C,D}, and (x,y) ≠ (A,C).
   - 8 good pair types: {BB, CC, BC, CB, BD, CD, AB, AD}.
   - 8 bad pair types: {AA, AC, BA, CA, DA, DB, DC, DD}.

3. Score is a function of which of the 16 pair positions are good. It is:
   - Position-invariant (translation symmetry of good pair-runs).
   - Capped at 9.
   - For a single contiguous block of g good pairs: score follows a piecewise threshold:
     g=0-3:0, g=4-5:1, g=6-7:2, g=8:3, g=9-10:4, g=11:5, g=12-13:6, g=14:7, g=15:8, g=16:9.
   - For multiple separated good-pair-runs: there's a "split bonus" that can be significant.
   - Some bonus configurations: {4,4,4}=8, {5,5,5}=9, {2,2,2,2}=6, etc.

4. Many distinct sequences reach the cap of 9, including:
   - Pure monomer chains: BBBB..., CCCC...
   - Period-2 patterns: BCBC, CBCB, ABAB, ADAD, BDBD, CDCD
   - Period-4 patterns: ABCD, CDAB, ABCB, CBCD, BCCD, ABBB, CCCB, CCBC, ABCC, ...
   - Most sequences with all even-aligned pairs being "good"

5. The "biology" appears to involve a pairing/dimerization rule where positions are paired even-to-odd, and the chemistry of each pair determines its activity. D acts as "acceptor-only" (cannot initiate a pair); A acts as "donor-only" (cannot receive). B and C are bidirectional, but the specific (A,C) pair fails (perhaps steric).

I'll spend remaining experiments to confirm and explore.

## 2026-06-28 15:52 — query 428

FINAL THEORY (revised):

The organism evaluates 32-char sequences over {A,B,C,D}. Score caps at 9. The scoring involves:

1. EVEN-ALIGNED PAIRS: Pairs (s[2i], s[2i+1]) for i=0..15 are the fundamental units.

2. PAIR CLASSIFICATION: A pair (x,y) is "good" iff:
   - x ∈ {A,B,C} (i.e., not D)
   - y ∈ {B,C,D} (i.e., not A)
   - AND (x,y) ≠ (A,C)
   8 good pair types: BB, CC, AB, AD, BC, BD, CB, CD
   8 bad pair types: AA, AC, BA, CA, DA, DB, DC, DD

3. SCORE FORMULA (approximate): The score is determined by the configuration of which of the 16 pair-positions are good vs bad. It is:
   - Position-invariant (shifting the pattern doesn't change score)
   - Capped at 9
   - For a single contiguous good-pair run of length g:
     g=1-3: 0; g=4-5: 1; g=6-7: 2; g=8: 3; g=9-10: 4; g=11: 5; g=12-13: 6; g=14: 7; g=15: 8; g=16: 9
   - For multiple separated good-pair runs:
     * More runs generally give higher score (more "diversity bonus")
     * Larger gaps between runs (≥2 bad pairs) give higher score than smaller gaps (1 bad pair)
     * Pattern of run sizes matters: balanced runs > skewed runs
   - The combination of these factors is complex and not reducible to a simple formula I've fully derived.

4. ODD-ALIGNED PAIRS: Do not contribute (confirmed via AABAB... = 0).

5. CHARACTER ROLES:
   - B, C: "bidirectional" — work as both first and second in pairs
   - A: "donor only" — works as first char of pair (except (A,C))
   - D: "acceptor only" — works as second char of pair

This is reminiscent of a chemical bonding rule: think of A as electron donor, D as acceptor, B/C as flexible reactants. Bonds form on even-odd phasing.

PREDICTIONS:
- BBBB...B and similar uniform good patterns hit cap 9.
- ABCD repeats hit cap 9.
- ANY sequence with all 16 even pairs good = 9.
- Sequences with isolated single good pairs need ≥3-char period (gap ≥2 pair positions) to contribute.

I've used 428/500 experiments. Will continue exploring to refine and confirm.

## 2026-06-28 15:55 — query 461

CONFIRMED THEORY (final):

1. EVEN-ALIGNED PAIR RULE: For positions (2i, 2i+1), the pair (x, y) is "good" iff:
   x ∈ {A, B, C} AND y ∈ {B, C, D} AND (x, y) ≠ (A, C)
   
   8 good pair types: AB, AD, BB, BC, BD, CB, CC, CD
   8 bad pair types: AA, AC, BA, CA, DA, DB, DC, DD

2. ODD-ALIGNED PAIRS DON'T MATTER (confirmed by AABABAB... = 0)

3. SCORE depends ONLY on the 16 binary indicators (g_0, ..., g_15) of which pair-positions are good.

4. SCORE function:
   - Capped at 9
   - Position-invariant (shifts don't change score)
   - Single contiguous run of g good pairs:
     g: 1-3=0, 4-5=1, 6-7=2, 8=3, 9-10=4, 11=5, 12-13=6, 14=7, 15=8, 16=9
   - Splitting good pair-runs adds bonus, but only if separated by ≥2 bad pair-positions
   - Multiple runs with adequate spacing → higher scores than single contiguous run
   
5. INTERESTING EXAMPLES:
   - {16} = 9 (cap, all good)
   - {8} = 3 (single 8-run)
   - {4,4} with ≥2-pair gap = 4 (+1 from single 8-run)
   - {2,2,2,2} with 2-pair gaps = 6 (much more than single 8-run!)
   - {1,1,1,1,1,1} with 2-pair gaps = 6 (isolated 1-runs spaced out can contribute!)
   - {1,1,1,1,...} with 1-pair gap = 0 (too tight)
   - {4,4,4} with 2-pair gap = 8
   - {4,4,4} with 1-pair gap = 7

INTERPRETATION (speculative): This world's "biology" forms dimer bonds between adjacent positions, with specific chemistry (D=acceptor, A=donor, B/C=flexible). Score reflects how well these bonds tile the 16 pair-slots. Cooperative effects between distantly-spaced bond clusters contribute positively (mimicking some kind of allostery or domain organization).

Used 461/500 experiments. 39 left to consolidate.

## 2026-06-28 15:56 — query 473

FINAL COMPLETE THEORY (v2):

The biology of this world evaluates 32-character sequences over {A,B,C,D} via a complex but partially decoded scoring function. Maximum score = 9. Many sequences achieve 9.

CORE MODEL (verified, high confidence):
1. The 16 "pair-positions" are defined by even-aligned pairs (s[2i], s[2i+1]).
2. A pair (x,y) is "good" iff x∈{A,B,C} AND y∈{B,C,D} AND (x,y)≠(A,C).
3. 8 good pair types: {AB, AD, BB, BC, BD, CB, CC, CD}.
4. 8 bad pair types: {AA, AC, BA, CA, DA, DB, DC, DD}.
5. Score depends only on the 16-bit configuration of "good" indicators (g_0,...,g_15).
6. Odd-aligned pairs do not affect scoring.
7. Score is translation-invariant (shifts of pair-good pattern preserve score).
8. Score is capped at 9.

SCORE FORMULA (partially decoded):
- All 16 good → 9.
- Single contiguous run of g good pairs: thresholds (g→score):
  g=0-3:0, g=4-5:1, g=6-7:2, g=8:3, g=9-10:4, g=11:5, g=12-13:6, g=14:7, g=15:8, g=16:9
- Splitting into multiple runs adds bonus, but only if separated by ≥2 bad pair-positions.
- 1-pair-gap between runs: smaller bonus or no bonus.
- Isolated 1-pair "good" runs contribute if spaced by EVEN gap (2 or 4), not odd gap (1, 3, 5).
- Examples:
  * 6 isolated good with gap 2 (pattern BBAAAA): score 6
  * 6 isolated good with gap 3 (pattern BBAAAAAA): score 0
  * 4 isolated good with gap 4 (pattern BB AAAAAAAA): score 4
  * 3 isolated good with gap 4: score 2

INTERPRETATION:
The "biology" pairs adjacent positions (even+odd) and rewards specific chemical compatibility. Beyond pair-counting, there's a meso-structure: well-spaced pair clusters contribute via what might be analogous to allosteric communication or domain repeats. The gap-parity dependence (evens contribute, odds don't) suggests a wave-like or resonance-based scoring.

USED: 473/500 experiments. 27 remaining for refinement.

## 2026-06-28 15:59 — FINAL

=== FINAL REPORT ===

ORGANISM BIOLOGY (what I've decoded):

Sequences are 32 characters over the alphabet {A, B, C, D}. The organism evaluates them and returns an integer fitness, capped at 9.

CORE DISCOVERY: EVEN-ALIGNED PAIR RULE
The sequence is interpreted as 16 adjacent dimers at fixed even-aligned positions:
pair i = (s[2i], s[2i+1]) for i = 0..15
The odd-aligned pairs (s[1],s[2]), (s[3],s[4]), ... have NO effect on the score (verified by AABAB... = 0 while ABABAB... = 9 — same odd-pair structure, different even-pair structure).

PAIR CLASSIFICATION (8 good + 8 bad, fully mapped):
A pair (x, y) is GOOD iff:
  x ∈ {A, B, C}   (D cannot be the "donor" / first member)
  AND y ∈ {B, C, D}   (A cannot be the "acceptor" / second member)
  AND (x, y) ≠ (A, C)   (one specific exception)

Good pairs: AB, AD, BB, BC, BD, CB, CC, CD
Bad pairs:  AA, AC, BA, CA, DA, DB, DC, DD

This rule was confirmed by exhaustive period-2 testing (BCBC=9, BABA=0, CDCD=9, DCDC=0, ABAB=9, BDBD=9, DBDB=0, ADAD=9, DADA=0, CACA=0, ACAC=0...) and by single-pair substitution at positions 0-1 in an all-B background (every bad pair type cost exactly 1 from the cap, every good pair type cost 0).

Character roles:
  • A = "donor-only" (works as first half of a pair, except not paired with C)
  • D = "acceptor-only" (works as second half of a pair)
  • B, C = bidirectional, freely interchangeable in most contexts

SCORE FUNCTION (partially decoded):
Score depends only on the 16-bit vector of good/bad pair indicators (g_0,...,g_15). It is:
  • capped at 9
  • translation-invariant (shifts preserve score)
  • monotone in subtle ways (more good pairs ≥ less, usually)

For a single contiguous good-pair run of length g, the score thresholds are:
  g  : 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
  s  : 0 0 0 1 1 2 2 3 4  4  5  6  6  7  8  9

For multiple runs separated by bad pairs:
  • Splitting a single run into multiple gives a positive "diversity" bonus
  • A 2-pair-wide bad gap is much more effective than a 1-pair gap
  • Isolated single good pairs (run length 1) contribute IF spaced at "good" periods
    (period-3 in pair-positions, e.g., the CBA character pattern, gives 6 isolated goods → 6;
     while period-2 spacing gives 0)
  • Examples observed:
      {16}=9, {15}=8, {14}=7, {12}=6, {8}=3, {4}=1
      {4,4}=4, {2,2,2,2}=6, {4,4,4} 2-gap = 8, {3,3,3,3} = 7
      6 isolated 1-runs at period 3 = 6
      8 isolated 1-runs at period 2 = 0

I was unable to fit a closed-form formula for the below-cap score; it appears to involve both pair-count and a Fourier-like resonance with respect to the pair-position spacing. My best guess: the organism may have multiple sub-units of length 4-5 that must each be "occupied" by a good pair, with cooperative interactions between distant occupied sub-units.

BEST SEQUENCE (achieves cap 9):
Any sequence in which all 16 even-aligned pairs are "good". Cleanest examples:
  • "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" (all B)
  • "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" (all C)
  • "ABCDABCDABCDABCDABCDABCDABCDABCD" (period 4, all good pairs AB,CD)
  • "BCBCBCBCBCBCBCBCBCBCBCBCBCBCBCBC"
  • "ADADADADADADADADADADADADADADADAD"

WHAT I WOULD TEST NEXT (with more budget):
1. Fully exhaustive enumeration of small good-pair configurations to pin down the closed-form score formula below the cap. Specifically test all 2^16 configurations (too many) or systematic subsets to discover the underlying generating function.
2. Probe whether some longer-range motif (e.g., triple-position interaction) explains the gap-parity / period-3 effects observed in sparse patterns.
3. Test whether the cap of 9 is intrinsic or whether some configuration secretly exceeds it (probably not, given the strong evidence).
4. Verify the "donor/acceptor" character interpretation by testing whether there's a hidden 5th-character behavior (e.g., are A and D truly equivalent as "filler" everywhere? — they appear to be).
5. Explore odd-length sequences (different organism context) — would the rule shift to odd-aligned pairs?

CONFIDENCE:
- Pair classification rule: HIGH (8-fold verified)
- Even-only alignment: HIGH (verified by counterexamples)
- Cap at 9: HIGH
- Below-cap formula: PARTIAL — qualitative trends understood, exact function not nailed down.
