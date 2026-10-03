# M1 — Proof of Concept

**Milestone:** Initial Access · **Status:** ✅ Executed

---

## 1. Authorization and handling notice

> These reproductions were performed **only** against the Networkwalks authorised
> training target, within the rules of engagement in
> [`../../docs/rules-of-engagement.md`](../../docs/rules-of-engagement.md).
>
> **This repository contains no exploit automation.** There is no script, no
> payload file, no scanner configuration and no wrapper for anything below. The
> steps are documented so the findings can be reviewed and defended against — not
> so they can be executed at scale.
>
> Applying any of this to a system you do not own, without explicit written
> permission from its owner, is unlawful in most jurisdictions and unethical
> everywhere else.

---

## 2. Minimality standard applied

Every reproduction below stops at the point where the finding is substantiated.

| Rule | Applied to |
| --- | --- |
| One request to prove injection | One quote |
| One request to prove the bypass | One comment payload |
| No extraction beyond proof | No `UNION`, no `GROUP_CONCAT`, no table dump |
| No modification | No write, update or delete |
| No persistence | No foothold beyond a single authenticated session |
| No credential guessing | `admin` was confirmed to exist, then bypassed — not brute-forced |
| Stop after the protected resource is reached | Portal not enumerated further; no admin function invoked |

---

## 3. PoC — `NW-B083-M1-F01` Username enumeration

### Preconditions
None. Unauthenticated, single request per attempt.

### Reproduction

| Step | Request | Observed response |
| --- | --- | --- |
| 1 | `POST` login with `username=bob`, `password=test123` | `Username not found` |
| 2 | `POST` login with `username=admin`, `password=test123` | `Incorrect password` |

### Expected vs. observed

| | Step 1 | Step 2 |
| --- | --- | --- |
| **Expected** (secure) | `Invalid credentials.` | `Invalid credentials.` |
| **Observed** | `Username not found` | `Incorrect password` |

### Success criterion
The two responses differ. Any client can distinguish them, so the existence of
`admin` is disclosed.

### Side effects
None. No account state changed.

### Evidence
`NW-B083-M1-E03`, `NW-B083-M1-E04`

---

## 4. PoC — `NW-B083-M1-F02` SQL injection and authentication bypass

### 4a — Injection confirmation

**Preconditions:** none. Unauthenticated, single request.

#### Reproduction

| Step | Request | Observed response |
| --- | --- | --- |
| 1 | `POST` login with `username=admin'`, `password=test123` | `Warning: mysqli_query(): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1` |

#### Expected vs. observed

| | Response |
| --- | --- |
| **Expected** | `Invalid credentials.` — no database detail |
| **Observed** | Full MySQL diagnostic, including the driver, the database engine, the error position and the offending fragment |

#### Success criterion
A database-level syntax error proves that request input reached the SQL
interpreter. No further probing is required to establish injectability.

#### Side effects
None. The statement failed to parse and therefore executed nothing.

#### Evidence
`NW-B083-M1-E05`

### 4b — Authentication bypass

**Preconditions:** `admin` confirmed to exist (4a, or independently via F01).

#### Reproduction

| Field | Value |
| --- | --- |
| `username` | `admin' --` |
| `password` | any value |

#### Observed result
**Logged in.** The portal loaded with three reports listed.

#### Mechanism

| Fragment | Effect |
| --- | --- |
| `admin` | Literal match against a known-valid account |
| `'` | Closes the query's own string literal |
| `--` | Comments out the remainder of the statement, including the password comparison |

The executed statement's effective logic becomes `username = 'admin'` — the
password predicate is not part of the query any more.

#### Success criterion
An authenticated session is established for `admin` without any valid
credential.

#### Side effects
A session was created. Nothing was modified; no administrative function was
invoked; the portal was not enumerated beyond what was displayed.

#### Why this is sufficient and nothing more was attempted

| Further action possible | Why not performed |
| --- | --- |
| `UNION`-based extraction of other tables | Not needed to prove authentication bypass; extraction was out of bounds |
| Modification or deletion of records | Destructive testing prohibited |
| Creating a new privileged account | Data modification prohibited |
| Enumerating other accounts | `admin` was sufficient to substantiate impact |
| Establishing persistence | Prohibited |

---

## 5. PoC — `NW-B083-M1-F03` Document access after the bypass

### Preconditions
An authenticated session obtained via the bypass in §4b.

### Reproduction

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | Authenticate using the bypass | Portal loads |
| 2 | Observe the listing | Three reports listed |
| 3 | Download all three | `patient_report_1.pdf`, `patient_report_2.pdf`, `patient_report_3.pdf` |

### Success criterion
Documents behind the authentication control are retrievable using a session
obtained without a credential.

### Side effects
None. Files were downloaded; nothing on the server was changed. **The documents
were not opened** — only their security properties were assessed, in M2.

### Evidence
`NW-B083-M1-E06`, `NW-B083-M1-E07`, `NW-B083-M1-E08`

---

## 6. Evidence capture requirements

For each reproduction above, a compliant evidence package would contain:

| Item | Requirement |
| --- | --- |
| Request | Full request as sent — URL, method, headers, body. Redact `Cookie` and any `Authorization` header. |
| Response | Full response — status line, headers, body |
| Timestamp | UTC, with timezone |
| Tool context | Client used, and any proxy in the path |
| Redaction | Applied per [`../../evidence/README.md`](../../evidence/README.md). **Never** capture live session cookies. |
| Naming | `NW-B083-M1-E<nn>_<short-description>.png` / `.txt` / `.har` |
| Registration | Row added to [`../../evidence/evidence-register.csv`](../../evidence/evidence-register.csv) with sensitivity, redaction status and verification status |
| Integrity | SHA-256 recorded before any sanitisation |

> ⚠️ **Never capture live session material.** A screenshot of an authenticated
> page will often contain a valid session cookie in a visible element, a devtools
> panel, or a URL. Redact before capture where possible, and verify before
> publication.

---

## 7. Current evidence state

| Evidence ID | PoC | Artifact attached |
| --- | --- | --- |
| `NW-B083-M1-E03` | F01 — non-existent username | ❌ |
| `NW-B083-M1-E04` | F01 — existing username | ❌ |
| `NW-B083-M1-E05` | F02 — injection confirmation | ❌ |
| `NW-B083-M1-E06` | F02 — bypass result | ❌ |
| `NW-B083-M1-E07` | F03 — report 1 download | ❌ |
| `NW-B083-M1-E08` | F03 — reports 2 and 3 download | ❌ |

The observations are documented; the artefacts are not yet sanitised and
attached. Procedure: [`../../evidence/README.md`](../../evidence/README.md#5-closing-the-evidence-gap).

> **Reminder:** the sanitised artefacts for F01 and F02 will contain the exact
> request and response bodies. The password field in every captured login request
> **must** be redacted — those are test values in this engagement, but a captured
> credential teaches the wrong habit and could be a real one.
