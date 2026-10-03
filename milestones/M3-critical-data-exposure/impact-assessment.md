# M3 — Impact Assessment

**Milestone:** Deep Reconnaissance / Critical Data Exposure · **Status:** ✅ Documented

> **Privacy note.** This assessment describes **classes** of data at risk. It
> contains no individual names, salary figures, share percentages, share classes
> or other personal values. Data classification detail is in
> [`data-classification.md`](./data-classification.md).

---

## 1. Impact summary

| Dimension | Assessment |
| --- | --- |
| **Confidentiality** | 🔴 **Severely compromised.** Staff compensation and shareholder registers readable anonymously in cleartext |
| **Integrity** | 🟠 **At risk, not demonstrated.** A database backup implies a restorable database; restoring it would overwrite production data. **No modification was attempted and none should be.** |
| **Availability** | 🟢 **No impact observed.** No disruption was caused by the assessment |
| **Privacy** | 🔴 **Severely compromised.** Personal financial data processed without the controls its sensitivity requires |
| **Regulatory** | 🔴 **Likely reportable.** Personal-data breach obligations are commonly triggered by unauthorised disclosure of identifiable personal data. **Client to determine with its own counsel.** |
| **Reputational** | 🔴 **Severe.** A healthcare provider exposing staff compensation invites criticism on internal fairness and on security competence simultaneously. |
| **Fraud / extortion** | 🟠 **Elevated.** Compensation data enables targeted phishing and extortion; shareholding data enables corporate targeting |

---

## 2. Impact by data class

| Data class | Sensitivity | Individual harm | Organisational harm |
| --- | --- | --- | --- |
| Staff monthly salary | 🔴 High | Embarrassment, grievance claims, coercion | Pay-equity criticism; industrial-relations exposure |
| Job title and department | 🟠 Medium | Reveals career position | Full org chart; maps access rights to people |
| Staff identifier / email | 🟠 Medium | Phishing and pretexting fuel | Enables targeted credential attacks |
| Shareholder name | 🔴 High | — | Governance and ownership disclosure |
| Share percentage | 🔴 High | — | Control structure; takeover and activist targeting |
| Share class | 🟠 Medium | — | Voting and dividend rights |

---

## 3. Individual impact

| Harm | Mechanism |
| --- | --- |
| **Financial privacy loss** | Salary is among the most sensitive personal financial attributes. Once public, irreversibly so. |
| **Targeted phishing** | A message referencing a real salary and a real role is dramatically more effective than a generic one. |
| **Extortion and coercion** | Knowledge of pay is leverage in workplace disputes, and in jurisdictions where such data is legally protected, in others too. |
| **Identity profiling** | Identifier plus role plus department enables a complete profile from a single source. |
| **Unauthorised disclosure** | Individuals had no expectation their compensation would be publicly retrievable. |
| **Irreversibility** | A password can be changed. A salary published and indexed cannot be recalled. |

---

## 4. Organisational impact

| Area | Consequence |
| --- | --- |
| **Governance** | Shareholding structure disclosed. In many jurisdictions this is disclosure-controlled. |
| **Control environment** | An IT Systems Administrator moved a database backup and it remained publicly served. That is a control-environment finding about process, not about a person. |
| **Security maturity** | The exposure required no technique — a browser and a URL from `robots.txt`. |
| **Detection** | Nothing in the described control set would have detected this. No monitoring, no alerting, no external scanning. |
| **Prior access** | **Unknown.** Whether the file had been downloaded before discovery cannot be determined from application-layer evidence. This materially affects the response. |
| **Extent** | Two tables were extracted. The total exposure is **at least** this large. |
| **Regulatory posture** | Breach-assessment and notification duties are likely engaged. Time-bound. |

---

## 5. Business consequence

| Consequence | Severity | Note |
| --- | --- | --- |
| Notification and remediation costs | 🔴 High | Legal, forensic, communications, credit/identity monitoring |
| Individual redress | 🔴 High | If notification is required, per-subject handling follows |
| Employment-relations exposure | 🟠 Medium-high | Compensation disclosure invites grievance and equality claims |
| Governance and disclosure failure | 🔴 High | Shareholding disclosure may breach corporate obligations independently of privacy law |
| Reputational damage in a care setting | 🔴 High | A healthcare provider is held to a higher visible standard |
| Breach-of-trust with staff | 🟠 Medium-high | Hard to rebuild once compensation is known to be publicly readable |
| Security programme credibility | 🟠 Medium | A missing default and a stale artefact undermine confidence in the wider programme |

