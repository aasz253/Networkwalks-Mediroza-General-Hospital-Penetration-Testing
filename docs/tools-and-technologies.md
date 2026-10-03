# Tools and Technologies

**Engagement ID:** `NW-B083` · **Environment:** Networkwalks authorised training target

---

## 1. Verification policy

A tool inventory exists so that testing is reproducible and auditable. That value
is destroyed by listing tools that were not used.

| Status | Meaning |
| --- | --- |
| ✅ **Documented in use** | Appears in the engagement record with the purpose it served |
| ✅ **Verified in this repository** | Can be run here and its behaviour confirmed |
| ⚠️ **Capability required, not exercised** | Needed for the methodology but not used on this target |
| ⛔ **Not used / prohibited** | Explicitly excluded |

---

## 2. Tools documented in use

| # | Tool | Type | Purpose | Milestone |
| --- | --- | --- | --- | --- |
| T-01 | `curl` | CLI | Retrieve `robots.txt` | M1 |
| T-02 | Web browser | Interactive | Manual navigation of `/patient/`, the login form and the portal | M1, M3 |
| T-03 | Networkwalks Hash Calculator (`networkwalks.com/hash-calculator/`) | Web tool (provider-supplied) | Extract the `$pdf$` password hash from an encrypted PDF | M2 |
| T-04 | Networkwalks Password Cracker (`networkwalks.com/password-cracker/`) | Web tool (provider-supplied) | Wordlist-based key recovery against a `$pdf$` hash | M2 |
| T-05 | Built-in top-100 password list | Wordlist | First-pass key recovery for reports 1 and 2 | M2 |
| T-06 | Instructor-supplied JTR wordlist | Wordlist | Escalation for report 3 | M2 |
| T-07 | `qpdf` | CLI | Decrypt report 3 to an unlocked copy (`--password=… --decrypt`) | M2 → M3 |
| T-08 | `exiftool` | CLI | Read PDF metadata: author, comments, producer, dates | M3 |
| T-09 | `wget` | CLI | Download the exposed SQL backup from `/old/` | M3 |
| T-10 | Text editor | Interactive | Inspect `INSERT` statements in the backup | M3 |
| T-11 | AI assistant (conversational) | Analysis aid | Convert dense `INSERT` rows into readable tables | M3 |

> **On T-03 and T-04.** These are provider-supplied web tools for the lab
> environment. This repository documents their use; it contains **no automation**
> that calls them, and no wrapper, script or API integration is provided.

---

## 3. Tooling provided by this repository

Verifiable by running it here. Python 3.8+, standard library only, fully offline.

| Tool | Path | Purpose | Guarantee |
| --- | --- | --- | --- |
| `evidence_sanitizer.py` | [`../scripts/evidence_sanitizer.py`](../scripts/evidence_sanitizer.py) | Produce a sanitized **copy** of text-based evidence; flag likely sensitive patterns by class | Never writes to the input path; never prints matched secret values; manual review still required |
| `repo_checks.py` | [`../scripts/repo_checks.py`](../scripts/repo_checks.py) | Link integrity, CSV structure, evidence-reference existence, secret-pattern detection, CVSS vector lint | Offline; fails closed; reports secret *classes*, not values |
| `git` | — | Version control, history audit | History rewriting requires explicit approval |
| GitHub Actions | [`../.github/workflows/documentation-check.yml`](../.github/workflows/documentation-check.yml) | Runs the documentation gate on push and pull request | No network calls to any target |
| Mermaid | [`../diagrams/`](../diagrams/) | Diagram authoring | High-level only; no sensitive architecture detail |

---

## 4. Capabilities required but not exercised

Needed for a full black-box engagement; the lab route did not reach them. Listed
so the gap is visible rather than implied.

