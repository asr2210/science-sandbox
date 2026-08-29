
## 2026-06-28 15:06 — query 0

Starting study. Sequences are length 48 over {A,B,C,D}. 500 experiments budget.

Initial assumptions/hypotheses to test:
- Could be GC-content-like: certain characters preferred
- Could be motif-based: certain k-mers boost/depress score
- Could be positional: certain characters preferred at certain positions
- Could involve pairing/structure: complementary characters at distance
- Could involve composition balance
- Could have start/stop codon-like signals

Plan:
1. First test the 4 homogeneous sequences (AAAA..., BBBB..., CCCC..., DDDD...) to see baseline character preferences
2. Test 2-character alternations (ABAB..., ACAC..., etc.)
3. Test random-looking mixed sequences
4. Probe positional effects by swapping characters at specific positions
5. Look for motifs once we have signal

Starting with all-A homogeneous sequence.

## 2026-06-28 15:06 — query 4

Homogeneous results:
- AAAA...A = 0
- BBBB...B = 9
- CCCC...C = 9
- DDDD...D = 0

Hypothesis: B and C are "good" characters, A and D are "bad". Maybe each B or C contributes ~? 48 of them = 9? Or maybe it's based on some count.

Next: test BCBC alternation and mixed B/C to see if combining them is additive or boosts.

## 2026-06-28 15:09 — query 32

Data so far for single B-runs (rest A):
(8,0), (12,1), (16,1), (20,2), (24,3), (28,4), (32,4), (36,6), (38,6), (40,6), (44,7), (46,7), (48,9)

Two 8-B runs (3×8) = 5. Two 12-B runs = 4. Three 8 = 5. Four 6 = 6. Six 4 = 6.
Single 8-B run = 0 regardless of position.
24 B alternating = 0 (BABA).

Function deterministic. The relationship is non-monotonic which is strange (32→4, 36→6, 40→6, 44→7, 46→7, 48→9).

Possibility: the score might be ⌊(L²/256)⌋ + something? Let me check:
L²/256: 8→0.25, 12→0.56, 16→1, 20→1.56, 24→2.25, 28→3.06, 32→4, 36→5.06, 40→6.25, 44→7.56, 48→9
Floor:    0,    0,    1,  1,    2,    3,    4,    5,    6,    7,    9
Actual:   0,    1,    1,  2,    3,    4,    4,    6,    6,    7,    9

Close! Differences are small (off by 1 in several places). Wait actually L=12 gives 0.56→0 but actual 1. L=20 gives 1.56→1 but actual 2.

Try ROUND(L²/256):
12→1✓, 16→1✓, 20→2✓, 24→2 (got 3)✗, 28→3 (got 4)✗, 32→4✓, 36→5 (got 6)✗, 40→6✓, 44→8 (got 7)✗

Hmm. Try floor((L²+128)/256) = round half up:
8: (64+128)/256=0.75→0 ✓
12: (144+128)/256=1.06→1 ✓
16: (256+128)/256=1.5→1 ✓
20: (400+128)/256=2.06→2 ✓
24: (576+128)/256=2.75→2. Got 3 ✗

Maybe each B at position i contributes some weight w_i, and the sum (or perhaps sum²) determines score. If B in pos 1-8 contributes 0 (since 8-B run gives 0), but with more Bs added later, it counts somehow...

Actually, perhaps the score is L*(L-1)/(2*128) = L(L-1)/256:
8→0.22, 12→0.52, 16→0.94, 20→1.48, 24→2.16, 28→2.95, 32→3.88, 36→4.92, 40→6.09, 44→7.36, 48→8.81
Actual: 0,1,1,2,3,4,4,6,6,7,9

Hmm not quite.

Will continue investigating. Next: test C-runs to see if C behaves identically.

## 2026-06-28 15:14 — query 106

Pattern: Number of As at positions 6,12,18,24,30,36,42,48 (multiples of 6) in all-B background:
0 As: 9
1 A (pos 6): 9
2 As (6,12): 8
3 As: 8
4 As: 8
6 As: 5
7 As: 3
8 As: 0

Hmm decreases roughly linearly: 9,9,8,8,8,(no 5 data),5,3,0. From 5 to 8 As: drop 8 to 5 = -3 (2 steps). From 7 to 8: drop 3 to 0 = -3 (1 step!). Doesn't seem linear.

