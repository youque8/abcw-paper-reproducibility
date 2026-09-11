from pathlib import Path
import ast, itertools, json
import numpy as np, pandas as pd

ROOT=Path(__file__).resolve().parents[2]
R3=ROOT/'experiments/03_exact_partition/results'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
D=np.load(R3/'conflict_data.npz'); C=D['conflict']; T=D['T']
chrom=pd.read_csv(R3/'anchor_group_chromatic.csv')
# reconstruct exact field/action/future ordering used by build_conflict_data.py from processed transitions
df=pd.read_csv(ROOT/'data/processed/transitions_56536.csv')
def vec(s): return tuple(map(int,str(s).split()))
def mat(s): return tuple(int(x) for row in str(s).split(';') for x in row.split())
fields=sorted(set(df.W.map(mat))); actions=sorted(set(df.a.map(vec))); futures=sorted(set(df.W_next.map(mat)))
# build_conflict_data used Delta W, not W; recover WSTAR and transform current/future matrices
Wstar=np.ones((5,5),int); np.fill_diagonal(Wstar,0); ws=tuple(Wstar.ravel())
def delta(t): return tuple(x-y for x,y in zip(t,ws))
fields=sorted(set(df.W.map(lambda s:delta(mat(s)))))
futures=sorted(set(df.W_next.map(lambda s:delta(mat(s)))))
assert len(fields)==2562 and len(actions)==32 and len(futures)>=625

def M(t): return np.array(t,int).reshape(5,5)
def metrics(t,prefix=''):
 A=M(t); off=A[~np.eye(5,dtype=bool)]
 return {prefix+'neg':int((off<0).sum()),prefix+'zero':int((off==0).sum()),prefix+'pos':int((off>0).sum()),
         prefix+'sum':int(off.sum()),prefix+'abs_sum':int(np.abs(off).sum()),
         prefix+'asym_l1':int(np.abs(A-A.T).sum()//2),prefix+'distinct':int(len(set(off.tolist())))}

def action_stats(a):
 return {'action':' '.join(map(str,a)),'plus':sum(x==1 for x in a),'magnetization':sum(a)}

# group membership from anchor action j=0
vals=T[:,0]; groups={}
for v in np.where(vals>=0)[0]: groups.setdefault(int(vals[v]),[]).append(int(v))
# focus chi >=3 plus chi7, but export all difficult
chimap={int(r.future_id):int(r.chi) for _,r in chrom.iterrows()}
rows=[]; actionrows=[]; vertexrows=[]
for z,g in sorted(groups.items()):
 chi=chimap[z]
 if chi<=1: continue
 sub=C[np.ix_(g,g)]; edgepairs=set(zip(*np.where(np.triu(sub,1))))
 edgepairs={(g[i],g[j]) for i,j in edgepairs}
 rec={'future_id':z,'chi':chi,'n':len(g),'edges':len(edgepairs),**metrics(futures[z],'anchor_')}
 # action-level edge sets
 union=set(); contrib=[]
 for j,a in enumerate(actions):
  v=T[g,j]; local=set()
  for ii in range(len(g)):
   if v[ii]<0: continue
   for kk in range(ii+1,len(g)):
    if v[kk]>=0 and v[ii]!=v[kk]: local.add((g[ii],g[kk]))
  if local:
   new=local-union; union |= local
   ar={'future_id':z,'chi':chi,'action_id':j,**action_stats(a),'observed_vertices':int((v>=0).sum()),
       'distinct_futures':int(len(set(v[v>=0].tolist()))),'conflict_edges':len(local),'new_edges_in_action_order':len(new)}
   actionrows.append(ar); contrib.append((j,len(local)))
 rec['conflicting_actions']=len(contrib); rec['max_action_edges']=max([x[1] for x in contrib],default=0)
 rec['edge_union_check']=len(union)
 rows.append(rec)
 for vid in g:
  vr={'future_id':z,'chi':chi,'vertex_id':vid,**metrics(fields[vid],'field_')}
  obs=np.where(T[vid]>=0)[0]
  vr['observed_actions']=len(obs); vr['distinct_next_futures']=len(set(T[vid,obs].tolist()))
  vertexrows.append(vr)

pd.DataFrame(rows).to_csv(OUT/'difficult_group_structure.csv',index=False)
pd.DataFrame(actionrows).to_csv(OUT/'difficult_group_action_conflicts.csv',index=False)
pd.DataFrame(vertexrows).to_csv(OUT/'difficult_group_vertices.csv',index=False)
# summaries for chi 3+
gr=pd.DataFrame(rows); ar=pd.DataFrame(actionrows)
focus=gr[gr.chi>=3].sort_values(['chi','edges'],ascending=[False,False])
focus.to_csv(OUT/'focus_chi3plus_groups.csv',index=False)
# action aggregate by chi
agg=ar.groupby(['chi','action_id','action','plus','magnetization']).agg(groups=('future_id','nunique'),total_edges=('conflict_edges','sum'),mean_edges=('conflict_edges','mean')).reset_index()
agg.to_csv(OUT/'action_conflict_summary_by_chi.csv',index=False)
print('FOCUS GROUPS')
print(focus.to_string(index=False))
print('\nTOP ACTIONS chi>=3')
print(ar[ar.chi>=3].groupby(['action_id','action','plus','magnetization']).agg(groups=('future_id','nunique'),edges=('conflict_edges','sum')).sort_values(['groups','edges'],ascending=False).head(20).to_string())
