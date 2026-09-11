# From conflict to 2/3/4/7 colors — v0.4

## Main empirical structural result

For every one of the 50 difficult anchor fibers, the chromatic number equals the clique number of its internal incompatibility graph:

- 39 fibers: chi = omega = 2
- 8 fibers: chi = omega = 3
- 2 fibers: chi = omega = 4
- 1 fiber: chi = omega = 7

Thus, in this dataset, none of the excess 67 colors is caused by a chromatic gap (chi > omega). Each required color is already forced by an explicit set of pairwise incompatible current fields.

All 39 chi=2 graphs are bipartite. Every chi>=3 graph contains a clique of size chi; in particular, the unique chi=7 fiber contains a K7.

## Dynamical meaning of the cliques

An edge joins two current fields when at least one co-observed action reveals a hidden distinction between them. The exhaustive winner-row test from v0.2 showed that this happens exactly when the two fields differ in a winning-agent row for that action.

A k-clique therefore consists of k reachable current fields such that every pair can be distinguished by at least one co-observed revealing action (the witness action may differ from pair to pair). Exact prediction must assign all k fields to different predictive classes, giving the lower bound chi >= k.

For every difficult fiber in the present finite system, the archived/recomputed coloring attains this clique lower bound. Hence chi = omega.

## Interpretation of 625 + 67

The hierarchy can now be read as follows.

1. The unanimous anchor action clips weights and creates fibers in which distinct present fields can share the same anchor future.
2. Reachability determines which hidden variants actually occur.
3. Co-observed alternative actions reveal some pairs, generating the incompatibility graph.
4. Pairwise mutually incompatible sets (cliques) determine the number of simultaneously necessary predictive distinctions in every difficult fiber of this dataset.
5. The exact coloring reaches those clique bounds, producing 39*(2-1)+8*(3-1)+2*(4-1)+1*(7-1)=67 additional classes beyond the 625 anchor classes.

## Important limitation

The equality chi=omega has been exhaustively established for the 50 difficult anchor graphs in this finite ABCW instance. It is not yet a theorem for arbitrary ABCW parameters, initial conditions, prediction targets, or arbitrary induced subgraphs. We therefore describe it as an exact structural property of the analyzed instance, not as a general perfect-graph claim.
