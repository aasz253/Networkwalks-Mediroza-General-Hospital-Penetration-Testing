# Evidence management

Standard, redaction policy and sanitization workflow for engagement `NW-B083`.

> **Current state, stated once and plainly.** Twenty-two observations are
> registered. **Zero** artifacts are attached, because none has been supplied to
> this repository or passed the sanitization review described in §5. Every finding
> is therefore `Documented`, not `Evidence-attached`. Nothing in this repository
> simulates, reconstructs or re-renders an artifact in place of a real one.

---

## 1. Why this document exists

A penetration test report makes two different claims:

| Claim | Requires |
| --- | --- |
| "We observed this" | A narrative and reasoning |
| "Here is the artifact" | The artifact, sanitised, with provenance |

Only the first is currently supported for every finding. This repository keeps the
two visibly separate so that no reader can mistake the second for the first.

---

## 2. Evidence ID scheme

```
NW-B083-<MILESTONE>-E<nn>
        │        │      └── sequential within the milestone
        │        └───────── M1 · M2 · M3 · M4
        └────────────────── engagement ID
```

| Rule | Reason |
| --- | --- |
| IDs are never reused | A withdrawn observation must not be reissued, or old evidence appears to support a newer claim |
| IDs are stable once published | Findings, reports and registers must keep cross-referencing |
| An ID is assigned when the observation is *recorded*, not when an artifact exists | Otherwise the ID scheme leaks whether evidence exists |
| IDs never encode severity, data class or PII | Metadata belongs in register columns, not in filenames |

### Milestone ranges

| Milestone | Range | Count |
| --- | --- | --- |
| M1 Initial Access | `NW-B083-M1-E01` … `E08` | 8 |
| M2 Data Extraction | `NW-B083-M2-E01` … `E06` | 6 |
| M3 Critical Data Exposure | `NW-B083-M3-E01` … `E08` | 8 |
| M4 Reporting | not applicable | 0 |
| **Total** | | **22** |

---

## 3. Register

[`evidence-register.csv`](./evidence-register.csv) — one row per observation.

| Column | Purpose |
| --- | --- |
| `evidence_id` | The identifier above |
| `milestone` | `M1` · `M2` · `M3` |
| `step` | Engagement step the observation belongs to |
| `observation` | What was seen, in neutral language |
| `supports_finding` | Finding ID, or `n/a` |
| `expected_path` | Where the sanitised artifact will live |
| `artifact_present` | `YES` / `NO` — **`NO` on every row today** |
| `data_class` | `none` · `internal` · `personal` · `clinical` · `financial` · `credential` |
| `contains_pii` | `YES` / `NO` |
| `redaction_required` | What must be removed before the artifact may be published |
| `sanitization_status` | `not_started` / `sanitized` / `reviewed` / `published` |
| `reviewer` | Second person who checked the redaction — `UNASSIGNED` |

> `artifact_present=NO` on all 22 rows is the single most important honest fact in
> this repository. Changing any of those values requires the workflow in §5, not a
> quick edit.

---

## 4. Redaction policy

Two different questions, and the difference matters:

| Question | Answer for this engagement |
| --- | --- |
| Must the artifact be redacted before **internal** use in a client report? | Yes |
| Must it be redacted before **publication in this repository**? | Yes, more aggressively |

### 4.1 Never published in any form

| Category | Examples | Handling |
| --- | --- | --- |
| Credentials | The three recovered PDF passwords, session cookies, tokens | **Withheld entirely.** Characterised by strength class only |
| Patient content | Names, addresses, diagnoses, report narratives, any clinical text | **Never published.** Represent by table name and record count |
| Compensation data | Individual salary figures | **Never published.** Table name and column names only |
| Corporate governance data | Shareholder names, share counts, percentages, classes | **Never published.** Table name and column names only |
| Personal identifiers of staff | Account names, personal email addresses | **Masked** — `j.m***` |
| Bulk data | `INSERT` row contents, table dumps | **Never published.** Schema only |
| Hashes and keys | `$pdf$` identifiers, derived keys | **Withheld.** Recovery is described qualitatively |
| Session material | Cookies, `Authorization` headers, CSRF tokens | **Stripped** from any captured artifact |

### 4.2 Masking standard

| Rule | Example |
| --- | --- |
| Partial masking preserves the lesson, removes the person | `j.malik` → `j.m***` |
| Never mask so heavily the point is lost | ❌ `j.****` with no context |
| Credentials are never partially masked — they are withheld | `--password='<REDACTED>'`, never `--password='adm…'` |
| Synthetic values are labelled at the point of use | `SYNTHETIC — NOT CLIENT DATA` |

> **Why credentials are withheld entirely rather than masked.** A partially masked
> credential is still a credential disclosure waiting to be completed, and a
> reader has no way to tell how much was removed. Withholding is unambiguous.

