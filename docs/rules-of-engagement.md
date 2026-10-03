# Rules of Engagement

**Engagement ID:** `NW-B083` · **Environment:** Networkwalks authorised training target

---

## 1. Purpose

Rules of engagement make testing **bounded, safe and reproducible**. They answer
three questions before any technical step:

1. **What may I touch?** → [`authorization-and-scope.md`](authorization-and-scope.md)
2. **How hard may I push?** → this document
3. **What must I do when something goes wrong?** → §5

Applied to a lab target, these rules additionally make the exercise
*transferable*: the habit of stopping at substantiation is the professional habit,
regardless of who owns the host.

---

## 2. Core rules and compliance record

| # | Rule | Compliance in this engagement |
| --- | --- | --- |
| ROE-1 | Authorized target only | ✅ Only `https://medirozahospital.com`. Three paths from `robots.txt` exercised; `/staff/` recorded but not opened. |
| ROE-2 | No availability impact | ✅ No flood, stress or load activity. All interaction was manual and sequential. |
| ROE-3 | No destructive action | ✅ No write, modify or delete operation. No account creation. No workflow triggered. |
| ROE-4 | No credential attacks against site accounts | ✅ No brute force, spraying or stuffing. `admin` was confirmed to exist via error-message analysis, then accessed via injection — not by guessing a password. |
| ROE-5 | Minimal, non-persistent validation | ✅ A single quote proved injection; one bypass payload proved impact. No stacked queries, no extraction, no persistence. |
| ROE-6 | Validate only to the substantiation threshold | ✅ Bypass used to demonstrate document access, not to enumerate the portal further. Backup review stopped at schema confirmation. |
| ROE-7 | Stop on real sensitive data | ✅ **Applied as a data-minimisation rule.** Data was synthetic, but the same discipline was used: identify the exposed tables, prove readability, publish no values. |
| ROE-8 | Evidence confidentiality | ✅ Passwords, salary values and shareholder identities withheld from publication. Redaction policy in [`../evidence/README.md`](../evidence/README.md). |
| ROE-9 | Never publish credentials | ✅ **Applied in M2.** Recovered passwords are characterised by strength class, not printed. |
| ROE-10 | No repository-generated traffic to target | ✅ No script, workflow or documented command in this repository contacts the target. All Python is offline. |
| ROE-11 | Educational use only | ✅ Recorded in [`../LICENSE`](../LICENSE) and [README §12](../README.md#12-authorization-confidentiality-and-data-handling-statement). |

---

## 3. What "minimal validation" looked like in practice

The engagement is a good demonstration of ROE-5 and ROE-6, because the maximum
available exploitation was far larger than what was performed.

| Weakness | Maximum available | Actually performed | Why this is sufficient |
| --- | --- | --- | --- |
| SQL injection in login | Full database extraction via `UNION`/`GROUP_CONCAT` | One quote → error; one comment bypass → portal | Error confirms injection; bypass confirms impact. Extraction would prove nothing more. |
| Authentication bypass | Administer the portal; modify records | Logged in, downloaded three documents, stopped | Confirms the bypass reaches protected data. Administration proves nothing extra. |
| Weak document passwords | Recover all keys, read all documents | All three keys recovered offline; **no document content read or published** | Key recoverability is the finding. Content is not needed to prove it. |
| Exposed SQL backup | Dump the entire database | Extracted only the `staff` and `shareholders` `INSERT` statements | Those two tables are the finding. A full dump is unnecessary exposure. |

---

## 4. Prohibited — quick reference

| Activity | Verdict in this engagement |
| --- | --- |
| Passive/active reconnaissance on the authorized host | ✅ Performed |
| Manual interaction with login and portal | ✅ Performed |
| Error-based injection confirmation | ✅ Performed |
| Minimal authentication bypass | ✅ Performed |
| Offline hash extraction and wordlist key recovery | ✅ Performed |
| Offline metadata extraction | ✅ Performed |
| Download of an exposed backup to prove the finding | ✅ Performed |
| Automated scanning of the host | ❌ Not performed |
| Bulk data extraction from the backup | ❌ Not performed — deliberately limited |
| Credential attack against site accounts | ❌ Not performed |
| Denial-of-service / load testing | ❌ Not performed |
| Data modification or deletion | ❌ Not performed |
| `/staff/` exploration | ❌ Not performed — out of exercised scope |
| Persistence, lateral movement, pivoting | ❌ Not performed |
| Publishing recovered passwords or personal data | ❌ Not performed — enforced by policy |

---

## 5. Stop conditions

Testing halts, and does not resume without clearance, on any of:

| Trigger | Action taken / that would be taken |
| --- | --- |
| Site availability degrades | Stop and notify the supervisor. Did not occur. |
| Real personal, medical or financial data encountered | Stop collection; retain only the minimum metadata to substantiate; notify supervisor. Did not occur (data was synthetic), but the data-minimisation discipline of this rule was applied regardless. |
| Authorization withdrawn or expired | Stop all testing. Did not occur. |
| Scope unclear for a discovered asset | Do not test; record as an observation. Applied to `/staff/`. |
| A vulnerability with severe real-world impact is found | Stop, preserve minimal evidence, escalate. Applied to F06/F07 — the exposure was documented and reported rather than mined. |

### Escalation

| Role | Contact |
| --- | --- |
| Instructor / cohort supervisor | Networkwalks B082 cohort |
| Provider (target owner) | Networkwalks |

---

## 6. Operational care

| Control | Applied |
| --- | --- |
| Request rate | Manual, one request at a time |
| Concurrency | None |
| Retries | None beyond ordinary re-navigation |
| Site responsiveness | No degradation observed or reported |
| Off-hours activity | None |
| Unenumerated assets | `/staff/` left untouched |

---

## 7. A RoE question this engagement raises

The document passwords in M2 were recovered by dictionary attack. Under a strict
reading of ROE-4, "no credential attacks" could be read to cover offline key
recovery against a file the tester already possesses.

The engagement's position: ROE-4 governs **access to systems**. The PDFs were
already downloaded through an authorised bypass, and offline analysis of a file in
the tester's own possession is file analysis, not credential attack against a
service. No rate limit was hit, no account was targeted, and no third party's
credentials were involved.

This distinction is worth stating explicitly in a report, because a reviewer
otherwise has to guess which reading was intended. If a strict reading is
preferred, the correct action is to obtain written clarification **before**
performing key recovery — not to omit the analysis from the write-up.