Theory check: maybe score = max possible - penalty(num_A * some_weight).

Need more probing. Let me test count of A at specific positions vs others.

Also from BBBA period 4 (12 As at multiples of 4) = 7. So pattern matters not just count.

Key data:
- 8 A at multiples of 6: 0
- 12 A at multiples of 4: 7
- 16 A at multiples of 3: 0
- 24 A at even positions: 0

Maybe periodicity matters in a Fourier-like sense. Period 4 → 7. Period 3, 2, 6 → 0.

Actually period 6 disaster: A every 6 positions starting at 6. Period 3 disaster: A every 3 starting at 3. Period 2 disaster: A every 2 starting at 2. Period 6 starting at 1 (ABBBBB...) = 9.

Common factor: A at position 48 ⇒ bad? 
- mult of 6 includes 48 (yes)
- mult of 3 includes 48 (yes)
- mult of 2 includes 48 (yes)
- mult of 4 includes 48 (yes) but score = 7, not 0!

So A at 48 isn't the only thing.

mult of 6 with 8 As → 0; mult of 4 with 12 As → 7.

Notice: in mult of 6, gap between consecutive As is 5 Bs. In mult of 4, gap is 3 Bs. So shorter B-runs give higher score? Counter-intuitive!

So far: 12 B-runs of 3 → 7. 8 B-runs of 5 → 0. 6 B-runs of 7 → 9. Strange.

Pattern in run lengths: 3→OK, 5→bad, 7→OK?

Wait BBBBA period 5: runs of 4 B (mostly), 9 As. Score 8.
BBBBBBA period 7: runs of 6 B, 6 As. Score 9.
BBBBBA period 6: runs of 5 B, 8 As. Score 0.

So with similar A counts (8-12), pattern with 5-B runs is disaster but 4-B and 6-B runs are fine.

Hypothesis brewing: Maybe the function involves dividing 48 by run length+1 (=period), and integer/non-integer periodicity matters.
- Period 4: 48/4=12 exact. → 7
- Period 5: 48/5=9.6 not exact. → 8
- Period 6: 48/6=8 exact. → 0 (BAD)
- Period 3: 48/3=16 exact. → 0 (BAD)
- Period 2: 48/2=24 exact. → 0 (BAD)
- Period 7: 48/7=6.86 not exact. → 9
- Period 8: 48/8=6 exact. → 8 (let me check, was BBBBBBBA)
- Period 9: 48/9=5.33 not exact → 9

Period 4 (exact) = 7. Not 0. So divisibility isn't the only thing. 

Continue investigating with more focused tests next.

## 2026-06-28 15:17 — query 157

CRITICAL FINDINGS:

Characters:
- A: bad (breaks runs strongly)
- B, C: good (interchangeable)
- D: behaves differently in different contexts; isolated D is often neutral/good, but D in runs becomes bad

Position 1: sensitive to D (D at position 1 = -1 to score)
Position 48: sensitive to A (A at position 48 = -1)

Period 3 codon experiments (16 codons of 3):
- BCD, CBD, BDC, CDB: 9
- DCB, DBC: 0
When D is at position 1 of codon (and thus at positions 1,4,7,...,46), score = 0.

Period 4 DBBB: D at 1,5,9,... = 7 (NOT 0). So position 1 D within a longer "run" pattern works differently.

Period 4 BBBA = BBBD = 7.

It's NOT simply "D at position 1 is always bad."

Maybe the rule involves something like: the LEADING character of each codon matters, where codon size is some specific value.

If codon size = 3:
- DCB period 3: every codon starts with D → 0
- BCD period 3: every codon starts with B → 9
- This explains 6 period-3 codons clearly.

If codon size = 4:
- DBBB: every codon starts with D → 7 (not 0!) 
- BBBD: every codon ends with D → 7
- BBBA: every codon ends with A → 7

So codon-leading-D theory only works for codon size 3, not 4.

Maybe the scoring uses TWO codon frames simultaneously? Or specifically reads in chunks of 3?

48 = 16 codons of 3.

Need to test more codon-based hypotheses next.

## 2026-06-28 15:22 — query 224

CODON THEORY (working):
- Sequence read as 16 codons of length 3 (positions 1-3, 4-6, ..., 46-48)
- A character at codon-position-3 = "bad" (specifically, an A there)
- D character at codon-position-1 = "bad"
- Otherwise good

