# Security Policy

Applies to the **Networkwalks B083 — Mediroza General Hospital Penetration Testing**
documentation repository.

---

## 1. What this repository is

A documentation and automation repository for an authorized, internship-scale,
black-box web application assessment. It contains documentation, diagrams,
templates, CSV registers and Python utilities.

It is **not** an exploitation toolkit, and it **does not** contain, request or
require access to the client's systems.

---

## 2. Reporting a security issue

### 2.1 If you find sensitive client data committed to this repository

**Treat this as an incident.** Do not open a public issue. Do not share it on
social media. Do not clone or fork the repository until it is contained.

1. **Stop.** Do not add, commit or push anything further.
2. **Preserve.** Note the file paths, commit SHAs and branch names involved.
   Do not delete history yourself — that destroys the audit trail.
3. **Notify the repository owner immediately** via the private channel listed in
   the repository owner's GitHub profile, using the label:
   `INCIDENT — SENSITIVE DATA IN REPOSITORY`.
4. **Notify the engagement supervisor / Networkwalks** through the intern
   reporting channel, because client notification obligations may be time-bound
   under the authorization and any applicable confidentiality or data-protection
   agreement.
5. **Follow the incident procedure** in
   [`docs/ethical-considerations.md`](./docs/ethical-considerations.md) §7
   (Git history inspection and disclosure handling) for the credential-rotation,
   history-rewrite and verification steps.
6. **Await written instruction** before rewriting history, force-pushing,
   closing the repository or notifying the client.

Rationale for sequencing: the repository owner and the client decide on
notification and rotation. An intern acting unilaterally risks destroying
evidence, invalidating the audit trail, or creating a disclosure mismatch with
what the client was told.

### 2.2 If you find an inaccuracy in the documentation

Open a documentation issue using
[`documentation-task.md`](./.github/ISSUE_TEMPLATE/documentation-task.md).

If the inaccuracy would **overstate** the engagement's results — for example a
finding described as verified without evidence — treat it as urgent and mark the
issue `documentation-integrity` in the title. Overstated results are the most
serious documentation defect this project can have, because a portfolio
repository exists to be a truthful record.

### 2.3 If you want to report a vulnerability in a system you own

This repository's owner is not the relevant contact for vulnerabilities in
third-party systems. Report those directly to the system owner through their
own disclosure process. If the system belongs to the engagement client and the
issue arose from this project, route it through the engagement supervisor as
described above.

---

## 3. Handling rules contributors must follow

| Rule | Detail |
| --- | --- |
| **No live target traffic** | No script, workflow, test or manual step in this repository may send a request to the client target. CI and local tooling are strictly offline. |
| **No exploitation tooling** | Exploit frameworks, credential-attack tools, DoS tooling, fuzzers pointed at a live host, and payload generators are prohibited. |
| **No client-sensitive data** | Patient records, clinical data, salary figures, shareholder details, credentials, tokens, cookies, keys and raw unredacted evidence must never enter this repository, including in issue text. |
| **No secrets, ever** | `.env.example` contains dummy values only. `.env` and all key material are gitignored. |
| **Evidence sanitization is mandatory** | Raw evidence lives off-repository. Only reviewed, sanitized derivatives are committed, and each one is registered in [`evidence/evidence-register.csv`](./evidence/evidence-register.csv). |
| **Redaction is manual-verified** | The sanitizer in [`scripts/evidence_sanitizer.py`](./scripts/README.md) is a *first pass only*. Automated redaction is not guaranteed and always requires human review. |
| **No fabricated results** | No finding may be moved out of `PENDING VERIFICATION` without a traceable sanitized artifact. |
| **No client approval claims** | Never state or imply that the client reviewed, approved or accepted any part of this repository. |
| **Respect the rules of engagement** | Testing scope is defined in [`docs/rules-of-engagement.md`](./docs/rules-of-engagement.md). Documentation work must not extend it. |

---

## 4. Automated protections in this repository

| Control | Implementation |
| --- | --- |
| CI documentation gate | [`.github/workflows/documentation-check.yml`](./.github/workflows/documentation-check.yml) |
| Broken relative link detection | `scripts/repo_checks.py` |
| CSV header and structure validation | `scripts/repo_checks.py` |
| Evidence reference existence checks | `scripts/repo_checks.py` |
| Secret-pattern detection (values never logged) | `scripts/repo_checks.py` |
| Client-data file exclusion | [`.gitignore`](./.gitignore) |
| Safe local sanitization | `scripts/evidence_sanitizer.py` |

The CI checks run **without network access** and are designed to fail closed: if a
check cannot complete, the job fails rather than silently passing.

---

## 5. Supported versions and scope of testing

| Item | Policy |
| --- | --- |
| Documentation in `docs/`, `milestones/`, `reports/` | Reviewed during active project weeks; corrections accepted via pull request |
| `scripts/` utilities | Best-effort; Python 3.8+ |
| Live client target | **Out of scope for this repository entirely.** See [`SECURITY.md`](./SECURITY.md) §3 and [`docs/rules-of-engagement.md`](./docs/rules-of-engagement.md) |
| Dependency vulnerabilities in third-party tooling | This repository has **no runtime third-party dependencies** (Python standard library only), so there is no dependency supply chain to patch here |

---

## 6. Acknowledgement

Reports that identify a genuine sensitive-data exposure or a materially overstated
claim are treated as priority work and acknowledged in
[`CHANGELOG.md`](./CHANGELOG.md).
