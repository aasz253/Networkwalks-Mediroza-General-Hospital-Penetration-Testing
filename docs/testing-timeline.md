# Testing Timeline

**Engagement ID:** `NW-B083` · **Duration:** 5 business days · **Week 4 final project**

> **Status: EXECUTED.** All four milestones were completed. This file records what
> was done, in which milestone, and what evidence each step produced. Day-level
> hour allocation was not recorded in the source lab record and is marked as such
> rather than estimated.

---

## 1. Milestone schedule

| Milestone | Theme | Steps | Status |
| --- | --- | --- | --- |
| M1 | Initial Access | 6 | ✅ Complete |
| M2 | Data Extraction / File Security | 4 | ✅ Complete |
| M3 | Deep Reconnaissance / Critical Data Exposure | 5 | ✅ Complete |
| M4 | Penetration Testing Report | — | ✅ Complete |

---

## 2. M1 — Initial Access (6 steps)

| Step | Activity | Result | Evidence ID |
| --- | --- | --- | --- |
| 1 | Recon: fetch `robots.txt` | `Disallow: /patient/`, `/staff/`, `/old/` | `NW-B083-M1-E01` |
| 2 | Navigate to `/patient/` | Login page at `/patient/login.php` | `NW-B083-M1-E02` |
| 3 | Username enumeration | `bob` → *Username not found*; `admin` → *Incorrect password* → `admin` confirmed to exist | `NW-B083-M1-E03`, `E04` |
| 4 | SQL injection confirmation | Single quote in username → `mysqli_query()` SQL syntax warning | `NW-B083-M1-E05` |
| 5 | Authentication bypass | `admin' --` with any password → logged in; portal shows 3 reports | `NW-B083-M1-E06` |
| 6 | Document retrieval | Downloaded all three PDFs from the portal | `NW-B083-M1-E07`, `E08` |

**Analysis note (Step 1).** All three significant paths were disclosed in the
first request. `/patient/` drove M1, `/old/` drove M3, `/staff/` was recorded and
not exercised.

**Analysis note (Step 3).** Two distinct error messages for two distinct failure
modes is the finding. It is a confidentiality leak about account existence, and
it is also what made the bypass cheap: knowing `admin` was valid meant the
injector did not have to guess.

**Analysis note (Steps 4–5).** Validation was minimal by design. A single quote
produced a database-level error — sufficient proof with no data modification, no
stacked query, and no extraction. The bypass payload used a comment marker to
neutralise the password predicate rather than to guess a credential.

---

## 3. M2 — Data Extraction / Document Security (4 steps)

| Step | Activity | Result | Evidence ID |
| --- | --- | --- | --- |
| 1 | Extract `$pdf$` hash from each PDF via the Networkwalks Hash Calculator | Three hashes obtained | `NW-B083-M2-E01` |
| 2 | Built-in top-100 list against reports 1 and 2 | Both recovered immediately | `NW-B083-M2-E02`, `E03` |
| 3 | Report 3: built-in list exhausted, then instructor-supplied JTR list | Recovered after list escalation | `NW-B083-M2-E04` |
| 4 | `qpdf --decrypt` on report 3 | Unlocked copy produced for metadata analysis | `NW-B083-M2-E05` |

**Analysis note (Step 3).** This is the most instructive step in the milestone.
A failed small-list run is not evidence of a strong password; it is evidence of a
narrow wordlist. The third password looked materially stronger beside the first
two — it required character-class diversity — and still fell to a slightly larger
list.

**Analysis note (Step 4).** Decryption was necessary because a locked PDF exposes
almost no metadata. This is a general lesson: *protection mechanisms reduce
forensic visibility as well as confidentiality*, and the unlocked copy had to be
created deliberately and then discarded.

---

## 4. M3 — Deep Reconnaissance / Critical Data Exposure (5 steps)

| Step | Activity | Result | Evidence ID |
| --- | --- | --- | --- |
| 1 | `exiftool` on unlocked report 3 | `Author: j.malik`; comment *"DB backup moved to /old before site migration, do not delete"* | `NW-B083-M3-E01`, `E02` |
| 2 | Cross-check against Day-1 recon | `/old/` was already listed in `robots.txt` — independent corroboration | `NW-B083-M3-M1` (cross-ref `NW-B083-M1-E01`) |
| 3 | Request `/old/` | Directory listing enabled; `mediroza_db_backup_2019.sql` visible and downloaded | `NW-B083-M3-E03`, `E04` |
| 4 | Extract `staff` and `shareholders` `INSERT` rows; convert to readable tables | Confirmed cleartext salary and shareholder data | `NW-B083-M3-E05`, `E06` |
| 5 | Correlate `j.malik` against the staff table | Matched the IT Systems Administrator record — chain closed | `NW-B083-M3-E07` |

