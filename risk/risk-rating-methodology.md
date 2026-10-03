# Risk rating methodology

How severity bands, confidence and priority are assigned in engagement `NW-B083`.

---

## 1. Three separate questions

| Question | Instrument | Output |
| --- | --- | --- |
| **How bad is the impact?** | Severity band | 🔴 Critical / 🔴 High / 🟠 Medium / 🟢 Low |
| **How confident are we?** | Confidence | High / Medium / Low |
| **How sure is the rating itself?** | Rating status | Confirmed / Provisional |
| **How thoroughly is it substantiated?** | Verification status | Documented / Evidence-attached / Verified |

> These are frequently collapsed into a single number. Keeping them apart is what
> allows "Medium severity, High confidence, Provisional rating, Documented
> verification" to be a coherent and honest combination — as `NW-B083-M3-F01`
> demonstrates.

---

## 2. Severity bands

### 🔴 Critical
Unauthenticated remote path to sensitive data, or full defeat of the
authentication control. Immediate remediation.

| Applies to | Why |
| --- | --- |
| `M1-F02` | Authentication defeated in two requests with no credential |
| `M3-F02`* | Directory listing disclosed the backup's location and filename |
| `M3-F03` | Entire database anonymously downloadable in cleartext |

\* `M3-F02` is Critical **because** its contents included the backup. Directory
listing in isolation is a Medium finding. The rating is coupled to the contents and
is flagged provisional accordingly.

### 🔴 High
Practical path to confidential documents or recoverable credentials. Remediate
within days.

| Applies to | Why |
| --- | --- |
| `M1-F03` | Patient documents obtained without a credential, via the bypass |
| `M2-F01` | All three document keys recoverable offline by anyone holding a copy |

### 🟠 Medium
Information disclosure that materially assists other attacks, or a real weakness
with no independent data-compromise path. Remediate within weeks.

| Applies to | Why |
| --- | --- |
| `M1-F01` | Username enumeration — enabled a targeted attack but exposed no data |
| `M3-F01` | Metadata leak — decisive only in combination with `M3-F02`/`M3-F03` |

### 🟢 Low
Hardening item with no demonstrated compromise path. No finding in this engagement
reached Low.

---

## 3. Modifiers applied on top of the band

| Modifier | Effect |
| --- | --- |
| **Unauthenticated (`PR:N`)** | Raises operational urgency — no access control stands in the way |
| **No user interaction (`UI:N`)** | Raises urgency — no user can be tricked into it |
| **Data class** | 🔴 clinical / personal finance → highest business consequence regardless of technical band |
| **Detectability** | ⚪ undetectable offline → raises urgency; the control's only benefit was assumption |
| **Chain position** | A finding that enables other findings is prioritised even when its own band is lower |
| **Effort to fix** | A one-line configuration change outranks an architectural change at equal severity |

> **`M3-F01` is the clearest example of chain position mattering.** Banded Medium,
> yet it is the bridge to two Critical findings. It carries P0-adjacent urgency in
> the remediation plan while remaining Medium on its own merits. Band ≠ priority.

---

## 4. Confidence

| Level | Definition | Findings |
| --- | --- | --- |
| **High** | The weakness was observed directly and its effect confirmed | All 7 |
| **Medium** | The weakness was observed but its effect was inferred | 0 |
| **Low** | Suspected from indirect indicators only | 0 |

All seven are High confidence **because the effects were observed, not inferred** —
with one caveat recorded openly: `M1-F02`'s `VI:H` is inferred from the weakness
class even though the bypass itself was observed. The confidence applies to the
finding; the metric caveat applies to one vector component.

---

## 5. Rating status

| Status | Definition | Count |
| --- | --- | --- |
| **Confirmed** | Every metric input determining the band is directly evidenced, and any inferred input is named in the record | 4 |
| **Provisional** | One or more inputs missing or uncertain | 3 |

Which is which, and why:

| Finding | Status | Reason |
| --- | --- | --- |
| `M1-F01` | Confirmed | Two distinct responses observed |
| `M1-F02` | Confirmed | Authentication bypass executed; `VC` directly evidenced. `VI` is inferred from an administrative session and is named in the record. The band does not depend on it |
| `M1-F03` | **Provisional** | `PR` inferred from the testing path; direct unauthenticated access untested |
| `M2-F01` | **Provisional** | Key-reuse scope and mutation result unknown |
| `M3-F01` | Confirmed | Fields read directly |
| `M3-F02` | **Provisional** | `VC` coupled to unenumerated directory contents |
| `M3-F03` | Confirmed | Downloaded, restored and read |

---

## 6. Verification status

