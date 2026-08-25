#!/usr/bin/env python3
"""
ABCW Season 2 - n=5 adaptive strategy experiment v0.1

Extension of the fixed-strategy simulator:
    s_i(t) in {-1,+1}
    win  -> keep strategy
    loss -> flip strategy
    payoff 0 -> keep strategy

Update order in one game t:
    1. payoff u(t) from a(t)
    2. reference signal sigma(t) from W(t), E, a(t)
    3. strategy update s(t) -> s(t+1)
    4. action update a(t) -> a(t+1)
       - winner / payoff 0: hold action
       - loser: use the NEW strategy s(t+1) and sigma(t)
       - loser with sigma=0: hold action
    5. W(t) -> W(t+1) from u(t)

Experiment:
    n=5, complete directed topology without self loops
    W(0)=E (all existing edges have weight 1)
    eta=1
    exhaustive 32 initial action profiles x 32 initial strategy profiles = 1024 cases

Strategy convention:
    +1 = trend-following (T)
    -1 = contrarian (C)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import itertools
import csv
import numpy as np


@dataclass
class ABCWAdaptiveConfig:
    E: np.ndarray
    eta: int = 1

    def __post_init__(self):
        self.E = np.asarray(self.E, dtype=int)
        if self.E.ndim != 2 or self.E.shape[0] != self.E.shape[1]:
            raise ValueError("E must be square.")
        if not np.all(np.isin(self.E, [0, 1])):
            raise ValueError("E entries must be 0 or 1.")
        if self.eta <= 0:
            raise ValueError("eta must be positive.")


class ABCWAdaptiveSimulator:
    def __init__(self, config, initial_actions, initial_strategy, initial_weights):
        self.E = config.E
        self.eta = int(config.eta)
        self.n = self.E.shape[0]
        self.actions = np.asarray(initial_actions, dtype=int).copy()
        self.s = np.asarray(initial_strategy, dtype=int).copy()
        self.W = np.asarray(initial_weights, dtype=int).copy()

        if self.actions.shape != (self.n,) or not np.all(np.isin(self.actions, [-1, 1])):
            raise ValueError("initial_actions must be +/-1 with shape (n,).")
        if self.s.shape != (self.n,) or not np.all(np.isin(self.s, [-1, 1])):
            raise ValueError("initial_strategy must be +/-1 with shape (n,).")
        if self.W.shape != (self.n, self.n) or np.any(self.W < 0):
            raise ValueError("initial_weights must be nonnegative with shape (n,n).")
        self.W[self.E == 0] = 0
        self.t = 0

    def payoff(self, actions):
        n_plus = int(np.sum(actions == 1))
        n_minus = int(np.sum(actions == -1))
        if n_plus == self.n or n_minus == self.n:
            return -np.ones(self.n, dtype=int)
        if n_plus == n_minus:
            return np.zeros(self.n, dtype=int)
        minority_action = 1 if n_plus < n_minus else -1
        return np.where(actions == minority_action, 1, -1).astype(int)

    def reference_signal(self, i, actions, W):
        incoming = np.where(self.E[:, i] == 1)[0]
        if incoming.size == 0:
            return 0.0
        incoming_weights = W[incoming, i]
        m_i = np.max(incoming_weights)
        if m_i <= 0:
            return 0.0
        max_nodes = incoming[incoming_weights == m_i]
        return float(np.mean(actions[max_nodes]))

    def update_strategy(self, s, payoffs):
        s_next = s.copy()
        s_next[payoffs < 0] *= -1
        return s_next

    def next_actions(self, actions, payoffs, W, s_next):
        sigmas = np.array(
            [self.reference_signal(i, actions, W) for i in range(self.n)],
            dtype=float
        )
        nxt = actions.copy()
        for i in range(self.n):
            if payoffs[i] >= 0:
                continue
            if np.isclose(sigmas[i], 0.0):
                continue
            value = s_next[i] * sigmas[i]
            nxt[i] = 1 if value > 0 else -1
        return nxt, sigmas

    def update_weights(self, W, payoffs):
        W_next = W.copy()
        for i in range(self.n):
            for j in range(self.n):
                if self.E[i, j] == 1:
                    W_next[i, j] = max(0, W[i, j] + self.eta * int(payoffs[i]))
                else:
                    W_next[i, j] = 0
        return W_next

    def state_key(self):
        # Exact dynamical state at the beginning of a game.
        return (
            tuple(self.actions.tolist()),
            tuple(self.s.tolist()),
            tuple(self.W.ravel().tolist()),
        )

    def step(self):
        a_t = self.actions.copy()
        s_t = self.s.copy()
        W_t = self.W.copy()

        u_t = self.payoff(a_t)
        s_next = self.update_strategy(s_t, u_t)
        a_next, sigma_t = self.next_actions(a_t, u_t, W_t, s_next)
        W_next = self.update_weights(W_t, u_t)

        rec = {
            "t": self.t,
            "actions": a_t,
            "strategy": s_t,
            "k_trend": int(np.sum(s_t == 1)),
            "payoffs": u_t,
            "sigma": sigma_t,
            "W": W_t,
            "next_strategy": s_next,
            "next_actions": a_next,
            "next_W": W_next,
        }

        self.actions = a_next
        self.s = s_next
        self.W = W_next
        self.t += 1
        return rec


def complete_directed_topology(n):
    E = np.ones((n, n), dtype=int)
    np.fill_diagonal(E, 0)
    return E


def pm_string(x):
    return "".join("+" if int(v) == 1 else "-" for v in x)


def strategy_string(x):
    return "".join("T" if int(v) == 1 else "C" for v in x)


def compact_weights(W, E):
    return tuple(int(W[i,j]) for i in range(W.shape[0]) for j in range(W.shape[1]) if E[i,j] == 1)


def run_case(initial_actions, initial_strategy, max_steps=1000):
    n = 5
    E = complete_directed_topology(n)
    sim = ABCWAdaptiveSimulator(
        ABCWAdaptiveConfig(E=E, eta=1),
        initial_actions=initial_actions,
        initial_strategy=initial_strategy,
        initial_weights=E.copy(),
    )

    seen = {}
    records = []
    max_weight = int(np.max(sim.W))
    for _ in range(max_steps):
        key = sim.state_key()
        if key in seen:
            start = seen[key]
            period = sim.t - start
            return {
                "status": "cycle",
                "cycle_start": start,
                "cycle_length": period,
                "records": records,
                "max_weight": max_weight,
            }
        seen[key] = sim.t
        rec = sim.step()
        records.append(rec)
        max_weight = max(max_weight, int(np.max(rec["next_W"])))

    return {
        "status": "no_exact_cycle_within_limit",
        "cycle_start": None,
        "cycle_length": None,
        "records": records,
        "max_weight": max_weight,
    }


def summarize_case(case_id, a0, s0, result):
    recs = result["records"]
    k_values = [r["k_trend"] for r in recs]
    distinct_actions = len({tuple(r["actions"]) for r in recs})
    distinct_strategies = len({tuple(r["strategy"]) for r in recs})
    final = recs[-1]
    w0 = 1
    maxw = result["max_weight"]

    # "drift_candidate" is conservative: no exact full-state cycle and weights exceed the initial scale substantially.
    drift_candidate = (
        result["status"] != "cycle"
        and maxw >= 20
    )

    return {
        "case_id": case_id,
        "initial_actions": pm_string(a0),
        "initial_strategy": strategy_string(s0),
        "initial_k_trend": int(np.sum(np.asarray(s0) == 1)),
        "status": result["status"],
        "cycle_start": result["cycle_start"],
        "cycle_length": result["cycle_length"],
        "distinct_action_states": distinct_actions,
        "distinct_strategy_states": distinct_strategies,
        "k_min": min(k_values),
        "k_max": max(k_values),
        "final_k_trend": final["k_trend"],
        "max_weight_observed": maxw,
        "drift_candidate": int(drift_candidate),
        "final_actions": pm_string(final["next_actions"]),
        "final_strategy": strategy_string(final["next_strategy"]),
    }


def main():
    n = 5
    profiles = list(itertools.product([-1, 1], repeat=n))
    rows = []
    results = {}
    case_id = 0
    for a0 in profiles:
        for s0 in profiles:
            result = run_case(a0, s0, max_steps=1000)
            results[case_id] = (a0, s0, result)
            rows.append(summarize_case(case_id, a0, s0, result))
            case_id += 1

    fields = list(rows[0].keys())
    with open("abcw_n5_adaptive_strategy_1024cases.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # Aggregate by initial k and outcome.
    agg = {}
    for r in rows:
        key = (r["initial_k_trend"], r["status"], r["cycle_length"] if r["status"] == "cycle" else "NA")
        agg[key] = agg.get(key, 0) + 1

    with open("abcw_n5_adaptive_strategy_aggregate.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["initial_k_trend", "status", "cycle_length", "count"])
        for key, count in sorted(agg.items(), key=lambda x: (x[0][0], str(x[0][1]), str(x[0][2]))):
            w.writerow([*key, count])

    # Representative traces: shortest period for each observed period + one drift candidate.
    cycle_rows = [r for r in rows if r["status"] == "cycle"]
    reps = []
    by_period = {}
    for r in cycle_rows:
        p = int(r["cycle_length"])
        by_period.setdefault(p, r["case_id"])
    for p in sorted(by_period):
        reps.append(by_period[p])
    drift = next((r["case_id"] for r in rows if r["drift_candidate"]), None)
    if drift is not None:
        reps.append(drift)

    with open("abcw_n5_adaptive_strategy_representative_traces.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        header = ["case_id","t","actions","strategy","k_trend","payoffs",
                  "sigma","weights","next_strategy","next_actions"]
        w.writerow(header)
        E = complete_directed_topology(n)
        for cid in reps:
            a0, s0, res = results[cid]
            # for traces, only first max(40, cycle_start+2*period) or 60 for noncycle
            if res["status"] == "cycle":
                limit = min(len(res["records"]), max(40, int(res["cycle_start"]) + 2*int(res["cycle_length"])))
            else:
                limit = min(len(res["records"]), 60)
            for rec in res["records"][:limit]:
                w.writerow([
                    cid, rec["t"], pm_string(rec["actions"]), strategy_string(rec["strategy"]),
                    rec["k_trend"], pm_string(rec["payoffs"]),
                    ";".join(f"{x:.3g}" for x in rec["sigma"]),
                    ";".join(map(str, compact_weights(rec["W"], E))),
                    strategy_string(rec["next_strategy"]), pm_string(rec["next_actions"])
                ])

    # Console summary
    from collections import Counter
    status_counts = Counter(r["status"] for r in rows)
    periods = Counter(int(r["cycle_length"]) for r in rows if r["status"] == "cycle")
    print("cases", len(rows))
    print("status", dict(status_counts))
    print("periods", dict(sorted(periods.items())))
    print("drift_candidates", sum(r["drift_candidate"] for r in rows))
    print("k range frequencies", Counter((r["k_min"], r["k_max"]) for r in rows))


if __name__ == "__main__":
    main()
