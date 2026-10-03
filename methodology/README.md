# Methodology procedures

The procedures followed in engagement `NW-B083`, written as reusable and
**defensive** guidance.

> **Scope warning.** These procedures are documentation, not tooling. Nothing in
> this directory contains a script, payload collection or harness that targets a
> live system. Every procedure below states the authorisation precondition that
> must hold *before* the described step is performed.

---

## 1. Procedures

| # | Procedure | Covers |
| --- | --- | --- |
| 1 | [`reconnaissance.md`](./reconnaissance.md) | Passive and low-impact discovery; disclosure-file review; recording scope and stopping conditions |
| 2 | [`web-application-testing.md`](./web-application-testing.md) | Application mapping, request capture, error-handler review, technology inference vs. fingerprinting |
| 3 | [`authentication-assessment.md`](./authentication-assessment.md) | Response-discrepancy testing, injection at authentication boundaries, minimal-validation bypass demonstration |
| 4 | [`input-validation.md`](./input-validation.md) | Injection classes, encoding, error-based inference, and where to stop |
| 5 | [`access-control.md`](./access-control.md) | Object-level and function-level authorisation, direct object reference, privilege boundaries |
| 6 | [`file-security.md`](./file-security.md) | Document encryption strength, key strength assessment, metadata hygiene, backups as data assets |
| 7 | [`reporting.md`](./reporting.md) | Finding structure, status vocabulary, honest limitations, redaction in deliverables |

---

## 2. Framework alignment

| Framework | Use in this engagement |
| --- | --- |
| **OWASP WSTG** | Test phases and technique coverage |
| **PTES** | Engagement phases and reporting expectations |
| **OWASP Top 10 (2021)** | Finding categories |
| **OWASP ASVS** | Verification criteria in retest sections |
| **CVSS v4.0** | Standardised severity encoding — [`../risk/cvss-assessment.md`](../risk/cvss-assessment.md) |

Alignment narrative: [`../docs/methodology.md`](../docs/methodology.md).

---

## 3. Principles applied throughout

### 3.1 Minimal validation is sufficient

Where an error message, a difference in response, or a status code proves a
weakness, stop there. Data extraction beyond that point is unnecessary to
substantiate the finding and expands both risk and handling burden.

| Proven by | Further action avoided |
| --- | --- |
| A database syntax error | `UNION`-based extraction of other tables |
| A rendered portal after comment truncation | Enumerating other accounts or administrative functions |
| A directory index | Guessing any filename |

### 3.2 Absence of testing is never reported as absence of risk

| Category | Treatment |
| --- | --- |
| Tested and failed | Finding |
| Observed but not assessed | Observation |
| Not tested | **Untested hypothesis**, with the open question named |

The engagement's hypotheses H-4 to H-10 in
[`../milestones/M1-initial-access/vulnerability-analysis.md`](../milestones/M1-initial-access/vulnerability-analysis.md) §4 follow this rule.

### 3.3 Probability is recorded separately from observation

| Statement | Acceptable |
| --- | --- |
| "The error message revealed a MySQL syntax error" | ✅ Observed |
| "The stack is likely PHP with MySQL" | ✅ Labeled inference |
| "The application probably has other injectable parameters" | ✅ Recorded as hypothesis |
| "The application is probably vulnerable to SQLi everywhere" | ❌ Unsupported generalisation |

### 3.4 Handling burden is a test-design input

The exposure assessment read table structure and row counts, and stopped. Reading
row contents would have added no evidentiary value and multiplied the data-handling
risk. See [`file-security.md`](./file-security.md) §7.

### 3.5 Do not trust a control because it is present

| Control | Assumed state | Actual state found |
| --- | --- | --- |
| Password-protected documents | Protection in place | Keys recoverable by dictionary attack |
| Directory present | Contents controlled | Anonymous index plus a database backup |
| `robots.txt` | Search-engine guidance | Attack map for the engagement |
| Encrypted fields | Confidentiality | Cleartext in a backup |

---

## 4. Documentation conventions

| Convention | Rule |
| --- | --- |
| Severity | 🔴 Critical · 🔴 High · 🟠 Medium · 🟢 Low — [`../risk/risk-rating-methodology.md`](../risk/risk-rating-methodology.md) §2 |
| Verification | `Documented` · `Evidence-attached` · `Verified` — [`../findings/README.md`](../findings/README.md) §1 |
| Rating | `Confirmed` · `Provisional` — [`../risk/cvss-assessment.md`](../risk/cvss-assessment.md) §2 |
| Evidence IDs | `NW-B083-<MS>-E<nn>` — [`../evidence/README.md`](../evidence/README.md) §2 |
| Missing data | Write `UNKNOWN` or `PENDING — <what is required>`. Never omit the field and never guess |
| Credentials | Withheld entirely; never partially masked |
| Identified individuals | Masked, e.g. `j.m***`; referred to by role |
| Synthetic values | Labelled `SYNTHETIC — NOT CLIENT DATA` at the point of use |

---

## 5. What these procedures deliberately exclude

| Excluded | Reason |
| --- | --- |
| Automated exploitation or payload delivery | Out of scope and unnecessary |
| Brute-force or spraying tooling | Prohibited; minimal validation achieved the goal |
| Denial-of-service or stress testing | Prohibited |
| Unscoped port or host scanning | Off-target risk |
| Persistence, lateral movement, pivoting | Out of scope |
| Credential reuse testing against other accounts | Unnecessary once a bypass existed |
| Social engineering and physical testing | Out of scope |

Justification: [`../docs/rules-of-engagement.md`](../docs/rules-of-engagement.md) ·
tools actually used: [`../docs/tools-and-technologies.md`](../docs/tools-and-technologies.md)

---

## 6. Applying these procedures elsewhere

| Step | Action |
| --- | --- |
| 1 | Obtain and record written authorisation **before** any active step. Scope, timing, permitted techniques |
| 2 | Agree data-handling rules: what may be collected, what must be deleted, what must never be recorded |
| 3 | Agree evidence custody: where artifacts live, who reviews redactions, what may be published |
| 4 | Set stopping conditions per test class in advance |
| 5 | Follow the procedures, recording what was **not** done as carefully as what was |
| 6 | Report findings with honest status, retest criteria and residual uncertainty |
| 7 | Re-run the verification criteria after remediation — a fix is not demonstrated until it is retested |

> **Step 5 is the one most often skipped.** An assessment's value lies as much in
> the completeness of its record of untested areas as in its findings.