**Analysis note (Step 2).** The strongest single lesson in the engagement. A clue
found late pointed at a path found early. Neither fact alone was critical; the
conjunction was. Reconnaissance that stops after the first day discards half the
value of what it found.

**Analysis note (Step 5).** Correlation used one record to establish identity and
role, then stopped. That is the [data-minimisation rule](../docs/authorization-and-scope.md#6-data-minimisation-applied-to-m3)
in action: substantiate the chain, publish none of the personal data.

---

## 5. M4 — Penetration Testing Report

| Activity | Output | Location |
| --- | --- | --- |
| Consolidate findings | 7 findings with location and severity | [Findings summary](../reports/penetration-testing-report.md#5-summary-of-findings) |
| Write executive summary | Non-technical overview of the chain and the top risks | [Executive summary](../milestones/M4-final-report/executive-summary.md) |
| Derive CVSS v4.0 vectors | Per-metric rationale for all 7 findings | [CVSS assessment](../risk/cvss-assessment.md) |
| Write technical findings | Full finding records | [Technical findings](../milestones/M4-final-report/technical-findings.md) |
| Write remediation recommendations | 5 themes from the engagement, expanded to 8 prioritised actions | [Remediation plan](../milestones/M4-final-report/remediation-plan.md) |
| Build remediation tracker | CSV with owner, priority, retest criteria | [Tracker](../reports/remediation-tracker.csv) |
| Produce management summary | Board-level summary | [Management summary](../reports/management-summary.md) |
| Populate evidence register | 22 rows across M1–M3 | [Evidence register](../evidence/evidence-register.csv) |

---

## 6. Effort allocation

Actual hour allocation was not recorded. Recorded instead is the relative
emphasis visible in the step counts, which is what the engagement record supports.

| Workstream | Steps | Relative emphasis |
| --- | --- | --- |
| Reconnaissance and mapping | M1 steps 1–2, M3 step 2 | Moderate — recon was brief but decisive |
| Authentication and injection | M1 steps 3–5 | High — the decisive technical work |
| Access control / document retrieval | M1 step 6 | Low |
| Document security | M2 steps 1–4 | Moderate — four steps, three deliverables |
| Exposure investigation | M3 steps 3–5 | Moderate |
| Reporting | M4 | High — seven findings plus report set |

---

## 7. Progress log

| Milestone | Date | Steps completed | Evidence captured | Findings added | Blockers |
| --- | --- | --- | --- | --- | --- |
| M1 | _not recorded in source record_ | 6 of 6 | 8 registered / 0 artifacts attached | F01, F02, F03 | None |
| M2 | _not recorded in source record_ | 4 of 4 | 6 registered / 0 artifacts attached | F04 | None |
| M3 | _not recorded in source record_ | 5 of 5 | 8 registered / 0 artifacts attached | F05, F06, F07 | None |
| M4 | _not recorded in source record_ | — | n/a | Report set | None |

> Dates and hours are genuinely absent from the source record. They are left as
> `not recorded` rather than invented. If the daily notes are available, populate
> them from [`../templates/daily-progress-template.md`](../templates/daily-progress-template.md).

---

## 8. Deliverable acceptance

| Milestone | Acceptance criteria | Met |
| --- | --- | --- |
| M1 | Sensitive paths discovered; authentication weakness identified and proven; documents retrieved | ✅ |
| M2 | All three files assessed; key recovery method and escalation documented; verification approach stated | ✅ |
| M3 | Exposure discovered via independent corroborating paths; impact substantiated; evidence redacted | ✅ |
| M4 | All required report sections present; findings separated by verification status; limitations stated | ✅ |
| Cross-cutting | No credentials or personal data published; no repository-generated traffic to target | ✅ |
| Cross-cutting | Evidence artifacts sanitized and attached | ❌ Outstanding — [evidence §5](../evidence/README.md#5-closing-the-evidence-gap) |
| Cross-cutting | CVSS v4.0 numeric base scores computed | ❌ Outstanding — [CVSS §4](../risk/cvss-assessment.md#4-why-base-scores-are-not-printed-here) |
| Cross-cutting | Batch number reconciled | ❌ Outstanding — [overview §9](../docs/project-overview.md#9-batch-discrepancy) |
