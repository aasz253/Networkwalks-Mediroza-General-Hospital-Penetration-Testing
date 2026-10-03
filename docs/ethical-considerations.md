# Ethical Considerations

**Engagement ID:** `NW-B083` · **Environment:** Networkwalks authorised training target

---

## 1. The core obligation

A penetration test borrows someone else's system without permission to break it,
and often handles data they would rather nobody saw. Both halves of that
obligation — do no harm, and protect what you see — are the whole of professional
practice here.

This engagement's data was synthetic, which made the *harm* easy. It did not make
the *discipline* optional, because the discipline is what has to be automatic
before the day the data is real.

---

## 2. Authorisation and boundaries

| Principle | How it was honoured |
| --- | --- |
| Only test what is authorised | Single authorized host; three paths from `robots.txt`; `/staff/` left untouched |
| Produce authorisation on demand | Provider statement recorded in [`authorization-and-scope.md`](authorization-and-scope.md) |
| Do no harm to availability | Manual, sequential interaction; no load activity |
| Do no harm to data | No write, modify or delete operation of any kind |
| Validate minimally | One quote to prove injection; one bypass to prove impact; no extraction beyond substantiation |
| Report, do not remediate unilaterally | Findings and recommendations delivered; no change made to the target |
| Do not claim approval | No client review or sign-off is claimed anywhere |

---

## 3. Handling of sensitive material

The engagement surfaced three categories of data that would be highly sensitive in
a real hospital. Treatment applied:

| Category | Handling |
| --- | --- |
| **Recovered document passwords** | **Withheld from publication.** Characterised by length, character-class composition and dictionary membership. The values remain available to the client under the engagement's own disclosure process. See [M2 results](../milestones/M2-data-extraction/results.md). |
| **Employee salary data** | **Values withheld.** Only table schema and data classes published. See [M3 classification](../milestones/M3-critical-data-exposure/data-classification.md). |
| **Shareholder information** | **Names, percentages and classes withheld.** Schema only. |
| **Patient report content** | **Never opened or reproduced.** Only encryption properties and metadata fields were assessed. |
| **Identified staff account** | Partially masked in published tables (`j.m***`). Full value retained only in the confidential record. |
| **The artifacts themselves** | Gitignored. Not committed. |

### 3.1 Why passwords were withheld even though they are "just lab passwords"

Two reasons, and the second is the important one.

1. **They are credentials.** A published password is a published credential, in
   any environment. A reader who later encounters a similarly-named resource has
   been handed a working string by a security repository.
2. **The habit is the deliverable.** The finding is *"document keys are
   dictionary-recoverable"*, and that finding is fully substantiated by strength
   analysis. Printing the values adds nothing to the finding and establishes a
   norm that would be indefensible on a real engagement.

---

## 4. Data minimisation

Minimisation is not "we deleted some data later". It is a decision made **at the
moment of collection** about how much to take.

| Decision point | Lesser collection rejected | Chosen bound |
| --- | --- | --- |
| M1 Step 5 — after the bypass | Enumerating the whole portal, testing admin functions | Download the three documents; stop |
| M1 Step 6 — document retrieval | Reading document contents | Retrieve for encryption analysis only |
| M2 — key recovery | Read every document to "see what's inside" | Recover keys, assess strength, do not read content |
| M2 Step 4 — decryption | Keeping decrypted copies of all three | Decrypt report 3 only, because metadata was the objective |
| M3 Step 4 — backup review | Full database dump, complete row extraction | Extract only the `staff` and `shareholders` `INSERT` statements |
| M3 Step 5 — correlation | Building a profile of the individual | Match one record to establish role; stop |
| Publication | Publishing any real value | Schemas and data classes only |

---

## 5. The AI tooling caveat

Step 4 of M3 involved pasting `INSERT` statement rows into a third-party AI
assistant to convert them into a readable table.

**This is a disclosure event.** Even against a lab target, the professional lesson
matters more than the convenience:

| Consideration | Assessment |
| --- | --- |
| What was sent | Synthetic staff and shareholder rows |
| What a production equivalent would send | Real names, job titles, salaries, shareholdings |
| Provider retention | Depends on the service and account tier — frequently a retention risk that the tester does not control |
| Training reuse | Consumer tiers may use submitted content for model improvement |
| Jurisdiction | Data residency and cross-border transfer may apply to health-adjacent and payroll data |
| Consent | Data subjects generally have no expectation that their salary is pasted into a chatbot |
| Reversibility | A prompt is not a deletion. Once submitted, recall cannot be guaranteed |

