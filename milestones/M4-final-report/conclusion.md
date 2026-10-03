# Conclusion

Overall assessment, what remains unknown, and the current status of this report.

---

## 1. Overall assessment

An anonymous party could obtain the entire application database — clinical,
personal-finance and corporate-governance data — using a browser, `curl`, and
information the application itself returned.

| Question | Assessment |
| --- | --- |
| Was the data reachable anonymously? | **Yes. Demonstrated.** |
| Was advanced capability required? | **No.** No scanner, no exploit framework, no credential attack |
| How many requests? | One to retrieve the database. Zero in two of four milestones |
| Is any control partially effective? | Only in the smaller findings. **The Critical exposure had none** |
| Is remediation within reach? | **Yes.** The severe exposure is one misplaced file |

---

## 2. What went well

| Observation | Why it matters |
| --- | --- |
| Disclosure files narrowed the search immediately | Reduced an open-ended assessment to three paths |
| Error-based injection confirmation needed no tooling | Minimal validation was sufficient to prove a Critical weakness |
| Offline analysis of documents cost zero requests | Kept handling risk low and scope tight |
| A **negative control** was recorded — one recovery attempt failed | Proved the tooling behaved correctly, making the successes meaningful |
| One security assessment, no clients, no servers harmed | Proportionality held throughout |

---

## 3. What did not go well

### 3.1 Application and infrastructure

| Gap | Consequence |
| --- | --- |
| Input concatenated into a login query | Authentication defeated |
| Verbose database errors returned to the client | Injection confirmed, and the query structure revealed |
| Documents served as static files in the web root | One session check was the only barrier |
| Directory indexing enabled on a legacy path | A backup's filename was handed out |
| A database backup stored unencrypted in a web root | Complete cleartext database exposure |
| No owner or lifecycle for migration artefacts | The legacy path survived |
| Distinct login error messages | A valid account was identified for free |
| No metadata stripping on document export | A backup location travelled inside a patient report |

### 3.2 Assessment gaps — recorded as candidly as the findings

| Gap | Why it matters |
| --- | --- |
| Unauthenticated access to known document URLs not tested | One rating stays provisional; the test would likely raise it to Critical |
| Object-level authorisation not tested | Horizontal escalation may exist |
| No evidence artifacts supplied | **No finding can be called verified** |
| No CVSS base scores computed | Vectors must be scored independently |
| No fingerprinting performed | The stack is inference, not observation |
| No timestamps or tool versions recorded | Artifacts cannot be independently dated |
| Rate limiting, lockout and session management untested | Behaviour under sustained attack unknown |
| Legacy directory not fully enumerated | One rating stays provisional |
| One table in the backup not characterised | Cannot be assumed benign |
| Remediation not retested | Every fix here is a recommendation |

> **The four largest gaps are all cheap to close** — one request, one directory
> enumeration, one calculator, and a sanitization pass. None requires new access.

---

## 4. Counterfactual analysis

Which single control, added at any point, would have broken the chain?

| Control introduced | Chain broken at | Findings prevented |
| --- | --- | --- |
| Parameterised queries | `M1-F02` | `M1-F02`, and downstream `M1-F03`, `M2-F01`, `M3-F01`, `M3-F02`, `M3-F03` |
| Documents outside the web root | `M1-F03` | `M1-F03`, `M2-F01` — and `M3-F01` never begins |
| Metadata stripping on export | `M3-F01` | `M3-F01`, `M3-F02`, `M3-F03` |
| Directory indexing disabled | `M3-F02` | Reduces discoverability — **not** reachability of the backup |
| **Backups outside the web root** | `M3-F03` | `M3-F03` |
| Generic login errors | `M1-F01` | `M1-F01` only; the bypass would still be found |

| Observation |
| --- |
| **No single control prevents everything** — which is the actual argument for defence in depth |
| The deepest break point is the SQL injection: it invalidates five of the seven findings |
| Disabling directory listing is the **weakest** apparent fix — it hides the index while the backup stays reachable |

