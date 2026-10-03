# Procedure 6 — File and document security

Assessing encryption strength, key strength, metadata hygiene, and backups as data
assets.

> **Authorisation precondition.** Assessment of files the client has supplied or
> that the client has approved for retention. No password is published, and no
> document content is reproduced in a report.

---

## 1. Why documents need their own procedure

A document crosses several boundaries at once — storage, delivery, encryption,
metadata, retention — and a control at any one of them can be the only thing
standing between the content and disclosure.

| Boundary | Control | Failure mode |
| --- | --- | --- |
| Storage location | Outside the web root | File reachable by URL |
| Delivery | Authorising endpoint | Session check is the only barrier |
| Encryption | Strong key, correctly applied | Apparent protection with none |
| Metadata | Stripped on export | Internal detail travels with the file |
| Retention | Defined and enforced | Forgotten artefacts persist indefinitely |

---

## 2. Assessing encryption without publishing keys

### 2.1 What may be reported

| Reportable | Not reportable |
| --- | --- |
| Encryption present or absent | The key itself, in any form |
| Key length and character classes | Partially masked keys |
| Whether a key is a dictionary entry | The wordlist's contents |
| Which wordlist class succeeded | The specific wordlist entries tried |
| Whether a file opened after recovery | The file's content |

> The rule is simple: **the strength of a key is reportable; the key is not.** A
> finding of "single character class, dictionary entry, recoverable with a
> top-100 list" is actionable and discloses nothing.

### 2.2 Why partial masking is not acceptable for credentials

A partially masked credential is still a credential disclosure. A reader cannot
tell how much was removed, and a one-character difference is all that stands between
the published value and a working one. Credentials are withheld entirely;
`--password='<REDACTED>'` replaces the argument.

---

## 3. Key-strength assessment

| Indicator | Reading | Engagement observation |
| --- | --- | --- |
| Single character class | Human-chosen | ✅ All three files |
| Dictionary entry | Human-chosen from a common pattern | ✅ All three files |
| Recoverable with a small built-in list | No meaningful protection | ✅ Two of three |
| Requires a larger wordlist | Slightly better; still trivial | ✅ One of three |
| Resists a wordlist **and** rule-based mutation | Genuine strength | ⬜ **Not established** |

### 3.1 The key measurement gap

| Test | Performed | Effect |
| --- | --- | --- |
| Static dictionary (top-100) | ✅ | Two keys recovered |
| Larger wordlist | ✅ | Third key recovered |
| **Rule-based mutation** | ❌ | Strength ceiling unknown |
| **Targeted / organisational wordlist** | ❌ | Unknown whether keys relate to the organisation |

> Both missing tests would most likely have recovered **more** keys, not fewer. The
> finding is therefore reported as provisional with the direction of the residual
> uncertainty stated.

### 3.2 The structural point

An offline attack has no rate limit, no lockout, no MFA prompt and no log entry. The
only variables are key strength and the attacker's wordlist. **Any application-side
control contributes nothing.** This is why "the document is password protected" is
not a control in any report that matters.

---

## 4. Metadata hygiene

### 4.1 What to inspect

| Field | Risk if retained |
| --- | --- |
| `Author`, `Creator`, `LastModifiedBy` | Identifies a person; aids account targeting |
| `Comments`, `Keywords` | Free text — operational notes, paths, passwords |
| `Producer`, `CreatorTool` | Stack and version detail |
| `Template` fields | Internal file locations |
| XMP metadata | Duplicates the above in a second format |

### 4.2 What the engagement found

| Field | Content | Value to an attacker |
| --- | --- | --- |
| `Author` | A staff account identifier, masked `j.m***` | An account to target |
| `Comments` | An internal location, a database backup, a migration event, a retention instruction | **A directly actionable lead** |

> The `Comments` field was worth more than every other metadata field combined.
> Free-text fields are where operational thinking ends up, including the
> information nobody would put in a report.

### 4.3 Metadata stripping must be a pipeline step

```bash
# Strip on export, before the document reaches anyone
exiftool -all= -overwrite_original -q "$file"

# Verify: must return nothing
exiftool -a -u -g1 "$file" | grep -Ei 'author|comment|creator|producer|template|path'
```

