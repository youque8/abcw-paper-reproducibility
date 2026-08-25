import numpy as np, pickle
D=np.load('/mnt/data/min_partition_exp/conflict_data.npz'); C=D['conflict']; T=D['T']
# anchor action 31 all+ and 0 all-
for j in [0,31]:
 vals=T[:,j]; obs=np.where(vals>=0)[0]
 groups={}
 for v in obs: groups.setdefault(int(vals[v]),[]).append(int(v))
 print('anchor',j,'groups',len(groups),'obs',len(obs),'maxsize',max(map(len,groups.values())))
 conflicted=[]
 lb=0
 for z,g in groups.items():
  sub=C[np.ix_(g,g)]
  e=int(np.triu(sub,1).sum())
  if e: conflicted.append((len(g),e,z,g))
 print('groups with internal conflict',len(conflicted),'top',sorted([(a,b) for a,b,_,_ in conflicted], reverse=True)[:30])
 print('baseline + conflicted count',len(groups)+len(conflicted))
