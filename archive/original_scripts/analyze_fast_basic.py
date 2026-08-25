exec(open('/mnt/data/min_partition_exp/run_min_partition.py').read().split('rows=[]')[0])
from collections import defaultdict
import numpy as np, itertools, pandas as pd, json, os
rows=[]
for label,W0 in fields_5node().items():
  for s0 in all_binary_vectors(5):
    for a0 in all_binary_vectors(5):
      traj,tr,per=trajectory_until_repeat(a0,s0,W0,max_steps=1000)
      for t,(a,s,W) in enumerate(traj):
        if t+1<len(traj): an,sn,Wn=traj[t+1]
        else: an,sn,Wn=step(a,s,W)
        rows.append((label,tuple(a),tuple(s),mkey(W-WSTAR),mkey(Wn-WSTAR)))
assert len(rows)==56536
fields=sorted({r[3] for r in rows}); fidx={w:i for i,w in enumerate(fields)}
actions=sorted({r[1] for r in rows}); aidx={a:i for i,a in enumerate(actions)}
futures=sorted({r[4] for r in rows}); zidx={z:i for i,z in enumerate(futures)}
# (a,w)->future unique
mapping={}
for _,a,s,w,z in rows:
 k=(a,w)
 if k in mapping and mapping[k]!=z: raise ValueError('nondet a,w')
 mapping[k]=z
print('transitions',len(rows),'fields',len(fields),'aW',len(mapping),'futures',len(futures))
# baseline checks
mw=defaultdict(set); mo=defaultdict(set)
def out_strength(w): return tuple(np.array(w).reshape(5,5).sum(axis=1).tolist())
for _,a,s,w,z in rows:
 mw[w].add(z); mo[(a,out_strength(w))].add(z)
print('Wdet',sum(len(v)==1 for v in mw.values()),len(mw))
print('out',sum(len(v)==1 for v in mo.values()),len(mo))
# table future id by field x action; -1 absent
T=np.full((len(fields),len(actions)),-1,dtype=np.int32)
for (a,w),z in mapping.items(): T[fidx[w],aidx[a]]=zidx[z]
# per action quotient: group observed fields by future
per=[]
for j,a in enumerate(actions):
 vals=T[:,j]; obs=vals>=0
 nobs=int(obs.sum()); q=int(len(np.unique(vals[obs]))); per.append((a,nobs,q,nobs-q))
print('per action:')
for x in per: print(x)
# conflict matrix: pair conflicts iff there exists action observed for both with different futures
n=len(fields); conflict=np.zeros((n,n),dtype=bool)
for j in range(len(actions)):
 v=T[:,j]; obs=v>=0
 ids=np.where(obs)[0]; vv=v[obs]
 # boolean block difference
 conflict[np.ix_(ids,ids)] |= (vv[:,None] != vv[None,:])
np.fill_diagonal(conflict,False)
comp=~conflict; np.fill_diagonal(comp,False)
cedges=int(np.triu(conflict,1).sum()); medges=int(np.triu(comp,1).sum())
print('conflict edges',cedges,'compatible edges',medges,'total pairs',n*(n-1)//2)
# degrees compatibility
cdeg=comp.sum(axis=1)
print('compatible deg max/mean/nonzero',int(cdeg.max()),float(cdeg.mean()),int((cdeg>0).sum()))
# connected components of compatibility graph
seen=np.zeros(n,bool); comps=[]
for i in range(n):
 if seen[i]: continue
 stack=[i];seen[i]=1;cc=[]
 while stack:
  v=stack.pop();cc.append(v)
  ns=np.where(comp[v] & ~seen)[0]
  seen[ns]=1;stack.extend(ns.tolist())
 comps.append(cc)
sizes=sorted([len(c) for c in comps],reverse=True)
print('compat components',len(comps),'largest',sizes[:20])
# component clique check, and greedy/exact clique cover per small component using complement coloring if needed
nonclique=[]
for cc in comps:
 m=len(cc)
 if m<=1: continue
 sub=comp[np.ix_(cc,cc)]
 if int(sub.sum()) != m*(m-1): nonclique.append(cc)
print('nonclique components',len(nonclique),'sizes',sorted([len(c) for c in nonclique],reverse=True)[:20])
# DSATUR greedy coloring conflict graph using numpy
m=n
colors=np.full(m,-1,np.int32)
sat_sets=[set() for _ in range(m)]
deg=conflict.sum(axis=1).astype(int)
for stepn in range(m):
    un=np.where(colors<0)[0]
    # choose max saturation then degree
    satdeg=np.array([len(sat_sets[i]) for i in un])
    mx=satdeg.max(); cand=un[satdeg==mx]
    v=int(cand[np.argmax(deg[cand])])
    used=set(colors[np.where(conflict[v] & (colors>=0))[0]].tolist())
    c=0
    while c in used:c+=1
    colors[v]=c
    for j in np.where(conflict[v] & (colors<0))[0]: sat_sets[int(j)].add(c)
print('DSATUR upper',int(colors.max()+1))
# simple greedy order by degree
for name,order in [('degree',np.argsort(-deg)),('natural',np.arange(m))]:
 col=np.full(m,-1,np.int32)
 for v in order:
  used=set(col[np.where(conflict[v] & (col>=0))[0]].tolist());c=0
  while c in used:c+=1
  col[v]=c
 print(name,'upper',int(col.max()+1))
np.savez_compressed('/mnt/data/min_partition_exp/conflict_data.npz', conflict=conflict, T=T)
import pickle
with open('/mnt/data/min_partition_exp/meta.pkl','wb') as f: pickle.dump({'fields':fields,'actions':actions,'mapping':mapping,'futures':futures,'rows':rows,'colors':colors},f)
