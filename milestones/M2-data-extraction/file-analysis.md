# M2 — File Analysis

**Milestone:** Data Extraction / File Security · **Status:** ✅ Documented

---

## 1. File identification

Non-identifying labels are used throughout this repository. Original filenames are
recorded once, here, for traceability with the source system.

| Label | Original filename | Source | Size | Hash |
| --- | --- | --- | --- | --- |
| `LAB-PDF-01` | `patient_report_1.pdf` | `/patient/reports/` via M1 Step 6 | Not recorded | Not recorded |
| `LAB-PDF-02` | `patient_report_2.pdf` | `/patient/reports/` via M1 Step 6 | Not recorded | Not recorded |
| `LAB-PDF-03` | `patient_report_3.pdf` | `/patient/reports/` via M1 Step 6 | Not recorded | Not recorded |

> ⚠️ **Outstanding.** File size and SHA-256 were **not recorded** in the engagement
> record. Both should have been captured immediately on download, before analysis,
> so that any later modification would be detectable. This is a process gap worth
> noting rather than back-filling with invented values.

```bash
# What should have been run on receipt
sha256sum patient_report_*.pdf
ls -l patient_report_*.pdf
```

> **The label convention is a working practice, not cosmetics.** Once a file
> carries a real name and a real hash, writing it in a report, an issue, a commit
> message or a chat message discloses it. Choosing the label at acquisition time
> removes the temptation later.

---

## 2. File format

| Property | Value | Basis |
| --- | --- | --- |
| Format | PDF | File extension and processing behaviour |
| Version | Not recorded | — |
| Producer / creator application | Not recorded for `LAB-PDF-01`/`02`; readable only after decryption for `LAB-PDF-03` | See §4 |
| Encryption | User password present on all three | Observed — the files would not open without a key |
| Permissions password | Not observed | No editing restriction was encountered |
| JavaScript / embedded objects | Not assessed | — |
| Digital signature | **None observed** | No signature was present or indicated |
| Object count / page count | Not recorded | — |

---

## 3. Security-property analysis

The properties below are what determine whether a document is safe to distribute.

| # | Property | Question | Assessment |
| --- | --- | --- | --- |
| 1 | **Confidentiality** | Can an unauthorised party read the content? | **Depends entirely on the password.** Encryption present; key strength assessed in [`encryption-assessment.md`](./encryption-assessment.md) |
| 2 | **Key strength** | Is the password resistant to guessing? | ❌ **Weak on all three.** Recovered in this engagement |
| 3 | **Metadata hygiene** | Does the file carry internal information? | ❌ **Fail on `LAB-PDF-03`** — author plus an internal operational note. See [M3](../M3-critical-data-exposure/) |
| 4 | **Integrity** | Can the recipient verify the file is unaltered? | ⚠️ **No signature observed.** A tampered document would be undetectable |
| 5 | **Origin authenticity** | Does the recipient know who produced it? | ❌ No signature. The metadata author field is not an authenticity control |
| 6 | **Access control** | Is access governed server-side? | ❌ **No.** The documents were static files in the web root, retrieved once the login was bypassed — [F03](../../findings/verified-findings/NW-B083-M1-F03-document-access-control.md) |
| 7 | **Permissions** | Can the recipient print, copy or extract? | Not assessed. Permissions are not a confidentiality control — the key is what protects content |
| 8 | **Residual data** | Does the file retain prior content or revisions? | Not assessed — incremental-update history can leave earlier content recoverable. Worth checking on any document template |
| 9 | **Embedded content** | Scripts, attachments, launch actions? | Not assessed. Relevant if documents are opened in a viewer that executes actions |
| 10 | **Downstream leakage** | Can content be extracted once opened? | ⚠️ Weak by nature. A password-protected PDF viewed on screen can generally be photographed |

### 3.1 The most important line in that table

> **#2, #3, #4, #5, #6 are all controls the application owner actually had, and
> #2, #3 and #6 failed.**

A document password alone would never have been sufficient. The defensible
position is that **access control must carry the security**, and document-level
protection is an additional layer — never the only one.

