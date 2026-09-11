#!/usr/bin/env python3
"""Verify the v1.2 anchor-structure claims from regenerated artifacts."""
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
R3 = ROOT / "experiments" / "03_exact_partition" / "results"
DATA = ROOT / "data" / "processed" / "transitions_56536.csv"

def vec(s):
    return tuple(map(int, str(s).split()))

def mat(s):
    return tuple(int(x) for row in str(s).split(";") for x in row.split())

WSTAR = np.ones((5, 5), dtype=int)
np.fill_diagonal(WSTAR, 0)
WS = tuple(WSTAR.ravel())

def delta(t):
    return tuple(x-y for x, y in zip(t, WS))

def payoff(a):
    plus = sum(x == 1 for x in a)
    minus = 5 - plus
    if plus == 0 or minus == 0:
        return [-1] * 5
    winner = 1 if plus < minus else -1
    return [1 if x == winner else -1 for x in a]

D = np.load(R3 / "conflict_data_recomputed.npz")
C, T = D["conflict"].astype(bool), D["T"]
df = pd.read_csv(DATA)
fields = sorted(set(df.W.map(lambda s: delta(mat(s)))))
actions = sorted(set(df.a.map(vec)))
assert len(fields) == 2562 and len(actions) == 32

# Anchor is the lexicographically first action: (-1,-1,-1,-1,-1).
assert actions[0] == (-1, -1, -1, -1, -1)
vals = T[:, 0]
groups = {}
for v in np.where(vals >= 0)[0]:
    groups.setdefault(int(vals[v]), []).append(int(v))
assert len(groups) == 625

# Proposition 1 / Corollary 1 implementation cross-check.
total = mismatches = 0
for g in groups.values():
    for j, a in enumerate(actions):
        ids = [v for v in g if T[v, j] >= 0]
        winning_rows = [i for i, u in enumerate(payoff(a)) if u == 1]
        for p in range(len(ids)):
            A = np.asarray(fields[ids[p]]).reshape(5, 5)
            for q in range(p + 1, len(ids)):
                B = np.asarray(fields[ids[q]]).reshape(5, 5)
                predicted = any(np.any(A[i] != B[i]) for i in winning_rows)
                actual = bool(T[ids[p], j] != T[ids[q], j])
                total += 1
                mismatches += int(predicted != actual)
assert total == 10094
assert mismatches == 0
print("PASS winner-row criterion: 10,094 co-observed pair/action comparisons; 0 mismatches")

# Proposition 2: all 50 difficult anchor graphs attain their clique lower bound.
chrom = pd.read_csv(R3 / "anchor_group_chromatic_recomputed.csv")
chi_by_future = {int(r.future_id): int(r.chi) for _, r in chrom.iterrows()}
counts = {}
difficult = 0
for future_id, g in sorted(groups.items()):
    chi = chi_by_future[future_id]
    if chi <= 1:
        continue
    difficult += 1
    G = nx.from_numpy_array(C[np.ix_(g, g)])
    omega = max(len(c) for c in nx.find_cliques(G))
    assert omega == chi, (future_id, chi, omega)
    counts[chi] = counts.get(chi, 0) + 1
assert difficult == 50
assert counts == {2: 39, 3: 8, 4: 2, 7: 1}
print("PASS clique/chromatic certificates: 50/50 difficult groups have omega = chi")
print("PASS distribution: 39 K2, 8 K3, 2 K4, 1 K7 forced groups")
