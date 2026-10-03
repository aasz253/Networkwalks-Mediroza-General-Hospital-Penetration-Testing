# Scripts

Offline, standard-library-only Python utilities. **Neither script performs network
access**, and neither contains code that targets a live system.

| Script | Purpose |
| --- | --- |
| [`evidence_sanitizer.py`](./evidence_sanitizer.py) | Removes mechanical identifiers — cookies, bearer tokens, e-mail addresses, IP addresses, key material, inline password arguments — from text-based evidence |
| [`repo_checks.py`](./repo_checks.py) | Verifies internal consistency of the documentation set: links, CSV structure, ID references, CVSS vectors, secret patterns, stated counts |

Requirements: **Python 3.8+**, standard library only. No installation, no
dependencies, no configuration.

---

## 1. `evidence_sanitizer.py`

### Guarantees

| Guarantee | Detail |
| --- | --- |
| Offline | No socket is ever opened |
| Non-destructive | The input file is never modified; output goes to a new file or directory |
| Mechanical only | It cannot judge meaning — see the limitation below |
| Idempotent | Sanitising an already-sanitised file changes nothing |
| Testable | `--self-test` verifies every rule against built-in cases |

### Rules applied

| Rule | Target |
| --- | --- |
| `cookie_header` | `Cookie:` and `Set-Cookie:` header lines |
| `authorization_header` | `Authorization:` header lines |
| `bearer_token` | Bearer tokens appearing inline |
| `inline_password` | `--password=…`, `-p …`, `password=…` arguments |
| `aws_access_key` | `AKIA`/`ASIA`-prefixed access key identifiers |
| `email_address` | E-mail addresses |
| `ipv4_address` | IPv4 addresses |
| `private_key_block` | PEM private key blocks |

### Usage

```bash
# Verify the rules
python3 scripts/evidence_sanitizer.py --self-test

# What will it match?
python3 scripts/evidence_sanitizer.py --list-rules

# Sanitise a copy — the input is untouched
python3 scripts/evidence_sanitizer.py \
  --input evidence/raw/artifact.txt \
  --output-dir /tmp/nw-sanitized

# Pipe mode
cat artifact.txt | python3 scripts/evidence_sanitizer.py --stdin > sanitized.txt
```

### Demonstration on synthetic data

```bash
python3 scripts/evidence_sanitizer.py \
  --input scripts/sample-data/synthetic-sample-log.txt \
  --output-dir /tmp/nw-sanitizer-demo
```

[`sample-data/synthetic-sample-log.txt`](./sample-data/synthetic-sample-log.txt) is
**fabricated for demonstration** and contains no client data. The only real-looking
string in it is an RFC 5737 documentation IP address, which routes nowhere.

### Limitation that matters most

> **This tool finds mechanical identifiers. It cannot find meaning.** It will not
> recognise a salary, a diagnosis, a person's name in prose, or a shareholder
> value. Every output requires manual review under
> [`../evidence/README.md`](../evidence/README.md) §4, and two-person review before
> publication.

---

## 2. `repo_checks.py`

### Checks performed

| # | Check | Verifies |
| --- | --- | --- |
| 1 | Markdown links resolve | Every relative link points at an existing path; fenced code blocks are ignored |
| 2 | CSV structure | Consistent column counts and unique key columns in all three registers |
| 3 | Finding evidence IDs exist | Every evidence ID cited by a finding is registered |
| 4 | Finding IDs resolve | Every referenced finding has a record on disk |
| 5 | CVSS vectors consistent | No finding carries two different vectors; every vector has the eleven v4.0 base metrics with valid values |
| 6 | Secret patterns | No live-looking credential in any tracked text file |
| 7 | Severity distribution | The counts stated in prose match the risk register |
| 8 | Evidence artifact status | `artifact_present` is `YES`/`NO`, and any `YES` is flagged for human confirmation |

### Usage

```bash
python3 scripts/repo_checks.py           # summary
python3 scripts/repo_checks.py --verbose # every failure listed
python3 scripts/repo_checks.py --root /path/to/repo
```

### Exemptions, stated rather than hidden

| Exemption | Reason |
| --- | --- |
| `scripts/evidence_sanitizer.py` | Defines the secret patterns and carries test fixtures |
| `scripts/repo_checks.py` | Same |
| `scripts/sample-data/` | Deliberately contains synthetic secret-shaped values |
| Any value containing `REDACTED`, `SYNTHETIC`, `EXAMPLE`, `PLACEHOLDER` | Placeholder, not a secret |

### Limitation

> **These checks verify internal consistency, not truth.** They confirm that a
> finding, a vector and a register row agree with each other. They cannot confirm
> that any recorded observation actually occurred. A repository of entirely fictional
> findings would pass every check.

---

## 3. What is deliberately absent

| Not present | Reason |
| --- | --- |
| Any script that sends a request | Repository tooling must never touch the target |
| Exploit payloads or payload generators | Out of scope; unethical to publish against a named target |
| Credential-attack tooling | Prohibited; unnecessary once minimal validation was achieved |
| Port or host scanners | Off-target risk |
| Unarchiving or parsing of client artifacts | Would require handling data this repository refuses to hold |
| Automatic finding generation | A finding requires judgement; a script would fabricate one |
| Automatic CVSS scoring from a chosen band | Would produce numbers nobody derived |

---

## 4. CI

| Workflow | Trigger | What it runs |
| --- | --- | --- |
| [`documentation-check.yml`](../.github/workflows/documentation-check.yml) | Push and pull request | Both scripts, offline |
| [`ci.yml`](../.github/workflows/ci.yml) | Push and pull request | Python byte-compilation across the tree |

Neither workflow installs dependencies or reaches the network. Both are expected to
pass on a clean checkout with Python 3.8 or later.

---

## 5. Adding a script

| Requirement | Reason |
| --- | --- |
| Standard library only | No supply-chain surface, no install step |
| No network access | The repository must never interact with a target |
| `--self-test` or an equivalent check | Untested defensive tooling is a liability |
| Documented limitation | A reader must know what the tool does **not** do |
| Idempotent where it rewrites files | Re-running must not compound changes |