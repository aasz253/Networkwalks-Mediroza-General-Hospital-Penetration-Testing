# M2 — Results

**Milestone:** Data Extraction / File Security · **Status:** ✅ Assessed
**Finding:** `NW-B083-M2-F01` — 🔴 High

---

## 1. Result summary

| File | Encryption | Key recovered | Method | Dictionary position | Effective protection | Content read |
| --- | --- | --- | --- | --- | --- | --- |
| `LAB-PDF-01` | ✅ Present | ✅ Yes | Built-in top-100 | Within the first 100 candidates | **None** | ❌ No |
| `LAB-PDF-02` | ✅ Present | ✅ Yes | Built-in top-100 | Within the first 100 candidates | **None** | ❌ No |
| `LAB-PDF-03` | ✅ Present | ✅ Yes | **JTR list** after exhaustion | Beyond top-100, within the JTR list | **Negligible** | ❌ No |

**3 of 3 keys recovered. 0 of 3 files effectively protected.**

---

## 2. Per-file results

### 2.1 `LAB-PDF-01`

| Attribute | Value |
| --- | --- |
| Encryption | Password-based, user password required |
| Key extraction | `$pdf$…` identifier obtained |
| Recovery attempt 1 — built-in top-100 | ✅ **Recovered** |
| Recovery attempt 2 — JTR list | Not required |
| Password length class | 6 characters |
| Character classes present | Digits only |
| Dictionary membership | Within the 100 most common passwords |
| Key published here | 🔒 Withheld |
| Verdict | **No effective protection.** Recovered in seconds from the first 100 candidates |

Evidence: `NW-B083-M2-E02`

### 2.2 `LAB-PDF-02`

| Attribute | Value |
| --- | --- |
| Encryption | Password-based, user password required |
| Key extraction | `$pdf$…` identifier obtained |
| Recovery attempt 1 — built-in top-100 | ✅ **Recovered** |
| Recovery attempt 2 — JTR list | Not required |
| Password length class | 8 characters |
| Character classes present | Lowercase alphabetic only |
| Dictionary membership | A common English word within the top-100 list |
| Key published here | 🔒 Withheld |
| Verdict | **No effective protection.** A longer key than `LAB-PDF-01` and no more resistant, because length without unpredictability is not strength |

Evidence: `NW-B083-M2-E03`

### 2.3 `LAB-PDF-03`

| Attribute | Value |
| --- | --- |
| Encryption | Password-based, user password required |
| Key extraction | `$pdf$…` identifier obtained |
| Recovery attempt 1 — built-in top-100 | ❌ `Exhausted wordlist. No match. ACCESS DENIED.` |
| Recovery attempt 2 — instructor-supplied JTR list | ✅ **Recovered** |
| Password length class | 6 characters |
| Character classes present | Symbols only |
| Dictionary membership | Beyond the top-100; within the JTR list |
| Key published here | 🔒 Withheld |
| Additional action | Decrypted with `qpdf` to a temporary copy for metadata analysis; copy discarded |
| Verdict | **Negligible protection.** Appeared strong relative to its siblings; fell to a modestly larger dictionary |

Evidence: `NW-B083-M2-E04`, `NW-B083-M2-E05`

---

## 3. Password strength assessment (values withheld)

> 🔒 **Why the values are withheld.** These are credentials. Publishing a
> recovered password in a public repository establishes a norm that is
> indefensible on a real engagement, and the finding is fully substantiated
> without it. The values remain available to the client through the engagement's
> own disclosure process.
>
> See [`../../docs/ethical-considerations.md`](../../docs/ethical-considerations.md) §3.1.

### 3.1 Strength properties

| Property | `LAB-PDF-01` | `LAB-PDF-02` | `LAB-PDF-03` |
| --- | --- | --- | --- |
| Length class | 6 | 8 | 6 |
| Lowercase | ❌ | ✅ | ❌ |
| Uppercase | ❌ | ❌ | ❌ |
| Digits | ✅ | ❌ | ❌ |
| Symbols | ❌ | ❌ | ✅ |
| Character classes | 1 of 4 | 1 of 4 | 1 of 4 |
| Dictionary word | ✅ Yes | ✅ Yes | ✅ Yes |
| Recovered by top-100 | ✅ | ✅ | ❌ |
| Recovered by JTR list | ✅ | ✅ | ✅ |

### 3.2 Analysis

Every key uses exactly **one** character class. None mixes classes. Every key is a
dictionary entry. Combined with short length, all three sit inside the region of
the keyspace that dictionary attack covers first.

The apparent ordering — `LAB-PDF-02` (8 chars) stronger than `LAB-PDF-03`
(symbols) stronger than `LAB-PDF-01` (digits) — did not survive testing. All three
fell.

### 3.3 The instructive case: `LAB-PDF-03`

| Assumption | Outcome |
| --- | --- |
| "It needs symbols, so it must be strong" | It fell to a moderately larger dictionary |
| "Six symbols is high entropy" | It is six symbols, and it was in someone's wordlist |
| "It resisted the first attack, so the control works" | It resisted *one list*. The control's strength is a function of the attacker's wordlist, not of the key. |

**Lesson.** Character-class diversity and length raise cost per guess. Neither
addresses *predictability*. A password that a person chose because it "looks
complex" is usually derived from a pattern a wordlist already contains — which is
exactly what happened here.

### 3.4 On entropy claims

