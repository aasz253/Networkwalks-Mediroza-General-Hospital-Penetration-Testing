# Authorization and Scope

**Engagement ID:** `NW-B083` · **Project week:** Week 4 (final project)

> **Source of truth.** The source lab record states:
> *"This document is produced by Networkwalks for educational purposes only. The
> target has been authorised for security testing... The target is owned/client by
> Networkwalks."*
> That provider statement is the authorisation basis for this engagement and is
> the controlling instrument. Where this file and the provider's instrument
> differ, the provider's instrument governs.

---

## 1. Authorization basis

| Item | Value |
| --- | --- |
| Engagement type | Authorised black-box web application penetration test |
| Authorising party | Networkwalks |
| Client of record | Mediroza General Hospital (training scenario) |
| Target ownership | Networkwalks (per the provider statement) |
| Authorization statement | Provider-stated authorisation for security testing; educational purpose |
| Authorization holder | Antony Sifuna (`SifunaCodex`), intern |
| Reference | `NW-B083` |
| Environment type | **Training / lab target.** Not a production hospital system. |

### 1.1 Training-target consequence

Because the target is a lab environment:

- The data exposed is **synthetic**. Salary figures, shareholder records and
  patient-report content are constructed for the exercise.
- Findings are assessed against **real-world severity**, not lab difficulty.
  A Critical rating here describes what the same defect would mean in production.
- Techniques are recorded for education. Applying them to a system without
  written owner permission is prohibited.

### 1.2 Non-ambiguity rule

Where an action is ambiguous with respect to authorisation, it is not performed;
clarification is requested in writing from the instructor or engagement
supervisor and recorded in [`../CHANGELOG.md`](../CHANGELOG.md). Silence is not
authorisation.

---

## 2. Authorized target

| Field | Value |
| --- | --- |
| In-scope host | `https://medirozahospital.com` |
| Scheme | HTTPS |
| Paths in scope | `/patient/`, `/patient/login.php`, `/patient/reports/`, `/old/`, `/staff/`, `/robots.txt` |
| Paths observed but not exercised | `/staff/` — disclosed in `robots.txt`, not opened. Recorded as an observation; see [M1 attack surface](../milestones/M1-initial-access/attack-surface.md). |
| IP addresses | Not recorded in this repository |
| Subdomains | None enumerated or tested |

> ⚠️ **Unenumerated assets remain out of scope.** `robots.txt` disclosed exactly
> three paths. Anything not named there was not tested, and its existence is not
> asserted.

---

## 3. In-scope activities — as exercised

| # | Activity | Where documented |
| --- | --- | --- |
| S-1 | Passive reconnaissance: `robots.txt` retrieval | [M1 Step 1](../milestones/M1-initial-access/reconnaissance.md) |
| S-2 | Manual navigation of the authorized host | [M1 Step 2](../milestones/M1-initial-access/reconnaissance.md) |
| S-3 | Authentication error-handling analysis | [M1 Step 3](../milestones/M1-initial-access/vulnerability-analysis.md) |
| S-4 | Error-based SQL injection confirmation | [M1 Step 4](../milestones/M1-initial-access/vulnerability-analysis.md) |
| S-5 | Minimal authentication bypass to prove impact | [M1 Step 5](../milestones/M1-initial-access/proof-of-concept.md) |
| S-6 | Download of the three documents exposed by that bypass | [M1 Step 6](../milestones/M1-initial-access/proof-of-concept.md) |
| S-7 | Hash extraction from the encrypted PDFs | [M2 Step 1](../milestones/M2-data-extraction/tools-and-methods.md) |
| S-8 | Wordlist-based key recovery for those PDFs | [M2 Steps 2–3](../milestones/M2-data-extraction/results.md) |
| S-9 | Offline decryption of one report for metadata analysis | [M2 Step 4](../milestones/M2-data-extraction/tools-and-methods.md) |
| S-10 | PDF metadata extraction | [M3 Step 1](../milestones/M3-critical-data-exposure/exposure-analysis.md) |
| S-11 | Directory-listing review of `/old/` | [M3 Step 3](../milestones/M3-critical-data-exposure/exposure-analysis.md) |
| S-12 | Download and offline review of the exposed backup | [M3 Steps 4–5](../milestones/M3-critical-data-exposure/exposure-analysis.md) |
| S-13 | Reporting, evidence handling, redaction | [Reports](../reports/), [Evidence](../evidence/README.md) |

