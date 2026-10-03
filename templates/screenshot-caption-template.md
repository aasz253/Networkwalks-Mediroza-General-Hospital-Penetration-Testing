# Evidence caption — {{EVIDENCE ID}}

| Field | Value |
| --- | --- |
| **Evidence ID** | `NW-B083-<MS>-E<nn>` |
| **Artifact path** | `evidence/screenshots/<MS>/NW-B083-<MS>-E<nn>_<slug>.<ext>` |
| **Artifact present** | NO |
| **Milestone / step** | |
| **Supports finding** | `{{ID}}` or `n/a` |
| **Data class** | none / internal / personal / clinical / financial / credential |
| **Contains PII** | NO / YES |
| **Sanitization status** | not_started / sanitized / reviewed / published |
| **Reviewer** | `UNASSIGNED` |
| **Captured at** | `UNKNOWN` |
| **Tool and version** | `UNKNOWN` |

---

## 1. Caption

One sentence describing what is visible, in neutral language.

| Good | Bad |
| --- | --- |
| "Login error response for a non-existent username" | "Attacker steals the admin account" |
| "Directory index rendering seven entries" | "Everything is exposed" |

> A caption states what is visible. Interpretation belongs in the finding.

---

## 2. What the artifact shows

| Field | Observation |
| --- | --- |
| Request | Method, path, parameters — **parameter values redacted where sensitive** |
| Response | Status code, relevant headers, relevant body content |
| Anomaly | The specific line, header or field that constitutes the observation |

---

## 3. Sanitization record

Every item must be addressed, not merely considered.

| Item | Present? | Action taken |
| --- | --- | --- |
| `Cookie` / `Set-Cookie` | | Removed |
| `Authorization` header or bearer token | | Removed |
| Session identifiers | | Removed |
| CSRF tokens | | Removed |
| E-mail addresses | | Replaced with `<REDACTED-EMAIL>` |
| IP addresses | | Replaced with `<REDACTED-IP>` |
| Internal hostnames | | Replaced or generalised |
| Internal filesystem paths | | Generalised |
| Individual names or account identifiers | | Masked, e.g. `j.m***` |
| Credentials | | Value withheld entirely |
| Special-category or clinical data | | Not captured; recorded as class and count |
| Compensation or ownership values | | Not captured; schema only |
| Bulk data rows | | Not captured |

| Tool used | Version |
| --- | --- |
| `scripts/evidence_sanitizer.py` | 1.0.0 |

> The sanitiser is a **first pass**. It cannot recognise a salary or a diagnosis in a
> sentence. Manual review under [`../../evidence/README.md`](../evidence/README.md) §4
> is mandatory.

---

## 4. Provenance

| Field | Value |
| --- | --- |
| Collected by | |
| Collection method | |
| Working copies location | |
| Copies destroyed | |
| Second-person review | `UNASSIGNED` |

---

## 5. Publication decision

| Question | Answer |
| --- | --- |
| Suitable for a client report? | |
| Suitable for a public repository? | |
| Additional masking required? | |
| Reviewer decision | `UNASSIGNED` |

---

## 6. Rules

| Rule | Reason |
| --- | --- |
| Register the observation **before** processing the artifact | The ID must not depend on whether evidence exists |
| Never overwrite the original | The chain of custody requires it |
| Filenames carry no severity, data class or personal name | Filenames leak through directory listings |
| A placeholder is not evidence | A file with the intended name and a description of what it would show invites fabrication |
| Two-person review before publication | The author may not self-approve a redaction |