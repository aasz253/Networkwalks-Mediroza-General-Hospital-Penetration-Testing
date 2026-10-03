# M3 — Evidence

**Milestone:** Deep Reconnaissance / Critical Data Exposure · **Status:** 🟡 Documented, artifacts pending

> 🔴 **Most sensitive milestone.** This milestone produced evidence of personal
> financial data and confidential corporate data exposure. Every artifact here
> requires row-level redaction and manual review before publication.

Handling standard: [`../../evidence/README.md`](../../evidence/README.md) ·
Register: [`../../evidence/evidence-register.csv`](../../evidence/evidence-register.csv)

---

## 1. Evidence register — M3

| Evidence ID | Description | Finding | Sensitivity | Artifact |
| --- | --- | --- | --- | --- |
| `NW-B083-M3-E01` | `exiftool` output — `Author` field | F05 | 🟠 Personal | ❌ |
| `NW-B083-M3-E02` | `exiftool` output — `Comments` field with the internal note | F05 | 🔴 Internal | ❌ |
| `NW-B083-M3-E03` | Directory index at `/old/` listing the backup | F06 | 🔴 Internal | ❌ |
| `NW-B083-M3-E04` | Download of the SQL backup | F06, F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E05` | `staff` table schema and data classes | F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E06` | `shareholders` table schema and data classes | F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E07` | Identity correlation against one staff record | F05, F07 | 🔴 Personal | ❌ |
| `NW-B083-M3-E08` | Cross-reference to `NW-B083-M1-E01` — the `robots.txt` `/old/` disclosure | F06 | 🟠 Internal | ❌ |

---

## 2. What each artifact must prove — and the minimum needed to prove it

The governing principle: **evidence must be sufficient to substantiate the finding
and no more.**

| Finding | What must be proven | Minimum sufficient evidence | What must NOT be captured |
| --- | --- | --- | --- |
| **F05** metadata leak | The document carries an internal author identifier and an internal operational note | The two metadata fields, with the account identifier **masked** | Any other metadata field that could carry content or a host path |
| **F06** directory listing | The folder is anonymously browsable and exposes a backup | The directory index showing the filename | Contents of any other file listed |
| **F07** cleartext exposure | Staff compensation and shareholder data are readable without a key | Table names, **column names**, and one **fully masked** example row | Any real name, salary, percentage or share class |

### 2.1 Masked row illustration

If an artifact must show a row to prove the format, every value is replaced:

```sql
-- SYNTHETIC — NOT CLIENT DATA
-- Row shape only. Values replaced.

INSERT INTO `staff`
  (`full_name`, `job_title`, `department`, `monthly_salary`)
VALUES
  ('<REDACTED>', '<REDACTED>', '<REDACTED>', <REDACTED>);
```

---

## 3. Redaction standard

### 3.1 Mandatory — never publish

| Item | Reason |
| --- | --- |
| Any staff name | Direct personal identifier |
| Any salary figure | Special-category personal financial data |
| Any shareholder name | Confidential ownership information |
| Any share percentage or class | Confidential ownership information |
| Any email address or local-part | Personal identifier and a phishing enabler |
| Any real `INSERT` row | Aggregates the above |
| Connection strings, credentials or API keys in the backup | **Not extracted, not reported** — but must be checked for in any artifact |
| Patient document content | Out of scope; potentially clinical |
| Full file listing of `/old/` beyond the backup | Scope discipline — other files were not assessed |

### 3.2 Safe to publish

| Item | Sufficient for |
| --- | --- |
| `robots.txt` output | F06 corroboration |
| The directory index showing one filename | F06 |
| `exiftool` field names with the author **masked** | F05 |
| The `Comments` field quoted in full | F05 — this **is** the finding |
| Table names and column names | F07 |
| Data-class descriptions | F07 |
| Fully masked example rows | F07 format demonstration |
| Synthetic reproductions | Format illustration |

### 3.3 Irreversible over cosmetic

| Preferred ✅ | Avoid ❌ |
| --- |---|
| Delete the value entirely | Blur it — redaction tools fail and layers are recoverable |
| Replace with `<REDACTED>` | Black rectangle over text in a screenshot — often recoverable from the original |
| Re-export from a masked copy | Crop a screenshot — the original retains the data |

> **Screenshot redaction is the highest-risk step in this repository.** Cropping,
> blurring and drawing boxes all leave the original intact, and PDF/PNG layers can
> be separated. Redact from the source, then capture. If the source cannot be
> redacted, **do not publish the artifact at all** — the finding stands on the
> documented observation, and a partially redacted screenshot of payroll data is
> worse than no screenshot.

---

## 4. Automated sanitization and its limits

For **text** artifacts:

```bash
python3 scripts/evidence_sanitizer.py --input <raw-capture> --output-dir ./sanitized-out
```

The sanitizer flags, and never prints: SQL `INSERT` statements, `CREATE TABLE`
statements, email addresses, SQL connection strings, credential-bearing CLI
arguments, and bearer tokens. It reports **class and line number only**.

> ⚠️ **It cannot help with screenshots.** Rows rendered in a terminal or editor are
> pixels. Every image artifact in this milestone requires fully manual redaction
> from source, and `redaction_status` must be set by a person.

Self-test: `python3 scripts/evidence_sanitizer.py --self-test`

---

## 5. LLM data-handling record

Step 4 of M3 involved submitting extracted `INSERT` rows to a third-party AI
assistant to convert dense SQL into a readable table.

### 5.1 Disclosure record

| Field | Value |
| --- | --- |
| Data submitted | `staff` and `shareholders` `INSERT` rows |
| Data subject | Synthetic in this environment |
| Production equivalent | **Real names, job titles, departments and salaries; real shareholdings** |
| Service | Third-party conversational AI assistant |
| Justification | Convenience of format conversion |
| Minimisation before submission | **Partial** — tables were restricted, but row content was not stripped |
| Provider retention | Unknown; depends on service and tier |
| Training reuse | Possible on consumer tiers |
| Withdrawal | **Not possible.** Submission is disclosure, not a local operation. |

### 5.2 Assessment

The step was acceptable **in a synthetic lab** and would be **unacceptable against
a production healthcare system.** In production it would constitute a personal-data
disclosure to a third party, likely requiring assessment under the organisation's
data-protection obligations and almost certainly lacking a lawful basis.

### 5.3 Correct alternative

The conversion required was trivial:

```bash
# Extract INSERT statements for one table — local, no disclosure
grep -i "INSERT INTO \`staff\`" mediroza_db_backup_2019.sql