---

## 4. Metadata inventory

| File | Metadata readable without decryption | Metadata readable after decryption | Findings |
| --- | --- | --- | --- |
| `LAB-PDF-01` | Minimal — encryption state only | Not attempted | — |
| `LAB-PDF-02` | Minimal — encryption state only | Not attempted | — |
| `LAB-PDF-03` | Minimal — encryption state only | ✅ Yes | **F05 — sensitive metadata** |

### 4.1 Fields observed on `LAB-PDF-03`

| Field | Value | Sensitivity | Concern |
| --- | --- | --- | --- |
| `Author` | `j.malik` — **masked in publication** as `j.m***` | 🟠 Personal — an individual's identifier | Correlates a document with a specific staff account |
| `Comments` | `DB backup moved to /old before site migration, do not delete` | 🔴 **Internal operational** | Names an internal system, a migration event, a filesystem location and a retention instruction |
| Encryption state | Password-protected | — | Protection was present; it did not survive |
| Other fields | Not recorded | — | — |

Full analysis: [M3 exposure analysis](../M3-critical-data-exposure/exposure-analysis.md)

### 4.2 Why the metadata fields matter individually

| Field | What it tells an attacker |
| --- | --- |
| `Author` | Which staff account touched the document. A local-part email or username maps directly to an account and often to a role. |
| `Comments` | An internal location (`/old/`), an internal event (a site migration), and the belief that the item was still needed ("do not delete"). Each is a lead. |
| Producer / creator tool | Sometimes includes a **user path** — on Windows builds this frequently reveals a hostname and a directory structure. Not observed here, but routinely worth checking. |
| Creation / modification dates | Business timeline: when a migration happened, how stale a document is, whether a reissued version exists elsewhere |

> **Practical note.** `Comments` and `Keywords` are free-text fields that people
> genuinely use as scratch space. Treating them as sensitive is not paranoia — this
> engagement's entire Critical chain in M3 began with one of them.

---

## 5. Handling of the files during analysis

| Action | Performed | Rationale |
| --- | --- | --- |
| Downloaded from the portal | ✅ | Necessary to assess the files — this is what F03 exposed |
| Opened to read content | ❌ | Content was not the objective and was out of scope |
| Keys recovered offline | ✅ | The core M2 activity |
| File decrypted to a temporary copy | ✅ One file | Required to read metadata |
| Decrypted copies retained | ❌ | Discarded after metadata extraction |
| Content read or transcribed | ❌ | Never |
| Content published | ❌ | Never — no patient data exists in this repository |
| Files committed to the repository | ❌ | `.gitignore` excludes `*.pdf` and `*.sql` |
| Files uploaded to any third-party service | ✅ **Hash/keys only** | The provider's calculator and cracker received **hashes**, not documents. This distinction matters: a hash leaks far less than a document. |

---

## 6. Recommendations arising from file analysis

| # | Recommendation | Priority |
| --- | --- | --- |
| 1 | Record size and SHA-256 on acquisition of every artefact, before analysis | **P0** — process fix |
| 2 | Treat document-level protection as secondary; enforce authorisation server-side | **P0** |
| 3 | Generate random document keys; never derive them from a name, date or patient identifier | **P0** |
| 4 | Strip metadata on export, as a pipeline step rather than a manual one | P2 |
| 5 | Review the `Comments`/`Keywords` habit across all document generation | P2 |
| 6 | Sign documents where authenticity matters, so tampering is detectable | P3 |
| 7 | Check for residual incremental-update content when publishing revised documents | P3 |
| 8 | Store keys in a secrets manager; never in filenames, URLs, mail or chat | P1 |

---

## 7. Evidence

| Evidence ID | Description | Artifact |
| --- | --- | --- |
| `NW-B083-M2-E01` | Hash extraction output for all three files | ❌ Not attached |
| `NW-B083-M2-E06` | Structural and metadata summary | ❌ Not attached |

Registration: [`../../evidence/evidence-register.csv`](../../evidence/evidence-register.csv)
Policy: [`../../evidence/README.md`](../../evidence/README.md)
