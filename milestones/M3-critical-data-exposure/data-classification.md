# M3 — Data Classification

**Milestone:** Deep Reconnaissance / Critical Data Exposure · **Status:** ✅ Documented

---

> ## 🔒 No data values are published in this document
>
> This file records the **structure** and **sensitivity classes** of the exposed
> data. It contains no names, no salary figures, no share percentages, no share
> classes, no email addresses and no row contents.
>
> Why: publication is where most real engagements leak. The finding is fully
> substantiated by the schema and the readability, and neither requires a value.

---

## 1. Tables identified

Two tables were extracted from `mediroza_db_backup_2019.sql`, and only these two.

| # | Table | Rows extracted | Purpose | Sensitivity |
| --- | --- | --- | --- | --- |
| 1 | `staff` | Minimal — sufficient to prove readability | Employee compensation register | 🔴 **Critical** |
| 2 | `shareholders` | Minimal — sufficient to prove readability | Ownership register | 🔴 **Critical** |

> **Extent caveat.** These two tables are **not** the full extent of the exposure.
> Other tables exist in the file and were deliberately **not** extracted. The true
> exposure is *at least* this large.

---

## 2. `staff` — schema

Column names as they appear in the `INSERT` statements:

| # | Column | Data class | Identifies a person? | Sensitivity |
| --- | --- | --- | --- | --- |
| 1 | Staff name | Direct identifier | ✅ Yes | 🔴 High |
| 2 | Job title | Employment attribute | 🟠 Indirectly | 🟠 Medium |
| 3 | Department | Organisational attribute | 🟠 Indirectly | 🟠 Medium |
| 4 | Monthly salary | Financial attribute | 🟠 Indirectly, via name | 🔴 **High** |

**Classification:** 🔴 **Restricted — personal financial data**
Contains direct identifiers joined to compensation. Compensation data is treated
as highly sensitive in essentially every privacy regime because it is both
financial and a strong predictor of personal circumstance.

---

## 3. `shareholders` — schema

| # | Column | Data class | Identifies a person? | Sensitivity |
| --- | --- | --- | --- | --- |
| 1 | Shareholder name | Direct identifier | ✅ Yes | 🔴 High |
| 2 | Share percentage | Ownership attribute | 🟠 Indirectly | 🔴 High |
| 3 | Share class | Ownership/governance attribute | 🟠 Indirectly | 🟠 Medium |

**Classification:** 🔴 **Restricted — confidential corporate information**
Ownership structure is commercially sensitive and frequently subject to
disclosure-control obligations independent of privacy law.

---

## 4. Why each column matters

### `staff`

| Column | Why it matters beyond the obvious |
| --- | --- |
| Name | The join key for everything else. Without it the remaining columns are merely interesting; with it they are personal data. |
| Job title | Reveals who holds system access — and therefore who is worth targeting technically. |
| Department | Completes the org chart and identifies business-critical roles. |
| Monthly salary | The highest-value column. Enables grievance claims, targeted phishing and extortion. |

### `shareholders`

| Column | Why it matters |
| --- | --- |
| Shareholder name | Reveals who ultimately benefits — organisations, trusts or individuals. |
| Share percentage | Reveals control. Combined with share class it establishes voting power and therefore who can influence the organisation. |
| Share class | Determines dividend and voting rights. Together with percentage it reveals the full governance structure. |

---

## 5. Classification matrix

| Data class | Classification | Sensitivity | Legal/regulatory character | Handling requirement |
| --- | --- | --- | --- | --- |
| Staff name | Personal identifier | 🔴 High | Personal data | Encrypt at rest and in transit; restrict to business need |
| Job title | Personal / employment data | 🟠 Medium | Personal data where linked to an identifier | Same as above |
| Department | Personal / employment data | 🟠 Medium | Personal data where linked | Same as above |
| **Monthly salary** | **Financial personal data** | 🔴 **Critical** | Special-category in some regimes; high-risk everywhere | Encrypt; restrict to payroll-authorised roles; never store in a web root |
| Shareholder name | Corporate identity data | 🔴 High | May be personal or organisational depending on form | Restrict; disclosure control may apply |
| **Share percentage** | **Ownership data** | 🔴 **Critical** | Market-sensitive; disclosure-controlled | Restrict; treat as confidential commercial information |
| Share class | Governance data | 🟠 Medium | Disclosure-controlled | Restrict |
| Document metadata (`Author`) | Personal identifier | 🟠 Medium | Personal data | Strip before distribution |
| Document metadata (`Comments`) | Internal operational | 🔴 High | May disclose system or security detail | Strip before distribution |

---

## 6. How the data was exposed

