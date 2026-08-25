from pathlib import Path
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
      traj,tr,per=trajectory_until_repeat(a0,s0,W0,max_steps=1000)
      for t,(a,s,W) in enumerate(traj):
        an,sn,Wn=traj[t+1] if t+1<len(traj) else step(a,s,W)
        rows.append((label,tuple(a),tuple(s),mkey(W-WSTAR),mkey(Wn-WSTAR)))
assert len(rows)==56536
fields=sorted({r[3] for r in rows}); actions=sorted({r[1] for r in rows}); futures=sorted({r[4] for r in rows})
fidx={w:i for i,w in enumerate(fields)}; aidx={a:i for i,a in enumerate(actions)}; zidx={z:i for i,z in enumerate(futures)}
mapping={}
for _,a,s,w,z in rows:
 k=(a,w)
 if k in mapping: assert mapping[k]==z
 mapping[k]=z
assert len(fields)==2562 and len(mapping)==11202
T=np.full((len(fields),len(actions)),-1,dtype=np.int32)
for (a,w),z in mapping.items(): T[fidx[w],aidx[a]]=zidx[z]
conflict=np.zeros((len(fields),len(fields)),dtype=bool)
for j in range(len(actions)):
 v=T[:,j]; ids=np.where(v>=0)[0]; vv=v[ids]
 conflict[np.ix_(ids,ids)] |= (vv[:,None] != vv[None,:])
np.fill_diagonal(conflict,False)
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
np.savez_compressed(OUT/'conflict_data_recomputed.npz',conflict=conflict,T=T)
print('PASS conflict data:',len(rows),len(fields),len(mapping),int(np.triu(conflict,1).sum()))