| Capability | Why it would be needed | Representative tooling |
| --- | --- | --- |
| DNS enumeration | Record review, subdomains, mail configuration | `dig`, `host` |
| TLS inspection | Protocol/cipher configuration, certificate chain | `openssl s_client`, `sslyze` |
| HTTP fingerprinting | Server, framework, CMS, WAF identification | Manual header inspection, `whatweb` |
| Intercepting proxy | Systematic header review, request manipulation | Burp Suite Community, OWASP ZAP |
| Crawling | Surface enumeration beyond manual navigation | `wget`, Burp/ZAP spider |
| Content discovery | Directory and file enumeration | `ffuf`, `feroxbuster`, `gobuster` |
| Hashing / integrity | Evidence integrity, file identification | `sha256sum`, `file`, `strings` |
| Screenshot capture | Evidence artefacts | OS/browser capture |

---

## 5. Prohibited — not used, not provided

| Class | Reason | RoE |
| --- | --- | --- |
| Exploitation frameworks | Validation limited to substantiation | ROE-5, ROE-6 |
| Credential attack against site accounts (brute force, spraying, stuffing) | Prohibited activity | ROE-4 |
| Denial-of-service, stress, load tools | Availability risk | ROE-2 |
| Destructive or data-modifying tooling | Data integrity | ROE-3 |
| Automated host scanners | Scope boundary; unnecessary on a known lab target | ROE-1 |
| Bulk database extraction tooling | Data minimisation | ROE-7 |
| Anything that sends traffic to the target from this repository | Repository must never generate target traffic | ROE-10 |

> **Explicitly absent by design:** no exploit script, no login-bypass automation,
> no password-cracking harness, no scanner configuration, no target-specific
> payload file. The techniques are documented in prose; the automation is not
> provided.

---

## 6. Technology observations

**Not performed.** The lab route did not require stack fingerprinting, so no
technology is claimed for the target. Recording this as unknown is the honest
entry — an invented stack identification would be the kind of small fabrication
that discredits a whole report.

| Layer | Observed | Evidence |
| --- | --- | --- |
| Web server | Unknown — PHP/MySQL implied by the `mysqli_query()` error text | `NW-B083-M1-E05` |
| Language / runtime | PHP implied (`login.php`, `mysqli_*` error) | `NW-B083-M1-E02`, `E05` |
| Database | MySQL implied (explicit `MySQL server version` in the error text) | `NW-B083-M1-E05` |
| Framework / CMS | Unknown | — |
| Front-end libraries | Unknown | — |
| CDN / WAF / reverse proxy | Unknown | — |
| TLS configuration | Not assessed | — |
| Security headers | Not assessed | — |
| Backup tooling behind the `.sql` file | Unknown | — |

> These are **inferences from an error string**, labelled as inferences. They are
> sufficient to explain why the injection behaved as it did, and insufficient to
> support version-specific conclusions.

---

## 7. Reproducibility

Reproduce this repository's own automation:

```bash
git clone https://github.com/aasz253/Networkwalks-Mediroza-General-Hospital-Penetration-Testing.git
cd Networkwalks-Mediroza-General-Hospital-Penetration-Testing

python3 --version
python3 scripts/repo_checks.py
python3 scripts/evidence_sanitizer.py --self-test
python3 scripts/evidence_sanitizer.py \
  --input scripts/sample-data/synthetic-sample-log.txt \
  --output-dir /tmp/nw-sanitizer-demo
```

No `pip install`, no credentials, no configuration, no network access.

**Reproducing the target assessment is deliberately not documented as a runbook.**
That would amount to publishing an attack procedure; the authorisation for this
engagement is specific to it and does not transfer to a reader. The *reasoning* is
documented in full — the *execution* is not automated.

---

## 8. Outstanding work

| Item | Required |
| --- | --- |
| §4 capability statuses | Fingerprint the stack in a follow-up engagement, or record permanently as out of scope for this lab route |
| §6 technology table | Same |
| Evidence artefacts | Capture and sanitise; see [`../evidence/README.md`](../evidence/README.md) §5 |
