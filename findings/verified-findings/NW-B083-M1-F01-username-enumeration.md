# NW-B083-M1-F01 — Username enumeration on the login page

| Field | Value |
| --- | --- |
| **Finding ID** | `NW-B083-M1-F01` |
| **Milestone** | M1 — Initial Access |
| **Affected component** | `https://medirozahospital.com/patient/login.php` |
| **Severity** | 🟠 **Medium** |
| **Rating status** | Confirmed |
| **Verification status** | Documented |
| **Confidence** | High |
| **OWASP category** | A07 — Identification and Authentication Failures |
| **CWE** | CWE-204 — Observable Response Discrepancy |
| **Evidence IDs** | `NW-B083-M1-E03`, `NW-B083-M1-E04` |
| **Status** | Open |

---

## 1. Description

The authentication handler returns a different error message depending on which
check failed, disclosing whether a username exists. An unauthenticated party can
determine the existence of any account by observing which of two responses is
returned.

---

## 2. Affected component

| Field | Value |
| --- | --- |
| Location | `/patient/login.php` |
| Type | Login form |
| Authentication to reach it | None |
| Parameters | `username`, `password` |
| Data at risk | The username namespace — which accounts exist |

---

## 3. Preconditions

| # | Precondition | Present in this engagement? |
| --- | --- | --- |
| 1 | Network access to the authorized host | ✅ Yes |
| 2 | No credential, account or prior access | ✅ Yes |

**No credentials were used to establish this finding.**

---

## 4. Technical evidence

### 4.1 Observation

| Input | Response |
| --- | --- |
| `bob` / `test123` | `Username not found` |
| `admin` / `test123` | `Incorrect password` |

| Evidence ID | Observation | Artifact |
| --- | --- | --- |
| `NW-B083-M1-E03` | Response for a non-existent username | ❌ Not attached |
| `NW-B083-M1-E04` | Response for an existing username | ❌ Not attached |

### 4.2 Expected vs. observed

| | `bob` (does not exist) | `admin` (exists) |
| --- | --- | --- |
| **Expected** | `Invalid credentials.` | `Invalid credentials.` |
| **Observed** | `Username not found` | `Incorrect password` |

### 4.3 Mechanism

The handler branches on the account-lookup result, and each branch returns its own
message.

```
lookup(username)
   ├── not found ──────► "Username not found"      ← distinguishable
   └── found
        └── bad password ─► "Incorrect password"    ← distinguishable
```

**Probable root cause:** convenience in the error path rather than an
authentication-design decision.

| Probable cause | Confidence | To confirm |
| --- | --- | --- |
| Separate not-found and wrong-password branches with distinct user-facing messages | High | Review the authentication controller |

---

## 5. Reproduction summary

> Authorized training environment only. Two unauthenticated requests.

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | Submit the login form with a non-existent username | `Username not found` |
| 2 | Submit with a known or suspected username | `Incorrect password` |

| Bound | Limit |
| --- | --- |
| Requests required | 2 |
| Authentication required | None |
| Side effects | **None.** No account state changed. |

**Explicitly not performed:**

| Action | Reason |
| --- | --- |
| Automated username enumeration at scale | Two requests were sufficient to establish the differential; bulk enumeration was out of scope |
| Password guessing against any account | Prohibited |
| Enumerating the full account list | Not required to substantiate the finding |

---

## 6. Security impact

| Dimension | Assessment |
| --- | --- |
| Confidentiality | The username namespace is disclosed to unauthenticated parties |
| Integrity | No effect |
| Availability | No effect |
| Data sensitivity | Internal — account identifiers |
| Business consequence | Enables targeted attacks against known-valid accounts, and turns a blind injection into a targeted one |
| Detection likelihood | **High.** Enumeration is inherently noisy, but no rate limiting or monitoring was observed |

### 6.1 Cross-finding effect

**This finding directly enabled `NW-B083-M1-F02`.** Knowing `admin` was a valid
account meant the injection payload did not have to guess a username:

| With enumeration | Without enumeration |
| --- | --- |
| One targeted payload against `admin` | Enumeration or guessing required first |

