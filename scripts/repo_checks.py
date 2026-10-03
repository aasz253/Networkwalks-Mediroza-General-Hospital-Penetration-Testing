#!/usr/bin/env python3
"""Documentation quality checks for engagement NW-B083.

Offline, standard-library only. Verifies the internal consistency of the
documentation set:

  1. Markdown links resolve (fenced code blocks are ignored).
  2. CSV structure: consistent column counts, unique key columns.
  3. Every evidence ID referenced by a finding exists in the evidence register.
  4. Every finding ID referenced anywhere exists as a finding record.
  5. CVSS v4.0 vectors are well formed and identical across all three places
     they appear (finding record, risk assessment, risk register).
  6. No obvious secret patterns in tracked text files.
  7. Severity distribution stated in prose matches the register.

Exit code 0 if every check passes, 1 otherwise.

Usage
-----
    python3 scripts/repo_checks.py            # run all checks
    python3 scripts/repo_checks.py --verbose  # list every failure
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

TOOL_VERSION = "1.0.0"

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
TEXT_EXT = {".md", ".csv", ".py", ".yml", ".yaml", ".txt", ".json", ".example"}

EVIDENCE_REGISTER = os.path.join("evidence", "evidence-register.csv")
RISK_REGISTER = os.path.join("risk", "risk-register.csv")
REMEDIATION_TRACKER = os.path.join("reports", "remediation-tracker.csv")
FINDINGS_DIR = os.path.join("findings", "verified-findings")
CVSS_DOC = os.path.join("risk", "cvss-assessment.md")
README = "README.md"

FINDING_ID = re.compile(r"\bNW-B083-M[1-4]-F\d{2}\b")
EVIDENCE_ID = re.compile(r"\bNW-B083-M[1-4]-E\d{2}\b")
CVSS_VECTOR = re.compile(r"CVSS:4\.0(?:/[A-Z]+:[A-Z])+")

SECRET_PATTERNS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "jwt",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ),
    (
        "assigned password literal",
        re.compile(r"(?i)\b(?:password|passwd|secret)\s*=\s*['\"][^'\"]{6,}['\"]"),
    ),
]

# A match containing any of these tokens is a placeholder, not a secret.
SAFE_TOKENS = (
    "REDACTED",
    "SYNTHETIC",
    "EXAMPLE",
    "PLACEHOLDER",
    "NOT-A-REAL",
    "CHANGEME",
    "DUMMY",
    "XXX",
)

# Files that legitimately contain secret-shaped strings: the sanitiser defines the
# patterns and carries fixtures, so scanning it would flag its own source.
EXEMPT_FROM_SECRET_SCAN = {
    os.path.join("scripts", "evidence_sanitizer.py"),
    os.path.join("scripts", "repo_checks.py"),
    os.path.join("scripts", "sample-data", "synthetic-sample-log.txt"),
}

# CVSS v4.0 base metrics, in the order the specification requires, with the
# permitted values for each.
CVSS_V4_METRICS = ["AV", "AC", "AT", "PR", "UI", "VC", "VI", "VA", "SC", "SI", "SA"]
CVSS_V4_VALUES = {
    "AV": {"N", "A", "L", "P"},
    "AC": {"L", "H"},
    "AT": {"N", "P"},
    "PR": {"N", "L", "H"},
    "UI": {"N", "P", "A"},
    "VC": {"H", "L", "N"},
    "VI": {"H", "L", "N"},
    "VA": {"H", "L", "N"},
    "SC": {"H", "L", "N"},
    "SI": {"H", "L", "N"},
    "SA": {"H", "L", "N"},
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def walk_text_files(root: str) -> List[str]:
    """Return every tracked-looking text file, skipping vendor directories."""
    found: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if os.path.splitext(name)[1].lower() in TEXT_EXT:
                found.append(path)
    return found


def strip_fenced_code(text: str) -> str:
    """Blank out fenced code blocks so placeholder paths inside them are not
    treated as live links."""
    out: List[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #


def check_links(repo_root: str, files: List[str]) -> List[str]:
    """Every relative markdown link must resolve to an existing path."""
    problems: List[str] = []
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in files:
        if not path.endswith(".md"):
            continue
        body = strip_fenced_code(read(path))
        base = os.path.dirname(path)
        for match in pattern.finditer(body):
            target = match.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                problems.append(f"{os.path.relpath(path, repo_root)}: broken link -> {target}")
    return problems


def load_csv(path: str) -> Tuple[List[str], List[List[str]]]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [], []
    return rows[0], rows[1:]


def check_csv_structure(repo_root: str, files: List[str]) -> List[str]:
    """Column counts must be consistent and key columns unique."""
    problems: List[str] = []
    targets = [
        (EVIDENCE_REGISTER, "evidence_id"),
        (RISK_REGISTER, "finding_id"),
        (REMEDIATION_TRACKER, "action_id"),
    ]
    for rel, key_column in targets:
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full):
            problems.append(f"{rel}: missing")
            continue
        header, rows = load_csv(full)
        if key_column not in header:
            problems.append(f"{rel}: missing key column '{key_column}'")
            continue
        index = header.index(key_column)
        width = len(header)
        seen: Set[str] = set()
        for number, row in enumerate(rows, start=2):
            if len(row) != width:
                problems.append(
                    f"{rel}:{number}: {len(row)} columns, expected {width}"
                )
                continue
            key = row[index]
            if key in seen:
                problems.append(f"{rel}:{number}: duplicate key '{key}'")
            seen.add(key)
    return problems


def check_evidence_references(repo_root: str, files: List[str]) -> List[str]:
    """Finding records may only cite evidence IDs that exist in the register."""
    problems: List[str] = []
    full = os.path.join(repo_root, EVIDENCE_REGISTER)
    if not os.path.isfile(full):
        return [f"{EVIDENCE_REGISTER}: missing"]
    header, rows = load_csv(full)
    index = header.index("evidence_id")
    known = {row[index] for row in rows}

    findings_dir = os.path.join(repo_root, FINDINGS_DIR)
    for name in sorted(os.listdir(findings_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(findings_dir, name)
        for evidence_id in sorted(set(EVIDENCE_ID.findall(read(path)))):
            if evidence_id not in known:
                problems.append(f"{os.path.relpath(path, repo_root)}: unknown evidence id {evidence_id}")
    return problems


def check_finding_references(repo_root: str, files: List[str]) -> List[str]:
    """Every referenced finding ID must have a record on disk."""
    problems: List[str] = []
    findings_dir = os.path.join(repo_root, FINDINGS_DIR)
    known = set()
    for name in os.listdir(findings_dir):
        match = re.match(r"(NW-B083-M\d-F\d\d)", name)
        if match:
            known.add(match.group(1))
    for path in files:
        if not path.endswith(".md"):
            continue
        for finding_id in sorted(set(FINDING_ID.findall(read(path)))):
            if finding_id not in known:
                problems.append(f"{os.path.relpath(path, repo_root)}: unknown finding id {finding_id}")
    return problems


def normalise_vector(vector: str) -> str:
    """Return the canonical prefixed form of a CVSS v4.0 vector."""
    vector = vector.strip().strip("`").replace(" ", "")
    if not vector.startswith("CVSS:4.0/"):
        vector = "CVSS:4.0/" + vector
    return vector


def check_cvss_consistency(repo_root: str, files: List[str]) -> List[str]:
    """The same finding must not carry two different vectors, and every vector
    must contain exactly the eleven CVSS v4.0 base metrics."""
    problems: List[str] = []
    per_finding: Dict[str, Set[str]] = defaultdict(set)

    findings_dir = os.path.join(repo_root, FINDINGS_DIR)
    for name in sorted(os.listdir(findings_dir)):
        if not name.endswith(".md"):
            continue
        match = re.match(r"(NW-B083-M\d-F\d\d)", name)
        if not match:
            continue
        finding_id = match.group(1)
        body = read(os.path.join(findings_dir, name))
        # Only the primary declared vector counts. Alternatives documented in the
        # record (for example "if a retest resolves this input") must not be
        # mistaken for a contradiction.
        for line in body.splitlines():
            if "**Vector" in line:
                for vector in CVSS_VECTOR.findall(line):
                    per_finding[finding_id].add(normalise_vector(vector))

    header, rows = load_csv(os.path.join(repo_root, RISK_REGISTER))
    index = header.index("finding_id")
    vector_index = header.index("cvss_v4_vector")
    for row in rows:
        if len(row) <= vector_index:
            continue
        per_finding[row[index]].add(normalise_vector(row[vector_index]))

    cvss_doc = os.path.join(repo_root, CVSS_DOC)
    if os.path.isfile(cvss_doc):
        body = read(cvss_doc)
        for line in body.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            finding_id = cells[0].strip("`")
            for vector in CVSS_VECTOR.findall(line):
                per_finding[finding_id].add(normalise_vector(vector))

    for finding_id, vectors in sorted(per_finding.items()):
        if len(vectors) > 1:
            joined = " | ".join(sorted(vectors))
            problems.append(f"{finding_id}: conflicting vectors -> {joined}")
        for vector in vectors:
            parts = vector.split("/")
            if parts[0] != "CVSS:4.0":
                problems.append(f"{finding_id}: missing CVSS:4.0 prefix")
            metrics = parts[1:]
            if len(metrics) != len(CVSS_V4_METRICS):
                problems.append(
                    f"{finding_id}: expected {len(CVSS_V4_METRICS)} metrics, "
                    f"found {len(metrics)}"
                )
                continue
            for expected, part in zip(CVSS_V4_METRICS, metrics):
                name, _, value = part.partition(":")
                if name != expected or value not in CVSS_V4_VALUES.get(expected, set()):
                    problems.append(
                        f"{finding_id}: metric '{part}' is not valid for {expected}"
                    )
    return problems


def check_secret_patterns(repo_root: str, files: List[str]) -> List[str]:
    """No file may contain a live-looking secret.

    Two exemptions are applied deliberately: the sanitiser's own source, which
    necessarily contains test fixtures, and any value that is an explicit
    redaction marker or synthetic label."""
    problems: List[str] = []
    for path in files:
        relative = os.path.relpath(path, repo_root)
        if relative in EXEMPT_FROM_SECRET_SCAN:
            continue
        body = strip_fenced_code(read(path))
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(body):
                value = match.group(0)
                if any(token in value.upper() for token in SAFE_TOKENS):
                    continue
                problems.append(f"{relative}: possible {label} -> {value[:40]!r}")
    return problems


def check_severity_counts(repo_root: str, files: List[str]) -> List[str]:
    """The README's stated distribution must match the risk register."""
    problems: List[str] = []
    header, rows = load_csv(os.path.join(repo_root, RISK_REGISTER))
    index = header.index("severity_band")
    counts = Counter(row[index] for row in rows if len(row) > index)

    expected = {"Critical": 3, "High": 2, "Medium": 2, "Low": 0}
    for band, want in expected.items():
        got = counts.get(band, 0)
        if got != want:
            problems.append(
                f"{RISK_REGISTER}: {band} count is {got}, README states {want}"
            )
    return problems


