# Risk assessment

Severity, confidence, rating status and prioritisation for the seven findings.

---

## 1. Summary

| Band | Count | Findings |
| --- | --- | --- |
| 🔴 Critical | 3 | `M1-F02`, `M3-F02`, `M3-F03` |
| 🔴 High | 2 | `M1-F03`, `M2-F01` |
| 🟠 Medium | 2 | `M1-F01`, `M3-F01` |
| 🟢 Low | 0 | — |

| Axis | Result |
| --- | --- |
| Confidence | High on all seven — every effect was observed |
| Rating status | 4 Confirmed · 3 Provisional |
| Verification status | 7 Documented · 0 Evidence-attached · 0 Verified |
| CVSS v4.0 | 7 vectors derived · **0 base scores computed** |
| Business consequence | 🔴 Highest — clinical, personal-finance and governance data in one anonymous download |

Method: [`../../risk/risk-rating-methodology.md`](../../risk/risk-rating-methodology.md)

---

## 2. Band definitions in this engagement

| Band | Definition | Remediation window |
| --- | --- | --- |
| 🔴 Critical | Unauthenticated remote path to sensitive data, or full defeat of the authentication control | Immediate |
| 🔴 High | Practical path to confidential documents or recoverable credentials | Days |
| 🟠 Medium | Information disclosure that materially assists other attacks, or a real weakness with no independent compromise path | Weeks |
| 🟢 Low | Hardening item with no demonstrated compromise path | Ongoing |

> **Bands are judgements in the engagement's own vocabulary; the CVSS vector is a
> standardised encoding.** They answer different questions and are recorded
> separately. Where a reviewer could reasonably prefer a different band, the record
> says so — see [`technical-findings.md`](./technical-findings.md) §6.

---

## 3. Per-finding risk

| Finding | Band | Vector | Rating | Priority | Data class |
| --- | --- | --- | --- | --- | --- |
| `M1-F01` | 🟠 Medium | `PR:N/UI:N/VC:L` | Confirmed | P2 | internal |
| `M1-F02` | 🔴 Critical | `PR:N/UI:N/VC:H/VI:H/VA:L/SC:H` | Confirmed | **P0** | clinical |
| `M1-F03` | 🔴 High | `PR:L/UI:N/VC:H/VI:L` | **Provisional** | **P0** | clinical |
| `M2-F01` | 🔴 High | `PR:L/UI:N/VC:H` | **Provisional** | **P0** | clinical |
| `M3-F01` | 🟠 Medium | `PR:N/UI:N/VC:L` | Confirmed | P2 | internal |
| `M3-F02` | 🔴 Critical | `PR:N/UI:N/VC:H` | **Provisional** | **P0** | internal |
| `M3-F03` | 🔴 Critical | `PR:N/UI:N/VC:H` | Confirmed | **P0** | clinical |

Full vectors: [`../../risk/cvss-assessment.md`](../../risk/cvss-assessment.md) §2

---

## 4. Why severity alone does not set priority

Three findings show the difference between severity and priority.

| Finding | Band | Priority | Reason priority differs |
| --- | --- | --- | --- |
| `M3-F01` | 🟠 Medium | **P2, but high-value** | It is the bridge to two Critical findings. Fixing metadata stripping removes a whole chain link for a trivial cost |
| `M1-F01` | 🟠 Medium | P2 | Enabled the targeted attack, but the bypass would have been found eventually without it |
| `M3-F02` | 🔴 Critical | **P0** | Rated Critical *because* it led to the backup — but disabling listing alone does not remove the backup |

> The last row is the important one. Two P0 actions are required because **either one
> alone leaves the exposure reachable**.

---

## 5. Risk concentration

### 5.1 By root cause

| Root cause | Findings | Risk eliminated by one fix |
| --- | --- | --- |
| Unparameterised input in a SQL query | `M1-F02` | Most of the M1 and M2 chain |
| Documents in the web root, served statically | `M1-F03`, `M2-F01` | Both, entirely |
| Backups permitted in the web root | `M3-F02`, `M3-F03` | The entire M3 Critical pair |
| Migration leftovers with no owner | `M3-F02`, `M3-F03` | The systemic cause of both |
| Distinct login error messages | `M1-F01` | Its own finding |
| Verbose database errors | `M1-F02` | A contributing weakness |
| No metadata stripping | `M3-F01` | Its own finding |

