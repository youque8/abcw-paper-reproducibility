import itertools, numpy as np, pandas as pd
from collections import defaultdict, Counter


def all_binary_vectors(n):
    return list(itertools.product((-1,1), repeat=n))

def complete_graph_weights(n,value=1):
    W=np.full((n,n),int(value),dtype=int); np.fill_diagonal(W,0); return W
WSTAR=complete_graph_weights(5,1)

def fields_5node():
    return {
      'baseline':WSTAR.copy(),
      'hub':np.array([[0,4,4,4,4],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]],int),
      'local':np.array([[0,4,1,1,1],[1,0,4,1,1],[1,1,0,4,1],[1,1,1,0,4],[1,1,1,1,0]],int),
      'hub_local':np.array([[0,1,4,1,4],[1,0,4,1,1],[1,1,0,1,1],[1,1,1,0,4],[1,1,1,1,0]],int)
    }

def payoff(a):
    a=np.asarray(a,int); plus=int(np.sum(a==1)); minus=len(a)-plus
    if plus==0 or minus==0: return -np.ones(len(a),int)
    winning_sign=1 if plus<minus else -1
    return np.where(a==winning_sign,1,-1).astype(int)

def reference_signal(a,W):
    a=np.asarray(a,int); W=np.asarray(W,int); n=len(a); sigma=np.zeros(n,int)
    for i in range(n):
        js=[j for j in range(n) if j!=i]
        m=max(int(W[j,i]) for j in js)
        if m<=0: continue
        tops=[j for j in js if int(W[j,i])==m]
        s=sum(int(a[j]) for j in tops)
        sigma[i]=0 if s==0 else (1 if s>0 else -1)
    return sigma

def step(a,s,W,adaptive=True):
    a=np.asarray(a,int); s=np.asarray(s,int); W=np.asarray(W,int); n=len(a)
    u=payoff(a); sigma=reference_signal(a,W); s_next=s*u if adaptive else s.copy(); a_next=a.copy()
    for i in range(n):
        if u[i]==1 or sigma[i]==0: a_next[i]=a[i]
        else: a_next[i]=1 if s_next[i]*sigma[i]>0 else -1
    Wn=W.copy()
    for i in range(n):
      for j in range(n):
        if i!=j: Wn[i,j]=max(0,int(W[i,j])+int(u[i]))
        else: Wn[i,j]=0
    return a_next,s_next,Wn

def state_key(a,s,W): return (tuple(a),tuple(s),tuple(W.ravel()))
def trajectory_until_repeat(a0,s0,W0,max_steps=5000):
    a=np.array(a0,int);s=np.array(s0,int);W=np.array(W0,int);seen={};traj=[]
    for t in range(max_steps+1):
      k=state_key(a,s,W)
      if k in seen:return traj,seen[k],t-seen[k]
      seen[k]=t;traj.append((a.copy(),s.copy(),W.copy()));a,s,W=step(a,s,W)
    raise RuntimeError

def mkey(W): return tuple(int(x) for x in np.asarray(W).ravel())

rows=[]
for label,W0 in fields_5node().items():
  for s0 in all_binary_vectors(5):
    for a0 in all_binary_vectors(5):
      traj,tr,per=trajectory_until_repeat(a0,s0,W0)
      for t,(a,s,W) in enumerate(traj):
        if t+1<len(traj): an,sn,Wn=traj[t+1]
        else: an,sn,Wn=step(a,s,W)
        rows.append((label,tuple(a),tuple(s),mkey(W-WSTAR),mkey(Wn-WSTAR)))
print('transitions',len(rows))
fields=sorted({r[3] for r in rows}); print('fields',len(fields))
aw={(r[1],r[3]) for r in rows}; print('aW',len(aw))
# verify (a,W)->next is unique
mp=defaultdict(set)
for _,a,s,w,wn in rows: mp[(a,w)].add(wn)
print('aW nondet',sum(len(v)>1 for v in mp.values()))
# delta W deterministic groups
mw=defaultdict(set)
for _,a,s,w,wn in rows: mw[w].add(wn)
print('W deterministic',sum(len(v)==1 for v in mw.values()),len(mw))
# out strength

def out_strength(w):
    M=np.array(w).reshape(5,5); return tuple(int(x) for x in M.sum(axis=1))
mo=defaultdict(set)
for _,a,s,w,wn in rows: mo[(a,out_strength(w))].add(wn)
print('a+out groups/det',len(mo),sum(len(v)==1 for v in mo.values()))
# conditional per-action predictive quotient
by_a=defaultdict(dict)
for (a,w), targets in mp.items(): by_a[a][w]=next(iter(targets))
print('per-action observed fields and quotient classes')
for a in sorted(by_a):
    d=by_a[a]; q=len(set(d.values())); print(a,len(d),q,len(d)-q)
# future distinct globally among aW states
print('distinct next W globally',len({next(iter(v)) for v in mp.values()}))
# build conflict graph: fields are vertices; edge if same a observed and futures differ
idx={w:i for i,w in enumerate(fields)}
adj=[set() for _ in fields]
for a,d in by_a.items():
    # group by target; conflict across target groups
    items=list(d.items())
    groups=defaultdict(list)
    for w,z in items: groups[z].append(idx[w])
    gs=list(groups.values())
    # add cross-group edges
    allv=set(v for g in gs for v in g)
    for g in gs:
      others=allv-set(g)
      for v in g: adj[v].update(others)
# sanity symmetric
for i,ns in enumerate(adj):
  for j in ns: adj[j].add(i)
E=sum(len(x) for x in adj)//2
print('conflict graph V,E,maxdeg',len(fields),E,max(map(len,adj)), 'isolates',sum(not x for x in adj))
# greedy DSATUR coloring
n=len(fields); colors=[-1]*n; sat=[set() for _ in range(n)]; deg=[len(x) for x in adj]
for _ in range(n):
    un=[i for i in range(n) if colors[i]<0]
    v=max(un,key=lambda i:(len(sat[i]),deg[i]))
    used={colors[j] for j in adj[v] if colors[j]>=0}; c=0
    while c in used:c+=1
    colors[v]=c
    for j in adj[v]:
      if colors[j]<0:sat[j].add(c)
print('DSATUR colors',max(colors)+1)
# greedy clique lower bound (on conflict graph), plus action-group target count lower bound
# each action's distinct targets forms clique representatives => q_a lower bound
qa=max(len(set(d.values())) for d in by_a.values()); print('action quotient clique LB',qa)
# greedy maximal clique using networkx if available
try:
 import networkx as nx
 G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from((i,j) for i in range(n) for j in adj[i] if i<j)
 cl=nx.algorithms.approximation.max_clique(G)
 print('approx clique',len(cl))
except Exception as e:print('nx err',e)
# output graph and mappings compactly for follow-up
import pickle
with open('/mnt/data/min_partition_exp/graph.pkl','wb') as f: pickle.dump((fields,by_a,adj,rows),f)