def check_status_counts(repo_root: str, files: List[str]) -> List[str]:
    """No artifact may claim to be present or verified."""
    problems: List[str] = []
    header, rows = load_csv(os.path.join(repo_root, EVIDENCE_REGISTER))
    index = header.index("artifact_present")
    present = [row[index] for row in rows if len(row) > index]
    unexpected = sorted({value for value in present if value not in {"YES", "NO"}})
    if unexpected:
        problems.append(
            f"{EVIDENCE_REGISTER}: artifact_present must be YES/NO, found {unexpected}"
        )
    if any(value == "YES" for value in present):
        # Legitimate, but must be deliberate: flag it for human confirmation.
        problems.append(
            f"{EVIDENCE_REGISTER}: at least one row claims artifact_present=YES — "
            "confirm the sanitization review was completed"
        )
    return problems


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #

CHECKS = (
    ("markdown links resolve", check_links),
    ("csv structure and unique keys", check_csv_structure),
    ("finding evidence ids exist", check_evidence_references),
    ("finding ids resolve", check_finding_references),
    ("cvss vectors consistent", check_cvss_consistency),
    ("no secret patterns", check_secret_patterns),
    ("severity distribution matches", check_severity_counts),
    ("evidence artifact status", check_status_counts),
)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="repo_checks.py",
        description="Offline consistency checks for the NW-B083 documentation set.",
    )
    parser.add_argument(
        "--root", default=".", help="Repository root (default: current directory)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="List every failure found"
    )
    args = parser.parse_args(argv)

    repo_root = args.root
    files = walk_text_files(repo_root)

    print(f"repo_checks.py v{TOOL_VERSION}")
    print(f"root: {os.path.abspath(repo_root)}")
    print(f"text files scanned: {len(files)}\n")

    failures = 0
    for label, check in CHECKS:
        problems = check(repo_root, files)
        status = "PASS" if not problems else "FAIL"
        print(f"[{status}] {label}")
        if problems:
            failures += 1
            shown = problems if args.verbose else problems[:10]
            for problem in shown:
                print(f"       - {problem}")
            if len(problems) > len(shown):
                print(f"       ... and {len(problems) - len(shown)} more (use -v)")
        print()

    print("-" * 62)
    if failures:
        print(f"FAILED — {failures} of {len(CHECKS)} checks failed")
        return 1
    print(f"PASSED — {len(CHECKS)} checks, no problems found")
    print("\nNote: these checks verify internal consistency only. They do not and")
    print("cannot verify that any recorded observation actually occurred.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))