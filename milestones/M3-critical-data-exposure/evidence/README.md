# M3 — Evidence Index

**Milestone:** Deep Reconnaissance / Critical Data Exposure · **Registered observations:** 8 · **Artifacts attached:** 0

> 🔴 **Highest-sensitivity milestone.** This milestone evidences exposure of staff
> compensation and shareholder data. Every artifact requires row-level redaction
> **from source**, second-person review, and manual verification that no value
> survives.

Narrative and handling standard: [`../evidence.md`](../evidence.md) ·
Global policy: [`../../../evidence/README.md`](../../../evidence/README.md) ·
Register: [`../../../evidence/evidence-register.csv`](../../../evidence/evidence-register.csv)

---

## 1. Evidence register — M3

| Evidence ID | Description | Finding | Sensitivity | Artifact |
| --- | --- | --- | --- | --- |
| `NW-B083-M3-E01` | `exiftool` — `Author` metadata field | F05 | 🟠 Personal | ❌ |
| `NW-B083-M3-E02` | `exiftool` — `Comments` metadata field (the internal note) | F05 | 🔴 Internal | ❌ |
| `NW-B083-M3-E03` | Directory index at `/old/` listing the backup | F06 | 🔴 Internal | ❌ |
| `NW-B083-M3-E04` | Download of `mediroza_db_backup_2019.sql` | F06, F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E05` | `staff` schema and data classes | F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E06` | `shareholders` schema and data classes | F07 | 🔴 Confidential | ❌ |
| `NW-B083-M3-E07` | Identity correlation against one staff record | F05, F07 | 🔴 Personal | ❌ |
| `NW-B083-M3-E08` | Cross-reference to `NW-B083-M1-E01` (`robots.txt` `/old/` disclosure) | F06 | 🟠 Internal | ❌ |

---

## 2. Expected artifacts

| Evidence ID | Type | Filename convention | Mandatory redaction |
| --- | --- | --- | --- |
| `NW-B083-M3-E01` | Terminal capture | `NW-B083-M3-E01_exiftool-author-masked.txt` | Mask the account identifier to `j.m***` |
| `NW-B083-M3-E02` | Terminal capture | `NW-B083-M3-E02_exiftool-comments-note.txt` | Review every other metadata field present; strip host paths |
| `NW-B083-M3-E03` | Screenshot | `NW-B083-M3-E03_old-directory-listing.png` | Confirm no other file contents visible; crop from source |
| `NW-B083-M3-E04` | Terminal capture | `NW-B083-M3-E04_backup-download-command.txt` | Remove shell history; verify no other URLs captured |
| `NW-B083-M3-E05` | Text capture | `NW-B083-M3-E05_staff-schema-masked.txt` | **All names, titles, departments and salaries removed or replaced** |
| `NW-B083-M3-E06` | Text capture | `NW-B083-M3-E06_shareholders-schema-masked.txt` | **All names, percentages and share classes removed or replaced** |
| `NW-B083-M3-E07` | Text capture | `NW-B083-M3-E07_identity-correlation-masked.txt` | Mask the identifier; publish the **role**, not the person |
| `NW-B083-M3-E08` | Text capture | `NW-B083-M3-E08_robots-txt-cross-reference.txt` | None expected |

Target directory: `evidence/screenshots/M3/`

---

## 3. Mandatory redaction — M3

### 3.1 Never publish, in any form

| Item | Class |
| --- | --- |
| Staff names | 🔴 Direct personal identifier |
| Monthly salary figures | 🔴 Personal financial data |
| Job titles and departments *where tied to an individual* | 🟠 Employment data |
| Shareholder names | 🔴 Confidential ownership data |
| Share percentages | 🔴 Confidential ownership data |
| Share classes | 🟠 Confidential governance data |
| Email addresses, including local-parts | 🟠 Personal identifier |
| Any real `INSERT` row, in whole or in part | 🔴 Aggregate of the above |
| Connection strings, credentials or API keys present in the backup | 🔴 Not extracted; must be positively confirmed absent |
| Patient document content | 🔴 Potentially clinical |

### 3.2 Safe to publish

| Item | Sufficient to substantiate |
| --- | --- |
| `robots.txt` output | F06 corroboration |
| The directory index with a single filename | F06 |
| Metadata field **names**, with the author masked | F05 |
| The `Comments` note quoted in full | F05 — this is the finding |
| Table and column names | F07 |
| Data-class descriptions | F07 |
| Fully masked example rows | F07 |
| The matched individual's **role title only** | F07 chain closure |
| Synthetic reproductions | Format illustration |