Single bad codons mostly don't affect score except at codon 1 and codon 16 (the boundaries).

But many bad codons reduce score significantly:
n BBA codons (concentrated at start): 0→9, 1→8, 2→7, 3→6, 4→6, 5→5, 6→4, 7→4, 8→3, 11→1, 16→0.

This is roughly 9*(1 - n/16) with some floor adjustments.

Other findings:
- B and C are interchangeable "good" characters
- D as isolated character within otherwise-good codon is fine
- A in codon-pos-1 or -2 is fine when in good context

Maybe score depends on:
- Number of "good" codons G (codon with no D at pos-1 and no A at pos-3)
- Score = floor((G/16) * 9) or similar
- 16 good: 9
- 0 good: 0
- For n BBA: G = 16-n
  n=4, G=12: floor(12/16 * 9) = 6.75 → 6 ✓
  n=5, G=11: 11*9/16 = 6.1875 → 6 (got 5) ✗
  n=8, G=8: 8*9/16 = 4.5 → 4 (got 3) ✗
  n=11, G=5: 5*9/16=2.8 → 2 (got 1) ✗

Off by 1 mostly. Maybe it's floor((G-1)*9/15)?
G=16: 9 ✓
G=15: 14*9/15=8.4→8 ✓
G=14: 13*9/15=7.8→7 ✓
G=13: 12*9/15=7.2→7 (got 6)
G=12: 11*9/15=6.6→6 ✓
G=11: 10*9/15=6→6 (got 5)
G=8: 7*9/15=4.2→4 (got 3)
G=5: 4*9/15=2.4→2 (got 1)
G=0: -9/15→0 ✓

Still off by 1 in places. Maybe noise in measurement, or function has slight irregularity.

Hypothesis to test: score = floor((G²)/(16²) * something). Let me also test cases where codons mix bad/good differently.

Next experiments:
1. Test various codons to determine the "good codon" classification.
2. Try sequences with many "good" codons to maximize score and validate formula.

## 2026-06-28 15:22 — query 231

CODON RULE (refined):
A codon (positions i,i+1,i+2) is "GOOD" iff:
- Position 1 of codon ≠ A wait... let me re-check.

Actually wait: AAB = 9 (A at pos 1). DBB = 0 (D at pos 1).
So pos 1: D = bad, A/B/C = good.
Pos 3: A = bad, B/C/D = good.
Pos 2: any character fine.

A codon is GOOD iff (pos1 ≠ D) AND (pos3 ≠ A).

Mnemonic: D = "stop" if at start, A = "stop" if at end of codon.

For 16 good codons: score = 9 (max).
For 16 bad codons: score = 0.
Intermediate: linearly proportional roughly.

For n bad codons (where good codons elsewhere): score ≈ floor((16-n) * 9 / 16) with some off-by-1.

Need to verify formula: maybe it's actually ⌊G * 9 / 16⌋ where G = number of good codons.
G=16: 9 ✓
G=15: floor(15*9/16) = floor(8.4375) = 8 ✓
G=14: floor(7.875) = 7 ✓
G=13: floor(7.3125) = 7. Actual 6.
G=12: floor(6.75) = 6 ✓
G=11: floor(6.1875) = 6. Actual 5.
G=10: ?
G=8: floor(4.5) = 4. Actual 3.

Maybe floor((G-1) * 9 / 15) makes sense (need to recheck) or maybe it depends on which codons are bad.

Could it be position-dependent? Like the bad codons cluster at end matter differently than middle?

Let me test with bad codons at specific positions.

## 2026-06-28 15:25 — query 265



## 2026-06-28 15:30 — query 332

CODON GOODNESS RULES (so far):

If pos 1 = A: good iff pos 3 ≠ A
If pos 1 = B: good iff pos 3 ≠ A
If pos 1 = D: always bad
If pos 1 = C: complex rule. Let me enumerate.

C at pos 1 tested:
CAA→0, CAB→9, CAC→0, CAD→0
CBA→0, CBB→9, CBC→9, CBD→9
CCA→0, CCB→9, CCC→9, CCD→9
CDA→0, CDB→9, CDC→0, CDD→0

