# M1 — Initial Access

**Milestone status:** ✅ Complete · **Steps executed:** 6 of 6
**Findings produced:** `NW-B083-M1-F01`, `NW-B083-M1-F02`, `NW-B083-M1-F03`

---

## 1. Objective and authorized scope

**Objective.** Establish an authorised, evidence-backed path to the application's
protected document store, and document the weaknesses that permitted it.

| In scope for this milestone | Source |
| --- | --- |
| `https://medirozahospital.com/robots.txt` | Named target |
| `https://medirozahospital.com/patient/` and `/patient/login.php` | Disclosed in `robots.txt` |
| `https://medirozahospital.com/patient/reports/` | Reached via the login flow |
| `/staff/` | Disclosed but **not exercised** — recorded as an observation |

Out of scope: `/old/` was out of scope for M1 *testing* and became M3's subject
once the metadata clue independently pointed at it. Full scope:
[`../../docs/authorization-and-scope.md`](../../docs/authorization-and-scope.md)

---

## 2. Step-by-step record

### Step 1 — Reconnaissance: `robots.txt`

```bash
curl https://medirozahospital.com/robots.txt
```

Observed output:

```
Disallow: /patient/ Disallow: /staff/ Disallow: /old/
```

| Disclosed path | Treatment in this engagement |
| --- | --- |
| `/patient/` | Pivotal — led directly to the login page and the milestone's entire chain |
| `/staff/` | Recorded; **not exercised** |
| `/old/` | Recorded at this step, **not followed**. Became M3's entry point after an independent clue pointed there |

> **This is the most consequential step in the engagement.** Three of the four
> significant locations in the final report were named in a file that any
> anonymous client could fetch in one request.

Evidence: `NW-B083-M1-E01`

### Step 2 — Locate the login page

Requesting `https://medirozahospital.com/patient/` in a browser returned a login
form served from:

```
https://medirozahospital.com/patient/login.php
```

Observation: the `.php` extension and the `login.php` filename confirm a
server-side PHP application and reveal a naming convention useful for later
endpoint mapping.

Evidence: `NW-B083-M1-E02`

### Step 3 — Username enumeration

A secure login form returns **one** message for every failed attempt. Two inputs
were compared.

| Input | Response | Inference |
| --- | --- | --- |
| `bob` / `test123` | `Username not found` | Application distinguishes "no such user" from other failures |
| `admin` / `test123` | `Incorrect password` | `admin` **exists**; only the password was wrong |

The behavioural difference is the finding. No account was accessed at this step —
the difference alone discloses account existence.

**Why this mattered operationally:** it converted an unbounded username problem
into a single known-valid target. The next step did not have to guess.

Finding: [`NW-B083-M1-F01`](../../findings/verified-findings/NW-B083-M1-F01-username-enumeration.md)
Evidence: `NW-B083-M1-E03`, `NW-B083-M1-E04`

### Step 4 — SQL injection confirmation

A single quote was submitted as the username:

| Input | Response |
| --- | --- |
| `admin'` / `test123` | `Warning: mysqli_query(): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1` |

Analysis of the response:

| Signal | Inference |
| --- | --- |
| `mysqli_query()` | PHP with the MySQL extension; the native (non-PDO) API is in use |
| `You have an error in your SQL syntax` | The query failed to parse — input reached the SQL interpreter |
| `near ''' at line 1` | The quote terminated a string literal, leaving an unterminated fragment |
| Error text reflected to the client | Verbose error reporting is enabled in production |

A database-level syntax error is confirmation. No data was read, no data was
modified, and no further probing was needed.

**Secondary weakness noted:** verbose database errors are returned to an
unauthenticated user. That is an information-disclosure issue in its own right and
is carried into the finding record.

Finding: [`NW-B083-M1-F02`](../../findings/verified-findings/NW-B083-M1-F02-sqli-authentication-bypass.md)
Evidence: `NW-B083-M1-E05`

### Step 5 — Authentication bypass

```
username: admin' --
password: anything
```

Result: **logged in.** The portal loaded with three reports listed.

Mechanism:

| Fragment | Effect |
| --- | --- |
| `admin'` | Closes the string literal opened by the query's own quoting |
| `--` | Comments out the remainder of the statement, including the password comparison |

The query's logical shape stops being *"user = supplied AND password = supplied"*
and becomes *"user = supplied"* — a match on `admin` with the password predicate
removed entirely.

**No password was guessed, cracked or recovered.** The credential check was
deleted from the query at runtime.

**Minimality:** one authenticated request established reachability of the document
store. The portal was not enumerated further, no administrative function was
invoked, and no record was modified.

Evidence: `NW-B083-M1-E06`

### Step 6 — Retrieve the documents

Three PDFs were downloaded from the portal:

| Label | Original filename | Notes |
| --- | --- | --- |
| `LAB-PDF-01` | `patient_report_1.pdf` | Password-protected |
| `LAB-PDF-02` | `patient_report_2.pdf` | Password-protected |
| `LAB-PDF-03` | `patient_report_3.pdf` | Password-protected; carried recoverable metadata — see [M3](../M3-critical-data-exposure/) |

The documents were retrieved **without opening them**. Their content was never
read or reproduced — only their security properties were assessed in M2.

