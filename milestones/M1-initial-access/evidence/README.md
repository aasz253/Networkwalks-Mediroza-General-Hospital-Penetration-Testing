# M1 — Evidence Index

**Milestone:** Initial Access · **Registered observations:** 8 · **Artifacts attached:** 0

Policy and procedure: [`../../evidence/README.md`](../../../evidence/README.md) ·
Master register: [`../../evidence/evidence-register.csv`](../../../evidence/evidence-register.csv)

---

## 1. Evidence register — M1

| Evidence ID | Description | Related finding | Sensitivity | Artifact |
| --- | --- | --- | --- | --- |
| `NW-B083-M1-E01` | `robots.txt` output listing `/patient/`, `/staff/`, `/old/` | F06, F07 (correlation) | Internal | ❌ |
| `NW-B083-M1-E02` | Login page served at `/patient/login.php` | F01, F02 | Internal | ❌ |
| `NW-B083-M1-E03` | Login response for a non-existent username | F01 | Internal | ❌ |
| `NW-B083-M1-E04` | Login response for an existing username | F01 | Internal | ❌ |
| `NW-B083-M1-E05` | `mysqli_query()` SQL syntax error response | F02 | Internal | ❌ |
| `NW-B083-M1-E06` | Portal rendered after the authentication bypass | F02, F03 | Internal | ❌ |
| `NW-B083-M1-E07` | Download of `LAB-PDF-01` | F03, F04 | **Confidential** | ❌ |
| `NW-B083-M1-E08` | Download of `LAB-PDF-02` and `LAB-PDF-03` | F03, F04 | **Confidential** | ❌ |

---

## 2. Expected artifacts

| Evidence ID | Artifact type | Filename convention | Redaction required |
| --- | --- | --- | --- |
| `NW-B083-M1-E01` | Terminal capture | `NW-B083-M1-E01_robots-txt-disclosure.txt` | None expected |
| `NW-B083-M1-E02` | Screenshot | `NW-B083-M1-E02_login-page.png` | Redact any visible session material |
| `NW-B083-M1-E03` | Request/response capture | `NW-B083-M1-E03_login-response-nonexistent-user.txt` | **Redact password field** |
| `NW-B083-M1-E04` | Request/response capture | `NW-B083-M1-E04_login-response-existing-user.txt` | **Redact password field** |
| `NW-B083-M1-E05` | Request/response capture | `NW-B083-M1-E05_sql-error-single-quote.txt` | **Redact password field** |
| `NW-B083-M1-E06` | Screenshot | `NW-B083-M1-E06_portal-after-bypass.png` | Redact session cookie, account identifiers, document titles |
| `NW-B083-M1-E07` | Screenshot | `NW-B083-M1-E07_report-01-download.png` | Redact any document content in view |
| `NW-B083-M1-E08` | Screenshot | `NW-B083-M1-E08_reports-02-03-download.png` | Redact any document content in view |

Target directory: `evidence/screenshots/M1/`

---

## 3. Image references

Image references are added **only once the corresponding file exists**. Until then
this section deliberately contains placeholders rather than broken links.

```
![Placeholder — NW-B083-M1-E01](../../evidence/screenshots/M1/NW-B083-M1-E01_robots-txt-disclosure.txt)
```

> The line above is a **documented placeholder in fenced code**, not a live image
> reference. It records the intended path without creating a broken link. Convert
> it to a live `![…]()` reference only after the artifact exists, has been
> sanitised, has been manually reviewed, and has a row in the register.

---

## 4. Redaction checklist for M1 artifacts

- [ ] `Cookie`, `Set-Cookie` and `Authorization` headers removed
- [ ] Password field values removed from every captured login request
- [ ] Session identifiers and tokens removed
- [ ] Account identifiers masked (`admin` is a role label — confirm no real account is named)
- [ ] No patient content visible in any document thumbnail or preview
- [ ] Browser URL bar checked for tokens in query strings
- [ ] Devtools panels cropped if visible
- [ ] Terminal history not captured in the same frame
- [ ] SHA-256 recorded **before** redaction; redacted copy hashed separately
- [ ] Manual review completed — automated redaction is a first pass only

---

## 5. Outstanding work

| # | Task | Status |
| --- | --- | --- |
| 1 | Capture the 8 M1 artifacts into the off-repository raw store | ❌ Not done |
| 2 | Sanitise using [`../../scripts/evidence_sanitizer.py`](../../../scripts/README.md) for text captures | ❌ Not done |
| 3 | Manually review and redact per §4 | ❌ Not done |
| 4 | Place reviewed artifacts in `evidence/screenshots/M1/` | ❌ Not done |
| 5 | Update `artifact_present` to `YES` and `redaction_status` in the register | ❌ Not done |
| 6 | Convert §3 placeholders to live image references | ❌ Blocked by 4 |
| 7 | Record SHA-256 for each artifact | ❌ Not done |

Until items 1–5 are complete, M1 findings remain at status **Documented** rather
than **Evidence-attached**. That distinction is maintained in
[`../../findings/README.md`](../../../findings/README.md) and is deliberate.
