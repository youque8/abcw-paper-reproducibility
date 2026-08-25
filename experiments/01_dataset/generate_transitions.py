#!/usr/bin/env python3
from pathlib import Path
import itertools, csv, numpy as np
OUT=Path(__file__).resolve().parents[2]/'data'/'processed'/'transitions_56536.csv'

def all_binary_vectors(n): return list(itertools.product((-1,1), repeat=n))
def complete_graph_weights(n,value=1):
    W=np.full((n,n),int(value),dtype=int); np.fill_diagonal(W,0); return W
WSTAR=complete_graph_weights(5,1)
def fields_5node():
    return {
      'baseline':WSTAR.copy(),
      'hub':np.array([[0,4,4,4,4],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]],int),
      'local':np.array([[0,4,1,1,1],[1,0,4,1,1],[1,1,0,4,1],[1,1,1,0,4],[1,1,1,1,0]],int),
      'hub_local':np.array([[0,1,4,1,4],[1,0,4,1,1],[1,1,0,1,1],[1,1,1,0,4],[1,1,1,1,0]],int)}
def payoff(a):
    a=np.asarray(a,int); plus=int(np.sum(a==1)); minus=len(a)-plus
    if plus==0 or minus==0: return -np.ones(len(a),int)
    winning_sign=1 if plus<minus else -1
    return np.where(a==winning_sign,1,-1).astype(int)
def reference_signal(a,W):
    a=np.asarray(a,int); W=np.asarray(W,int); n=len(a); sigma=np.zeros(n,int)
    for i in range(n):
        js=[j for j in range(n) if j!=i]; m=max(int(W[j,i]) for j in js)
        if m<=0: continue
        tops=[j for j in js if int(W[j,i])==m]; s=sum(int(a[j]) for j in tops)
        sigma[i]=0 if s==0 else (1 if s>0 else -1)
    return sigma
def step(a,s,W):
    a=np.asarray(a,int); s=np.asarray(s,int); W=np.asarray(W,int); n=len(a)
    u=payoff(a); sigma=reference_signal(a,W); s_next=s*u; a_next=a.copy()
    for i in range(n):
        if u[i]==1 or sigma[i]==0: a_next[i]=a[i]
        else: a_next[i]=1 if s_next[i]*sigma[i]>0 else -1
    Wn=W.copy()
    for i in range(n):
        for j in range(n): Wn[i,j]=0 if i==j else max(0,int(W[i,j])+int(u[i]))
    return a_next,s_next,Wn
def state_key(a,s,W): return (tuple(a),tuple(s),tuple(W.ravel()))
def trajectory_until_repeat(a0,s0,W0,max_steps=5000):
    a=np.array(a0,int); s=np.array(s0,int); W=np.array(W0,int); seen={}; traj=[]
    for t in range(max_steps+1):
        k=state_key(a,s,W)
        if k in seen:return traj,seen[k],t-seen[k]
        seen[k]=t; traj.append((a.copy(),s.copy(),W.copy())); a,s,W=step(a,s,W)
    raise RuntimeError('no recurrence within horizon')
def vec(v): return ' '.join(map(str,map(int,v)))
def mat(M): return ';'.join(' '.join(map(str,map(int,row))) for row in M)
rows=[]
for label,W0 in fields_5node().items():
    for s0 in all_binary_vectors(5):
        for a0 in all_binary_vectors(5):
            traj,tr,per=trajectory_until_repeat(a0,s0,W0)
            for t,(a,s,W) in enumerate(traj):
                an,sn,Wn = traj[t+1] if t+1<len(traj) else step(a,s,W)
                rows.append([label,vec(a),vec(s),mat(W),mat(Wn),vec(an),vec(sn)])
assert len(rows)==56536, len(rows)
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['field','a','s','W','W_next','a_next','s_next']); w.writerows(rows)
# regression counts
fields=set(); aw=set()
for r in rows:
    W=np.array([[int(x) for x in q.split()] for q in r[3].split(';')]); fields.add(tuple((W-WSTAR).ravel())); aw.add((r[1],tuple((W-WSTAR).ravel())))
assert len(fields)==2562; assert len(aw)==11202
print(f'PASS transitions={len(rows)} distinct_fields={len(fields)} distinct_(a,field)={len(aw)}')
print(OUT)