**Rule adopted for this repository:** where an LLM is used to process
substantially-identifiable data, the decision must be recorded, the data must be
minimised first, and a non-LLM method must be considered. A regex or a 20-line
script over a local file is usually sufficient, faster, and leaks nothing.

Practically, in this engagement a local `sed`/`awk` extraction would have produced
the same proof with no disclosure at all. That is the correct future approach.

---

## 6. Evidence handling principles

| Principle | Implementation |
| --- | --- |
| Raw evidence stays off-repository | Access-controlled store; this repository holds only sanitised derivatives |
| Every artefact is identified | `NW-B083-<MS>-E<nn>` |
| Every artefact is classified | Sensitivity, redaction status, verification status in the [register](../evidence/evidence-register.csv) |
| Automated redaction is a first pass | [Sanitizer](../scripts/evidence_sanitizer.py) flags classes; a human decides |
| Matched secrets are never printed | Sanitizer and QA tool report class and location only |
| Publication requires review | Checklist in [`../evidence/README.md`](../evidence/README.md) §6 |

---

## 7. If sensitive data is found committed

Follow this order. Do not improvise.

1. **Stop.** Make no further commits or pushes.
2. **Preserve.** Record paths, commit SHAs, branches. **Do not rewrite history** — that destroys the audit trail.
3. **Notify the repository owner privately**, labelled `INCIDENT — SENSITIVE DATA IN REPOSITORY`.
4. **Notify Networkwalks**, because client-notification obligations may be
   time-bound under the engagement's confidentiality terms.
5. **Assess exposure.** Determine whether the repository was public, for how long,
   and who could have fetched it.
6. **Await written instruction** before force-pushing, rotating anything, or
   notifying affected parties. The owner and provider decide; unilateral action
   creates a mismatch with what was reported.
7. **Then remediate:** rotate any exposed secret, purge with an explicit rewrite
   if instructed, purge forks and caches where possible, and notify anyone who
   cloned during the exposure window.
8. **Record the outcome** in [`../CHANGELOG.md`](../CHANGELOG.md) and
   [`../SECURITY.md`](../SECURITY.md).

### History inspection

```bash
# Large files that should not be in a documentation repository
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3 > 1048576 {print $3, $4}' | sort -rn | head

# Search all history for a sensitive-token pattern (never paste a real secret here)
git log --all -S'<pattern>' --oneline

# Confirm no forbidden extensions were ever committed
git log --all --diff-filter=A --name-only --format='' \
  | sort -u | grep -Ei '\.(sql|pdf|pem|key|env)$'
```

> If a *real* secret is ever committed, **rotating it is mandatory and
> non-negotiable.** Rewriting history is damage limitation; rotation is the fix.
> Assume anything committed has been read by somebody.

---

## 8. Respect for the client

| Consideration | Practice |
| --- | --- |
| Report accuracy over impressiveness | Severity derived from impact, not excitement |
| State limitations | Seven documented limitations in [`../reports/penetration-testing-report.md`](../reports/penetration-testing-report.md) |
| No sensationalism | A SQL injection is described as an authentication-bypass path, not as "total system compromise" |
| Actionable recommendations | Every finding has a fix and a retest criterion |
| Report the systemic cause | F06/F07 are framed as a lifecycle-ownership problem, not just two misconfigurations |
| Do not publish client detail | No infrastructure internals, no real values, no artifacts |
| Do not claim endorsement | Explicitly disclaimed in [`../LICENSE`](../LICENSE) |

---

## 9. Educational-use boundary

The provider's own statement applies to this repository's contents:

> *"This document is produced by Networkwalks for educational purposes only. The
> target has been authorised for security testing. These techniques must never be
> applied to any system without explicit written permission from the owner."*

Every technique recorded here — disclosure-file analysis, username enumeration,
injection confirmation, authentication bypass, document key recovery, metadata
forensics, directory-listing abuse, backup exposure — is a real technique used by
real attackers against real systems, many of which are healthcare organisations.

The authorisation for this engagement is **specific to this engagement**. It does
not travel with this repository, and reading it is not permission to test anything.