The same two messages also exposed the PHP/MySQL stack once the injection error
appeared, because the two failure modes looked nothing alike.

---

## 7. Severity

| Attribute | Value |
| --- | --- |
| Band | 🟠 **Medium** |
| Rationale | Directly usable information that materially assists other attacks, but no direct data compromise. Rated below the injection it enabled, because enumeration alone discloses identifiers rather than access. Rated above a cosmetic information leak because it is automatable, unrate-limited, and was decisive in practice. |
| Confidence | High — directly observed twice, deterministically |
| Rating status | **Confirmed.** Every CVSS metric input is evidenced. |

---

## 8. CVSS v4.0

**Vector:** `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N`

**Base score:** `PENDING — compute with the FIRST CVSS v4.0 calculator`
(vector is validated by `scripts/repo_checks.py`; derivation in
[`../../risk/cvss-assessment.md`](../../risk/cvss-assessment.md))

| Metric | Value | Justification |
| --- | --- | --- |
| AV | `N` | Exploitable over the network with an HTTP request |
| AC | `L` | No conditions beyond attacker control; deterministic |
| AT | `N` | No specific deployment prerequisite |
| PR | `N` | No account or access required |
| UI | `N` | No human must act |
| VC | `L` | Leaks account existence — a partial, low-volume confidentiality loss |
| VI | `N` | Nothing is modified |
| VA | `N` | No availability effect |
| SC | `N` | No subsequent system affected |
| SI | `N` | — |
| SA | `N` | — |

> VC is `L` rather than `H`: the leak is scoped to whether specific accounts exist,
> not to their contents. Attributing `H` here would inflate the score.

---

## 9. Remediation

### 9.1 Primary fix

Return **one** message for every failed authentication — identical wording,
formatting and behaviour regardless of cause:

```php
// VULNERABLE — distinct messages per failure mode
if (!$user) {
    $error = "Username not found";
} elseif (!password_verify($_POST['password'], $user['password_hash'])) {
    $error = "Incorrect password";
}

// FIXED — one message, one path
$user = find_user_by_username($_POST['username']);
$ok = $user && password_verify($_POST['password'], $user['password_hash']);

if (!$ok) {
    $error = "Invalid credentials.";   // identical in every failure case
}
```

| Must be | Must not be |
| --- | --- |
| One message for every failure | `Username not found` |
| Same status code and same page | `Incorrect password` |
| Comparable response timing | A redirect only on one path |

### 9.2 Additional hardening

| # | Measure | Addresses |
| --- | --- | --- |
| 1 | Normalise response timing between code paths | Timing side channel |
| 2 | Rate-limit and throttle repeated failures per source and per account | Enumeration at scale |
| 3 | Alert on enumeration patterns — many failures, many distinct usernames | Detection |
| 4 | Consider a step-up challenge instead of a different error for existing users | Removes the signal entirely |
| 5 | Ensure registration and password-reset flows do not leak existence either | Same class, adjacent surfaces |

---

## 10. Retest criteria

| # | Criterion | Method | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | Identical failure response | Submit an existing and a non-existent username | Byte-identical response body and status | ⬜ Not tested |
| 2 | Comparable timing | Measure response time across both paths | No statistically significant difference | ⬜ Not tested |
| 3 | No existence leak via registration or reset | Submit a known and an unknown identifier to each flow | Indistinguishable responses | ⬜ Not tested |
| 4 | Rate limiting active | Repeated failed attempts | Throttling engages and an alert is raised | ⬜ Not tested |

---

## 11. Status

| Field | Value |
| --- | --- |
| Status | **Open** |
| Verification status | **Documented** |
| Rating status | **Confirmed** |
| Evidence artifacts attached | 0 of 2 |
| Outstanding to close | Capture and sanitise `E03`/`E04`; redaction must remove the submitted password values |

---

## 12. Confidentiality declaration

- [x] No credential present — submitted test values would be redacted from any artifact
- [x] No patient content reproduced
- [x] No personal data value reproduced
- [x] No client approval or sign-off claimed