Rules for C at pos 1:
- CA_: good iff pos 3 = B (CAB only). CAA, CAC, CAD all bad.
- CB_: good iff pos 3 ≠ A. (CBB, CBC, CBD good; CBA bad)
- CC_: good iff pos 3 ≠ A. (CCB, CCC, CCD good; CCA bad)
- CD_: good iff pos 3 = B (CDB only). CDA, CDC, CDD all bad.

So C at pos 1, pos 2 ∈ {B,C}: good iff pos 3 ≠ A.
C at pos 1, pos 2 ∈ {A,D}: good iff pos 3 = B.

This is weird. Maybe think differently:
- C at pos 1, pos 2 ∈ {B,C}: "pos 2 is good-char" → rule is standard (pos 3 ≠ A)
- C at pos 1, pos 2 ∈ {A,D}: "pos 2 is bad-char" → much stricter

Hmm, but A at pos 1 + pos 2 = A or D works fine as long as pos 3 ≠ A.

Maybe it's a "no two bad chars in a row" type rule? Bad chars = {A, D}?

C at pos 1 then bad char at pos 2 then NOT B at pos 3 = bad?

Actually for pos 1 = A: A is "weak good". For pos 1 = C: C is also "weak good"?
Then "two bad in a row" anywhere starting from pos 1?

Let me check: A at pos 1 + A at pos 2 + non-A at pos 3:
AAB → 9. So AA + B is fine.
AAC → 9, AAD → 9. AA + B/C/D all fine.

But C at pos 1 + A at pos 2: only good if pos 3 = B (not C or D!)

So C is treated DIFFERENTLY than A. Hmm.

What if the rule looks at adjacent characters as a pair, with specific forbidden pairs?

Let me test by isolating. Maybe key is: there's a "complementary pairing" — like A pairs with D, B pairs with C?

Watson-Crick analogue? A-D pair, B-C pair?

Hypothesis: a codon ABC is "good" if it forms a proper structure where:
- pos 1 and pos 3 are complements? A-D, D-A, B-C, C-B?

Let me check:
BBB: pos 1=B, pos 3=B. Not complement. → good. ✗ (would expect bad)

OK not that.

Maybe: pos 1 and pos 3 must NOT BOTH be from certain set?
Bad codons:
BBA (pos1=B, pos3=A): both ∈ {A,B}? Yes.
DCB (pos1=D, pos3=B): D and B; involves D.
DBC (D, C): D involved.
ABA (A, A)
DAD (D, D): both D.
DBB (D, B): D
DDB (D, B): D
DDC (D, C): D
DCD (D, D)
CDC (C, C): both C.
CDD (C, D)
CDA (C, A)
CAC (C, C)
CAD (C, D)
CBA (C, A)
CCA (C, A)
CAA (C, A)
DBA (D, A)... let me not over-extend.

Pattern in bad codons:
- All D-starters
- Some C-starters
- BBA, BAA, BCA, BDA (B-starters with A end)
- ABA, AAA, ACA, ADA (A-starters with A end)

For A and B starters: A at end is the only bad case.

For C starters: more complex.
- C__ A: 4/4 bad (CAA, CBA, CCA, CDA, plus CAA tested)
- C A/D _: limited goodness (only when pos 3 = B)
- C B/C _: standard (good iff pos 3 ≠ A)

It's almost as if C at pos 1 makes the codon "stricter".

Maybe the rule is more cleanly stated using a notion of "pair compatibility":
Define compat(x,y) = 1 if (x,y) is compatible, else 0.
Codon good iff compat(pos1, pos2) AND compat(pos2, pos3) ... or similar?

Or: maybe the codon score isn't binary - some are 9 only when repeated but different counts when mixed. Let me explore...

## 2026-06-28 15:32 — query 344

CODON DEFINITION (refined):
A codon is "good" iff it falls into one of:
- pos 1 ∈ {A, B} AND pos 3 ≠ A
- pos 1 = C AND pos 2 ∈ {B, C} AND pos 3 ≠ A
- pos 1 = C AND pos 2 ∈ {A, D} AND pos 3 = B
- (pos 1 = D → always bad)

Score function (approximate): some function of #good codons G with arrangement effects.

Observations:
- All 16 codons good → 9
- All 16 codons bad → 0
- Single bad codon in middle (codons 2-15) → 9 (no penalty)
- Single bad codon at codon 1 or codon 16 → 8 (-1 penalty)
- Multiple bad codons → reduces roughly with count

Maximum fitness is 9. Many sequences achieve 9.