---

## 5. Recommendations in one paragraph

Remove the backup immediately and search every web-served path for others; treat all
data it contained as compromised and assess notification obligations; decommission
the legacy path; disable directory indexing globally; parameterise every query and
stop returning database errors to clients; move documents out of the web root behind
an authorising endpoint with per-object checks; generate document keys with a CSPRNG
and manage them in a secrets manager; strip metadata automatically on export; store
backups off-web-root with KMS-held keys and enforced retention; add a CI gate that
fails on artefacts in web roots; and require decommissioning sign-off after any
migration. Then retest every criterion in [`remediation-plan.md`](./remediation-plan.md) §6.

---

## 6. Status of this report

| Field | Value |
| --- | --- |
| Report state | **Draft for review** |
| Findings | 7 documented; 0 verified |
| Evidence artifacts | 22 observations registered; **0 attached** |
| CVSS base scores | **Not computed** — deliberately pending the official calculator |
| Remediation owners | `UNASSIGNED` |
| Remediation retested | **No** |
| Batch reference | **Discrepancy open** — source record B082, project brief B083 |
| Client review | **None** |
| Classification decision | Not made |
| Sign-off | **None claimed** |
| Currency of findings | Point-in-time. **Current state unknown** |

### 6.1 Outstanding before issue

| # | Item | Blocking? |
| --- | --- | --- |
| 1 | Attach sanitised evidence artifacts | ✅ Yes — indefensible without them in a client report |
| 2 | Compute CVSS v4.0 base scores | ✅ Yes |
| 3 | Assign remediation owners and dates | ✅ Yes |
| 4 | Reconcile the batch reference | ✅ Yes |
| 5 | Confirm data currency of the backup | ✅ Yes — affects notification scope |
| 6 | Obtain client review, classification and sign-off | ✅ Yes |
| 7 | Confirm the M4 report format matches the engagement's expected format | No |
| 8 | Test unauthenticated access to a known document URL | No — but it may raise a rating |

---

## 7. Statement of limitations

This report is based on a point-in-time black-box assessment of one authorised
training environment over five business days, using manual techniques and no
exploitation tooling. Its findings are **documented, not verified**: no sanitised
evidence artifact has been supplied, so no observation in this report can be
independently re-examined by a third party. No finding should be read as proof that a
weakness is absent where testing was not performed.

The absence of findings for untested areas — object-level authorisation, session
management, rate limiting, sibling injectable parameters, and the wider estate — is
**not** assurance. Each is recorded as an open item for the reasons given in
[`scope-and-methodology.md`](./scope-and-methodology.md) §8 and
[`risk-assessment.md`](./risk-assessment.md) §8.

Recovered credentials, patient content, compensation figures, ownership data and
identified individuals are withheld throughout by policy. Schema and record counts
are published in place of data. No client review, approval, sign-off or
breach-notification decision is claimed anywhere in this report.

---

## 8. Sign-off

| Role | Name | Status | Date |
| --- | --- | --- | --- |
| Assessor | Antony Sifuna (`SifunaCodex`) | Report authored | — |
| Technical reviewer | `UNASSIGNED` | Not reviewed | — |
| Client technical reviewer | `UNASSIGNED` | Not reviewed | — |
| Client management approver | `UNASSIGNED` | Not reviewed | — |

> **No signature is recorded, and none should be inferred from the existence of this
> document.**

---

## 9. Related documents

| Document | Purpose |
| --- | --- |
| [`executive-summary.md`](./executive-summary.md) | Management-level summary |
| [`scope-and-methodology.md`](./scope-and-methodology.md) | Scope, authority, method, limitations |
| [`technical-findings.md`](./technical-findings.md) | Finding index and chain analysis |
| [`risk-assessment.md`](./risk-assessment.md) | Severity and prioritisation |
| [`remediation-plan.md`](./remediation-plan.md) | Actions and retest criteria |
| [`appendices.md`](./appendices.md) | Registers, ID schemes, glossary, references |