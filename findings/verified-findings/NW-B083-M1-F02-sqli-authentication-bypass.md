# NW-B083-M1-F02 — SQL injection in the login form enabling authentication bypass

| Field | Value |
| --- | --- |
| **Finding ID** | `NW-B083-M1-F02` |
| **Milestone** | M1 — Initial Access |
| **Affected component** | `https://medirozahospital.com/patient/login.php` |
| **Severity** | 🔴 **Critical** |
| **Rating status** | Confirmed |
| **Verification status** | Documented |
| **Confidence** | High |
| **OWASP category** | A03 — Injection |
| **CWE** | CWE-89 — Improper Neutralization of Special Elements used in an SQL Command |
| **Evidence IDs** | `NW-B083-M1-E05`, `NW-B083-M1-E06` |
| **Status** | Open — **highest remediation priority** |

---

## 1. Description

The `username` field is incorporated into a SQL query by string concatenation without
parameterisation. A submitted single quote causes a MySQL syntax error, and a SQL
comment marker removes the password comparison from the executed statement, allowing
authentication as `admin` without any credential.

---

## 2. Affected component

| Field | Value |
| --- | --- |
| Location | `/patient/login.php` |
| Type | Login form |
| Authentication to reach it | None |
| Parameters | `username` (confirmed injectable), `password` (same query — **not separately tested**) |
| Data at risk | Everything reachable by the bypassed account, including patient documents |

---

## 3. Preconditions

| # | Precondition | Present in this engagement? |
| --- | --- | --- |
| 1 | Network access to the authorized host | ✅ Yes |
| 2 | Knowledge of a valid username | ✅ Obtained via `NW-B083-M1-F01`, not guessed |
| 3 | Any credential | ❌ **Not required** |

---

## 4. Technical evidence

### 4.1 Observation

**Stage 1 — injection confirmed:**

| Input | Response |
| --- | --- |
| `admin'` | `Warning: mysqli_query(): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1` |

**Stage 2 — authentication bypassed:**

| Input | Result |
| --- | --- |
| `admin' --` with any password | **Logged in.** Portal loaded with three reports listed |

| Evidence ID | Observation | Artifact |
| --- | --- | --- |
| `NW-B083-M1-E05` | `mysqli_query()` syntax error from a single quote | ❌ Not attached |
| `NW-B083-M1-E06` | Portal rendered after the bypass | ❌ Not attached |

### 4.2 Expected vs. observed

| | Expected (secure) | Observed |
| --- | --- | --- |
| **Invalid input** | `Invalid credentials.` | Full MySQL diagnostic including driver, engine, error position and offending fragment |
| **Valid username + wrong password** | Login refused | **Login granted.** Password predicate removed from the query |

### 4.3 Mechanism

Intended query shape:

```
... WHERE username = '<input>' AND password = '<hash-or-input>'
                    ^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     both required   ^^^^^^^^^^^^^^^^^^^^^^^^^^^ neutralised by --
```

| Fragment | Effect |
| --- | --- |
| `admin` | Literal match against a valid account |
| `'` | Closes the string literal opened by the query's own quoting |
| `--` | Comments out the rest of the statement, including the password comparison |

Effective logic changes from `A AND B` to `A`. **No password was guessed, cracked
or recovered — the check was deleted from the executed statement.**

### 4.4 Secondary weakness — verbose error disclosure

Database diagnostics are returned verbatim to an unauthenticated client.

| Benefit to an attacker | Provided by the error text |
| --- | --- |
| Fingerprint the stack | `mysqli_query()`, `MySQL server version` |
| Confirm injection without probing | Syntax error and position marker `near ''' at line 1` |
| Infer query structure | Position of the unterminated literal |

This is dangerous **because** the endpoint is injectable. On a properly
parameterised endpoint the same error would be harmless. Both must be fixed.

**Probable root cause:**

| Probable cause | Confidence | To confirm |
| --- | --- | --- |
| Query built by string concatenation and passed to `mysqli_query()` | High | Review the login handler for query construction |
| Verbose error reporting enabled in production | High | Review PHP and application error configuration |
| A shared query helper may exist elsewhere and be unused here | Medium | Search the codebase for prepared-statement helpers |

