#!/usr/bin/env python3
"""Compute NSGA-II non-dominated Pareto fronts and stagnation checks for evolve candidates.

Input JSON schema (via file path or stdin):
{
  "objectives": {"quality": "max", "latency_ms": "min", "complexity_loc": "min"},
  "primary_objective": "quality",
  "stagnation_threshold_pct": 5.0,
  "candidates": [
    {"id": "gen0-base", "gen": 0, "family": "baseline", "metrics": {"quality": 0.72, "latency_ms": 120, "complexity_loc": 45}},
    ...
  ]
}
"""
import argparse
import json
import sys
from pathlib import Path


def dominates(a: dict, b: dict, objectives: dict[str, str]) -> bool:
    better_in_any = False
    for k, direction in objectives.items():
        va, vb = float(a["metrics"][k]), float(b["metrics"][k])
        if direction == "max":
            if va < vb:
                return False
            if va > vb:
                better_in_any = True
        elif direction == "min":
            if va > vb:
                return False
            if va < vb:
                better_in_any = True
        else:
            raise ValueError(f"Objective direction for '{k}' must be 'max' or 'min', got {direction!r}")
    return better_in_any


def rank_fronts(candidates: list[dict], objectives: dict[str, str]) -> list[list[dict]]:
    remaining = list(candidates)
    fronts = []
    while remaining:
        front = []
        for c in remaining:
            if not any(dominates(other, c, objectives) for other in remaining if other is not c):
                front.append(c)
        fronts.append(front)
        front_ids = {id(x) for x in front}
        remaining = [c for c in remaining if id(c) not in front_ids]
    return fronts


def check_stagnation(candidates: list[dict], primary: str, direction: str, threshold_pct: float) -> dict:
    by_gen: dict[int, list[float]] = {}
    for c in candidates:
        g = int(c.get("gen", 0))
        by_gen.setdefault(g, []).append(float(c["metrics"][primary]))
    gens = sorted(by_gen)
    best_per_gen = {g: (max(vals) if direction == "max" else min(vals)) for g, vals in by_gen.items()}
    gains = []
    for i in range(1, len(gens)):
        prev_v = best_per_gen[gens[i - 1]]
        cur_v = best_per_gen[gens[i]]
        if prev_v == 0:
            pct = 0.0 if cur_v == 0 else 100.0
        elif direction == "max":
            pct = ((cur_v - prev_v) / abs(prev_v)) * 100.0
        else:
            pct = ((prev_v - cur_v) / abs(prev_v)) * 100.0
        gains.append({"from_gen": gens[i - 1], "to_gen": gens[i], "improvement_pct": round(pct, 2)})

    stagnated = len(gains) >= 2 and all(g["improvement_pct"] < threshold_pct for g in gains[-2:])
    return {"best_per_gen": best_per_gen, "generation_gains": gains, "stagnated_stop_recommended": stagnated}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?", help="Path to candidates JSON file (or omit to read stdin).")
    args = ap.parse_args()

    try:
        raw = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
        data = json.loads(raw)
        objectives = data["objectives"]
        candidates = data["candidates"]
        primary = data.get("primary_objective") or next(iter(objectives))
        threshold = float(data.get("stagnation_threshold_pct", 5.0))

        fronts = rank_fronts(candidates, objectives)
        ranked = []
        for idx, front in enumerate(fronts, 1):
            for c in front:
                ranked.append({
                    "id": c["id"],
                    "gen": c.get("gen", 0),
                    "family": c.get("family", "unknown"),
                    "pareto_front": idx,
                    "dominated": idx > 1,
                    "metrics": c["metrics"],
                })

        stag = check_stagnation(candidates, primary, objectives[primary], threshold)
        out = {
            "status": "ok",
            "pareto_front_1": [c["id"] for c in fronts[0]] if fronts else [],
            "dominated_candidates": [r["id"] for r in ranked if r["dominated"]],
            "ranked": ranked,
            "stagnation": stag,
        }
        print(json.dumps(out, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