| Property | Value | Consequence |
| --- | --- | --- |
| Format | Cleartext SQL | Readable without any key or tooling |
| Structure | Normalised `INSERT` rows | Immediately queryable; usable as-is |
| Anonymisation | **None** | Direct identifiers joined to sensitive attributes |
| Encryption | **None** | No key required |
| Integrity protection | **None** | Tamperable; and a backup implies restorability |
| Access control | **None** | Anonymous HTTP request |
| Location | Inside the web document root | Served directly by the web server |
| Discoverability | **High** | Directory listing; also disclosed in `robots.txt` |
| Data format portability | **High** | `INSERT` rows load into any compatible database in one command |

> The final row deserves emphasis. This is not merely *readable* data — it is
> **machine-consumable** data. An attacker needs no parsing skill and no
> reconnaissance of the schema; the file contains both.

---

## 7. Data handling applied

| Action | Rule | Applied |
| --- | --- | --- |
| Extraction | Only the two tables constituting the finding | ✅ |
| Row extraction | Minimal — sufficient to prove readability | ✅ |
| Format demonstration | Synthetic example in this repository; real values never used | ✅ |
| Retention of extracted rows | Discarded after readability was proven | ✅ |
| Publication of values | **Prohibited** | ✅ None published |
| Identity in published text | Masked as `j.m***` | ✅ |
| Screenshots | Any future artefact showing rows requires full row masking | ⬜ Pending sanitisation |
| Third-party submission | Hash identifiers only in M2; **M3 row data was submitted to an LLM once — recorded** | ⚠️ See [`evidence.md`](./evidence.md) §5 |

---

## 8. Synthetic schema illustration

> **`SYNTHETIC — NOT CLIENT DATA`.** Generated by
> [`../../scripts/sample-data/`](../../scripts/README.md) to demonstrate the report
> format. Values are invented and correspond to no person.

```sql
-- SYNTHETIC — NOT CLIENT DATA
-- Illustrative schema only. No real value appears anywhere.

CREATE TABLE `staff_example` (
  `id`            INT AUTO_INCREMENT PRIMARY KEY,
  `full_name`     VARCHAR(120) NOT NULL,
  `job_title`     VARCHAR(120) NOT NULL,
  `department`    VARCHAR(120) NOT NULL,
  `monthly_salary` DECIMAL(10,2) NOT NULL
);

-- Illustrative row shape. All values fabricated.
INSERT INTO `staff_example`
  (`full_name`, `job_title`, `department`, `monthly_salary`)
VALUES
  ('<REDACTED>', '<REDACTED>', '<REDACTED>', 0.00);

CREATE TABLE `shareholders_example` (
  `id`                INT AUTO_INCREMENT PRIMARY KEY,
  `shareholder_name`  VARCHAR(160) NOT NULL,
  `share_percentage`  DECIMAL(5,2) NOT NULL,
  `share_class`       VARCHAR(60)  NOT NULL
);

-- Illustrative row shape. All values fabricated.
INSERT INTO `shareholders_example`
  (`shareholder_name`, `share_percentage`, `share_class`)
VALUES
  ('<REDACTED>', 0.00, '<REDACTED>');
```

---

## 9. Classification conclusions

| # | Conclusion |
| --- | --- |
| 1 | Both tables are 🔴 Restricted. Neither is publishable in any form that retains values. |
| 2 | `monthly_salary` and `share_percentage` are the highest-value columns and the reason the finding is Critical. |
| 3 | Direct identifiers are present, so the data is personal data — not merely "internal information". |
| 4 | The exposure needs no interpretation: cleartext, complete, structured, machine-consumable. |
| 5 | **Only two of an unknown number of tables were examined.** The exposure is a floor, not a ceiling. |
| 6 | Document metadata (`Author`, `Comments`) is itself classified data, and was the discovery vector. |
| 7 | Data currency is unverified. **Staleness does not reduce sensitivity.** |

---

## 10. Outstanding

| # | Item | Required |
| --- | --- | --- |
| 1 | Confirm the actual table names and full schema | Client-side review of the real backup |
| 2 | Establish how many tables and rows the backup contains | Client-side review |
| 3 | Confirm whether any other backups exist elsewhere | Client-side review |
| 4 | Confirm data currency | Database owner |
| 5 | Establish the data's lawful basis and retention period | Data protection owner |
| 6 | Determine whether notification obligations are engaged | Counsel |
| 7 | Review access logs for prior download | Infrastructure owner |

> Items 1–7 require client-side access that the assessment did not have. They are
> listed so the client knows what remains unknown — **not** as a suggestion that
> the tester pursue them.
