# M2 — Data Extraction and File Security

**Milestone status:** ✅ Complete · **Steps executed:** 4 of 4
**Files assessed:** `LAB-PDF-01`, `LAB-PDF-02`, `LAB-PDF-03`
**Finding produced:** `NW-B083-M2-F01`

---

## 1. Objective and authorized scope

**Objective.** Assess the security properties of the three PDF test files supplied
through the portal reached in [M1](../M1-initial-access/): encryption presence,
key strength, metadata hygiene, and the security of their storage and distribution
path.

### Handling rules for this milestone

| Rule | Application |
| --- | --- |
| Files are labelled `LAB-PDF-01…03` | Non-identifying labels; original filenames are recorded once, in the [file inventory](./file-analysis.md) |
| Document **content** was never opened | Only encryption properties and metadata fields were assessed |
| Recovered passwords are **withheld** | Strength characterised instead — [results](./results.md) §3 |
| No patient data is reproduced | Not applicable — no content was read |
| Analysis was offline | The files were already in the tester's possession; no service was contacted |

---

## 2. The question this milestone answers

M1 produced three password-protected PDFs. The instinctive conclusion is that the
documents are protected.

**They were not.** All three files carried encryption, and all three keys fell to
dictionary attack — two to a list of the 100 most common passwords in the world,
and one to a moderately larger list.

This is the milestone's real lesson: *encryption that depends on a guessable
secret provides no protection.* The control existed, appeared to be working, and
delivered nothing against the most likely attacker.

---

## 3. Summary of results

| File | Encryption present | Key recovered | Method | Dictionary rank class | Effective protection |
| --- | --- | --- | --- | --- | --- |
| `LAB-PDF-01` | ✅ Yes | ✅ Yes | Built-in top-100 list | Immediate — within the first 100 | **None** |
| `LAB-PDF-02` | ✅ Yes | ✅ Yes | Built-in top-100 list | Immediate — within the first 100 | **None** |
| `LAB-PDF-03` | ✅ Yes | ✅ Yes | **Instructor-supplied JTR list** after the built-in list was exhausted | Larger dictionary | **Negligible** |

