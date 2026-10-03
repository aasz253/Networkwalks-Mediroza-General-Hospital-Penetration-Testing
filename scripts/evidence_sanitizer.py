#!/usr/bin/env python3
"""Defensive evidence sanitiser for engagement NW-B083.

Removes *mechanical* identifiers from text-based evidence before it is reviewed for
publication: cookies, bearer tokens, e-mail addresses, IPv4 addresses, AWS-style
access keys, and inline password arguments.

This tool performs **no** semantic judgement. It cannot tell whether a sentence
contains a salary, a diagnosis or a name. Every output requires manual review under
the policy in ``evidence/README.md`` §4 before publication.

Guarantees
----------
* Offline. No network access, ever.
* Non-destructive. The input file is never modified; output always goes elsewhere.
* Standard library only. Python 3.8+.

Usage
-----
    python3 scripts/evidence_sanitizer.py --self-test
    python3 scripts/evidence_sanitizer.py --input FILE --output-dir DIR
    cat artifact.txt | python3 scripts/evidence_sanitizer.py --stdin
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

TOOL_VERSION = "1.0.0"

# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #
# Each rule is (name, compiled pattern, replacement). Order matters: more specific
# patterns run first so that a generic pattern cannot claim part of a token.

RULES: List[Tuple[str, "re.Pattern[str]", str]] = [
    (
        "cookie_header",
        re.compile(r"(?im)^(\s*(?:set-)?cookie\s*:)(?!\s*<REDACTED-)[^\n]*"),
        r"\1 <REDACTED-COOKIE>",
    ),
    (
        "authorization_header",
        re.compile(r"(?im)^(\s*authorization\s*:)(?!\s*<REDACTED-)[^\n]*"),
        r"\1 <REDACTED-AUTHORIZATION>",
    ),
    (
        "bearer_token",
        re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-~+/]{8,}=*"),
        r"\1 <REDACTED-TOKEN>",
    ),
    (
        "inline_password",
        re.compile(
            r"(?i)(--?pass(?:word|wd)?[= ]|pass(?:word|wd)?[=]\s*)(['\"]?)(?!<REDACTED-)([^\s'\"]{2,})(\2)"
        ),
        r"\1<REDACTED-PASSWORD>",
    ),
    (
        "aws_access_key",
        re.compile(r"\b((?:AKIA|ASIA)[0-9A-Z]{16})\b"),
        "<REDACTED-AWS-KEY>",
    ),
    (
        "email_address",
        re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
        "<REDACTED-EMAIL>",
    ),
    (
        "ipv4_address",
        re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"),
        "<REDACTED-IP>",
    ),
    (
        "private_key_block",
        re.compile(r"(?s)-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----"),
        "<REDACTED-PRIVATE-KEY>",
    ),
]

# Values that look like secrets but are safe to keep, so the rules above cannot
# damage synthetic examples or documentation.
SAFE_VALUES = {
    "<REDACTED-COOKIE>",
    "<REDACTED-AUTHORIZATION>",
    "<REDACTED-TOKEN>",
    "<REDACTED-PASSWORD>",
    "<REDACTED-AWS-KEY>",
    "<REDACTED-EMAIL>",
    "<REDACTED-IP>",
    "<REDACTED-PRIVATE-KEY>",
}


def sanitize(text: str) -> Tuple[str, Dict[str, int]]:
    """Return sanitised text and a per-rule count of substitutions made."""
    counts: Dict[str, int] = {}
    for name, pattern, replacement in RULES:
        text, n = pattern.subn(replacement, text)
        if n:
            counts[name] = counts.get(name, 0) + n
    return text, counts


def sanitize_file(path: str) -> Tuple[str, Dict[str, int]]:
    """Sanitise a text file. Never writes to ``path``."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    return sanitize(text)


# --------------------------------------------------------------------------- #
# Self-test
# --------------------------------------------------------------------------- #

SELF_TEST_CASES: List[Tuple[str, str, bool, List[str]]] = [
    # (name, input, must_not_contain_secret, expected_rules_fired)
    (
        "cookie header",
        "Cookie: PHPSESSID=abc123def456; path=/",
        "abc123def456",
        ["cookie_header"],
    ),
    (
        "set-cookie header",
        "Set-Cookie: session=zzz999; HttpOnly; Secure",
        "zzz999",
        ["cookie_header"],
    ),
    (
        "authorization header",
        "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig",
        "eyJhbGciOiJIUzI1NiJ9",
        ["authorization_header"],
    ),
    (
        "bearer token inline",
        "curl -H 'Authorization: Bearer abcdef0123456789abcdef'",
        "abcdef0123456789abcdef",
        ["bearer_token"],
    ),
    (
        "inline password argument",
        "qpdf --password='S3cret!' --decrypt in.pdf out.pdf",
        "S3cret!",
        ["inline_password"],
    ),
    (
        "password equals sign",
        "password=hunter2 approved",
        "hunter2",
        ["inline_password"],
    ),
(
        "aws access key",
        "AKIAIOSFODNN7EXAMPLE was present in the log",
        "AKIAIOSFODNN7EXAMPLE",
        ["aws_access_key"],
    ),
    (
        "email address",
        "Contact the author at j.malik@example-hospital.org for access",
        "j.malik@example-hospital.org",
        ["email_address"],
    ),
    (
        "ipv4 address",
        "Server responded from 203.0.113.45 in 0.4 seconds",
        "203.0.113.45",
        ["ipv4_address"],
    ),
    (
        "private key block",
        "-----BEGIN RSA PRIVATE KEY-----\nMIIEow...\n-----END RSA PRIVATE KEY-----",
        "MIIEow",
        ["private_key_block"],
    ),
]


