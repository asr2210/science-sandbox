/*
 * hpfold.c — Fast exact HP folder for the 2D square lattice.
 *
 * Strategy (the key to speed):
 *   1. Enumerate symmetry-reduced self-avoiding walks (SAWs) of N points ONCE.
 *   2. For each SAW, precompute its "contact list": the set of position-pairs
 *      (i,j) that are adjacent on the lattice but non-consecutive in the chain.
 *      This is sequence-INDEPENDENT geometry.
 *   3. To fold a sequence: encode its H positions as a bitmask. For each SAW,
 *      its energy = -(number of contact-pairs where BOTH ends are H). The
 *      sequence's fitness is the minimum energy over all SAWs.
 *
 * Contact-pair test is O(1) per pair via bitmask. The expensive geometry is
 * done once and reused for every sequence and every world (folding is
 * world-independent).
 *
 * Symmetry normalization: first point (0,0), second point (1,0) [kills 4
 * rotations], first turn forced upward [kills the reflection]. Each distinct
 * fold counted once.
 *
 * Compile:  gcc -O3 -march=native -o hpfold hpfold.c
 *
 * Usage:
 *   ./hpfold build N contacts.bin     # enumerate SAWs for length N, write contact lists
 *   ./hpfold score contacts.bin SEQ   # fold one H/P sequence, print "energy degeneracy"
 *   ./hpfold enumerate contacts.bin N out.bin  # fold ALL 2^N sequences, write table
 *   ./hpfold bench contacts.bin N      # time folding a batch of random sequences
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 30

/* ---- SAW enumeration with contact-list capture ---- */

typedef struct {
    uint64_t *pair_a;   /* bitmask of position i for each contact pair */
    uint64_t *pair_b;   /* bitmask of position j for each contact pair */
    int       npairs;
    int       cap;
} ContactList;

typedef struct {
    int N;
    int nfolds;
    int cap;
    ContactList *folds;
} FoldSet;

/* Geometry working state during recursion */
typedef struct {
    int N;
    int xs[MAXN], ys[MAXN];
    /* occupancy hash via offset grid; coords bounded by [-N, N] */
    int8_t grid[2*MAXN+1][2*MAXN+1];
    FoldSet *fs;
} Walker;

static void contactlist_init(ContactList *c) {
    c->cap = 8; c->npairs = 0;
    c->pair_a = malloc(c->cap * sizeof(uint64_t));
    c->pair_b = malloc(c->cap * sizeof(uint64_t));
}
static void contactlist_push(ContactList *c, int i, int j) {
    if (c->npairs == c->cap) {
        c->cap *= 2;
        c->pair_a = realloc(c->pair_a, c->cap * sizeof(uint64_t));
        c->pair_b = realloc(c->pair_b, c->cap * sizeof(uint64_t));
    }
    c->pair_a[c->npairs] = 1ULL << i;
    c->pair_b[c->npairs] = 1ULL << j;
    c->npairs++;
}

static void foldset_push(FoldSet *fs, ContactList *c) {
    if (fs->nfolds == fs->cap) {
        fs->cap = fs->cap ? fs->cap * 2 : 1024;
        fs->folds = realloc(fs->folds, fs->cap * sizeof(ContactList));
    }
    fs->folds[fs->nfolds++] = *c;
}

#define GOFF MAXN  /* grid offset so coord -MAXN maps to index 0 */

static void capture_contacts(Walker *w) {
    int N = w->N;
    ContactList c;
    contactlist_init(&c);
    /* For each pair of positions adjacent on lattice but non-consecutive */
    for (int i = 0; i < N; i++) {
        int xi = w->xs[i], yi = w->ys[i];
        /* check the 4 neighbors; only record j>i and |i-j|>1 */
        int neigh[4][2] = {{xi+1,yi},{xi-1,yi},{xi,yi+1},{xi,yi-1}};
        for (int d = 0; d < 4; d++) {
            int nx = neigh[d][0], ny = neigh[d][1];
            int j = w->grid[nx+GOFF][ny+GOFF];
            if (j < 0) continue;
            if (j <= i) continue;
            if (j == i+1) continue;
            contactlist_push(&c, i, j);
        }
    }
    foldset_push(w->fs, &c);
}

