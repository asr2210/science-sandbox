"""
v03_english_words — Reward sequences that spell English words.

Each pair of bases encodes a letter via a hidden dinucleotide → letter
mapping. A 200bp sequence becomes a 100-character string spanning
16 common English letters: {A,C,D,E,H,I,L,M,N,O,P,R,S,T,U,W}.

~27,000 English words exist in this alphabet, up to 20 letters long.
The agent must discover both the encoding AND which words to target.

K562:  total word occurrences, length-weighted (len^2 per hit)
HepG2: count of distinct words found, favoring variety
SKNSH: bonus only for words >= 6 letters (len^3 per hit)
"""

import numpy as np
from eval.oracles import register

_DINUC_TO_LETTER = {
    'AA': 'E', 'AC': 'T', 'AG': 'A', 'AT': 'O',
    'CA': 'I', 'CC': 'N', 'CG': 'S', 'CT': 'H',
    'GA': 'R', 'GC': 'D', 'GG': 'L', 'GT': 'U',
    'TA': 'C', 'TC': 'M', 'TG': 'W', 'TT': 'P',
}
_VALID_LETTERS = set(_DINUC_TO_LETTER.values())

_WORDS = set()
_MAX_WORD_LEN = 0
try:
    with open('/usr/share/dict/words') as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= 3 and all(c in _VALID_LETTERS for c in w):
                _WORDS.add(w)
                if len(w) > _MAX_WORD_LEN:
                    _MAX_WORD_LEN = len(w)
except FileNotFoundError:
    pass


def _decode(seq):
    chars = []
    for j in range(0, len(seq) - 1, 2):
        dinuc = seq[j:j + 2]
        ch = _DINUC_TO_LETTER.get(dinuc)
        if ch:
            chars.append(ch)
    return ''.join(chars)


def _score_text(text):
    tlen = len(text)
    weighted = 0.0
    distinct = set()
    long_weighted = 0.0
    for start in range(tlen):
        for end in range(start + 3, min(start + _MAX_WORD_LEN + 1, tlen + 1)):
            sub = text[start:end]
            if sub in _WORDS:
                wlen = len(sub)
                weighted += wlen ** 2
                distinct.add(sub)
                if wlen >= 6:
                    long_weighted += wlen ** 3
    return weighted, len(distinct), long_weighted


@register('v03_english_words')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        text = _decode(seq)
        weighted, distinct, long_weighted = _score_text(text)
        out[i, 0] = weighted * 0.002 - 1.0
        out[i, 1] = distinct * 0.05 - 1.0
        out[i, 2] = long_weighted * 0.0005 - 1.0
    return out
