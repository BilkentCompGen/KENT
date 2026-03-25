#!/usr/bin/env python3
"""
compare_abundance.py — compare two pathogen abundance CSV files.

Usage:
    python compare_abundance.py <file1.csv> <file2.csv> [--output out.csv]

Outputs a table with columns for each file's values plus the difference.
Rows unique to one file are included with N/A for the missing side.
"""

import csv
import sys
import argparse
from pathlib import Path

NUMERIC_COLS = ["Count", "Proportion_All(%)", "Proportion_Classified(%)"]
KEY_COL = "Name"


def load_file(path: str) -> dict[str, dict]:
    rows = {}
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = row[KEY_COL]
            rows[key] = row
    return rows


def fmt(value, decimals=6):
    try:
        return f"{float(value):.{decimals}g}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "N/A"


def diff_str(a, b):
    try:
        d = float(b) - float(a)
        sign = "+" if d >= 0 else ""
        return f"{sign}{d:.6g}"
    except (TypeError, ValueError):
        return "N/A"


def compare(file1: str, file2: str, output: str | None):
    data1 = load_file(file1)
    data2 = load_file(file2)

    label1 = Path(file1).stem
    label2 = Path(file2).stem

    all_keys = sorted(set(data1) | set(data2))

    header = [KEY_COL]
    for col in NUMERIC_COLS:
        header += [f"{col} ({label1})", f"{col} ({label2})", f"{col} (diff)"]

    rows = []
    for key in all_keys:
        r1 = data1.get(key)
        r2 = data2.get(key)
        row = [key]
        for col in NUMERIC_COLS:
            v1 = r1[col] if r1 else None
            v2 = r2[col] if r2 else None
            row += [fmt(v1), fmt(v2), diff_str(v1, v2)]
        rows.append(row)

    # --- write output ---
    if output:
        with open(output, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Saved to {output}")
    else:
        # pretty-print to terminal
        col_widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))]
        sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
        fmt_row = lambda r: "| " + " | ".join(str(r[i]).ljust(col_widths[i]) for i in range(len(r))) + " |"

        print(sep)
        print(fmt_row(header))
        print(sep)
        for row in rows:
            in_only_1 = key in data1 and key not in data2
            in_only_2 = key not in data1 and key in data2
            print(fmt_row(row))
        print(sep)
        print(f"\nTotal rows: {len(rows)}  |  Only in {label1}: {sum(1 for k in all_keys if k not in data2)}  |  Only in {label2}: {sum(1 for k in all_keys if k not in data1)}  |  In both: {sum(1 for k in all_keys if k in data1 and k in data2)}")


def main():
    parser = argparse.ArgumentParser(description="Compare two pathogen abundance CSV files.")
    parser.add_argument("file1", help="First abundance CSV")
    parser.add_argument("file2", help="Second abundance CSV")
    parser.add_argument("--output", "-o", help="Save results to this CSV file (optional; prints to terminal if omitted)")
    args = parser.parse_args()
    compare(args.file1, args.file2, args.output)


if __name__ == "__main__":
    main()