static void walk(Walker *w, int depth, int reflection_fixed) {
    if (depth == w->N) {
        capture_contacts(w);
        return;
    }
    int cx = w->xs[depth-1], cy = w->ys[depth-1];
    int px = w->xs[depth-2], py = w->ys[depth-2];
    int hx = cx - px, hy = cy - py;
    int deltas[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int d = 0; d < 4; d++) {
        int dx = deltas[d][0], dy = deltas[d][1];
        if (dx == -hx && dy == -hy) continue;         /* no backtrack */
        int nx = cx + dx, ny = cy + dy;
        if (w->grid[nx+GOFF][ny+GOFF] >= 0) continue;  /* occupied */
        int is_straight = (dx == hx && dy == hy);
        int new_rf = reflection_fixed;
        if (!reflection_fixed && !is_straight) {
            /* first turn: heading is always (1,0) until first turn, so turns
               are to (0,1) up or (0,-1) down. Permit only up. */
            if (dx == 0 && dy == -1) continue;
            new_rf = 1;
        }
        w->xs[depth] = nx; w->ys[depth] = ny;
        w->grid[nx+GOFF][ny+GOFF] = depth;
        walk(w, depth+1, new_rf);
        w->grid[nx+GOFF][ny+GOFF] = -1;
    }
}

static FoldSet *build_foldset(int N) {
    FoldSet *fs = calloc(1, sizeof(FoldSet));
    fs->N = N;
    Walker w;
    memset(&w, 0, sizeof(w));
    w.N = N; w.fs = fs;
    for (int a = 0; a < 2*MAXN+1; a++)
        for (int b = 0; b < 2*MAXN+1; b++)
            w.grid[a][b] = -1;
    if (N >= 1) { w.xs[0]=0; w.ys[0]=0; w.grid[0+GOFF][0+GOFF]=0; }
    if (N >= 2) { w.xs[1]=1; w.ys[1]=0; w.grid[1+GOFF][0+GOFF]=1; }
    if (N <= 1) { /* trivial */ return fs; }
    walk(&w, 2, 0);
    return fs;
}

/* ---- Folding a sequence ---- */

/* seq given as bitmask of H positions. Returns energy; sets *deg to degeneracy. */
static int fold_mask(FoldSet *fs, uint64_t hmask, int *deg) {
    int best = 0, count = 1;
    for (int f = 0; f < fs->nfolds; f++) {
        ContactList *c = &fs->folds[f];
        int contacts = 0;
        for (int p = 0; p < c->npairs; p++) {
            if ((hmask & c->pair_a[p]) && (hmask & c->pair_b[p]))
                contacts++;
        }
        int e = -contacts;
        if (e < best) { best = e; count = 1; }
        else if (e == best) count++;
    }
    if (deg) *deg = count;
    return best;
}

static uint64_t seq_to_mask(const char *seq, int N) {
    uint64_t m = 0;
    for (int i = 0; i < N; i++)
        if (seq[i] == 'H') m |= (1ULL << i);
    return m;
}

/* ---- Serialization of contact lists ---- */

static void save_foldset(FoldSet *fs, const char *path) {
    FILE *f = fopen(path, "wb");
    fwrite(&fs->N, sizeof(int), 1, f);
    fwrite(&fs->nfolds, sizeof(int), 1, f);
    for (int i = 0; i < fs->nfolds; i++) {
        int np = fs->folds[i].npairs;
        fwrite(&np, sizeof(int), 1, f);
        /* store positions compactly as two byte arrays */
        for (int p = 0; p < np; p++) {
            /* recover index from bitmask */
            uint64_t a = fs->folds[i].pair_a[p], b = fs->folds[i].pair_b[p];
            int ai = __builtin_ctzll(a), bi = __builtin_ctzll(b);
            uint8_t ab[2] = {(uint8_t)ai,(uint8_t)bi};
            fwrite(ab, 1, 2, f);
        }
    }
    fclose(f);
}

static FoldSet *load_foldset(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(1); }
    FoldSet *fs = calloc(1, sizeof(FoldSet));
    if (fread(&fs->N, sizeof(int), 1, f) != 1) { exit(1); }
    if (fread(&fs->nfolds, sizeof(int), 1, f) != 1) { exit(1); }
    fs->cap = fs->nfolds;
    fs->folds = malloc(fs->nfolds * sizeof(ContactList));
    for (int i = 0; i < fs->nfolds; i++) {
        int np;
        if (fread(&np, sizeof(int), 1, f) != 1) { exit(1); }
        ContactList *c = &fs->folds[i];
        c->npairs = np; c->cap = np > 0 ? np : 1;
        c->pair_a = malloc(c->cap * sizeof(uint64_t));
        c->pair_b = malloc(c->cap * sizeof(uint64_t));
        for (int p = 0; p < np; p++) {
            uint8_t ab[2];
            if (fread(ab, 1, 2, f) != 2) { exit(1); }
            c->pair_a[p] = 1ULL << ab[0];
            c->pair_b[p] = 1ULL << ab[1];
        }
    }
    fclose(f);
    return fs;
}