| Status | Definition | Count |
| --- | --- | --- |
| **Documented** | The engagement record contains the observed output | **7** |
| **Evidence-attached** | A sanitised, reviewed artifact exists and is referenced | **0** |
| **Verified** | Evidence-attached **and** independently reviewed against the claim | **0** |

> Every finding is `Documented`. None is `Verified`, because no artifact has been
> supplied. Publishing a Critical finding with reasoning but no artifact is
> defensible in a portfolio context and indefensible in a client report — which is
> why the distinction is enforced on every record rather than noted once.
> See [`../evidence/README.md`](../evidence/README.md) §5.

---

## 7. Prioritisation

Severity is not the same as priority. Priority combines severity, chain position,
detection and remediation cost.

| Priority | Meaning | Examples |
| --- | --- | --- |
| **P0** | Immediate. Exploitable now, or a root cause of other findings | Remove the backup; disable listing; parameterise the login query; move documents out of the web root |
| **P1** | Days. Detection and recurrence prevention | Bulk-access alerting; secrets management for document keys; CI gate against web-root artifacts; review prior access to the backup |
| **P2** | Weeks. Defence in depth and hygiene | Generic auth errors; metadata stripping in the export pipeline; rate limiting; SAST |
| **P3** | Ongoing. Programme maturity | External exposure monitoring; data inventory and retention; document signing; periodic retest |

### 7.1 Root-cause concentration

Seven root causes account for seven findings.

| Root cause | Findings | Fixed by one change? |
| --- | --- | --- |
| Unparameterised input reaching a SQL query | `M1-F02` | Partially — other parameters untested |
| Documents served as static files from the web root | `M1-F03`, `M2-F01` | ✅ Yes |
| No metadata stripping in the export path | `M3-F01` | ✅ Yes |
| Directory listing enabled | `M3-F02` | ✅ Yes |
| Backups permitted inside the web root | `M3-F02`, `M3-F03` | ✅ Yes |
| No owner or lifecycle for migration leftovers | `M3-F02`, `M3-F03` | ✅ Yes — the systemic cause |
| Distinct authentication error messages | `M1-F01` | ✅ Yes |
| Verbose database errors returned to the client | `M1-F02` | ✅ Yes |

> Six of the eight are configuration or process, not code. That is the single most
> useful conclusion for management: **this was not an advanced attack, and it is not
> expensive to fix.**

---

## 8. Business consequence weighting

Severity is technical; consequence is not. This engagement's data classes determine
the business outcome:

| Data class | Present | Consequence |
| --- | --- | --- |
| 🔴 Clinical | ✅ Patient records | Notifiable breach; potential patient harm; regulatory exposure |
| 🔴 Personal | ✅ Addresses and contact details | Privacy-law exposure; phishing and fraud risk |
| 🟠 Financial | ✅ Salary and shareholder data | Insider-trading and governance concerns; coercion risk; employment-relations exposure |
| 🟠 Internal | ✅ Account and infrastructure names | Credential attacks against other systems |
| ⚪ Unknown | Table of undetermined purpose | Cannot be assumed benign; recorded as an open question |

> **`M3-F03` combines the top three classes in a single anonymous download.** That
> combination, not any single weakness, is what makes it the engagement's
> highest-consequence finding.

---

## 9. Known weaknesses in this method

| # | Weakness | Mitigation applied |
| --- | --- | --- |
| 1 | CVSS v4.0's base metrics model system weaknesses; weak key strength in a file is an imperfect fit | Alternative framing (`PR:N/AT:P`) recorded in `M2-F01` §8.1 |
| 2 | CVSS cannot express "requires another finding" | Dependency recorded in narratives and in §3.3 of the CVSS assessment |
| 3 | CVSS measures impact in isolation, not chain role | Chain position applied separately in §3 |
| 4 | No base score computed | Policy in [`cvss-assessment.md`](./cvss-assessment.md) §4 |
| 5 | Bands are judgements, not measurements | Rationale recorded per finding; disagreement preserved rather than resolved |
| 6 | Data currency of the backup is unknown | Recorded as affecting notification scope, not the rating |

---

## 10. Related documents

| Document | Purpose |
| --- | --- |
| [`cvss-assessment.md`](./cvss-assessment.md) | Vector derivation and scoring policy |
| [`risk-register.csv`](./risk-register.csv) | Machine-readable register |
| [`../findings/README.md`](../findings/README.md) | Register of records and statuses |
| [`../reports/remediation-tracker.csv`](../reports/remediation-tracker.csv) | Actions, owners, priorities |
| [`../milestones/M4-final-report/risk-assessment.md`](../milestones/M4-final-report/risk-assessment.md) | Management-facing risk view |