### 3.3 The identity, specifically

The engagement identified an individual — the IT Systems Administrator whose
account appears as the document `Author` and who matches a `staff` record.

| Publish | Withhold |
| --- | --- |
| The role title (`IT Systems Administrator`) | The account identifier |
| That the correlation was positive | The masked or full identifier |
| That the role is consistent with the metadata note | Any attribute of that record beyond role |

Published consistently as `j.m***`.

> **Attribution discipline.** This is an organisational control failure, not a
> personal one. The finding must not read as blame. Publishing a named
> individual's salary alongside a note that they misplaced a backup would be both
> a privacy failure and unprofessional.

---

## 4. Redaction checklist

- [ ] Redacted **from source** — no cropping, blurring or overlay boxes
- [ ] Every `INSERT` value verified individually, not by pattern alone
- [ ] `j.m***` masking applied consistently in prose, code blocks and filenames
- [ ] Column names retained; values removed
- [ ] No host path, hostname, IP or internal URL beyond the authorized target
- [ ] Connection strings and credentials **positively confirmed absent** — not merely "not noticed"
- [ ] Shell history and terminal scrollback excluded
- [ ] Browser tab, bookmarks and address-bar history excluded
- [ ] Editor tabs and file-tree panes checked for adjacent files
- [ ] Second-person review completed
- [ ] SHA-256 recorded before redaction; redacted copy hashed separately
- [ ] `redaction_status` updated in the register by a person
- [ ] Git history checked for accidental inclusion

### 4.1 History check — run before publication

```bash
# No forbidden artefact types should ever appear
git log --all --diff-filter=A --name-only --format='' \
  | sort -u | grep -Ei '\.(sql|pdf|pem|key|env|bak|dump)$'

# Expected: no output

# Confirm no large blob was committed
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3 > 1048576 {print $3, $4}' | sort -rn | head
```

If either command returns output, **stop.** Follow
[`../../../docs/ethical-considerations.md`](../../../docs/ethical-considerations.md) §7.

---

## 5. Automated sanitization

```bash
python3 scripts/evidence_sanitizer.py --input <raw-capture> --output-dir ./sanitized-out
python3 scripts/evidence_sanitizer.py --self-test
```

Flags SQL `INSERT`/`CREATE TABLE` statements, email addresses, connection strings,
credential-bearing arguments and bearer tokens — reporting **class and line number
only**, never values.

> ⚠️ **Text only.** A terminal screenshot of a payroll dump is pixels. It requires
> complete manual redaction from source. Treat any unredacted row appearing in an
> image artifact as a disclosure incident and follow §7 of the ethical
> considerations.

---

## 6. Image references

Intended paths recorded in fenced code so no broken link exists while artifacts are
absent.

```
![Placeholder — NW-B083-M3-E02](../../../evidence/screenshots/M3/NW-B083-M3-E02_exiftool-comments-note.txt)
![Placeholder — NW-B083-M3-E03](../../../evidence/screenshots/M3/NW-B083-M3-E03_old-directory-listing.png)
```

Convert to live references only after artifacts exist, are redacted from source,
have passed second-person review, and are registered.

---

## 7. Outstanding work

| # | Task | Status |
| --- | --- | --- |
| 1 | Capture the 8 M3 artifacts to the raw store | ❌ Not done |
| 2 | Sanitize text captures | ❌ Not done |
| 3 | Redact from source, artifact by artifact | ❌ Not done |
| 4 | Positively confirm no credential or connection-string material in any artifact | ❌ Not done |
| 5 | Obtain second-person review | ❌ Not done |
| 6 | Place reviewed artifacts in `evidence/screenshots/M3/` | ❌ Not done |
| 7 | Update `artifact_present` and `redaction_status` in the register | ❌ Not done |
| 8 | Convert §6 placeholders to live references | ❌ Blocked by 6 |
| 9 | Record SHA-256 for each artifact | ❌ Not done |
| 10 | Verify `git log --all` contains no `.sql` or `.pdf` | ❌ Not done — **highest priority** |
| 11 | Confirm raw backup and extracted rows exist nowhere in the working tree | ❌ Not done |

Until items 1–7 are complete, `NW-B083-M3-F01`, `F02` and `F03` remain at status
**Documented**, and F06/F07 retain **provisional** risk ratings per
[`../../../risk/cvss-assessment.md`](../../../risk/cvss-assessment.md).