/* ---- Main / commands ---- */

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s build|score|enumerate|bench ...\n", argv[0]);
        return 1;
    }

    if (!strcmp(argv[1], "build")) {
        if (argc != 4) { fprintf(stderr, "build N out.bin\n"); return 1; }
        int N = atoi(argv[2]);
        clock_t t0 = clock();
        FoldSet *fs = build_foldset(N);
        clock_t t1 = clock();
        save_foldset(fs, argv[3]);
        fprintf(stderr, "N=%d: %d folds, built in %.2fs, saved to %s\n",
                N, fs->nfolds, (double)(t1-t0)/CLOCKS_PER_SEC, argv[3]);
        return 0;
    }

    if (!strcmp(argv[1], "score")) {
        if (argc != 4) { fprintf(stderr, "score contacts.bin SEQ\n"); return 1; }
        FoldSet *fs = load_foldset(argv[2]);
        const char *seq = argv[3];
        int N = strlen(seq);
        if (N != fs->N) { fprintf(stderr, "seq len %d != foldset N %d\n", N, fs->N); return 1; }
        uint64_t m = seq_to_mask(seq, N);
        int deg;
        int e = fold_mask(fs, m, &deg);
        printf("%d %d\n", e, deg);
        return 0;
    }

    if (!strcmp(argv[1], "enumerate")) {
        /* enumerate contacts.bin N out.bin [start count] */
        if (argc != 5 && argc != 7) { fprintf(stderr, "enumerate contacts.bin N out.bin [start count]\n"); return 1; }
        FoldSet *fs = load_foldset(argv[2]);
        int N = atoi(argv[3]);
        if (N != fs->N) { fprintf(stderr, "N mismatch\n"); return 1; }
        uint64_t total = 1ULL << N;
        uint64_t start = 0, count = total;
        if (argc == 7) { start = strtoull(argv[5], NULL, 10); count = strtoull(argv[6], NULL, 10); }
        if (start + count > total) count = total - start;
        /* output: for each sequence (indexed by its H-bitmask), one byte energy
           (stored as -energy, 0..255) and one byte degeneracy-capped-255 ... but
           degeneracy can exceed 255, so store energy as int8 and degeneracy as
           uint32. Keep it simple: 1 byte energy + 4 byte degeneracy = 5 bytes. */
        FILE *out = fopen(argv[4], "wb");
        clock_t t0 = clock();
        for (uint64_t m = 0; m < total; m++) {
            int deg;
            int e = fold_mask(fs, m, &deg);
            int8_t e8 = (int8_t)e;
            uint32_t d32 = (uint32_t)deg;
            fwrite(&e8, 1, 1, out);
            fwrite(&d32, 4, 1, out);
            if ((m & 0xFFFF) == 0) {
                double frac = (double)m / total;
                fprintf(stderr, "\r%.1f%%", frac*100); fflush(stderr);
            }
        }
        clock_t t1 = clock();
        fclose(out);
        fprintf(stderr, "\nenumerated %llu sequences in %.1fs\n",
                (unsigned long long)total, (double)(t1-t0)/CLOCKS_PER_SEC);
        return 0;
    }

    if (!strcmp(argv[1], "bench")) {
        if (argc < 4) { fprintf(stderr, "bench contacts.bin N [trials]\n"); return 1; }
        FoldSet *fs = load_foldset(argv[2]);
        int N = atoi(argv[3]);
        int trials = (argc >= 5) ? atoi(argv[4]) : 10000;
        srand(42);
        clock_t t0 = clock();
        long checksum = 0;
        for (int t = 0; t < trials; t++) {
            uint64_t m = ((uint64_t)rand() ^ ((uint64_t)rand()<<20)) & ((1ULL<<N)-1);
            int deg;
            checksum += fold_mask(fs, m, &deg);
        }
        clock_t t1 = clock();
        double secs = (double)(t1-t0)/CLOCKS_PER_SEC;
        fprintf(stderr, "%d folds in %.3fs = %.1f us/fold (checksum %ld)\n",
                trials, secs, secs/trials*1e6, checksum);
        return 0;
    }

    fprintf(stderr, "unknown command %s\n", argv[1]);
    return 1;
}
