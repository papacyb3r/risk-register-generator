#!/usr/bin/env python3
"""Risk Register Generator.

Reads a CSV of risks, scores each one (likelihood x impact on a 5x5 scale),
and writes a prioritised Markdown report with a heat map.

Usage:
    python risk_register.py sample_risks.csv
    python risk_register.py my_risks.csv --out register.md
"""
import argparse
import csv
import sys
from pathlib import Path

# Score bands for a 5x5 matrix (score = likelihood x impact).
BANDS = [(17, "Critical"), (10, "High"), (5, "Medium"), (1, "Low")]
REQUIRED = {"id", "risk", "likelihood", "impact", "owner", "treatment"}


def band(score):
    for floor, name in BANDS:
        if score >= floor:
            return name
    return "Low"


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"Missing columns: {', '.join(sorted(missing))}")
        risks = []
        for row in reader:
            try:
                likelihood, impact = int(row["likelihood"]), int(row["impact"])
            except ValueError:
                sys.exit(f"Risk {row['id']}: likelihood and impact must be whole numbers 1-5")
            if not (1 <= likelihood <= 5 and 1 <= impact <= 5):
                sys.exit(f"Risk {row['id']}: likelihood and impact must be between 1 and 5")
            row["likelihood"], row["impact"] = likelihood, impact
            row["score"] = likelihood * impact
            row["rating"] = band(row["score"])
            risks.append(row)
    return sorted(risks, key=lambda r: (-r["score"], r["id"]))


def heat_map(risks):
    cells = {}
    for r in risks:
        cells.setdefault((r["likelihood"], r["impact"]), []).append(r["id"])
    lines = ["| Likelihood \\ Impact | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
    for likelihood in range(5, 0, -1):
        row = [f"**{likelihood}**"]
        for impact in range(1, 6):
            ids = ", ".join(cells.get((likelihood, impact), [])) or "·"
            row.append(ids)
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render(risks):
    counts = {name: 0 for _, name in BANDS}
    for r in risks:
        counts[r["rating"]] += 1
    out = ["# Risk Register", ""]
    out.append("**Summary:** " + ", ".join(f"{n}: {counts[n]}" for _, n in BANDS))
    out += ["", "## Prioritised risks", "",
            "| ID | Risk | L | I | Score | Rating | Owner | Treatment |",
            "|---|---|---|---|---|---|---|---|"]
    for r in risks:
        out.append(f"| {r['id']} | {r['risk']} | {r['likelihood']} | {r['impact']} | "
                   f"{r['score']} | {r['rating']} | {r['owner']} | {r['treatment']} |")
    out += ["", "## Heat map", "", heat_map(risks), "",
            "Scoring: likelihood x impact. Critical 17-25, High 10-16, Medium 5-9, Low 1-4."]
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("risks", help="CSV: id,risk,likelihood,impact,owner,treatment")
    p.add_argument("--out", help="write the Markdown report to this file")
    args = p.parse_args()
    report = render(load(args.risks))
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Register written to {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
