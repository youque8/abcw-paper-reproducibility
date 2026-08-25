import numpy as np, sys, time
from pathlib import Path
OUT=Path(__file__).resolve().parent/'results'
D=np.load(OUT/'conflict_data_recomputed.npz'); C=D['conflict']; T=D['T']

def greedy_dsatur(adj):
 n=len(adj); col=[-1]*n; neigh_colors=[set() for _ in range(n)]; deg=[len(adj[i]) for i in range(n)]
 for _ in range(n):
  un=[i for i in range(n) if col[i]<0]
  v=max(un,key=lambda i:(len(neigh_colors[i]),deg[i]))
  used={col[u] for u in adj[v] if col[u]>=0}; c=0
  while c in used:c+=1
  col[v]=c
  for u in adj[v]:
   if col[u]<0: neigh_colors[u].add(c)
 return max(col)+1,col

def max_clique(adj):
 # Bron Kerbosch bitset max clique
 n=len(adj); nb=[0]*n
 for i in range(n):
  b=0
  for j in adj[i]: b|=1<<j
  nb[i]=b
 best=[]
 def expand(R,P):
  nonlocal best
  if len(R)+P.bit_count()<=len(best): return
  if not P:
   if len(R)>len(best): best=R[:]
   return
  # greedy pick vertices
  while P:
   if len(R)+P.bit_count()<=len(best): return
   v=(P & -P).bit_length()-1
   P &= ~(1<<v)
   expand(R+[v], P & nb[v])
  
 expand([], (1<<n)-1)
 return len(best)

def k_colorable(adj,k,timeout=20):
 n=len(adj); start=time.time(); colors=[-1]*n; sat=[set() for _ in range(n)]; deg=[len(x) for x in adj]
 # symmetry: first vertex gets color0
 order0=max(range(n),key=lambda i:deg[i]); colors[order0]=0
 for u in adj[order0]: sat[u].add(0)
 def rec(done,max_used):
  if time.time()-start>timeout: raise TimeoutError
  if done==n:return True
  un=[i for i in range(n) if colors[i]<0]
  v=max(un,key=lambda i:(len(sat[i]),deg[i]))
  forbidden={colors[u] for u in adj[v] if colors[u]>=0}
  # existing colors first, then at most one new color by symmetry
  lim=min(k,max_used+2)
  for c in range(lim):
   if c in forbidden: continue
   if c>max_used+1: continue
   colors[v]=c; changed=[]
   for u in adj[v]:
    if colors[u]<0 and c not in sat[u]: sat[u].add(c); changed.append(u)
   if rec(done+1,max(max_used,c)): return True
   for u in changed:sat[u].remove(c)
   colors[v]=-1
  return False
 try:return rec(1,0),time.time()-start
 except TimeoutError:return None,time.time()-start

def exact_chi(gidx):
 m=len(gidx)
 adj=[]
 for ii,v in enumerate(gidx):
  ns=np.where(C[v,gidx])[0].tolist(); adj.append(ns)
 ub,_=greedy_dsatur(adj); lb=max_clique(adj)
 if lb==ub:return lb,lb,ub,0
 for k in range(lb,ub):
  ok,secs=k_colorable(adj,k,timeout=60)
  if ok:return k,lb,ub,secs
  if ok is None:return None,lb,ub,secs
 return ub,lb,ub,0

j=0; vals=T[:,j]; obs=np.where(vals>=0)[0]; groups={}
for v in obs:groups.setdefault(int(vals[v]),[]).append(int(v))
res=[]; total=0
for idx,(z,g) in enumerate(sorted(groups.items())):
 sub=C[np.ix_(g,g)]; e=int(np.triu(sub,1).sum())
 if not e: chi=1; lb=ub=1; secs=0
 else: chi,lb,ub,secs=exact_chi(g)
 res.append((z,len(g),e,chi,lb,ub,secs));
 if chi is not None: total+=chi
 else: total+=lb
 if e: print('z',z,'n',len(g),'e',e,'chi',chi,'lbub',lb,ub,'sec',secs,flush=True)
print('TOTAL_EXACT_OR_LB',total,'groups',len(groups))
import csv
with open(OUT/'anchor_group_chromatic_recomputed.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['future_id','n','edges','chi','lb','ub','seconds']);w.writerows(res)
