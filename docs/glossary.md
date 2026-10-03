# Glossary and Conventions

Terms used in this repository, plus the naming and ID conventions that make
findings and evidence traceable.

---

## 1. Identification conventions

| Convention | Format | Example |
| --- | --- | --- |
| Engagement ID | `NW-B<batch>` | `NW-B083` |
| Finding ID | `NW-B<batch>-<MS>-F<nn>` | `NW-B083-M1-F02` |
| Evidence ID | `NW-B<batch>-<MS>-E<nn>` | `NW-B083-M1-E05` |
| Remediation action ID | `R-<n>` | `R-2` |
| Risk register row | Finding ID | `NW-B083-M3-F03` |
| Test file label | `LAB-PDF-<nn>` | `LAB-PDF-03` |
| Cross-reference | `NW-B083-<MS>-<other>` | `NW-B083-M1-E01` cited from M3 |

**Milestone codes:** `M1` Initial Access · `M2` Data Extraction / Document
Security · `M3` Deep Reconnaissance / Critical Data Exposure · `M4` Final Report

**Status vocabulary — used consistently, never loosely:**

| Term | Meaning |
| --- | --- |
| **Documented** | The engagement record contains the observed output. No sanitised artefact attached yet. |
| **Evidence-attached** | A sanitised artefact exists in `evidence/` and is referenced from the finding. |
| **Verified** | Evidence-attached **and** independently reviewed against the finding claim. |
| **Provisional** | Rating is issued but a stated input is missing or uncertain. |
| **Observation** | Recorded fact with no weakness implied. |
| **Hypothesis** | Plausible weakness, untested. Never presented as a finding. |
| **Withdrawn** | Tested and refuted. Reason recorded. ID never reused. |

---

## 2. Attack and vulnerability terms

| Term | Definition |
| --- | --- |
| **Attack surface** | The set of points where an untrusted party can supply input. Here: `/patient/login.php`, `/patient/reports/`, `/old/`, `/robots.txt` |
| **Authentication bypass** | Gaining an authenticated session without valid credentials — by defeating the check rather than satisfying it |
| **Authorisation** | Determining what an *already authenticated* party may do or see |
| **Broken access control** | Server-side enforcement failure allowing access beyond the intended permission |
| **Cleartext** | Data stored or transmitted without encryption |
| **Comment truncation** | Using a SQL comment marker (`--`, `#`, `/*`) to neutralise the remainder of a query |
| **CWE-204** | Observable Response Discrepancy — the weakness class behind username enumeration |
| **CWE-89** | Improper Neutralisation of Special Elements in SQL Command — SQL injection |
| **CWE-548** | Exposure of Information Through Directory Listing |
| **CWE-538** | Insertion of Sensitive Information into Externally-Accessible File or Directory |
| **Directory listing / autoindex** | Web server behaviour that renders a file index when no index page exists |
| **Error-based injection** | Confirming injection by provoking a database error that reveals query structure |
| **Exposure** | A condition where data is reachable by a party that should not have it |
| **Hash cracking** | Recovering a secret by comparing candidate inputs against a stored hash |
| **`$pdf$` hash** | The identifier format used by password crackers for PDF encryption keys |
| **IDOR** | Insecure Direct Object Reference — accessing an object by identifier without an authorisation check |
| **Information disclosure** | Revealing information beyond what the recipient requires |
| **Metadata** | Data *about* a file — author, producer, creation time, comments — carried inside it |
| **OWASP Top 10** | The ten broad web-application risk categories used to categorise findings here |
| **OWASP WSTG** | The test-case catalogue whose structure the procedures follow |
| **OWASP ASVS** | Verification requirements used to frame remediation |
| **PTES** | The penetration testing lifecycle model |
| **Payload** | Input crafted to trigger a specific behaviour |
| **Personal Identifiable Information (PII)** | Data identifying a natural person |
| **Portal** | The authenticated area of the application reached after login |
| **Robots exclusion protocol** | `/robots.txt` directives intended to discourage indexing of paths |
| **SQL backup** | A `.sql` file containing DDL and `INSERT` statements able to recreate a database |
| **Subsequent system** | In CVSS terms, a system beyond the vulnerable component's security authority |
| **Vulnerable system** | In CVSS terms, the component whose security authority is directly affected |
| **Wordlist** | A file of candidate secrets used in dictionary attacks |
| **Zero-day** | A weakness with no available patch. Not applicable to any finding here |

---

## 3. Document security terms

| Term | Definition |
| --- | --- |
| **Encryption (PDF)** | Password-based protection preventing casual opening of a document |
| **Permissions password** | An owner password restricting editing, printing or extraction — not the same as the user password required to open |
| **Character-class diversity** | Mixing uppercase, lowercase, digits and symbols. Raises cost per guess; does **not** prevent dictionary attack |
| **Decryption** | Producing a readable copy from an encrypted document, given the key |
| **Key strength** | The practical resistance of a secret to recovery — the meaningful measure, not whether protection is present |
| **Metadata stripping** | Removing metadata fields before distributing a file |
| **Metadata leak** | Sensitive information carried in metadata to a party that should not receive it |

