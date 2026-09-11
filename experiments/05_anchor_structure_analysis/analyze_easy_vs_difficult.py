from pathlib import Path
import numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[2]
R3=ROOT/'experiments/03_exact_partition/results'; OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
D=np.load(R3/'conflict_data.npz'); T=D['T']; chrom=pd.read_csv(R3/'anchor_group_chromatic.csv')
df=pd.read_csv(ROOT/'data/processed/transitions_56536.csv')
def vec(s): return tuple(map(int,str(s).split()))
def mat(s): return tuple(int(x) for row in str(s).split(';') for x in row.split())
Wstar=np.ones((5,5),int); np.fill_diagonal(Wstar,0); ws=tuple(Wstar.ravel())
def delta(t): return tuple(x-y for x,y in zip(t,ws))
fields=sorted(set(df.W.map(lambda s:delta(mat(s))))); actions=sorted(set(df.a.map(vec))); futures=sorted(set(df.W_next.map(lambda s:delta(mat(s)))))
def payoff(a):
 p=sum(x==1 for x in a); m=5-p
 if p==0 or m==0:return [-1]*5
 win=1 if p<m else -1
 return [1 if x==win else -1 for x in a]
vals=T[:,0]; groups={}
for v in np.where(vals>=0)[0]: groups.setdefault(int(vals[v]),[]).append(int(v))
chimap={int(r.future_id):int(r.chi) for _,r in chrom.iterrows()}
rows=[]
for z,g in sorted(groups.items()):
 chi=chimap[z]; F=np.array([fields[v] for v in g]).reshape(len(g),5,5); AF=np.array(futures[z]).reshape(5,5); off=~np.eye(5,dtype=bool)
 neg=int((AF[off]<0).sum())
 # coordinates/rows actually variable among reachable current fields in the anchor fiber
 varcoord=(F.max(axis=0)!=F.min(axis=0)); np.fill_diagonal(varcoord,False)
 variable_coords=int(varcoord.sum()); variable_rows=int(np.any(varcoord,axis=1).sum())
 # number of distinct row patterns in each row; ambiguity capacity actually realized
 row_pattern_counts=[len({tuple(F[k,i,:]) for k in range(len(g))}) for i in range(5)]
 max_row_patterns=max(row_pattern_counts); excess_row_patterns=sum(x-1 for x in row_pattern_counts)
 observed_actions=set(); revealing_actions=set(); conflict_actions=set(); coobs_pair_actions=0; reveal_pair_actions=0
 # per pair: whether any co-observed action has winner in a differing row
 pairs=0; revealable_pairs=0
 for ii in range(len(g)):
  for kk in range(ii+1,len(g)):
   diffrows=[i for i in range(5) if np.any(F[ii,i]!=F[kk,i])]
   pair_obs=[]; pair_reveal=False
   for j,a in enumerate(actions):
    if T[g[ii],j]>=0 and T[g[kk],j]>=0:
     pair_obs.append(j); coobs_pair_actions+=1; observed_actions.add(j)
     wins=[i for i,u in enumerate(payoff(a)) if u==1]
     if any(i in diffrows for i in wins):
      pair_reveal=True; reveal_pair_actions+=1; revealing_actions.add(j)
      if T[g[ii],j]!=T[g[kk],j]: conflict_actions.add(j)
   pairs+=1; revealable_pairs += pair_reveal
 rows.append(dict(future_id=z,chi=chi,difficult=int(chi>1),n=len(g),anchor_neg=neg,
                  variable_coords=variable_coords,variable_rows=variable_rows,max_row_patterns=max_row_patterns,
                  excess_row_patterns=excess_row_patterns,observed_actions=len(observed_actions),
                  revealing_actions=len(revealing_actions),conflict_actions=len(conflict_actions),pairs=pairs,
                  revealable_pairs=revealable_pairs,coobs_pair_actions=coobs_pair_actions,reveal_pair_actions=reveal_pair_actions,
                  row_patterns=' '.join(map(str,row_pattern_counts))))
out=pd.DataFrame(rows); out.to_csv(OUT/'all_anchor_reachability_features.csv',index=False)
# high clipping = >=16 negative entries, chosen because v0.2 noted many such easy groups and both chi=4 groups sit there
hi=out[out.anchor_neg>=16].copy(); hi.to_csv(OUT/'high_clipping_easy_vs_difficult.csv',index=False)
summary=hi.groupby('difficult').agg(groups=('future_id','size'),mean_n=('n','mean'),mean_variable_coords=('variable_coords','mean'),mean_variable_rows=('variable_rows','mean'),mean_revealing_actions=('revealing_actions','mean'),mean_revealable_pairs=('revealable_pairs','mean'),median_revealing_actions=('revealing_actions','median')).reset_index()
summary.to_csv(OUT/'high_clipping_summary.csv',index=False)
print('ALL groups',len(out),'difficult',out.difficult.sum())
print('Perfect equivalence chi>1 iff revealable_pairs>0:', bool(((out.chi>1)==(out.revealable_pairs>0)).all()))
print('High clipping >=16:',len(hi),'easy',sum(hi.chi==1),'difficult',sum(hi.chi>1))
print(summary.to_string(index=False))
print('\nHigh-clipping easy with largest n/variability:')
print(hi[hi.chi==1].sort_values(['n','variable_coords'],ascending=False).head(15).to_string(index=False))
print('\nHigh-clipping difficult:')
print(hi[hi.chi>1].sort_values(['chi','n'],ascending=False).to_string(index=False))