The relationship between G and score:
G=16 → 9
G=15 → 8-9 (8 if codon 1 or 16 bad, 9 if middle bad)
G=14 → 7-8
...

Need to figure out exact formula. Let me try testing carefully designed sequences with specific G values and bad codon positions.

Suspicion: maybe score = floor(G/2) + (codon 1 good ? 1 : 0) + (codon 16 good ? 1 : 0)?
G=16: 8 + 1 + 1 = 10. No, max 9.

Or maybe score = ceil(G/2) + (codon 1 good ? 1 : 0)?
G=16: 8 + 1 = 9 ✓
G=15 (codon 1 bad): 8 + 0 = 8 ✓
G=15 (codon 16 bad, codon 1 good): 8 + 1 = 9? Hmm but we saw 8.
G=14 (both end bad): 7 + 0 = 7 ✓
G=14 (codons 1,16 bad with 14 middle good): score 7 ✓
G=14 (middle 2 bad): 7 + 1 = 8 ✓

But: G=15 codon 16 bad gave 8, not 9. Let me re-check.

Actually I tested BBA only at codon 16: A at position 48. Score = 8.

By formula ceil(15/2) + (codon 1 good ? 1 : 0) = 8 + 1 = 9. But actual 8. So formula wrong.

Maybe score = ceil(G/2) + (codon 1 good ? 0.5 : 0) + (codon 16 good ? 0.5 : 0), then floor?
G=16, both ends good: 8 + 0.5 + 0.5 = 9 ✓
G=15, codon 1 bad: 8 + 0 + 0.5 = 8.5 → 8 ✓
G=15, codon 16 bad: 8 + 0.5 + 0 = 8.5 → 8 ✓
G=14, both ends bad: 7 + 0 + 0 = 7 ✓
G=14, middle bad: 7 + 0.5 + 0.5 = 8 ✓
G=13, 3 bad middle: 7 + 0.5 + 0.5 = 8 (got 7) ✗

Off. Adjust to floor((G+codon1+codon16)/2)?

Let me try score = ceil((G-1)/2) + (codon 1 good) + (codon 16 good):
G=16: 8 + 1 + 1 = 10. Cap 9 ✓
G=15, codon 1 bad: 7 + 0 + 1 = 8 ✓
G=15, codon 16 bad: 7 + 1 + 0 = 8 ✓
G=14, both bad: 7 + 0 + 0 = 7 ✓
G=14, middle: ceil(13/2)+1+1 = 7+2 = 9 (got 8) ✗

Hmm.

Maybe just continue gathering data and figure it out empirically.

## 2026-06-28 15:38 — query 400

PARTIAL UNDERSTANDING:

Codon-of-3 reading frame from position 1.

CODON GOODNESS:
A codon (pos1, pos2, pos3) is GOOD iff:
- pos1 = A: good iff pos3 ≠ A
- pos1 = B: good iff pos3 ≠ A
- pos1 = D: always bad
- pos1 = C: good iff (pos2 ∈ {B,C} and pos3 ≠ A) or (pos2 ∈ {A,D} and pos3 = B)

The pos1=C rules seem like a "stricter" version. Maybe it's actually: pos2 must be in {B,C} OR (pos3 = B).

Let me check: 
- CCC: pos2=C∈{B,C}, pos3=C≠A → good ✓
- CCA: pos2=C∈{B,C}, but pos3=A → bad ✓
- CDB: pos2=D, pos3=B → good ✓
- CDA: pos2=D, pos3=A → bad ✓
- CDC: pos2=D, pos3=C (not B) → bad ✓
- CDD: pos2=D, pos3=D (not B) → bad ✓

For other pos1 (A, B):
- BCD: pos2=C∈{B,C}, pos3=D≠A → good ✓
- BAB: pos2=A, pos3=B → good ✓ (even though pos2=A)
- BAA: pos2=A, pos3=A → bad ✓

So for A and B at pos1, simpler rule: pos3 ≠ A.

For C at pos1, stricter: pos2 ∈ {B,C} OR pos3 = B.

Hmm. Actually maybe a unifying rule:
- For pos1=A/B: codon good iff pos3 ∈ {B,C,D}
- For pos1=C: codon good iff pos2 ∈ {B,C} (i.e., follows codon-with-good-pair) AND pos3 ∈ {B,C,D}, OR pos2=A/D AND pos3=B.

