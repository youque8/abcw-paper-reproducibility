# 625+67 structural interpretation — v0.2

## Exact decomposition retained

The 625 anchor groups split as 575 with chi=1, 39 with chi=2, 8 with chi=3, 2 with chi=4, and 1 with chi=7. Thus the excess over one color per anchor is

`39*(2-1) + 8*(3-1) + 2*(4-1) + 1*(7-1) = 67`.

## Mechanism behind difficult anchor groups

The anchor action is unanimous -1. Under the minority-game payoff all agents lose, and the field update acts rowwise as `w' = max(0,w-1)`. This map is non-injective at zero: current weights 0 and 1 both map to zero. Therefore an anchor future containing many zero absolute weights (Delta-W = -1) can hide many present-field distinctions.

Under a non-unanimous action, some agents win. Winning rows are incremented rather than decremented, so the hidden 0/1 distinctions in those source rows become visible in the next field. This produces incompatibility edges inside an anchor fiber.

The criterion was exhaustively checked on all 10,094 co-observed within-anchor field-pair/action comparisons: an internal conflict occurs iff the two current fields differ in at least one winning-agent row. Mismatches: 0.

## chi >= 3 groups

The unique chi=7 group (future_id 0) is maximally clipped: all 20 off-diagonal anchor-future entries are Delta-W=-1, i.e. the absolute future field is zero. It has 44 vertices and 224 internal edges. Thirty non-unanimous actions create conflicts.

The two chi=4 groups have respectively 16 negative anchor entries (future_id 374; 12 vertices, 10 edges) and 16 negative entries (future_id 578; 6 vertices, 6 edges). The eight chi=3 groups have 12--19 negative entries. Thus high chromatic complexity is concentrated toward anchors with many clipped coordinates, although negative-entry count alone is not sufficient: many anchors with 16 or more negative entries remain chi=1.

## Reassessment of asymmetry

Difficult anchors have lower simple asymmetry on average, but negative-entry count and asymmetry are themselves correlated (r approximately -0.52 across the 625 anchors). The mechanistic analysis directly explains the negative-entry effect through clipping; it does not independently establish low asymmetry as a cause. The safer interpretation is therefore **clipping-induced hidden distinctions**, with symmetry/asymmetry retained as a secondary descriptor pending further analysis.

## Next question

Negative-entry count determines the number of coordinates at which the anchor map can hide distinctions, but not whether reachable current fields actually realize conflicting variants or whether the relevant alternative actions are co-observed. The next analysis should characterize this reachability/action-coverage condition and ask whether it predicts which high-clipping anchors become difficult.
