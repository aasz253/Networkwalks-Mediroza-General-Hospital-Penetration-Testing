# M2 — Tools and Methods

**Milestone:** Data Extraction / File Security · **Status:** ✅ Documented

---

## 1. Tools used

| # | Tool | Type | Purpose | Version |
| --- | --- | --- | --- | --- |
| T-03 | Networkwalks Hash Calculator (`networkwalks.com/hash-calculator/`) | Provider web tool | Extract the `$pdf$` key identifier from an encrypted PDF | Not recorded |
| T-04 | Networkwalks Password Cracker (`networkwalks.com/password-cracker/`) | Provider web tool | Wordlist-based key recovery against a `$pdf$` identifier | Not recorded |
| T-05 | Built-in top-100 wordlist | Wordlist | First-pass recovery for `LAB-PDF-01`, `LAB-PDF-02` | Provider-supplied |
| T-06 | Instructor-supplied JTR wordlist | Wordlist | Escalation for `LAB-PDF-03` | Instructor-supplied |
| T-07 | `qpdf` | CLI | Decrypt `LAB-PDF-03` to a temporary unlocked copy | Not recorded |

Supporting: text editor for inspecting file structure; `exiftool` was used in
[M3](../M3-critical-data-exposure/) on the decrypted copy.

> ⚠️ **Versions not recorded.** A professional assessment records the exact tool
> version, because cracker behaviour and output formats change. This is a genuine
> gap in the engagement record rather than something to back-fill.

> 🔒 **Data handling during tool use.** Only **hash identifiers** were submitted to
> the provider's tools — not the documents. This distinction matters: a `$pdf$`
> hash leaks materially less than a patient document. Had the files been uploaded,
> that would have been a disclosure event requiring disclosure to the client.

---

## 2. Method

### 2.1 Sequence

| Step | Action | Command / interface | Output |
| --- | --- | --- | --- |
| 1 | Extract key identifier | Networkwalks Hash Calculator | `$pdf$…` per file |
| 2 | Baseline dictionary attack | Networkwalks Password Cracker, built-in list | Recovery for files 1 and 2 |
| 3 | Escalation | Networkwalks Password Cracker, JTR list | Recovery for file 3 |
| 4 | Decrypt for metadata access | `qpdf --password=… --decrypt in.pdf out.pdf` | Temporary unlocked copy |
| 5 | Metadata extraction | `exiftool report3_open.pdf` | Fed [M3](../M3-critical-data-exposure/) |

### 2.2 Why hash-then-crack rather than attack the file

| Approach | Consequence |
| --- | --- |
| Attack the encrypted file directly | Requires the file in the cracking tool; slower; often needs format-specific handling |
| Extract the key identifier, then attack it | Portable, fast, format-agnostic, and the identifier can be handled more safely than the document |

### 2.3 Why the escalation at Step 3 was necessary

A single exhausted wordlist is a weak experiment. Two lists producing different
results establish something more useful: a **bracket** on key strength.

| Outcome | Interpretation |
| --- | --- |
| Recovered by list A | Key is within list A |
| Not recovered by list A, recovered by list B | Key is between A and B — bounded above and below |
| Not recovered by either | Key is outside both — still no lower bound |

---

## 3. Test conditions

| Condition | Value | Note |
| --- | --- | --- |
| Attack type | Offline dictionary | No service interaction, no rate limit, no lockout |
| Requests to the target during M2 | **Zero** | The files were already held locally |
| Data submitted to a third party | `$pdf$` hash identifiers only | Documents were **not** uploaded |
| Wordlists used | 2 — built-in top-100, instructor-supplied JTR list | Rule-based mutations **not** used |
| Hardware | Not recorded | Cloud-based provider tooling was used |
| Time per file | Seconds | No meaningful constraint |
| Retries | None required beyond the escalation | — |
| Files decrypted | 1 of 3 | Only `LAB-PDF-03`, because metadata was the M3 objective |
| Decrypted copies retained | None | Discarded after metadata extraction |
| Document content read | **Never** | Out of scope by design |

---

## 4. Limitations

| # | Limitation | Effect on conclusions |
| --- | --- | --- |
| 1 | No rule-based mutation attack | Key strength is understated. A key recovered from a static list may also fall to mutations of common patterns. |
| 2 | No targeted wordlist | A list derived from the organisation's own vocabulary, names, or visible internal terminology was not attempted. Such lists are often dramatically more effective. |
| 3 | No dedicated GPU hardware | Recovery cost in absolute compute terms is overstated; wall-clock time is what matters, and it was seconds. |
| 4 | Provider web tooling, versions unrecorded | Output format and behaviour cannot be independently reproduced |
| 5 | Single pass per list | No measurement of position within the list, so recovery cost is described ordinally ("within the first 100") rather than numerically |
| 6 | Encryption algorithm not analysed | The algorithm is irrelevant given key strength; stating so avoids the appearance of a crypto review that did not happen |
| 7 | Transport security not assessed | Whether the documents were served over correctly configured TLS was never tested — see [threat model](./encryption-assessment.md#6-threat-model) |
| 8 | Only three files assessed | No basis for claiming the weakness extends across the estate |

---

## 5. What a stronger assessment would add

| # | Addition | Value |
| --- | --- | --- |
| 1 | Rule-based mutation pass | Would likely recover more keys and better bound the weakness |
| 2 | Targeted wordlist from organisational vocabulary | The most likely real-world success path |
| 3 | Password-reuse check across the estate | Determines whether one key exposes multiple documents |
| 4 | Confirm keys are transmitted and stored securely | A recoverable key is a smaller problem than a key in an email thread |
| 5 | Assess the document distribution channel | How does a recipient obtain the key? If by email, the channel is the weakness |
| 6 | Record tool versions | Reproducibility |
| 7 | Assess TLS as documents are distributed | Closes limitation 7 |

---

## 6. Reproducibility note

This milestone's method is **described, not scripted**, and that is intentional.

| Reason | Detail |
| --- | --- |
| Authorisation is specific | Permission to test the training target does not transfer to a reader of this repository |
| Publishing a cracking harness would be a different thing entirely | A repository containing a ready-to-run key-recovery pipeline for arbitrary PDFs is a weapon, not documentation |
| The intellectual content is the *reasoning* | Which list, why escalate, what the failure meant, why "strong" is the wrong conclusion — none of which needs automation |
| Provider tooling was used | The lab supplied purpose-built web tools; wrapping them in automation would add nothing |

An authorised tester assessing **their own** files has every tool available on the
public internet and needs none from this repository.

---

## 7. Data-handling record

| Action | Performed | Note |
| --- | --- | --- |
| Documents uploaded to any third-party service | ❌ No | Only hash identifiers were submitted |
| Hash identifiers submitted | ✅ Yes | Materially lower sensitivity than the documents |
| Recovered keys recorded in this repository | ❌ No | Withheld by policy — [results §3](./results.md#3-password-strength-assessment-values-withheld) |
| Recovered keys written to a file | ✅ Transiently, during verification | Necessary to confirm a key opens its file. Never committed. |
| Keys passed on a command line | ✅ Yes, to `qpdf` | Poor practice — lands in shell history and process listings. Prefer an environment variable or interactive prompt. Recorded as a lesson, not repeated. |
| Keys printed to a terminal captured as evidence | ❌ Not published | Evidence artefacts for this milestone require mandatory redaction — [`evidence/README.md`](./evidence/README.md) §4 |
| Document content read | ❌ No | Never |
