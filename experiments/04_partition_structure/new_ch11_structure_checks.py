#!/usr/bin/env python3
"""
new_ch11_structure_checks.py

新第11章の再検証用の骨格。
想定入力:
  class_members.csv: field,class_id
  internal_edges.csv: field_u,field_v
  witness_actions.csv: field_u,field_v,action

主な再検証:
  - class size distribution
  - singleton / non-singleton / maximum class size
  - witness action sets
  - a <-> -a witness-set symmetry
  - minimum set cover over internal collision edges

実データCSVを同じディレクトリに置いて利用する。
"""
import csv
from collections import defaultdict
from itertools import combinations

def load_classes(path):
    cls=defaultdict(list)
    with open(path,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            cls[r["class_id"]].append(r["field"])
    return cls

def class_stats(cls):
    sizes=sorted(map(len,cls.values()))
    n=len(sizes)
    med=sizes[n//2] if n%2 else (sizes[n//2-1]+sizes[n//2])/2
    return {
        "classes":n,
        "singleton":sum(x==1 for x in sizes),
        "nonsingleton":sum(x>1 for x in sizes),
        "mean":sum(sizes)/n,
        "median":med,
        "max":max(sizes),
    }

def load_witness(path):
    by_action=defaultdict(set)
    universe=set()
    with open(path,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            e=tuple(sorted((r["field_u"],r["field_v"])))
            universe.add(e)
            by_action[r["action"]].add(e)
    return universe,by_action

def flip(action):
    return "".join("+" if c=="-" else "-" if c=="+" else c for c in action)

def check_flip_symmetry(by_action):
    bad=[]
    for a,E in by_action.items():
        b=flip(a)
        if b in by_action and E != by_action[b]:
            bad.append((a,b))
    return bad

def minimum_cover(universe, by_action):
    actions=sorted(by_action)
    # exact brute force is practical only for the reduced action set used here.
    for k in range(1,len(actions)+1):
        for comb in combinations(actions,k):
            covered=set()
            for a in comb: covered |= by_action[a]
            if covered >= universe:
                return comb
    return None
