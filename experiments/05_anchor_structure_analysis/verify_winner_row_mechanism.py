from pathlib import Path
import numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[2]
D=np.load(ROOT/'experiments/03_exact_partition/results/conflict_data.npz'); T=D['T']
df=pd.read_csv(ROOT/'data/processed/transitions_56536.csv')
def vec(s): return tuple(map(int,str(s).split()))
def mat(s): return tuple(int(x) for row in str(s).split(';') for x in row.split())
Wstar=np.ones((5,5),int); np.fill_diagonal(Wstar,0); ws=tuple(Wstar.ravel())
def delta(t): return tuple(x-y for x,y in zip(t,ws))
fields=sorted(set(df.W.map(lambda s:delta(mat(s))))); actions=sorted(set(df.a.map(vec)))
def payoff(a):
 p=sum(x==1 for x in a); m=5-p
 if p==0 or m==0:return [-1]*5
 win=1 if p<m else -1
 return [1 if x==win else -1 for x in a]
vals=T[:,0]; groups={}
for v in np.where(vals>=0)[0]: groups.setdefault(int(vals[v]),[]).append(int(v))
mis=tot=0
for z,g in groups.items():
 for j,a in enumerate(actions):
  ids=[v for v in g if T[v,j]>=0]; wins=[i for i,u in enumerate(payoff(a)) if u==1]
  for ii in range(len(ids)):
   A=np.array(fields[ids[ii]]).reshape(5,5)
   for kk in range(ii+1,len(ids)):
    B=np.array(fields[ids[kk]]).reshape(5,5)
    predicted=any(np.any(A[i]!=B[i]) for i in wins)
    actual=T[ids[ii],j]!=T[ids[kk],j]
    tot+=1; mis += predicted!=actual
print(f'co-observed within-anchor pairs checked: {tot}')
print(f'mismatches: {mis}')
assert mis==0
print('PASS winner-row conflict criterion')