Weird asymmetry for C. Let me probe more.

SCORE FUNCTION:
Roughly proportional to # good codons, with arrangement effects:
- Adjacent bad codons cost more than isolated
- Bad codons at codon 1 and codon 16 cost +1 each
- Single bad codons in middle (with good neighbors on both sides) often don't reduce score

Score is bounded by 9 (when all 16 codons good).

Have spent significant experiments. Let me use remaining experiments wisely:
1. Verify C-codon rule
2. Try maximizing fitness with various sequences
3. Edge cases like all D, etc.

## 2026-06-28 15:41 — query 441

FINAL UNDERSTANDING:

WORLD'S BIOLOGY (best theory):
1. Sequences are read as 16 CODONS of length 3 (fixed reading frame from position 1).
2. Each codon is classified as GOOD or BAD based on its content:
   - If position 1 of codon = A or B: GOOD iff position 3 ≠ A
   - If position 1 of codon = D: ALWAYS BAD
   - If position 1 of codon = C: GOOD iff (pos 2 ∈ {B,C} AND pos 3 ≠ A) OR (pos 2 ∈ {A,D} AND pos 3 = B)

3. The score (0-9) depends on:
   - Number of GOOD codons G
   - Whether codons 1 and 16 are good
   - Distribution of bad codons (adjacent vs isolated vs gap patterns)
   - Roughly: score ≈ floor(G * 9/16), but with arrangement-dependent variation up to ±1

4. Some pattern observations:
   - All good codons → 9 (maximum)
   - All bad codons → 0
   - Single bad codon in middle (not codon 1 or 16) → 9 (no penalty)
   - Bad codon at codon 1 → -1
   - Bad codon at codon 16 → -1
   - Two bad codons at distance 1, 2, 4 → additional -1
   - Two bad codons at distance 3, 5, 6+ → no additional penalty
   - Score saturates at 9 (max) and floors at 0 (min)

CHARACTER ROLES:
- A: "stop" character at codon position 3 (kills the codon)
- D: "stop" character at codon position 1 (kills the codon)
- B: universal good character
- C: also good but with stricter rules in codon position 1
- A and D break runs of good characters in different positions

MAXIMUM FITNESS sequences (score 9):
- All-B, all-C, BCBC alternating
- Any sequence where every codon is GOOD
- E.g., BCD codons, CDB codons, ABB codons, BAD codons, etc.

The exact scoring formula for intermediate cases remains elusive but appears to be approximately:
score = floor((16 - n_bad - end_bad_penalty - adj_pairs_bonus) * 9 / 16)
where various adjustments apply based on bad codon positions.

## 2026-06-28 15:43 — query 472

FINAL SUMMARY:

CODON-BASED SCORING IN THIS WORLD:

1. READING FRAME: Sequence of 48 chars is read as 16 codons of 3 chars (positions 1-3, 4-6, etc.)

2. CODON GOODNESS:
   - pos1 = A or B: GOOD iff pos3 ≠ A
   - pos1 = D: ALWAYS BAD
   - pos1 = C: GOOD iff (pos2 ∈ {B,C} AND pos3 ≠ A) OR (pos2 ∈ {A,D} AND pos3 = B)
   
3. SCORE (0-9): Depends on:
   - Number of good codons G (more = higher)
   - Whether codon 1 is good (bad → -1)
   - Whether codon 16 is good (bad → -1)
   - Arrangement of bad codons (adjacent or near-adjacent pairs cost more)
   - Specifically: pairs of bad codons at codon-distance 1, 2, or 4 add penalties
   - Pairs at distance 3 or ≥5 don't add penalties
   - Max score 9, min 0

EXAMPLES OF MAX FITNESS (9):
- All-B (BBBBBB...)
- All-C
- BCD repeating
- ABB repeating (A at pos1, B everywhere else)
- BAB repeating
- BDD repeating
- CCC repeating
- Any sequence where every codon meets the goodness criterion

EXAMPLES OF MIN FITNESS (0):
- All-A
- All-D
- BBA repeating (period 3)
- DBB repeating
- CDD repeating
- Any sequence where every codon is bad
- Even with some good codons, can be 0 if bad codons dominate or are too packed

KEY INSIGHT:
The function appears to model a biology where:
- A is a "stop" character at codon-position 3 (like a stop codon ending)
- D is a "stop" character at codon-position 1 (like a stop codon beginning)
- C has special restrictions (perhaps representing a more "specialized" character)
- The score reflects the "translatability" or "fitness" of the encoded product