### 5.2 By detectability

| Detectability | Findings | Implication |
| --- | --- | --- |
| ⚪ **Undetectable** | `M2-F01`, `M3-F01`, `M3-F03` | Offline attacks and file-borne data leave no trace on any system |
| 🟡 Low | `M1-F01`, `M1-F02`, `M1-F03`, `M3-F02` | Only detectable with web-request monitoring that was not observed |

> Four of seven are effectively undetectable without new monitoring. That is why
> alerting on bulk document access, enumeration and unusual file retrieval is a P1
> action rather than a P3 nice-to-have.

---

## 6. Provisional ratings

| Finding | Unknown input | Direction if resolved | Retest that resolves it |
| --- | --- | --- | --- |
| `M1-F03` | Whether a document is reachable with **no session** | **Upward to Critical** (`PR:N`) | One request to a known document URL with no cookies |
| `M2-F01` | Rule-based mutation result; key-reuse scope | Band likely stable, scope wider | Re-run recovery with a mutation pass; audit key reuse |
| `M3-F02` | Full contents of the legacy directory | Either direction | Enumerate the directory under authorisation |

> A provisional rating is an incomplete measurement. Two of the three could become
> worse, and the cheapest test in this table would raise a severity band.

---

## 7. Risk after remediation, as recommended

| State | Findings remaining | Residual risk |
| --- | --- | --- |
| As assessed | 7 | Three Critical chains intact |
| P0 complete | `M1-F01`, `M3-F01` | Low; enumeration and metadata hygiene remain |
| P0 + P1 complete | `M1-F01`, `M3-F01` | Low; detection now exists |
| All actions complete and retested | None outstanding | Untested classes remain untested — see §8 |

> **This projection is a hypothesis, not a measurement.** It becomes true only when
> the retest criteria in [`remediation-plan.md`](./remediation-plan.md) §5 are
> executed and pass. No remediation has been verified in this engagement.

---

## 8. Residual risk from untested areas

| Untested area | Residual risk |
| --- | --- |
| Unauthenticated access to known document URLs | If accessible, `M1-F03` is Critical and standalone |
| Object-level authorisation between accounts | Horizontal privilege escalation may exist |
| Predictability of document identifiers | IDOR may compound `M1-F03` |
| Session management and rotation | Session fixation or prediction may be possible |
| Rate limiting, lockout, CAPTCHA | Credential attacks may be unmitigated — untested by design |
| Sibling injectable parameters | Other injection points may exist |
| Full legacy directory enumeration | Additional exposures may remain under `M3-F02` |
| Other legacy paths and web roots | Other misplaced artefacts may exist |
| Purpose of one table in the backup | Unknown sensitivity; cannot be assumed benign |

> **The most important line in this report.** These are untested, not clean. The
> highest-value follow-up is a single unauthenticated request to a known document URL.

---

## 9. Risk acceptance and ownership

| Field | Status |
| --- | --- |
| Risk owner | `UNASSIGNED` |
| Risk acceptance decision | Not requested; not recorded |
| Target remediation dates | `UNASSIGNED` |
| Residual risk after fixes | Untested — no retest performed |
| Formal acceptance | **None.** No client decision exists in this engagement |

> No risk is accepted by this report. Rating a risk is not accepting it, and nothing
> here should be read as a decision by the client.

---

## 10. Related documents

| Document | Purpose |
| --- | --- |
| [`../../risk/risk-rating-methodology.md`](../../risk/risk-rating-methodology.md) | Bands, modifiers, confidence rules |
| [`../../risk/cvss-assessment.md`](../../risk/cvss-assessment.md) | Vector derivation and scoring policy |
| [`../../risk/risk-register.csv`](../../risk/risk-register.csv) | Machine-readable register |
| [`technical-findings.md`](./technical-findings.md) | Full records and judgement calls |
| [`remediation-plan.md`](./remediation-plan.md) | Actions, priorities, retest criteria |
| [`conclusion.md`](./conclusion.md) | Overall assessment and sign-off status |