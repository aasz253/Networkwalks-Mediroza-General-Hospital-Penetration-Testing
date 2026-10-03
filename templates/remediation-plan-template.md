# Remediation plan — {{ENGAGEMENT OR COMPONENT}}

> Full-plan template. For a single action use
> [`remediation-template.md`](./remediation-template.md).

| Field | Value |
| --- | --- |
| Engagement / component | |
| Plan date | |
| Plan author | |
| Approved by | `UNASSIGNED` |

---

## 1. Priority model

State the model explicitly, because priority is not the same as severity.

| Priority | Meaning | Window |
| --- | --- | --- |
| P0 | Immediate — exploitable now, or a root cause of other findings | Same day |
| P1 | Detection and recurrence prevention | Days |
| P2 | Defence in depth and hygiene | Weeks |
| P3 | Programme maturity | Ongoing |

---

## 2. Actions

| # | Action | Addresses | Priority | Effort | Owner | Due | Retested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | | | P0 | | `UNASSIGNED` | `UNASSIGNED` | ❌ |

### 2.1 Sequencing rules

| Rule | Reason |
| --- | --- |
| Close exposed data before closing the paths that reach it | Removes the impact before spending time on access |
| Close paths before closing the weaknesses that made them reachable cheaply | Cheapest fixes first, where they buy the most |
| Process controls alongside every technical fix | Otherwise the fix is undone at the next deadline |
| Every P0 action must have a pass condition that proves absence, not just unavailability | A retest of one URL cannot prove a file is gone |

---

## 3. Retest criteria

Consolidated and deduplicated. One criterion, one observable condition.

| # | Criterion | Pass condition | Covers |
| --- | --- | --- | --- |
| T-01 | | | R-01 |

### 3.1 Criteria that prove absence

| Weak form | Strong form |
| --- | --- |
| "The old URL returns 404" | "A filesystem search of all web-served paths returns zero backup files" |
| "Directory listing is off" | "No index is rendered at any path **and** no artefact remains reachable" |
| "Passwords are stronger now" | "No key was recovered using wordlist X plus a rule-based mutation pass" |

---

## 4. Progress summary

| Metric | Value |
| --- | --- |
| Total actions | 0 |
| P0 / P1 / P2 / P3 | 0 / 0 / 0 / 0 |
| Owners assigned | 0 |
| Target dates assigned | 0 |
| Actions completed | 0 |
| Actions retested and passing | 0 |

> `0 of 0 assigned` is the honest starting state of most remediation plans, and it
> is the single clearest indicator of whether a plan is real.

---

## 5. Risk projection after remediation

| State | Findings remaining | Residual risk |
| --- | --- | --- |
| As assessed | | |
| P0 complete | | |
| P0 + P1 complete | | |
| All actions complete and retested | | |

> This is a **projection, not a measurement**. It becomes true only when the retest
> criteria pass. Always label it as such.

---

## 6. Out-of-scope and deferred

| Item | Why deferred | Revisit when |
| --- | --- | --- |
| | | |

---

## 7. Sign-off

| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Technical owner | `UNASSIGNED` | | |
| Management approver | `UNASSIGNED` | | |

> No signature is recorded in this repository, and none should be inferred from the
> existence of this document.