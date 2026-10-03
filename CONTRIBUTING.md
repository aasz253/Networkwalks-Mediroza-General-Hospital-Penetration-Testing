# Contributing

Thanks for helping keep this an accurate, safe and useful technical record.
This repository has a deliberately high bar: **every claim must be traceable to
evidence, and no client-sensitive data may ever be committed.**

---

## 1. Before you contribute

Read, in order:

1. [`SECURITY.md`](./SECURITY.md) — handling rules and incident process
2. [`docs/authorization-and-scope.md`](./docs/authorization-and-scope.md) — what is authorized
3. [`docs/rules-of-engagement.md`](./docs/rules-of-engagement.md) — how testing is bounded
4. [`docs/ethical-considerations.md`](./docs/ethical-considerations.md) — confidentiality and evidence handling

If your contribution would require information you do not have, the correct
contribution is a clearly-marked `PENDING VERIFICATION` placeholder, not a
plausible guess.

---

## 2. Hard rules

These are not style preferences. Violating any of them makes a change ineligible
for merge.

| # | Rule |
| --- | --- |
| 1 | **Never** commit patient records, clinical data, salary figures, shareholder details, credentials, tokens, cookies, keys or raw unredacted evidence. |
| 2 | **Never** add tooling that contacts the client target, or that automates exploitation, credential attacks, denial-of-service or destructive activity. |
| 3 | **Never** state that a finding is verified unless a sanitized artifact exists in [`evidence/`](./evidence/README.md) and a matching row exists in [`evidence/evidence-register.csv`](./evidence/evidence-register.csv). |
| 4 | **Never** assign a CVSS score without a documented, evidence-based vector. |
| 5 | **Never** claim client review, approval or sign-off. |
| 6 | **Never** paste secrets into example commands, `.env.example`, or documentation. |
| 7 | Label every synthetic example `SYNTHETIC — NOT CLIENT DATA`. |
| 8 | Redact evidence manually after running the automated sanitizer, then update the register's `redaction_status`. |

---

## 3. Workflow

```bash
git clone https://github.com/SifunaCodex/networkwalks-b083-mediroza-pentest.git
cd networkwalks-b083-mediroza-pentest

git switch -c docs/short-descriptive-change

# edit files

python3 scripts/repo_checks.py          # must exit 0
git add -A
git commit -m "docs(scope): clarify authorized host definition"
git push origin docs/short-descriptive-change
```

Then open a pull request using the description below.

### Commit message convention

```
<type>(<scope>): <short summary>

types:   docs | evidence | risk | scripts | templates | ci | fix | chore
scopes:  scope, roe, methodology, m1, m2, m3, m4, findings, register, report,
         sanitizer, checks
```

Examples:

```
docs(m3): add redaction standard for salary exposure evidence
evidence(register): reserve M1 evidence rows E01-E05
risk(cvss): document provisional-rating rule for unverified findings
scripts(sanitizer): never write output to the input path
ci(checks): fail closed when CSV validation cannot run
```

---

## 4. Pull request description template

```markdown
## What changed
<!-- one paragraph -->

## Why
<!-- link to the milestone, finding or issue this supports -->

## Evidence linkage
<!-- Evidence IDs (NW-B083-<MS>-E<nn>) or Finding IDs (NW-B083-<MS>-F<nn>).
     Write "None — documentation only" if not applicable. -->

## Verification status
- [ ] No new findings are claimed as verified
- [ ] No CVSS score added without an evidence-based vector
- [ ] Any synthetic content is labelled `SYNTHETIC — NOT CLIENT DATA`

## Confidentiality self-check
- [ ] No client-sensitive data present
- [ ] No credentials, tokens, cookies or keys present
- [ ] No live-target tooling introduced
- [ ] `python3 scripts/repo_checks.py` exits 0
```

---

## 5. Style guide

### Markdown

- One `#` H1 per file, matching the file's purpose.
- Relative links only (`./docs/...`). No absolute URLs to internal files.
- Wrap lines at roughly 100 characters for readability in diffs.
- Use tables for structured data — they are what makes this repository auditable.
- Use `<details>` blocks for long procedures or verbose output.
- Mermaid diagrams live in [`diagrams/`](./diagrams/) as `.mmd` sources and are
  **embedded** into Markdown where they aid understanding. Keep `.mmd` files
  high-level: no real hostnames, no real internal architecture.

### Finding language

Use precise cybersecurity language and keep the epistemic status of every
sentence visible:

| Use | Avoid |
| --- | --- |
| "The response indicates the session cookie lacks the `Secure` attribute." | "The site is insecure." |
| "No evidence of successful exploitation was obtained." | "The vulnerability was exploited successfully." |
| "Hypothesis — untested." | Stating a hypothesis as a result. |
| "Verified — evidence `NW-B083-M1-E03`." | "Verified." |

### Finding IDs and evidence IDs

- Findings: `NW-B083-<milestone>-F<nn>` → `NW-B083-M1-F01`
- Evidence: `NW-B083-<milestone>-E<nn>` → `NW-B083-M1-E01`
- Candidates that turn out not to be findings still keep their ID, with
  `status: withdrawn` and a one-line reason. IDs are never reused.

---

## 6. Adding a finding

1. Copy [`findings/finding-template.md`](./findings/finding-template.md) to
   `findings/verified-findings/NW-B083-<MS>-F<nn>-<slug>.md`.
2. Fill every section. Where evidence is missing, write `PENDING VERIFICATION —
   required: <exactly what is needed>`. Do not delete the section.
3. Add a row to [`risk/risk-register.csv`](./risk/risk-register.csv) and to the
   finding summary table in [`README.md`](./README.md).
4. Add every supporting artifact to
   [`evidence/evidence-register.csv`](./evidence/evidence-register.csv).
5. Sanitize, manually review, and only then reference the image with a relative path.
6. Record the verification decision in the finding's `Status` field.

A finding with an empty evidence section is not ready for merge. It is fine as a
draft on a branch, provided it is marked `PENDING VERIFICATION`.

---

## 7. Adding evidence

1. Store the raw artifact **off-repository** in the access-controlled store.
2. Assign the next evidence ID for that milestone.
3. Run the sanitizer:
   ```bash
   python3 scripts/evidence_sanitizer.py --input <raw-file> --output-dir ./sanitized-out
   ```
4. Manually review the sanitized copy. The tool cannot detect every sensitive
   value — it does not understand free text in images, PDFs, or handwriting.
5. Place the reviewed copy in `evidence/screenshots/<MS>/` with the naming
   convention `<evidence-id>_<short-description>.<ext>`.
6. Add the register row and reference it from the finding with a relative path.

See [`evidence/README.md`](./evidence/README.md) for the full standard.

---

## 8. Validation

CI runs on every push and pull request. Locally:

```bash
python3 scripts/repo_checks.py                 # all checks
python3 scripts/repo_checks.py --verbose       # per-file detail
python3 scripts/repo_checks.py --json          # machine-readable
python3 scripts/evidence_sanitizer.py --self-test
```

The gate checks: Markdown relative-link integrity, CSV headers and shape, that
referenced evidence files exist, and that no obvious secret pattern is committed.
Secret matches are reported by **class and location only** — never by value.

The gate is offline and fails closed. See
[`.github/workflows/documentation-check.yml`](.github/workflows/documentation-check.yml).

---

## 9. Code of conduct

Be accurate, be respectful, and assume good faith. Disagreeing about a severity
rating is normal and productive; inflating a rating to look impressive, or
withholding a limitation because it weakens the report, is not acceptable.
