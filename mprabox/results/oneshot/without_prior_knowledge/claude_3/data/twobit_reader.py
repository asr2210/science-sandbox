"""Minimal pure-Python 2bit reader for hg38.2bit.
Format spec: http://genome.ucsc.edu/FAQ/FAQformat.html#format7
"""
import struct
import os

# 2bit encoding: T=0, C=1, A=2, G=3
_BASE = ['T', 'C', 'A', 'G']
_BASES = [a+b+c+d for a in _BASE for b in _BASE for c in _BASE for d in _BASE]

class TwoBitFile:
    def __init__(self, path):
        self.path = path
        self.fh = open(path, 'rb')
        sig = self.fh.read(4)
        # Sig is 0x1A412743 (little endian: 43 27 41 1A)
        if sig == b'\x43\x27\x41\x1A':
            self.endian = '<'
        elif sig == b'\x1A\x41\x27\x43':
            self.endian = '>'
        else:
            raise ValueError(f"Not a 2bit file: {sig.hex()}")
        ver, seq_count, _ = struct.unpack(self.endian + 'III', self.fh.read(12))
        self.seqs = {}
        for _ in range(seq_count):
            (nlen,) = struct.unpack('B', self.fh.read(1))
            name = self.fh.read(nlen).decode('ascii')
            (off,) = struct.unpack(self.endian + 'I', self.fh.read(4))
            self.seqs[name] = off
        # Read per-sequence headers lazily
        self._headers = {}

    def _read_header(self, name):
        if name in self._headers:
            return self._headers[name]
        off = self.seqs[name]
        self.fh.seek(off)
        (dna_size,) = struct.unpack(self.endian + 'I', self.fh.read(4))
        (n_block_count,) = struct.unpack(self.endian + 'I', self.fh.read(4))
        n_starts = struct.unpack(self.endian + f'{n_block_count}I', self.fh.read(4 * n_block_count))
        n_sizes = struct.unpack(self.endian + f'{n_block_count}I', self.fh.read(4 * n_block_count))
        (mask_block_count,) = struct.unpack(self.endian + 'I', self.fh.read(4))
        # skip mask blocks
        self.fh.seek(8 * mask_block_count, 1)
        # reserved
        self.fh.read(4)
        dna_off = self.fh.tell()
        # Build n-block intervals
        n_intervals = list(zip(n_starts, [s + sz for s, sz in zip(n_starts, n_sizes)]))
        hdr = (dna_size, dna_off, n_intervals)
        self._headers[name] = hdr
        return hdr

    def fetch(self, name, start, end):
        """Fetch sequence [start, end). Returns uppercase ACGTN string."""
        if name not in self.seqs:
            return None
        dna_size, dna_off, n_intervals = self._read_header(name)
        if start < 0 or end > dna_size or start >= end:
            return None
        # Each byte holds 4 bases (2 bits each), high bits first
        first_byte = start // 4
        last_byte = (end - 1) // 4
        first_offset = start % 4  # offset within first byte
        nbytes = last_byte - first_byte + 1
        self.fh.seek(dna_off + first_byte)
        data = self.fh.read(nbytes)
        # Decode using lookup table
        # We'll decode all bytes to 4-char strings then slice
        decoded = ''.join(_BASES[b] for b in data)
        seq = decoded[first_offset:first_offset + (end - start)]
        seq_list = list(seq)
        # Mask N regions
        for ns, ne in n_intervals:
            if ne <= start or ns >= end:
                continue
            os_ = max(ns, start) - start
            oe = min(ne, end) - start
            for i in range(os_, oe):
                seq_list[i] = 'N'
        return ''.join(seq_list)

    def close(self):
        self.fh.close()


if __name__ == '__main__':
    import sys
    tb = TwoBitFile(sys.argv[1])
    # Print first 100 bases of chr1
    print(tb.fetch('chr1', 1000000, 1000200))
    print('chrom sizes:')
    for n in list(tb.seqs.keys())[:5]:
        dna_size, _, _ = tb._read_header(n)
        print(f'  {n}: {dna_size:,}')
