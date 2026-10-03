# Management summary

**Networkwalks — Mediroza General Hospital Penetration Testing** · `NW-B083`
One page · Non-technical · For decision-makers

---

## The situation

An anonymous visitor could download the hospital's entire database — patient
records, staff salaries and shareholder information — using nothing more than a web
browser and information the website itself provided.

No specialist tools were used. No passwords were stolen. No malware was deployed.

---

## What we found

| Severity | Count | In plain terms |
| --- | --- | --- |
| 🔴 **Critical** | 3 | A login page that can be bypassed; a public folder listing; a database file downloadable by anyone |
| 🔴 **High** | 2 | Patient reports reachable without a proper login; document passwords too weak to protect them |
| 🟠 **Medium** | 2 | The login page reveals which usernames exist; a patient report leaked internal system details |
| 🟢 Low | 0 | — |

---

## Why it happened

Not one problem. **Eight separate causes**, and six of them are configuration
settings rather than complicated code.

| Cause | Change needed |
| --- | --- |
| The login page builds a database query by pasting text into it | Use prepared statements — a standard, well-understood fix |
| The login page shows different errors for "no such user" and "wrong password" | Show one generic error for every failure |
| Patient reports are stored as ordinary files inside the website folder | Store them privately and serve them only after checking permission |
| A website folder automatically lists its contents | Turn the listing off |
| A copy of the database was left inside that folder | Move backups off the website, encrypt them, delete old ones on schedule |
| Nobody was responsible for cleaning up after the old site was replaced | Make "decommission the old site" a signed-off step |
| Document passwords could be guessed from a common-password list | Generate random, unique passwords automatically |
| Documents kept internal notes and file paths in their properties | Strip document properties automatically on export |

---

## What it cost to fix

| Finding | Effort | Risk removed |
| --- | --- | --- |
| Remove the exposed database file | **Minutes** | The most serious exposure in this assessment |
| Turn off folder listings | Minutes | Reduces discoverability |
| Stop returning database errors to visitors | Minutes | Removes the injection signal |
| Store backups properly | Hours | Prevents recurrence |
| Fix the login query | Days | Fixes the root cause of most of the assessment |
| Serve documents through a permission check | Days | Removes reliance on document passwords |
| Everything else | Weeks to ongoing | Defence in depth |

> **The single highest-value action is also the cheapest: move one file.**

---

## What it could cost to leave

| Risk | Consequence |
| --- | --- |
| Patient information disclosed | Regulatory reporting; possible harm to patients; loss of public trust |
| Salary and shareholder data disclosed | Governance concerns; market sensitivity; employment-relations issues |
| Compliance exposure | Health-data regimes in most jurisdictions require notification of a breach of this scale |
| Reputational damage | In healthcare, trust is the foundation of the relationship |
| Repeat occurrence | Nothing in place would prevent a similar file being exposed again |

> **Obligations do not end when the file is removed.** If personal data was exposed,
> notification duties may still apply.

---

## What we recommend

**Immediately**

1. Remove the exposed database file, and search the whole website for any others.
2. Assess whether notification is legally required.
3. Check server logs to see whether anyone else already accessed the file.
4. Turn off automatic folder listings.

**Within days**

5. Fix the login page's database handling and stop showing database errors.
6. Store patient reports privately and serve them only after a permission check.
7. Set up alerts for unusual download volumes, repeated login failures and access to
   old, retired addresses.

**Within weeks**

8. Use one generic message for all failed logins.
9. Remove document properties automatically when files are issued.
10. Move all backups off the website, encrypted, with automatic deletion.

**Ongoing**

11. Periodically check for exposed files, review what data is stored together, and
    repeat this assessment after fixes are made.

---

## What we could not confirm

| Item | Why it matters |
| --- | --- |
| No supporting screenshots or logs were attached to this review | Findings are documented but not independently verified |
| Some parts of the system were not tested | **Not tested does not mean safe** |
| Whether anyone else already accessed the file is unknown | Log review recommended above |
| How current the exposed data was is unknown | Affects the scope of any notification |
| No fixes have been retested | Every recommendation here is a proposal, not a completed change |

---

## Status

| Field | Value |
| --- | --- |
| Report state | **Draft for review** |
| Client review | **None yet** |
| Approval | **Not granted, not requested** |
| Next step | Assign owners and dates, attach supporting evidence, retest after fixes |

---

## Detailed documents

| Document | For |
| --- | --- |
| [`../milestones/M4-final-report/executive-summary.md`](../milestones/M4-final-report/executive-summary.md) | Executives |
| [`../milestones/M4-final-report/remediation-plan.md`](../milestones/M4-final-report/remediation-plan.md) | Owners of each fix |
| [`../milestones/M4-final-report/risk-assessment.md`](../milestones/M4-final-report/risk-assessment.md) | Risk and technical reviewers |
| [`../milestones/M4-final-report/technical-findings.md`](../milestones/M4-final-report/technical-findings.md) | Developers |
| [`../milestones/M4-final-report/appendices.md`](../milestones/M4-final-report/appendices.md) | Auditors |
| [`remediation-tracker.csv`](./remediation-tracker.csv) | Tracking |

---

> This assessment covers one authorised training environment. No client data appears
> in this report: passwords, patient information, salary figures and shareholder
> records are withheld by policy, and are described only by type and quantity.