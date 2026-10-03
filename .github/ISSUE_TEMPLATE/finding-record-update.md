---
name: Finding record update
about: Propose a change to a finding, rating, evidence row or remediation action
title: '[FINDING] '
labels: finding
assignees: ''
---

<!--
This template is for updating the record of an already-documented finding. It is not
a channel for reporting a new vulnerability in the target, and it must never be used
to request testing activity. Scope is fixed by the engagement record.

SECURITY: do not paste credentials, recovered document keys, patient content, salary
figures, shareholder records, database row contents or raw artifacts. Describe them by
type, class and count. If client data has been exposed, follow SECURITY.md.
-->

## Finding

| Field | Value |
| --- | --- |
| Finding ID | `NW-B083-M1-F01` |
| Current severity | |
| Current rating status | Confirmed / Provisional |
| Current verification status | Documented / Evidence-attached / Verified |
| Change requested | New evidence / Rating correction / Status correction / Retest result / Editorial |

## The change

<!-- Exactly what differs, before and after. For a rating change, name the single
     CVSS metric that moves and the observation that moves it. A rating may not change
     because a document was re-read more persuasively. -->

## Evidence for the change

| Field | Value |
| --- | --- |
| Evidence ID | `NW-B083-M1-E03` |
| Observation | |
| Artifact present | NO — or, if a sanitized artifact is genuinely available, its path and review status |
| Reviewer | `UNASSIGNED` |

> **Verification status may only move forward with an attached, sanitized,
> second-person-reviewed artifact** — see `evidence/README.md` §5. Reasoning alone
> does not upgrade `Documented`.

## For a severity or CVSS change

| Question | Answer |
| --- | --- |
| Which metric changes? | |
| What observation justifies it? | |
| Was the impact executed, or only enabled? | |
| Does the provisional reason in the record resolve? | |
| Is the base score computed with the official FIRST v4.0 calculator? | |

> Impact **enabled** is not impact **executed**. A finding that reveals a schema is not
> `VI:L` unless a modification was actually performed.

## For a remediation or retest result

| Field | Value |
| --- | --- |
| Action ID | `R-07` |
| Owner | `UNASSIGNED` |
| Date completed | |
| Retest criteria that passed | |
| Criteria not tested | |
| Residual findings | |

> Record precisely what was attempted. "No key recovered with wordlist X plus a
> mutation pass" is a measurement; "the passwords are now strong" is a claim.

## Confidentiality check

- [ ] No credential or key material
- [ ] No patient content
- [ ] No salary figure or shareholder record
- [ ] No database row contents
- [ ] Individual masked and referred to by role
- [ ] Synthetic content labelled

## Cross-references affected

<!-- e.g. risk/risk-register.csv, risk/cvss-assessment.md, findings/README.md,
     reports/remediation-tracker.csv, milestones/M4-final-report/*.md -->