---

## 5. Reproduction summary

> Authorized training environment only. Two requests. No data extracted or modified.

### 5a — Injection confirmation

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | Submit `admin'` as the username | MySQL syntax error returned to the client |

### 5b — Authentication bypass

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | Submit `admin' --` with any password | Authenticated session established; portal loaded |

| Bound | Limit |
| --- | --- |
| Requests required | 2 |
| Authentication required | None |
| Side effects | A session was created. **Nothing was modified.** No administrative function invoked. Portal not enumerated beyond what was displayed. |

**Explicitly not performed:**

| Action | Reason |
| --- | --- |
| `UNION`-based extraction from other tables | Not needed to substantiate authentication bypass; extraction out of scope |
| `GROUP_CONCAT` schema or data dumping | Same |
| Stacked queries | Same |
| Data modification or deletion | Destructive testing prohibited |
| Creating a privileged account | Data modification prohibited |
| Enumerating other accounts | `admin` was sufficient to substantiate impact |
| Establishing persistence | Prohibited |

> **Untested and not ruled out:** whether the injection is reachable from other
> parameters, whether it permits modification, and whether other accounts are
> accessible by the same route. These are recorded as hypotheses H-4 through H-7
> in the [M1 analysis](../../milestones/M1-initial-access/vulnerability-analysis.md#4-hypothesis-register),
> not as absent weaknesses.

---

## 6. Security impact

| Dimension | Assessment |
| --- | --- |
| Confidentiality | **Severe.** Full read access wherever the bypassed account can read — demonstrated against the patient document store |
| Integrity | **Probable, not demonstrated.** The same primitive normally permits modification. No write path was exercised. Recorded as *not tested*, **not** *not possible* |
| Availability | Not demonstrated |
| Data sensitivity | 🔴 Clinical — patient report documents |
| Business consequence | Complete defeat of the authentication control on a healthcare application |
| Detection likelihood | **Low.** A single unauthenticated request produces a verbose database error; detection would depend entirely on a downstream alert existing |

### 6.1 Cross-finding effect

**This is the root defect of the engagement.**

| Downstream finding | Relationship |
| --- | --- |
| `NW-B083-M1-F01` | Enabled this finding by identifying a valid account |
| `NW-B083-M1-F03` | Direct consequence — documents reachable via this bypass |
| `NW-B083-M2-F01` | Indirect — the documents obtained had weak keys |
| `NW-B083-M3-F01` | Indirect — one retrieved document carried the metadata that started M3 |

---

## 7. Severity

| Attribute | Value |
| --- | --- |
| Band | 🔴 **Critical** |
| Rationale | Unauthenticated, remote, low-complexity defeat of authentication on a healthcare application holding patient documents. Every metric is at its most favourable to an attacker. Rated above a standard injection because the endpoint is the authentication control itself, and the impact was demonstrated rather than inferred. |
| Confidence | High — bypass executed and its effect directly observed |
| Rating status | **Confirmed.** Every CVSS metric input is evidenced. |

---

## 8. CVSS v4.0

**Vector:** `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:N/SA:N`

**Base score:** `PENDING — compute with the FIRST CVSS v4.0 calculator`
(derivation in [`../../risk/cvss-assessment.md`](../../risk/cvss-assessment.md))

| Metric | Value | Justification |
| --- | --- | --- |
| AV | `N` | One HTTP request over the network |
| AC | `L` | Deterministic; no race, no special condition. `admin' --` succeeded on the first attempt |
| AT | `N` | No deployment prerequisite beyond a reachable login form |
| PR | `N` | No account required |
| UI | `N` | No human must act |
| VC | `H` | Read access to protected patient documents was **demonstrated** |
| VI | `H` | A query-composition primitive on an authentication query implies write capability in the same store. *Not demonstrated* — see note below |
| VA | `L` | No availability effect observed. `L` rather than `N` because write access to an authentication store raises the possibility of lockout or account destruction, untested |
| SC | `H` | The authentication component's compromise extends to the entire application and its document store — a subsequent system beyond the query itself |
| SI | `N` | No integrity effect on a subsequent system asserted |
| SA | `N` | No availability effect on a subsequent system asserted |

> **Two metrics carry uncertainty and both are stated rather than hidden.**
>
> - **VI = `H`** is inferred from the weakness class, not demonstrated. If a reviewer
>   requires demonstrated-only evidence, VI should be `N` — which lowers the score.
>   The `H` rating reflects the standard treatment of an authentication-query
>   injection, where modification is inherent to the primitive. This is a judgment
>   call and is flagged as such.
> - **AV is unambiguous** — nothing about the attack needed physical or adjacent
>   network position.
>
> This is the one finding in the engagement where a metric rests on inference
> rather than observation. A retest that safely demonstrates a modification
> capability would resolve it; a retest that does not should reduce VI to `N`.

---

## 9. Remediation

### 9.1 Primary fix — remove the primitive

```php
// VULNERABLE — input concatenated into the statement
$sql = "SELECT id, role FROM users
        WHERE username = '" . $username . "' AND password = '" . $hash . "'";
$result = mysqli_query($conn, $sql);

// FIXED — parameterised; the driver sends data and SQL separately
$stmt = mysqli_prepare($conn,
    "SELECT id, role FROM users WHERE username = ? AND password_hash = ?");
mysqli_stmt_bind_param($stmt, "ss", $username, $hash);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);
```

### 9.2 Mandatory accompanying actions

| # | Action | Priority |
| --- | --- | --- |
| 1 | Parameterise **every** query at every call site. One vulnerable path does not prove the rest are safe — audit the whole codebase | **P0** |
| 2 | Verify passwords with `password_verify()` against a `password_hash()` hash, never by SQL comparison | **P0** |
| 3 | Disable verbose database errors in production: `display_errors=Off`, `log_errors=On`, details to the log only | **P0** |
| 4 | Allow-list any value used to build dynamic SQL (table names, column names, sort direction) | **P0** |
| 5 | Add SAST to CI to detect concatenation into `mysqli_query()`, `->query()` and equivalent | P1 |
| 6 | Review the full schema for other injectable entry points — search, filters, report parameters, admin tooling | P1 |
| 7 | Add rate limiting and alerting on repeated database-error responses | P1 |
| 8 | Adopt a query builder or ORM as the default path so raw concatenation is hard to write | P2 |

### 9.3 Remediation priority

**P0 — immediate.** This is the root defect of the engagement. Every other finding
is downstream of it.

---

## 10. Retest criteria

| # | Criterion | Method | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | Injection removed from `username` | Repeat the single-quote test | No database error; generic auth failure |
| 2 | Injection removed from `password` | Repeat against the password field | No database error |
| 3 | No injection on any parameter | Test all identified entry points | No database error anywhere |
| 4 | Verbose errors disabled | Trigger any application error | No stack trace, driver name or SQL fragment returned |
| 5 | Passwords verified in application code | Code review | `password_verify()` used; no SQL password comparison |
| 6 | No bypass remains | Re-attempt the comment-truncation payload | Login refused |
| 7 | SAST in place | CI run | Concatenation into a query API fails the build |
| 8 | Monitoring active | Repeated failed logins | Alert raised and triaged |

---

## 11. Status

| Field | Value |
| --- | --- |
| Status | **Open — P0** |
| Verification status | **Documented** |
| Rating status | **Confirmed**, with VI inferred rather than demonstrated (§8) |
| Evidence artifacts attached | 0 of 2 |
| Outstanding to close | Capture and sanitise `E05`/`E06`; redact submitted password values; resolve the VI metric by safe demonstration or downgrade it to `N` |

---

## 12. Confidentiality declaration

- [x] No credential present — no password was recovered; the bypass required none
- [x] No patient content reproduced
- [x] No personal data value reproduced
- [x] Synthetic reproduction labelled as such
- [x] Root cause stated as probable — no source access
- [x] No exploit automation provided in this repository
- [x] No client approval or sign-off claimed