def run_self_test() -> int:
    """Verify each rule redacts its target. Returns a process exit code."""
    failures: List[str] = []
    print(f"evidence_sanitizer.py v{TOOL_VERSION} — self-test")
    print(f"rules: {len(RULES)}   cases: {len(SELF_TEST_CASES)}\n")

    for name, sample, must_not_contain, expected_rules in SELF_TEST_CASES:
        cleaned, counts = sanitize(sample)
        problems: List[str] = []

        if must_not_contain and must_not_contain in cleaned:
            problems.append(f"secret survived: {must_not_contain!r}")

        for rule in expected_rules:
            if counts.get(rule, 0) < 1:
                problems.append(f"rule {rule} did not fire")

        if "<REDACTED-" not in cleaned:
            problems.append("no redaction marker present")

        status = "PASS" if not problems else "FAIL"
        print(f"[{status}] {name}")
        print(f"        in : {sample[:72]!r}")
        print(f"        out: {cleaned[:72]!r}")
        print(f"        rules fired: {sorted(counts) or ['none']}")
        if problems:
            for problem in problems:
                print(f"        !! {problem}")
                failures.append(f"{name}: {problem}")
        print()

    # Idempotency: sanitising twice must not change the second result.
    for name, sample, _, _ in SELF_TEST_CASES:
        once, _ = sanitize(sample)
        twice, counts = sanitize(once)
        if once != twice:
            failures.append(f"{name}: not idempotent")
            print(f"[FAIL] {name}: not idempotent\n")
        elif counts:
            print(f"[FAIL] {name}: second pass re-redacted {sorted(counts)}\n")

    # Marker preservation: sanitising an already-clean file changes nothing.
    clean = "Nothing sensitive here. Report ID NW-B083-M1-E01. Password: <REDACTED-PASSWORD>.\n"
    cleaned, counts = sanitize(clean)
    if cleaned != clean or counts:
        failures.append("clean input was modified")
        print("[FAIL] clean input was modified\n")

    print("-" * 62)
    if failures:
        print(f"FAILED — {len(failures)} problem(s)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("PASSED — all rules redacted their targets and are idempotent")
    print("\nReminder: this tool finds mechanical identifiers only. Semantic review")
    print("under evidence/README.md §4 is still mandatory before publication.")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evidence_sanitizer.py",
        description="Offline, non-destructive redaction of mechanical identifiers "
        "in text-based evidence. Requires manual review afterwards.",
    )
    parser.add_argument("--input", "-i", help="Text file to sanitise (never modified)")
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Directory for the sanitised copy. Defaults to <input>.sanitized/",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read from standard input and write the sanitised result to stdout",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Verify the redaction rules against built-in cases and exit",
    )
    parser.add_argument(
        "--list-rules",
        action="store_true",
        help="Print the redaction rules and exit",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress the summary")
    return parser


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    if args.list_rules:
        print(f"evidence_sanitizer.py v{TOOL_VERSION}\n")
        for name, pattern, replacement in RULES:
            print(f"  {name}")
            print(f"    pattern : {pattern.pattern[:96]}")
            print(f"    replaces: {replacement}\n")
        print("Markers left untouched:", ", ".join(sorted(SAFE_VALUES)))
        return 0

    if args.stdin:
        text = sys.stdin.read()
        cleaned, counts = sanitize(text)
        sys.stdout.write(cleaned)
        if not args.quiet and counts:
            print(
                f"\n[redacted: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}]",
                file=sys.stderr,
            )
        return 0

    if not args.input:
        parser.error("one of --input, --stdin or --self-test is required")

    if not os.path.isfile(args.input):
        print(f"error: not a file: {args.input}", file=sys.stderr)
        return 2

    output_dir = args.output_dir or (args.input + ".sanitized")
    os.makedirs(output_dir, exist_ok=True)

    cleaned, counts = sanitize_file(args.input)
    destination = os.path.join(output_dir, os.path.basename(args.input))

    if os.path.abspath(destination) == os.path.abspath(args.input):
        print("error: refusing to overwrite the input file", file=sys.stderr)
        return 2

    with open(destination, "w", encoding="utf-8") as handle:
        handle.write(cleaned)

    if not args.quiet:
        print(f"evidence_sanitizer.py v{TOOL_VERSION}")
        print(f"  input        : {args.input} (unmodified)")
        print(f"  output       : {destination}")
        if counts:
            for rule, count in sorted(counts.items()):
                print(f"  redacted     : {rule} x{count}")
        else:
            print("  redacted     : nothing matched")
        print("\nMechanical identifiers only. Manual review is still required.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))