### 4.3 Sanitizer scope

[`../scripts/evidence_sanitizer.py`](../scripts/evidence_sanitizer.py) removes
*mechanical* identifiers — cookies, bearer tokens, e-mail addresses, IP addresses,
AWS-style keys. It does **not** judge whether a sentence contains a salary or a
diagnosis.

> **The sanitizer is a first pass, not an approval.** Every output requires manual
> review before publication. A tool that cannot read meaning must never be the last
> control between client data and a public repository.

---

## 5. Closing the evidence gap

The procedure that converts a row from `NO` to `YES`.

| # | Step | Done by | Gate |
| --- | --- | --- | --- |
| 1 | Capture the artifact at source, in the lab | Assessor | Artifact exists outside this repository |
| 2 | Add or confirm the register row **before** processing | Assessor | Row present with correct data class |
| 3 | Run [`evidence_sanitizer.py`](../scripts/evidence_sanitizer.py) on a **copy** | Assessor | Output produced; input untouched |
| 4 | Manual redaction review against §4 | Assessor | Every item in the policy addressed |
| 5 | Second-person review of the redacted copy | Reviewer ≠ author | `reviewer` column filled; `sanitization_status=reviewed` |
| 6 | Place in [`screenshots/<MS>/`](./screenshots/) using the naming convention | Assessor | Path matches `expected_path` |
| 7 | Set `artifact_present=YES` | Assessor | Row updated |
| 8 | Promote the finding's verification status | Assessor | Only now may `Documented` → `Evidence-attached` |
| 9 | Independent check against the finding claim | Reviewer | Only now may `Verified` |

### 5.1 Naming convention

```
NW-B083-<MS>-E<nn>_<slug>.<ext>

Examples:
  NW-B083-M1-E01_robots-txt-disclosure.txt
  NW-B083-M1-E02_login-page.png
  NW-B083-M2-E02_report-01-key-recovered.png
  NW-B083-M3-E02_pdf-comments-metadata.png
  NW-B083-M3-E03_old-directory-listing.png
```

Rules: lowercase, hyphen-separated slug; extension describes the format, never the
sensitivity; **nothing in a filename may reveal severity, data class or a person's
name.**

### 5.2 Artifact directories

| Directory | Intended contents | Status |
| --- | --- | --- |
| [`screenshots/M1/`](./screenshots/M1/) | `E01`–`E08` | Empty — placeholder manifest only |
| [`screenshots/M2/`](./screenshots/M2/) | `E01`–`E06` | Empty — placeholder manifest only |
| [`screenshots/M3/`](./screenshots/M3/) | `E01`–`E08` | Empty — placeholder manifest only |
| [`screenshots/M4/`](./screenshots/M4/) | Reporting artefacts | Empty by design |

Each directory carries a `README.md` listing the intended artifact paths. These are
**manifests of intent, not stand-ins for evidence.**

---

## 6. Chain of custody

| Stage | Record | Note |
| --- | --- | --- |
| Collection | Register row created at source | ID assigned before processing |
| Handling | Local working copy only | Never uploaded to a third-party service |
| Processing | Sanitizer output to a new file | Input is never overwritten |
| Review | Two-person sign-off | Author may not self-review |
| Publication | This repository, or a client-delivered report | Public repository is the most permissive channel |

> **Third-party tooling is a custody decision.** Sending a screenshot through an
> online redaction or conversion service transfers the unredacted artifact to that
> provider. For artifacts containing any `data_class` above `internal`, processing
> stays local. This is the same principle that governs the AI-tooling caveat in
> [`../milestones/M3-critical-data-exposure/evidence.md`](../milestones/M3-critical-data-exposure/evidence.md) §5.

---

## 7. Limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | No artifact supplied | No finding can be `Evidence-attached` or `Verified` |
| 2 | No collection timestamps or tool versions recorded in the source record | Artifacts cannot be independently dated; stated as `UNKNOWN` rather than guessed |
| 3 | Original lab artifacts are not in this repository | Chain of custody for the originals rests with the engagement record, not here |
| 4 | Sanitizer coverage is pattern-based | Mechanical identifiers only; semantic review remains mandatory |
| 5 | Screenshots of a training target may still resemble real data | Masking policy applied regardless of the data's fictional status |

---

## 8. Related documents

| Document | Purpose |
| --- | --- |
| [`evidence-register.csv`](./evidence-register.csv) | The register |
| [`../findings/README.md`](../findings/README.md) | Verification-status definitions |
| [`../docs/ethical-considerations.md`](../docs/ethical-considerations.md) | Data-handling obligations |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Contribution rules, including evidence submission |
| [`../scripts/evidence_sanitizer.py`](../scripts/evidence_sanitizer.py) | Mechanical redaction helper |
| [`../scripts/repo_checks.py`](../scripts/repo_checks.py) | Register/evidence-reference consistency checks |