---

## 4. Risk terms

| Term | Definition |
| --- | --- |
| **Attack Vector (AV)** | How an attacker reaches the weakness: Network, Adjacent, Local, Physical |
| **Attack Complexity (AC)** | Conditions beyond the attacker's control that must hold |
| **Attack Requirements (AT)** | A CVSS v4.0 metric replacing v3.x's scope-dependent privileges-at-another-scope nuance: None or Present |
| **Privileges Required (PR)** | Level of access the attacker must already hold |
| **User Interaction (UI)** | Whether a human must act for the attack to succeed: None, Passive, Active |
| **Vulnerable System (VC/VI/VA)** | Impact on confidentiality / integrity / availability of the vulnerable component |
| **Subsequent System (SC/SI/SA)** | Impact on a system beyond the vulnerable component's authority |
| **CVSS v4.0** | Common Vulnerability Scoring System, version 4.0 — base, threat and environmental metric groups |
| **MacroVector** | The intermediate representation v4.0 uses to produce a base score |
| **Confidence** | How sure the assessor is that the finding is real, independent of severity |
| **Provisional rating** | A rating issued with a stated missing or uncertain input |
| **Retest criterion** | The objective check that closes a finding after remediation |

---

## 5. Evidence and documentation terms

| Term | Definition |
| --- | --- |
| **Artifact** | A concrete file: screenshot, log, capture |
| **Sanitisation** | Producing a publishable derivative with sensitive content removed |
| **Redaction** | The removal itself; irreversible removal is preferred over obscuring |
| **Data minimisation** | Collecting only what is needed to substantiate a finding |
| **Synthetic data** | Machine-generated illustrative data, not derived from a real subject |
| **Placeholder** | An explicit `PENDING VERIFICATION` marker naming exactly what is required |
| **Confidentiality classification** | The sensitivity label applied to an artefact |
| **Chain of custody** | Documented handling history of an artefact |
| **PoC (proof of concept)** | The minimal demonstration that a weakness is real |
| **Root cause** | The underlying fault. *Probable* root cause where no source or log access exists |

---

## 6. Commands referenced in this repository

| Command | Purpose | Caution |
| --- | --- | --- |
| `curl <url>` | Retrieve a resource | Only for the authorized target under engagement rules |
| `wget <url>` | Download a file | Only for the authorized target; verify the destination directory first |
| `qpdf --password=… --decrypt in.pdf out.pdf` | Decrypt a PDF to an unlocked copy | Handles a credential — keep it out of shell history and out of version control |
| `exiftool <file>` | Read metadata | Metadata may itself be sensitive; read it before you publish it |
| `exiftool -all= <file>` | Strip metadata on export | Should be a step in the export pipeline, not a manual fix |
| `sha256sum <file>` | Hash for integrity and identification | Record hashes before analysis so later edits are detectable |
| `git log -S'<pattern>'` | Search history for a string | Never paste a real secret as the pattern |
| `python3 scripts/repo_checks.py` | Repository documentation QA | Offline |
| `python3 scripts/evidence_sanitizer.py` | Sanitised copy of text evidence | Offline; never overwrites the input; manual review still required |

---

## 7. Abbreviations

| Abbreviation | Expansion |
| --- | --- |
| AC / AT / AV / PR / SC / SI / UI / VA / VC / VI / SA | CVSS metric abbreviations (§4) |
| ASVS | Application Security Verification Standard |
| CVSS | Common Vulnerability Scoring System |
| CWE | Common Weakness Enumeration |
| DoS | Denial of Service |
| HSTS | HTTP Strict Transport Security |
| ID | Identifier |
| JTR | John the Ripper — the source of the instructor-supplied wordlist |
| LLM | Large Language Model |
| OWASP | Open Worldwide Application Security Project |
| PDF | Portable Document Format |
| PII | Personally Identifiable Information |
| PoC | Proof of Concept |
| PTES | Penetration Testing Execution Standard |
| RoE | Rules of Engagement |
| SQL | Structured Query Language |
| TLS | Transport Layer Security |
| TTP | Tactics, Techniques and Procedures |
| WAF | Web Application Firewall |
| WSTG | Web Security Testing Guide |
| XSS | Cross-Site Scripting |

---

## 8. Related documentation

| Document | Purpose |
| --- | --- |
| [`methodology.md`](methodology.md) | How the method was applied |
| [`authorization-and-scope.md`](authorization-and-scope.md) | Scope boundaries |
| [`rules-of-engagement.md`](rules-of-engagement.md) | Operating constraints |
| [`../findings/README.md`](../findings/README.md) | Status vocabulary in use |
| [`../risk/risk-rating-methodology.md`](../risk/risk-rating-methodology.md) | Rating definitions |
| [`../evidence/README.md`](../evidence/README.md) | Evidence classification scheme |
