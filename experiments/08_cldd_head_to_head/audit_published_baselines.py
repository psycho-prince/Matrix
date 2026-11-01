#!/usr/bin/env python3
"""Audit published CLDD evaluation CSV baselines without claiming a fresh run.

Usage:
  python audit_published_baselines.py data/evaluate/data_frame.csv
"""
from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

STRATEGIES = ("FT", "EWC", "SI")
BOUNDARIES = ("abrupt", "gradual", "slow")
METRICS = (
    "ocl.accuracy_final",
    "ocl.accuracy_seen_avg",
    "ocl.backward_transfer",
    "ttt.accuracy",
)


def summarize(values: list[float]) -> dict[str, float | int | None]:
    clean = [v for v in values if math.isfinite(v)]
    if not clean:
        return {"n": 0, "mean": None, "sd": None}
    return {
        "n": len(clean),
        "mean": statistics.mean(clean),
        "sd": statistics.stdev(clean) if len(clean) > 1 else 0.0,
    }


def main(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("CSV contains no data rows.")
    required = {"strategy", "detector", "boundary", "seed", *METRICS}
    missing = required.difference(rows[0])
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    selected = [
        row for row in rows
        if row["strategy"] in STRATEGIES and row["detector"] == "oracle"
    ]
    report: dict = {
        "source_file": str(path),
        "source_type": "published CLDD evaluation CSV; not a fresh training run",
        "detector": "oracle",
        "strategies": {},
    }

    for strategy in STRATEGIES:
        subset = [r for r in selected if r["strategy"] == strategy]
        strategy_report = {
            "n_rows": len(subset),
            "unique_seeds": sorted({r["seed"] for r in subset}),
            "by_boundary": {},
            "overall": {},
        }
        for boundary in BOUNDARIES:
            group = [r for r in subset if r["boundary"] == boundary]
            strategy_report["by_boundary"][boundary] = {
                "n_rows": len(group),
                "metrics": {
                    metric: summarize([
                        float(row[metric]) for row in group
                        if row[metric] not in ("", "nan", "NaN")
                    ])
                    for metric in METRICS
                },
            }
        strategy_report["overall"] = {
            metric: summarize([
                float(row[metric]) for row in subset
                if row[metric] not in ("", "nan", "NaN")
            ])
            for metric in METRICS
        }
        report["strategies"][strategy] = strategy_report

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Provide path to CLDD data/evaluate/data_frame.csv")
    main(Path(sys.argv[1]))
