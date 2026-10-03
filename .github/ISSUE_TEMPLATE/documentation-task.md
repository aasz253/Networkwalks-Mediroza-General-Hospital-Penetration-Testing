---
name: Documentation task
about: Correctness, consistency, link or redaction problem in the documentation set
title: '[DOCS] '
labels: documentation
assignees: ''
---

<!--
Documentation-only issue template for engagement NW-B083.

This repository holds no client data. Do not paste credentials, patient content,
salary figures, shareholder records or raw artifacts into an issue, a comment or an
attachment. If you believe client data has been exposed, report it privately using the
process in SECURITY.md instead of opening a public issue.
-->

## What is wrong

<!-- One sentence. "The link in X points at Y" beats "the docs are broken". -->

## Where

| Field | Value |
| --- | --- |
| File | <!-- e.g. risk/cvss-assessment.md --> |
| Line or section | |
| What you expected | |
| What you found | |

## Type of problem

- [ ] Broken or wrong internal link
- [ ] Cross-document inconsistency (a vector, count or status that disagrees)
- [ ] Unresolved placeholder or `TODO`
- [ ] Statement that overstates what was verified
- [ ] Missing limitation, or a limitation buried too deep
- [ ] Redaction gap — content that should be withheld by policy
- [ ] Typo, formatting or accessibility
- [ ] Other

## Verification

| Question | Answer |
| --- | --- |
| Does `python3 scripts/repo_checks.py` reproduce this? | |
| Does `python3 scripts/repo_checks.py --verbose` name it? | |
| If not a script finding, how was it confirmed? | |

## Proposed change

<!-- A diff, or the exact replacement text. State whether it changes any finding's
     status, severity, vector or verification status — those fields are deliberate and
     should not change as a side effect of a documentation fix. -->

## Confidentiality check

- [ ] Contains no credential
- [ ] Contains no patient content
- [ ] Contains no salary figure or shareholder record
- [ ] Contains no individual name or unmasked identifier
- [ ] Contains no evidence artifact or raw client output

## Affected documents

<!-- Every file whose content or cross-reference must change with this fix. -->