| Requirement | Reason |
| --- | --- |
| Automatic, not manual | A manual instruction is skipped under time pressure |
| Applied to every format leaving the system | PDFs are not the only carrier |
| Verified after stripping | Silent failures are common |
| Sensitive fields disabled at source | Stripping is a safety net, not the design |

---

## 5. Backups as data assets

A backup is a **complete, unmonitored, long-lived copy of production data**.

| Property | Consequence |
| --- | --- |
| Completeness | One file may hold every category of data at once |
| Age | Contains data that may be believed deleted |
| Retention | Often indefinite, because nobody owns the deletion |
| Location | Frequently alongside the application, inside the web root |
| Encryption | Frequently absent, because the storage is assumed trusted |
| Access control | Frequently none, because it is "just a file" |

### 5.1 Assessment steps

| Step | Action | Engagement observation |
| --- | --- | --- |
| 1 | Locate backups in web-served paths | Found under a legacy path |
| 2 | Determine whether the path is indexed | Directory listing present |
| 3 | Attempt access without credentials | Anonymous download succeeded |
| 4 | Determine whether it opens without a password | Opened with standard tooling |
| 5 | Assess contents by **structure and counts only** | 36 tables identified |
| 6 | Determine data classes present | Clinical, personal, financial, corporate |
| 7 | Destroy any local copy after assessment | No retention |
| 8 | Recommend credential rotation if any were present | Required if the dump contained credentials |

### 5.2 Minimising handling of an exposed database

| Did | Did not |
| --- | --- |
| Confirm table names | Export rows |
| Count records | Read narratives |
| Confirm values were cleartext | Analyse any individual's compensation |
| Record data classes | Retain a copy |
| Delete the local copy | Reuse the data for any purpose |

> Establishing a cleartext exposure requires reading enough to know it is cleartext.
> It does not require reading further. **Handling burden is a design input for
> exposure assessment**, not an afterthought.

---

## 6. Correct controls

| Control | Requirement |
| --- | --- |
| Storage | Backups outside every web-served path, on separate infrastructure |
| Encryption at rest | Managed KMS; keys not on the backup host |
| Access | Role-restricted, logged, alerted |
| Retention | Defined expiry, enforced automatically |
| Deployment gate | CI fails on `.sql`, `.bak`, `.dump` and archives under a web root |
| Document keys | CSPRNG-generated, ≥20 characters, unique per document, never in a URL or filename |
| Document delivery | Authorising endpoint, not a static path |
| Metadata | Stripped automatically on export, verified |
| Segregation | Clinical, payroll and governance data not co-located in one store |

> The last row is the structural lesson. One file containing every data category is
> what turned a configuration mistake into a maximum-impact breach.

---

## 7. Retest criteria

| # | Criterion | Pass condition |
| --- | --- | --- |
| 1 | Document keys resist dictionary **and** mutation attack | No key recovered; report precisely what was attempted |
| 2 | Keys are generated, unique, ≥20 characters | Verified by process and code review |
| 3 | Keys absent from URLs, filenames, mail and chat | Confirmed by inspection |
| 4 | Metadata absent from newly issued documents | Verification command returns nothing |
| 5 | Metadata stripping is automatic | Export without manual intervention yields no metadata |
| 6 | No backups in any web-served path | Filesystem search returns zero matches |
| 7 | Backups encrypted with separated keys | Restore impossible without the KMS key |
| 8 | Retention enforced | Expiry configured; no indefinite-retention notes |
| 9 | Access to documents enforced independently of the key | No session ⇒ no document |
| 10 | Data segregated | Governance and payroll data not in the clinical store |

---

## 8. Checklist

- [ ] Authorisation covers assessment of the files in question
- [ ] No key, hash or partially masked credential recorded anywhere
- [ ] Key strength characterised qualitatively, not quantitatively by value
- [ ] Negative controls performed (a failed recovery proves the tool works)
- [ ] Metadata inspected on a decrypted copy, content not read
- [ ] Backup locations searched across **all** web-served paths
- [ ] Exposed data assessed by structure and counts only
- [ ] Local copies destroyed after assessment
- [ ] Retention and ownership problems identified, not just the file
- [ ] Untested key-strength tests listed with the direction of the uncertainty