---

## 4. Explicitly out of scope — and not exercised

| # | Activity | Status |
| --- | --- | --- |
| O-1 | Any host other than the authorized target | Not exercised |
| O-2 | Denial-of-service, stress or load testing | Not exercised |
| O-3 | Destructive testing or data modification | Not exercised |
| O-4 | Credential stuffing, spraying, bulk password attacks against site accounts | Not exercised |
| O-5 | Social engineering, phishing, physical testing | Not exercised |
| O-6 | Exploitation beyond what was needed to substantiate a finding | Not exercised |
| O-7 | Persistence, lateral movement, pivoting | Not exercised |
| O-8 | Bulk extraction of the exposed dataset | **Observed but deliberately limited** — see §6 |
| O-9 | Opening or exercising `/staff/` | Not exercised |
| O-10 | Automated scanning of the host | Not exercised |
| O-11 | Cloud metadata, SSRF chaining, internal network access | Not exercised |
| O-12 | Any traffic generated by this repository or its CI | Never — enforced by design |

> **Note on O-8.** The backup file was downloaded because that *was* the
> substantiation of the finding. Once the exposed tables were identified, no
> further extraction was performed. This is the data-minimisation rule in
> practice: prove the exposure, then stop.

---

## 5. Test accounts

| Item | Value |
| --- | --- |
| Accounts supplied by client | None |
| Accounts self-registered | None |
| Access obtained | Via the injection-based authentication bypass (M1 Step 5) |
| Account affected | The administrative `admin` account |

No legitimate credentials were used, guessed or brute-forced anywhere in this
engagement. Document passwords were recovered offline against file hashes — they
are not site credentials, and no site account was accessed with them.

---

## 6. Data minimisation applied to M3

The exposure finding required proof that payroll and shareholder data was
readable. The following bounds were applied:

| Bound | Implementation |
| --- | --- |
| Prove, do not harvest | Only the `staff` and `shareholders` `INSERT` statements were extracted; no full-database export, no complete table dumps. |
| No bulk export | No automated extraction of all rows. |
| Format demonstration only | Rows were converted to a readable table to prove readability, then the values were discarded and are not published here. |
| Masked publication | This repository publishes table **schemas** and **data classes** only — no names, salaries, share percentages or share classes. |
| Corroboration, not accumulation | The `j.malik` author field was correlated against a single matching staff record to close the chain, then the correlation was documented and the personal data withheld. |

---

## 7. Time window

| Item | Value |
| --- | --- |
| Duration | 5 business days |
| Project week | Week 4 |
| Daily window | Not recorded in the source lab record |
| Escalation contact | Networkwalks instructor / cohort supervisor |

---

## 8. Change control

No scope change was requested or recorded during this engagement. `/old/` was
disclosed in `robots.txt` at the first reconnaissance step and therefore in scope
from the outset; M3 required no scope extension.

---

## 9. Verification checklist

| # | Item | State |
| --- | --- | --- |
| 1 | Authorisation basis identified and recorded | ✅ Provider statement captured |
| 2 | Target host confirmed | ✅ Single host |
| 3 | In-scope paths enumerated | ✅ Three paths from `robots.txt` |
| 4 | Prohibited activity list defined | ✅ [RoE](rules-of-engagement.md) §2 |
| 5 | Data-minimisation rule for M3 defined and applied | ✅ §6 above |
| 6 | Evidence storage and redaction policy defined | ✅ [Evidence standard](../evidence/README.md) |
| 7 | Confidentiality obligations recorded | ✅ [Ethical considerations](ethical-considerations.md) |
| 8 | No repository-generated traffic to target | ✅ Enforced; CI and scripts are offline |
| 9 | Batch number confirmed | ❌ **Discrepancy: B082 vs B083 — [project overview §9](project-overview.md#9-batch-discrepancy)** |