---

## 6. Attacker's likely use of this data

| Objective | Feasibility | Notes |
| --- | --- | --- |
| Credential phishing with real context | 🔴 Trivially easy | Real name, real role, real department |
| Ransomware or extortion leverage | 🔴 High | Operational and personal leverage |
| Insider recruitment | 🟠 High | Compensation benchmarks enable targeted approaches |
| Competitive intelligence | 🟠 High | Shareholding structure, staff cost base |
| Pivot to further access | 🟠 High | A backup implies credentials, connection strings and schema — **not pursued; out of scope** |
| Extortion via data publication | 🔴 High | Credible given the data is already public |

> **Important boundary.** The assessment stopped at confirming the exposure.
> Connection strings, credentials, schema details beyond the two tables, and any
> attempt to use the file to reach the live database were **not** pursued.
> Reporting what the file implies is in scope; acting on it is not.

---

## 7. Severity

| Attribute | Assessment |
| --- | --- |
| Severity band | 🔴 **Critical** |
| Confidence | High — exposure directly observed |
| Vector | `AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N` |
| Derivation | [`../../risk/cvss-assessment.md`](../../risk/cvss-assessment.md) |

**Why Critical rather than High:** no authentication, no complexity, no
interaction, and a complete high-sensitivity dataset in cleartext. Any one of
those alone would justify High.

---

## 8. Factors affecting final impact

| Factor | Status | Effect |
| --- | --- | --- |
| Data currency | ❓ Unverified — filename says 2019 | **Staleness must not be assumed to reduce impact.** Historic salary data remains personal financial data. Currency affects remediation urgency and notification scope, not sensitivity. |
| Prior access | ❓ Undetermined | If downloaded before discovery, notification scope widens |
| Full extent | ❓ At least two tables | Total exposure may be larger |
| Other hosts | ❓ Not assessed | The same process may have failed elsewhere |
| Detection capability | ❓ Not assessed | If no monitoring exists, recurrence is likely |

---

## 9. Response priorities

Immediate, in order:

| # | Action | Rationale |
| --- | --- | --- |
| 1 | **Remove the backup from the web root** | Eliminates the exposure |
| 2 | **Disable directory listing on all directories** | Closes F06 |
| 3 | **Begin a breach assessment with qualified counsel** | Determines notification duties; time-bound |
| 4 | **Review web server logs for that path** | Establishes whether prior access occurred |
| 5 | Communicate internally to affected staff **after** counsel advises on wording | Reduces speculation; avoids premature or incorrect disclosure |
| 6 | Consider identity or financial monitoring support for affected individuals | A recognised mitigation where notification is required |
| 7 | Review for other legacy artefacts and other hosts | Establishes whether this is systemic |
| 8 | Assign ownership and a deadline for all legacy artefacts | Addresses the root cause |
| 9 | Implement scheduled external exposure monitoring | Prevents recurrence |
| 10 | Confirm data currency with the database owner | Informs urgency and scope |

> **Sequencing note.** Items 1 and 2 are technical and immediate. Items 3 onward are
> legal and organisational, and they depend on facts — including currency and prior
> access — that the client must establish. The temptation to notify before those
> facts are known should be resisted; the opposite temptation to delay should be
> resisted harder.

---

## 10. Assumptions

| # | Assumption | If wrong |
| --- | --- | --- |
| 1 | The target is a training environment with synthetic data | Findings remain valid as demonstrations; real data would add regulatory urgency |
| 2 | The data is genuinely payroll and shareholder data, per the table and column names | If the content differs, the classification changes — **the classification must be confirmed by the client** |
| 3 | No prior access control was applied to `/old/` | Observed directly |
| 4 | The backup is a genuine database backup | Structure observed directly |
| 5 | No defensive WAF or filtering exists in front of `/old/` | None observed; not tested with evasion in mind |

---

## 11. Related documents

| Document | Purpose |
| --- | --- |
| [`exposure-analysis.md`](./exposure-analysis.md) | Discovery record and root cause |
| [`data-classification.md`](./data-classification.md) | Schema and data-class detail |
| [`evidence.md`](./evidence.md) | Redaction standard and LLM caveat |
| [`../M4-final-report/impact-analysis.md`](../M4-final-report/technical-findings.md) | Consolidated business impact |
| [`../../reports/management-summary.md`](../../reports/management-summary.md) | Non-technical presentation |
