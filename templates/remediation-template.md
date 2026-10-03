# Remediation action — {{ACTION TITLE}}

> One action. Use [`remediation-plan-template.md`](./remediation-plan-template.md)
> for a full plan, and this format for tracking an individual action to closure.

| Field | Value |
| --- | --- |
| **Action ID** | `R-{{nn}}` |
| **Addresses** | `{{finding IDs}}` |
| **Priority** | P0 / P1 / P2 / P3 |
| **Owner** | `UNASSIGNED` |
| **Target date** | `UNASSIGNED` |
| **Status** | Not started / In progress / Blocked / Done |
| **Verified by retest** | NO / YES |
| **Verified on** | `UNKNOWN` |
| **Verified by** | `UNASSIGNED` |

---

## 1. The action

One sentence, in the imperative. It must be possible to tell from the sentence alone
whether it is finished.

> ✅ *Remove the database backup from every web-served path and purge CDN and proxy
> caches.*
>
> ❌ *Improve backup security.*

| Attribute | Value |
| --- | --- |
| Effort estimate | |
| Depends on | Other action IDs, or `NONE` |
| Blocks | Action IDs or findings that cannot be verified until this completes |

---

## 2. Why it matters here

Tie the action to a specific finding and a specific consequence. If the action
cannot be traced to an observation, it is a hardening wish rather than remediation.

| Finding | What the action removes |
| --- | --- |
| `{{ID}}` | |

---

## 3. Implementation

| Element | Guidance |
| --- | --- |
| Where | Files, configuration, infrastructure or process |
| How | Concrete steps a developer or operator can follow |
| Verification of implementation | How to confirm the change is present at all |

```text
// Illustrative configuration or code — no live target, no automation
```

---

## 4. Retest criteria

| # | Criterion | Method | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | | | | ❌ |

### 4.1 Reporting a failed retest

| Rule | Reason |
| --- | --- |
| Record exactly what was attempted | Absence of a result is meaningless without it |
| Distinguish "not recovered" from "uncrackable" | The first is a measurement; the second is a claim |
| Record the date, tester and configuration | A retest result without context cannot be re-examined |
| If a criterion cannot be tested, say so | An untested criterion is not a passed one |

> **A fix is not demonstrated until its retest criteria pass.** A closed action with
> `Verified by retest: NO` is an open action with better paperwork.

---

## 5. Post-fix verification record

| Field | Value |
| --- | --- |
| Date tested | |
| Tester | |
| Build or configuration version | |
| Criteria passed | 0 of 0 |
| Criteria not tested | |
| Residual issues found | |
| Follow-up actions raised | |

---

## 6. Data-handling obligations

Some remediations create obligations that outlive the technical fix.

| Question | Answer |
| --- | --- |
| Was sensitive data exposed? | |
| Does a notification obligation arise? | |
| Were local copies of any exposed data retained by the assessor? | |
| Are credentials present in the exposed material still valid? | |
| Must caches, backups or replicas also be purged? | |

> Removing a file does not discharge a notification duty arising from its exposure.

---

## 7. Closure

| Field | Value |
| --- | --- |
| Closed on | |
| Closed by | |
| Residual risk accepted by | `UNASSIGNED` |
| Acceptance evidence | |
| Follow-up review date | |

> Risk acceptance is a decision by an accountable owner. Recording it in a technical
> document does not constitute acceptance.