Finding: [`NW-B083-M1-F03`](../../findings/verified-findings/NW-B083-M1-F03-document-access-control.md)
Evidence: `NW-B083-M1-E07`, `NW-B083-M1-E08`

---

## 3. Attack surface established

| Surface element | Type | Auth required | Role in the chain |
| --- | --- | --- | --- |
| `/robots.txt` | Static file | No | Disclosed all three significant paths |
| `/patient/` | Redirect / entry | No | Led to the login form |
| `/patient/login.php` | Form | No | Site of F01 and F02 |
| `/patient/reports/` | Document store | Yes (bypassed) | Site of F03; source of `LAB-PDF-01…03` |
| `/old/` | Directory index | No | Site of F06; led to F07 — M3 |
| `/staff/` | Unknown | Unknown | **Not exercised.** Observation only |

Full inventory: [`attack-surface.md`](./attack-surface.md)

---

## 4. Findings summary

| ID | Title | Severity | Evidence |
| --- | --- | --- | --- |
| `NW-B083-M1-F01` | Username enumeration on login page | 🟠 Medium | `E03`, `E04` |
| `NW-B083-M1-F02` | SQL injection enabling authentication bypass | 🔴 Critical | `E05`, `E06` |
| `NW-B083-M1-F03` | Patient documents accessible after login bypass | 🔴 High | `E07`, `E08` |

Records: [`../../findings/verified-findings/`](../../findings/verified-findings/)

---

## 5. Security impact

| Impact area | Assessment |
| --- | --- |
| **Confidentiality** | Severe. An anonymous internet user reached the protected document store without any credential. |
| **Integrity** | Not demonstrated. No write path was exercised, though the same injection class would ordinarily permit modification. Recorded as *not tested* rather than *not possible*. |
| **Availability** | No impact. Interaction was minimal and sequential. |
| **Authentication** | Defeated outright. The check is not strong; it is absent from the executed query. |
| **Data at risk** | Patient report documents, and by extension whatever else the portal exposes. |
| **Detection** | A single unauthenticated request produces a verbose database error. An attacker would very likely be noticed only by a downstream alert — if one exists. |

---

## 6. Remediation

| ID | Recommendation | Priority | Addresses |
| --- | --- | --- | --- |
| R-1 | Return one generic message for every failed login — never reveal which field was wrong | P2 | F01 |
| R-2 | Replace string-concatenated SQL with parameterised queries or prepared statements at every call site | **P0** | F02 |
| R-3 | Disable verbose database error output in production; log details server-side only | **P0** | F02 |
| R-4 | Store documents outside the web root and authorise every request server-side | **P0** | F03 |
| R-5 | Add rate limiting and monitoring on repeated failed logins and on database-error responses | P1 | F01, F02 |
| R-6 | Introduce CI security checks (SAST plus a dependency audit) to prevent recurrence | P2 | F02 |

Full plan: [`../M4-final-report/remediation-plan.md`](../M4-final-report/remediation-plan.md)

---

## 7. Evidence index

| Evidence ID | Description | Milestone | Artifact |
| --- | --- | --- | --- |
| `NW-B083-M1-E01` | `robots.txt` output listing three disallowed paths | M1 | ❌ Not attached |
| `NW-B083-M1-E02` | Login page at `/patient/login.php` | M1 | ❌ Not attached |
| `NW-B083-M1-E03` | Response for a non-existent username | M1 | ❌ Not attached |
| `NW-B083-M1-E04` | Response for an existing username | M1 | ❌ Not attached |
| `NW-B083-M1-E05` | `mysqli_query()` syntax error from a single quote | M1 | ❌ Not attached |
| `NW-B083-M1-E06` | Portal loaded after bypass, three reports listed | M1 | ❌ Not attached |
| `NW-B083-M1-E07` | Download of report 1 | M1 | ❌ Not attached |
| `NW-B083-M1-E08` | Download of reports 2 and 3 | M1 | ❌ Not attached |

Policy: [`evidence/README.md`](./evidence/README.md) · Procedure to attach:
[`../../evidence/README.md`](../../evidence/README.md#5-closing-the-evidence-gap)

---

## 8. Milestone conclusion

M1 achieved its objective. A path from anonymous internet user to protected
patient documents was established in six steps using manual requests only, with no
automation and no destructive activity.

Three findings were produced: a Medium confidentiality leak (F01), a Critical
authentication defect (F02), and a High access-control consequence (F03). F02 is
the root defect — F01 made it cheap to target, F03 is what it delivered.

The most transferable lesson is at Step 1. Every location that mattered was named
in a file that required no privilege to read, and two of the three were not
followed up until later milestones.

---

## 9. Documents in this milestone

| Document | Contents |
| --- | --- |
| [`reconnaissance.md`](./reconnaissance.md) | `robots.txt` analysis and the disclosure lesson |
| [`attack-surface.md`](./attack-surface.md) | Full inventory and observations |
| [`vulnerability-analysis.md`](./vulnerability-analysis.md) | F01 and F02 analysis, CWE mapping |
| [`proof-of-concept.md`](./proof-of-concept.md) | Minimal, authorised reproduction for each finding |
| [`evidence/README.md`](./evidence/README.md) | Evidence references for M1 |
| [`../../methodology/`](../../methodology/) | General procedures applied here |