# Shape the output without sending it anywhere
grep -i "INSERT INTO \`staff\`" mediroza_db_backup_2019.sql \
  | tr ',' '\n' | sed 's/^[[:space:]]*//'
```

No network call, no disclosure, faster, fully auditable. **A local script should
always be preferred to an external service when handling personal data.**

### 5.4 Rule adopted

Where an LLM would process substantially-identifiable data:

1. Minimise locally **first**.
2. Prefer a local script; treat an LLM as a fallback, not a default.
3. Record the decision and the justification.
4. If an LLM is used anyway, record the data classes submitted and the provider.

Recorded here because the reasoning is the transferable part. A finding that
documents its own methodological weakness is more credible than one that does not.

---

## 6. Evidence handling procedure

| Step | Action | Owner |
| --- | --- | --- |
| 1 | Raw artifacts stored in the access-controlled off-repository location | Assessor |
| 2 | SHA-256 recorded **before** any redaction | Assessor |
| 3 | Run the sanitizer over text captures | Assessor |
| 4 | Redact from source — never crop or blur | Assessor |
| 5 | Manual review of every artifact against §3 | Assessor |
| 6 | Second-person review where personal data is involved | Reviewer |
| 7 | Place reviewed artifacts in `evidence/screenshots/M3/` | Assessor |
| 8 | Update `artifact_present` and `redaction_status` in the register | Assessor |
| 9 | Convert placeholders to live image references | Assessor |
| 10 | Record SHA-256 of the redacted copy | Assessor |

> **Step 6 is not optional for this milestone.** Every other milestone's evidence
> can reasonably be self-reviewed. Evidence of a payroll exposure warrants a
> second pair of eyes before publication.

---

## 7. Image references

Intended paths are recorded in fenced code so no broken link exists while the
artifacts are absent.

```
![Placeholder — NW-B083-M3-E03](../../evidence/screenshots/M3/NW-B083-M3-E03_old-directory-listing.png)
![Placeholder — NW-B083-M3-E02](../../evidence/screenshots/M3/NW-B083-M3-E02_pdf-comments-metadata.png)
```

Convert to live references only after artifacts exist, are sanitised, are manually
reviewed, and are registered.

---

## 8. Outstanding work

| # | Task | Status |
| --- | --- | --- |
| 1 | Capture the 8 M3 artifacts to the raw store | ❌ Not done |
| 2 | Sanitize text captures | ❌ Not done |
| 3 | Redact **from source** — no cropping or blurring | ❌ Not done |
| 4 | Confirm no credential or connection-string material appears in any artifact | ❌ Not done |
| 5 | Obtain second-person review of all M3 artifacts | ❌ Not done |
| 6 | Place reviewed artifacts in `evidence/screenshots/M3/` | ❌ Not done |
| 7 | Update the register | ❌ Not done |
| 8 | Convert §7 placeholders to live references | ❌ Blocked by 6 |
| 9 | Record SHA-256 for each artifact | ❌ Not done |
| 10 | Confirm the raw backup and extracted rows are **not** in the repository or its history | ❌ Not done |
| 11 | Review `git log --all` for any accidental inclusion | ❌ Not done |

Item 11 is the highest-consequence. Verify it before publication:

```bash
git log --all --diff-filter=A --name-only --format='' \
  | sort -u | grep -Ei '\.(sql|pdf|pem|key|env)$'
```

Expected result: **no output.**

Until items 1–7 are complete, `NW-B083-M3-F01`, `F02` and `F03` remain at status
**Documented** rather than **Evidence-attached**, and F06/F07 retain **provisional**
risk ratings.
