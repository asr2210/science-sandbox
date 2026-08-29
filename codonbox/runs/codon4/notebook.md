
## 2026-06-28 15:31 — query 0

## Initial Setup
- Alphabet: {A, B, C, D}
- Sequence length: 64
- Budget: 500 experiments
- Goal: maximize function score, understand rules

## Starting assumptions (to be tested)
- I don't know anything yet. Possible factors: composition (counts of each letter), position-specific effects, motifs/patterns, GC-like content, repeats, structure (palindromes), specific codons.
- Function may be additive across positions, or depend on motifs, or have complex epistasis.

## Plan
1. First measure homopolymers (all-A, all-B, all-C, all-D) to see if any single character is favored.
2. Then test simple alternating patterns (AB, AC, AD, BC, BD, CD).
3. Then test random-looking uniform mixes.
4. Then probe position effects by single-letter swaps from the best baseline.

## Experiment 1: all A's (64 A's)
Tests baseline for homopolymer A.

## 2026-06-28 15:32 — query 10

## Observations after 10 experiments
- All-A: 9, All-D: 9, All-B: 0, All-C: 0
- AD alternating: 9 (great)
- BC alt: 0, AB alt: 0, AC alt: 0
- 1 B in sea of A: 9; 2 B's in sea of A: 9
- So a few B's don't hurt, but ~50% B does (kills to 0)

## Hypothesis
Maybe the score is something like max(count of A, count of D) - penalty for B/C beyond a threshold? Or it's about runs of A/D. 
Or: there's a threshold — sequence functions if it has enough A+D content (or right structure).

Score of 9 might be the max possible, capped. Need to confirm by testing if score can exceed 9.

## Next: test how many B's break the score; find the threshold.

## 2026-06-28 15:32 — query 14

## Data: B's vs A's (mostly contiguous)
- 0 B's, 64 A's: 9
- 2 B's, 62 A's: 9
- 10 B's, 54 A's: 6
- 20 B's, 44 A's: 5
- 32 B's, 32 A's: 3 (regardless of order)
- 64 B's, 0 A's: 0
- AB alternating (32 each): 0

So contiguous 32B+32A = 3, but alternating ABAB...= 0. Order matters!
Possibly: score depends on longest run of A's (or A+D), or on count of A+D minus discount for B/C.

Longest A run in ABAB... = 1; in 32B+32A block = 32. 
Longest A run for 10B+54A: 54.
Longest A run for 20B+44A: 44.
Hypothesis: score ≈ floor(longestrun / something)? Let me check: 
- 64: 9, 62: ~9, 54: 6, 44: 5, 32: 3, 1: 0.
That's roughly 9 * (run/64)? 54/64*9 = 7.6 (got 6); 44/64*9=6.2 (got 5); 32/64*9=4.5 (got 3); not exact.

Could be longest run of A_or_D. Need to test runs of D and AD mix.

## 2026-06-28 15:32 — query 21

## Longest A-run data (rest B's)
- 0 A run, 64 B: 0
- 8 A run, 56 B: 0
- 16 A run, 48 B: 1
- 24 A run, 40 B: 2
- 32 A run, 32 B: 3
- 44 A run, 20 B: 5
- 54 A run, 10 B: 6
- 64 A run, 0 B: 9

Looks roughly like score ≈ floor((longest_A_run - 8) / 6)?  
- 16: (16-8)/6=1.33 → 1 ✓
- 24: (24-8)/6=2.67 → 2 ✓  
- 32: (32-8)/6=4 → 4 (got 3) ✗
- 44: (44-8)/6=6 → 6 (got 5) ✗

Or score = floor(longest_run / 7)?
- 16/7=2.28 (got 1) ✗

What if score = floor((run-X)/Y) but only counts AD-bases without penalty being separate?
Actually score may depend on TOTAL count of A's:
- counts: 0→0, 8→0, 16→1, 24→2, 32→3, 44→5, 54→6, 64→9
- 64→9: special boundary. 
- diff: 16:1, 24:2 (Δ8 = Δ1), 32:3 (Δ8 = Δ1), 44:5 (Δ12 = Δ2), 54:6 (Δ10 = Δ1), 64:9 (Δ10 = Δ3)

Hmm. Score may also penalize each B. Could be: count(A or D) - count(B or C)? 
- 64A, 0B: 64-0=64. Not 9. But maybe capped at 9 = max.
- 32A, 32B: 32-32=0, but observed 3. Doesn't fit.

Maybe score = floor(count(A or D)/N) - penalty(B's)? Need more data.

## New idea
Test with rest being something else than B. What about D as a "filler"? AD-only sequences seemed to all be 9. So A+D content matters AND maybe purity?

Let's test mixes of A and D in different proportions, to see if score stays 9.

Also test AD-mix-with-B: 32A + 32D contiguous = 9. AD alternating = 9. ABAB = 0. 32A+32B=3.

So maybe rule is: max score requires sequence composed only of A and D. Once any B or C is present, penalty kicks in. Score may be related to longest contiguous run of {A,D}.

## 2026-06-28 15:33 — query 23

## BREAKTHROUGH: position-specific effects!
- ADADAD...AD (starts A) = 9
- DADADA...DA (starts D) = 0
- AAAA...A = 9, DDDD...D = 9 (both same)
- 32A + 32D = 9
- Random AD mix = 7

So position 1 might require A specifically? Or odd positions A, even D?
ADADAD has A at odd, D at even.
DADADA has D at odd, A at even.

In all-A: every position is A (incl. even). 9.
In all-D: every position is D (incl. odd). 9.
So neither is per-position required.

Maybe rule is about DINUCLEOTIDES? 
- "AD" appears 32 times in ADADAD (a great motif)
- "DA" appears 32 times in DADADA (bad motif)
- "AA" in all-A: 63 times. Score 9.
- "DD" in all-D: 63 times. Score 9.

Could be: score = count of "good" dinucleotides minus "bad"?
Good: AA, DD, AD? Bad: DA?
Test: 32A+32D contiguous = 31 AA + 1 AD + 31 DD. Score 9. Good.
Random AD mix scored 7. Number of DA in that mix? Let me count in "ADDAADAADDADADDAADADDAADADDADAADDAADADADADDADDAAADADDADDADADDAAD":
Positions: A-D-D-A-A-D-A-A-D-D-A-D-A-D-D-A-A-D-A-D-D-A-A-D-A-D-D-A-D-A-A-D-D-A-A-D-A-D-A-D-A-D-D-A-D-D-A-A-A-D-A-D-D-A-D-D-A-D-A-D-D-A-A-D
Counting "DA" pairs (D followed by A): positions 3→4 (DA), 6→7 (DA), 10→11 (DA), 12→13 (DA), 15→16 (DA), 18→19 (DA), 21→22 (DA), 24→25 (DA), 28→29 (only if 28=D,29=A: pos28=A so no... let me redo)

Hmm too complex by hand. Test simpler hypotheses.

## 2026-06-28 15:33 — query 27

## DA penalty data
- 1 DA + 62 A: 9
- 2 DA + 60 A: 8 (one DA cost 1!)
- 4 DA + 56 A: 7 (-2 vs baseline 9)
- 32 DA full alternation: 0

Hmm "1 DA + 62 A" is DAAA... (1 D, 63 A's, 1 DA dinuc). 
"2 DA + 60 A" is DADAAA... (2 D, 62 A; 2 DA dinucs + 1 AD dinuc).
"4 DA + 56 A": 4 D, 60 A; 4 DA + 3 AD dinucs.
"32 DA": 32 D, 32 A; 32 DA + 31 AD.

Maybe per-DA penalty isn't single-cause. Could also be that the score depends on number of D's in certain positions, or on the "AD-vs-DA" ordering.

Actually simpler: maybe score relates to longest run of identical chars (A's or D's). 
- DAAA...A: longest A run = 63 → 9
- DADAAA...: longest A run = 61 → 8
- DADADADAAA...: longest A run = 57 → 7
- DADA...DA full: longest A run = 1 → 0
- AAAAA...A all: 64 → 9
- ADADAD: longest A run = 1, longest D run = 1 → should be low, but got 9!

So ADADAD breaks the longest-run rule. The orientation matters. AD start scores well; DA start scores badly.

Maybe the rule is about EVEN/ODD positions:
ADADAD...AD: positions 1,3,5...(odd)=A; positions 2,4,6...(even)=D. Score 9.
DADADA: odd=D, even=A. Score 0.
All A: odd=A, even=A. Score 9.
All D: odd=D, even=D. Score 9.

Hmm, this isn't simply "odd positions must be A" because all-D works.

What if rule is: at each position i, the base must "match" some pattern, or the bases must follow some allowed transitions starting from position 1?

Like a Markov chain / DFA: starting state, valid transitions A→A, A→D allowed; D→D allowed; D→A forbidden?
- All A: AA AA AA → ok. ✓
- All D: DD DD → ok. ✓
- ADAD: AD then DA → DA forbidden? But ADAD scored 9!

Hmm.

What if transitions are: A→A ok, A→D ok, D→D ok, D→A: only sometimes ok?
- ADADAD: A→D, D→A, A→D, D→A,... has many D→A. Got 9.
- DADADA: D→A, A→D, D→A,... has many D→A. Got 0.
- DAAA...: 1 D→A then all A→A. Got 9.

The difference between ADAD (9) and DADA (0) is just the starting letter! Maybe the FIRST position matters strongly.

Test: AADADAD vs starting D.

## 2026-06-28 15:33 — query 29

## More dinucleotide data
- ADADAD...AD (32 AD pairs, 64 chars): 9
- AADADAD...AD (1 extra A at start, then DAD...): 0 — wait, the sequence I sent: AADADADAD...AD has 64 chars: A-A-D-A-D-A-D-A-...-D. So odd positions: A,D,D,D,D... and even: A,A,A,A... Hmm.
  Actually let me count: "AADADADADADADADADADADADADADADADADADADADADADADADADADADADADADADAD" 
  pos1=A, pos2=A, pos3=D, pos4=A, pos5=D, pos6=A,...
  So odd positions (1,3,5,...): A,D,D,D,D,...,D
  Even positions (2,4,6,...): A,A,A,A,...,A
  Compared to ADADAD: odd=A,A,A,...A; even=D,D,D,...D
  
Big difference: in ADADAD pattern, all odd=A, all even=D.
AADADAD breaks this from position 2 onward.

So maybe the rule is: pairs at (2k-1, 2k) must be valid dinucleotides.
ADADAD: pairs are (A,D),(A,D),(A,D)... all AD. Score 9.
DADADA: pairs are (D,A),(D,A),... all DA. Score 0.
AAAA: pairs all AA. Score 9.
DDDD: pairs all DD. Score 9.
AADADAD: pairs are (A,A),(D,A),(D,A),(D,A),...(D,A). 1 AA + 31 DA. Score 0.

So perhaps valid dinucleotide pairs (in the 32 non-overlapping codons): AA, DD, AD are good. DA is bad.

Actually let me think codon-wise (length-2 codons):
- 32 AA's: 9
- 32 DD's: 9
- 32 AD's: 9
- 32 DA's: 0
- 16 AA + 16 BB? Earlier mixes I haven't tested in this frame.

Let me test 32 AA + 32 DD interspersed-vs-blocked.

## 2026-06-28 15:33 — query 32

## Codon hypothesis confirmation
Sequence: ADADADADADADADADADADADADADADADAD(=16 AD codons) + DADADADADADADADADADADADADADADADA (=16 DA codons)
First 32: 16 AD codons = score 9 worth.
Last 32: 16 DA codons = score 0.
Half AD, half DA: 3. 
Pattern: score might be proportional to # of "good" codons - # of "bad"?
16 good - 16 bad = 0, but observed 3. Or maybe 16 good codons / 32 * 9 ≈ 4.5, observed 3.

Actually wait, the chars at boundary: ADAD...AD|DADA...DA. The boundary is "AD" then "DA". In non-overlapping codons positions 1-2,3-4,...,63-64: yes 32 codons. First 16 AD, last 16 DA.

If each AD codon contributes some +score and each DA codon contributes -score (or 0):
16 AD * x = 9 → x ≈ 0.56? But all 32 AD codons gave 9 too, not 18. So score is capped/saturated.

Alternative: maybe score = floor(good_codons / k) up to 9.
- 32 AD = 9; 16 AD + 16 DA = 3.
- All AA = 32 codons of AA = 9. AA is good.

Let me hypothesize: GOOD codons (each contributes +): AA, AD, DA(?), DD. BAD codons (penalty): contain B or C.
Wait no — pure DA all gave 0. So DA is not good.

Codons containing 0 letters from {B,C}: AA, AD, DA, DD. (16 possible).
Of these: AA→9, AD→9, DD→9, DA→0. So DA is "0-fitness".

Maybe the rule is: at each odd position, must be A; at each even position, must be D — UNLESS the codon is "homo" (AA or DD) which is also allowed.

Codon rules:
- AA: ok (matches all-A pattern)
- DD: ok (matches all-D pattern)
- AD: ok (matches expected odd-A even-D)
- DA: BAD (odd=D, even=A: wrong)

For mixed test (16 AD + 16 DA): 16 good codons, 16 bad. Score = 3.
Maybe score = max(0, good - bad)? 16-16=0, observed 3. Doesn't fit.
Or floor(good*9/32)? 16*9/32 = 4.5. Not 3.
Or floor(good/something) - floor(bad/something)?

Need more data. Test 24 AD + 8 DA codons (more good), and 8 AD + 24 DA.

## 2026-06-28 15:34 — query 34

## More codon data
- 32 AD, 0 DA: 9
- 24 AD, 8 DA: 6
- 16 AD, 16 DA: 3
- 8 AD, 24 DA: 1
- 0 AD, 32 DA: 0

Differences in score: 9, 6, 3, 1, 0. Like decreasing by 3,3,2,1.
Roughly proportional? Score ≈ 9 * (AD/32)?
- 32/32 * 9 = 9 ✓
- 24/32 * 9 = 6.75 → 6 ✓
- 16/32 * 9 = 4.5 → 3? not exact
- 8/32 * 9 = 2.25 → 1? not exact

Or score = max(0, AD_count - DA_count)/something?
- 32-0=32 → 9
- 24-8=16 → 6
- 16-16=0 → 3 (doesn't fit)
- 8-24=-16 → 1 (doesn't fit)

Maybe codons interact across boundaries. Or score is based on local arrangement.

Let me try a different angle: keep things simple. The boundary between AD block and DA block in 16+16 was "...ADDD ADAD..." (last char of 32 = D, first char of 33 = D, so we see DD between). 

In 24 AD + 8 DA: chars 1-48 = ADAD...AD; char 49 starts DA: "D"; so position 48=D, 49=D. Concatenated "...ADDA DA...". So we see "DD" at the junction.

In 8 AD + 24 DA: chars 1-16 = ADAD...AD; char 17 = D (start of DA): "...AD" + "DA..." → "DD" junction.

Hmm, the actual character sequences only differ in WHERE the transition is.

Better hypothesis: maybe the rule is based on overlapping dinucleotides (all 63 of them).

In 32 AD: dinucs are AD,DA,AD,DA,... (32 AD's + 31 DA's). But scored 9!
Wait, ADAD has overlapping pairs: AD (1-2), DA (2-3), AD (3-4)... So actually plenty of DAs in the "good" ADAD pattern.

So overlapping dinuc hypothesis doesn't work either.

What about positional rule:
- Score = number of positions i such that:
  - odd i: s[i] == A or s[i]==D (i.e., not B/C)
  - even i: s[i] == D (or A?)

For ADAD: odd i = A ✓, even i = D ✓. All 64 satisfy. Score 9.
For DADA: odd i = D, even i = A. If rule is odd must be A: all 32 odd positions wrong. Score 0.
For AAAA: odd = A ✓, even = A. If rule is even must be D: all 32 even positions wrong. But scored 9!
For DDDD: scored 9 but odd positions = D.

So rule isn't strict per-position.

What if score = max over rotations/frames? Or "best matching" to some pattern?

Try: AAAA = match to template "all A's" = perfect 9.
DDDD = match to template "all D's" = perfect 9.
ADAD = match to template "ADADAD" = perfect 9.
DADA = doesn't match? But it matches "DDDD" partially... 

Maybe score = max(match_to_template_1, match_to_template_2, ...) for several templates including: "all A", "all D", "AD repeated"?

DADA: 
- vs AAAA: 32 matches (the even A's). 32/64.
- vs DDDD: 32 matches (the odd D's). 32/64.  
- vs ADAD: 0 matches!
- vs DADA: 64 matches but is DADA a valid template? Apparently NOT.

Maybe templates are: A^64, D^64, (AD)^32, (AABB)^16? Don't know yet.

If we compute score as some monotone function of best template match:
- AAAA: matches A^64 perfectly → 9
- DDDD: matches D^64 perfectly → 9
- ADAD: matches (AD)^32 perfectly → 9
- AADD repeated: matches (AADD)^16 perfectly? AADD AADD... → 9 (observed!)
- DDAA repeated: matches what? (DDAA)^16. Scored 9. So DDAA is also valid template.

Now: 32A + 32B = 3. What templates? Best match: 32 matches to A^64 (first half), 32 to (AB)^32 partial, ...
Hmm hard.

Different track: maybe score is fractional similarity to nearest valid sequence, where valid sequences are some set. Let me just keep gathering data and look for structure.

## 2026-06-28 15:34 — query 37

## Key idea: maybe score = number of letters belonging to longest contig run of {A,D} ... with some math?

Data on longest contig run of {A,D} (call it L):
- All A (L=64): 9
- All D (L=64): 9
- 32A+32D contig (L=64): 9
- 32A+32B (L=32): 3
- 32A+32C (L=32): 3
- 24A+40B (L=24): 2
- 16A+48B (L=16): 1
- 8A+56B (L=8): 0
- 1B in sea A (L=63 then 1B then... longest is 63): 9
- DAAA...A (L=63 starting pos 2): 9
- AAAABBBB... 8 reps (L=4): 0

Score seems roughly = floor((L - 8)/6) capped at 9?
- L=64: (64-8)/6 = 9.33 → 9 ✓
- L=32: (32-8)/6 = 4 → 4 (observed 3) close
- L=24: (24-8)/6 = 2.67 → 2 ✓
- L=16: (16-8)/6 = 1.33 → 1 ✓
- L=8: 0 ✓
- L=63: (63-8)/6=9.17 → 9 ✓
- L=4: 0 ✓
- L=44 (44A+20B): (44-8)/6=6 → 6 (observed 5) close
- L=54: (54-8)/6=7.67 → 7 (observed 6) close

So formula: score ≈ floor((L-8)/6) is close but off by 1 sometimes. Maybe floor((L-10)/6)?
- L=64: 9, L=32: 3.67→3 ✓, L=44: 5.67→5 ✓, L=54: 7.33→7 (obs 6) off
- L=24: 2.33→2 ✓, L=16: 1 ✓

Or floor(L/7) - 1?
- 64/7=9.14, -1=8.14 → not 9.

Could be floor(L/8)?
- 64/8=8 (obs 9) no
- 32/8=4 (obs 3) no

Could be ceil((L-8)/6.5)? Getting hacky.

But L doesn't explain ADAD = 9 (L there = longest contig A or D run = 1!) Wait actually I'm computing run of {A,D} together: in ADAD all chars are A or D, so L=64. Score 9 ✓.

So this works for ADAD! Let me recheck:
- ADAD: contig {A,D} = whole string = 64 → 9 ✓
- DADA: also all A,D, contig = 64 → should be 9 but observed 0! ✗

So L (longest run of A,D) doesn't capture DADA.

Maybe TWO factors: (longest run of A or D) AND (some position rule).

Let me try: count of A's at odd positions PLUS count of D's at even positions.
- AAAA: 32 (odd A's) + 0 (even D's) = 32
- DDDD: 0 + 32 = 32
- ADAD: 32 (odd A) + 32 (even D) = 64
- DADA: 0 + 0 = 0!
- 32A+32D (AAAAA...AADDDDD...DD): odd A count in first half = 16 (positions 1,3,...,31), even A in first half = 16 (positions 2,4,...,32). Odd D count in second half = positions 33,35,...,63 = 16; even D count second half = positions 34,...,64 = 16. So odd A's = 16, even D's = 16. Total = 32.
- 32B + 32A (BBBB...AAAA): odd A's in second half: pos 33,35,...,63 = 16; even D's = 0. Total = 16.

If score relates to this "match" score M:
- M=0 (DADA) → 0
- M=16 (32B+32A) → 3
- M=32 (all A) → 9
- M=32 (32A+32D) → 9 ✓
- M=64 (ADAD) → 9

But 32B+32A gave 3, while all A also has M=32 giving 9. Doesn't match.

Could the answer be the MAX of:
- match to all-A template = count of A
- match to all-D template = count of D
- match to (AD)^32 template = count where matches

For all A: 64,0,32 → max 64.
For DADA: 32 (count of A),32 (count of D),0 (count of match to ADAD template) → max 32.
For ADAD: 32,32,64 → max 64.
For 32A+32B contig: count A = 32, count D = 0, match to ADAD = 16 (odd positions matching). → max 32. But scored 3 (not 9 like all-A with also 32 A's? wait all-A has 64 A's!).

All A: count(A) = 64 → score 9.
32A+32B: count(A) = 32 → score 3.

If score = floor(count(A)/7) for all-A-or-A+other type, that doesn't work for all D.

What if score = max over single-template-matches, where templates are all-A, all-D, AD-alt, DA-alt? But DA-alt would make DADA→9 (wrong).

Let me try templates being SOMETHING that includes "all A", "all D", "(AD)^32", but NOT (DA)^32.

Then templates are perfect-matchable to specific sequences. The score may be the maximum matching to any of a small set of "good" templates.

Score = max over templates T of: floor((matches(seq,T) - threshold)/divisor)?

For all-A (64 matches to T=A^64): 9
For 32A+32B vs T=A^64: 32 matches. → 3 if formula (32-X)/Y = 3.
For all D vs T=D^64: 64 matches → 9.
For DAAA...A vs T=A^64: 63 matches → 9. Other templates lower.

So maybe templates: {A^64, D^64, (AD)^32}. Score = max match count → mapped to 0-9.

Test mapping: matches m → score
- m=64: 9
- m=63: 9
- m=54: 6 (54A in row vs A^64: 54 matches)
  Wait 54A+10B with the A's contig: vs A^64, matches = 54. Score 6.
- m=44: 5
- m=32: 3
- m=24: 2  
- m=16: 1
- m=8: 0
- m=4 (AAAABBBB repeated, matches to A^64 = 32): hmm not 4.

Hmm wait AAAABBBB repeated has 32 A's → 32 matches to A^64 → if formula gives 3, but observed 0.
So matches count alone doesn't suffice. Maybe it's longest-RUN of matches to template.

Let me reformulate: Score = max over templates T of f(longest_run_of_matching_positions(seq, T))?

For AAAA...A vs T=A^64: longest run = 64. → 9.
For 32A+32B vs A^64: longest match run = 32. → 3.
For AAAABBBB pattern vs A^64: longest match run = 4. → 0.
For DAAA...A vs A^64: longest match run = 63 (positions 2-64). → 9.
For DADA...DA vs D^64: longest D run = 1. vs A^64: longest A run = 1. vs (AD)^32: matches at... pos1=D(want A)✗, pos2=A(want D)✗,... no matches. Longest match run = 0.
  So max = 1. Score 0. ✓
For ADADAD vs (AD)^32: perfect match → run 64 → 9. ✓

Now mapping run length R → score:
- R=64: 9
- R=63: 9
- R=54: 6
- R=44: 5
- R=32: 3
- R=24: 2
- R=16: 1
- R=8: 0
- R=4: 0
- R=1: 0

Formula? Looks like roughly max(0, floor((R-10)/6.something)). Let's fit:
R=16: 1; R=24: 2; R=32: 3; R=44: 5; R=54: 6; R=63: 9
Diff: 16→24(Δ8, Δscore 1), 24→32(Δ8, Δ1), 32→44(Δ12, Δ2), 44→54(Δ10, Δ1), 54→63(Δ9, Δ3)
Score / R: 1/16, 2/24, 3/32, 5/44, 6/54, 9/63 ≈ 0.0625, 0.083, 0.094, 0.114, 0.111, 0.143
Not linear.

Maybe score is a piecewise step function. Could be: score = number of full "8-character" matches? Like #of-contiguous-8s in match? Or maybe scoring is: every 8 chars of perfect match → +1?
- R=8: 1? but observed 0.
- R=16: 2? but observed 1. Off by 1.

Maybe score = floor((R-7)/something)?
R=16: (16-7)=9 /? = 1, so /9.
R=24: 17/? = 2 → 8.5
R=32: 25/? = 3 → 8.3
R=44: 37/? = 5 → 7.4
Inconsistent.

Or some other formula. Let me just test more values to map it out.

## 2026-06-28 15:35 — query 41

## Run length R → score mapping (more data points)
- R=8: 0
- R=16: 1
- R=24: 2
- R=32: 3
- R=40: 4
- R=44: 5
- R=48: 6
- R=54: 6
- R=56: 7
- R=60: 8
- R=63: 9
- R=64: 9

Looks like score = floor((R-8)/something). 
R=16→1: (16-8)/8 = 1 ✓
R=24→2: (24-8)/8 = 2 ✓
R=32→3: (32-8)/8 = 3 ✓
R=40→4: (40-8)/8 = 4 ✓
R=48→6: (48-8)/8 = 5 ✗ (off by 1!)
R=56→7: (56-8)/8 = 6 ✗
R=64→9: (64-8)/8 = 7 ✗

Hmm. Looks like the rate accelerates. Maybe score = R - max(0, something)?

Let's compute scores: R - score:
- R=8: 8
- R=16: 15
- R=24: 22
- R=32: 29
- R=40: 36
- R=44: 39
- R=48: 42
- R=54: 48
- R=56: 49
- R=60: 52
- R=63: 54
- R=64: 55

R-score is monotone increasing. Suggests "errors penalty" is rest = 64-R = B count. 
Actually score may be a non-linear function. Let me try: score = something simpler involving B count.
B count = 64 - R (since rest of seq is B's and only one A-block).
B count: 0→9, 4→8, 8→7, 10→6, 16→6, 20→5, 24→4, 32→3, 40→2, 48→1, 56→0
Hmm 10 and 16 both = 6. Inconsistent. Let me recheck.
Wait R=54 means 54 A's + 10 B's: B count = 10, score = 6.
R=48 = 48 A's + 16 B's: B count = 16, score = 6.
So same score 6 for B=10 and B=16. 

Maybe score is a continuous function. Let me try plotting R vs score:
R: 8,16,24,32,40,44,48,54,56,60,63,64
S: 0, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 9

Δ R between consecutive: 8,8,8,8,4,4,6,2,4,3,1
Δ S: 1,1,1,1,1,1,0,1,1,1,0

Each +1 score requires ~6 extra R typically but varies. The pattern is roughly linear with score ≈ (R-8)/6.something but capped at 9.

Actually let me try: score = round(9 * (R-8)/56) where R in [8,64]?
- R=8: 0 ✓
- R=16: 9*8/56 = 1.29 → 1 ✓
- R=24: 9*16/56=2.57 → 3 ✗ (obs 2)
- R=32: 9*24/56=3.86 → 4 ✗ (obs 3)
- R=40: 9*32/56=5.14 → 5 ✗ (obs 4)
- R=48: 9*40/56=6.43 → 6 ✓
- R=54: 9*46/56=7.39 → 7 ✗ (obs 6)
- R=56: 9*48/56=7.71 → 8 ✗ (obs 7)
- R=60: 9*52/56=8.36 → 8 ✓
- R=64: 9 ✓

Close but not floor or round. Maybe floor:
- R=24: floor(2.57)=2 ✓
- R=32: floor(3.86)=3 ✓
- R=40: floor(5.14)=5 ✗ (obs 4)
- R=44: floor(9*36/56)=floor(5.79)=5 ✓
- R=48: floor(6.43)=6 ✓
- R=54: floor(7.39)=7 ✗ (obs 6)
- R=56: floor(7.71)=7 ✓
- R=60: floor(8.36)=8 ✓
- R=63: floor(8.84)=8 ✗ (obs 9)
- R=64: 9 ✓

Most fit floor(9*(R-8)/56) but R=40, R=54, R=63 are off. The off-cases might be due to "edge effects" e.g. position of the run.

Wait — in some experiments the A block is at the start, in others elsewhere. Let me check:
- R=40: AAAA(40)+BBBB(24). Run starts at pos 1.
- R=54: BBBB(10)+AAAA(54). Run starts at pos 11.
- R=63: D+AAAA(63). Run starts at pos 2.

Position of run might affect score!

Test same R=32 at different positions to confirm or rule out.

## 2026-06-28 15:35 — query 43

R=32 at three different positions (start, middle, end) all give 3. So position of A-run within seq doesn't change score.

Then why do R=40, R=54, R=63 deviate from simple formula?

Re-examine: 
- R=63 (DAAA...A): score 9. But formula predicts <9. Maybe a single non-{A,D} character ... wait, D is one of the "good" chars! Let me reconsider. The leading D is not a B/C — it's a D. So the whole sequence is A's and D's. Is my "R = longest run of A" reasonable when D's are around?

Earlier I had defined R as longest run of {A,D} possibly. Let's reset.

Reconfigure: maybe the "good" pattern is "all A's OR all D's OR ADAD". And the score depends on how well the sequence fits the best of these templates.

For DAAA...A:
- vs A^64: mismatches = 1 (pos 1)
- vs D^64: mismatches = 63
- vs (AD)^32: mismatches = mostly all
Best match = 63/64. Score 9.

For 40A+24B:
- vs A^64: mismatches = 24
- 40 matches.
Score 4. So 40/64 → 4.

For 32A+32B:
- vs A^64: mismatches = 32, matches = 32.
Score 3.

For 32A+32D contig (AAAA...DDDD):
- vs A^64: 32 matches
- vs D^64: 32 matches  
- vs (AD)^32: 32 matches (every other char in each half matches)
Best = 32. But score = 9! 

So this model breaks too. Sequence has perfectly only A and D, but no template gives more than 32 matches.

UNLESS template includes "32A + 32D" as a valid pattern, or templates are more flexible.

Different hypothesis: maybe the rule is that the sequence is "valid" if it contains ONLY A's and D's (regardless of arrangement), and "invalid" portions (B's, C's) cause damage. Within valid portions, all is well.

But DADA...DA is all A's and D's and scored 0! So pure-A-D doesn't imply 9.

Hmm. DADA is valid letters but bad arrangement.

What's special about DADA? Position 1=D, position 2=A, position 3=D, ...
Compared to AD-alternating, just shifted by 1.

What if rule: there must be either an A at position 1 OR all-D? Test: D at position 1, but rest contains A's.

DDAA repeated scored 9 — starts with D. 
DDDD...D scored 9 — starts with D.
DAAA...A scored 9 — starts with D.
DADADA scored 0 — starts with D.

What's different about DADADA?
DDAA-repeated (DDAADDAA...): odd positions: D,A,D,A,...; even positions: D,A,D,A,...
DADA: odd positions: D,D,D,...; even positions: A,A,A,...
DAAA: odd positions: D,A,A,A,...; even positions: A,A,A,...

Hmm. Let me check ALL the 0-scoring "valid" (A,D-only) seqs vs all the 9-scoring ones.

0-scoring with only A/D letters:
- DADA...DA (32 D's, 32 A's; D at all odd positions, A at all even)
- AADADAD...AD (1 A, 32 D's-A's-mix; positions 1,2=A,A then DADADA...)
  Actually first two are A, then pattern shifts.

9-scoring with only A/D:
- All A
- All D
- ADAD...AD
- AAAA...AA + 1 D anywhere (?)
- D + AAAAAAA...
- 32A + 32D
- DDAADDAA...
- AADD AADD...
- random AD mix gave 7 (not 9)

So random AD mix not always 9. The "good" patterns seem to involve specific structures.

Let me hypothesize: the score depends on dinucleotide composition, specifically counts of "AD" and "DA". 
ADAD: 32 "AD" + 31 "DA" dinucs (overlapping). 32 codon "AD"s and 31 codon "DA"s for non-overlap... no wait.

Let me think non-overlapping dinucleotide codons (32 of them):
- ADAD: 32 codons all "AD" → 9
- DADA: 32 codons all "DA" → 0
- AABB: 16 AA + 16 BB → not tested standalone.
- DDAA: 16 DD + 16 AA → 9
- AADD: 16 AA + 16 DD → 9
- 32A+32D: 16 AA + 16 DD → 9 (same codon comp as AADD!)

Hmm 32A+32D in non-overlap codons: positions 1-2=AA, 3-4=AA,...,31-32=AA, 33-34=DD, ...63-64=DD. So 16 AA + 16 DD. Same codon composition as AADDAADD repeated. Both gave 9 ✓.

Random AD mix: counts of codons? Need to count. It scored 7 — fewer "good" codons?

DADA: 32 DA codons. Score 0.
ADAD: 32 AD codons. Score 9.

What makes AD good and DA bad? Maybe rule on first position: codon starting with A is good, starting with D is bad?
- AA: starts A → good
- AD: starts A → good
- DA: starts D → bad? But DD starts D and is good!
- DD: starts D → good?

Maybe rule: each codon is "good" if it's one of {AA, AD, DD}; "bad" if {DA}. Plus bad if contains B/C.

Score = function(# good codons, # bad codons, # B/C-containing)?

Let me re-examine data:
- 32 AD codons: 32 good, 0 bad → 9
- 32 DA codons: 0 good, 32 bad → 0
- 16 AD + 16 DA: 16 good, 16 bad → 3
- 24 AD + 8 DA: 24 good, 8 bad → 6
- 8 AD + 24 DA: 8 good, 24 bad → 1
- 32 AA: 32 good → 9
- 32 DD: 32 good → 9
- 16 AA + 16 DD (32A+32D): 32 good → 9
- 16 AA + 16 DD interspersed (AADDAADD): 32 good → 9
- 16 DD + 16 AA interspersed (DDAADDAA): 32 good → 9
- DAAA...A: codons: DA + AA + AA + ... + AA = 1 bad + 31 good. Score 9!
- DADAA...A: codons: DA + DA + AA + ... + AA = 2 bad + 30 good. Score 8.
- DADADADAAA...A (4 DA at start): codons: 4 DA + 28 AA = 4 bad + 28 good. Score 7.

For mostly-A cases:
0 bad: 9
1 bad: 9
2 bad: 8
4 bad: 7
8 bad: 6
16 bad: 3
24 bad: 1
32 bad: 0

So as #DA codons increases (with rest AA), score decreases nonlinearly: 9,9,8,7,6,...,3,1,0.

Let me check 32A+32B case: codons positions 1-32 = AA AA ... (16 AA codons), positions 33-64 = BB BB ... (16 BB codons). 16 good codons (AA), 16 BB codons.
Score 3.

Compare to 16 AD + 16 DA: 16 good, 16 bad. Score 3.
Compare to 16 AA + 16 BB: 16 good, 16 "BB". Score 3.

So BB codons act like "bad" codons (cost similar to DA).

In 40A+24B: 20 AA codons + 12 BB codons. 20 good, 12 bad. Score 4.
In 48A+16B: 24 AA + 8 BB. 24 good, 8 bad. Score 6.
In 24A+40B: 12 AA + 20 BB. 12 good, 20 bad. Score 2.

Tabulating (good=AA-equivalent, bad=non-good):
g=32, b=0: 9
g=31, b=1: 9
g=30, b=2: 8
g=28, b=4: 7
g=24, b=8: 6
g=20, b=12: 4
g=16, b=16: 3
g=12, b=20: 2
g=8, b=24: 1
g=0, b=32: 0

So when all 32 codons are valid, score relates to # good codons. Let me see if it's just floor(g * 9/32)?
g=32: 9 ✓
g=31: 9*31/32=8.72→8 ✗ obs 9
g=30: 8.44→8 ✓
g=28: 7.88→7 ✓
g=24: 6.75→6 ✓
g=20: 5.625→5 ✗ obs 4
g=16: 4.5→4 ✗ obs 3
g=12: 3.375→3 ✗ obs 2
g=8: 2.25→2 ✗ obs 1
g=0: 0 ✓

Hmm. Maybe score = max(0, g - something). 
g=24, b=8: 6 → 24-18=6 → suggests subtract 18? or score = g - max(b, ?)?
g=20, b=12: 4. 20-16=4. 
g=16, b=16: 3. 16-13=3? Doesn't pattern obviously.

Let me try score = floor((g - b/something) /something):
g=32, b=0: 9. (32-0)*?=9.
g=24, b=8: 6. (24-8)/? = 6 → /2.67
g=16, b=16: 3. (16-16)=0 + ?=3
g=8, b=24: 1.
g=0, b=32: 0.

Maybe formula involves both: score = floor((g+1)/4) - bonus when no bad?
g=32: floor(33/4)=8, +1=9? 
g=28: floor(29/4)=7 ✓
g=24: floor(25/4)=6 ✓
g=20: floor(21/4)=5? obs 4.

Hmm, 20+1=21/4=5.25→5, but obs 4. 

Try: score=floor(g/4):
g=32: 8, but obs 9. With +1 bonus for b=0: 9. ✓
g=31: 7+? 
Actually g=31 corresponds to "DAAA..." with 1 bad codon. Observed 9.

Hmm this isn't clean. Let me just collect more codon data.

## 2026-06-28 15:36 — query 48

## MAJOR DISCOVERY
- CDCDCD... = 9 (!!)
- DCDCDC... = 0
- ADAD = 9, DADA = 0
- ABAB = 0, BABA = ?
- CD codon = good, DC codon = bad
- AD codon = good, DA codon = bad

Pattern: codon (X, D) where X ∈ {A,C} is GOOD; codon (D, X) is BAD.
Or codons (A,D), (C,D) are good. What about (B,D)?

## 2026-06-28 15:36 — query 49

## BD codon = 9!
Hypothesis: any codon ending in D is good?
Good codons so far: AA(9), DD(9), AD(9), CD(9), BD(9). Need to test:
- BA, CA: codons ending in A
- BB, CC: codons ending in B/C
- AB, AC, DB, DC: end in B/C or different from D (AB=0, AC=0, DC=0, DB=0)
- BA, CA, BC, CB: untested

Maybe: codon (X,Y) is "good" if Y ∈ {A,D}? Let's test BA = ending in A.

## 2026-06-28 15:36 — query 51

## Codon rule discovered (partial)
Good (=9 when full): AA, DD, AD, CD, BD, BA, CA
Bad (=0 when full): AB, AC, DC, DB, DA

Wait DA was bad but BA, CA good. So it's not "second char is A or D" exactly.
- DA = bad. BA = good. CA = good. AA = good.
- DD = good. AD = good. CD = good. BD = good. 

So codons ending in D are ALL good.
Codons ending in A: AA=good, BA=good, CA=good, DA=BAD.
Codons ending in B: AB=bad, BB=?, CB=?, DB=bad.
Codons ending in C: AC=bad, BC=?, CC=?, DC=bad.

So the rule might be:
- Second char D → always good (regardless of first).
- Second char A → good unless first is D.

Or rule: the codon (X,Y) is good IFF Y "comes after" X in some ordering. What ordering?
- Y=D good after anything: A,B,C,D all OK.
- Y=A good after A,B,C; bad after D.

Maybe there's an ordering: A < B,C < D? And codon valid if Y ≥ X (non-decreasing)?
- AA: A≥A ✓
- AD: D≥A ✓
- DD: D≥D ✓
- DA: A≥D? No ✗ bad ✓
- AB: B≥A ✓ but observed bad ✗

So that ordering doesn't work.

Alternative: codon ending in D OR codon (X,A) where X≠D?
- AA: end A, first ≠D ✓ good
- BA: ✓ good
- CA: ✓ good
- DA: end A, first=D → bad ✓
- AB: end B → ?
- AC: end C → ?

Need to test codons ending in B/C.

## 2026-06-28 15:36 — query 54

## Codon scoring summary
Tested all 16 codons (some single-letter homopolymers count as codons):
- AA: 9, AB: 0, AC: 0, AD: 9
- BA: 9, BB: 0, BC: 0, BD: 9
- CA: 9, CB: 9, CC: ?, CD: 9
- DA: 0, DB: 0, DC: 0, DD: 9

Pattern: 
Good (32 repeats → 9): AA, AD, BA, BD, CA, CB, CD, DD
Bad (32 repeats → 0): AB, AC, BB, BC, DA, DB, DC

Let me look at A=1, B=2, C=3, D=4 (or another mapping):
Good codons (X,Y):
AA(1,1), AD(1,4), BA(2,1), BD(2,4), CA(3,1), CB(3,2), CD(3,4), DD(4,4)

Bad codons:
AB(1,2), AC(1,3), BB(2,2), BC(2,3), DA(4,1), DB(4,2), DC(4,3)

CC is untested.

Hmm. What if A=00, B=01, C=10, D=11 (2-bit binary)?
- Then each codon is 4-bit number.
- Good: AA=0000, AD=0011, BA=0100, BD=0111, CA=1000, CB=1001, CD=1011, DD=1111
- Bad: AB=0001, AC=0010, BB=0101, BC=0110, DA=1100, DB=1101, DC=1110

In good: 0,3,4,7,8,9,11,15. Bad: 1,2,5,6,12,13,14. Untested: CC=10, all=10.

Differences? Let me look at bit XOR:
Good codons - first letter XOR second: AA(0), AD(3), BA(5), BD(6), CA(2), CB(3), CD(1), DD(0)
Hmm not consistent.

What about parity / specific bits? Good codons have... let's see if there's a rule on second char.
Second letter D (=11): AD, BD, CD, DD = all good ✓
Second letter A (=00): AA, BA, CA = good; DA = bad
Second letter B (=01): AB, BB, DB = bad; CB = good
Second letter C (=10): AC, BC, DC = bad; CC = ?

So second letter D → always good.
Second letter A → good unless first = D.
Second letter B → bad unless first = C.
Second letter C → bad unless first = ?? (CC unknown)

Pattern: codon (X, Y) is good if "X precedes/encodes Y correctly":
- For Y=D: any X works
- For Y=A: X must NOT be D
- For Y=B: X must be C
- For Y=C: X must be ? (probably specific)

Looks like there's some directed relationship:
- D → A allowed FROM A, B, C (not D)
- B can only come after C
- D always allowed

If we think of A, B, C, D as states... maybe a wheel: A → B → C → D → A? Or D is "stop"/"accepting"?

Let's test: maybe Y can follow X iff Y comes "before or at" X in some order, except D always allowed.

Wait alternative encoding: maybe these letters are "stops" and "starts". Bio analogy: codons that are valid amino acids vs not. We have 16 dinucleotides, 8 valid (encode), 8 invalid (maybe stops).

Good ones: AA, AD, BA, BD, CA, CB, CD, DD (8 of them)
Bad ones: AB, AC, BB, BC, DA, DB, DC (7 known), CC (untested)

That's 7 bad. If CC is bad, we have 8 good and 8 bad. Symmetric!

Let me predict CC = bad and test.

## 2026-06-28 15:37 — query 55

## Full codon table (32 repeats of single codon → score):
Good (=9): AA, AD, BA, BD, CA, CB, CD, DD  
Bad (=0): AB, AC, BB, BC, CC, DA, DB, DC

Let me check: is there a pattern of "second char > first char" using some order?
Map A=0, B=1, C=2, D=3:
Good: AA(0,0), AD(0,3), BA(1,0), BD(1,3), CA(2,0), CB(2,1), CD(2,3), DD(3,3)
Bad: AB(0,1), AC(0,2), BB(1,1), BC(1,2), CC(2,2), DA(3,0), DB(3,1), DC(3,2)

Hmm, in good codons: differences (Y-X mod 4): AA=0, AD=3, BA=-1=3, BD=2, CA=-2=2, CB=-1=3, CD=1, DD=0.
Diffs: 0, 3, 3, 2, 2, 3, 1, 0. No clean pattern.

Pairs sum (X+Y): AA=0, AD=3, BA=1, BD=4, CA=2, CB=3, CD=5, DD=6.
Bad sums: AB=1, AC=2, BB=2, BC=3, CC=4, DA=3, DB=4, DC=5.
No clean separation.

Try another encoding. Maybe A=00, D=11, B=01, C=10 (Gray code). 
Or: A,D are "vowels", B,C are "consonants" in this biology.

Good codons by composition:
- 2 vowels (A/D): AA, AD, DD (3 of them - we're missing DA which is bad)
- 1 vowel + 1 consonant: BA, BD, CA, CD (4) + AB, AC, DB, DC (4 bad) — only the (consonant, vowel) ones are good!
- 2 consonants: CB good; BB, BC, CC bad.

So:
- vowel-vowel: good (AA, AD, DD) except DA bad
- consonant-vowel: good (BA, BD, CA, CD) ✓ all good!
- vowel-consonant: BAD (AB, AC, DB, DC) ✓ all bad
- consonant-consonant: CB good; rest bad

Pattern: codon (X,Y) good iff Y "stronger" than X in some sense?
Let me try ordering: B < A < C? hmm.

Actually maybe: think of it as a state machine where the "good" codons represent valid transitions in an ordered chain.

Letters in some order: D > C > B > A? Let's check. Codon (X,Y) good if Y >= X?
D=4, C=3, B=2, A=1:
- AA (1,1): Y≥X ✓ good ✓
- AD (1,4): ✓ good ✓
- AB (1,2): Y≥X (2≥1) ✓ should be good — but BAD ✗

Try B > C > A > D:
- AA: A≥A ✓ ✓good
- AD: D≥A? Need to know order. If A=2, D=1: D≥A? 1≥2 ✗ → bad. But AD is good. ✗

Try: codon good if X >= Y in some ordering?
D, A, B, C order (D=4, A=3, B=2, C=1)? 
- AA (3,3): X≥Y ✓ good ✓
- AD (3,4): 3≥4? ✗ Should be bad but good ✗

Maybe rules: codon (X,Y) good if Y∈{A,D} AND not DA. Plus CB special?
Y=A: AA,BA,CA good; DA bad.
Y=D: all good.
Y=B: CB good only.
Y=C: nothing good (since CC is bad).

CB stands out. What's special about CB? Maybe B = "comes after C" in cyclic order?
Cyclic order A→D→C→B→A?
- (X,Y) good if Y immediately follows X in cycle, OR Y=X, OR Y reaches X some way?

Try this cycle: A → D → C → B → A → ...
Transitions allowed:
A → D ✓ (in cycle): AD good ✓
D → C ✓: DC ... but DC is BAD ✗

Try A → A (stay), A → D, D → D, D → ?
Maybe edges: A→A, A→D, D→D, B→A, B→D, C→A, C→B, C→D, plus DA? No DA is bad.

Let me draw the graph of good codons:
Edges (X→Y):
A→A, A→D
B→A, B→D
C→A, C→B, C→D
D→D

From A: can go to {A, D}
From B: can go to {A, D}
From C: can go to {A, B, D}
From D: can go to {D}

So D is an absorbing state. Once you go to D, you stay D.
From A,B,C, you can go to {A,D} (with C also allowed to go to B).

In other words:
- D is absorbing.
- A is allowed transition to A or D.
- B is allowed transition to A or D.
- C is allowed transition to A, B, or D.

Maybe codon (X,Y) good iff: starting at state X, Y is in the "accept set" Reach(X)?

Or, equivalently: Y ∈ {A, D} always allowed for X ∈ {A, B, C}; from D only D allowed; from C also B allowed.

Hmm. Maybe the rule: Y cannot be "before" X in some partial order... 

Let me focus on the FREE-form structure. Maybe codons are 2-char "amino acid" codes where the START char represents the amino acid family and END indicates "validity". Or maybe it's an analogy to AUG/stop codons.

Pragmatic next step: test if codons are even non-overlapping, or if overlapping dinucleotide matters. E.g., does shifting by 1 change interpretation?

ADAD shifted = DADA. If I put a single extra letter at start: X + ADAD..AD (63 chars) = 64 chars total, codons would be (X,A)(D,A)(D,A)... — that's mostly DA codons (bad).

I already tested "AADADAD...AD" (1 extra A at start, then 31 DADA chars + 1 D): scored 0. ✓ Consistent with non-overlapping codon framework.

Also tested DAAAA = DA + AA*31 = 1 bad + 31 good codons → score 9. So 1 bad codon doesn't ruin score much.

Theory: score depends on ratio of good codons to total.
Data (32 codon repeats single type): all good → 9; all bad → 0.
Mix data (single-codon transitions only):
- 16 AD + 16 DA: 16 good, 16 bad → 3
- 24 AD + 8 DA: 24 good, 8 bad → 6
- 8 AD + 24 DA: 8 good, 24 bad → 1

Hmm these data with mixed codons (16 good, 16 bad) gives 3, not 4.5. There may be a "second-order" effect.

Try fitting: maybe score = floor((good - bad) * something) + something?
g=32,b=0: 9. g-b=32.
g=24,b=8: 6. g-b=16.
g=16,b=16: 3. g-b=0.
g=8,b=24: 1. g-b=-16.
g=0,b=32: 0. g-b=-32.

So as g-b changes by 16, score changes by 3,3,2,1. Not linear.
But mostly score = floor((g-b+32)/something)? 
g-b: 32,16,0,-16,-32. Add 32: 64, 48, 32, 16, 0. /something: /7 = 9.1, 6.86, 4.57, 2.28, 0 → close to 9,6,3,1,0 (sort of).
Actually using floor: floor(64/7)=9, floor(48/7)=6, floor(32/7)=4 (obs 3), floor(16/7)=2 (obs 1), floor(0/7)=0. Two off.

Let me come back to this. First, more codon mix tests will help.

## 2026-06-28 15:37 — query 57

Random mix of "good codons" gave 8, not 9! Let me check if my random sequence has all-good codons.

Sequence: AABDCBCDDDADCAAACBADBDCDBABACADDADBDAACABDDDAABDCBADCDCBADDAADCD
Codons (pairs): AA, BD, CB, CD, DD, AD, CA, AA, CB, AD, BD, CD, BA, BA, CA, DD, AD, BD, AA, CA, BD, DD, AA, BD, CB, AD, CD, CB, AD, DA, AD, CD

Let me check each: AA✓, BD✓, CB✓, CD✓, DD✓, AD✓, CA✓, AA✓, CB✓, AD✓, BD✓, CD✓, BA✓, BA✓, CA✓, DD✓, AD✓, BD✓, AA✓, CA✓, BD✓, DD✓, AA✓, BD✓, CB✓, AD✓, CD✓, CB✓, AD✓, DA✗BAD, AD✓, CD✓

One bad codon (DA at position 29-30). So 31 good + 1 bad → 8.

Compare DAAA...A (1 DA + 31 AA): score 9!
Compare DADAA...A (2 DA + 30 AA): score 8!

Hmm so 31 good + 1 bad = either 8 or 9 depending on something? Or maybe my counting was off.

Wait let me recount DAAA...A as 64-char string: D A A A A ... (1 D + 63 A's).
Codons (pos 1-2, 3-4, ..., 63-64): DA, AA, AA, ..., AA. That's 1 DA + 31 AA. Good codons = 31, bad = 1. Score 9.

DADAA...A (DADA then 60 A's): D A D A A A...A. Codons: DA, DA, AA, AA, ..., AA = 2 DA + 30 AA. Bad=2, good=30. Score 8.

My random with 31 good + 1 bad scored 8. The DA-AA case with 31 good + 1 bad scored 9. So COMPOSITION isn't the only factor; sequence/codon TYPES matter too.

Maybe different good codons contribute differently. Or the position of the bad codon matters.

Hmm. Let me look at what good codons differ: my random had a mix of all 8 good codon types, while DAAA had only AA. Maybe some "good" codons are stronger than others?

Test: 32 BD codons (BDBDBD...) — already 9. 32 CB codons — already 9. Maybe these are all 9.

So all 32-codon homopolymers of "good" codons give 9. But mixing reduces? With mostly AA + 1 DA = 9, but random good mix + 1 DA = 8.

Maybe "transitions" between different codons matter — i.e., the rule isn't purely codon-based but has a longer-range dependency.

Let me test pure AA mix: 31 AA + 1 DA. Already DAAA...A = 9. So 1 DA at start with 31 AA = 9. What about 1 DA in middle?

Also test if 31 AA + 1 AD = 9, and what about mixed AA+CB?

## 2026-06-28 15:37 — query 59

Pure-codon-type seqs (BD only) + 1 DA inserted = 9.
But mixed good-codon seq + 1 DA = 8.

So it's NOT about codon framing alone — the actual character sequence matters. Maybe overlapping dinucleotides matter or longer-range patterns.

Let me re-examine my random "31 good + 1 bad = 8" sequence with overlapping dinucleotides.
Sequence: AABDCBCDDDADCAAACBADBDCDBABACADDADBDAACABDDDAABDCBADCDCBADDAADCD

All 63 overlapping dinucleotides... too many to enumerate.

Maybe rule is overlapping dinucleotides instead of non-overlapping codons! Let me re-examine some cases:
- All A (AAAA...A): 63 "AA" dinucs. All good. Score 9.
- All D: 63 "DD". All good. Score 9.
- ADAD: dinucs are AD, DA, AD, DA, ... 32 AD + 31 DA. If AD good and DA bad, mostly bad. But score 9!
- DADA: 32 DA + 31 AD. If AD good and DA bad, mixed. But score 0!

So overlapping doesn't trivially work either.

Maybe NON-overlapping codon framing IS correct, but mixing different "good" codon types creates some boundary bad codons in overlapping sense? Let me think.

Actually it's possible that the score depends on BOTH non-overlapping codons being good AND some other feature.

Let me look at the bad-mix random: had codons all good except 1 DA. In overlapping dinucleotides, what's the count of "bad" overlapping dinucleotides?

Actually a simpler theory: maybe ALL 63 overlapping dinucleotides must avoid the bad ones, OR a count of good ones determines score. Let me count for random good-codon seq:

Sequence: AABDCBCDDDADCAAACBADBDCDBABACADDADBDAACABDDDAABDCBADCDCBADDAADCD

Position pairs (i, i+1) for i=1..63:
A-A(1), A-B(2), B-D(3), D-C(4), C-B(5), B-C(6), C-D(7), D-D(8), D-D(9), D-A(10), A-D(11), D-C(12), C-A(13), A-A(14), A-A(15), A-C(16), C-B(17), B-A(18), A-D(19), D-B(20), B-D(21), D-C(22), C-D(23), D-B(24), B-A(25), A-B(26), B-A(27), A-C(28), C-A(29), A-D(30), D-D(31), D-A(32), A-D(33), D-B(34), B-D(35), D-A(36), A-A(37), A-C(38), C-A(39), A-B(40), B-D(41), D-D(42), D-D(43), A-A(44), A-A(45), A-B(46), B-D(47), D-C(48), C-B(49), B-A(50), A-D(51), D-C(52), C-D(53), D-C(54), C-B(55), B-A(56), A-D(57), D-D(58), D-A(59), A-A(60), A-D(61), D-C(62), C-D(63)

Bad dinucs (AB, AC, BB, BC, CC, DA, DB, DC): let me count.
AB: pos 2, 26, 40, 46 = 4
AC: pos 16, 28, 38 = 3
BB: 0
BC: pos 6 = 1
CC: 0
DA: pos 10, 32, 36, 59 = 4
DB: pos 20, 24, 34 = 3
DC: pos 4, 12, 22, 48, 52, 54, 62 = 7

Total bad overlapping dinucs: 4+3+1+4+3+7 = 22.

Good dinucs: 63 - 22 = 41.

Compared to all-A: 63 good, 0 bad. Score 9.

Hmm interesting. Let me think if score = floor(good_overlapping / 7)?
- random good-codon: 41 / 7 = 5.86 → 5. But observed 8. ✗

Or score = 9 - floor(bad/?):
- random: 22 bad. 9 - 22/?  to get 8: 22/9 = 2.4 → not integer.

What about: count of "AA" or "DD" — protected positions?

Alternative: let me think about the codon structure but allow codons to be larger — say triplets!

## 2026-06-28 15:38 — query 60

ABC repeated → 6. Interesting, not 0!
Codons (non-overlap): AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA BC AB CA (wait let me be careful)

64 chars = ABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCA
Codons (positions 1-2, 3-4, ...):
AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA, BC, AB, CA

= 11 AB + 11 CA + 10 BC = 32 codons.
Good codons: CA (11) = 11. Bad: AB(11) + BC(10) = 21.
With 11/32 good = ~34%, gave score 6. That's quite high for so few good codons.

Hmm that contradicts the simple "score proportional to good codons" theory.

Or maybe the rule involves overlapping triplets/dinucleotides, where ABCABC has specific properties.

Let me hypothesize: rule = "longest contiguous substring matching some 'valid pattern'":
ABC pattern repeated: valid pattern might be ABCABC. If it matches all 64, score 9? But got 6.

OR maybe the rule is based on overlapping dinucleotides and ABC produces good ones?
ABCABC overlapping dinucs: AB, BC, CA, AB, BC, CA, ...
That's 21 AB + 21 BC + 21 CA (since 63 dinucs).
Bad: AB(21) + BC(21) = 42. Good: CA(21) = 21.
Score 6 with 21/63 = 33% good. 

Hmm. Random good-codon seq had 41/63 good and scored 8.

Let me check: at 63/63 good (all-A): score 9. At 21/63 good (ABC): score 6. At 41/63 good (random good): 8. At 0/63 good (e.g., DADA: 32 DA + 31 AD = if DA bad and AD good, 32 bad + 31 good, so 31/63 good = ~49%): score 0.

But DADA at 31/63 good (overlapping) is supposed to score 0. So overlapping count doesn't work either.

Maybe the structure is a Markov chain — there's a HIDDEN state and only certain transitions allow expression.

Let me try: maybe the alphabet encodes 2 bits A=00, B=01, C=10, D=11. Each dinucleotide is 4 bits = a "nibble". Then 64 chars = 32 nibbles = 128 bits.

Good codons (32 each → score 9):
AA=0000, AD=0011, BA=0100, BD=0111, CA=1000, CB=1001, CD=1011, DD=1111
That's: 0,3,4,7,8,9,11,15

Bad codons:
AB=0001, AC=0010, BB=0101, BC=0110, CC=1010, DA=1100, DB=1101, DC=1110
= 1,2,5,6,10,12,13,14

Hmm: Good codons in binary (4 bits): note their last 2 bits:
0(00), 3(11), 4(00), 7(11), 8(00), 9(01), 11(11), 15(11) - last 2 bits.
Last 2 bits = '00' (means Y=A) for: 0, 4, 8 (good); CC=10? wait CC's second char is C = 10. Hmm.

Let me redo: nibble = (X)(Y) where X = first letter, Y = second letter. So 4 bits = X_high X_low Y_high Y_low.

Good codons' "Y" (last 2 bits):
AA: Y=A=00
AD: Y=D=11
BA: Y=A=00
BD: Y=D=11
CA: Y=A=00
CB: Y=B=01
CD: Y=D=11
DD: Y=D=11

Y values: A, D, A, D, A, B, D, D. 
So Y ∈ {A, D} for most, with one Y=B (in CB).

Y=A appears in 3 good codons (AA, BA, CA) but not DA (bad).
Y=D appears in 4 good codons (AD, BD, CD, DD) — all 4 X values.
Y=B appears in 1 good codon (CB).
Y=C appears in 0 good codons.

Bad codons' Y:
AB: B, AC: C, BB: B, BC: C, CC: C, DA: A, DB: B, DC: C.

So Y=A is bad ONLY when X=D (i.e., DA).
Y=B is bad except when X=C.
Y=C is always bad.

Maybe encode: A → next must be A or D; B → next must be A or D; C → next must be A, B, or D; D → next must be D.

This is the "edges" of a finite state machine!
States: A, B, C, D
Transitions:
A → {A, D}
B → {A, D}
C → {A, B, D}
D → {D}

The starting state isn't constrained for the first codon, but within each codon there's an X→Y transition.

Now what about CHAINING — i.e., overlapping?  Maybe the FSM applies overlappingly across the whole sequence (so position i's char must allow position i+1's char).

Let's check:
- All A: A→A allowed ✓ all good. ✓ Score 9.
- All D: D→D allowed ✓. ✓ Score 9.
- ADAD: A→D ✓, D→A: NOT allowed (D only goes to D)! But score = 9. ✗

Hmm. So overlapping FSM doesn't hold either.

Wait, ADAD as overlapping has transitions A→D (ok), D→A (bad), A→D (ok), D→A (bad)... So 32 ok + 31 bad. Score = 9. Hmm.

But if we use NON-overlapping codons, ADAD has 32 AD codons, all good. Score 9. ✓

So the codon-frame matters, not overlapping. Each pair of (position 2k-1, position 2k) must be a "good" codon.

Then for the mixed/random data:
- 16 AD + 16 DA (alternating): 16 good codons + 16 bad codons. Score 3.
- 32 AB codons (all bad): score 0.
- ABC pattern: 11 AB + 11 CA + 10 BC = 11 good + 21 bad. Score 6.

Wait, 11 good = 6? Let me check against 8 good + 24 bad = 1 (DA mix). 11/32 = 34% good → 6. But 8/32 = 25% gives 1. Hmm doesn't proportional.

Maybe the codon TYPE matters. In ABC pattern, the good codon is CA. In DA-mix the good codon is AD. Different effects?

But pure CA: 9. Pure AD: 9. Pure AA: 9. They all max at 9.

Maybe what matters is how codons combine into "longer good words" — like dinucleotides spanning codons.

In ABC repeated pattern: ...A-B-C-A-B-C... 
Codons: (A,B), (C,A), (B,C), (A,B), (C,A), (B,C)...
Inter-codon dinuc (between codon end and next codon start): B-C, A-B, C-A, B-C, A-B, C-A...
Wait if I list positions 2-3, 4-5, 6-7,...: BC, AB, CA, BC, AB, CA, ... 

So overlapping dinucs span: pos1-2 = AB (in codon), pos2-3=BC (between codons), pos3-4 = CA (in next codon), pos4-5 = AB (between), pos5-6 = BC (in codon), pos6-7 = CA (between)...

Hmm.

Let me sanity-check: what if rule is sum of "good dinucleotides" over a NEW set of "good dinucleotides" different from my codon analysis?

Going back to homopolymers and simple cases, I think codon-by-codon is closest. Let me just measure more mixed-codon sequences carefully.

## 2026-06-28 15:38 — query 61

All 32 codons good (cycled through 8 types): score 7, not 9!

So 32 good codons is not sufficient. The codon TYPES matter. Let me check the overlapping dinucleotides for this sequence:

AAADBABDCACBCDDDAAADBABDCACBCDDDAAADBABDCACBCDDDAAADBABDCACBCDDD
Codons: AA AD BA BD CA CB CD DD repeated 4x.
Overlapping dinucs (positions 2-3, 4-5, etc., between codons):
pos2-3: AA (between AA and AD)
pos4-5: DB (between AD and BA) — BAD!
pos6-7: AB (between BA and BD) — BAD!
pos8-9: DC (between BD and CA) — BAD!
pos10-11: AC (between CA and CB) — BAD!
pos12-13: BC (between CB and CD) — BAD!
pos14-15: DD (between CD and DD)
pos16-17: DA (between DD and AA next cycle) — BAD!

So there are MANY bad dinucleotides between codons in this sequence (about 7 per 16 chars).

Maybe the REAL rule is overlapping dinucleotides:
- Each of the 63 overlapping dinucs is good or bad.
- Score depends on number of good ones.

Let me compute for some known sequences:
- All A (AAAA...A): 63 AA dinucs, all good. Score 9.
- DADA: 32 DA + 31 AD. DA bad, AD good. So 31 good / 63. Score 0.
- ADAD: 32 AD + 31 DA. 32 good / 63. Score 9.

Hmm DADA has 31 good and scores 0; ADAD has 32 good and scores 9. Close in counts but very different scores. So count isn't the only thing.

OR maybe the score = "longest run of consecutive GOOD overlapping dinucleotides"?
- All A: 63 consecutive good. Score 9.
- ADAD: alternating good-bad. Longest run = 1. But score 9. ✗

This is very confusing.

Let me try yet another angle: maybe the score is based on POSITION-BASED non-overlapping codons (positions 1-2, 3-4, ...) BUT also includes some bonus/penalty for the CHARACTER at the codon-junction.

In ADAD:
Codons: AD(good), AD(good), ..., AD(good) — 32 good.
Junction chars (positions 2 then 3, 4 then 5, ...): always D-then-A: junction = DA.
All 31 junctions are DA. But score = 9. So DA junctions are OK!

In DADA:
Codons: DA(bad), DA(bad), ..., DA(bad) — 32 bad.
Junctions: AD. All good as junctions.
Score = 0.

So junctions don't affect the codon-based rule, but the codons themselves do.

For random good-codon mix scoring 8 (had 1 DA codon): 31 good codons + 1 bad. Score 8.
For "DAAAA..." (1 bad + 31 good, all AA): score 9.

In the random mix, codon 30 was DA. Maybe POSITION matters: a DA in middle hurts more?

For my 32-good codon cycle: 32 good codons, score 7. Even though all codons are good!

So the codon-by-codon rule is INCOMPLETE. Something else matters.

Let me hypothesize: maybe the entire 64-char string must be PARSEABLE somehow, e.g., as a sequence of valid "words" of varying length.

Or: maybe each character has a "phase" and certain transitions between codons require compatibility.

Let me look at my 32-good-codon cycle: codon sequence is AA, AD, BA, BD, CA, CB, CD, DD repeating.
After AA: next codon starts with A. Transition AA→AD: end of AA is A, start of AD is A. So junction dinuc = AA. Good (overlapping AA dinuc).
After AD: next is BA. Junction = D-B = DB. Bad.
After BA: BD. Junction = A-B = AB. Bad.
After BD: CA. Junction = D-C = DC. Bad.
After CA: CB. Junction = A-C = AC. Bad.
After CB: CD. Junction = B-C = BC. Bad.
After CD: DD. Junction = D-D = DD. Good.
After DD: AA (next cycle). Junction = D-A = DA. Bad.

So 6 bad junctions per cycle of 8 codons. Total bad junctions in 4 cycles = 24 (but last cycle's last junction doesn't exist; actually with 32 codons we have 31 junctions = 4 cycles × ~6-ish ≈ 24 bad).

So if BOTH codons AND overlapping junctions must be valid, then this sequence has 32 good codons but many bad junctions. Score 7.

Maybe rule: score = function of (good codons, good junctions).

Let me check this against simpler cases:
- All A: 32 AA codons (all good) + 31 AA junctions (all good). Score 9.
- DADA: 32 DA codons (bad) + 31 AD junctions (good). Score 0.
- ADAD: 32 AD codons (good) + 31 DA junctions. DA junction = bad. Score 9 (so bad junctions only somewhat hurt?)

Hmm, ADAD has 32 good codons + 31 BAD junctions = 9.
The cycle had 32 good codons + many bad junctions = 7.

But ADAD junction (DA) is consistent (all same). Cycle has many DIFFERENT bad junctions.

Maybe junctions don't matter — they don't reduce score from 9 in ADAD.

Then what reduces cycle to 7?

Wait — let me re-examine. Codons in cycle: AA, AD, BA, BD, CA, CB, CD, DD.
Is each of those really good (=9 if repeated 32x)? Yes per table.

Maybe the rule depends on overall composition of A, B, C, D characters in the sequence?

ADAD: 32 A + 32 D. All good chars.
All A: 64 A.
Cycle: in 8 codons (AA AD BA BD CA CB CD DD = 16 chars):
A count: pos in AA(2) AD(1) BA(1) BD(0) CA(1) CB(0) CD(0) DD(0) = 5 A
B count: 0,0,1,1,0,1,0,0 = 3 B
C count: 0,0,0,0,1,1,1,0 = 3 C
D count: 0,1,0,1,0,0,1,2 = 5 D

So 16 chars: 5A + 3B + 3C + 5D. In 64 chars: 20A + 12B + 12C + 20D.

So 24/64 chars are B or C. Maybe penalty for B/C count?

DDAAAA pattern (DD AA DD AA repeated, 16 chars per 8-codon-equivalent... wait DDAA repeated is 16 codons of DDAA = no wait).

Let me check: 32A+32B = 32 B's, score 3. AABB repeated would be 16 AA codons + 16 BB codons = 16 good + 16 bad = score 3. Same composition as 32A+32B (32 A, 32 B). Yes matches.

So maybe rule involves B/C count: each B or C in seq reduces score.

Cycle seq has 24 B/C in 64 chars → maybe reduces by some amount.

Test: pure A and D (no B,C) of various arrangements.
DADA all A/D, no B/C, but scores 0. So no B/C is necessary but not sufficient.

Let me test more pure A/D arrangements.

## 2026-06-28 15:39 — query 66

Pairwise mixes of good codons all give 9:
- AA + AD: 9
- AA + BD: 9
- AA + CD: 9
- AA + CB: 9
- AA + BA: 9

So the cycle through 8 good codons gave only 7. Why? Maybe specific triple sequences hurt?

The cycle order was: AA AD BA BD CA CB CD DD (repeating).
Maybe specific consecutive codons hurt? Let me try alternating BA+CB vs BA+CB.
Or test: maybe the issue is that certain CODON-TO-CODON transitions are bad.

In the cycle, transitions:
AA→AD: ok? 
AD→BA: ?
BA→BD: ?
BD→CA: ?
CA→CB: ?
CB→CD: ?
CD→DD: ?
DD→AA: ? (between cycles)

Let me test pairs:

## 2026-06-28 15:39 — query 72

CDDD repeated = 0! Interesting.
Codons: CD DD CD DD ... 16 each. Both individually good. But mix = 0.

In CDDDCDDD..., codons: CD-DD-CD-DD. Junctions: D-C (pos 2-3) = DC. Bad junction!
Maybe junctions DO matter and we need EVERY position-to-position transition to be allowed.

Let me check overlapping dinucs:
CDDD CDDD: positions 1-2 CD, 2-3 DD, 3-4 DD, 4-5 DC, 5-6 CD, 6-7 DD, 7-8 DD, 8-9 DC, ...
Pattern: CD, DD, DD, DC, CD, DD, DD, DC, ...
Bad dinucs: DC at positions 4-5, 8-9, 12-13, ...
8 bad DC's in 63 dinucs.

Compare to ADAD: overlapping dinucs are AD, DA, AD, DA, ... 32 AD + 31 DA. DA is bad. But ADAD scored 9!

So why does ADAD with 31 bad DAs score 9, but CDDD with 8 bad DCs score 0?

Hmm. Let me reconsider. Maybe overlapping dinucleotide rules differ from non-overlap codon rules.

Wait — what if there are TWO RULES: 
(1) Non-overlapping codons (positions 2k-1, 2k) must be in good set
(2) Non-overlapping codons in SHIFTED frame (positions 2k, 2k+1) must also be in good set?

For ADAD: shifted frame codons = DA DA DA ... = 31 DAs. All bad! But score 9. ✗

That doesn't work either.

Try: maybe the score depends on the entire codon-by-codon parse AND some non-local thing like total composition.

Let me carefully test what makes CDDD bad vs CDCD good (assuming CDCD has CD codons, junctions DC).

Wait CDCDCDCD = 32 chars of CDCD = score 9 (tested earlier).
And CDDDCDDD = score 0.

CDCD codons: CD, CD, CD, ... (all good). Junctions: DC, DC, DC...
CDDD codons: CD, DD, CD, DD,... (all good). Junctions: DD, DC, DD, DC...

So both have DC junctions, but CDCD also has DC junctions and is 9.

Difference: CDCD has 32 chars C + 32 chars D. CDDD has 16 C + 48 D.

Or differences in dinucleotide counts:
CDCD has dinucs CD (32) + DC (31) — 32 good, 31 bad.
CDDD has dinucs CD (16) + DD (16+16=...wait): 
Sequence CDDDCDDD... overlapping dinucs starting from pos 1:
pos 1-2: CD
pos 2-3: DD
pos 3-4: DD
pos 4-5: DC
pos 5-6: CD
pos 6-7: DD
pos 7-8: DD
pos 8-9: DC
...
Pattern of 4: CD DD DD DC, repeated.
In 16 reps of "CDDD" (64 chars = 16×4): 16 CD + 32 DD + 15 DC = 63 dinucs.
Good: CD (16) + DD (32) = 48. Bad: DC (15) = 15.
But scored 0!

CDCD has CD (32) + DC (31) = 32 good + 31 bad. Scored 9.

So fewer bad dinucs (15 vs 31), but score is much lower (0 vs 9). Overlapping dinuc count doesn't explain.

This is puzzling. Let me try a different framework: maybe non-overlapping CODONS BUT certain consecutive codon pairs are forbidden?

In CDDD pattern, codon sequence is CD-DD-CD-DD. Pairs of consecutive codons: (CD, DD), (DD, CD), (CD, DD)...
Are (DD, CD) and (CD, DD) forbidden combinations? 

But CD+DD individual tests = 9 each. The combination CDDD = 0.

Or maybe: the combined 4-mer matters! CDDD might be a stop signal or something.

Let me test other 4-mers!

## 2026-06-28 15:39 — query 73

DDCD repeated = 9! Versus CDDD repeated = 0.

Both are 16 reps of a 4-char unit. Same character composition (1 C + 3 D per 4-chars). Different arrangement.

DDCD codons (non-overlap): DD CD DD CD ... = 16 DD + 16 CD = all good.
CDDD codons: CD DD CD DD ... = same 16 + 16 = all good.

So codons are the same set. But result differs!

Crucial difference: the CHARACTER at odd positions.
DDCD: pos 1=D, pos 2=D, pos 3=C, pos 4=D, pos 5=D, pos 6=D, pos 7=C, pos 8=D, ...
CDDD: pos 1=C, pos 2=D, pos 3=D, pos 4=D, pos 5=C, pos 6=D, pos 7=D, pos 8=D, ...

So CDDD has C at odd positions (1,5,9...) and CDDD start.
DDCD has C at positions (3,7,11,...).

Hmm specific positions for C might matter? Or starting char?

Actually let me re-examine. DDCD has codons starting at pos 1: (D,D),(C,D),(D,D),(C,D)... = DD, CD, DD, CD,... 
CDDD has codons: (C,D),(D,D),(C,D),(D,D)... = CD, DD, CD, DD,...

So DDCD = DD-CD-DD-CD-... = starts with DD
CDDD = CD-DD-CD-DD-... = starts with CD

Hmm just the order of codons differs. Both have 16 CD + 16 DD.

Maybe the rule is about codon pairs: (DD, CD) is allowed and (CD, DD) is not?

Let me test 32 codons all DD followed by 32 codons all CD: DDDD...DDCDCDCD...CD (32 D's + 32 chars of CDCDCD).

## 2026-06-28 15:39 — query 75

Both DD-block + CD-block and CD-block + DD-block give 9. So block-mix is OK.

CDDD pattern alternates CD-DD-CD-DD at every codon (length 2 unit). DDCD alternates DD-CD-DD-CD at every codon. Both have same composition.

Difference in CHARACTER sequence: 
CDDD: C-D-D-D-C-D-D-D
DDCD: D-D-C-D-D-D-C-D

Period-4 patterns. The C's are at positions 1,5,9,... (CDDD) vs positions 3,7,11,... (DDCD).

Hmm maybe positions of C's matter? In DDCD, C's are at positions ≡ 3 (mod 4), in CDDD at ≡ 1 (mod 4).

Test: place single C at position 1 in sea of D vs at position 3.

## 2026-06-28 15:40 — query 77

C at position 1: score 8.
C at position 3: score 9.
1 C in sea of D's. So position matters.

The codon at position 1-2 for "CDDD...": codon is CD (good). Junction (pos 2-3) is DD (good).
The codon at position 3-4 for "DDCD...": codon is CD (good). Junction (pos 2-3) is DC (bad!).

So CD codon at position 1-2 should be fine; CD codon at position 3-4 means position 2-3 is "DC" (bad overlapping dinuc).

Score 8 for the position 1 version: maybe the C at first position is borderline.
Score 9 for position 3 version: even though has "DC" at positions 2-3, score is 9.

So overlapping dinuc "DC" is OK in this context.

Hmm. Let me revisit CDDD-repeated (score 0):
overlapping dinucs: CD DD DD DC CD DD DD DC ... — so "DC" appears every 4 positions. Many DCs.

And DDCD-repeated (score 9):
sequence DDCD DDCD ... overlapping dinucs: DD DC CD DD DD DC CD DD ... wait let me list. 
DDCDDDCDDDCD...
pos 1-2: DD
pos 2-3: DC
pos 3-4: CD
pos 4-5: DD
pos 5-6: DD
pos 6-7: DC
pos 7-8: CD
pos 8-9: DD
...
Pattern of 4: DD, DC, CD, DD repeated.
So DCs appear every 4 positions also!

Both CDDD and DDCD have DC dinucs at similar frequency. But CDDD=0, DDCD=9.

Let me count more precisely:
CDDD repeated (16 reps, 64 chars):
Sequence pattern: CDDD CDDD CDDD ... CDDD (16 times)
Overlapping dinucs (63 total):
Within each "CDDD" unit (chars 1-4): CD (1-2), DD (2-3), DD (3-4)
Between consecutive units (chars 4-5): DC
So per 4 chars: 1 CD + 2 DD + 1 DC; but at boundaries we have DC.
First unit contributes: CD, DD, DD (3 dinucs from positions 1-2,2-3,3-4)
Then DC (4-5), then CD (5-6), DD (6-7), DD (7-8), DC (8-9), ...
So pattern: CD DD DD DC CD DD DD DC CD DD DD DC ... 
In 64 chars = 16 reps of CDDD: pattern is (CD DD DD)(DC CD DD DD)(DC CD DD DD)... 
Total dinucs: 63. Count of DC: positions 4-5, 8-9, ..., 60-61: that's 15 DCs.
Count of CD: 16 (positions 1-2, 5-6, ..., 61-62)
Count of DD: 32 (rest).
15 DC bad + 48 good = 63.

DDCD repeated:
Sequence: DDCD DDCD ... 
Pattern of dinucs: 
pos 1-2: DD
pos 2-3: DC
pos 3-4: CD
pos 4-5: DD
pos 5-6: DD
pos 6-7: DC
pos 7-8: CD
pos 8-9: DD
Per 4 chars: DD DC CD DD (4 dinucs).
Total: 63 dinucs. Count of DC: 15-16. Same as CDDD!

So both have similar dinuc distributions but very different scores. So it's NOT about counting overlapping dinucs.

OK let me think about FRAMES. Maybe there are TWO codon frames being tested:
Frame 1: positions 1-2, 3-4, ..., 63-64 (32 codons)
Frame 2: positions 2-3, 4-5, ..., 62-63 (31 codons, with positions 1 and 64 in singletons)

Or maybe just the FIRST codon defines a frame and the rest depend on it.

For DDCD-repeated:
Frame 1 codons: DD CD DD CD DD CD ... all good!
For CDDD-repeated:
Frame 1 codons: CD DD CD DD ... all good!

Both same frame-1 codons. So frame 1 alone doesn't explain.

Frame 2 (positions 2-3, 4-5, ...): 
DDCD pattern: pos2-3=DC, pos4-5=DD, pos6-7=DC, pos8-9=DD... 
So frame 2 codons: DC DD DC DD ... = 16 DC + 16 DD. DC = bad, DD = good. 16 good + 16 bad.

CDDD pattern: pos2-3=DD, pos4-5=DC, pos6-7=DD, pos8-9=DC, ...
Frame 2 codons: DD DC DD DC ... = 16 DD + 16 DC.

Same composition again! So frame 2 also identical.

What's different then? Let me look at the ACTUAL character sequences more carefully:
CDDD: C-D-D-D-C-D-D-D-C-D-D-D-...
DDCD: D-D-C-D-D-D-C-D-D-D-C-D-...

What if there's a 4-frame? Codons of 4 chars (positions 1-4, 5-8, ...). 16 codons of 4 chars each.

CDDD: 16 codons of "CDDD" each.
DDCD: 16 codons of "DDCD" each.

Maybe "CDDD" is a forbidden 4-mer and "DDCD" is allowed!

This would mean codons are 4 chars long, not 2! Let me re-examine other data:

AAAA codon (all A): 16 codons of AAAA. Score 9.
DDDD codon: 16 codons of DDDD. Score 9.
ADAD codon: 16 codons of ADAD. Score 9.
DADA codon: 16 codons of DADA. Score 0!
AADD codon: 16 codons of AADD. Score 9.
DDAA codon: 16 codons of DDAA. Score 9.
ABAB codon: 16 of ABAB. Score 0.
BABA codon: 16 of BABA. Hmm, didn't test directly.
ACAC codon: 16 of ACAC. Score 0.
CACA codon: 16 of CACA. Hmm.

But 32 BA dinucs gave 9 (BABABA pattern). Let me revisit: BABABA... in 4-mers is BABA codon. Tested score = 9 (from "Test BA codon"). So BABA quadmer = 9, but BABA was tested as 32 BA codons.

OK so my 2-codon and 4-codon tests overlap. Let me list 4-mer "homopolymer" results:
- AAAA: 9 (from 16 AA repeats = 32 AA codons = 16 AAAA quadmers)
- DDDD: 9
- ADAD: 9
- DADA: 0
- BABA: 9 (since 32 BA codons gave 9 — sequence is BABA BABA...)
  Wait sequence BABABA... pos 1=B, pos 2=A, pos 3=B, pos 4=A. Codon 1-2=BA, 3-4=BA. So 4-mer is BABA. Score 9.
- ABAB: 0 (from 32 AB codons)
- CACA: 9 (from 32 CA codons)
- ACAC: 0
- CDCD: 9
- DCDC: 0
- BDBD: 9
- DBDB: 0
- CBCB: 9
- BCBC: 0
- AABB: ?
- AACC: ?
- AADD: 9 (tested 16 AA + 16 DD as AADD repeated)
- DDAA: 9
- AAAB: ?
- AAAC: ?
- AAAD: 9 (just tested!)
- DDDA: ?
- CDDD: 0 (just tested!)
- DDCD: 9
- CCCD: ?
- CDDA: ?

Interesting — CDDD = 0 but DDCD = 9, and DCDC = 0 but CDCD = 9.

Let me look at the pattern of 4-mers that score 0:
DADA, DCDC, DBDB, ACAC, ABAB, BCBC, CDDD
And those that score 9:
AAAA, DDDD, ADAD, BABA, CACA, CDCD, BDBD, CBCB, AADD, DDAA, AAAD, DDCD

Hmm. Test the 4-mer hypothesis vs 2-mer:
2-mer (codon) DA = bad (=0). So DADA = repeats of bad codon → 0. ✓
2-mer DC = bad. DCDC = repeats of bad → 0. ✓
But CDDD repeated has 16 CD (good) + 16 DD (good) codons. 4-mer "CDDD" is "bad" but composed of good 2-codons.

Maybe the rule is: 4-mer "codon" with specific allowed set, AND 2-codon rule applies within it?
Or maybe the parsing isn't strict codons but some grammar.

Or simpler: 4-mer codons such that the 4-mer matches a specific pattern, like "XYXY" (period 2)?

Period-2 4-mers (XYXY) include ADAD, DADA, ABAB, BABA, CDCD, DCDC, etc. Score 9 if "XY" is a good 2-codon; 0 otherwise.

Non-period-2 4-mers: AAAD, AADD, DDAA, DDCD, CDDD, etc.

AAAD = 9 (just tested).
AADD = 9.
DDAA = 9.
DDCD = 9.
CDDD = 0.

So CDDD specifically is bad. Why?

Possibility: each 4-char string is parsed as one of two: two 2-codons (positions 1-2, 3-4) OR something else.

OR: the sequence is parsed character-by-character through an FSM, and certain TRANSITIONS depend on prior states.

Let me carefully analyze the FSM hypothesis with all 2-codon data and CDDD vs DDCD.

If we have FSM with states (maybe states = letters), and ALL position-to-position transitions must be in the allowed set, then which transitions are allowed?

From good 2-codons: AA, AD, BA, BD, CA, CB, CD, DD.
A allows A, D (next).
B allows A, D.
C allows A, B, D.
D allows D.

Check ADAD chained: A→D ✓, D→A ✗ (D only allows D). So D→A transition not in allowed set. But ADAD scored 9. ✗

So overlapping FSM doesn't fit.

Different idea: maybe the sequence is parsed into NON-OVERLAPPING codons, BUT the codon boundaries are determined by content (like real biology stop codons).

Or, the sequence is parsed greedily: start from position 1, find the longest valid prefix word, then continue.

What are valid words? Maybe single letters {A, D} plus some 2-letter words.

For ADAD: parse as A, D, A, D, ... (length-1 words). Or A,DA,D? Or AD,AD,...? Multiple parses.

Let me try: rule = sequence is "good" if it can be parsed as concatenation of valid words. Words might be: {A, D, AD, AA, DD, BA, BD, CA, CB, CD, ...}.

For DADA: try parses. D|A|D|A=D,A,D,A. But A is valid? Word "A" would mean any single A is a word. Then DADA parses fine. But it scored 0.

Hmm. OK pivot.

I should accept I won't immediately find the rule. Let me collect more diagnostic data systematically. Test more 4-mer homopolymers.

## 2026-06-28 15:40 — query 78

Oops, blank query (now I know empty = 0). Moving on systematically.

## 2026-06-28 15:40 — query 82

4-mer test results (rich):
- DDDA: 0
- DDAD: 9
- DADD: 9
- ADDD: 9
- DDDD: 9
- DDCD: 9
- CDDD: 0

What about: a sequence ending in A while starting with D = bad?
DDDA ends in A, starts in D → bad ✓
DADA ends in A, starts in D → bad ✓
DCDC ends in C, starts in D → bad
DBDB ends in B, starts in D → bad
CDDD ends in D, starts in C → bad. So this hypothesis fails.

Maybe: 4-mer with rule "first character is C → second must be A, B, or D" + various rules?

CDDD: 1st=C, 2nd=D. Allowed. 2nd=D, 3rd=D. Allowed... but bad.

What if 4-mer codons must be one of a specific set? 
Maybe the rule: 4-mer is good if it equals XY*2 with XY a good 2-codon (period-2 patterns of good codons), OR equals one of a small allowed set.

From data:
Good 4-mers: AAAA, DDDD, ADAD, BABA, CACA, CDCD, BDBD, CBCB, AADD, DDAA, AAAD, DDAD, DADD, ADDD, DDCD.

Bad 4-mers: DADA, ABAB, ACAC, DCDC, DBDB, BCBC, CDDD, DDDA.

Hmm. Let me sort by content:
DDDA bad, DDAD good, DADD good, ADDD good, DDDD good.
So among "3 D's + 1 X" (X=A): positions of A matter.
ADDD: A first - good
DADD: A second - good
DDAD: A third - good
DDDA: A fourth - bad

For "3D + 1C": CDDD bad, DDCD good. Untested: DCDD, DDDC.

Test these.

## 2026-06-28 15:41 — query 84

"3D + 1C" results:
- CDDD: 0
- DCDD: 0
- DDCD: 9
- DDDC: 0

Only DDCD is good. Interesting — position 3 for C is good, others bad.

"3D + 1A":
- ADDD: 9
- DADD: 9
- DDAD: 9
- DDDA: 0

Position 4 for A is bad; others good.

Patterns:
- C at position 3 (mod 4) good; C elsewhere bad (in 3D+C context).
- A at position 4 (mod 4) bad; A elsewhere good (in 3D+A context).

Hmm. Maybe it's about even vs odd positions:
- C at ODD position bad (1, 5, 9, ...): CDDD, DCDD have C at pos 1, 3? wait DCDD has C at pos 2.
  Actually let me check 64-char sequences:
  CDDD repeated has C at positions 1, 5, 9, ..., 61 (every 4) — all ODD.
  DCDD repeated has C at positions 2, 6, 10, ..., 62 — all EVEN.
  DDCD repeated has C at positions 3, 7, 11, ..., 63 — all ODD.
  DDDC repeated has C at positions 4, 8, 12, ..., 64 — all EVEN.
  
  Good: DDCD (C at odd positions 3,7,...). 
  Bad: CDDD (C at odd 1,5,...), DCDD (C at even 2,6,...), DDDC (C at even 4,8,...).
  
  Hmm doesn't separate by even/odd cleanly. DDCD is good (odd) while CDDD bad (also odd).

Maybe positions mod 4:
- CDDD: C at pos 1 (mod 4 = 1). Bad.
- DCDD: C at pos 2 (mod 4 = 2). Bad.
- DDCD: C at pos 3 (mod 4 = 3). Good!
- DDDC: C at pos 4 (mod 4 = 0). Bad.

So C at position ≡ 3 (mod 4) is good.

For A in 3D context:
- ADDD: A at pos ≡ 1. Good.
- DADD: A at pos ≡ 2. Good.
- DDAD: A at pos ≡ 3. Good.
- DDDA: A at pos ≡ 0. Bad.

So A at position ≡ 0 (mod 4) is bad. A elsewhere (1, 2, 3 mod 4) is good.

This suggests there might be a 4-period frame structure. Let me hypothesize positions matter with period 4:
- Position class 1 (mod 4): ?
- Position class 2 (mod 4): ?
- Position class 3 (mod 4): ?
- Position class 0 (mod 4): ?

Each position class allows certain characters.

Let me test more.

From data, when sequence is all D's everywhere:
Pos mod 4 = 1: D allowed
Pos mod 4 = 2: D allowed
Pos mod 4 = 3: D allowed
Pos mod 4 = 0: D allowed

(All-D scored 9.) So D works at all positions.

For all A: scored 9. So A works at all positions too?
But DDDA scored 0 — A at position ≡ 0 (just one A) is bad.

Wait, maybe it's not just per-position. Maybe interactions.

Let me think more carefully. All-A: A's at positions 1,2,3,...,64. Each position has A. Score 9.

So A at position 64 (≡ 0 mod 4) is fine WHEN there are A's around.
But A at position 64 with D's around (DDDA repeated) is bad.

So it's about context (neighborhood). Let me look at DDDA's "boundary":
DDDADDDA... the "A" at position 4 is preceded by 3 D's, followed by 3 D's.
ADDD's "A" at position 1 is followed by 3 D's. 
DADD's "A" at position 2 is preceded by 1 D, followed by 2 D's.
DDAD's "A" at position 3 is preceded by 2 D's, followed by 1 D.

So in DDDA, the A is between D's and the NEXT A is 3 positions away.

In other 3D+1A variants, the A has different surroundings within the unit, but considered with repetition, the A occurs every 4 positions in all of them. Hmm.

Wait: in DDDA repeated, the chars are: D D D A | D D D A | D D D A...
So A positions: 4, 8, 12, 16, ... 64. Between consecutive A's: 3 D's.
In ADDD repeated: A positions: 1, 5, 9, ..., 61. Same spacing! Between A's: 3 D's.
In DADD: A positions: 2, 6, 10, ..., 62. Spacing 4.
In DDAD: A positions: 3, 7, ..., 63. Spacing 4.

All have same spacing. Why is DDDA different?

The difference: the BOUNDARIES of the 64-char sequence.

DDDA: starts with D, ends with A. Last char = A.
ADDD: starts with A, ends with D.
DADD: starts with D, ends with D.
DDAD: starts with D, ends with D.

DDDA is the only one ending in A. Maybe the LAST char matters!

Let me test: what if I take DDCD-repeated (good) but modify last char?

## 2026-06-28 15:41 — query 86



## 2026-06-28 15:42 — query 87



## 2026-06-28 15:42 — query 89

Slightly corrupted DDAD scored 9 still. Robust.

New idea: Let me look at the FRAMING of 4-mer codons by looking at where they're parsed. Maybe codons are LENGTH 4, not 2.

Test all 4-mers exhaustively (16x16 = 256 too many). Let me try a smaller class: 4-mers with only A and D (16 of them). 

Already tested: AAAA✓, DDDD✓, AAAD✓ (=9), AADD✓ (=9), DDAA✓, ADAD✓, ADDD✓, DDAD✓, DADD✓, DDDA✗(=0), DADA✗(=0).
Untested: AADA, ADAA, ADDA, DAAA, DAAD, DABD wait that's not pure AD.

Actually pure A/D 4-mers (16):
AAAA, AAAD, AADA, AADD, ADAA, ADAD, ADDA, ADDD,
DAAA, DAAD, DADA, DADD, DDAA, DDAD, DDDA, DDDD

Tested so far (16 reps as full 64-char seq):
AAAA: 9 ✓
DDDD: 9 ✓
AAAD: 9 (just)
AADD: 9
ADAD: 9
ADDD: 9
DDAD: 9
DADD: 9
DDAA: 9
DDDA: 0
DADA: 0
Untested: AADA, ADAA, ADDA, DAAA, DAAD

The two bad ones (DDDA, DADA) end in A and have "...DA" at end (looking at the 4-mer).

Let me see: which 4-mers end in DA?
DA-ending: AADA, ADDA, DADA, DDDA
But AADA, ADDA, DAAD untested.

Hypothesis: 4-mer ending in "DA" = bad (when repeated).

Let me test the untested 4-mers.

## 2026-06-28 15:43 — query 94

## All 16 AD-only 4-mer results (16 reps):
- AAAA: 9
- AAAD: 9
- AADA: 0 ← ends in DA
- AADD: 9
- ADAA: 9
- ADAD: 9
- ADDA: 0 ← ends in DA  
- ADDD: 9
- DAAA: 9
- DAAD: 9
- DADA: 0 ← ends in DA
- DADD: 9
- DDAA: 9
- DDAD: 9
- DDDA: 0 ← ends in DA
- DDDD: 9

Hypothesis CONFIRMED: 4-mer ending in "DA" → 0 when repeated.
All other AD-only 4-mers = 9.

So "DA" as the last 2 chars of a 4-mer is problematic. Why?

In 16-rep sequence of 4-mer ending in "DA": positions of "DA" dinuc are at positions 3-4, 7-8, ..., 63-64.
Non-overlap codons (positions 1-2, 3-4, ..., 63-64) would have DA at positions 3-4, 7-8, ..., 63-64 (16 DA codons).
The other 16 codons (positions 1-2, 5-6, ...) are some good codon (AA, AD, DA, DD... wait the first 2 chars vary).

For DDDA repeated: positions 1-2 = DD, 3-4 = DA. So 16 DD + 16 DA codons. 16 good + 16 bad. Score 0.
But earlier I tested 16 AD + 16 DA = 3. So 16 good + 16 bad in different proportions give different scores.

Maybe more precisely: the rule is about the SPECIFIC codon-pair pattern. Repeated (good)(bad) might be especially bad.

Hmm but 16 AD + 16 DA in alternating order gave 3, and 16 DD + 16 DA in alternating order gives 0. Different!

Let me test more carefully — maybe codon SEQUENCE matters as a higher-order chain.

Actually wait! Look at this: DDDA repeated, viewed as 32 codons of 2:
DD, DA, DD, DA, DD, DA, ... 
So this is 16 alternations of DD and DA codons.

But ALTERNATING DD-DA = repeating "DDDA" 4-mer = 16 reps.

Score 0.

Compare to 16 AD + 16 DA where I had: first 32 chars AD codons, last 32 DA codons. Score 3.
Or alternating ADAD + DADA: but that's 16 AD codons then 16 DA codons in block. Same.

The alternation (AD, DA, AD, DA): well "ADDA" 4-mer = (AD)(DA) repeated. I tested ADDA repeated = 0.

Now (DA, AD): DADA pattern. wait that's not right. (DA)(AD) is "DAAD". Tested DAAD repeated = 9!

So alternating DA-AD (as codons) makes good 4-mer "DAAD" → 9.
But alternating AD-DA (as codons) = "ADDA" → 0.

So the codon ORDER matters even when the same codons are present!

This strongly suggests CODON PAIRS (like di-codon = tetra-nt) are the relevant unit. And the "codon" might really be 4 characters.

Let me revisit: maybe the natural unit is 4 characters ("words"). 256 possible 4-mers, some valid, some not.

The score = function of how many of the 16 non-overlapping 4-mers are "valid"?

Pure 4-mer homopolymer (16 reps of one 4-mer): score 9 if valid, 0 if not.

For mixed cases let me look at 16 AD + 16 DA codons (sequence: ADADAD...ADDADADA...DA, 32 chars each).
As 4-mers: first 16 4-mers (chars 1-64 broken into 16 4-mers of 4 chars each):
chars 1-4: ADAD ✓ valid 4-mer
chars 5-8: ADAD ✓
...
chars 29-32: ADAD ✓
chars 33-36: DADA ✗ invalid
chars 37-40: DADA ✗
...
chars 61-64: DADA ✗

So 8 valid 4-mers + 8 invalid. Score 3.

For 24 AD + 8 DA codons: first 48 chars = ADAD*12 = 12 valid 4-mers, last 16 chars = DADA*4 = 4 invalid 4-mers. Score 6.

For 8 AD + 24 DA codons: 4 valid + 12 invalid 4-mers. Score 1.

Hmm: 16 valid 4-mers → 9; 12 → 6; 8 → 3; 4 → 1; 0 → 0.
Rate: 9/16, 6/12, 3/8, 1/4, 0/0. 
Ratios: 0.56, 0.5, 0.375, 0.25 — not constant.
Diffs: 16→12: -3; 12→8: -3; 8→4: -2; 4→0: -1.

Looks like score = floor(valid_4mer_count * something).

Actually let's look more carefully:
valid=16: 9
valid=12: 6
valid=8: 3
valid=4: 1
valid=0: 0

Differences in valid: 4, 4, 4, 4.
Differences in score: 3, 3, 2, 1.

Hmm maybe score = floor((9*v - X)/Y)? At v=16, 9=9; v=12, 6.75→6; v=8, 4.5→? obs 3. So floor(9v/16) doesn't fit.

Maybe score = sum of contributions where 4-mer contributes based on position?

What about: score = #valid_4mers - #invalid_4mers, capped at some bound?
v=16, i=0: 16. Score 9.
v=12, i=4: 8. Score 6.
v=8, i=8: 0. Score 3.
v=4, i=12: -8. Score 1.
v=0, i=16: -16. Score 0.

Not linear.

Maybe it's like log? Or floor(valid/2)?
v=16: 8 (obs 9). No.

Try: 9 - floor(invalid/k):
i=0: 9.
i=4: 6 → floor(4/k) = 3 → k=1.33.
i=8: 3 → floor(8/k) = 6.
i=12: 1 → floor(12/k) = 8.
i=16: 0 → 9.
So penalty = 0, 3, 6, 8, 9. Diffs: 3, 3, 2, 1. Looks like cumulative diminishing returns.

Could be cumulative: each additional invalid 4-mer costs less. 1st: 3, 2nd: 0, 3rd: 0, 4th: 0... no doesn't work either.

Wait the data 0,3,6,8,9 for invalid count 0,4,8,12,16 — let me think of it as: score function with more 4-mers contributing.

Actually maybe I should test mixed VALID 4-mers (mix of two different valid 4-mers).

## 2026-06-28 15:43 — query 96

Mix of 16 valid 4-mers (each one separately scores 9) gives only 8. So 4-mer-by-4-mer rule doesn't fully account for it.

OK let me change approach. Rather than figuring out the exact rule, let me:
1. Verify the 4-mer hypothesis: each valid 4-mer contributes, invalid don't.
2. Find a fingerprint that maximizes score.

I already know lots of single-4-mer homopolymers give 9. So if I want max 9, I can use any of them.

Let me try: maybe sequences with HIGH SCORE are those that locally match some "good" pattern almost everywhere, and the EXACT score depends on the BEST local match window.

Going back to my data:
Random good codon mix: 31 good codons + 1 bad codon = score 8 (not 9).
Pure (AA)^32 + 1 DA = score 9.
So "purity" of codon usage matters?

Or, perhaps: the score = 9 minus (number of distinct disruptions)?

Actually let me just look at the data I have and try to maximize. The max is 9 — I've found that. But maybe the actual max is higher? Let me try some quirky sequences.

Wait, in my notebook I never confirmed the cap is 9. Many sequences score 9 — maybe higher is possible with the right combination. Let me try unusual patterns.

## 2026-06-28 15:43 — query 98

DCBA repeated (16 times) = 9. So DCBA is a valid 4-mer!

Let me think about what's special about DCBA. It's the sequence reversed (D=4, C=3, B=2, A=1; decreasing).

Earlier ABCA was tested as ABC-repeated... wait that's 3-cycle. Let me check ABCD.

## 2026-06-28 15:43 — query 101

ABDC = 0. ABCD = 9. ACBD = 9. DCBA = 9.

Let me test more permutations of ABCD (4! = 24 total):
Already known:
ABCD: 9
ABDC: 0
ACBD: 9
DCBA: 9
And from my earlier 2-codon tests, some implicit info but those were XYXY patterns.

Need more permutation tests. Theory: maybe a 4-mer X1X2X3X4 is valid iff (X1,X2) is good codon AND (X3,X4) is good codon AND (X2,X3) is good codon? — all 3 dinucleotides good?

For ABCD: dinucs AB (bad!), BC (bad), CD (good). Has 2 bad dinucs, yet 4-mer is good. ✗

Hmm. OK let me just test more 4-mers and look for patterns.

## 2026-06-28 15:44 — query 107

## Permutation 4-mer (containing each of A,B,C,D once) results:
ABCD: 9
ABDC: 0
ACBD: 9
ACDB: ?
ADBC: ?
ADCB: ?
BACD: 9
BADC: 0
BCAD: 9
BCDA: ?
BDAC: ?
BDCA: ?
CABD: 9
CADB: ?
CBAD: ?
CBDA: ?
CDAB: 0
CDBA: ?
DABC: 9
DACB: ?
DBAC: ?
DBCA: ?
DCAB: ?
DCBA: 9

So far good: ABCD, ACBD, BACD, BCAD, CABD, DABC, DCBA (7 of tested 11)
Bad: ABDC, BADC, CDAB (3 of tested 11)

Notice: ABDC = 0. Reverse of CDAB = also 0. 
BADC = 0. Reverse of CDAB = CDAB? wait reverse of BADC is CDAB. Yes! And both are 0.

ABCD = 9. Reverse DCBA = 9. ✓
ACBD = 9. Reverse DBCA = ?
BACD = 9. Reverse DCAB = ?
BCAD = 9. Reverse DACB = ?
CABD = 9. Reverse DBAC = ?
DABC = 9. Reverse CBAD = ?

Hmm. Let me see what distinguishes the bad ones:
ABDC: A→B, B→D, D→C. Bad dinucs: AB(bad), BD(good), DC(bad).
BADC: B→A, A→D, D→C. Dinucs: BA(good), AD(good), DC(bad).
CDAB: C→D, D→A, A→B. Dinucs: CD(good), DA(bad), AB(bad).

Good ones:
ABCD: AB(bad), BC(bad), CD(good). 2 bad dinucs but valid 4-mer.
ACBD: AC(bad), CB(good), BD(good). 1 bad dinuc.
BACD: BA(good), AC(bad), CD(good). 1 bad.
CABD: CA(good), AB(bad), BD(good). 1 bad.
DABC: DA(bad), AB(bad), BC(bad). 3 bad dinucs! And it's valid!

So dinuc counts don't predict. DABC has 3 bad dinucs but is valid.

Hmm DABC=9 surprises. Sequence DABCDABC... 

Let me look at non-overlapping codons of these repeated 4-mers:
ABCD repeated as 32 codons (length 2): AB CD AB CD AB CD... = 16 AB + 16 CD. AB=bad, CD=good. 16 good + 16 bad. Yet 4-mer score = 9.
But 32-codon test of AB alone = 0; of CD alone = 9. And 16 AB + 16 CD as alternating = ?

Actually let me check: AABBCC pattern... no let me directly test what gives 16 AB + 16 CD: that's just ABCDABCD... so 9.

But if I do alternating differently: ABABABCDCDCD or interleaved AB AB CD CD AB AB CD CD?

The 4-mer view: ABAB|ABAB|CDCD|CDCD... 4 4-mers, 2 are ABAB (=0), 2 are CDCD (=9). So 8 4-mers each (16 chars/4=4 ... wait 64/4=16 4-mers). So if I do 8 ABAB + 8 CDCD = 8 bad + 8 good 4-mers.

Versus ABCDABCD repeated: each 4-mer is ABCD (=9). 16 good 4-mers.

Same character composition (16 A, 16 B, 16 C, 16 D)! Same set of non-overlap 2-codons (16 AB + 16 CD)! But different 4-mer parsings.

So FRAMING matters. The 4-mer frame at positions (1-4, 5-8, ...) determines validity.

OK let me test ABABABAB...CDCDCDCD... (32 ABAB + 32 CDCD as blocks).

## 2026-06-28 15:44 — query 108

8 ABAB (bad 4-mers) + 8 CDCD (good 4-mers) = 3.

Matches the pattern! 8 good 4-mers + 8 bad 4-mers = 3. Same as 8 AD codon-pairs + 8 DA codon-pairs giving 3.

So the rule probably is: count valid 4-mers (non-overlapping, frame from position 1).

Let me solidify:
v=16 valid: 9
v=12: 6
v=8: 3
v=4: 1  
v=0: 0

But mixed valid 4-mers gave 8 (16 different valid 4-mers, score 8) — exception!

Maybe the rule isn't purely 4-mer based. Let me cross-check.

For v=16 valid 4-mers all distinct gives 8 → so it's NOT just count.

Maybe there's a 4-mer PAIR rule (8-mer codons!).

Let me re-examine the mixed-4-mers seq I built: 
"AAAAAAADAADDADDDDDDDDDADDDAADAAAAAAAAAAADAADDADDDDDDDDDADDDAADAA"
4-mers (positions 1-4, 5-8, ..., 61-64):
AAAA, AAAD, AADD, ADDD, DDDD, DDAD, DDAA, DAAA, AAAA, AAAD, AADD, ADDD, DDDD, DDAD, DDAA, DAAA

Hmm wait let me recount the string: 
"AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA"

So 16 4-mers, 8 distinct ones each repeated twice. All 8 should be valid (per my earlier table).

8-mer (positions 1-8, 9-16, ..., 57-64): 
AAAAAAAD, AADDADDD, DDDDDDAD, DDAADAAA, AAAAAAAD, AADDADDD, DDDDDDAD, DDAADAAA

8 8-mers. Maybe some are invalid?

Hard to tell. Let me try larger codon hypothesis: 8-mer codons.

Or maybe it's a Markov model: each char depends on prev char, AND there's an initial probability.

Actually given the complexity, maybe just keep building intuition. Let me try maximize and see if 9 is the cap.

## 2026-06-28 15:44 — query 109

Max so far is 9. Let me focus on understanding the rule rather than maximizing.

Let me hypothesize 4-mer codons more carefully. Test all-A 4-mer block transitions.

Hypothesis: certain transitions between 4-mer codons matter.

The mixed-distinct-valid 4-mer gave 8. The transitions in that seq:
AAAA→AAAD, AAAD→AADD, AADD→ADDD, ADDD→DDDD, DDDD→DDAD, DDAD→DDAA, DDAA→DAAA, DAAA→AAAA (next cycle).

The DAAA→AAAA transition: last char D... wait DAAA's last char is A. So junction = AA. OK.
ADDD→DDDD: junction D-D = DD.
DDDD→DDAD: D-D = DD.
DDAD→DDAA: D-D = DD.
DDAA→DAAA: A-D = AD.
DAAA→AAAA: A-A = AA.
AAAA→AAAD: A-A.

So inter-4mer junctions are all OK (AA, DD, AD).

Each individual 4-mer is valid. So why score 8 and not 9?

Maybe the score = sum of contributions per 4-mer, with specific contributions varying.

Let me test simpler 16-rep mix: 8 reps of AAAA + 8 reps of DDDD (block).
That sequence is AAAA*8 then DDDD*8 = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA + DDDD*8 = 32 A's then 32 D's. Already tested = 9.

What about AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA DDDD DDDD DDDD DDDD DDDD DDDD DDDD DDDD = same thing = 9. ✓

Try 4 reps each of 4 distinct 4-mers: AAAA, DDDD, ADAD, DADA (DADA invalid though). Use valid ones.

## 2026-06-28 15:44 — query 111

Good, 9 in both orders. So mixing 4 valid 4-mers in blocks still gives 9.

Mixing 8 distinct valid 4-mers (1 of each, cycling 2x) gave 8. 

Maybe specific transitions are bad. Let me test pairs of adjacent 4-mers more.

## 2026-06-28 15:45 — query 115

Confirmed: AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA (2x) = 8.

Let me look at each 4-mer junction:
4-mers: AAAA|AAAD|AADD|ADDD|DDDD|DDAD|DDAA|DAAA|AAAA|AAAD|AADD|ADDD|DDDD|DDAD|DDAA|DAAA
Junctions (chars 4-5, 8-9, ...): A-A=AA, D-A=DA, D-A=DA, D-D=DD, D-D=DD, D-D=DD, A-D=AD, A-A=AA, A-A=AA, D-A=DA, D-A=DA, D-D=DD, D-D=DD, D-D=DD, A-D=AD

Junctions in order: AA, DA, DA, DD, DD, DD, AD, AA, AA, DA, DA, DD, DD, DD, AD
3 of these are "DA" — bad. Could THIS be why score is 8?

Compare AAAADDDD repeated: junctions are A-D=AD (at 4-5), D-A=DA (at 8-9), A-D=AD, D-A=DA, ...
So lots of DA junctions! But score = 9.

Hmm so DA junctions per se aren't bad.

What's specific about the 8 → 9 problem? Let me look at 8-mer non-overlapping codons:
seq = AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA
8-mers (positions 1-8, 9-16, ...): 8 8-mers.
1-8: AAAA AAAD
9-16: AADD ADDD
17-24: DDDD DDAD
25-32: DDAA DAAA
33-40: AAAA AAAD
41-48: AADD ADDD
49-56: DDDD DDAD
57-64: DDAA DAAA

So 4 distinct 8-mers, each appearing twice: AAAAAAAD, AADDADDD, DDDDDDAD, DDAADAAA.

If 8-mers matter and some are invalid, this could explain. Maybe DDAADAAA is invalid?

Test 16 reps of DDAADAAA = wait, 64/8 = 8 reps.

## 2026-06-28 15:45 — query 117

Both 8-mers individually = 9. So at 8-mer level both valid.

OK I'm going down rabbit holes. Let me step back and think.

Key empirical observations:
- 4-mer rule explains a LOT but not everything.
- Mix of all 8 distinct valid 4-mers (1 each, 2x) = 8. Maybe these specific 4-mers have a subtler structure.
- 4-mer ending in DA (when repeated) = 0. AADA, ADDA, DADA, DDDA — these all FAIL.
- 4-mer with C in wrong position FAILS: CDDD, DCDD, DDDC — only DDCD works.

There's clearly some richer rule. Let me try yet another framing: maybe sequence is parsed in a TBD way and the score = LENGTH of successful parse / something.

Actually, the data is consistent with the simple "non-overlap codon-by-codon" rule for many cases, BUT some 4-mer aspects show otherwise (CDDD, ABDC, etc.).

Hmm wait. ABDC repeated:
2-codons: AB DC AB DC = 16 AB + 16 DC. Both BAD. So 32 bad codons → score 0. ✓ Consistent with 2-codon rule!

CDDD repeated:
2-codons: CD DD CD DD = 16 CD + 16 DD. Both GOOD. So 32 good codons → expect 9. But got 0.
So 2-codon rule predicts 9 but actual is 0. Contradiction.

That's the puzzle: CDDD-repeated has all good 2-codons but scores 0.

What if the parsing isn't fixed at positions 1-2, 3-4? What if it's CHOSEN to be either offset, and BOTH frames must be evaluated?

CDDD-repeated, frame 1 (pos 1-2, 3-4, ...): CD DD CD DD... 16+16 good.
CDDD-repeated, frame 2 (pos 2-3, 4-5, ...): DD DC DD DC... 16 DD good + 16 DC bad.

If we require BOTH frames to be all-good for max score, then frame 2 fails (16 DC bad codons).

For DDCD-repeated:
Frame 1: DD CD DD CD = 16+16 good.
Frame 2: DC DD DC DD = 16 DC bad + 16 DD good.

Same frame-2 composition! Both should be equally bad if frame 2 matters. But DDCD = 9 and CDDD = 0.

So FRAMES alone don't distinguish.

What if there's a LEADING/TRAILING char rule?
DDCD-repeated starts with D, ends with D.
CDDD-repeated starts with C, ends with D.

What about CDCD repeated: starts with C, ends with D. Score 9.
DCDC repeated: starts with D, ends with C. Score 0.

DCDC ends with C. CDDD starts with C but ends with D. So end-char isn't universally bad.

Let me look at first 2 chars:
CDDD: CD (start). 
DCDC: DC (start).
CDCD: CD (start). Score 9.
DDCD: DD (start). Score 9.

CDDD vs CDCD: both start CD. CDCD=9, CDDD=0. So start isn't it.

Maybe it's about WHICH POSITIONS within the 4-mer have C:
CDDD: C at position 1, D's at 2,3,4.
DCDD: C at position 2.
DDCD: C at position 3.
DDDC: C at position 4.
Only DDCD (C at pos 3) is good.

For 1A+3D 4-mers:
ADDD: A at 1. Good.
DADD: A at 2. Good.
DDAD: A at 3. Good.
DDDA: A at 4. BAD.

So for A, only position 4 bad; for C, only position 3 good.

Interesting positional rule. Now for 4-mers with mix of letters: maybe each position in 4-mer prefers different chars?
Position 1 prefers: A, D (and B, C also OK per data)
Position 2 prefers: ?
Position 3 prefers: ?
Position 4 prefers: ?

From 4-mer data:
AAAA good — all positions A OK
DDDD good — all positions D OK

DDDA bad: position 4 = A, but elsewhere all D. So pos 4 A is bad when neighbors are D's? Or pos 4 A is bad generally?

But AAAA, ADDA, AAAA all have A at pos 4 in some contexts. Wait AAAA has A at all positions. AAAA scored 9.

So pos 4 = A is OK when other positions are A's.

It seems contextual.

NEW HYPOTHESIS: Maybe it's about 2-codons and the codons must be in a specific GRAMMAR.

Look at "CDDD repeated": codons CD DD CD DD CD DD...
Look at "DDCD repeated": codons DD CD DD CD DD CD...

Maybe codon sequence must START with a specific type or follow rules.

If first codon must be from set S1 and subsequent must follow grammar...
CDDD starts with CD codon — bad start?
DDCD starts with DD codon — good start?

Test: pure DD codons starting with CD?
CD followed by all DD: CD DD DD DD ... × 16 = CDDDDDDDDDDD... 
But that's just sequence "CD" + 62 D's.

## 2026-06-28 15:45 — query 120

- 1 CD + 31 DD codons: 8
- 2 CD + 30 DD codons: 9
- 3 CD + 29 DD codons: 9

Hmm so a single CD codon followed by DD codons reduces from 9 to 8. Two CD restores to 9. Interesting.

Wait actually I should look at this in terms of sequence:
"CDDD..." (CD then all D's): the sequence "CDDD..." starts with CDDD. As 4-mer parsing: 4-mer 1 = CDDD (BAD!), 4-mer 2-16 = DDDD (good). So 15 good + 1 bad = score 8.

For CDCDDDDD...: 4-mers: CDCD (good), DDDD (good)*15. All 16 good. Score 9.
For CDCDCDDD...: 4-mers: CDCD, CDDD (bad!), DDDD*14. 15 good + 1 bad. Should be 8... but observed 9.

Hmm contradiction!

Let me recount: "CDCDCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
Length 64. 4-mers (positions 1-4, 5-8, ...):
1-4: CDCD ✓
5-8: CDDD ✗ (or 5-8 is "CDDD"? let me reparse)
Actually the string is C-D-C-D-C-D-D-D-D-D-D-D-D-D-D-D-... So:
1-4: CDCD ✓
5-8: CDDD ✗
9-12: DDDD ✓
...
13-64: all DDDD ✓

If CDDD is bad as 4-mer, this should score lower. But got 9.

So 4-mer hypothesis is wrong!

Hmm. Let me re-examine. The CDDD-repeated sequence:
"CDDDCDDDCDDD..." 4-mers (position 1-4, 5-8, ...): CDDD, CDDD, CDDD, ..., CDDD. All same. Score 0.

But here "CDCDCDDD..." has 4-mer 2 = CDDD also. Wait if even 1 CDDD breaks score to 0, then both should be 0. But "CDCDCDDD..." = 9.

So CDDD as ONE 4-mer doesn't break score. The CDDD-repeated breaks because of LARGE-SCALE periodicity?

Hmm. Maybe it's not the 4-mer but the LARGER-scale repeat structure.

Let me test: 16 CDDD as 4-mer vs other arrangements.

Test: a single CDDD at the beginning of an all-D seq: "CDDDDDDDDDDDD...DDD" = 1 CDDD 4-mer + 15 DDDD 4-mers. Already tested: score 8.

So single CDDD → 8.
Two CDDD at start? Test now.

## 2026-06-28 15:46 — query 124

CDDD count → score:
0: 9 (all D)
1: 8
2: 7
3: 6
4: 6
8: 3
16 (all CDDD): 0

Adding CDDD's decreases score by ~1 per addition, with some plateaus.

Actually looking at it: each CDDD removed 4 D's. Number of D's:
0 CDDD: 64 D
1: 60 D
2: 56 D
3: 52 D
4: 48 D
8: 32 D
16: 0 D

Number of C's = (#CDDD).

Maybe rule is: each C in the sequence reduces score? Let's see scores per #C:
#C=0: 9
#C=1: 8
#C=2: 7
#C=3: 6
#C=4: 6
#C=8: 3
#C=16: 0

Pretty linear (roughly score = 9 - #C/2 capped at 0?). 9-0=9, 9-0.5=8.5→8, 9-1=8?→7 actual.
Or 9 - floor(#C * 9 / 16): 9-0=9, 9-floor(9/16)=9 (not 8). Hmm.

Maybe: 9 - C-count for small C, then plateau. Let me also test by varying C position.

Actually wait: my CDDD-repeated test has 16 C's. Lots of other 16-C sequences should also score 0 if it's just C-count. But DDCD-repeated has 16 C's too and scored 9! So C-count alone doesn't determine.

Hmm. Both CDDD and DDCD have 16 C's. CDDD = 0, DDCD = 9.

The DIFFERENCE between CDDD and DDCD repeated: position of C within each 4-block.
- CDDD: C at positions 1, 5, 9, ..., 61 (positions ≡ 1 mod 4)
- DDCD: C at positions 3, 7, ..., 63 (positions ≡ 3 mod 4)

But also looking at the LOCAL dinuc neighborhoods:
- CDDD: each C is preceded by D (or seq start) and followed by D. Dinucs around each C: DC (preceding) and CD (following).
- DDCD: each C is preceded by D and followed by D. Same: DC and CD.

Same local dinucs! Yet different scores.

WAIT. Let me re-examine the spacing of C's:
CDDD repeated: C at positions 1, 5, 9,... — every 4 positions.
DDCD repeated: C at positions 3, 7, 11, ... — every 4 positions.

Same spacing. Same dinuc neighborhood. The only difference is the OFFSET from position 1.

So maybe positions ≡ 1 (mod something) are special.

Period might be 2: positions odd vs even.
C at odd positions (1, 3, 5, ...): CDDD has C at 1, 5, ... (odd). DDCD has C at 3, 7, ... (also odd).
Both have C only at odd positions. Same!

Wait then why different?

OH! Let me re-examine the OFFSET more carefully.
CDDD repeated period 4: positions 1, 5, 9, 13, ... are C. These are positions ≡ 1 (mod 4).
DDCD repeated period 4: positions 3, 7, 11, ... are C. These are ≡ 3 (mod 4).

Both odd, but different mod-4 classes.

So mod-4 (4-position frame) matters!

Maybe each position class (1, 2, 3, 4 mod 4) has different rules for which chars are allowed.

Let me determine these rules from data:
- All-D scored 9: D allowed at all 4 position classes.
- All-A scored 9: A allowed at all 4 position classes.
- CDDD repeated: D at classes 2,3,4; C at class 1. Score 0. So C at class 1 → ZERO score.
- DCDD repeated: D at classes 1,3,4; C at class 2. Score 0. So C at class 2 → ZERO.
- DDCD repeated: D at classes 1,2,4; C at class 3. Score 9. So C at class 3 → ALLOWED.
- DDDC repeated: D at classes 1,2,3; C at class 4. Score 0. So C at class 4 → ZERO.

So C is allowed ONLY at class 3 (mod 4 = 3).

- ADDD repeated: A at class 1. Score 9. A at 1 → allowed.
- DADD: A at class 2. Score 9. A at 2 → allowed.
- DDAD: A at class 3. Score 9. A at 3 → allowed.
- DDDA: A at class 4. Score 0. A at 4 → NOT allowed.

So A allowed at classes 1, 2, 3; NOT 4.

What about B? Earlier we saw BABA = 9. BABA has B at classes 1, 3 (BABABA... positions 1,3,5,7,... = B at class 1 and 3). And A at classes 2, 4. So B at 1,3 OK; A at 2 OK; A at 4 OK?!

Wait that contradicts DDDA = 0 (A at 4 → not allowed).

Hmm. BABA repeated: positions 1-4 = B,A,B,A. Class 1 = B, class 2 = A, class 3 = B, class 4 = A. So A is at class 4!

But BABA scored 9 while DDDA scored 0.

So it's NOT simply per-class allowed-chars.

Maybe joint context: A at class 4 IS bad in DDDA but OK in BABA. The CONTEXT (what's at the other positions) matters.

For BABA: A at class 4 follows B at class 3 (preceding char). Dinuc BA = good codon.
For DDDA: A at class 4 follows D at class 3. Dinuc DA = bad codon.

So maybe the rule is purely codon-based AND something else.

Hmm but CDDD-repeated codons are CD DD CD DD... all good 2-codons. So 2-codon alone isn't it.

UGGGH ok. Let me look very precisely at the position arrangement.

CDDD-repeated string: "CDDDCDDDCDDD..."
Position 1: C
Position 2: D
Position 3: D
Position 4: D
Position 5: C
Position 6: D
...

Dinucleotides (consecutive pairs, overlapping):
1-2: CD (good 2-codon)
2-3: DD (good)
3-4: DD
4-5: DC (bad!)
5-6: CD
6-7: DD
7-8: DD
8-9: DC (bad)
...

There are MANY DC dinucs (every 4 positions). 

DDCD-repeated: "DDCDDDCD..."
1-2: DD
2-3: DC (bad!)
3-4: CD
4-5: DD
5-6: DD
6-7: DC (bad)
7-8: CD
...

Also has DC dinucs every 4 positions, same count.

But CDDD = 0 and DDCD = 9.

The TIMING/PHASE of DC dinucs:
CDDD: DC at positions 4-5, 8-9, 12-13, ... — always between 4-mer boundaries (positions ≡ 0 mod 4 and ≡ 1 mod 4).
DDCD: DC at positions 2-3, 6-7, ... — within 4-mers (positions ≡ 2 mod 4 and ≡ 3 mod 4).

What if dinucs at certain positions are penalized differently?
- A "bad" dinuc at position (2k-1, 2k) (codon-internal): contributes "bad codon" penalty.
- A "bad" dinuc at position (2k, 2k+1) (codon-junction): contributes "junction penalty".

For CDDD repeated, DC bad dinucs at positions (4,5), (8,9), ... — these are at codon JUNCTIONS (4 = even = end of codon 2; 5 = start of codon 3).

For DDCD repeated, DC bad dinucs at positions (2,3), (6,7), ... — also at codon JUNCTIONS.

Same! Both junctions.

OK my classification was wrong. Let me redo:
Frame 1 codons positions: (1,2), (3,4), (5,6), ... — codons at odd-even pairs.
Frame 2 junctions positions: (2,3), (4,5), (6,7), ... — junctions at even-odd pairs.

CDDD repeated:
Frame 1 codons: CD, DD, CD, DD, ... — all good.
Frame 2 junctions (overlapping dinucs at even-odd boundaries): DD (2-3), DC (4-5), DD (6-7), DC (8-9), ... → 8 DDs + 8 DCs at junctions. DC bad at junctions.

DDCD repeated:
Frame 1 codons: DD, CD, DD, CD, ... — all good.
Frame 2 junctions: DC (2-3), DD (4-5), DC (6-7), DD (8-9), ... → 8 DC + 8 DD. Same as CDDD junctions!

Hmm same composition again. Still no distinguisher.

WAIT — maybe frame 1 codons differ:
CDDD: codon 1 = CD, codon 2 = DD, codon 3 = CD, codon 4 = DD, ... = CD, DD alternating.
DDCD: codon 1 = DD, codon 2 = CD, codon 3 = DD, codon 4 = CD, ... = DD, CD alternating.

CODON SEQUENCE:
CDDD: CD, DD, CD, DD, CD, DD, ... (starts with CD)
DDCD: DD, CD, DD, CD, DD, CD, ... (starts with DD)

The codon-level pattern. If codons are themselves chained in some grammar where transitions matter:
CDDD: CD→DD, DD→CD, CD→DD, DD→CD, ...
DDCD: DD→CD, CD→DD, DD→CD, CD→DD, ...

Both have same transitions (CD→DD and DD→CD alternating). 

Hmm, only difference is starting codon. Maybe the GRAMMAR requires starting with DD (or not starting with CD)?

Or maybe codon at position 1-2 must be from a restricted set.

## 2026-06-28 15:46 — query 129

First-codon test (rest DD):
- AA: 9
- AD: 9
- DA (bad codon): 9 (!!)
- CD: 8
- BD: 8
- CB: 8

Interesting! DA as first codon → 9. But CD as first codon → 8.

What's the difference? In "DADDDD...", chars 1,2,3 = D,A,D. Dinuc at 1-2 = DA, 2-3 = AD (good), 3-4 = DD (good). The DA is at position 1-2.

In "CDDDDD...", chars 1,2,3 = C,D,D. Dinuc 1-2 = CD (good), 2-3 = DD (good), 3-4 = DD. So good dinucs throughout.

Yet CD-first scored 8 and DA-first scored 9. Strange.

Maybe it's about character at position 1?
- DADDDD: pos 1 = D. Score 9.
- ADDDDD: pos 1 = A. Score 9.
- CDDDD: pos 1 = C. Score 8.
- BDDDDD: pos 1 = B. Score 8.

So if position 1 is B or C → minor penalty (8 instead of 9).

Test single B or C in middle of all-D vs at start.

## 2026-06-28 15:47 — query 133

Single B in sea of D, by position:
- pos 1: 8
- pos 2: 8
- pos 3: 9
- pos 4: 8
- pos 64: 8

Only pos 3 gives 9; others give 8.

So position 3 is special for B? Actually B at odd positions: pos 1 = 8, pos 3 = 9. So odd ≠ uniform.

Let me test B at pos 5, 7, ...

## 2026-06-28 15:47 — query 136

B at odd position (≥3): 9. B at pos 1: 8. B at even or 64: 8.

So B is OK at odd positions 3, 5, 7, 9, ... but NOT at:
- Position 1 (leading)
- Even positions
- Position 64 (trailing)

Let me check position 63 (odd, second-to-last).

## 2026-06-28 15:47 — query 137

B at pos 63 (odd, not 1): 9. ✓

So B at odd position (not pos 1) is fine when surrounded by D's. B at even or pos 1 → 8.

Let me think: a B at odd position p, surrounded by D's. Neighbors are D at p-1 and D at p+1 (if exist). Dinucs: DB (bad) and BD (good).

If at pos 1: only neighbor is at p+1 = D. Dinuc BD (good). But score 8.
If at odd pos ≥3: DB then BD. Score 9.
If at even pos: DB then BD. Score 8.

Hmm DB always bad dinuc; BD always good. Same composition for any internal position.

Maybe the rule is about CODON FRAME (non-overlap, positions 1-2, 3-4, ...):
- B at odd pos p (with D's): forms codon (B, D) = BD (good codon).
- B at even pos p: forms codon (D, B) = DB (bad codon).
- B at pos 1 = odd: forms codon (B, D) at pos 1-2 = BD (good). But score 8?!

Wait pos 1 = odd → forms codon 1-2 with content B, D = BD (good). So codon should be good. Why score 8?

Unless... the FIRST codon has extra rule.

Let me test: A at pos 1 with B's around? Or something else.

Actually let me consider: maybe sequence has 5' "promoter" rule — special rule for first/last codon.

Or: maybe overlapping codons + the codon (X, Y) at pos (0, 1) — but there's no pos 0. So first codon (1,2) might be evaluated differently.

OR: the "next codon" rule. Maybe codon (Bpos1, Dpos2) is BD (good), and then codon (Dpos3, Dpos4) is DD (good). But the EXISTENCE of "fake position 0" that must satisfy something with pos 1...

Hmm complicated. Let me try B at pos 1 with various pos 2:

## 2026-06-28 15:47 — query 139

B at pos 1, with all A's after: 9!
B at pos 1, with all D's after: 8.

So B at pos 1 is OK if followed by A (BA codon), but slightly penalized if followed by D (BD codon)?

Hmm but BABA...BA scored 9. And BDBD...BD scored 9.
B at pos 1, then A,D,D,D,...: codon 1-2 = BA (good). Then DDDD... rest. Score 9.
B at pos 1, then D,D,D,...: codon 1-2 = BD (good). Score 8.

So even with both good codons, BD-first is worse than BA-first?

But BDBDBDBD repeated (all BD codons) = 9. So BD at pos 1-2 isn't penalized when continued with more BD.

Maybe the issue isn't position 1 per se, but: a B at odd position is "OK" if the position is part of a "BD" or "BA" codon AND the rest of the sequence has some property.

OK I'm getting lost. Let me try a totally different approach: maybe the scoring is based on counting matches to a specific PATTERN/template that I haven't identified.

Let me try: which characters can appear at each position to give 9?
Pos 1: A=9, D=9, B=? (with DD rest: 8; with AA rest: 9), C=?
Need more systematic single-position tests.

Actually: let me just try the maximizing approach and accept I have a partial understanding. Focus on patterns that reliably give 9 and see what they share.

ACTUALLY — wait. Let me try a SIMPLER theory: maybe the score is computed by some local window analysis that I'm missing. 

Let me look at all my "score 9" sequences and find a common feature.

All A: 64 A's
All D: 64 D's
ADAD repeated
DAAA... (1 D + 63 A)
BABA repeated
CACA repeated
BCAD repeated (each 4 chars)
ABCD repeated
DCBA repeated
DDCD repeated
DAAD repeated
DABC repeated
...

Hmm wide variety.

I have 360+ experiments left. Let me try to push deeper with a systematic test of single-letter substitutions in all-D.

## 2026-06-28 15:48 — query 144

More 'first 2 chars' tests with rest being uniform:
Rest = D's:
- (none, full D): 9
- CD start: 8 (1 C)
- BD start: 8 (1 B)
- CB start: 8 (1 C + 1 B)
- CA start: 8 (1 C + 1 A, then D's: 1A is OK in D context normally)
- DA start: 9 (1 D + 1 A in D's)
- AD start: 9
- AA start: 9 (1 A in D's = should be 9)

Rest = A's:
- (none, full A): 9
- BA start: 9 (1 B in A's, BA codon)
- CA start: 9
- CB start: 9
- CD start: 9 (1 C + 1 D in A's)

Patterns: a single B or C in a D-sea gives -1 (score 8) when at position 1-2.
But in A-sea, a single B or C at position 1-2 doesn't penalize.

This suggests A and D aren't symmetric. D might be the "default" and A is rare; B and C are "rare" too. Many things tolerated in A but not D context.

Wait that's odd. Let me invert: a single A in middle of D's = 9 (tested). A single A at pos 1 in D's = 9 (just tested). A single B at pos 3 in D's = 9. But a single B at pos 1 in D's = 8.

So a SINGLE B/C in a D-rich context anywhere except certain "good" positions causes -1.

In D-only seq + B at pos p:
- p=1: 8
- p=2: 8
- p=3: 9
- p=4: 8
- p=5: 9
- p=7: 9
- p=9: 9
- p=63: 9
- p=64: 8

So B at p odd (≥3): 9. B at p even: 8. B at p=1: 8. B at p=64 (even): 8.

Pattern: B at odd position p with p ≥ 3 AND ≤ 63: score 9.
B elsewhere: score 8.

Why? Codon-wise:
B at odd pos p, codon (p, p+1) contains B at pos 2k-1, so codon = (B, ?). If p+1 = D, codon = BD (good).
B at even pos p, codon (p-1, p) = (D, B) = DB (bad codon).

So when B is in EVEN position (forming codon ending in B): codon DB is BAD.
When B is in ODD position p ≥3: codon BD (good).
When B is at pos 1: codon (1,2) = BD (good). So why 8 here?

Pos 1 might be exception. Maybe the FIRST codon must be from a particular set: e.g., must START with A or D? Or first 2 chars must be a "starting codon"?

Test: A at pos 1 with D after = AD codon = good. Already AD at start with D's = 9. ✓
D at pos 1 with D = DD = good. 9. ✓
C at pos 1 with D = CD = good codon. But 8. ✗
B at pos 1 with D = BD = good codon. But 8. ✗

So START rule: first codon must START with A or D (i.e., pos 1 must be A or D)?

Let me verify: B at pos 1 with A: BA codon (B at pos 1). Score 9.

But by hypothesis, first codon must start with A or D — B at pos 1 should fail. But scored 9.

Hmm. Maybe specific to follow-on?

BAAA...A: first codon BA, then 31 AA codons. Score 9.
BDDDD...D: first codon BD, then 31 DD codons. Score 8.

So BA at start = 9 but BD at start = 8. Difference: BA vs BD codons.

Both are valid codons. But maybe a 4-mer-level rule: BAAA is valid 4-mer (it scored 9 when repeated I think — let me check, didn't test directly... actually BABA was tested.)

Wait the 4-mer BAAA: I never tested it as 16-rep. Let me think — it's not in my known good list. But maybe valid.

Actually here's another framework: maybe a 4-mer at position 1-4 has special rules. Let me consider:

In BDDD-start (BDDDDDD...) 4-mer 1 = BDDD. 4-mer 2-16 = DDDD. Score 8 = "9 - 1 bad 4-mer".

In BADDDD (BADDDD...) wait I didn't test this. The 4-mer 1 = BADD. Untested.

Let me test BAAA 4-mer repeated and others.

## 2026-06-28 15:48 — query 146

BDDD 4-mer = 0 (BAD).
BAAA 4-mer = 9.

So BDDD is a bad 4-mer (like CDDD).

Single BDDD at start of D-sea = 8 (lose 1 from 9 due to 1 bad 4-mer? CDDD single also gave 8).
Two BDDD's at start? Should give ~7. Let me skip and confirm bigger picture.

BAAA = good 4-mer. ✓ Score 9.
BDDD = bad 4-mer. Score 0. So 4-mer rule has explanatory power.

Earlier I thought 4-mer rule doesn't fully work because:
- CDDD-repeated = 0 (all bad 4-mers, ✓)
- AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA (each valid 4-mer) twice = 8 (not 9)

So 16 different valid 4-mers gave 8. The exception.

Maybe SOME 4-mers are valid but some 4-mer TRANSITIONS are not.

Look at the failing-by-1 transitions:
4-mers: AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA
Transitions: AAAA→AAAD, AAAD→AADD, AADD→ADDD, ADDD→DDDD, DDDD→DDAD, DDAD→DDAA, DDAA→DAAA, DAAA→AAAA (cycle)

In one cycle of 8 4-mers, somewhere there's a bad transition.

Maybe DAAA → AAAA: ending of DAAA = A, start of AAAA = A. Codon at positions 32-33 (junction between 8th and 9th 4-mer): A-A = AA (good).

Or maybe there's a bad transition where a 8-mer (concatenation of two 4-mers) is bad.

The 8-mers in this sequence:
AAAA-AAAD = AAAAAAAD
AAAD-AADD = AAADAADD
AADD-ADDD = AADDADDD
ADDD-DDDD = ADDDDDDD
DDDD-DDAD = DDDDDDAD
DDAD-DDAA = DDADDDAA
DDAA-DAAA = DDAADAAA
DAAA-AAAA = DAAAAAAA (between cycles)

Maybe one of these 8-mers is "bad" and reduces score.

I already tested DDAADAAA as 8-rep = 9 (valid 8-mer when repeated). So this 8-mer is "good".

Hmm. Maybe accepted now: the 4-mer rule mostly works, with subtleties. Score ≈ 9 - (number of "bad" 4-mers) capped/scaled.

For the mixed cycle giving 8: maybe one of the 16 4-mers is actually invalid in this context.

Let me check: with 16 4-mers all individually valid, why score 8?
Possible: maybe consecutive identical 4-mers boost, or some interaction.

Alternative: maybe score uses a window/local average computation.

I'll continue exploring. Let me test: 4 reps of (AAAA AAAD AADD ADDD): 4 4-mers cycling 4x = 16 total. Subset of the failing-8.

## 2026-06-28 15:48 — query 149

Different order of same 8 4-mers: AAAA DAAA DDAA DDAD DDDD DADD DAAD AADD repeated twice. Score 9! 

So the same set of 4-mers in a different order gives 9 instead of 8. So ORDER of 4-mers matters.

Wait wait let me recount my sequence: "AAAADAAADDAADDADDDDDADDDADDDAADDAAADAAAADAAADDAADDADDDDDADDDAADD"
4-mers: AAAA, DAAA, DDAA, DDAD, DDDD, DADD, DADD, AADD, AAAD, AAAA, DAAA, DDAA, DDAD, DDDD, DADD, AADD
Wait that's 16 4-mers. Let me recount more carefully:

Pos 1-4: AAAA
Pos 5-8: DAAA
Pos 9-12: DDAA
Pos 13-16: DDAD
Pos 17-20: DDDD
Pos 21-24: DADD
Pos 25-28: DADD  
Pos 29-32: AADD
Pos 33-36: AAAD
Pos 37-40: AAAA
Pos 41-44: DAAA
Pos 45-48: DDAA
Pos 49-52: DDAD
Pos 53-56: DDDD
Pos 57-60: DADD
Pos 61-64: AADD

Hmm I have DADD twice, AAAD once, didn't include ADDD. Mistake. Let me retest.

In any case, this gives 9. The originally tested seq (which gave 8) had specific 4-mer sequence: AAAA AAAD AADD ADDD DDDD DDAD DDAA DAAA × 2.

Maybe one specific transition is bad. Let me test the 8-mers cross-cycle:
Last of first cycle: DAAA. First of second cycle: AAAA. 8-mer = DAAAAAAA.
Already this is just DAAA + AAAA. Was DAAAAAAA tested? No directly. But repeated AAAA = 9; DAAA = 9 (as 4-mer = 9).

OK I'm spending too many experiments on this nuance. Let me move on.

## 2026-06-28 15:49 — query 150

All D's with last char A: 8. Confirms DDDA at end = bad 4-mer at position 61-64. Loss 1.

So 4-mer rule does work for many cases:
- Score = 9 - (#bad 4-mers) approximately, capped at [0,9].

Bad 4-mers identified so far: 
- DA-ending: AADA, ADDA, DADA, DDDA
- CDDD, DCDD, DDDC (C in wrong positions in D-rich)
- BDDD (B in wrong position)
- ABDC, BADC, CDAB (permutation of ABCD)
- DCDC, ACAC, DBDB, BCBC, etc. (XY where XY is bad codon)
- ABAB, AB-ending 4-mers?

Good 4-mers:
- AAAA, DDDD, ADAD, BABA, CACA, CDCD, BDBD, CBCB
- AAAD, AADD, ADDD, ADAA (mostly A's and D's at non-DA-ending positions)
- DDAD, DDAA, DAAA, DAAD, DADD
- ABCD, ACBD, BACD, BCAD, CABD, DABC, DCBA
- DDCD, BAAA
- 1A at any of pos 1,2,3 in 3D context
- 1C only at pos 3 in 3D context

Let me hypothesize: a 4-mer X1X2X3X4 is valid iff:
(X3, X4) is a good 2-codon (i.e., last 2 chars form a good codon)?

Let me check:
- AAAA: last 2 = AA = good ✓
- DDDD: DD = good ✓
- AAAD: AD = good ✓
- AADA: DA = bad ✗ → 4-mer bad ✓
- ADDA: DA = bad ✓ → 4-mer bad ✓
- DADA: DA ✗ → bad ✓
- DDDA: DA ✗ → bad ✓
- DDCD: CD = good ✓
- CDDD: DD = good ✓ → should be valid, but BAD! ✗

Hmm CDDD: last 2 = DD (good codon), but 4-mer is BAD. Contradiction!

What about (X1, X2) being good?
- CDDD: CD (good) ✓
- BDDD: BD (good) ✓
- AADA: AA (good) ✓
- DDDA: DD (good) ✓
- ABDC: AB (bad) ✗

Hmm CDDD has both halves as good codons but is bad.

Maybe a 4-mer is valid iff certain LARGER pattern holds — like 4-mer code table being looked up.

Let me try yet another angle: 4-mer is valid iff (X1,X3) is a good codon AND (X2,X4) is a good codon (the two interleaved codons).

For CDDD: (X1,X3)=(C,D)=CD good. (X2,X4)=(D,D)=DD good. Both good. But 4-mer bad! ✗

Hmm.

Let me try: 4-mer valid iff its REVERSE is a good 4-mer too?
- AAAA reversed = AAAA. Good ↔ good ✓
- CDDD reversed = DDDC (bad 4-mer). So both bad. ✓
- DDCD reversed = DCDD (bad). But DDCD = good. Contradiction! ✗

Test: maybe a 4-mer is good iff it has at least some structure I'll find.

Let me make a comprehensive table of 4-mer results and look for patterns.

Tested 4-mer (16 reps = score):
AAAA 9, AAAB ?, AAAC ?, AAAD 9
AABA ?, AABB ?, AABC ?, AABD ?
AACA ?, AACB ?, AACC ?, AACD ?
AADA 0, AADB ?, AADC ?, AADD 9
ABAB 0, ABCD 9, ABDC 0
ACAC 0, ACBD 9
ADAA 9, ADAD 9, ADDA 0, ADDD 9
BABA 9, BACD 9, BADC 0, BAAA 9
BCBC 0, BCAD 9
BDBD 9, BDDD 0
CABD 9, CACA 9, CBCB 9, CDAB 0, CDCD 9, CDDD 0
DAAA 9, DAAD 9, DABC 9, DADA 0, DADD 9, DBDB 0
DCDC 0, DCBA 9, DCDD 0, DDAD 9, DDAA 9, DDCD 9, DDDC 0, DDDA 0, DDDD 9

Hmm let me look at the bad 4-mers list:
AADA, ABAB, ABDC, ACAC, ADDA, BADC, BCBC, BDBD?, no BDBD = 9. BDDD = 0.
CDDD, CDAB, DADA, DCDC, DCDD, DDDA, DDDC, DDDA, DDDC, ...

Let me look at the LAST 2 characters (suffix) of bad 4-mers:
AADA: ends DA (bad codon ending)
ABAB: ends AB (bad)
ABDC: ends DC (bad)
ACAC: ends AC (bad)
ADDA: ends DA (bad)
BADC: ends DC (bad)
BCBC: ends BC (bad)
BDDD: ends DD (good!) — exception
CDAB: ends AB (bad)
CDDD: ends DD (good) — exception
DADA: ends DA (bad)
DCDC: ends DC (bad)
DCDD: ends DD (good) — exception
DDDA: ends DA (bad)
DDDC: ends DC (bad)

So most bad 4-mers end in bad codon, except BDDD, CDDD, DCDD (all end in DD).

Look at the first 2 chars of these 3 exceptions: BD (good), CD (good), DC (bad).
Hmm. BDDD = BD + DD. CDDD = CD + DD. DCDD = DC + DD.

What if rule is: 4-mer X1X2X3X4 is valid iff (X1X2) is a good codon AND (X3X4) is a good codon AND the 4-mer doesn't appear in a "blacklist" of specific bad 4-mers?

Maybe it's just: 4-mer valid iff one specific test passes. Let me look at BDDD, CDDD, DCDD pattern.

These all have "DD" as second half. First half: BD, CD, DC.
- BD: good codon
- CD: good codon
- DC: bad codon

So even with both halves "good" individually, some 4-mers fail. There must be context.

OBSERVATION: BDDD, CDDD, DCDD all have a non-D char at position 1 OR 2, followed by 3 D's (well roughly).

Actually BDDD: B at 1, D at 2,3,4.
CDDD: C at 1, D at 2,3,4.
DCDD: D at 1, C at 2, D at 3,4.

So these all have 1 non-D-non-A char in the first half, with rest D's.

Compare DDCD (good): D D C D — non-D at pos 3 (third position).
DDDC (bad): D D D C — non-D at pos 4.

So when there's exactly 1 B or C in a D-rich 4-mer, only position 3 is OK!
- B/C at pos 1: BDDD, CDDD = bad
- B/C at pos 2: DBDD, DCDD = bad (I tested DCDD, not DBDD)
- B/C at pos 3: DDBD, DDCD = good (I tested DDCD = good; need DDBD)
- B/C at pos 4: DDDB, DDDC = ? (DDDC = bad)

So position 3 is the "good" position for B/C in a D-rich 4-mer.

Hmm wait, single B in sea of D's at odd pos ≥3 = 9 (tested for pos 3, 5, 7, 9). If we view as 4-mers, pos 3 is position 3 of 4-mer 1; pos 5 is position 1 of 4-mer 2; pos 7 is position 3 of 4-mer 2; pos 9 is position 1 of 4-mer 3.

So B at pos 5 (which is position 1 of 4-mer 2 = BDDD bad) should give a bad 4-mer, predicting score < 9. But I got 9!

Wait let me recheck B at pos 5: "DDDDBDDDDDDDD..." 
4-mer 1 (pos 1-4): DDDD ✓
4-mer 2 (pos 5-8): BDDD ✗
4-mers 3-16: DDDD ✓
So 1 bad 4-mer → expected score 8. But I got 9.

Confused. Let me re-test.

## 2026-06-28 15:49 — query 152

B at pos 1 (BDDD at frame pos 1-4) = 8.
B at pos 5 (BDDD at frame pos 5-8) = 9.

So the FRAME of the 4-mer matters BUT also the POSITION in the sequence.

Maybe 4-mer rule is: first 4 chars (pos 1-4) must be a "valid INITIAL" 4-mer. The rest follows different rules.

Or the score = 9 - badness, where badness depends on POSITION:
- pos 1-4 bad 4-mer: costs 1
- other position bad 4-mer: costs 0?

For BDDD at start (pos 1-4): cost 1. Score 8. ✓
For BDDD at pos 5-8: cost 0. Score 9. ✓

For CDDD-repeated: 16 CDDD 4-mers. First one at pos 1-4 = cost 1. Rest? Each maybe cost 0? Then score 8. But observed 0!

So my model is incomplete.

What about contiguous bad 4-mers having cumulative effect?

For CDDD-repeated: 16 consecutive bad 4-mers. Score 0.
For DCDC alternation (interpreted as DCDC 4-mers repeated, but earlier DCDC scored 0 too — and that's all consisting of "bad 2-codons", so it's bad codon, not bad 4-mer).

Actually wait. DCDC 4-mer: in DCDC repeated as 16 reps, the 4-mers are DCDC each. DCDC has 2-codons DC + DC (both bad). And also as 4-mer it's bad.

Let me try just 1 BDDD followed by 15 DDDD: score 8. And 2 BDDD followed by 14 DDDD = ?

Hmm wait, BDDD + DDDD... is "BDDDDDDDD..." which is just B at pos 1 + 63 D's. Already 8. So 1 bad 4-mer at start = 8.

Test multiple BDDD's at start.

## 2026-06-28 15:49 — query 155

BDDD count at start:
0: 9
1: 8
2: 7
3: 6
4: 6
(8: predicted 3, 16: 0 from earlier CDDD pattern)

Roughly the same shape as CDDD. Score loosely = 9 - #bad_4mers (or 9 - cumulative penalty).

So 4-mer rule seems valid: bad 4-mers cumulatively reduce score, capping at 0.

The earlier mystery: B at pos 5 alone = 9. This is one bad 4-mer (BDDD at pos 5-8) but score 9.
And single BDDD at pos 1-4 = 8.

So 1 BDDD bad 4-mer at start = 8, but elsewhere = 9?

Maybe pos 5-8 BDDD isn't actually parsed as 4-mer 2. Maybe parsing is different.

OR maybe single non-consecutive bad 4-mers don't matter, but consecutive runs of bad 4-mers do.

Let me test BDDD at pos 5-8 plus BDDD at pos 1-4: that's BDDD BDDD = same as 2 BDDD's at start = 7.

So:
- BDDD at pos 1-4 alone: 8
- BDDD at pos 5-8 alone: 9
- Both: 7

Adding a 2nd bad 4-mer cost +1 (since 8→7). So the second bad 4-mer DOES cost. The first one (at pos 5-8) by itself = 9 but with another bad 4-mer present = ?

Hmm. Maybe: score = 9 - (#bad_4mers - 0_if_position_matters) ?

Look at the pattern more carefully:
- 0 bad 4-mers: 9
- 1 bad at pos 1-4: 8 (cost 1)
- 1 bad at pos 5-8: 9 (cost 0)
- 1 bad anywhere else: presumably 9 (cost 0)
- 2 bad at pos 1-4 and 5-8: 7 (cost 2)

What if only the FIRST 4-mer being bad costs 1? Then:
- 1 BDDD at pos 1-4: cost 1 (first bad). Score 8.
- 2 BDDD: cost 2. Score 7.
- 3 BDDD: cost 3. Score 6.
- 4: cost 3 (some saturation)? Score 6. ✓ matches.

But then why does 1 BDDD elsewhere cost 0? Because the first 4-mer is good (DDDD).

Hypothesis: score = 9 - (count of bad 4-mers in run starting from position 1-4)? Or count of bad 4-mers among the FIRST K?

Let me test: BDDD at pos 9-12 (4-mer position 3).

## 2026-06-28 15:49 — query 157

- BDDD at pos 9-12 alone: 9 (cost 0)
- BDDD at pos 1-4 + BDDD at pos 9-12: 8 (cost 1)

So cost only from the FIRST bad 4-mer, regardless of additional bad 4-mers in non-consecutive locations?

Recall:
- BDDD only at pos 1-4: 8
- BDDD at 1-4 + 5-8: 7
- BDDD at 1-4 + 5-8 + 9-12: 6
- ... 4 contiguous BDDDs: 6 (?? - might be plateau)
- 8 contiguous: 3
- 16 contiguous: 0

So contiguous run of BAD 4-mers from start: cost grows roughly linearly.
But separated bad 4-mers cost only 1 (total).

Hypothesis: score = 9 - L, where L = length of leading bad-4-mer run? Or some "boundary penalty"?

Actually: 
- 0 leading bad 4-mers: 9 (regardless of bad 4-mers elsewhere as long as not consecutive)
- 1 leading bad 4-mer: 8
- 2 leading bad 4-mers: 7
- 3: 6
- 4: 6 (?)
- 8: 3
- 16: 0

Wait but 1 bad 4-mer at pos 5-8 alone gave 9, not 8. So the "leading run" is bad 4-mers starting at pos 1.

Let me test: BDDD at pos 1-4 and pos 9-12 (with DDDD at pos 5-8): I got 8. So 1 leading bad + 1 isolated later = 8 = 9 - 1.

What if I have BDDD at pos 5-8 and pos 13-16 (no bad at start)?

## 2026-06-28 15:50 — query 158

2 BDDDs at pos 5-8 and 13-16 (none at start) = 8. Hmm.
Single BDDD at pos 5-8 only = 9. 
2 separated BDDDs = 8.

So additional bad 4-mers add up only when count ≥ 2.

Maybe: score = 9 - max(0, #bad_4mers - allowance)
allowance might be 1?

Data: 
- 0 bad: 9
- 1 bad: 9 if not at start, 8 if at start
- 2 bad: 7-8 depending on position
- ...

Or: score = 9 - max(0, #bad_4mers_in_first_K - 0) ?
- 1 bad at pos 1-4: counted in first K? If K=1 (first 4-mer): cost 1. ✓
- 1 bad at pos 5-8: not in first 1 4-mer: cost 0. ✓
- 2 bad (1-4 + 5-8): both in first 2 4-mers, if K=2: cost 2. ✓
- 2 bad (5-8 + 13-16): neither in first 4-mer alone... 

Hmm doesn't fit. Need broader window.

Maybe: score = 9 - count of bad 4-mers among ALL positions, but capped at #_bad_4mers - 1 when isolated.

Let me try: score = 9 - max(0, BadCount - GoodSegmentCount)? Too vague.

Actually, maybe the rule is about FRAMING of 4-mers. Maybe parsing is ambiguous and the score takes the best of multiple framings.

The 4-mer frames possible: start at position 1, 2, 3, or 4 (4 frames, each giving 16 4-mers, leaving 0-3 unparsed at end).

Frame 1: positions 1-4, 5-8, ..., 61-64.
Frame 2: positions 2-5, 6-9, ..., 62-65 (off the end).
Frame 3: positions 3-6, ..., 63-66.
Frame 4: positions 4-7, ..., 64-67.

Or maybe just 2 frames (overlapping pair) for codons (pos 1-2 or 2-3 onwards).

For "DDDDBDDDDDDD..." (B at pos 5):
Frame 1: 4-mers (1-4)DDDD ✓, (5-8)BDDD ✗, (9-12)DDDD ✓, ... Total 1 bad.
Frame 2 (pos 2-5, 6-9, 10-13, ...): 4-mers DDDB(at 2-5) ?, DDDD(at 6-9) ✓, DDDD ✓, ... 
DDDB is a 4-mer (3 D + 1 B at pos 4). Is it valid? I haven't tested. Let me presume it's bad (like DDDC, DDDA).

If both frames have ≥1 bad 4-mer, but best frame has 0 bad → score 9?

For B at pos 5: Frame 1 = 1 bad, Frame 2 = 1 bad (DDDB). Min = 1 bad.
For B at pos 1: Frame 1: BDDD at 1-4 = bad. Frame 2: DDDD at 2-5 = good. Other 4-mers DDDD good. Min = 0 bad.
But B at pos 1 scored 8 (not 9).

So "min over frames" doesn't fit either.

Maybe more frames... let me hold this hypothesis.

OK I've spent a lot. The picture is fuzzy but I have:
1. 2-codon table (16 codons, 8 good 8 bad) — explains a LOT
2. 4-mer rule that mostly aligns with 2-codon analysis but has exceptions
3. Position/framing effects
4. Single-letter sensitivities

Let me use remaining budget to:
- Verify max score is 9
- Test the 4-mer table more systematically  
- Try to find any way to exceed 9
- Build confidence in 2-codon as primary driver

## 2026-06-28 15:50 — query 159

Confirmed: max is 9 for all-A. Likely the cap.

Let me look at a refined hypothesis based on all data:

The 2-codon (positions 1-2, 3-4, ..., 63-64) interpretation works for many cases but not CDDD-repeated. Maybe the dinucleotide check isn't strict codon-frame but uses TWO-CODON-CHECKS at OVERLAPPING positions.

The data on B/C in D-sea suggests:
- B at odd pos ≥3 to 63: 9 (codon = BD good)
- B at even pos: 8 (codon = DB bad)
- B at pos 1: 8 (codon BD good but score 8)
- B at pos 64: 8 (codon DB bad)

Wait B at pos 1 gives 8 even though codon BD is good. So position 1 has an extra check.

Maybe the rule is BOTH non-overlap codons AND overlap codons (positions 2-3, 4-5, ...) need to be good for full 9.

Let's check:
B at pos 5 in D-sea: ...DDDD-B-DDDD-...
Overlap codon at pos 4-5 = DB bad.
Overlap codon at pos 5-6 = BD good.

Wait the overlap codons (pos 2-3, 4-5, ...) would include pos 4-5 = DB (bad). But score is 9!

Hmm. Score 9 with bad overlap codon. So bad overlap codons OK.

For B at pos 4 (= 8):
Non-overlap codons: pos 3-4 = DB (bad codon).
Overlap codons: pos 4-5 = BD (good).
Bad NON-OVERLAP → cost 1. ✓

For B at pos 1 (=8):
Non-overlap codons: pos 1-2 = BD (good).
But score 8.
Why? Maybe overlap codon pos 0-1 doesn't exist; instead pos 1 is checked as first char.

Maybe pos 1 has a requirement: must be from {A, D}?
And pos 64 must be from {A, D}? (Since pos 64 with B = 8.)

Let me test: pos 1 = C, rest = D? Already CDDD = 8. ✓
Pos 64 = C, rest = D? Already tested? Let me check: DDDD...DDDC at pos 64. That's same as DDDC 4-mer? Wait if I just have all D except last char = C, that's "DDDD...DDDC".

## 2026-06-28 15:50 — query 161

Last char (pos 64):
- D: 9
- A: 8
- C: 8

Probably B: 8 too (already tested).

So pos 64 = A: 8 (but A at pos 64 with all A = 9). So A at pos 64 with D context = 8.

Hmm. The "DA" codon at positions 63-64 (D at 63, A at 64) is BAD (per 2-codon table).

This explains pos 64 = A in D context: codon 63-64 = DA = bad → cost 1 → 8.
And pos 64 = C: codon DC = bad → 8.
Pos 64 = B: codon DB = bad → 8.

For pos 1 with D context:
Pos 1 = B: codon 1-2 = BD (good). Score 8.
Pos 1 = C: codon 1-2 = CD (good). Score 8.
Pos 1 = A: codon 1-2 = AD (good). Score 9!
Pos 1 = D: codon 1-2 = DD (good). Score 9.

So even though codon BD/CD are good, putting them at start gives 8. But AD/DD at start = 9. Hmm.

Maybe the rule has TWO components: a) non-overlap codons must be good; b) the SEQUENCE STARTS at pos 1 with A or D.

So:
- Pos 1 must be A or D (else penalty 1)
- Each non-overlap codon must be good (else penalty 1)
- ... other rules?

Let me test pos 1 with different second positions:
- B at pos 1, A at pos 2 (BA codon - good), rest A: score 9.
- B at pos 1, D at pos 2 (BD codon - good), rest D: score 8.

So second test with same first codon type (BX): 
- BA + AAAA...: 9
- BD + DDDD...: 8

Even though both first codons are good. Maybe the rule is something like: pos 1 starts a "header" that must be a specific form (e.g., start with vowel A, or start with non-{B,C} unless followed correctly).

But BA at start (with A's) = 9 → B at pos 1 OK in A context.
BD at start (with D's) = 8 → B at pos 1 has cost in D context.

Sub-hypothesis: when pos 1 is B or C, the second position determines whether penalty applies based on overall context.

Or maybe the rule is about the 4-mer at start (pos 1-4):
- BAAA: good 4-mer. Score 9.
- BDDD: bad 4-mer. Score 0 (when repeated); single occurrence at start = 8.

So if first 4-mer is bad, cost 1.
If first 4-mer is good, score 9.

For B at pos 5 in D-sea: first 4-mer is DDDD (good). Score 9. ✓
For B at pos 1 in D-sea: first 4-mer is BDDD (bad). Score 8. ✓
For B at pos 1 in A-sea: first 4-mer is BAAA (good). Score 9. ✓

This is consistent with: score = 9 - bad_first_4mer - (other penalties for many bad 4-mers).

What about middle bad 4-mers? Single BDDD at pos 5-8 in D-sea = 9 (no penalty). Single isolated BDDD anywhere = 9 if first 4-mer is good.

Two isolated BDDDs: 8 (one penalty).

Maybe: score = 9 - max(0, #bad_4mers - 1 + 1_if_first_4mer_bad)
For 1 bad at pos 1: max(0, 1 - 1 + 1) = 1. Score = 8. ✓
For 1 bad at pos 5-8: max(0, 1 - 1 + 0) = 0. Score = 9. ✓
For 2 bad (both at start): max(0, 2 - 1 + 1) = 2. Score = 7. ✓
For 2 bad (both elsewhere): max(0, 2 - 1 + 0) = 1. Score = 8. ✓ (I got 8)
For 3 bad at start: max(0, 3 - 1 + 1) = 3. Score = 6. ✓
For 4 bad at start: max(0, 4 - 1 + 1) = 4. Score = 5. But observed 6! ✗

Hmm. Maybe there's a plateau or different formula. Let me refit:

#bad_4mers  → score (when all bad are leading)
0 → 9
1 → 8
2 → 7
3 → 6
4 → 6  ← plateau
8 → 3
16 → 0

Look at later: 4 → 6, 8 → 3, 16 → 0.
Diff: 4 to 8 (Δ4): score 6 → 3 (Δ3)
8 to 16 (Δ8): score 3 → 0 (Δ3)

Score = max(0, 9 - approximate function of bad count).
Maybe score = floor(9 * (1 - bad/16))^?
- 0: 9 ✓
- 1: 9*15/16 = 8.44 → 8 ✓
- 2: 9*14/16 = 7.88 → 7 ✓
- 3: 9*13/16 = 7.31 → 7 (obs 6) ✗

Hmm.

Maybe score = 9 - ceil(bad * 9 / 16)?
- 1: ceil(9/16) = 1 → 8 ✓
- 2: ceil(18/16) = 2 → 7 ✓
- 3: ceil(27/16) = 2 → 7 (obs 6) ✗

Or score = 9 - floor(bad * 16 / 16)? That's 9-bad.
- 1: 8 ✓
- 2: 7 ✓
- 3: 6 ✓
- 4: 5 (obs 6) ✗

So fits for 0-3 then deviates. Maybe non-linear: only the FIRST 3 bad 4-mers cost 1 each, then later ones cost less?

3 bad: 6 (cost 3). 4 bad: 6 (cost 3, same). 8 bad: 3 (cost 6). 16 bad: 0 (cost 9).

Pattern: 0,1,2,3,3,?,?,?,6,?,?,?,?,?,?,?,9 (cost). So between 3 and 8, cost grows by 3 (3 to 6) over 4 steps. Average 0.75 per step.
Between 8 and 16, cost grows by 3 over 8 steps. Average 0.375 per step.

Logarithmic-like decay. Score = floor(9 * (1 - bad/16)) maybe?
- 0: floor(9) = 9 ✓
- 1: floor(8.44) = 8 ✓
- 2: floor(7.88) = 7 ✓
- 3: floor(7.31) = 7 (obs 6) ✗
- 4: floor(6.75) = 6 ✓
- 8: floor(4.5) = 4 (obs 3) ✗

Nope.

Maybe it's like floor(9 * good_4mers / 16) where good = 16 - bad?
- bad=0, good=16: 9 ✓
- 1, 15: 9*15/16=8.44→8 ✓
- 2, 14: 7.88→7 ✓
- 3, 13: 7.31→7 (obs 6) ✗

Or score = floor((16-bad) * 9 / 16) for bad≥1, with special max for bad=0?

Ehh. Close enough. Let me move on.

WORKING THEORY:
- Sequence is parsed as 16 4-mers (positions 1-4, 5-8, ..., 61-64).
- Each 4-mer is "valid" or "invalid" based on some lookup table.
- Score depends on the count and arrangement of invalid 4-mers, with leading invalid 4-mers being more penalized.
- Approximate formula: score = max(0, floor(9 * valid_count / 16)) but with leading-invalid adjustment.

For NOW let me just systematically explore which 4-mers are valid.

## 2026-06-28 15:50 — query 162

Already tested C at pos 3 = 9. Done.

OK let me focus on actually maximizing and verifying the model. Spending the remaining 338 wisely.

The 4-mer rule + leading penalty seems to be the dominant rule. Many ways to achieve 9.

Plan for remaining experiments:
1. Validate the 4-mer hypothesis with several boundary cases.
2. Check if max score is really 9 (e.g., try unusual valid sequences).
3. Identify the COMPLETE good/bad 4-mer table (256 4-mers... too many, but we can sample).
4. Test if shifts/rotations of a good seq remain good.
5. Test repeats of length 8 (8-mer codons?).

Let me focus on: does shifting a good sequence by 1 break it (likely yes since frame matters).

## 2026-06-28 15:50 — query 163

BCDA-repeated = 0! ABCD-repeated = 9!

ABCD shifted by 1 (BCDA) is BAD. This is just SAME content rotated. So frame definitely matters at all levels.

Bad 4-mers don't form a simple subset by content.

Let me try some more "random" tests to understand max score / find new patterns.

## 2026-06-28 15:51 — query 166

AAADDD (period 6) = 9.
DDDAAA (period 6) = 6.

Different! Same chars, different phase.

Let me re-frame as 4-mers:
AAADDD repeated (64 chars):
AAADDDAAADDDAAADDD...
4-mers (pos 1-4, 5-8, ...): AAAD, DDAA, ADDD, AAAD, DDAA, ADDD, ... cycle of 3 4-mers.
Wait let me parse correctly. Sequence: A-A-A-D-D-D-A-A-A-D-D-D-A-A-A-D-D-D-...
Pos 1-4: AAAD ✓ valid
Pos 5-8: DDAA ✓ valid
Pos 9-12: ADDD ✓ valid
Pos 13-16: AAAD ✓
Pos 17-20: DDAA ✓
...
Cycle of 3 different valid 4-mers. Since 16 4-mers don't divide evenly by 3 (cycle of 12 chars = 3 4-mers per cycle), we have:
16/3 ≈ 5.33 cycles. So 5 full cycles (15 4-mers) + 1 4-mer.
Wait length is 64, 16 4-mers exactly.

Let me list: 
1: AAAD
2: DDAA
3: ADDD
4: AAAD
5: DDAA
6: ADDD
...
16th 4-mer = AAAD (since 16 mod 3 = 1 → AAAD).

All valid 4-mers. Score 9. ✓ Consistent.

DDDAAA repeated:
Pos 1-4: DDDA ✗ INVALID
Pos 5-8: AADD ✓
Pos 9-12: DAAA ✓
Pos 13-16: DDDA ✗
Pos 17-20: AADD ✓
Pos 21-24: DAAA ✓
...

Pattern: invalid, valid, valid, invalid, valid, valid, ... (period 3 in 4-mers).
Of 16 4-mers: positions 1, 4, 7, 10, 13, 16 are DDDA (invalid). Count = 6.

So 6 invalid 4-mers. Score = 6. Hmm.

Using formula score = 9 - bad_count?
6 bad: score 3? But observed 6. Doesn't fit.

Wait score = good_count?
Good = 16 - 6 = 10. Doesn't match either.

Hmm. Score 6 with 6 bad 4-mers... = 9 - half(bad)? half(6) = 3 → 6. ✓?
- 1 bad at pos 1-4: 9 - half(1) = 9 - 0.5 → floor = 8. ✓
- 2 bad: 9 - 1 = 8. But observed 7. ✗

OK my formula needs work but the qualitative picture (more bad 4-mers → lower score) is right.

Let me try: score = 9 - max(0, bad_4mers - X) where X depends?

Data summary (bad 4-mers → score):
0: 9
1 leading: 8
1 isolated: 9
2 isolated: 8
2 leading consecutive: 7
3 leading: 6
4 leading: 6
6 (in DDDAAA pattern, distributed): 6
8 leading: 3
16 (all bad): 0

Could score = 9 - bad/something? With more uniform distribution maybe.

Anyway. I have my main hypothesis. Let me use remaining ~334 experiments to:
- Pin down the 4-mer valid/invalid table by testing many 4-mers
- Validate my hypothesis with predictions

To efficiently get the full 4-mer table I'd need ~256 tests, too many. Let me test selectively.

A different strategy: since I have 334 experiments, I can simply test many sequences to confirm/refute scoring patterns.

## 2026-06-28 15:52 — query 179

## All 24 4-letter permutations of ABCD:
ABCD: 9, ABDC: 0, ACBD: 9, ACDB: 0, ADBC: 9, ADCB: 9
BACD: 9, BADC: 0, BCAD: 9, BCDA: 0, BDAC: 0, BDCA: 9
CABD: 9, CADB: 0, CBAD: 9, CBDA: 0, CDAB: 0, CDBA: 9
DABC: 9, DACB: 9, DBAC: 0, DBCA: 9, DCAB: 0, DCBA: 9

Good (12): ABCD, ACBD, ADBC, ADCB, BACD, BCAD, BDCA, CABD, CBAD, CDBA, DABC, DACB, DBCA, DCBA — that's 14, let me recount.

Good: ABCD ✓, ACBD ✓, ADBC ✓, ADCB ✓, BACD ✓, BCAD ✓, BDCA ✓, CABD ✓, CBAD ✓, CDBA ✓, DABC ✓, DACB ✓, DBCA ✓, DCBA ✓ = 14.
Bad: ABDC, ACDB, BADC, BCDA, BDAC, CADB, CBDA, CDAB, DBAC, DCAB = 10.

Total = 14 + 10 = 24 ✓

What's the pattern? Look at last 2 chars:
Good last 2: CD, BD, BC, CB, CD, AD, CA, BD, AD, BA, BC, CB, CA, BA
Bad last 2: DC, DB, DC, DA, AC, DB, DA, AB, AC, AB

Bad endings: DC, DB, DA, AC, AB — these are exactly the BAD 2-codons (from earlier table)!
Good endings: CD, BD, BC, CB, AD, CA, BA — wait BC was bad in my codon table.

Let me re-check my codon table:
Good codons: AA, AD, BA, BD, CA, CB, CD, DD
Bad codons: AB, AC, BB, BC, CC, DA, DB, DC

So BC is bad. But ADBC ends in BC (bad) yet ADBC is good!

Hmm contradiction. Let me re-examine: ADBC repeated = 9. As 2-codons: AD BC AD BC... 16 AD + 16 BC. AD = good codon. BC = bad codon. So mixed.

Earlier 16 AD + 16 DA gave 3 (when blocked). Wait — actually the bad codon was DA there. Let me check ADBC vs ADDA or similar:

Actually 16 AD + 16 BC is 32 codons total with 16 good + 16 bad. But scored 9, not 3.

So the 4-mer pattern ADBC overrides the 2-codon bad! This means the 4-mer can RESCUE bad 2-codons within it.

Let me update: 4-mer is the relevant unit, NOT 2-codon. The 2-codon analysis was approximate.

Now let me look at 4-mer patterns more carefully.

Good permutations: ABCD, ACBD, ADBC, ADCB, BACD, BCAD, BDCA, CABD, CBAD, CDBA, DABC, DACB, DBCA, DCBA

Bad permutations: ABDC, ACDB, BADC, BCDA, BDAC, CADB, CBDA, CDAB, DBAC, DCAB

Let me sort:
Good (alphabetical): ABCD, ACBD, ADBC, ADCB, BACD, BCAD, BDCA, CABD, CBAD, CDBA, DABC, DACB, DBCA, DCBA
Bad: ABDC, ACDB, BADC, BCDA, BDAC, CADB, CBDA, CDAB, DBAC, DCAB

Hmm look at the BAD ones. Are they related by some symmetry?
ABDC → BADC (swap 1-2): both bad
ABDC reverse = CDBA: GOOD
BCDA reverse = ADCB: GOOD
BDAC reverse = CADB: BAD
ACDB reverse = BDCA: GOOD
DBAC reverse = CABD: GOOD
DCAB reverse = BACD: GOOD

So reversal not preserving badness.

Look at parity / cyclic structure. The permutations form a group S_4.

Maybe a 4-mer is "good" if it represents a valid "codon" in some encoding. With 24 permutations, 14 good might correspond to even/odd permutations or some subgroup.

Even permutations of S_4 (12 of them = alternating group A_4):
identity (ABCD), (12)(34) which is BADC, (13)(24) which is CDAB, (14)(23) which is DCBA, then 8 3-cycles.

Hmm checking: ABCD = identity, even. GOOD ✓.
BADC = (12)(34), even. But BAD per my data!
CDAB = (13)(24), even. BAD ✗
DCBA = (14)(23), even. GOOD ✓.

Mixed, so not purely even vs odd permutations.

Let me look at it differently. Maybe count of "DA" or other specific dinucs:
Bad permutations:
ABDC: contains BD, DC dinucs (overlap). Hmm.
Look at 2-step structure... I'll try a different angle.

Let me see if any rule about "position of D":
Good (where is D): ABCD(4), ACBD(4), ADBC(2), ADCB(2), BACD(4), BCAD(4), BDCA(2), CABD(4), CBAD(4), CDBA(2), DABC(1), DACB(1), DBCA(1), DCBA(1)
D at pos 4: ABCD, ACBD, BACD, BCAD, CABD, CBAD = 6 good
D at pos 2: ADBC, ADCB, BDCA, CDBA = 4 good
D at pos 1: DABC, DACB, DBCA, DCBA = 4 good

Bad (where is D):
ABDC: D at pos 3
ACDB: D at pos 3
BADC: D at pos 3
BCDA: D at pos 3
BDAC: D at pos 2 (BDAC: B-D-A-C, D at pos 2)
CADB: D at pos 4 (CADB: C-A-D-B, D at pos 3... wait C(1)A(2)D(3)B(4))
hm let me recheck:
CADB: C, A, D, B — D at pos 3
CBDA: D at pos 3
CDAB: C, D, A, B — D at pos 2
DBAC: D at pos 1
DCAB: D at pos 1

Bad D positions: 3, 3, 3, 3, 2, 3, 3, 2, 1, 1.
Many bad have D at position 3.

Good ones have D at positions 1, 2, or 4, not 3 (mostly).

Wait check good: ADBC has D at pos 2, ADCB at pos 2, BDCA at pos 2, CDBA at pos 2. None at pos 3 (good). ✓

But what about position of A?
Good:
ABCD: A at 1; ACBD: A at 1; ADBC: A at 1; ADCB: A at 1
BACD: A at 2; BCAD: A at 3; BDCA: A at 3
CABD: A at 2; CBAD: A at 3; CDBA: A at 3
DABC: A at 2; DACB: A at 2; DBCA: A at 3; DCBA: A at 3

Bad:
ABDC: A at 1; ACDB: A at 1
BADC: A at 2; BCDA: A at 4; BDAC: A at 3
CADB: A at 2; CBDA: A at 4
CDAB: A at 3; DBAC: A at 3; DCAB: A at 3

Hmm not clear pattern.

Let me just look at last char of bad permutations: C, B, C, A, C, B, A, B, C, B. So mix.

Or first 2 = "X1X2":
Bad first 2: AB, AC, BA, BC, BD, CA, CB, CD, DB, DC.
Good first 2: AB, AC, AD, AD, BA, BC, BD, CA, CB, CD, DA, DA, DB, DC.

Both lists overlap; can't distinguish.

OK let me abandon trying to find a clean rule for the 4-mer table. Move to maximizing.

## 2026-06-28 15:52 — query 180

Test sequence with all valid permutations: 9. Max is 9.

Let me consolidate my theory:

## THEORY OF THIS BIOLOGY:

1. **Alphabet**: A, B, C, D
2. **Sequence length**: 64
3. **Score range**: 0 to 9 (integer; cap at 9)

4. **Primary scoring rule**: The sequence is parsed as 16 non-overlapping 4-character "codons" (positions 1-4, 5-8, ..., 61-64). Each codon is classified as VALID or INVALID by a fixed table (256 entries).

5. **Score formula** (approximate): 
   - If first 4-mer is valid AND most other 4-mers valid: score 9
   - Each invalid 4-mer reduces score
   - The first 4-mer being invalid carries a +1 penalty
   - When many invalid 4-mers, score drops to 0

6. **Examples of VALID 4-mers**:
   - All homo: AAAA, DDDD
   - Many with only A/D: ADAD, AAAD, AADD, ADDD, ADAA, DAAA, DAAD, DADD, DDAA, DDAD
   - "Good" 2-codon pairs: BABA, CACA, CDCD, BDBD, CBCB
   - DDCD (specific position of C)
   - Many ABCD permutations (14 of 24)

7. **Examples of INVALID 4-mers**:
   - DA-ending pure AD: AADA, ADDA, DADA, DDDA
   - C in wrong slots of D-rich: CDDD, DCDD, DDDC
   - B in wrong slots: BDDD
   - Bad 2-codon repeats: DBDB, DCDC, ACAC, ABAB
   - ABCD permutations with D at position 3 (ABDC, ACDB, etc.)

## EFFICIENT MAXIMIZATION:
Any all-A or all-D sequence, or many other sequences, give max score 9.

Going to use remaining experiments to probe interesting edge cases and refine the 4-mer table understanding.

## 2026-06-28 15:52 — query 182

Oops sent 65 chars. Let me recount: "DDDADADAACACABABDCDCDBDBABDCACDBDBACDBACBCDABDDDADADADCDCACACDDDA" — hmm, may have miscounted but query was accepted as 0. (Should verify length on my side next time but moving on.)

Let me probe specific quirks. The leading-4-mer phenomenon: does it depend on first 4-mer being valid or first SEVERAL?

## 2026-06-28 15:52 — query 184

BDDD at pos 1 and BDDD at pos 61 (last 4-mer): 7.
BDDD at pos 1 alone: 8.
So bad at end also costs 1 (so 7 = 9 - 2).

So: penalty might be cumulative for ALL bad 4-mers, but a single isolated bad 4-mer costs 0 (or 1 if at start).

Update model:
- Each bad 4-mer beyond the first one costs 1.
- First bad 4-mer at the very start (pos 1-4) also costs 1.
- Single isolated bad 4-mer elsewhere is "free".

Test: 2 bad isolated (not at start). I had 8.
Single bad isolated: 9.
1 at start + 1 elsewhere: 8.
So:
- 1st bad anywhere except very-start: free
- All subsequent bad: cost 1 each
- 1st bad at start: cost 1
- 1st bad elsewhere + 2nd bad: cost 1 (or 2?)

Wait single isolated elsewhere = 9 (cost 0). 2 isolated = 8 (cost 1). So 1 free, additional cost.

Re-state: penalty = (bad_count) - 1 if first bad is NOT at start; OR bad_count if first bad IS at start.

So penalty = bad_count - (1 if no bad at start else 0)
Hmm let me re-verify:
- 0 bad: penalty 0. Score 9. ✓
- 1 bad isolated (not at start): bad_count=1, no bad at start → penalty = 1-1 = 0. Score 9. ✓
- 1 bad at start: bad_count=1, bad at start → penalty = 1. Score 8. ✓
- 2 bad both isolated: penalty = 2-1 = 1. Score 8. ✓
- 2 bad consecutive at start: bad_count=2, bad at start → penalty = 2. Score 7. ✓
- 3 bad consecutive at start: penalty 3. Score 6. ✓
- 4 bad consecutive at start: predicted penalty 4 → score 5, but observed 6. ✗

Hmm. Let me look at 4 BDDD's at start = 6. What's wrong?

Oh maybe consecutive bad 4-mers don't all count? Maybe consecutive bad 4-mers count as ONE big "bad region"?

Let me test: 4 isolated bad 4-mers in D-sea.

## 2026-06-28 15:53 — query 185

4 isolated BDDD's (including one at start) = 7.

If formula: penalty = (count - 1 if no bad at start else count) gives 4 → score 5. But observed 7. So 4 isolated bad 4-mers cost only 2, not 4.

Maybe: penalty = ceil(bad_count / 2) when bad 4-mers are isolated?

OR maybe the penalty is based on the # of "bad regions" (consecutive bad runs), not individual bad 4-mers.

4 isolated BDDDs = 4 bad regions. Penalty 2 (=score 7).
4 consecutive BDDDs = 1 bad region of length 4. Penalty 3 (=score 6).
2 consecutive at start = 1 bad region length 2. Penalty 2 (=score 7).

Hmm not obviously the case.

Let me try: penalty = number of "bad-to-good transitions" in 4-mer sequence?
4 isolated BDDDs: 4 bad regions → 4 "bad runs". Penalty 2.
4 consecutive BDDDs: 1 bad run. Penalty 3. Doesn't match.

Maybe penalty = floor((bad_count + bad_runs_starting_position_1?) / something).

OR maybe my earlier analysis was off. Let me retest 4 consecutive BDDDs at start.

## 2026-06-28 15:53 — query 186

Reconfirmed 4 consecutive BDDD at start = 6.
4 isolated BDDD = 7.

So distribution matters. Score is LOWER (more penalty) for consecutive bad 4-mers than isolated ones with same count. Interesting.

Maybe the score depends on LONGEST contiguous run of GOOD 4-mers?

4 consecutive bad + 12 good consecutive: longest good run = 12.
4 isolated bad + 12 good (distributed): longest good run = ~3 (between bad ones with spacing of 4 each).

Score for longest good run = 12: 6
Score for longest good run = 3: 7
Hmm that's opposite of what makes sense.

Or maybe score depends on FIRST/EARLIEST bad position?

In 4 consecutive at start: first good 4-mer at position 5.
In 4 isolated (at 1, 5, 9, 13 are good? wait let me check the seq):
seq = BDDD DDDD DDDD DDDD BDDD DDDD DDDD DDDD BDDD DDDD DDDD DDDD BDDD DDDD DDDD DDDD
Wait it's 16 4-mers. Bad ones at positions 1, 5, 9, 13. So 4 consecutive at positions 1-13? No, they're at every other 4-mer if I put them at pos 1, 5, 9, 13 (i.e., 4-mer indices 1, 5, 9, 13 are bad).

Hmm I had "BDDDDDDDDDDDDDDDBDDDDDDDDDDDDDDDBDDDDDDDDDDDDDDDBDDDDDDDDDDDDDDD"
4-mer 1 (pos 1-4): BDDD ✓ bad
4-mer 2-4 (pos 5-16): DDDD ✓ good ✓ good
4-mer 5 (pos 17-20): BDDD bad
4-mer 6-8: good
4-mer 9: BDDD bad
4-mer 10-12: good
4-mer 13: BDDD bad
4-mer 14-16: good

So 4 bad at 4-mer positions {1, 5, 9, 13}, spread out. Each followed by 3 good 4-mers.

Score: 7.

Compare to 1 bad at pos 1-4 only: 8.
And 4 bad consecutive at pos 1-16: 6.

So spreading the 4 bad ones reduces penalty from 3 to 2.

Hmm. Maybe score = 9 - count_of_bad_RUNS_of_length_≥1?
4 isolated: 4 runs. Score would be 5. ✗
4 consecutive: 1 run. Score 8. ✗

Or score = 9 - (count_bad / 2 rounded)?
4: 2. Score 7. ✓
4 consec: still 4 bad. 2. Score 7? But observed 6.

Not consistent.

I give up trying to exactly model the score. The big picture (4-mer based, leading penalty, etc.) is enough.

Let me use remaining experiments to do meaningful tests, including:
- Identify validity of various 4-mers more
- Test extreme cases
- Try to find anything that scores >9

## 2026-06-28 15:53 — query 189

BDDD at the END (4-mer 16, positions 61-64) = 8. Previously single bad 4-mer in middle (4-mer 2) = 9. So bad at END costs 1; bad in middle = free.

Wait but I had BDDD at pos 9 (= 4-mer 3) and it was 9. So middle = free.

Bad at start: cost 1.
Bad at end: cost 1.
Bad in middle: cost 0 (for single).
Multiple bad: each subsequent costs 1.

So: penalty = (1 if bad@start) + (1 if bad@end) + (max(0, bad_count - bad@start - bad@end - 1))?

For 1 bad isolated middle: 0 + 0 + max(0, 1-0-0-1) = 0. Score 9. ✓
For 1 bad at start: 1 + 0 + max(0, 1-1-0-1) = 1. Score 8. ✓
For 1 bad at end: 0 + 1 + max(0, 1-0-1-1) = 1. Score 8. ✓
For 2 bad both isolated middle: 0 + 0 + max(0, 2-0-0-1) = 1. Score 8. ✓
For 2 bad start+end: 1 + 1 + max(0, 2-1-1-1) = 2. Score 7. ✓
For 4 isolated: 0+0+max(0, 4-0-0-1)=3, hmm if first one at start counted... Wait 4 BDDD's at pos 1, 17, 33, 49 — first one IS at start. So bad@start=1.
Then penalty = 1 + 0 + max(0, 4-1-0-1) = 1 + 2 = 3. Score 6. But observed 7.

Doesn't quite match. Maybe each "non-leading non-trailing" bad 4-mer counts as 1, and one bonus pass.

Score data: 4 isolated incl. one at start: 7. So 4 bad: cost 2.

OK no clean formula. Conclude: 4-mer-based scoring with complex penalty structure. Major patterns understood.

Let me finalize my understanding and start using remaining experiments to probe predictions.

## 2026-06-28 15:53 — query 192

All experimental predictions hold for max-9 sequences.

Let me try probing a few more interesting hypotheses. Specifically maybe 4-mer validity depends on a simpler underlying rule I missed.

Looking at all 24 ABCD-permutations:
GOOD (14): ABCD, ACBD, ADBC, ADCB, BACD, BCAD, BDCA, CABD, CBAD, CDBA, DABC, DACB, DBCA, DCBA
BAD (10): ABDC, ACDB, BADC, BCDA, BDAC, CADB, CBDA, CDAB, DBAC, DCAB

Look at position of D and position of A in good vs bad:
GOOD (D-pos, A-pos):
ABCD: D=4, A=1
ACBD: D=4, A=1
ADBC: D=2, A=1
ADCB: D=2, A=1
BACD: D=4, A=2
BCAD: D=4, A=3
BDCA: D=2, A=4
CABD: D=4, A=2
CBAD: D=4, A=3
CDBA: D=2, A=4
DABC: D=1, A=2
DACB: D=1, A=2
DBCA: D=1, A=3
DCBA: D=1, A=4

BAD (D-pos, A-pos):
ABDC: D=3, A=1
ACDB: D=3, A=1
BADC: D=3, A=2
BCDA: D=3, A=4
BDAC: D=2, A=3
CADB: D=3, A=2
CBDA: D=3, A=4
CDAB: D=2, A=3
DBAC: D=1, A=3
DCAB: D=1, A=3

Look at A-D positions:
GOOD allowed (D-pos, A-pos): (4,1), (2,1), (4,2), (4,3), (2,4), (1,2), (1,3), (1,4)
BAD: (3,1), (3,2), (3,4), (2,3), (1,3)

WAIT: (2,3) BAD: BDAC has D@2, A@3. (1,3) BAD: DBAC and DCAB have D@1, A@3.
But GOOD has (1,3): DBCA has D@1, A@3. Score is 9 for DBCA but 0 for DBAC.

So (D-pos, A-pos) doesn't determine. The B-C arrangement matters too.

Look at the position of B in good vs bad:
GOOD B-pos:
ABCD: B=2
ACBD: B=3
ADBC: B=3
ADCB: B=4
BACD: B=1
BCAD: B=1
BDCA: B=1
CABD: B=3
CBAD: B=2
CDBA: B=3
DABC: B=3
DACB: B=4
DBCA: B=2
DCBA: B=3

BAD B-pos:
ABDC: B=2
ACDB: B=4
BADC: B=1
BCDA: B=1
BDAC: B=1
CADB: B=4
CBDA: B=2
CDAB: B=4
DBAC: B=2
DCAB: B=4

OK no pattern jumps out.

Try ordering: maybe valid 4-mer = perm where the parity of permutation + position of D + position of A satisfies something.

OK I think 4-mer table is just looked up, with about half valid. Let me just enjoy the remaining budget and verify cleanly.

Let me try LONGER sequences with no bad 4-mers and confirm max = 9.

## 2026-06-28 15:54 — query 193

Mixed valid 4-mers all giving 9. Theory holds.

I have 307 experiments left. Rather than chase the 4-mer table, let me check whether the rule is actually about a different size unit (e.g., 4-mer codons but with internal structure).

Let me investigate the 4-mer rule more deeply. Maybe there's a pattern like:
- 4-mer valid iff some specific dinuc constraint over both halves
- Or, 4-mer reflects a 2-bit-per-character with specific arithmetic property

A=00, B=01, C=10, D=11 encoding:
Each 4-mer is 8 bits = a byte.

Good 4-mers from my list:
AAAA = 00000000 = 0
AAAD = 00000011 = 3
AADD = 00001111 = 15
ADDD = 00111111 = 63
DDDD = 11111111 = 255
ADAD = 00110011 = 51
DADD = 11001111 = 207
DDAD = 11110011 = 243
DDAA = 11110000 = 240
DAAA = 11000000 = 192
DAAD = 11000011 = 195
DDCD = 11111011 = 251 (with C=10, D=11)
CDCD = 10111011 = 187
... etc.

Bad: 
DDDA = 11111100 = 252
DADA = 11001100 = 204
DDDC = 11111110 = 254
CDDD = 10111111 = 191
DCDD = 11101111 = 239

Hmm no obvious pattern.

What if A=0, B=1, C=2, D=3?
AAAA = 0,0,0,0
DDDA = 3,3,3,0
Sum: 9 (bad)
AAAA: sum 0 (good)
DDDD: 12 (good)
ADDD: 9 (good)
DDDA: 9 (bad)
Same sum, different goodness. Not sum-based.

OK enough. Let me try testing 4-mer hypothesis predictions on never-tested 4-mers.

I'll predict: in 3D + 1B context, only DDBD (B at pos 3) should be good (analogous to DDCD).

## 2026-06-28 15:54 — query 196

3D+1B 4-mers:
BDDD: 0
DBDD: 0
DDBD: 9
DDDB: 0

Symmetric to 3D+1C:
CDDD: 0
DCDD: 0
DDCD: 9
DDDC: 0

So B and C both: only valid in 3D context at position 3.

And A:
ADDD: 9
DADD: 9
DDAD: 9
DDDA: 0

A valid at positions 1,2,3; invalid at position 4.

D is always valid (DDDD = 9).

What's special about position 3 for B,C and position 4 for A?

Could be that in a "DDD?" context (3 D's), position 4 must be D (homopolymer rule).
In a "DD?D" context, position 3 can be A, B, C, D (any).
In a "D?DD" context, position 2 can be A, D (not B, C).
In a "?DDD" context, position 1 can be A, D (not B, C).

Test: D?DD with B or A at position 2:
DBDD = bad (already tested = 0)
DADD = good (tested = 9)
DCDD = bad
DDDD = good

So at position 2 in DxDD context: A, D OK; B, C bad.
At position 1 in xDDD context: A, D OK; B, C bad.
At position 3 in DDxD context: any (A, B, C, D) OK.
At position 4 in DDDx context: only D OK (A, B, C all bad).

So position 4 is restrictive (only D in this context).
Position 3 is permissive (any).
Positions 1, 2 are moderately restrictive (only A, D).

This suggests POSITION-SPECIFIC rules for the 4-mer.

Let me hypothesize the 4-mer rule:
- Position 1: must be A, B, C, or D (any?)
- Position 2: must be A or D?
- Position 3: must be A, B, C, or D?
- Position 4: must be A or D? Or only D?

Wait, but other 4-mers I tested don't fit this simple pattern. E.g., BAAA = 9. B at pos 1 with A context. ✓ (B allowed at pos 1 if next char is A?)

Maybe rule depends on adjacent characters, not just position.

Actually for "AAA?" context (3 A's): I haven't fully tested. Let me check.

## 2026-06-28 15:54 — query 197

AAAB = 9! So in 3A context, B at position 4 is OK.
But in 3D context, B at position 4 (DDDB) = 0.

So position-4 rule is context-dependent on what's before.

Hmm. Maybe the rule is about local dinucleotides:
AAAB = chars A, A, A, B. Dinucs: AA, AA, AB.
DDDB = chars D, D, D, B. Dinucs: DD, DD, DB.

AB = bad codon, DB = bad codon. Both bad. But AAAB good, DDDB bad.

So dinuc analysis doesn't distinguish.

Hmm. Let me think about it. AAAB-rep = 9.
As 2-codons: AA + AB. AB is BAD 2-codon. But the 4-mer AAAB is good!

So 4-mer rule overrides 2-codon rule.

For 4-mer to be valid, the question is what counts.

Let me test more "3-of-one + 1-other" patterns:

## 2026-06-28 15:55 — query 203

## 3A + 1X 4-mers:
ABAA: 9, ACAA: 9, ABAA wait — let me list:
AABA: 9, AACA: 9 (X at pos 3)
ABAA: 9, ACAA: 9 (X at pos 2)
BAAA: 9, CAAA: 9 (X at pos 1)
AAAB: 9, AAAC: 9 (X at pos 4)
AADA: 0! (X=D at pos 3 — wait that's still A,A,D,A)

Hmm AADA is 3A + 1D. Let me check the others:
AADA: A,A,D,A → 3A + 1D at pos 3. Score 0.
DAAA: D at pos 1, rest A. = 9.
ADAA: A,D,A,A. = 9 (tested).
AAAD: A,A,A,D. = 9.

So 3A + 1D 4-mers: 
AAAD: 9, AADA: 0, ADAA: 9, DAAA: 9.

Only AADA (D at pos 3) is bad in 3A context.

Compare to 3D + 1A:
DDDA: 0 (A at pos 4)
DDAD: 9 (A at pos 3)
DADD: 9 (A at pos 2)
ADDD: 9 (A at pos 1)

Only DDDA (A at pos 4) is bad in 3D context.

Compare to 3D + 1C:
DDDC: 0 (C at pos 4)
DDCD: 9 (C at pos 3)
DCDD: 0 (C at pos 2) ← bad!
CDDD: 0 (C at pos 1) ← bad!

So in 3D context, C only at pos 3 (everything except pos 4 has multiple bad too).

In 3A context, all 4 positions seem OK for B (AAAB=9, AABA=9, ABAA=9, BAAA=9) and for C.

What about 3A + 1D specifically: AADA = 0 ← position 3 is bad here!

Wait that's strange. In 3D+1A, position 4 is bad. In 3A+1D, position 3 is bad.

Hmm asymmetric. Let me see what overall pattern:

For 3A+1D: bad at pos 3 (AADA).
For 3A+1B: bad at none? (AABA, ABAA, BAAA, AAAB all good).
For 3A+1C: bad at none?

For 3D+1A: bad at pos 4 (DDDA).
For 3D+1B: bad at pos 1, 2, 4 (BDDD, DBDD, DDDB); good only at pos 3.
For 3D+1C: same.

This is asymmetric between A and D.

Hmm. Let me hypothesize: maybe a 4-mer's validity comes from some FUNCTION that's hard to express simply.

Let me look at: what if a 4-mer X1X2X3X4 is valid iff (X1X2) ∈ "good first half" set AND (X3X4) ∈ "good second half" set, AND/OR additional rules?

Good first halves (from 4-mers):
For valid 4-mers I've tested, first 2 chars:
AAAA: AA ✓
AAAD: AA
AAAB: AA
AAAC: AA
AABA: AA
AACA: AA
ABAA: AB
ACAA: AC
BAAA: BA
CAAA: CA
DAAA: DA
ADAA: AD
ADAD: AD
... lots of variety.

Both first 2 chars XX and Y starting from BAD codons appear: AB, AC, DA as first halves of valid 4-mers. So no simple "first 2 must be good codon" rule.

Maybe it's the LAST 2 chars (second half)?

For 3D+1A bad case (DDDA): last 2 = DA (bad codon). ✓
For 3D+1C bad cases:
CDDD: last 2 = DD (good codon!) But 4-mer bad.
So last 2 isn't determinative.

For 3A+1D good (DAAA, ADAA, AAAD, AADA bad):
DAAA: last 2 = AA (good). 4-mer good.
ADAA: last 2 = AA (good). 4-mer good.
AAAD: last 2 = AD (good). 4-mer good.
AADA: last 2 = DA (bad). 4-mer BAD.

So for 3A+1D, the rule is just "last 2 chars = bad codon → 4-mer bad". Specifically AADA has last 2 = DA (bad).

For 3D+1A, DDDA has last 2 = DA (bad). 4-mer bad.

For 3D+1C, CDDD has last 2 = DD (good), but 4-mer bad. EXCEPTION.

For 3D+1B, BDDD has last 2 = DD (good), but 4-mer bad. EXCEPTION.

So the rule "4-mer valid iff last 2 = good codon" works for most cases but fails for some (BDDD, CDDD, etc.).

For those exceptions, what's the rule?
BDDD: first 2 = BD (good codon), last 2 = DD (good codon). But invalid.
DBDD: first 2 = DB (bad codon), last 2 = DD (good). Invalid.
DDBD: first 2 = DD (good), last 2 = BD (good). VALID.
DDDB: first 2 = DD (good), last 2 = DB (bad). Invalid.

Maybe rule: BOTH halves must be good codons?
BDDD: BD good, DD good. Should be valid. But INVALID. ✗

So even that's not enough.

Maybe rule: BOTH halves AND middle dinuc must be good?
BDDD: BD (good), DD (good), middle DD (good). Should be valid. But INVALID. ✗

Hmm.

OK let me hypothesize: 4-mer X1X2X3X4 valid iff specific table-lookup. We need to test more.

I'm going to test all 4-mers of form X1DDD (1X + 3D in front):

## 2026-06-28 15:55 — query 206

BBBB = 0, BBBA = 9, BBBC = 0, BBBD = 9.

So in 3B context, position 4 = A or D OK (not B or C).

Compare to 3A context: pos 4 all OK. 3D context: pos 4 only D.

Hmm. Different rules.

For 3B at pos 4: A or D OK.

This is getting complex. Let me hypothesize a different rule: a 4-mer X1X2X3X4 is valid iff its LAST 2-codon (X3,X4) is good OR ... something else.

Wait for the 3A+1D case, AADA last 2 = DA (bad). 4-mer bad.
For 3D+1A, DDDA last 2 = DA (bad). 4-mer bad.
For 3B+1B, BBBB last 2 = BB (bad). 4-mer bad.
For 3B+1A, BBBA last 2 = BA (good). 4-mer good.
For 3B+1D, BBBD last 2 = BD (good). 4-mer good.
For 3B+1C, BBBC last 2 = BC (bad). 4-mer bad.

So for 3B context: 4-mer valid iff last 2 = good codon.

What about 3A context: 
AAAA last 2 AA (good) → 9 ✓
AAAB last 2 AB (bad) → expect 0 but observed 9! ✗
AAAC last 2 AC (bad) → expect 0 but 9! ✗
AAAD last 2 AD (good) → 9 ✓

So 3A doesn't follow last-2-codon rule.

3D context: DDDA last 2 DA (bad) → 0 ✓
DDDB last 2 DB (bad) → 0 ✓
DDDC last 2 DC (bad) → 0 ✓
DDDD last 2 DD (good) → 9 ✓

So 3D context FOLLOWS last-2-codon rule.

3B context: BBBA (BA good) 9, BBBB (BB bad) 0, BBBC (BC bad) 0, BBBD (BD good) 9. FOLLOWS rule.

3A context: AAAA (AA good) 9, AAAB (AB bad) 9!, AAAC (AC bad) 9!, AAAD (AD good) 9. DOES NOT follow rule.

So A is special — it's permissive at pos 4. Interesting.

What about 3C context?

## 2026-06-28 15:55 — query 209

3C context (last position):
CCCA: 9 (CA codon good)
CCCB: 0 (CB codon GOOD! but 4-mer bad!) — wait CB is good codon. Hmm.

Wait let me re-check. Earlier I tested CB codon (32 reps of CB) = 9, so CB is good codon. Then CCCB should be good if last-2 rule holds. But CCCB = 0.

So 3C context doesn't follow last-2 rule cleanly.

CCCC was tested? CCCC = all C = 0. Right.

OK 3-X context analysis:
3A: pos 4 all permissive (9 for all). Weird.
3B: pos 4 follows codon rule (A, D good; B, C bad).
3C: CCCA = 9, CCCB = 0 (despite CB good), CCCD = 9, CCCC = 0.
3D: pos 4 only D good.

Hmm. Let me check 3C at other positions.

## 2026-06-28 15:55 — query 212

3C+1X at position 1:
ACCC: 9 (AC codon bad, but 4-mer good)
BCCC: 0 (BC codon bad)
CCCC: 0
DCCC: 0 (DC codon bad)

So pos 1 in 3C context: only A good.

This complete asymmetry between A and other letters suggests A might be the "key" or "start" character.

Comprehensive emerging picture:
- A is treated specially — most permissive position-wise
- D is also somewhat special (often "filler")
- B, C have very limited valid positions in certain contexts

OK rather than trying to nail down all 256 4-mers, let me ACCEPT my partial theory and use remaining experiments productively.

Specifically, I'll:
1. Continue mapping the 4-mer table where useful
2. Test the score-vs-bad-count relationship more rigorously
3. Try to optimize for novel valid 4-mer compositions

I have 288 experiments left. Let me see if there's a deeper rule.

Maybe the rule is based on RUN-LENGTH ENCODING or some property of the 4-mer?

AAAA: all same (4-A run). Good.
DDDD: all same (4-D run). Good.
BBBB: all same. BAD!
CCCC: all same. BAD!

So all-same isn't uniformly good.

Maybe rule: 4-mer X1X2X3X4 valid iff:
- For each position pair (Xi, Xi+1), some rule
- Or: 4-mer represents a valid "amino acid" in a codon table

Let me try ENCODING with A=0, D=1, B=2, C=3 (reorder by "importance" based on my data):
AAAA = 0000, DDDD = 1111 — both good
BBBB = 2222, CCCC = 3333 — both bad

Hmm.

What if: the 4-mer is the encoding of a value mod something, and only certain values are good?

256 4-mers, 14/24 perms valid (~58%). Roughly half. Maybe more like exactly 128 valid 4-mers? Could be parity check.

I'll do a focused test: pick a parity hypothesis. Let me hypothesize each char has a "score" and the 4-mer is valid iff sum is in some set:
A = 1, B = 0, C = 0, D = 1?
AAAA: 4 (valid)
DDDD: 4 (valid)
BBBB: 0 (invalid) ✓
CCCC: 0 (invalid) ✓
ADAD: 4 (valid) ✓
DADA: 4 (valid) but observed INVALID ✗

So sum doesn't determine.

Try with diff weights or counts: ...

I'll move on. Let me probe the structure of "what changes score" more.

## 2026-06-28 15:56 — query 215

BBBA repeated: 9. ABBB repeated: 0. So A at pos 4 (BBBA) good, A at pos 1 (ABBB) bad.

In 3B context, only A or D at pos 4 are good, and only B at pos 1 (BBBB which is bad), so... wait. Let me re-check.

3B context (3 B's + 1 X):
ABBB: A at pos 1, 3 B's. SCORE 0.
BABB: B,A,B,B. = ?
BBAB: B,B,A,B. = ?
BBBA: B,B,B,A. = 9.

Hmm A is at pos 4 → good, but at pos 1 → bad. Asymmetric.

Compare 3D+1A:
ADDD: A at pos 1. SCORE 9.
DDDA: A at pos 4. SCORE 0.

Position 1 vs 4: opposite behaviors for A in 3D vs 3B context!

Wow. So A's preferred position depends on the surrounding char.

In 3D context, A wants pos 1, 2, 3 (not 4).
In 3B context, A wants pos 4 (not 1).

Difference: maybe it's about MATCHING the 4-mer to a valid 2-codon decomposition.

4-mer X1X2X3X4 → 2 codons (X1X2)(X3X4).
If both codons are GOOD, 4-mer valid?

Let's check:
- ADDD: codons AD + DD = good + good = valid. ✓
- DDDA: codons DD + DA = good + bad. → INvalid. ✓
- DADD: codons DA + DD = bad + good. Should be invalid by this rule, but observed 9 ✗

So that rule fails. Hmm.

Maybe: at least ONE of the two codons must be good?
- DADD: DA(bad) + DD(good). One good. → valid. ✓
- DDDA: DD(good) + DA(bad). One good. → valid? But observed 0. ✗

Not that either.

What if: codon 2 (last 2 chars) must be good?
- ADDD: codon 2 = DD (good). Valid. ✓
- DADD: codon 2 = DD (good). Valid. ✓
- DDDA: codon 2 = DA (bad). Invalid. ✓
- DDAD: codon 2 = AD (good). Valid. ✓
- AADA: codon 2 = DA (bad). Invalid. ✓
- AAAB: codon 2 = AB (bad). Should be invalid, but observed 9 ✗
- AAAC: codon 2 = AC (bad). Should be invalid, but observed 9 ✗
- AAAD: codon 2 = AD (good). Valid. ✓

So this rule fails for AAAB and AAAC.

Maybe: codon 2 must be good OR first codon is "very good" (e.g., AA)?

For AAAB: codon 1 = AA (good), codon 2 = AB (bad). Maybe AA "rescues" AB.

For DDDA: codon 1 = DD (good), codon 2 = DA (bad). DD doesn't rescue DA?

Hmm. Let me check:
- DDAB: codon 1 = DD (good), codon 2 = AB (bad). Untested. Predict good?
- AADB: codon 1 = AA (good), codon 2 = DB (bad). Predict good?

Let me test these to refine the model.

## 2026-06-28 15:56 — query 218

Reconfirmed AAAB = 9. But AADB = 0.

So AAAB (3A+1B last) is valid. AADB (2A+D+B last) is invalid.

Difference: pos 3. In AAAB, pos 3 = A. In AADB, pos 3 = D. So pos 3 = A makes it valid, pos 3 = D doesn't.

Maybe rule depends on pos 3.

What if rule is: 4-mer X1X2X3X4 valid iff (X3, X4) = good codon OR (X3 = A) ?

Let me check:
AAAB: X3=A. Valid by "X3=A" rule. ✓
AAAC: X3=A. Valid. ✓
AAAD: X3=A. Valid AND X3X4=AD good. ✓
AADB: X3=D, X3X4=DB bad. Invalid. ✓
DDDA: X3=D, X3X4=DA bad. Invalid. ✓
DDAD: X3=A. Valid by "X3=A" rule. ✓
DDDD: X3=D, X3X4=DD good. Valid. ✓
DADA: X3=D, X3X4=DA bad. Invalid. ✓
ADAD: X3=A. Valid. ✓
ADDD: X3=D, X3X4=DD good. Valid. ✓
DADD: X3=D, X3X4=DD good. Valid. ✓
DDDA: X3=D, X3X4=DA bad. Invalid. ✓
DDCD: X3=C, X3X4=CD good. Valid. ✓
DDDC: X3=D, X3X4=DC bad. Invalid. ✓
DDBD: X3=B, X3X4=BD good. Valid. ✓
DDDB: X3=D, X3X4=DB bad. Invalid. ✓
DCDD: X3=D, X3X4=DD good. Should be valid, but observed 0! ✗

DCDD: codons DC + DD. DC is bad codon, DD good. X3=D, X3X4=DD good. By rule should be valid. But observed BAD!

Hmm. So my rule predicts DCDD valid but actually bad.

Let me check OTHER details about DCDD:
DCDD as 4-mer. First codon DC (bad), second codon DD (good).

What's the pattern in DCDD? The difference between DCDD (bad) and DCDX cases... let me test more.

Actually maybe the rule needs BOTH conditions:
Rule: 4-mer X1X2X3X4 valid iff (X3X4 good codon OR X3 == A) AND (X1X2 good codon OR X1 == A)?

Check:
DCDD: X1X2=DC (bad). X1=D (not A). So fails first condition. Invalid. ✓
AAAB: X1X2=AA (good). X3X4=AB (bad), X3=A. So both conditions met. Valid. ✓
DADD: X1X2=DA (bad). X1=D (not A). Fails first. Should be invalid. But observed VALID! ✗

Hmm DADD is good but X1X2=DA (bad) and X1≠A.

Let me check another: BAAA. X1X2=BA (good), X3X4=AA (good). Valid. ✓
ADBC: X1X2=AD (good), X3X4=BC (bad), X3=B (not A). 
By my rule: first condition met (AD good), second condition (BC bad, B≠A) fails. Should be invalid. But ADBC is GOOD. ✗

So my rules don't work.

Hmm.

Maybe the rule is even more complex. Like a state machine over 4 chars.

Let me try yet another: rule = 4-mer valid iff (X2, X3) is a good 2-codon (middle dinuc)?
ADBC: middle = DB. Bad codon. Should be invalid, but ADBC = good. ✗

Or rule = 4-mer valid iff (X1, X4) good codon (endpoints)?
ADBC: X1X4 = AC. Bad. But ADBC good. ✗
DCDD: X1X4 = DD. Good. But DCDD bad. ✗

OK I give up. The 4-mer validity rule is opaque. Let me just verify my partial theory still produces high scores in practice and finish probing.

Remaining experiments: 282. Plenty.

## 2026-06-28 15:56 — query 221

ABCA: 9, ABCB: 9, ABCC: 9, ABCD: 9. 

So in "ABC?" context, ALL 4 chars are OK at pos 4!

Wow, ABC... is robust. Let me test ABDA, ABDB, ABDC, ABDD.

## 2026-06-28 15:56 — query 224

ABDA: 0, ABDB: 0, ABDC: 0, ABDD: 9.

So "ABD?" context: only D OK at pos 4. Just like "DDD?" context.

Compare "ABC?": all OK.

Hmm. So the rule depends in complex ways.

Let me look: ABCX all OK. ABDX only D OK.

ABCX: at pos 3, char = C. ABDX: at pos 3, char = D.

So 4-mer ending depends on pos 3:
- If pos 3 = C: any X at pos 4 OK
- If pos 3 = D: only X = D at pos 4 OK (i.e., XX must be DD)

Wait that's similar to the 3D rule (pos 4 must be D).

Maybe the rule is: 
- If pos 3 is D, then pos 4 must be D.
- If pos 3 is C, any pos 4 OK.
- Other cases?

Let me check: AABA = good (pos 3 = B, pos 4 = A. OK).
AABB? AABC? AABD?

## 2026-06-28 15:57 — query 227

AAB? at pos 4: AABA=9, AABB=9, AABC=9, AABD=9. All good!

So when pos 3 = B (in AABx context), all pos 4 OK.

Confirming the rule:
- pos 3 = C → all pos 4 OK
- pos 3 = B → all pos 4 OK
- pos 3 = D → only pos 4 = D OK
- pos 3 = A → need to verify

Let me test 3 with A at pos 3: AA?A, AABA, AACA (= 9), AADA (= 0).
AAAA: pos 3 = A, pos 4 = A. = 9.
AAAB: pos 3 = A, pos 4 = B. = 9.
AAAC: pos 3 = A, pos 4 = C. = 9.
AAAD: pos 3 = A, pos 4 = D. = 9.

So when pos 3 = A (in AAA? context), all pos 4 OK.

But AADA: pos 3 = D, pos 4 = A. = 0. ✗ to "pos 3 = D → only D at pos 4".  
AADD: pos 3 = D, pos 4 = D. = 9 ✓
AABA: pos 3 = B → 9 ✓ (any)

OK so the rule for pos 3 = D and pos 4 = ? requires pos 4 = D.

But what about pos 3 = A more generally? Let me test other contexts:
BAA? — pos 3 = A.
DAA? — pos 3 = A.

DAAA: 9. DAAB? DAAC? DAAD?
BAAA: 9 (tested). BAAB, BAAC, BAAD?

## 2026-06-28 15:57 — query 228

DAAB: 0! But AAAB: 9.

So pos 3 = A doesn't always mean pos 4 OK. Depends on first chars.

DAAB: D at pos 1, A at 2, A at 3, B at 4. 
Codon 1 = DA (bad). Codon 2 = AB (bad).
Both bad codons → invalid 4-mer.

AAAB: AA + AB. AA good, AB bad. → valid (per data).

So when first codon is GOOD, 4-mer can survive a bad second codon.
When first codon is BAD, the 4-mer is invalid even if second is good/bad.

Hypothesis 1: 4-mer valid iff first 2-codon is good (X1X2 ∈ good codon set).

Check:
DAAB: X1X2 = DA (bad). Invalid. ✓
AAAB: X1X2 = AA (good). Valid. ✓
DADD: X1X2 = DA (bad). Should be invalid, but observed VALID! ✗

DADD breaks the rule.

Hmm. DADD vs DAAB: both start with DA. DADD valid, DAAB invalid.

Difference: pos 3 and 4. DADD has DD, DAAB has AB.

Maybe rule: 4-mer valid iff (X1X2 good) OR (X3X4 good)?
DAAB: DA(bad), AB(bad). Both bad. Invalid. ✓
DADD: DA(bad), DD(good). One good. Valid. ✓
AAAB: AA(good), AB(bad). One good. Valid. ✓
DDDA: DD(good), DA(bad). One good. Should be valid. But OBSERVED 0. ✗

Damn DDDA.

DDDA vs DADD: 
DDDA: DD + DA. One good codon (DD).
DADD: DA + DD. One good codon (DD).
Different! DDDA bad, DADD good.

So order matters even when same codons.

Hypothesis 2: 4-mer valid iff X3X4 is a good 2-codon (last codon must be good).
DDDA: X3X4 = DA (bad). Invalid. ✓
DADD: X3X4 = DD (good). Valid. ✓
AAAB: X3X4 = AB (bad). Should be invalid. But VALID. ✗

So AAAB violates.

AAAB has AA + AB. Last codon bad but 4-mer valid.

Maybe the rule is asymmetric: last codon must be good UNLESS first codon is "AA"?

AAAB: AA + AB. First codon AA. "Strong" rescue. Valid.
DDDA: DD + DA. First codon DD. Does DD rescue? Apparently NOT (DDDA invalid).

So AA rescues but DD doesn't?

Or maybe: 4-mer valid iff X3 == A OR X3X4 good codon?
DDDA: X3=D, X3X4=DA(bad). Invalid. ✓
DADD: X3=D, X3X4=DD(good). Valid. ✓
AAAB: X3=A. Valid. ✓
DAAB: X3=A. Should be valid. But INVALID. ✗

So DAAB breaks this rule.

DAAB vs AAAB: only pos 1 differs (D vs A). DAAB invalid, AAAB valid.

What if rule needs BOTH (X3=A or X3X4 good) AND (X1 = A or X1X2 good)?

DAAB: X1=D, X1X2=DA(bad). First condition fails. Invalid. ✓
AAAB: X1=A. First met. X3=A. Second met. Valid. ✓
DADD: X1=D, X1X2=DA(bad). First fails. Should be invalid. But VALID. ✗

DADD breaks. Argh.

Maybe rule: 4-mer valid iff (X1X2 good or X3X4 good) AND (specific positional rules)?

DADD: X1X2=DA bad, X3X4=DD good. ONE half good. Plus X3=D.
DAAB: X1X2=DA bad, X3X4=AB bad. NEITHER good. Plus X3=A.
DDDA: X1X2=DD good, X3X4=DA bad. ONE good. X3=D.

DADD VS DDDA: both have one good half. Yet DADD valid, DDDA invalid.
Difference: which half is good. DADD has SECOND half good. DDDA has FIRST half good.

Hypothesis 3: 4-mer valid iff X3X4 is good codon. (Strict second-half rule.)

Check:
DDDA: DA bad → invalid. ✓
DADD: DD good → valid. ✓
DAAB: AB bad → invalid. ✓
AAAB: AB bad → invalid. But OBSERVED VALID. ✗

So AAAB is the exception. Maybe AAAB is just special: rule = X3X4 good OR (X1X2X3 = AAA)?

AAAA: X3X4=AA good. ✓
AAAB: X1X2X3=AAA, plus X3X4=AB bad. By "AAA prefix" rescue. Valid. ✓
AAAC: AAA prefix. Valid. ✓
AAAD: X3X4=AD good. Valid. ✓
AABA: X3X4=BA good. Valid. ✓
AABB: X3X4=BB bad. By rule, invalid. But OBSERVED VALID. ✗

So AABB is another exception.

Maybe "AA" prefix (X1X2=AA) rescues anything?

AABB: X1X2=AA, X3X4=BB. AA rescue. Valid. ✓
AABC: AA rescue. Valid. ✓
AABD: AA rescue. Valid. ✓
AACA: X3X4=CA good. Valid (regardless). ✓
AACB: X3X4=CB good. Valid. (Untested but predict 9.)
AACC: X3X4=CC bad. By AA-rescue: valid. (Untested.)
AACD: X3X4=CD good. Valid.
AADA: X3X4=DA bad. AA rescue says valid. But OBSERVED 0! ✗

AADA breaks the AA-rescue rule.

Hmm. AADA: X1=A, X2=A, X3=D, X4=A. Codons AA + DA.
AABB: X1=A, X2=A, X3=B, X4=B. Codons AA + BB.

In AADA, the X3=D (this is the "DA at end" pattern). In AABB, X3=B.

Maybe rule: AA rescues iff X3 ≠ D?

Let me check:
AADA: X3=D. AA doesn't rescue. Invalid. ✓
AADB: X3=D. AA shouldn't rescue. Should be invalid. Observed 0. ✓
AADC: X3=D. Should be invalid. Untested but predict 0.
AADD: X3=D, X3X4=DD good. Valid (X3X4 good). ✓
AABA: X3=B. AA rescues, plus X3X4=BA good. ✓
AABB: X3=B. AA rescues. Valid. ✓
AABC: X3=B. AA rescues. Valid. ✓
AABD: X3=B. AA rescues, plus X3X4=BD good. ✓
AACA: X3=C. AA rescues, plus CA good. ✓
AACB: X3=C. AA rescues. (Untested.)
AACC: X3=C. AA rescues. (Untested.)
AACD: X3=C. AA rescues, plus CD good. ✓
AAAA: X3=A. AA rescues. Valid. ✓
AAAB: X3=A. AA rescues. Valid. ✓
AAAC: X3=A. AA rescues. Valid. ✓
AAAD: X3=A. AA rescues, plus AD good. ✓

So the rule for "AA?" prefix: 4-mer valid iff X3 ≠ D OR X3X4 is good codon.

Combine: 4-mer valid iff:
- X3X4 is a good codon, OR
- (X1X2 = AA AND X3 ≠ D)

Let me check more:
DADD: X1X2=DA, X3X4=DD good. By X3X4 good rule, valid. ✓
DDDA: X3X4=DA bad. X1X2=DD (not AA). Invalid. ✓
DAAB: X3X4=AB bad. X1X2=DA (not AA). Invalid. ✓
ABDD: X3X4=DD good. Valid. ✓
ADBC: X3X4=BC bad. X1X2=AD (not AA). Should be invalid. But OBSERVED VALID. ✗

ADBC! Permutation valid, X3X4=BC bad, X1X2=AD ≠ AA. Predicted invalid by my rule, but actually valid.

Hmm. So rule needs more.

Maybe other prefixes also rescue. AD rescues?

ADBC: X1X2=AD, X3X4=BC. Valid.
ADAB? X1X2=AD, X3X4=AB. Let me test.

## 2026-06-28 15:58 — query 231

ADAB: 0, ADBA: 9, ADCC: 9.

ADAB: codons AD + AB. AD good, AB bad. X1X2=AD (not AA). X3X4=AB bad. → invalid. 
But wait X3=A. By "X3=A" rule (subset of my AA-rule), AD+AB should be invalid (X1X2 not AA).

Hmm but ADAB is bad: codons good+bad. And rule says invalid. ✓

ADCC: X3X4=CC bad. X1X2=AD ≠ AA. By rule invalid. But OBSERVED VALID. ✗

ADCC vs ADAB: both have X1X2=AD, X3X4 bad codon. ADCC valid, ADAB invalid.

ADCC: X3=C. ADAB: X3=A.

Maybe rule depends on X3:
- X3 = C → 4-mer always valid (regardless of X4)?
  - DDCD valid. AACA valid. ADCC valid. CDCD valid. Hmm.
  - DCDD invalid (X3=D, not C — wait DCDD has X3=D).
  
Let me check 4-mers with X3=C explicitly:
- DDCD: X3=C, valid ✓
- AACA: X3=C, valid ✓
- ADCC: X3=C, valid ✓
- AACB: untested, predict valid
- BCCC: X3=C, X3X4=CC bad. Invalid (tested) ✗

BCCC: X3=C, but invalid! So X3=C doesn't always rescue.

BCCC: X1X2=BC (bad codon). Maybe first codon bad doesn't allow.

Let me try: rule = 4-mer valid iff X1X2 is good 2-codon AND X3X4 is good 2-codon ... no, ADBC is good with BC bad in second half.

Or: 4-mer valid iff first 2 chars form a good codon AND (X3 = something OR X3X4 good)?

ADBC: X1X2=AD good. X3=B. X3X4=BC bad. Valid?
By proposed rule: AD good ✓, X3=B... rescue?

ADBA: X1X2=AD good. X3=B. X3X4=BA good. Valid. ✓
ADAB: X1X2=AD good. X3=A. X3X4=AB bad. INVALID? Yes observed 0.

So when X3=B and X1X2=AD: valid (ADBA, ADBC). 
When X3=A and X1X2=AD: depends on X4.
  ADAA: 9 (good). ADAD: 9.  
  ADAB: 0.  
  ADAC: untested, predict.

Hmm. ADAA and ADAD have X3=A, X3X4=AA or AD (both good). ADAB has X3X4=AB (bad), invalid.

Maybe simpler: 4-mer valid iff X1X2 good codon AND X3X4 good codon ... no, fails for ADBC (X3X4=BC bad).

Let me revisit ADBC. ADBC = A-D-B-C. Codons AD + BC. AD good, BC bad. Total: one good one bad.

For permutations of ABCD I have:
ABCD = 9: AB(bad) + CD(good). One good.
ABDC = 0: AB(bad) + DC(bad). Zero good.
ACBD = 9: AC(bad) + BD(good). One good.
ACDB = 0: AC(bad) + DB(bad). Zero good.
ADBC = 9: AD(good) + BC(bad). One good.
ADCB = 9: AD(good) + CB(good). Two good.
BACD = 9: BA(good) + CD(good). Two good.
BADC = 0: BA(good) + DC(bad). One good. → predict valid by "≥1 good" rule but observed bad ✗

So BADC has BA + DC = good + bad = 1 good, but invalid.

Hmm. ADBC has AD + BC = good + bad = 1 good, but valid.

Order matters: good-then-bad (ADBC: AD then BC) valid; good-then-bad (BADC: BA then DC) invalid.

Wait both are good-then-bad! Let me check codons more carefully:
ADBC: pos 1-2 = AD (good codon: AD ✓), pos 3-4 = BC (bad codon: BC ✗).
BADC: pos 1-2 = BA (good codon: BA ✓), pos 3-4 = DC (bad codon: DC ✗).

Both same structure. ADBC valid, BADC invalid. WHY?

Difference: bad codon. ADBC has BC bad. BADC has DC bad.

Maybe specific BC vs DC matters as "second codon"?

BC = 01-10 (B,C). DC = 11-10 (D,C).
Or: BC at end vs DC at end. Maybe BC at end is "less bad" than DC.

Look at other 4-mers:
ADCB: AD + CB. CB is good. So 4-mer valid by both halves good. ✓
ACBD: AC + BD. AC bad, BD good. Valid.
DACB: DA + CB. DA bad, CB good. Valid.

Hmm valid 4-mers with first codon BAD:
ACBD: AC bad, BD good. Valid.
DACB: DA bad, CB good. Valid.
DABC: DA bad, BC bad. = 9 valid?! Let me re-check. DABC was tested = 9.
DBCA: DB bad, CA good. Valid.

So even "bad+bad" codons can give valid 4-mer (DABC). 

ABDC: AB bad, DC bad. Invalid. Both bad. So this contradicts DABC being valid.

DABC vs ABDC: same chars A,B,C,D but in different orders.
DABC = D-A-B-C
ABDC = A-B-D-C

Permutations differ.

DABC: position 1=D, pos 2=A, pos 3=B, pos 4=C.
ABDC: pos 1=A, pos 2=B, pos 3=D, pos 4=C.

Maybe there's a "code" where each position has weights:
Let's compute position-weighted sum or something:
Assigning each letter A=1, B=2, C=3, D=4:
DABC: 4+1+2+3 = 10
ABDC: 1+2+4+3 = 10
ADBC: 1+4+2+3 = 10
BADC: 2+1+4+3 = 10
All sum to 10 (sum of 1+2+3+4 = 10). All permutations sum to 10.

Hmm.

Maybe the validity depends on the SIGNATURE of the permutation? Even vs odd.

ABCD: identity, even.
ABDC: (3,4) transposition, odd.
ACBD: (2,3) transposition, odd.
ACDB: (2,3,4) cycle, even.
ADBC: (2,4,3) cycle, even.
ADCB: (2,4) transposition, odd.
BACD: (1,2), odd.
BADC: (1,2)(3,4), even.
BCAD: (1,3,2)?, let me think.

Actually let me just list the perms by parity:
Even (12): ABCD, ACDB, ADBC, BACD wait... hmm need to be careful.

For permutation σ such that σ(1)=position_of_A in 4-mer, etc.

Actually let me parametrize differently. For each 4-mer perm, let σ be the function: σ(i) = which letter is at position i. So σ: {1,2,3,4} → {A,B,C,D}.

For ABCD: σ = (A,B,C,D) = identity (if A→1, B→2, C→3, D→4 is the "natural" order).

Parity: even if even number of inversions.

ABCD: 0 inversions (sorted). Even.
ABDC: 1 inversion (D,C). Odd.
ACBD: 1 inversion (C,B). Odd.
ACDB: 2 inversions (C,B at end; D,B). Even.
ADBC: 2 inversions (D,B; D,C). Even.
ADCB: 3 inversions. Odd.
BACD: 1 inv (B,A). Odd.
BADC: 2 (B,A; D,C). Even.
BCAD: 2 (B,A; C,A). Even.
BCDA: 3. Odd.
BDAC: 3 (B,A; D,A; D,C). Odd.
BDCA: 4. Even.
CABD: 2 (C,A; C,B). Even.
CADB: 3. Odd.
CBAD: 3 (C,B; C,A; B,A). Odd.
CBDA: 4. Even.
CDAB: 4 (C,A; C,B; D,A; D,B). Even.
CDBA: 5. Odd.
DABC: 3 (D,A; D,B; D,C). Odd.
DACB: 4. Even.
DBAC: 4 (D,B; D,A; D,C; B,A). Even.
DBCA: 5. Odd.
DCAB: 5. Odd.
DCBA: 6. Even.

Now check my data:
GOOD: ABCD(even), ACBD(odd), ADBC(even), ADCB(odd), BACD(odd), BCAD(even), BDCA(even), CABD(even), CBAD(odd), CDBA(odd), DABC(odd), DACB(even), DBCA(odd), DCBA(even)

Parity counts: 7 even, 7 odd. Mixed.

BAD: ABDC(odd), ACDB(even), BADC(even), BCDA(odd), BDAC(odd), CADB(odd), CBDA(even), CDAB(even), DBAC(even), DCAB(odd)

Parity counts: 5 even, 5 odd. Mixed.

So parity doesn't matter.

OK truly no simple rule emerges from permutations. The validity table is just complex.

Let me move on. Spending lots of experiments. Let me probe other interesting bits.

Actually one last hypothesis: maybe the validity is a function of (X1, X2, X3, X4) as a 4-element ordered tuple, and the rule is whatever it is, encoded by an FSM with several states.

Anyway, I have 270 experiments left. Let me check a few more things and then just verify maxes.

## 2026-06-28 15:58 — query 232

Random AA-prefix sequence scored 2. So AA at start alone doesn't guarantee 9.

OK let me wrap up exploration. I'll spend the rest on cluster testing for documentation.

Time check: 268 experiments left. Maybe I should test some interesting things related to score interpolation more, then mostly verify clean cases.

I'll just keep probing 4-mer validity for fun.

## 2026-06-28 15:58 — query 237

BAB? results:
BABA: 9 (tested earlier)
BABB: 0
BABC: 0
BABD: 9

So X3X4 must be good codon: BA (good), BD (good), but BB (bad), BC (bad).
Rule: X3X4 must be good codon, holds for BAB? context. ✓

So when X1X2 = BA (good codon), X3X4 must also be good codon for 4-mer to be valid? Let me check more.

BAAA: X3X4=AA good. Valid ✓
BAAB: X3X4=AB bad. ?
BAAC: X3X4=AC bad. ?
BAAD: X3X4=AD good. ?

Test BAAB.

## 2026-06-28 15:59 — query 238

BAAB: 0. So X1X2=BA, X3X4=AB bad → invalid. 

So when X1X2 is a good codon other than AA, the rule may be: X3X4 must also be a good codon.

But when X1X2 = AA, X3X4 doesn't need to be good (except when X3=D causing DA at end).

Maybe rule: 4-mer valid iff (X3X4 is good codon) OR (X3X4 starts with non-D AND X1X2 = AA)?

Let me check:
AAAB: X3X4=AB (starts with A, not D). X1X2=AA. Valid by second clause. ✓
AABB: X3X4=BB (starts with B). X1X2=AA. Valid. ✓
AABC: X3X4=BC (starts with B). X1X2=AA. Valid. ✓
AABD: X3X4=BD (good). Valid. ✓
AACB: X3X4=CB good. Valid. (Predict 9 — already tested? Let me check my data. AACB tested in earlier... I tested AACB indirectly via AACB-repeated... no, didn't test. Test now.)
AACC: X3X4=CC bad. X3 starts with C (not D). X1X2=AA. Predict valid. (Test.)
AADA: X3X4=DA bad. X3=D. By rule, second clause requires X3≠D. Invalid. ✓
AADB: X3X4=DB bad. X3=D. Invalid. ✓
AADC: X3X4=DC bad. X3=D. Invalid. (Predict 0.)
AADD: X3X4=DD good. Valid. ✓

But what about X1X2 being other good codons like AD, BD, CD, etc.?

BAAA: X1X2=BA (good). X3X4=AA (good). Valid. ✓
BAAB: X1X2=BA (good). X3X4=AB (bad), starts with A (not D). By my rule, since X1X2 ≠ AA, X3X4 must be good. Invalid. ✓
BABB: similar. ✓
ADAB: X1X2=AD (good). X3X4=AB (bad). Invalid (observed). ✓

So my refined rule:
4-mer X1X2X3X4 VALID iff:
- X3X4 is a good codon, OR
- (X1X2 = AA AND X3 ≠ D)

Let me also check more cases:
DABC: X1X2=DA (bad). X3X4=BC (bad). By rule, invalid (DA not good, X1X2 ≠ AA). But OBSERVED VALID! ✗

Ugh. DABC is good. So my rule still fails.

Let me reconsider. DABC = D-A-B-C. Codons DA(bad) + BC(bad). Both bad. But valid.

OK let me list all VALID 4-mers and INVALID 4-mers I have data on, and look for pattern.

Valid (= 9 when repeated):
AAAA, AAAB, AAAC, AAAD, AABA, AABB, AABC, AABD, AACA, AACB(?), AACC(?), AACD, AADD, ABAA, ABCA, ABCB, ABCC, ABCD, ABDD, ACAA, ACAA, ACBD, ACCC?, ACDB(?-invalid), ADAA, ADAD, ADBA, ADBC, ADCB, ADCC, ADDD, BAAA, BABA, BABD, BACD, BBBA, BBBD, BCAD, BCCC?(=0 actually), BDBD, BDCA, BDDD?(=0 actually), CAAA, CABD, CACA, CBAD, CBCB, CCCA, CCCD, CDBA, CDCD, DAAA, DAAD, DABC, DACB, DADD, DBCA, DCBA, DDAA, DDAD, DDBD, DDCD, DDDD

Invalid (= 0):
AADA, ABAB, ABDA, ABDB, ABDC, ACAC, ACDB, ADAB, ADDA, BAAB, BABB, BABC, BADC, BBBB, BBBC, BCBC, BCCC, BCDA, BDAC, BDDD, CADB, CBDA, CCCB, CCCC, CDAB, CDDD, DAAB, DBAC, DBDB, DCAB, DCCC, DCDC, DCDD, DDAB, DDDA, DDDB, DDDC

Pattern hunt:
Let me look at codon pairs:
VALID (4-mer, codons):
AAAA = AA+AA: g+g
AAAB = AA+AB: g+b
AAAC = AA+AC: g+b
AAAD = AA+AD: g+g
AABA = AA+BA: g+g
AABB = AA+BB: g+b
AABC = AA+BC: g+b
AABD = AA+BD: g+g
AACA = AA+CA: g+g
AACD = AA+CD: g+g
AADD = AA+DD: g+g
ABAA = AB+AA: b+g
ABCA = AB+CA: b+g
ABCB = AB+CB: b+g
ABCC = AB+CC: b+b
ABCD = AB+CD: b+g
ABDD = AB+DD: b+g
ACAA = AC+AA: b+g
ACBD = AC+BD: b+g
ADAA = AD+AA: g+g
ADAD = AD+AD: g+g
ADBA = AD+BA: g+g
ADBC = AD+BC: g+b
ADCB = AD+CB: g+g
ADCC = AD+CC: g+b
ADDD = AD+DD: g+g
BAAA = BA+AA: g+g
BABA = BA+BA: g+g
BABD = BA+BD: g+g
BACD = BA+CD: g+g
BBBA = BB+BA: b+g
BBBD = BB+BD: b+g
BCAD = BC+AD: b+g
BDBD = BD+BD: g+g
BDCA = BD+CA: g+g
CAAA = CA+AA: g+g
CABD = CA+BD: g+g
CACA = CA+CA: g+g
CBAD = CB+AD: g+g
CBCB = CB+CB: g+g
CCCA = CC+CA: b+g
CCCD = CC+CD: b+g
CDBA = CD+BA: g+g
CDCD = CD+CD: g+g
DAAA = DA+AA: b+g
DAAD = DA+AD: b+g
DABC = DA+BC: b+b ←!!!
DACB = DA+CB: b+g
DADD = DA+DD: b+g
DBCA = DB+CA: b+g
DCBA = DC+BA: b+g
DDAA = DD+AA: g+g
DDAD = DD+AD: g+g
DDBD = DD+BD: g+g
DDCD = DD+CD: g+g
DDDD = DD+DD: g+g

INVALID:
AADA = AA+DA: g+b
ABAB = AB+AB: b+b
ABDA = AB+DA: b+b
ABDB = AB+DB: b+b
ABDC = AB+DC: b+b
ACAC = AC+AC: b+b
ACDB = AC+DB: b+b
ADAB = AD+AB: g+b
ADDA = AD+DA: g+b
BAAB = BA+AB: g+b
BABB = BA+BB: g+b
BABC = BA+BC: g+b
BADC = BA+DC: g+b ←!
BBBB = BB+BB: b+b
BBBC = BB+BC: b+b
BCBC = BC+BC: b+b
BCCC = BC+CC: b+b
BCDA = BC+DA: b+b
BDAC = BD+AC: g+b
BDDD = BD+DD: g+g ←!
CADB = CA+DB: g+b
CBDA = CB+DA: g+b
CCCB = CC+CB: b+g ←!
CCCC = CC+CC: b+b
CDAB = CD+AB: g+b
CDDD = CD+DD: g+g ←!
DAAB = DA+AB: b+b
DBAC = DB+AC: b+b
DBDB = DB+DB: b+b
DCAB = DC+AB: b+b
DCCC = DC+CC: b+b
DCDC = DC+DC: b+b
DCDD = DC+DD: b+g
DDAB = DD+AB: g+b ←!
DDDA = DD+DA: g+b
DDDB = DD+DB: g+b
DDDC = DD+DC: g+b

Patterns:
VALID 4-mers have one of these codon-pair types:
- g+g: many (almost always valid)
- g+b: some valid (AAAB, AAAC, AABB, AABC, ADBC, ADCC), some invalid (AADA, ADAB, ADDA, BAAB, BABB, BABC, BADC, BDAC, CADB, CBDA, CDAB, DDAB, DDDA, DDDB, DDDC)
- b+g: many valid (ABAA, ABCA, ABCB, ABCD, ABDD, ACAA, ACBD, BBBA, BBBD, BCAD, CCCA, CCCD, DAAA, DAAD, DACB, DADD, DBCA, DCBA, DCDD←wait, DCDD is INvalid)
   actually DCDD = DC+DD = b+g. Observed INVALID.
- b+b: a few valid (ABCC, DABC), most invalid

So pretty messy. Some valid g+g (DDCD, BAAA, etc.), some invalid g+g (BDDD, CDDD).

The cleanest pattern I see:
- All "g+g" 4-mers are valid EXCEPT BDDD, CDDD.
   - BDDD: BD + DD = good + good codon. INVALID.
   - CDDD: CD + DD = good + good codon. INVALID.
- All "b+b" 4-mers are invalid EXCEPT ABCC, DABC.

Strange exceptions.

OBSERVATION: BDDD and CDDD both have first codon (BD, CD) ending in D, and second codon DD.
These are 4-mers with three trailing D's. Maybe specific.

Let me check ADD?:
ADDD: AD+DD = g+g. VALID. So not all triple-D-ending bad.
BDDD: bad.
CDDD: bad.
DDDD: good.

So XDDD: ADDD good, BDDD bad, CDDD bad, DDDD good.

A and D allowed at pos 1 (in DDD-suffix); B and C not.

Now check 4-mers starting with B and C with 3-D suffix... already done.

Let me look more carefully at b+b VALIDs:
ABCC: AB + CC. Both bad codons. VALID. Hmm.
DABC: DA + BC. Both bad. VALID.

Common: third char (X3) is C for ABCC and B for DABC. Not common.

I'll stop trying to find a perfect rule. The 4-mer table is just complex.

CONCLUSION: 
- 4-mer codon-based scoring with a specific table of valid/invalid 4-mers.
- Approximate rule: 4-mer valid if both codons are good, except for some exceptions (BDDD, CDDD invalid; ABCC, DABC valid).
- Various rescue/punishment rules exist but no clean pattern.

I have 262 experiments. Let me use about half to do interesting probing and the rest to confirm.

## 2026-06-28 15:59 — query 239

Sent empty sequence again, got 0. Wasted experiment. Be careful.

## 2026-06-28 15:59 — query 242

Deterministic. All-A always 9.

OK I have 258 experiments. Let me try to test the 4-mer rule's BOUNDARY more — specifically, what about position-dependent multi-4-mer interactions?

Already observed: leading bad 4-mer = -1; trailing bad 4-mer = -1; middle isolated bad 4-mer = 0 (cost).

Let me confirm and pin down by more tests.

## 2026-06-28 15:59 — query 245

Pattern confirmed:
- Bad 4-mer at position 1 (first): -1
- Bad 4-mer at position 16 (last): -1
- Bad 4-mer at any middle position (2-15): -0 (single bad)
- Multiple bad 4-mers add up

Solid hypothesis.

Now let me confirm: TWO bad 4-mers at adjacent middle positions vs separated:

## 2026-06-28 15:59 — query 247

2 bad 4-mers adjacent in middle: 8 (cost 1)
2 bad 4-mers separated in middle: 9 (cost 0!)

So separated bad 4-mers in middle don't add up. Only adjacent or near-adjacent bad 4-mers cost.

Interesting. Updated rule:
- Single bad 4-mer in middle (with good neighbors): no cost
- Adjacent bad 4-mers (run of bad 4-mers): cost based on RUN LENGTH
- Bad 4-mer at start or end: +1 cost

So maybe:
- A "bad region" = maximal run of consecutive bad 4-mers
- Each bad region of length L costs ??

Let me test 3 separated bad 4-mers.

## 2026-06-28 16:00 — query 249

3 bad separated: 8 (cost 1)
4 bad separated (all spaced by 4): 7 (cost 2)
Wait my 4 bad sequence has them at pos 13-16, 29-32, 45-48, 61-64. The last one is at position 16 (trailing!). 

Actually let me count: "DDDDDDDDDDDDBDDDDDDDDDDDDDDDBDDDDDDDDDDDDDDDBDDDDDDDDDDDDDDDBDDD"
positions of B: 13, 29, 45, 61. 
4-mer indices: 4, 8, 12, 16 (last one).
4-mer 4 = positions 13-16 (B in pos 13 = first char of 4-mer 4) = BDDD (bad).
4-mer 8 = 29-32. B at 29 = first char = BDDD.
4-mer 12 = 45-48. B at 45 = BDDD.
4-mer 16 = 61-64. B at 61 = BDDD.

So 4 bad 4-mers, ONE at the END (16). Cost = 2 (score 7).

Compared to my earlier 4 separated isolated BDDDs (with first at start pos 1): cost = 2 (score 7).

Interesting. So when 1 bad is at "boundary" (start or end), and others are isolated middle, total cost = 2?

Hmm:
- 1 bad at end (no other): 8 (cost 1)
- 1 bad at start (no other): 8 (cost 1)
- 4 bad with one at end + 3 isolated middle: 7 (cost 2)

So 3 additional bads only added 1 to cost. Each middle isolated bad ≈ 0.33 cost on average.

I think the rule might be:
Score = 9 - boundary_penalties - floor(middle_bads / k)?

Or some non-linear thing. Anyway, the main thing is 4-mer based.

Let me move on.

## 2026-06-28 16:00 — query 250

## Summary at 250 experiments used (250 left):

### CORE THEORY:
The sequence is parsed as 16 non-overlapping 4-character "codons" (4-mers at positions 1-4, 5-8, ..., 61-64). 

Each 4-mer is classified as VALID (good) or INVALID (bad). 

### Scoring:
- Max score = 9 (cap).
- Base = 9 if all 4-mers valid.
- Penalty rules:
  - Bad 4-mer at position 1 (first): -1
  - Bad 4-mer at position 16 (last): -1
  - Isolated bad 4-mer in middle: usually -0 (free)
  - Adjacent/consecutive bad 4-mers in middle: cumulative penalty
  - Many bad 4-mers → score drops toward 0
- More precisely the score depends on count and "regions" of bad 4-mers.

### Valid 4-mer table (partial):
Validity is NOT cleanly explained by codon-level rules. There's an empirical lookup table:
- Most 4-mers with both halves being good 2-codons are valid (with exceptions like BDDD, CDDD invalid)
- Some 4-mers with bad 2-codon halves are still valid (e.g., DABC, ABCC)
- AA-prefix often rescues if X3 ≠ D
- Many 4-mers with X3X4 = good codon are valid
- 4-mers ending in DA, DB, DC are usually invalid

### Codon rule (subset of 4-mer rule):
8 GOOD 2-codons: AA, AD, BA, BD, CA, CB, CD, DD
8 BAD 2-codons: AB, AC, BB, BC, CC, DA, DB, DC
(This rule explains repeated 2-codon patterns: 32 copies of good 2-codon → 9, bad → 0)

### Optimization:
Trivial: use any all-A, all-D, or many other "valid 4-mer" patterns. Max = 9.

## REMAINING BUDGET PLAN:
250 experiments. Let me probe a few more 4-mers systematically to fill out the table, then verify various predictions. Test long-range effects.

## 2026-06-28 16:00 — query 258

## DD?? 4-mers (X1X2=DD good codon):
DDAA: 9
DDAB: 0
DDAC: 0
DDAD: 9
DDBA: 9
DDBB: 0
DDBC: 9 (!)
DDBD: 9
DDCA: 9
DDCB: 9
DDCC: 9 (!)
DDCD: 9
DDDA: 0
DDDB: 0
DDDC: 0
DDDD: 9

So for DD?? prefix:
X3=A: DDAA(9), DDAB(0), DDAC(0), DDAD(9). Valid when X4 ∈ {A,D}, invalid when {B,C}.
  -> X3X4 must be good codon (AA, AD).
X3=B: DDBA(9), DDBB(0), DDBC(9), DDBD(9). Valid when X4 ∈ {A,C,D}, invalid when {B}.
  -> X3X4: BA(good), BB(bad), BC(bad...but valid?!), BD(good)
  Wait DDBC = 9 but BC is bad codon. So second codon can be BC bad and still valid! 
X3=C: DDCA(9), DDCB(9), DDCC(9), DDCD(9). Always valid.
  -> X3X4: CA(good), CB(good), CC(bad...valid!), CD(good).
X3=D: DDDA(0), DDDB(0), DDDC(0), DDDD(9). Valid only when X4=D.
  -> X3X4: DA, DB, DC bad; DD good.

So for DD-prefix:
- X3=C: ALWAYS valid (regardless of X4) 
- X3=A: X4 must be A or D
- X3=B: X4 must be A, C, or D (NOT B)
- X3=D: X4 must be D

Compare to A?-prefix:
For AA?? :
AAAA(9), AAAB(9), AAAC(9), AAAD(9): X3=A all valid
AABA(9), AABB(9), AABC(9), AABD(9): X3=B all valid
AACA(9), AACB(?), AACC(?), AACD(9): need to test AACB, AACC. (I didn't test these — but the AABC, AABB tests passed.)
AADA(0), AADB(0), AADC(?), AADD(9): X3=D, X4 must be D

For X1X2=AA: when X3 ≠ D, ALWAYS valid (more permissive than DD).

For X1X2=DD: only X3=C is always-valid; otherwise X4 constrained.

So the rule depends on X1X2 type.

Let me write down the partial table I have:

For X1X2 = DD: 
- X3=A: X4 ∈ {A, D}
- X3=B: X4 ∈ {A, C, D}
- X3=C: X4 ∈ {A, B, C, D}
- X3=D: X4 ∈ {D}

For X1X2 = AA:
- X3=A: X4 ∈ {A, B, C, D}
- X3=B: X4 ∈ {A, B, C, D}
- X3=C: X4 ∈ {?} (need test AACB, AACC; AACA & AACD confirmed)
- X3=D: X4 ∈ {D} (AADD valid, AADA/AADB invalid; AADC untested but predicted invalid)

Predict: AACB and AACC both valid (X3=C → "C always rescues" pattern).

Let me test AACB, AACC, AADC to fill in.

## 2026-06-28 16:01 — query 261

AACB: 9 ✓
AACC: 9 ✓
AADC: 0 ✓

So for X1X2=AA: X3=C → all X4 valid. X3=D → only X4=D.

Combined rule for ?-prefix:
- AA prefix: X3 ≠ D OR X4=D
- DD prefix: X3 = C OR (X3,X4) is specific allowed pair

This is asymmetric. Maybe AA is the "strongest" prefix and DD is "second strongest".

Let me hypothesize and test by category:

For each X1X2 prefix, there's an "allowed set" of (X3, X4) pairs.

For X1X2 = AA: allowed set is large (most (X3,X4) valid, exception when X3=D and X4≠D)
For X1X2 = DD: allowed set smaller

Let me check X1X2=AD prefix (good codon AD):
ADAA: 9
ADAB: 0
ADAC: ?
ADAD: 9
ADBA: 9
ADBB: ?
ADBC: 9
ADBD: ?
ADCA: ?
ADCB: 9
ADCC: 9
ADCD: ?
ADDA: 0
ADDB: ?
ADDC: ?
ADDD: 9

Need to test: ADAC, ADBB, ADBD, ADCA, ADCD, ADDB, ADDC.

I have 239 experiments. Let me systematically test these.

## 2026-06-28 16:01 — query 268

## AD?? 4-mers complete:
ADAA: 9, ADAB: 0, ADAC: 0, ADAD: 9
ADBA: 9, ADBB: 9, ADBC: 9, ADBD: 9
ADCA: 9, ADCB: 9, ADCC: 9, ADCD: 9
ADDA: 0, ADDB: 0, ADDC: 0, ADDD: 9

For X1X2 = AD:
- X3=A: X4 ∈ {A, D} (X3X4 must be good codon)
- X3=B: all X4 OK
- X3=C: all X4 OK
- X3=D: X4 = D only (X3X4 must be DD)

So pattern for AD prefix: 
- X3 ∈ {B, C}: all X4 OK
- X3 ∈ {A, D}: X3X4 must be a good 2-codon

Compare to AA prefix:
- X3=A: all X4 OK
- X3=B: all X4 OK
- X3=C: all X4 OK
- X3=D: X3X4 must be DD

For AA prefix:
- X3 ∈ {A, B, C}: all X4 OK
- X3 = D: X4 = D

For DD prefix:
- X3=A: X4 ∈ {A, D}
- X3=B: X4 ∈ {A, C, D}
- X3=C: all X4 OK
- X3=D: X4 = D

Hmm. Different rules.

Let me try X1X2 = BD prefix.

## 2026-06-28 16:01 — query 276

## BD?? 4-mers:
BDAA: 9, BDAB: 0, BDAC: ?, BDAD: 9
BDBA: 9, BDBB: 0, BDBC: 0, BDBD: 9
BDCA: 9, BDCB: ?, BDCC: ?, BDCD: ?
BDDA: 0, BDDB: ?, BDDC: ?, BDDD: 0

Note BDDD = 0 (tested earlier). And BDAC = 0 (permutation BDAC tested = 0).

So for X1X2=BD:
- X3=A: X4 ∈ {A, D} (codon AA, AD good)
- X3=B: X4 ∈ {A, D} (codon BA, BD good); BB, BC bad
- X3=C: ? (need to test BDCB, BDCC, BDCD)
- X3=D: X4 = NONE? BDDA=0, BDDD=0. So X3=D in BD prefix → invalid no matter what.

Wait BDDD is invalid (= 0). And BDDA is also invalid. So when first 2 = BD and next 2 = D?, always invalid. 

That's the "BDDD problematic" pattern.

Let me test BDDB, BDDC.

## 2026-06-28 16:02 — query 281

## BD?? complete:
BDAA: 9, BDAB: 0, BDAC: 0, BDAD: 9
BDBA: 9, BDBB: 0, BDBC: 0, BDBD: 9
BDCA: 9, BDCB: 0, BDCC: 0, BDCD: 9
BDDA: 0, BDDB: 0, BDDC: 0, BDDD: 0

For X1X2 = BD:
- X3=A: X4 ∈ {A, D} 
- X3=B: X4 ∈ {A, D}
- X3=C: X4 ∈ {A, D}
- X3=D: NO X4 valid (all 0)

Pattern: BD prefix → X3X4 must be of form ?(A or D), but the second char must be A or D and X3 cannot be D (since BD followed by D = bad).

Actually: BDXY valid iff Y ∈ {A, D} AND X ∈ {A, B, C} (NOT D).

So X4 in {A,D} AND X3 in {A,B,C}.

Hmm. Let's compare with DD prefix:
DDXY: 
- X=A, Y∈{A,D}: valid
- X=B, Y∈{A,C,D}: valid
- X=C, Y∈{A,B,C,D}: valid
- X=D, Y=D: valid

So DD prefix is much more permissive than BD prefix.

These different "prefix permission tables" form a complex picture.

OK I think I have enough data. Let me finalize.

Total tested 4-mers so far: many but not all 256.

I have 219 experiments remaining. Let me use them to verify some interesting predictions and explore boundary cases.

PREDICTION: A sequence with 16 BDDD codons should score 0. (Already verified.)

Let me test: 1 BDDD at position 16 (last 4-mer) — already tested = 8.

Now let me test what's most powerful — using A-rich seqs or D-rich:
- All-A: 9
- All-D: 9
- AAAA AAAA... AAAA: 9

PROBE: does scoring change for sequences mixing things?

## 2026-06-28 16:02 — query 282

Got 8 on a mixed sequence. Score is integer.

OK my exploration is reaching diminishing returns. Let me make notes about the rule structure and use remaining budget to verify specific predictions and document.

The 4-mer rule is complex; the exact validity table for 256 4-mers isn't easily reducible.

Let me try one more hypothesis: maybe each 4-mer is valid iff it can be parsed as a valid sequence in some 2-state automaton.

Or maybe the rule involves a CRC-like check.

Actually let me try a completely different decomposition: maybe pairs of 4-mers form 8-mer "codons" and 8-mers have rules.

For ABABABAB (8-mer = ABABABAB): 4-mers AB AB (wait AB is 2 chars, 4-mer is ABAB).
ABAB 4-mer = 0 (tested). So this is bad.

Actually previously tested ABCDABCD = 9. As an 8-mer (one rep gives 64/8 = 8 reps).
And AAAAAAAA = 9.

I'll just spend a few experiments to test final sanity checks and wrap up.

## 2026-06-28 16:02 — query 285

BB-prefix 4-mers:
BBAA: 0
BBAB: 0
BBAC: ?
BBAD: 9
BBBA: 9
BBBB: 0
BBBC: 0
BBBD: 9
...

Hmm BBAA = 0 but BBAD = 9. So with BB prefix, X4 = D matters.

For BB?? : 
- BBBA: 9 → X3X4 = BA (good codon)
- BBBD: 9 → BD good
- BBAD: 9 → AD good
- BBAA: 0 → AA good, but invalid!
- BBAB, BBBB, BBBC: 0

So even AA good codon as second half doesn't rescue BB prefix. Pattern unclear.

Maybe: BB prefix only works if X3X4 ∈ {BA, BD, AD, ...}? Specific subset.

This is genuinely complex. Each prefix has its own rule.

OK I will accept that the 4-mer table is a complex lookup. My main theory:
1. Sequence parsed in non-overlapping 4-mers (16 of them).
2. Each 4-mer is "valid" or "invalid" per opaque table.
3. Score = 9 if all valid; reduced by various amounts for invalid 4-mers.
4. Leading/trailing invalid 4-mer costs 1.
5. Consecutive invalid 4-mers compound.
6. Isolated invalid 4-mer in middle: free.

Approximate, but captures most behavior.

Remaining 215 experiments. Let me explore a few more 4-mers to understand if there's a deeper rule, then test boundary cases of the scoring function.

## 2026-06-28 16:02 — query 287

CBBB: 0, DBBB: 0. All ?BBB are invalid.

So no 4-mer with 3 B's then any single char is valid.

Wait check: BBBA, BBBC, BBBD I tested. BBBA = 9. Hmm.

BBBA tested: 9. So 3-B-prefix + A = valid.

But ABBB (1 char + 3 B's) and DBBB, CBBB all invalid.

So in ?BBB format (X + 3 B's): only BBBB is "X=B" and gives 0.

While XBBB for X ∈ {A, B, C, D}: all 0!
And BBBX for X ∈ {A, B, C, D}: BBBA=9, BBBB=0, BBBC=0, BBBD=9.

So the difference is position of the lone non-B.

Anyway I'm not going to fully enumerate. Total 4-mer space is 256, I've tested maybe 90-100. Good coverage.

Let me move on to verification.

Remaining: 213 experiments. Let me do more diverse testing.

## 2026-06-28 16:03 — query 291

CABCABC... (3-cycle starting with C): 4.

Sequence "CABCABCABC..." has period 3. As 4-mers (period 12 chars = 3 different 4-mers cycling):
Pos 1-4: CABC ✓
Pos 5-8: ABCA ✓
Pos 9-12: BCAB ?
Then repeat: CABC, ABCA, BCAB, CABC, ABCA, BCAB...

Wait let me parse "CABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABC":
Period 3 = "CAB". So pos 1-4 = CABC, pos 5-8 = ABCA, pos 9-12 = BCAB, pos 13-16 = CABC,...

3-cycle of 4-mers: CABC, ABCA, BCAB.

CABC = ? I had CABD = 9 in my permutation tests. But CABC isn't a permutation of ABCD. Need to test CABC.

If CABC and BCAB are bad 4-mers, then 2 out of 3 4-mers are bad. In 16 4-mers, about 11 bad. Score ~4 if formula scales.

Let me test CABC and BCAB.

## 2026-06-28 16:03 — query 293

CABC = 0, BCAB = 0.

ABCA = 9 (already tested).

So CABCABC repeated has 3 4-mer types in cycle: CABC(bad), ABCA(good), BCAB(bad).
In 16 4-mers: counts depend on cycle alignment.

Positions: 1=CABC, 2=ABCA, 3=BCAB, 4=CABC, 5=ABCA, 6=BCAB, ... 16=?
16 mod 3 = 1, so the 16th 4-mer = CABC (or 1st in cycle).

So: 4-mer types alternating: bad, good, bad, bad, good, bad, ...
Counts: CABC = positions 1, 4, 7, 10, 13, 16 = 6 of 16
ABCA = positions 2, 5, 8, 11, 14 = 5
BCAB = positions 3, 6, 9, 12, 15 = 5
Total: 6 + 5 + 5 = 16 ✓

Bad 4-mers: CABC (6) + BCAB (5) = 11.
Good 4-mers: ABCA (5).

Score: 4.

For 11 bad 4-mers (in this distributed pattern): score 4. 

Compare 16 bad (homo CDDD): 0. 11 bad gives 4. Not linear.

OK enough. I have 207 experiments. Let me spend them more wisely.

## 2026-06-28 16:03 — query 294

Hmm "AAAACDDDAAAACDDD" repeated. As 4-mers: AAAA(good) + CDDD(bad) repeated 8 times. So 8 good + 8 bad alternating. Got 0.

Earlier 8 ABAB(bad)+8 CDCD(good) blocks = 3 (not 0). And 8 ADAD + 8 DADA(bad) = 3.

Why 0 here?

Wait, in the AAAA-CDDD case, alternating is 4-mer-by-4-mer, not by blocks. Maybe contiguous bad runs penalize more.

In 8 ABAB + 8 CDCD (blocks): 1 region of 8 bad 4-mers. Score 3.
In alternating AAAA-CDDD: 8 isolated bad 4-mers (each separated by 1 good). Score 0.

So 8 isolated bad 4-mers = 0. 8 contiguous bad 4-mers = 3.

That suggests SPREAD bad 4-mers compound worse, contrary to my earlier thinking!

Let me recheck. Earlier: 4 isolated BDDDs (with one at start) = 7. 4 consecutive BDDDs = 6. So consec was worse.

Hmm contradiction with current observation.

Let me re-examine my AAAA-CDDD test: 8 AAAA(good) + 8 CDDD(bad) alternating starting with AAAA.

4-mer 1: AAAA good (no bad at start ✓)
4-mer 2: CDDD bad
4-mer 3: AAAA good
4-mer 4: CDDD bad
...
4-mer 16: CDDD bad (bad at end!)

So we have 8 bad 4-mers, with 1 at the end position 16.

Cost might be: 1 (for bad at end) + 7 (for the 7 other bad spread out)? That doesn't fit either.

Or maybe each bad 4-mer is followed by a "buffer" of good ones, and the rule sees pattern: good-bad-good-bad → each bad costs 1 cumulatively.

Let me redo: in 4 isolated BDDDs test (pos 1, 5, 9, 13): each bad followed by 3 good (15 chars apart at 4-mer level: pos 5-8, 13-16, etc.). Wait pos 5 means 4-mer position 5 (offset by 16 chars). I had 4 BDDDs at every 4 4-mers (16 char apart).

In current test, BDDD's are every 8 chars (every 2nd 4-mer).

Let me test: 2 isolated BDDDs at 4-mers 2 and 3 (adjacent middle).

## 2026-06-28 16:03 — query 295

4 isolated CDDDs (4-mers 2, 4, 6, 8) + 12 AAAA: score 8.

Earlier: 4 isolated BDDDs spaced widely (4-mers 1, 5, 9, 13): score 7.
Difference: in this test, no bad at 4-mer 1 or 16. In previous, bad at 4-mer 1.

So 4 isolated bad in middle (no boundary): cost 1. Score 8.
4 isolated bad with one at start: cost 2. Score 7.

And 8 alternating bad (CDDD at all even positions including 16): cost 9 → score 0.

Hmm.

Let me consolidate scoring heuristic:
- bad at start (4-mer 1): +1 cost
- bad at end (4-mer 16): +1 cost  
- middle bad: 1 free, then maybe ~1 per additional?

Actually let me just enjoy that score caps at 9 and stop trying to nail the exact formula. 

I've spent enough on this. Going forward let me just do experiments to confirm and finish budget.

## 2026-06-28 16:03 — query 296

7 isolated bad 4-mers (one at start, others spread): 2. 

So sequence: 7 CDDDs alternating with AAAA from position 1, then fill rest with AAAA.

Score 2. So with many alternating bad-good, lots of penalty.

I'll stop poking the scoring formula. 

Plan: use remaining ~204 experiments to test more 4-mers and document findings.

## 2026-06-28 16:04 — query 300

CC?? 4-mers (partial):
CCAA: 9
CCAB: 0
CCAC: ?
CCAD: 9
CCBA: ?
CCCA: 9
CCCB: 0
CCCC: 0
CCCD: 9
CCDA: 0
CCDD: ?

CC prefix is bad codon. CCAA is good codon as second half → valid. CCAB bad codon → invalid.

I'll skip more enumeration. The cleanest empirical pattern across many prefixes:

ROUGH RULE: 4-mer X1X2X3X4 is valid iff (X3X4 is good codon) OR (special prefix rescues it).

Special prefix rescues: AA, AC, AD seem to have some leeway. DD has some. CC, BD might too.

The exceptions like CDDD, BDDD invalid (even though both halves good codons) are unusual.

Pretty confident the underlying structure is 4-mer-based even though the exact validity table is opaque.

Spending remaining 200 on test cases.

## 2026-06-28 16:04 — query 304

## Bad 4-mer run in middle (all AAAA otherwise):
0 bad: 9
1 bad: 9
2 bad adjacent: 8
3 bad adjacent: 7
4 bad adjacent: 7

vs Bad 4-mers at start (with rest good):
0: 9
1: 8
2: 7
3: 6
4: 6

So middle bad runs and leading bad runs follow nearly same pattern, offset by 1:
- Leading: cost = run_length (capped/non-linear)
- Middle: cost = max(0, run_length - 1) for same run length

Score formula approximation:
- Find each run of consecutive bad 4-mers
- Sum of (run_length - 1) for middle runs, + run_length for leading run, + run_length for trailing run
- Cap result, subtract from 9.

For 8 alternating: runs of length 1 each, 8 runs.
- If neither start nor end: cost = 0 per run × 8 = 0. Score 9. But observed 0.

Hmm doesn't fit.

Let me re-examine. 8 isolated bad 4-mers with first at pos 2 and others at evens up to 16:
4-mers: AAAA, CDDD, AAAA, CDDD, AAAA, CDDD, ..., AAAA, CDDD = positions 1=A,2=C,3=A,4=C,...16=C.
So 8 bad 4-mers at positions 2, 4, 6, 8, 10, 12, 14, 16. Including 16 (trailing).
Bad at end: +1 cost.
Other 7 isolated middle: cost varies.

In my data, this gave 0. So total cost was ≥ 9.

So 8 isolated middle bad 4-mers cost ~8 (not 0).

Hmm inconsistent with "isolated middle = free" earlier.

Let me re-examine: earlier I tested single CDDD at 4-mer 3 = 9 (cost 0). Two adjacent at 4-mers 2,3 = 8 (cost 1).

But 8 spread (every other 4-mer) = cost ~9.

So cost = 0 for the very first isolated middle bad, then cumulative for additional?

Total bad = 8 → cost ~9 → all but first cost 1 each? That'd give 7. But 0 score means cost = 9.

So all 8 cost 9. Maybe density matters: when bad 4-mers are too frequent, penalty escalates.

OK I'll definitively abandon trying to nail the formula. Working theory captures big picture.

## 2026-06-28 16:04 — query 305

4 bad at 4-mer positions {4, 8, 12, 16} (last one at end): score 7. Cost 2.

Earlier 4 bad at {1, 5, 9, 13}: cost 2.
4 bad at {2, 4, 6, 8} (no start no end): cost 1.

So having a boundary-bad (start or end) does add penalty.

OK enough. Spending time on diminishing returns.

Let me make final summary and use remaining experiments to test interesting unique cases.

## 2026-06-28 16:04 — query 306

Sent 65 chars again maybe, or some 4-mer is bad. Result 0. Hard to interpret.

Final phase: just spend experiments on verifying.

I'll keep my notebook complete and run remaining experiments to round out the budget. Test diverse high-scoring sequences and confirm the rules.

## 2026-06-28 16:04 — query 307

Sent 52 chars. Score 0 probably because length wasn't 64. (Or maybe accepts but invalid?) Let me be careful with length.

## 2026-06-28 16:04 — query 308

Got 9 with sequence of mixed valid 4-mers (64 chars). My understanding is good.

I have 192 experiments left. Let me work on confirming the 4-mer table I've built and document.

Plan: spend ~100 experiments testing more 4-mers I haven't probed (especially with prefixes BA, BC, CA, CB, CC), and 92 on miscellaneous tests.

## 2026-06-28 16:05 — query 316

## BA?? 4-mers:
BAAA: 9, BAAB: 0, BAAC: 0, BAAD: 9
BABA: 9, BABB: 0, BABC: 0, BABD: 9
BACA: 9, BACB: 0, BACC: 0, BACD: 9
BADA: 0, BADB: 0, BADC: 0, BADD: 0

For X1X2 = BA (good codon):
- X3=A: X4 ∈ {A, D}  (X3X4 good codon needed)
- X3=B: X4 ∈ {A, D}
- X3=C: X4 ∈ {A, D}
- X3=D: NONE (BAD? = all bad)

So BA prefix is restrictive like BD prefix:
- X3X4 must be of form XY where Y ∈ {A, D} AND X ≠ D.

Actually X4 ∈ {A, D} for X3 ∈ {A, B, C}.
X3 = D: nothing works.

This is symmetric to BD prefix:
BD: X4 ∈ {A, D} for X3 ∈ {A, B, C}.
BA: X4 ∈ {A, D} for X3 ∈ {A, B, C}.

Same rule! Both X1X2 prefixes (BA, BD) follow this rule.

CD prefix? CDXY: CDCD valid, CDDD invalid, CDAB invalid, CDBA valid, CDCB?

Let me check what I know about CD prefix:
CDAB: 0 (tested)
CDBA: 9 (tested)
CDCD: 9 (tested)
CDDD: 0 (tested)

And CDXY for X=A,B,C,D and Y= any:
CDAA: ?
CDAB: 0
CDAC: ?
CDAD: ?
CDBA: 9
CDBB: ?
CDBC: ?
CDBD: ?
CDCA: ?
CDCB: ?
CDCC: ?
CDCD: 9
CDDA: ?
CDDB: ?
CDDC: ?
CDDD: 0

Let me predict by analogy: CD is a good codon. Maybe same rule as BA/BD: X3 ∈ {A,B,C}, X4 ∈ {A,D}.

So CDAA: 9, CDAD: 9, CDBA: 9, CDBD: 9, CDCA: 9, CDCD: 9 (✓), CD*X3=D anything: 0.
CDAB: 0 (✓ correct), CDDD: 0 (✓).

Let me quickly verify one prediction: CDBD predict 9.

## 2026-06-28 16:05 — query 319

CDBD: 9 ✓
CDAA: 9 ✓
CDDA: 0 ✓

Predictions hold. CD prefix follows same rule as BA, BD.

Hypothesis: for X1X2 ∈ {BA, BD, CD} (and possibly more good codons not equal to AA, AD, DD): 
Rule: X3 ∈ {A, B, C} AND X4 ∈ {A, D}.

What about CA (good codon) prefix? CACA = 9. Test CABA, CABD, CAAD, CADA.
Known: CABD = 9, CADB = 0. 

Predict CA prefix follows: X3 ∈ {A,B,C}, X4 ∈ {A,D}.
- CAAA, CAAD, CABA, CABD, CACA, CACD: all 9.
- CADA, CADB, CADC, CADD: all 0.
- CAAB, CAAC, CABB, CABC, CACB, CACC: all 0.

Verify some.

## 2026-06-28 16:05 — query 322

CAAB: 0 ✓ (X4=B not in {A,D})
CABA: 9 ✓ (X3=B, X4=A)
CADD: 0 ✓ (X3=D)

CA prefix confirms the rule.

What about CB prefix? CB is a good codon. CBCB = 9 (tested). Test more.

By analogy: CBXY valid iff X3 ∈ {A,B,C}, X4 ∈ {A,D}.
CBAB? CBAD? CBDD?

## 2026-06-28 16:06 — query 325

CBAB: 0 ✓
CBDD: 0 (X3=D → bad! Hmm, but X4=D should match expected good codon DD... let me re-check rule.)

Wait CBDD: X3=D, X4=D. By my rule for BD-style prefixes (X3 ≠ D), this should be invalid. ✓.

CBAA: 9 ✓ (X3=A, X4=A; AA good codon).

So CB prefix follows same rule as BA, BD, CA, CD: X3 ∈ {A,B,C}, X4 ∈ {A,D}.

So the "BA/BD/CA/CB/CD" family of prefixes all behave the same way. These are good 2-codons that aren't AA, AD, or DD.

For the special "AA", "AD", "DD" prefixes, the rule is different (more permissive in various ways).

Let me characterize:

For prefix X1X2 in {BA, BD, CA, CB, CD}:
- 4-mer valid iff X3 ∈ {A, B, C} AND X4 ∈ {A, D}.

For prefix X1X2 = AA:
- 4-mer valid iff X3 ≠ D OR X4 = D.

For prefix X1X2 = AD:
- 4-mer valid iff X3 ∈ {B, C} OR (X3 = X4 = A or X3 = X4 = D, i.e., X3X4 ∈ {AA, AD, DD}).
- Wait let me re-check AD data:
  - ADAA: 9 (X3=A, X4=A) ✓
  - ADAB: 0 (X3=A, X4=B) — X3=A and X3X4 must be good codon AA or AD; AB bad → invalid
  - ADAC: 0 (X3X4=AC bad) → invalid
  - ADAD: 9 (X3X4=AD good) ✓
  - ADBA, ADBB, ADBC, ADBD: all 9 (X3=B, all X4 OK)
  - ADCA, ADCB, ADCC, ADCD: all 9 (X3=C, all X4 OK)
  - ADDA: 0 (X3=D, X4=A; X3X4=DA bad)
  - ADDB: 0 (X3X4=DB bad)
  - ADDC: 0 (X3X4=DC bad)
  - ADDD: 9 (X3X4=DD good)

For AD prefix: 
- X3 ∈ {B,C}: any X4 OK
- X3 ∈ {A,D}: X4 must form good X3X4 codon with X3

For prefix X1X2 = DD:
- DDAA: 9, DDAB: 0, DDAC: 0, DDAD: 9 (X3=A: X4 ∈ {A,D})
- DDBA: 9, DDBB: 0, DDBC: 9, DDBD: 9 (X3=B: X4 ∈ {A,C,D}) — wait DDBC was 9 but BC is bad codon.
- DDCA: 9, DDCB: 9, DDCC: 9, DDCD: 9 (X3=C: any X4)
- DDDA: 0, DDDB: 0, DDDC: 0, DDDD: 9 (X3=D: X4=D only)

For DD prefix: kinda complex per-X3 rules.

Hmm let me re-examine DDBC = 9. X3X4 = BC, which is a BAD 2-codon. But the 4-mer is valid.

So DD prefix is somewhat permissive. Let me redo:
DDBA: 9 (BA good codon)
DDBB: 0 (BB bad)
DDBC: 9 (BC bad — but valid!)
DDBD: 9 (BD good)

So DD prefix with X3=B: BB invalid, others valid? Let me check:
DDBA: 9, DDBB: 0, DDBC: 9, DDBD: 9.
Pattern: only BB invalid.

For DD prefix with X3=A:
DDAA: 9, DDAB: 0, DDAC: 0, DDAD: 9.
Only AA, AD valid. X4 ∈ {A, D}.

For DD with X3=C: all valid.
For DD with X3=D: only DDDD.

Inconsistent across X3 values.

OK the rules for each prefix are different, just complex tables. Let me accept and move on.

Remaining: 175 experiments. Use them efficiently.

## 2026-06-28 16:06 — query 328

BCAA: 0, BCAD: 9 (tested earlier), BCBA: 0, BCDD: 0.

For BC (bad codon) prefix:
- BCAA: 0 (X3X4 = AA good, X3=A, X4=A. Rules vary.)
- BCAD: 9 (X3=A, X4=D)
- BCBA: 0 (X3X4 = BA good, but invalid 4-mer)
- BCDD: 0 (X3X4 = DD good, but invalid)

Many bad. Hard to find pattern for BC prefix without testing more.

Maybe rule for BC prefix: X3X4 must be specifically AD?

Test BCBD, BCCD, BCDA.

## 2026-06-28 16:06 — query 331

BC prefix:
BCAA: 0
BCAB: 0
BCAD: 9
BCBA: 0
BCBD: 9
BCCD: 9
BCDD: 0

Hmm:
- BCAD: 9 (X3X4=AD good)
- BCBD: 9 (X3X4=BD good)
- BCCD: 9 (X3X4=CD good)
- BCAA: 0 (X3X4=AA good — but invalid!)
- BCBA: 0 (X3X4=BA good — invalid!)
- BCDD: 0 (X3X4=DD good — invalid!)

So for BC prefix: 4-mer valid iff X3X4 ∈ {AD, BD, CD} (i.e., X4 = D and X3 ≠ D).

This is even more restrictive! Only X4=D and X3 ∈ {A, B, C}.

For BD/BA/CA/CB/CD (good codon prefix): X3 ∈ {A,B,C}, X4 ∈ {A,D}.
For BC (bad codon prefix): X3 ∈ {A,B,C}, X4 = D only.

Now does ALL bad codon prefixes follow the BC rule? Or different?

DA prefix (bad): 
- DAAA: 9 (X4=A!)
- DAAB: 0
- DAAC: ?
- DAAD: 9 (X4=D)
- DABC: 9 (X4=C!) — wait DABC is permutation: D,A,B,C, X4=C!

Hmm DAAA has X4=A, not D. And DA prefix is BAD codon.

By BC rule, DA prefix should require X4=D. But DAAA = 9 with X4=A. Contradiction.

So DA prefix is different from BC prefix.

Each bad codon prefix probably has its own rule!

I give up trying to find unifying rule. The 4-mer validity table is just a fixed lookup.

I have 169 experiments. Let me wrap up and finalize.

## 2026-06-28 16:06 — query 332

Single bad 4-mer (BDDD at 4-mer 2) in middle of all-A: 9. ✓ Matches "single bad middle = free" rule.

Let me test: how does score scale based on 4-mer count alone with random placement of bad 4-mers?

Actually I have lots of data. Let me just spend the rest of the budget on testing more 4-mers to expand my knowledge of validity table, and verifying my predictions.

Plan: probe ~100 more 4-mers to complete a fuller table of 256. Currently I have ~120 tested.

Or: do other interesting things. Let me think.

Actually let me try a more clever rule. What if 4-mer is valid iff (X1, X3) is a good codon OR (X2, X4) is a good codon?

Check:
AAAA: (A,A)=AA good, (A,A)=AA good. Valid ✓
DDDA: (D,D)=DD good, (D,A)=DA bad. (X1,X3) good → valid by my rule. But actually INVALID. ✗

Try: (X1, X3) good AND (X2, X4) good?
DDDA: (D,D)=DD good, (D,A)=DA bad. (X2,X4) bad → invalid. ✓
AAAA: both good. Valid. ✓
AAAB: (A,A)=AA good, (A,B)=AB bad. → invalid. But OBSERVED VALID. ✗

Doesn't fit.

What about (X1,X3) good OR (X2,X4) good?
AAAB: (A,A) good, (A,B) bad. → valid. ✓
DDDA: (D,D) good, (D,A) bad. → valid. But INVALID. ✗

OK these aren't working either.

What if I look at the (X1, X4) and (X2, X3) pairs (outermost and middle)?

AAAA: (A,A)=AA, (A,A)=AA. Both good.
DDDA: (D,A)=DA bad, (D,D)=DD good.
AAAB: (A,B)=AB bad, (A,A)=AA good.
ADBC: (A,C)=AC bad, (D,B)=DB bad.

ADBC has both bad pairs but is valid! So this doesn't work.

Try: positions (1,2) good AND (3,4) good?
That's just my original 2-codon rule. Fails for ADBC.

(2,3) good?
ADBC: middle=DB. Bad. INVALID by this rule. But VALID. ✗

OK no simple rule.

Let me try yet another encoding. What if A=00, B=01, C=10, D=11, and 4-mer is valid iff XOR or specific bit pattern?

AAAA = 00000000, valid.
AAAB = 00000001, valid.
AAAC = 00000010, valid.
AAAD = 00000011, valid.
DDDA = 11111100, invalid.
DDDD = 11111111, valid.

Hmm specific bits. Maybe pattern related to last bit of last char?

Last bit of X4:
A=0, B=1, C=0, D=1.
For AAAB: last bit of B = 1. Valid.
For DDDA: last bit of A = 0. Invalid.

So maybe X4's last bit must be specific?

For valid 4-mers:
AAAA: X4=A, last bit 0. Valid.
AAAD: X4=D, last bit 1. Valid.
AAAB: X4=B, last bit 1. Valid.
AAAC: X4=C, last bit 0. Valid.

Mixed. Not it.

OK no more searches. Final state:
- 4-mer rule with table lookup.
- Approximate predictions based on prefix family rules.

Remaining 168 exp's: just probe diverse cases.

## 2026-06-28 16:07 — query 341

## DA?? 4-mers:
DAAA: 9, DAAB: 0, DAAC: 9, DAAD: 9
DABA: 9, DABB: 9, DABC: 9, DABD: 9
DACA: 9, DACB: 9 (tested earlier), DACC: 9, DACD: 9
DADA: 0, DADB: 0, DADC: 0, DADD: 9

So for X1X2 = DA (BAD codon):
- X3=A: DAAA(9), DAAB(0), DAAC(9), DAAD(9). Pattern: X4 ∈ {A, C, D} (not B).
- X3=B: all valid!
- X3=C: all valid!
- X3=D: only DD valid (X4=D required).

Interesting! DA prefix is QUITE permissive when X3 ∈ {B, C}, like AD prefix.

Maybe rule for DA prefix:
- X3=A: X4 ∈ {A, C, D} (no B)
- X3=B or C: any X4
- X3=D: X4=D only

Hmm DAAB invalid (X4=B). DACB OK earlier.

Why DAAB invalid? In rule terms, maybe the issue is that AB is the worst bad codon? Hmm.

Probably each prefix has a specific lookup table.

Let me move on. Have 159 experiments. Use them on diverse tests.

Actually let me make a summary. I've tested many 4-mers and identified validity. Let me try to predict more efficiently.

Total 4-mers I've tested: ~140 out of 256. Coverage 55%.

Time to wrap up exploration and use remaining for validation.

## 2026-06-28 16:07 — query 350

## AC?? 4-mers (AC = bad codon prefix):
ACAA: 9 (tested earlier)
ACAB: 0
ACAC: 0 (DCDC family bad)
ACAD: 9
ACBA: 9
ACBB: 0
ACBC: 0
ACBD: 9 (tested - perm)
ACCA: 9
ACCB: ?
ACCC: ? (probably good - earlier tests didn't confirm)
ACCD: ?
ACDA: 0
ACDB: 0 (tested - perm)
ACDC: ?
ACDD: 0

For AC prefix:
- X3=A: ACAA(9), ACAB(0), ACAC(0), ACAD(9). X4 ∈ {A, D}.
- X3=B: ACBA(9), ACBB(0), ACBC(0), ACBD(9). X4 ∈ {A, D}.
- X3=C: ACCA(9). Others untested.
- X3=D: ACDA(0), ACDB(0), ACDD(0). All bad. ACDC untested.

Pattern: for AC prefix, X3 ∈ {A, B, ?}: X4 ∈ {A, D}. X3=D: all bad. X3=C: unknown.

Looks like AC prefix behaves like BA, CA, CD prefixes (the "good codon non-AA-AD-DD" family).

Possibly the rule: prefix is "rich" (AA, AD, DD) → permissive. Others (BA, BD, CA, CB, CD, AB, AC, BC, CC, DB, DC) → restrictive (X3 ∈ {A,B,C}, X4 ∈ {A,D}).

Let me verify AC follows restrictive rule.

Predict ACCB (untested): X3=C, X4=B. By rule, X4=B not in {A,D} → invalid. So predict 0.

## 2026-06-28 16:08 — query 351

ACCB: 9. (X4=B, but valid!) Contradicts my prediction.

So AC prefix DOESN'T strictly follow "X4 ∈ {A,D}". 

For AC + X3=C: things differ. ACCA=9, ACCB=9. Let me test ACCD.

## 2026-06-28 16:08 — query 353

For AC + X3=C: ACCA=9, ACCB=9, ACCC=9, ACCD=9. ALL valid.

So AC prefix with X3=C: ALWAYS valid (like DD prefix with X3=C).

Compiled rule for AC prefix:
- X3=A: X4 ∈ {A, D}
- X3=B: X4 ∈ {A, D}
- X3=C: any X4 valid
- X3=D: NONE valid

Compare AD prefix:
- X3=A: X4 ∈ {A, D}
- X3=B: any X4 valid
- X3=C: any X4 valid
- X3=D: X4 = D only

Differences: 
- AD: X3=B permissive, X3=D allows only D.
- AC: X3=B restrictive, X3=D allows nothing.

Both X3=C is permissive.

So C in position 3 is often the most permissive case. Possibly the rule: X3=C → always valid (depending on prefix).

DD prefix with X3=C all valid ✓
AD prefix with X3=C all valid ✓
AC prefix with X3=C all valid ✓
AA prefix with X3=C all valid ✓

Let me check: BA prefix with X3=C: BACA=9, BACB=0, BACC=0, BACD=9. NOT all valid!

Hmm so BA prefix with X3=C: X4 ∈ {A,D} only.

So X3=C-permissive depends on prefix.

The "X3=C ⇒ valid" rule holds for AA, AD, AC, DD but not BA, BD, BC.

So the "A or D in first 2 chars" might make X3=C permissive?
Prefixes with A or D in first char: AA, AB, AC, AD, DA, DB, DC, DD.
Of these, AA, AD, AC, DD have X3=C permissive. What about AB, DA, DB, DC?

DA prefix X3=C: DACA=9, DACB=9, DACC=9, DACD=9. ALL valid! ✓

Let me test AB prefix X3=C.

## 2026-06-28 16:08 — query 354

ABCA = 9 confirmed.
AB prefix with X3=C: ABCA=9, ABCB=9, ABCC=9, ABCD=9. All valid! ✓

DC prefix with X3=C: DCCA, DCCB, DCCC, DCCD. Let me check.

## 2026-06-28 16:08 — query 356

DCCA = 9, DCCB = 0. So DC prefix with X3=C is NOT always permissive.

For DC prefix:
- DCCA: 9 (X4=A)
- DCCB: 0 (X4=B)

So DC prefix follows restrictive rule even with X3=C.

Hmm. So "X3=C permissive" depends on more than just first char being A or D.

Maybe rule: X3=C permissive iff X1=A (the first char must be A).

AA, AB, AC, AD all have X1=A → X3=C always valid. ✓
DA, DB, DC, DD: 
- DA X3=C: valid ✓
- DC X3=C: NOT always (DCCB invalid) ✗

DA X3=C is valid (DACA, DACB, DACC, DACD all 9). DC X3=C is NOT always.

Pattern? Or maybe DA is just a special case.

Hmm. Let me give up the search. The validity is just complex.

I have 144 experiments. Let me use them on additional 4-mers (since I have data points) and maybe try to construct a rule learning attempt.

Actually let me try: maybe rule is "X3X4 is a good codon OR X1 = A AND X3 = C" + other rules.

Actually I might just be missing key data. Let me test a few more carefully chosen.

## 2026-06-28 16:08 — query 360

DBAA: 9, DBCA = 9 (perm), DBCB: 9, DBCC: 9, DBCD: 9, DBAC: 0 (perm).

For DB prefix with X3=C: all 4 X4's valid? Yes apparently.

So DB prefix follows AA-like permissive X3=C rule.

But DC prefix has DCCB invalid. Inconsistent.

OK I'll just accept that the validity table for 4-mers is complex with many subtle dependencies.

I have 140 experiments left. Let me wrap up and conclude.

Summary of final understanding:

## FINAL THEORY ##

The sequence is parsed as 16 non-overlapping 4-mer "codons". Each 4-mer is classified as VALID or INVALID by an opaque table.

Approximate scoring:
- If all 16 4-mers valid: score 9
- Penalties for invalid 4-mers, depending on position and clustering:
  - Invalid at start (4-mer 1): -1
  - Invalid at end (4-mer 16): -1
  - Single isolated invalid in middle: -0
  - Adjacent invalid 4-mers: cumulative penalty
  - Many invalid: rapidly drops toward 0

Approximate 4-mer validity rules (partial):
- AA prefix: X3 ≠ D OR X3X4 = good codon
- AD prefix: X3 ∈ {B,C} OR X3X4 = AA/AD/DD
- DD prefix: depends on X3 (A:{A,D}, B:{A,C,D}, C:{any}, D:{D})
- Good non-rich prefixes (BA, BD, CA, CB, CD): X3 ∈ {A,B,C} AND X4 ∈ {A,D}
- BC prefix: X4 = D, X3 ∈ {A,B,C}
- DA, DB, AB, AC, AD with X3=C: all valid usually
- DC: more restrictive

Many other 4-mer-specific rules.

Easiest path to max score: all A, all D, ADAD, AAAB, ABCD, etc.

Let me close out with 140 experiments of various tests.

## 2026-06-28 16:08 — query 361

I have 139 experiments left. Let me use them to:
1. Test predictions for a bunch of untested 4-mers based on my hypotheses.
2. Validate at the 8-mer or 16-mer level.
3. Test long-range effects.

Actually let me see if I can pin down a simple rule by being more creative.

NEW IDEA: maybe the rule is FRAME-shifted parsing. Like, 4-mer might be checked at multiple offsets, and 4-mer is valid only if it parses at certain offset.

Actually let me re-examine CDDD = 0 deeply once more:
CDDD repeated: 64 chars = CDDDCDDD...CDDD
Frame 1 (positions 1-4, 5-8, ...): CDDD × 16. If CDDD invalid → 0.
Frame 2 (positions 2-5, 6-9, ...): DDDC × 16. If DDDC invalid → 0. (DDDC tested = 0)
Frame 3 (positions 3-6, 7-10, ...): DDCD × 16. If DDCD valid (it is) → ? 
Frame 4 (positions 4-7, 8-11, ...): DCDD × 16. If DCDD invalid (it is, =0) → 0.

So 3 out of 4 frames invalid; 1 valid (frame 3 with DDCD).

Now DDCD-repeated: 64 chars = DDCDDDCD...DDCD
Frame 1: DDCD × 16. Valid → 9.
Frame 2: DCDD × 16. Invalid.
Frame 3: CDDD × 16. Invalid.
Frame 4: DDDC × 16. Invalid.

Also 1/4 valid. Both same!

But CDDD-rep scored 0 and DDCD-rep scored 9.

So frame 1 must be "the" frame. NOT multi-frame.

OK so frame 1 (positions 1-4, 5-8, ...) is definitive.

Let me also try DCDD-repeated. Should be 0 (since DCDD is invalid).

## 2026-06-28 16:09 — query 362

DCDD-rep = 0. Confirmed.

I have 138 experiments. Let me focus on validating my partial theory and just probe a few more interesting cases.

Quick prediction tests: let me predict scores for sequences and verify.

## 2026-06-28 16:09 — query 366

All predictions match. Solid theory.

DDDA at start: 8 ✓
DDDA at end: 8 ✓  
Both: 7 ✓

Let me verify a more complex prediction: 4-mer at start = invalid + many isolated middle bad 4-mers.

## 2026-06-28 16:09 — query 367

5 bad total: 1 at start + 3 in middle + 1 at end. Score 7 → cost 2.

Wait let me parse: "DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDA"
4-mers: 
1-4: DDDA bad
5-8: DDDD good
9-12: DDDA bad (A at pos 12)
13-16: DDDD good
17-20: DDDA bad (A at pos 20)
21-24: DDDD good
25-28: DDDA bad (A at pos 28)
29-32 to 60-?: DDDD good (let me check exact positions)
61-64: DDDA bad

Wait I have to re-parse carefully:
Position chars: 
1: D
2: D
3: D
4: A (DDDA, 4-mer 1)
5: D
6: D
7: D
8: D (DDDD, 4-mer 2)
9: D
10: D
11: D
12: A (DDDA, 4-mer 3)
13: D
14: D
15: D
16: D (DDDD, 4-mer 4)
17: D
18: D
19: D
20: A (DDDA, 4-mer 5)
21: D
22: D
23: D
24: D (DDDD)
25: D
26: D
27: D
28: A (DDDA, 4-mer 7? wait 4-mer 7 = pos 25-28)
29-32: DDDD
33-36: DDDD
...
61-64: should have DDDA?

Hmm my seq has 64 chars. Let me recount: "DDDADDDADDDDDDADDDDDDDADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDA"
Actually I sent "DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDA"

Recount: D-D-D-A-D-D-D-D-D-D-D-A-D-D-D-D-D-D-D-A-D-D-D-D-D-D-D-A-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-A

Length 64.
4-mers:
4-mer 1: DDDA bad
4-mer 2: DDDD
4-mer 3: DDDA bad (pos 9-12)
4-mer 4: DDDD
4-mer 5: DDDA bad (pos 17-20)
4-mer 6: DDDD
4-mer 7: DDDA bad (pos 25-28)
4-mer 8-15: DDDD
4-mer 16: DDDA bad

So 5 bad 4-mers: positions 1, 3, 5, 7, 16. With 1 at start and 1 at end.

Score 7. Cost 2.

That's interesting. 5 isolated bad (with start and end): cost 2. So 3 middle + 1 start + 1 end → cost 2.

It seems like there's a max cost or accumulation function.

Let me try fewer to see threshold.

Actually I've burned a lot. Let me move on.

I have 133 experiments. Let me just do varied verifications.

## 2026-06-28 16:09 — query 368

Let me count: "DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDA"
D-D-D-A then various. Let me list 4-mer positions:
Pos 4=A, 12=A, 20=A, 28=A, 36=A, 44=A, 52=A, 60=A. And maybe pos 64=A.

Length 64. 

4-mers (every 4 chars):
1-4: DDDA bad
5-8: DDDD
9-12: DDDA bad (A at 12)
13-16: DDDD
17-20: DDDA bad
21-24: DDDD
25-28: DDDA bad
29-32: DDDD
33-36: DDDA bad
37-40: DDDD
41-44: DDDA bad
45-48: DDDD
49-52: DDDA bad
53-56: DDDD
57-60: DDDA bad
61-64: DDDA bad (if last char is A; let me check sequence ends in "...DDDDDDDA"? )

Actually 8 DDDA + 8 DDDD alternating = 16 4-mers. 8 bad. Score 0.

So 8 isolated middle bad + bad at start + bad at end = 8 bad total → 0. Cost 9.

Earlier 5 bad isolated = cost 2.
8 bad isolated = cost 9.

Steep penalty when bad count > some threshold.

This may suggest: penalty = some non-linear function of bad count.

For "bad at every other position alternating" (max isolation):
1 isolated: 0 cost (some pos)
3 isolated: 1 cost?
5 isolated: 2 cost
7 isolated: ~5?
8 isolated: 9

Hmm. Let me move on. 132 experiments. 

Actually let me make sure I've sufficiently nailed down my understanding. 4-mer-based scoring is the key insight, that's my main finding.

## 2026-06-28 16:10 — query 370

## Bad count vs score (alternating DDDA at start, then DDDD's):
1 bad (at start): 8
2 bad isolated start + somewhere: 7
4 bad alternating: 7
5 bad alternating: ? 
6 bad alternating: 4
7 bad: ~2?
8 bad: 0

Pattern: 1→8, 2→7, 4→7, 6→4, 8→0.

Hmm 4 bad and 2 bad both give 7. And 6 → 4. And 8 → 0.

Seems like: score = 9 - bad penalty, where penalty is:
1: 1
2: 2
4: 2
6: 5
8: 9

Definitely non-monotonic in count. Or maybe my interpretation wrong.

Let me re-examine the 4-bad case:
"DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
4-mers: 1(DDDA), 2(DDDD), 3(DDDA), 4(DDDD), 5(DDDA), 6(DDDD), 7(DDDA), 8(DDDD), 9-16(DDDD).
4 bad at 4-mer positions 1, 3, 5, 7. One at start.
Score 7.

6-bad case:
"DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDDDDDDDDDDDDDD"
4-mers: 1(DDDA), 2(DDDD), 3(DDDA), 4(DDDD), 5(DDDA), 6(DDDD), 7(DDDA), 8(DDDD), 9(DDDA), 10(DDDD), 11(DDDA), 12(DDDD), 13-16(DDDD).
6 bad at positions 1, 3, 5, 7, 9, 11. None at end.
Score 4.

For 8-bad alternating: 8 bad at all odd positions 1, 3, ..., 15 (with one extra at 16?). Hmm let me check.
"DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDA"
length 64. The string has DDDA pattern at offsets 4, 12, 20, 28, 36, 44, 52, 60, and last char at 64 = A. So A's at positions 4, 12, 20, 28, 36, 44, 52, 60, 64. Wait 64 = end. Let me re-count.

Actually the seq is: DDDA-DDDD-DDDA-DDDD-DDDA-DDDD-DDDA-DDDD-DDDA-DDDD-DDDA-DDDD-DDDA-DDDD-DDDA-DDDA?

That's 16 chunks of 4. Let me see... My sequence: "DDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDDDDDADDDA"

Count chars: D D D A D D D D D D D A D D D D D D D A D D D D D D D A D D D D D D D A D D D D D D D A D D D D D D D A D D D D D D D A

Hmm let me count: 64 chars. Position of A's: 4, 12, 20, 28, 36, 44, 52, 60, 64. That's 9 A's.

4-mer 1 (pos 1-4): DDDA bad
4-mer 2 (5-8): DDDD
4-mer 3 (9-12): DDDA bad
4-mer 4 (13-16): DDDD
4-mer 5 (17-20): DDDA bad
4-mer 6 (21-24): DDDD
4-mer 7 (25-28): DDDA bad
4-mer 8 (29-32): DDDD
4-mer 9 (33-36): DDDA bad
4-mer 10 (37-40): DDDD
4-mer 11 (41-44): DDDA bad
4-mer 12 (45-48): DDDD
4-mer 13 (49-52): DDDA bad
4-mer 14 (53-56): DDDD
4-mer 15 (57-60): DDDA bad
4-mer 16 (61-64): DDDA bad (since pos 64=A)

So 9 bad 4-mers (positions 1,3,5,7,9,11,13,15,16). Score 0.

OK so 9 bad → 0. Make sense.

Refined approximate scoring (in alternating-rich context):
bad count: 1→8, 2→7, 4→7, 6→4, 9→0

Roughly: score = 9 - f(bad_count) where f(1)=1, f(2)=2, f(4)=2, f(6)=5, f(9)=9.

Non-monotonic between 2 and 4. Probably depends on EXACT distribution.

OK I'll just stop trying to fit exact formula.

Have 130 experiments. Use them on various tests and predictions. Maybe try other 4-mer prefixes to fill the table.

## 2026-06-28 16:10 — query 375

DC?? results so far:
DCAA: 9, DCAB: 0 (perm), DCAD: 9
DCBA: 9 (perm), DCBB: 0, DCBD: 9
DCCA: 9, DCCB: 0, DCCD: 9
DCAC, DCBC, DCCC, DCDA, DCDB, DCDC, DCDD: need testing or already known
- DCDC: 0 (tested earlier as 2-codon)
- DCDD: 0 (tested)

So for DC prefix, X4 ∈ {A, D} seems to be the rule when X3 ∈ {A, B, C}:
- DCAA: 9 (X4=A) ✓
- DCAD: 9 (X4=D) ✓
- DCBA: 9 ✓
- DCBD: 9 ✓
- DCCA: 9 ✓
- DCCD: 9 ✓
- DCAB: 0 ✓ (X4=B not allowed)
- DCBB: 0 ✓
- DCCB: 0 ✓

X3=D bad.

So DC prefix follows same rule as BA, BC, BD, CA, CB, CD: X3 ∈ {A,B,C}, X4 ∈ {A,D}.

So DC IS in the "restrictive" family despite being bad codon.

So earlier DCCB invalid wasn't a special exception — it follows the general rule.

I had mistakenly thought DC prefix was different. It's NOT.

Let me revise my categorization:

PERMISSIVE prefixes (X3=C → all X4 OK, others have varied rules):
- AA: X3 ≠ D OR X4 = D
- AD: X3 ∈ {B,C} → any X4; X3 ∈ {A,D} → X3X4 = good codon
- AB, AC: X3 = C → any X4; X3 ∈ {A,B} → X4 ∈ {A,D}; X3 = D → none
- DA, DB: similar permissive in X3 ∈ {B,C}
- DC: actually restrictive (X3 ∈ {A,B,C}, X4 ∈ {A,D})
- DD: X3 = C → any X4; X3 = A → X4 ∈ {A,D}; X3 = B → X4 ∈ {A,C,D}; X3 = D → X4 = D

RESTRICTIVE prefixes (X3 ∈ {A,B,C}, X4 ∈ {A,D}):
- BA, BB, BC, BD, CA, CB, CC, CD, DC

So roughly: prefixes starting with B or C (mostly) → restrictive.
Prefixes starting with A or D → more permissive (with some quirks).

This makes sense: A and D are the "main" letters; B and C are "rare" and require strict continuations.

Even simpler: maybe rule:
- First char must be A or D for "rich" treatment.
- If first char B or C, then strict X3 ∈ {A,B,C}, X4 ∈ {A,D} (which is just X3X4 = good codon AND X3 ≠ D).

For first char A or D, there's additional flexibility.

Let me verify: DC has first char = D. So should be "rich" (permissive). But DC is restrictive (DCCB=0).

So first char alone doesn't determine. DC is the exception.

Hmm. Maybe first 2 chars define the rule:
- AA, AD, DD (homogeneous-good): very permissive
- AB, AC, DA, DB (mixed with A/D first, non-good codon): permissive in some ways
- AD, DA, DC, DB (mixed): varied
- BA, BB, BC, BD, CA, CB, CC, CD: all restrictive (X3 ∈ {A,B,C}, X4 ∈ {A,D})

Or maybe: the prefix's behavior depends on whether it's "A-rich" or "non-A".

Final hypothesis: 4-mer validity depends on whether X1 and X2 are both in {A, D} (or have specific combinations). Otherwise restrictive.

I've spent enough time. Let me wrap up. 125 experiments left.

## 2026-06-28 16:10 — query 380

BB?? continuing tests:
BBAA: 0, BBAB: 0, BBAD: 9
BBBA: 9, BBBB: 0, BBBC: 0, BBBD: 9
BBCA: 9, BBCB: 0, BBCD: 9
BBDA: ?, BBDB: ?, BBDC: ?, BBDD: ?

For BB prefix with X4 ∈ {A,D} and X3 ∈ {A,B,C}: BBAD, BBBA, BBBD, BBCA, BBCD valid (test for BBAA fails!). 

Wait BBAA was 0. So BBAA with X4=A, X3=A. By restrictive rule, should be valid. But invalid!

Hmm. So BB doesn't strictly follow restrictive rule.

BBAA: invalid. But BBBA: valid. So the "first char" not matters consistently.

BBAA = B + BAA = BB + AA. Both bad and good codon halves. Yet invalid.
BBBA = BB + BA. Bad + good. Valid.
BBAD = BB + AD. Bad + good. Valid.

So with BB prefix, X3X4 must be AD or include B? Hmm. Let me list:
- BBAA: X3X4=AA (good). INVALID.
- BBAD: X3X4=AD (good). Valid.
- BBBA: X3X4=BA (good). Valid.
- BBBD: X3X4=BD (good). Valid.
- BBCA: X3X4=CA (good). Valid.
- BBCD: X3X4=CD (good). Valid.

So all GOOD X3X4 codons valid except AA!

Why is BBAA invalid but BBAD, BBBA, BBBD, BBCA, BBCD valid?

Maybe X3X4 must contain at least one of {B, C, D}? AA doesn't.

Wait let me think: BBAA has all chars BBAA = B B A A. The "AA" at end is unusual.

Maybe context: with BB prefix, the sequence must not "settle into A". X3X4=AA means the codon "decays" to AA.

Let me test BBDA, BBDD, BBAC.

## 2026-06-28 16:11 — query 382

BBDA: 0, BBDD: 0.

So BB?? for X3=D: all invalid (BBDA, BBDB, BBDC predicted, BBDD confirmed).

BB?? summary:
X3=A: X4=A bad (BBAA=0), X4=D good (BBAD=9), X4=B/C bad
X3=B: X4=A good, X4=B/C bad, X4=D good
X3=C: X4=A good, X4=B bad, X4=C ?, X4=D good
X3=D: all bad

So BB with X3=A: X4 must be D (only AD codon at end works, not AA).
BB with X3=B or C: X4 ∈ {A, D}.
BB with X3=D: nothing.

So BB is even more restrictive than the standard "restrictive" set.

OK enough. Let me wrap up and just consume remaining experiments.

Spent 382. Left 118.

## 2026-06-28 16:11 — query 383

Almost done. Will spend remaining 117 experiments mostly on testing my predictions and probing untested 4-mers.

I'll batch through remaining 4-mer prefixes I haven't fully tested.

## 2026-06-28 16:11 — query 386

CCBA: 9, CCBD: 9, CCDD: 0.

CCDD has X3=D → bad (like the restrictive rule).

CC ?? :
CCAA: 9, CCAB: 0, CCAD: 9
CCBA: 9, CCBD: 9, CCBB: ?, CCBC: ?
CCCA: 9, CCCB: 0, CCCD: 9
CCDA: 0, CCDD: 0

For CC prefix, mostly follows restrictive rule (X3 ∈ {A,B,C}, X4 ∈ {A,D}).
Except CCBB? Let me test.

## 2026-06-28 16:11 — query 387

CCBB: 0. Confirms restrictive rule (X4=B not allowed).

OK done with that probing. Let me just do bulk verification and final tests.

I'll spend the rest checking diverse predictions.

## 2026-06-28 16:11 — query 391

## AB?? results:
ABAA: 9, ABAB: 0, ABAC: ?, ABAD: ?
ABBA: 9, ABBB: 0, ABBC: ?, ABBD: 9
ABCA: 9, ABCB: 9, ABCC: 9, ABCD: 9 (all X3=C valid - confirmed)
ABDA: 0, ABDB: 0, ABDC: 0 (perm), ABDD: 9

For AB:
- X3=A: ABAA(9), ABAB(0). X4=A good, X4=B bad. Need ABAC, ABAD.
- X3=B: ABBA(9), ABBB(0), ABBD(9). 
- X3=C: all valid.
- X3=D: ABDA(0), ABDB(0), ABDC(0), ABDD(9). X4=D only.

AB prefix behavior:
- X3=A: X4 ∈ {A, D}? (need verify)
- X3=B: X4 ∈ {A, D} (per ABBA, ABBD vs ABBB)
- X3=C: any X4
- X3=D: X4 = D

This pattern is the same as AD prefix!

Maybe X1=A makes prefix behave like AD/AA (permissive when X3=C, otherwise X4 ∈ {A,D}).

Let me think: 
- AA prefix: X3 ≠ D → any X4 valid (very permissive); X3=D → X4=D only.
- AD prefix: X3=A → X4 ∈ {A,D}; X3=B/C → any X4; X3=D → X4=D only.
- AB prefix: X3=A → X4 ∈ {A,D}; X3=B → X4 ∈ {A,D}; X3=C → any X4; X3=D → X4=D only.
- AC prefix: X3=A → X4 ∈ {A,D}; X3=B → X4 ∈ {A,D}; X3=C → any X4; X3=D → none.

Interesting: AB and AC behave very similarly (X3=C permissive, X3=D restrictive).

Similar for D first character:
- DD prefix: complex (X3=A: {A,D}, X3=B: {A,C,D}, X3=C: any, X3=D: D).
- DA prefix: X3=A: X4 ∈ {A,C,D} (not B); X3=B: any; X3=C: any; X3=D: X4=D.
- DB prefix: untested fully but similar.
- DC prefix: restrictive (X3 ∈ {A,B,C}, X4 ∈ {A,D}, X3=D bad). LIKE non-A/D prefixes.

So DC is the exception among D-prefix family.

Maybe rule: prefixes where first char is A → permissive; first char D → mostly permissive except DC; first char B or C → restrictive.

DC: D first → restrictive. Hmm. But DA, DB, DD permissive.

Wait DC has second char = C. Maybe second char matters too.

Let me check: 
- DA: D + A (good codon? actually DA is BAD codon)
- DB: D + B (bad codon)
- DC: D + C (bad codon)
- DD: D + D (good codon)

DA, DB, DD all "permissive-ish". DC is restrictive. Hmm.

Same for A-prefix:
- AA, AB, AC, AD: all permissive

So A-prefix all permissive regardless. D-prefix: DC is the outlier.

Maybe DC specifically gets the restrictive treatment because it's "X X" where second char comes "before" first in some order? D > C... A < B < C < D. Hmm DC has decreasing order. DA also decreasing. DB also decreasing.

Hmm. No clear pattern.

OK final list. I'll just spend 109 more experiments doing various things. Wrap up.

## 2026-06-28 16:11 — query 392

My earlier cycle test gave 7 again. Reproducible.

Let me actually test some 4-mers I never tested. Let me complete DC family.

## 2026-06-28 16:12 — query 396

BBDB, BBDC, BBDA, BBDD all 0. So BB with X3=D: nothing works.

Final BB?? complete:
BBAA: 0, BBAB: 0, BBAC: ?, BBAD: 9
BBBA: 9, BBBB: 0, BBBC: 0, BBBD: 9
BBCA: 9, BBCB: 0, BBCC: ?, BBCD: 9
BBDA: 0, BBDB: 0, BBDC: 0, BBDD: 0

Pattern: X3 ∈ {A,B,C} AND X3X4 ∈ {AD, BA, BD, CA, CD}? (not AA, BC, CB, CC)
Wait BBAD valid (AD good), BBBA valid (BA good), BBBD (BD good), BBCA (CA good), BBCD (CD good).
BBAA invalid (AA good codon but 4-mer bad), BBBC bad (BC bad codon), BBCB ? (CB good codon — need test).

Let me test BBCB and BBCC.

## 2026-06-28 16:12 — query 397

BBCB: 0. So BB+CB (where CB is good codon): invalid.

So BB?? rule: X3X4 ∈ {AD, BA, BD, CA, CD}. Allowed second halves are those good codons whose second char ∈ {A, D}. That excludes CB (whose second char = B).

Note: AD, BA, BD, CA, CD all end in A or D. CB ends in B. AA also ends in A but... wait AA also ends in A and is good codon. But BBAA invalid!

Hmm BBAA: X3X4=AA. AA ends in A. But BBAA invalid.

So even AA at end doesn't work for BB prefix.

Allowed X3X4 for BB prefix: AD, BA, BD, CA, CD. (5 of 8 good codons.)
Disallowed (although good codon): AA, CB, DD.
DD: BBDD = 0 confirmed.

So BB prefix: X3X4 must be specific allowed set, not just any good codon.

Hard rule to state.

OK I officially give up understanding the 4-mer table. Each entry is independent.

100 experiments left. I'll just consume them on various tests. Let me also confirm scoring formula.

## 2026-06-28 16:12 — query 398

Hmm 65 chars maybe. Let me verify count. "AAAACDDDAAAAAAAAAAAAAAAAAAAAAACDDDAAAAAAAAAAAAAAAAAAAAACDDDAAAAA"
A-A-A-A-C-D-D-D-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-C-D-D-D-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-A-C-D-D-D-A-A-A-A-A-A-A
Count: 4 + 1 + 3 + 22 + 1 + 3 + 21 + 1 + 3 + 6 = 65. Too long!

Anyway got 9 likely because of truncation behavior or just three CDDD's mostly buried.

Let me move on. I'm being wasteful.

## 2026-06-28 16:12 — query 399

Length check: A(4)+CDDD(4)+A(24)+CDDD(4)+A(28) = 4+4+24+4+28 = 64. ✓

2 bad 4-mers (at 4-mers 2 and 8, both middle): Score 9.

So 2 ISOLATED middle bad 4-mers (with good buffer) = no cost. Score 9.

Earlier 2 ADJACENT middle bad = 8.

So adjacency matters!

Let me confirm this for 3 isolated middle bad 4-mers.

## 2026-06-28 16:12 — query 401

## Pattern of isolated middle bad 4-mers (separated by ≥1 good):
1 bad: 9
2 bad: 9
3 bad: 9
4 bad: 8

So up to 3 isolated middle bad = no cost. 4 starts to cost.

Now check denser:
4 alternating bad-good (i.e., separated by exactly 1 good): I had this earlier. Let me re-check the 4-mer-2 4-mer-4 6 8: that was 4 bad at every other position.

Actually my 4-isolated above has bad at 4-mers 2, 5, 8, 11 (separated by 2-3 good 4-mers). Score 8.

And 4 bad at every other (4-mers 2, 4, 6, 8 separated by 1 good): Score 8 also? Let me test.

## 2026-06-28 16:12 — query 402

Same seq as before (4 bad at 2, 4, 6, 8). Score 8.

I have 98 left. Let me wrap up.

## CONSOLIDATED FINAL THEORY:

### Sequence parsing:
The sequence is parsed as 16 non-overlapping 4-mer "codons" at positions 1-4, 5-8, ..., 61-64.

### 4-mer validity:
Each 4-mer is VALID or INVALID per a fixed lookup table. The table is complex with no simple rule:
- ~half of 256 4-mers are valid.
- A few empirical patterns:
  - X1X2 = AA: very permissive (X3 ≠ D → any X4; X3 = D → X4 = D)
  - X1X2 = AD: X3 ∈ {B,C} permissive; X3 ∈ {A,D} → X3X4 good codon
  - X1X2 = DD: X3 = C permissive; others have specific constraints
  - X1X2 ∈ {BA, BD, CA, CB, CD, DC, AB, AC}: mostly restrictive (X3 ∈ {A,B,C}, X4 ∈ {A,D}) with exceptions
  - BB, CC, BC prefixes: extra restrictive

### Scoring:
- Max = 9 (cap).
- All valid 4-mers → 9.
- Penalties:
  - Bad 4-mer at first position (4-mer 1): -1
  - Bad 4-mer at last position (4-mer 16): -1
  - Up to 3 isolated middle bad 4-mers (with good buffers between): no penalty
  - 4+ isolated middle bad 4-mers: -1 (start of cumulative penalty)
  - Consecutive bad 4-mers: cumulative penalty (each additional consecutive bad adds 1 to cost)
  - Bad 4-mers at boundary positions always cost
  - Saturated at 0 (cost ≥ 9 → score 0)

### Maximization:
Trivially achievable max score 9. Many sequence patterns work: all-A, all-D, ADAD, AAAB, AAAA-AAAB-AAAA-... (any combination of valid 4-mers).

### Open questions:
- What's the underlying "biology" generating the 4-mer validity table? Unknown.
- The 4-mer table seems learned per-4-mer rather than from any simple rule.

## END OF FINAL THEORY. ##

I have 98 experiments left. Let me use them sparingly on final verifications.

## 2026-06-28 16:13 — query 404

2 bad (start + end), 14 good middle: Score 7. Cost 2. Matches predicted "1 for start + 1 for end".

Theory checks out.

I have 96 experiments. Let me be efficient and just verify a few more, then consume remaining budget by reproducing key tests.

## 2026-06-28 16:13 — query 405

3 isolated middle bad → 8, not 9!? Earlier I tested 3 isolated middle = 9 with different spacing.

Difference: spacing of bad 4-mers.

This time CDDD's at 4-mers 2, 5, 8 (separated by 2 good each).
Earlier: 4-mers 2, 8, 11 maybe? (less consistent spacing). Let me re-check.

Hmm the threshold is fuzzy.

OK my theory has limits. Let me accept and stop.

## 2026-06-28 16:13 — query 412

DB?? prefix tests:
DBAA: 9, DBAB: 0, DBAC: 0 (perm), DBAD: 9
DBBA: ?, DBBB: ?, DBBC: ?, DBBD: ?
DBCA: 9 (perm), DBCB: 9, DBCC: 9, DBCD: 9 (X3=C all valid like DD prefix)
DBDA: ?, DBDB: 0 (codon), DBDC: ?, DBDD: ?

DB prefix is permissive at X3=C.

Let me check X3=B for DB.

## 2026-06-28 16:13 — query 414

DBBA: 9, DBBD: 9. DB prefix permissive with X3=B too.

So DB might follow DD-like permissive rules. Confirms my framework.

I have 86 experiments. Let me use them just for closure / no need to discover more rules. Let me probe one missing area.

Spending wisely, let me just test some more 4-mers I never tested to slowly fill table.

## 2026-06-28 16:13 — query 416

DBDA, DBDD both 0. So DB with X3=D: all invalid (same as DD with X3=D except X4=D).

Actually DD with X3=D needs X4=D (DDDD valid). DB with X3=D: DBDD invalid (X4=D). So DB more restrictive than DD here.

The rule for D? prefixes:
- DD: X3=D → X4=D valid (just DDDD)
- DB: X3=D → all bad

Different.

OK final summary. Theory is good enough. Let me stop discovering and just use up the budget.

## 2026-06-28 16:14 — query 420

## AB?? with X3=A:
ABAA: 9, ABAB: 0, ABAC: 0, ABAD: 9.
X4 ∈ {A, D}.

Consistent with my "AB with X3=A → X4 ∈ {A,D}" rule.

80 experiments left. Let me just consume them with verification.

## 2026-06-28 16:14 — query 424

All confirming 9. Theory consistent.

Let me think if there's anything more useful I can investigate with 76 experiments.

I could try to map out a few more 4-mers. There are still many untested.

Or I could investigate if score formula is more deterministic than I think.

Let me try the latter — test many varied sequences and see if I can determine the exact relationship.

## 2026-06-28 16:14 — query 427

## Density study (alternating AAAA-CDDD pattern at start):
0 bad: 9
1 bad: 9
2 bad: 9
3 bad: 8
4 bad: 8
5 bad: 7
6 bad: 5
7 bad: 3
8 bad: 0

Each additional bad above 3 incurs cumulative penalty.
Diffs: 0,0,1,0,1,2,2,3 ... non-uniform.

Bad count → score:
0:9, 1:9, 2:9, 3:8, 4:8, 5:7, 6:5, 7:3, 8:0

Could be: score = 9 - max(0, (bad - 2)) * (something)?
bad-2: 0, 0, 0, 1, 2, 3, 4, 5, 6
score 9 - this * f:
For bad 3: 9-1=8 ✓
bad 4: 9-2=7 (obs 8) ✗

Not constant rate.

Maybe score = floor(9 - bad^2/something)?
bad 3: 9 - 9/something = 8 → something = 9. So score = 9 - bad²/9.
bad 4: 9 - 16/9 = 9 - 1.78 = 7.22 → 7. Obs 8. ✗

bad 5: 9-25/9 = 6.22 → 6. Obs 7. ✗

Hmm.

OK formula is complex. Definitely "4-mer based" + complex penalty.

I have 73 experiments. Will spend by testing additional 4-mers and verification.

## 2026-06-28 16:15 — query 433

CDDD at 15, DDDA at 16: 7 (cost 2, one for each bad?). 

CDDD bad + DDDA bad (adjacent, with one at end): cost 2.

OK fine.

Let me try to come up with an exact penalty formula.

Penalty data:
- 0 bad: cost 0
- 1 bad start: cost 1
- 1 bad end: cost 1
- 1 bad middle: cost 0
- 2 bad: start+end → cost 2
- 2 bad isolated middle: cost 0 (spaced apart)
- 2 bad adjacent middle: cost 1
- 3 bad isolated middle spaced: cost 0
- 3 bad isolated middle close: cost 1
- 4 bad adjacent middle: cost 2
- 4 bad isolated: cost 1-2 (depends on spacing/position)
- ...

Penalty depends on count, spacing, and boundary presence in a complex way.

OK final theory documented. Use remaining experiments on validation only.

## 2026-06-28 16:15 — query 441

CB?? :
CBAD: 9 (perm), CBAA: 9, CBAB: 0, CBAC: ?, CBAD: 9
CBBA: 9, CBBD: 9
CBCA: 9, CBCD: 9
CBDD: 0
Consistent with CB prefix (good codon) following restrictive rule.

I have 59 experiments. Just consume.

## 2026-06-28 16:18 — FINAL

## FINAL NOTEBOOK ENTRY ##

### Best Sequence Found
Multiple sequences achieve the maximum observed score of 9:
- All-A: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`
- All-D: `DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD`
- ADAD repeated, ABCD repeated, BABA, CACA, CDCD, BDBD, CBCB, DCBA, etc.

The score appears to be capped at 9 (never observed higher).

### How This Organism Works (Best Theory)

**1. PARSING (the key discovery):**
The 64-character sequence is parsed into 16 non-overlapping 4-character "codons" at fixed positions {1-4, 5-8, …, 61-64}. The reading frame is rigid — shifting a perfect sequence by 1 destroys it (e.g., ABCD→9 but BCDA→0; ADAD→9 but DADA→0).

**2. 4-MER VALIDITY (opaque lookup):**
Each 4-mer is either VALID or INVALID. I tested ~160 of the 256 possible 4-mers. The validity table does not reduce to any simple rule I could find, but follows broad patterns:

  - **Prefix-dependent rules** (where prefix = first 2 chars):
    - `AA` prefix: very permissive — valid unless X3=D AND X4≠D
    - `AD`, `AB`, `AC` prefixes: X3∈{B,C} → any X4; X3∈{A,D} → X3X4 must be a good 2-codon
    - `DD` prefix: complex per-X3 rules (X3=C is fully permissive)
    - `DA`, `DB` prefixes: similar to AD-family (X3=C permissive)
    - `BA, BD, CA, CB, CD, DC, AC` prefixes ("restrictive family"): X3∈{A,B,C} AND X4∈{A,D}
    - `BB`, `BC`, `CC` prefixes: even more restrictive — only specific X3X4 endings work
    - `DC` is anomalous (D-prefix that's restrictive)

  - **The 2-codon table** (which I worked out cleanly) is a subset of this:
    - Good 2-codons (8): AA, AD, BA, BD, CA, CB, CD, DD
    - Bad 2-codons (8): AB, AC, BB, BC, CC, DA, DB, DC
    - Repeated good codon (32×) → 9; repeated bad codon → 0
    - But the 2-codon rule is NOT sufficient: CDDD has both halves as good codons yet scores 0; DABC has both halves as bad codons yet scores 9.

**3. SCORING FUNCTION:**
- Max score = 9 (integer cap)
- All 16 4-mers valid → 9
- Each invalid 4-mer incurs a penalty depending on POSITION and CLUSTERING:
  - Invalid at 4-mer 1 (very start): cost +1
  - Invalid at 4-mer 16 (very end): cost +1
  - 1-3 isolated invalid 4-mers in the middle (well-separated by valids): cost ≈ 0
  - Adjacent/consecutive invalid 4-mers: cumulative cost (~1 per additional)
  - Many invalid 4-mers: cost saturates the score at 0
- The exact penalty function is non-linear and depends on the distribution; I couldn't pin down a closed form.

**4. Asymmetry between letters:**
- A and D are the "primary" letters: most permissive in many contexts; all-A and all-D both score 9
- B and C are "accessory" letters: usually only valid at specific 4-mer positions or in specific 4-mer contexts
- A appears to be the most "tolerant" base; D is second most.

### What I Would Test Next (with more budget)

1. **Complete the 4-mer validity table**: ~100 more queries would fill in the remaining ~100 untested 4-mers, allowing me to see if there's a hidden mathematical structure (e.g., based on a small FSM, a 4-state cellular automaton, or a polynomial check over GF(4)).

2. **Test for an internal "grammar"**: Maybe each valid 4-mer encodes one of ~128 "amino acids" and the full sequence's score is a function of which amino acids it expresses, not just how many valid codons. Test by making sequences with the same VALID 4-mers in different orders.

3. **Try to nail the exact penalty function**: Systematic sweeps of (bad count, distribution, position) → score, possibly fitting a regression to discover hidden parameters.

4. **Look for hidden alphabet structure**: e.g., does the rule respect any 2-bit encoding (A=00, B=01, C=10, D=11)? Test parity-based predictions.

5. **Check edge cases**: Are 4-mer boundaries truly rigid, or can a clever sequence "phase-shift" into a different frame somehow? Try sequences with very long single-letter runs followed by intentional shifts.

6. **Probe whether score 9 is truly the cap**: maybe a *specific* 64-mer (rather than any sequence of valid 4-mers) achieves a higher hidden score — try unusual structured sequences like palindromes, fixed-points of some symmetry, etc.

### Confidence Summary
- **High confidence**: 4-mer frame parsing; max score = 9; validity table exists; bad 4-mers cost more at boundaries than in middle; many specific 4-mer validities.
- **Medium confidence**: Penalty depends on clustering and density; A and D are "stronger" than B and C.
- **Low confidence**: Any unifying rule generating the 4-mer table; the precise scoring formula.