No entropy figure is quoted for any key. Quoting one would imply a computation
that was not performed and a randomness model that a human-chosen password does
not satisfy. The measured property — *recovered from a dictionary* — is both
sufficient for the finding and honestly obtained.

---

## 4. Verification approach

A recovery claim is only as good as its verification. Each key was verified, and
each verification is stated with its limitation.

| # | Verification step | Method | Result | What it proves | What it does not prove |
| --- | --- | --- | --- | --- | --- |
| V-1 | Key extracts from the file | Hash calculator returned a well-formed `$pdf$` identifier | ✅ | The identifier is valid and derived from this file | Nothing about key strength |
| V-2 | Candidate accepted by the cracker | Cracker reported a match | ✅ | The candidate is consistent with the file's stored material | That it is the *original* password — see V-3 |
| V-3 | Key actually opens the document | Opened each file with the recovered key | ✅ | The key functions as a document password | That no other key would also work |
| V-4 | Result reproduced | Recovery re-run from the extracted identifier | ✅ | The result is repeatable, not a one-off | Anything about files not assessed |
| V-5 | Negative control | Built-in list exhausted against `LAB-PDF-03` | ✅ Failed as expected | The tool correctly reports failure — the escalation was real, not a false negative | That the JTR list is "the right size" for any threshold |

> **V-5 deserves emphasis.** A tool that always reports success would make every
> other step worthless. Observing a genuine failure on `LAB-PDF-03` demonstrates
> that the successes on files 1 and 2 were meaningful. **A negative control is
> what converts a tool result into evidence.**

---

## 5. Results matrix

| Test case | `LAB-PDF-01` | `LAB-PDF-02` | `LAB-PDF-03` |
| --- | :---: | :---: | :---: |
| File requires a password to open | Pass | Pass | Pass |
| Key identifier extracted | Pass | Pass | Pass |
| Protected against a top-100 dictionary | **Fail** | **Fail** | Pass |
| Protected against a larger dictionary | **Fail** | **Fail** | **Fail** |
| Metadata stripped or safe | Not assessed | Not assessed | **Fail** — see [F05](../../findings/verified-findings/NW-B083-M3-F01-sensitive-pdf-metadata.md) |
| Integrity signature present | **Fail** | **Fail** | **Fail** |
| Served only through an authorising endpoint | **Fail** — see [F03](../../findings/verified-findings/NW-B083-M1-F03-document-access-control.md) | **Fail** | **Fail** |
| Content read during assessment | ✅ No | ✅ No | ✅ No |

---

## 6. Security implications

| # | Implication |
| --- | --- |
| 1 | **Encryption was present on every file and effective on none.** The control existed, appeared operational, and delivered nothing. |
| 2 | **The attack is offline, so application controls are irrelevant.** Rate limiting, lockout and MFA protect the login; they do nothing once a file is in an attacker's hands. |
| 3 | **Document security was effectively single-layered.** With the login bypassable (F02), the document password was the only remaining barrier — and it fell. |
| 4 | **Protection also hid evidence.** Encryption concealed the metadata that produced M3's Critical findings. Treating protection as information-hiding is a misreading of what it does. |
| 5 | **The pattern suggests a process gap, not three bad passwords.** Three of three weak points to key generation and management, not chance. |
| 6 | **Human-chosen passwords were predictable across all three.** Single character class and dictionary membership in every case. |

---

## 7. Remediation and retest

| ID | Recommendation | Priority | Retest criterion |
| --- | --- | --- | --- |
| R-7 | Generate document passwords with a CSPRNG at full printable-ASCII length | **P0** | No key recovered by JTR list **plus** a rule-based mutation pass |
| R-8 | Store keys in a secrets manager; transmit out of band | P1 | Key absent from URLs, filenames, mail bodies and chat |
| R-9 | Enforce authorisation server-side; treat the document password as secondary | **P0** | Unauthenticated document request returns 401/403 |
| R-10 | Move documents outside the web root | **P0** | Direct document path returns 404 |
| R-11 | Forbid key reuse across documents | P1 | No reuse found on spot check |
| R-13 | Alert on bulk document downloads | P1 | Full-set download raises an alert |

### 7.1 Retest reporting rule

State results as **what was attempted and what happened**:

> ✅ Correct: *"No key recovered using the JTR list or a rule-based mutation pass."*
> ❌ Incorrect: *"The passwords are now strong."*

Unrecovered is not the same as uncrackable, and a retest that implies otherwise
misleads the reader about residual risk.

---

## 8. Evidence

| Evidence ID | Description | Sensitivity | Artifact |
| --- | --- | --- | --- |
| `NW-B083-M2-E01` | `$pdf$` key identifiers extracted | 🔴 Confidential | ❌ |
| `NW-B083-M2-E02` | `LAB-PDF-01` key recovery | 🔴 Confidential | ❌ |
| `NW-B083-M2-E03` | `LAB-PDF-02` key recovery | 🔴 Confidential | ❌ |
| `NW-B083-M2-E04` | `LAB-PDF-03` exhaustion then recovery | 🔴 Confidential | ❌ |
| `NW-B083-M2-E05` | `qpdf` decryption of `LAB-PDF-03` | 🔴 Confidential | ❌ |
| `NW-B083-M2-E06` | Structural and metadata summary | 🟠 Internal | ❌ |

Registration: [`../../evidence/evidence-register.csv`](../../evidence/evidence-register.csv) ·
Redaction: [`evidence/README.md`](./evidence/README.md) §4
