# M2 — Evidence Index

**Milestone:** Data Extraction / File Security · **Registered observations:** 6 · **Artifacts attached:** 0

> 🔴 **Highest-sensitivity milestone in the engagement.** Artifacts from M2 are
> the most likely to contain recoverable credentials. Treat every item as
> 🔴 Confidential until reviewed.

Policy and procedure: [`../../evidence/README.md`](../../../evidence/README.md) ·
Master register: [`../../evidence/evidence-register.csv`](../../../evidence/evidence-register.csv)

---

## 1. Evidence register — M2

| Evidence ID | Description | Related finding | Sensitivity | Contains credential material | Artifact |
| --- | --- | --- | --- | --- | --- |
| `NW-B083-M2-E01` | `$pdf$` key identifiers extracted from all three files | F04 | 🔴 Confidential | **Yes** — derived key material | ❌ |
| `NW-B083-M2-E02` | Key recovery result for `LAB-PDF-01` | F04 | 🔴 Confidential | **Yes** — recovered key | ❌ |
| `NW-B083-M2-E03` | Key recovery result for `LAB-PDF-02` | F04 | 🔴 Confidential | **Yes** — recovered key | ❌ |
| `NW-B083-M2-E04` | Wordlist exhaustion, then recovery, for `LAB-PDF-03` | F04 | 🔴 Confidential | **Yes** — recovered key | ❌ |
| `NW-B083-M2-E05` | `qpdf` decryption of `LAB-PDF-03` | F04, F05 | 🔴 Confidential | **Yes** — password inline in the command | ❌ |
| `NW-B083-M2-E06` | Structural and metadata summary of the three files | F04, F05 | 🟠 Internal | No | ❌ |

---

## 2. Expected artifacts

| Evidence ID | Type | Filename convention | Mandatory redaction |
| --- | --- | --- | --- |
| `NW-B083-M2-E01` | Text capture | `NW-B083-M2-E01_pdf-hash-identifiers.txt` | Truncate or hash the `$pdf$` identifiers |
| `NW-B083-M2-E02` | Screenshot | `NW-B083-M2-E02_report-01-key-recovered.png` | Blur the key value; show only the outcome |
| `NW-B083-M2-E03` | Screenshot | `NW-B083-M2-E03_report-02-key-recovered.png` | Blur the key value |
| `NW-B083-M2-E04` | Screenshot | `NW-B083-M2-E04_report-03-list-escalation.png` | Blur the key value; retain both attempt outcomes |
| `NW-B083-M2-E05` | Terminal capture | `NW-B083-M2-E05_qpdf-decrypt-command.txt` | **Remove the password from the command entirely** |
| `NW-B083-M2-E06` | Text capture | `NW-B083-M2-E06_file-structure-summary.txt` | Review for metadata disclosure |

Target directory: `evidence/screenshots/M2/`

---

## 3. Mandatory redaction rules for M2

### 3.1 Never publish

| Item | Reason |
| --- | --- |
| Any recovered document password | It is a credential. Publishing it teaches the wrong habit and shortens an attacker's work. |
| `$pdf$` hash identifiers in full | Derived key material. The strength analysis needs only the outcome, not the value. |
| A command line containing a password | Lands in shell history, `ps` output and process logs — and in a published terminal capture |
| Any document content | Out of scope, and possibly clinical |

### 3.2 Instead, publish

| Item | Sufficient to substantiate the finding |
| --- | --- |
| Length class, character classes present, dictionary membership | ✅ Full strength characterisation |
| Recovery outcome and the list used | ✅ Complete methodological record |
| A blurred or masked key value | ✅ Visual evidence of the result |
| The command with the password argument replaced by a placeholder | ✅ Reproducibility of the method without the secret |

### 3.3 Redaction checklist

- [ ] Recovered keys replaced with a placeholder such as `<REDACTED>` or `[MASKED]`
- [ ] `$pdf$` identifiers truncated or replaced
- [ ] `qpdf --password=…` rewritten as `qpdf --password='<REDACTED>' --decrypt …`
- [ ] Shell history, `.bash_history` and terminal scrollback excluded from any capture
- [ ] Browser autofill or password-manager UI excluded from screenshots
- [ ] Provider-tool screenshots cropped to show the outcome, not the input
- [ ] No decrypted document content captured
- [ ] No temporary decrypted copies committed
- [ ] SHA-256 recorded **before** redaction; redacted copy hashed separately
- [ ] Manual review completed — automated redaction will not catch a key in a screenshot

---

## 4. Automated sanitization — and its limit here

For **text** artifacts, the sanitizer can help:

```bash
python3 scripts/evidence_sanitizer.py \
  --input <raw-text-capture> \
  --output-dir ./sanitized-out
```

It flags pattern classes including `$pdf$…` identifiers, `--password=` arguments
and shell history paths. It reports **classes and locations**, never matched
values.

> ⚠️ **It cannot help with screenshots.** A recovered key rendered in a GUI is
> pixels. No regex will find it. For image artifacts, redaction is entirely manual —
> which is why the checklist in §3.3 exists and why `redaction_status` in the
> register must be set by a person.

Self-test: `python3 scripts/evidence_sanitizer.py --self-test`

---

## 5. Image references

Intended paths are recorded in fenced code so that no broken link exists while the
artifacts are absent.

```
![Placeholder — NW-B083-M2-E02](../../evidence/screenshots/M2/NW-B083-M2-E02_report-01-key-recovered.png)
```

Convert to a live reference only after: artifact exists → sanitised → manually
reviewed → registered → `artifact_present=YES`.

---

## 6. Outstanding work

| # | Task | Status |
| --- | --- | --- |
| 1 | Capture the 6 M2 artifacts into the off-repository raw store | ❌ Not done |
| 2 | Run the sanitizer over the text captures | ❌ Not done |
| 3 | Manually redact screenshots — mask every key value | ❌ Not done |
| 4 | Rewrite any captured command to remove inline passwords | ❌ Not done |
| 5 | Place reviewed artifacts in `evidence/screenshots/M2/` | ❌ Not done |
| 6 | Update `artifact_present` and `redaction_status` in the register | ❌ Not done |
| 7 | Convert §5 placeholders to live references | ❌ Blocked by 5 |
| 8 | Record SHA-256 for each artifact | ❌ Not done |
| 9 | Confirm no temporary decrypted copies exist anywhere in the working tree | ❌ Not done |

Until items 1–6 are complete, `NW-B083-M2-F01` remains at status **Documented**
rather than **Evidence-attached**.