> 🔒 **Password values are not published in this repository.** See
> [results §3](./results.md#3-password-strength-assessment-values-withheld) for the
> strength analysis and the reasoning.

**Finding:** [`NW-B083-M2-F01`](../../findings/verified-findings/NW-B083-M2-F01-weak-document-passwords.md) — 🔴 High

---

## 4. Step-by-step record

### Step 1 — Hash extraction

Password-based PDF encryption means the document cannot be read without the key.
Cracking therefore works against a **hash** of the key rather than the file
itself: candidate passwords are hashed and compared.

Each file was submitted to the Networkwalks Hash Calculator:

```
https://networkwalks.com/hash-calculator/
```

| File | Output |
| --- | --- |
| `LAB-PDF-01` | `$pdf$…` hash — **value withheld** |
| `LAB-PDF-02` | `$pdf$…` hash — **value withheld** |
| `LAB-PDF-03` | `$pdf$…` hash — **value withheld** |

> A `$pdf$` hash is a derived key identifier, not the password itself. It is
> nevertheless withheld here as a defence-in-depth measure: published alongside a
> strength description, it shortens an attacker's work for no analytical benefit.
> The client already possesses these values.

Evidence: `NW-B083-M2-E01`

### Step 2 — Key recovery for reports 1 and 2

Each hash was submitted to the Networkwalks Password Cracker with the built-in
list covering the 100 most common passwords:

```
https://networkwalks.com/password-cracker/
```

| File | Result | Attempts required |
| --- | --- | --- |
| `LAB-PDF-01` | ✅ Key recovered | Within the first 100 candidates |
| `LAB-PDF-02` | ✅ Key recovered | Within the first 100 candidates |

Evidence: `NW-B083-M2-E02`, `NW-B083-M2-E03`

### Step 3 — Key recovery for report 3, and the escalation lesson

| Attempt | Wordlist | Result |
| --- | --- | --- |
| 1 | Built-in top-100 | ❌ `Exhausted wordlist. No match. ACCESS DENIED.` |
| 2 | Instructor-supplied JTR list | ✅ Key recovered |

**The lesson.** A failed small-list run is **not** evidence of a strong password.
It is evidence of a small wordlist. `LAB-PDF-03`'s key required character-class
diversity and looked materially stronger beside the first two — and still fell to
a moderately larger dictionary.

| Wrong conclusion | Correct conclusion |
| --- | --- |
| "This password is strong; the small list was unlucky" | "The key is outside a 100-word dictionary" |
| "More effort is required" | "More candidates are required" |
| "The control is working" | "The control's strength is a function of the attacker's wordlist" |

**Why it matters:** an assessor who stops at the first exhausted list will report
a file as adequately protected that is not. Real attackers maintain multiple
lists precisely because this is the standard path.

Evidence: `NW-B083-M2-E04`

### Step 4 — Decryption of report 3

Key recovery alone does not expose metadata. A locked PDF exposes almost nothing —
which is itself worth noting: *protection mechanisms reduce forensic visibility as
well as confidentiality.*

To assess metadata, one unlocked copy was produced:

```bash
qpdf --password='<redacted>' --decrypt patient_report_3.pdf report3_open.pdf
```

| Item | Value |
| --- | --- |
| Files decrypted | **One** — `LAB-PDF-03` only |
| Reason | Report 3 was the one carrying metadata; the others were not needed |
| Decrypted copies retained | **None.** Temporary copies were used and discarded. |
| Purpose of the unlocked copy | Enable `exiftool` to read fields — feeding [M3](../M3-critical-data-exposure/) |
| Content | **Not read.** Only metadata fields were extracted. |

> 🔒 The command above is shown with the password redacted. Never commit a real
> key on a command line — it lands in shell history, in `ps` output, and in any
> process log. Prefer an environment variable or an interactive prompt.

Evidence: `NW-B083-M2-E05`

---

## 5. Security implications

| Implication | Detail |
| --- | --- |
| **Encryption is present but ineffective** | All three files were encrypted. Against a dictionary attacker, none of them was protected. |
| **Access control was the only real control** | The documents were protected by the login check — which M1 demonstrated was bypassable. Document encryption contributed nothing. |
| **Security by obscurity was mistaken for security** | A password chosen because it is obscure is not a control; it is a delay. |
| **Recovery cost is negligible** | Two files fell to the first 100 candidates. Any attacker reaches that within seconds. |
| **The strongest key was still weak** | `LAB-PDF-03` needed a bigger list, not a better algorithm. There was no cryptographic barrier at any point. |
| **Protection hid the metadata** | Locking the file also hid the `Author` field and the internal note that led to the Critical findings in M3. Any defender using password protection as an information-hiding measure is mistaken. |

---

## 6. Remediation

| ID | Recommendation | Priority |
| --- | --- | --- |
| R-7 | Generate cryptographically random document passwords — full printable-ASCII length, no dictionary words, no name or date patterns | **P0** |
| R-8 | Treat the document password as a **secondary** control only. Access control must carry the security. | **P0** |
| R-9 | Never treat a document password as the sole barrier to a patient record | **P0** |
| R-10 | Store documents outside the web root, served only through an authorising endpoint | **P0** |
| R-11 | Store document keys in a secrets manager, not in filenames, URLs, mail or chat | P1 |
| R-12 | Set PDF permissions (print/copy/extract restrictions) — defence in depth, not a control | P2 |
| R-13 | Log and alert on bulk document downloads | P1 |
| R-14 | Add a policy gate so documents cannot be published without a recorded key-management decision | P2 |

**Retest criterion.** Re-run hash extraction and dictionary recovery with at least
the JTR list plus a rule-based mutation pass. A file that fails all of them is not
*proven* strong — only uncracked by these methods. That distinction belongs in the
report.

---

## 7. Evidence index

| Evidence ID | Description | Finding | Sensitivity | Artifact |
| --- | --- | --- | --- | --- |
| `NW-B083-M2-E01` | `$pdf$` hash output for all three files | F04 | **Confidential** | ❌ |
| `NW-B083-M2-E02` | Key recovery result for `LAB-PDF-01` | F04 | **Confidential** | ❌ |
| `NW-B083-M2-E03` | Key recovery result for `LAB-PDF-02` | F04 | **Confidential** | ❌ |
| `NW-B083-M2-E04` | Wordlist exhaustion then recovery for `LAB-PDF-03` | F04 | **Confidential** | ❌ |
| `NW-B083-M2-E05` | `qpdf` decryption of `LAB-PDF-03` | F04, F05 | **Confidential** | ❌ |
| `NW-B083-M2-E06` | Structural and metadata summary of the three files | F04, F05 | Internal | ❌ |

> ⚠️ **M2 evidence is the most sensitive in the engagement.** Artifacts from this
> milestone are likely to contain recovered keys, hash values, or command lines
> with passwords inline. Mandatory redactions are listed in
> [`evidence/README.md`](./evidence/README.md) §4.

---

## 8. Milestone conclusion

All three files were assessed and all three keys were recovered. Two fell to the
100 most common passwords in the world; the third fell to a moderately larger
dictionary.

The control that was present on all three files provided no meaningful protection.
Combined with the bypassable login from M1, the documents' security reduced to
something a determined attacker with a wordlist and a free afternoon could
overcome — which is roughly what happened.

The escalation at Step 3 is the transferable part: **a failed small wordlist is a
statement about the wordlist, not about the key.**

---

## 9. Documents in this milestone

| Document | Contents |
| --- | --- |
| [`file-analysis.md`](./file-analysis.md) | File identification, format and structure, metadata inventory |
| [`encryption-assessment.md`](./encryption-assessment.md) | Encryption and password-protection analysis |
| [`tools-and-methods.md`](./tools-and-methods.md) | Tools used, method, test conditions, limitations |
| [`results.md`](./results.md) | Per-file results, verification approach, password strength analysis |
| [`evidence/README.md`](./evidence/README.md) | Evidence references and redaction requirements |
