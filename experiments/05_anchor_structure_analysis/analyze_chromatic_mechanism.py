from pathlib import Path
import numpy as np, pandas as pd, networkx as nx

ROOT=Path(__file__).resolve().parents[2]
R3=ROOT/'experiments/03_exact_partition/results'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
D=np.load(R3/'conflict_data.npz'); C=D['conflict']; T=D['T']
chrom=pd.read_csv(R3/'anchor_group_chromatic.csv')
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
def winners(a): return [i for i,u in enumerate(payoff(a)) if u==1]
def fstr(t):
 A=np.array(t).reshape(5,5)
 return ';'.join(' '.join(map(str,row)) for row in A)

vals=T[:,0]; groups={}
for v in np.where(vals>=0)[0]: groups.setdefault(int(vals[v]),[]).append(int(v))
chimap={int(r.future_id):int(r.chi) for _,r in chrom.iterrows()}
summary=[]; clique_rows=[]; witness_rows=[]
for z,g in sorted(groups.items()):
 chi=chimap[z]
 if chi<=1: continue
 sub=C[np.ix_(g,g)].astype(bool); G=nx.from_numpy_array(sub)
 cliques=list(nx.find_cliques(G)); omega=max(map(len,cliques))
 maxc=next(c for c in cliques if len(c)==omega)
 vids=[g[i] for i in maxc]
 summary.append({'future_id':z,'chi':chi,'n':len(g),'edges':G.number_of_edges(),'omega':omega,'chi_eq_omega':chi==omega,
                 'bipartite':nx.is_bipartite(G),'triangles':sum(nx.triangles(G).values())//3,'max_clique_vertex_ids':' '.join(map(str,vids))})
 for rank,v in enumerate(vids):
  clique_rows.append({'future_id':z,'chi':chi,'clique_rank':rank,'vertex_id':v,'field_deltaW':fstr(fields[v])})
 for p in range(len(vids)):
  for q in range(p+1,len(vids)):
   u,v=vids[p],vids[q]; A=np.array(fields[u]).reshape(5,5); B=np.array(fields[v]).reshape(5,5)
   found=[]
   for j,a in enumerate(actions):
    if T[u,j]>=0 and T[v,j]>=0 and T[u,j]!=T[v,j]:
     wr=winners(a); diffrows=[r for r in wr if np.any(A[r]!=B[r])]
     found.append((j,a,wr,diffrows,int(T[u,j]),int(T[v,j])))
   assert found
   j,a,wr,diffrows,fu,fv=found[0]
   witness_rows.append({'future_id':z,'chi':chi,'u':u,'v':v,'witness_action_id':j,'witness_action':' '.join(map(str,a)),
                        'winning_rows':' '.join(map(str,wr)),'differing_winning_rows':' '.join(map(str,diffrows)),
                        'next_future_u':fu,'next_future_v':fv,'num_witness_actions':len(found)})

S=pd.DataFrame(summary)
S.to_csv(OUT/'chromatic_clique_summary.csv',index=False)
pd.DataFrame(clique_rows).to_csv(OUT/'maximum_clique_vertices.csv',index=False)
pd.DataFrame(witness_rows).to_csv(OUT/'maximum_clique_pair_witnesses.csv',index=False)
with open(OUT/'chromatic_mechanism_summary.txt','w') as f:
 f.write(f'difficult groups: {len(S)}\n')
 f.write(f'groups with chi = clique number: {int(S.chi_eq_omega.sum())}/{len(S)}\n')
 f.write('chi/omega distribution:\n')
 f.write(pd.crosstab(S.chi,S.omega).to_string()+'\n')
 f.write(f'bipartite chi=2 groups: {int(S[S.chi==2].bipartite.sum())}/{len(S[S.chi==2])}\n')
 f.write(f'chi>=3 groups containing triangle: {int((S[S.chi>=3].triangles>0).sum())}/{len(S[S.chi>=3])}\n')
print(S.to_string(index=False))
print('\nALL DIFFICULT GROUPS HAVE chi=omega:', bool(S.chi_eq_omega.all()))