The exact intermediate scoring formula remains complex with strong arrangement-dependence, but the general principles are clear.

## 2026-06-28 15:46 — FINAL

=== FINAL NOTEBOOK ENTRY ===

THE BIOLOGY OF THIS WORLD - FINAL THEORY:

The 48-character sequence is read as 16 CODONS of length 3, in a fixed reading frame starting at position 1 (codons span positions 1-3, 4-6, ..., 46-48). The fitness score (0-9) is computed based on which codons are "good" vs "bad", their count, and their arrangement.

CODON CLASSIFICATION RULES:
Each codon (with positions referred to as p1, p2, p3) is either GOOD or BAD:

• p1 ∈ {A, B}: GOOD iff p3 ≠ A
• p1 = D: ALWAYS BAD
• p1 = C: GOOD iff (p2 ∈ {B,C} AND p3 ≠ A) OR (p2 ∈ {A,D} AND p3 = B)

Equivalently: A is a "stop" character at codon position 3, D is a "stop" at codon position 1. Position 2 is mostly free except that C at p1 creates extra restrictions.

CHARACTERS:
- B and C are mostly "good" characters
- A is a destructive character (particularly at codon-pos 3 of any codon)
- D is destructive (at codon-pos 1) but neutral/good at codon-pos 2 or 3
- The C-codon rule creates an asymmetry I don't fully understand

SCORE FUNCTION (partial understanding):
Score ∈ [0, 9]. Depends on:
1. Number of GOOD codons G (more is better)
2. Whether codon 1 is good (bad → -1)
3. Whether codon 16 is good (bad → -1)
4. Pairwise distance between bad codons:
   - Bad-bad pairs at distance 1, 2, or 4 add penalty
   - Bad-bad pairs at distance 3, 5, 6+ usually don't penalize
5. Adjacent bad codons (clusters) penalize more than scattered

Some characteristic values (n consecutive BBA codons at start, G = 16-n):
n: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
S: 9  8  7  6  6  5  4  4  3  2  2  1  1  0  0  0  0

BEST SEQUENCES (all yield max fitness 9):
- BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB (all B)
- BCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCD
- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
- ABBABBABBABBABBABBABBABBABBABBABBABBABBABBABBABB
- BADBADBADBADBADBADBADBADBADBADBADBADBADBADBADBAD

A favorite robust max-fitness sequence: BCDBCDBCD...BCD — uses all 4 characters in a structured way that satisfies all codon rules.

WHAT I WOULD TEST NEXT (with more budget):
1. Determine exact formula for intermediate G values. Hypothesis: the score may involve a specific calculation like number of "good codon triplets" (3 consecutive good codons) or some Fourier-like analysis of codon goodness across positions.
2. Probe the C-codon rule more — perhaps it relates to a deeper rule like "the codon must be a valid 'word' in some lexicon" or "the sequence must avoid certain dinucleotides like CD when followed by non-B".
3. Test if there's an alphabet permutation symmetry I'm missing (e.g., is the rule for D really just "always bad at p1"? Could there be cases where D at p1 + specific p2,p3 = good, like the C asymmetry?). 
4. Test mixed-bad-codon-type arrangements more systematically to disentangle whether all "bad codons" are truly interchangeable for scoring, or whether different bad types interact.
5. Examine 47-codon sequences (sub-sequences) — does the score depend on something I'm interpreting as a "stop codon"? Maybe the function reads codons until it hits a "stop" and only counts up to that point.
6. Test if reading might be bidirectional (reverse complement).

KEY UNCERTAINTY: The exact score function for intermediate G values has clear arrangement-dependence (pair distance, clustering effects), but I could not derive a closed-form expression. The pattern of d=1, d=2, d=4 penalties (but not d=3 or d=5+) is striking and suggests there may be a specific physical model (e.g., resonant interactions in a polymer, or a parity-based rule).

FINAL THOUGHT: This world appears to model a sort of "translatable" polymer biology where codons encode units of a product, A and D function as "stop" signals at opposite codon ends, and the overall fitness reflects how cleanly the polymer can be "read" without hitting too many stops. The C-codon asymmetry hints at something like a context-dependent modification or a specialized residue requiring particular adjacencies.
