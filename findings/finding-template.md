# Finding Template

Copy to `findings/verified-findings/NW-B083-<MS>-F<nn>-<slug>.md` and fill every
section.

> **Rules**
> 1. Do not delete a section. If information is missing, write
>    `PENDING VERIFICATION — required: <exactly what is needed>`.
> 2. Never state a result without an evidence ID.
> 3. Never publish a credential, personal data value or document content.
> 4. Root causes are **probable** unless source or log access exists.
> 5. Image references are added **only** once the artifact exists and is registered.

---

# NW-B083-<MS>-F<nn> — <Finding title>

| Field | Value |
| --- | --- |
| **Finding ID** | `NW-B083-<MS>-F<nn>` |
| **Title** | <short, specific, no severity in the title> |
| **Milestone** | `<M1 \| M2 \| M3 \| M4>` |
| **Affected component** | `<path, file, endpoint>` |
| **Severity** | `Critical \| High \| Medium \| Low` |
| **Rating status** | `Confirmed \| Provisional` |
| **Verification status** | `Documented \| Evidence-attached \| Verified` |
| **Confidence** | `High \| Medium \| Low` |
| **OWASP category** | `A01 \| A02 \| A03 \| A05 \| A07` |
| **CWE** | `CWE-<n> <name>` |
| **Evidence IDs** | `NW-B083-<MS>-E<nn>`, … |
| **Reported date** | `<YYYY-MM-DD>` |
| **Reporter** | Antony Sifuna (`SifunaCodex`) |
| **Status** | `Open \| In remediation \| Retest pending \| Closed \| Withdrawn` |

---

## 1. Description

<One paragraph. What the weakness is, in the present tense and without hedging.
State the component, the mechanism and the control that fails. No impact language
here — that belongs in §7.>

---

## 2. Affected component

| Field | Value |
| --- | --- |
| Location | `<URL or path>` |
| Component type | `<page \| form \| API \| file \| configuration>` |
| Authentication required to reach it | `<None \| Any \| Specific role>` |
| Data at risk | `<data classes — never values>` |

---

## 3. Preconditions

What an attacker must already have. If the answer is "nothing", say so explicitly.

| # | Precondition | Satisfied by the bypass in this engagement? |
| --- | --- | --- |
| 1 | <e.g. Network access to the host> | ✅ Yes |
| 2 | <e.g. A valid account> | ❌ No — <state how it was obtained, or that it was not needed> |

---

## 4. Technical evidence

### 4.1 Observation

<What was seen. Quote only what is necessary. Redact anything sensitive.>

| # | Evidence ID | Observation | Artifact |
| --- | --- | --- | --- |
| 1 | `NW-B083-<MS>-E<nn>` | <description> | ❌ Not attached |

### 4.2 Expected vs. observed

| | Expected (secure behaviour) | Observed |
| --- | --- | --- |
| **Response / behaviour** | <…> | <…> |

### 4.3 Mechanism

<Explain *why* the observed behaviour occurs. Use a table or an annotated snippet.
Show the incorrect and the correct form side by side where a code fix is involved.>

---

## 5. Reproduction summary

> Authorised environment only. Minimal, non-destructive, non-persistent.

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | <…> | <…> |

| Bound | Limit |
| --- | --- |
| Requests required | `<n>` |
| Authentication required | `<None \| …>` |
| Side effects | `<none — state explicitly>` |
| Validation threshold | <Why this is sufficient to substantiate the finding> |

**Explicitly not performed:**

| Action | Reason |
| --- | --- |
| <e.g. Bulk extraction> | <Not required to substantiate; prohibited> |

---

## 6. Root cause

**Probable** — no source or log access was available.

| Probable cause | Confidence | To confirm |
| --- | --- | --- |
| <…> | `High \| Medium \| Low` | <the check that would confirm it> |

---

## 7. Security impact

| Dimension | Assessment |
| --- | --- |
| Confidentiality | `<…>` |
| Integrity | `<… — state whether demonstrated or merely possible>` |
| Availability | `<…>` |
| Data sensitivity | `<clinical \| personal \| financial \| internal>` |
| Business consequence | `<…>` |
| Detection likelihood | `<…>` |

**Cross-finding effect:** <How this finding enabled or amplified another.>

---

## 8. Severity

| Attribute | Value |
| --- | --- |
| Severity band | `<Critical \| High \| Medium \| Low>` |
| Rationale | <Why this band and not the adjacent one — this is the part reviewers read> |
| Confidence | `<High \| Medium \| Low>` |
| Rating status | `<Confirmed \| Provisional>` |
| Provisional reason | <If provisional: which input is missing, and which way the rating could move> |

---

## 9. CVSS v4.0

**Vector:** `CVSS:4.0/AV:<…>/AC:<…>/AT:<…>/PR:<…>/UI:<…>/VC:<…>/VI:<…>/VA:<…>/SC:<…>/SI:<…>/SA:<…>`

**Base score:** `PENDING — compute with the FIRST CVSS v4.0 calculator`

| Metric | Value | Evidence-based justification |
| --- | --- | --- |
| AV | `<N\|A\|L\|P>` | <…> |
| AC | `<L\|H>` | <…> |
| AT | `<N\|P>` | <…> |
| PR | `<N\|L\|H>` | <…> |
| UI | `<N\|P\|A>` | <…> |
| VC | `<H\|L\|N>` | <…> |
| VI | `<H\|L\|N>` | <…> |
| VA | `<H\|L\|N>` | <…> |
| SC | `<H\|L\|N>` | <…> |
| SI | `<H\|L\|N>` | <…> |
| SA | `<H\|L\|N>` | <…> |

---

## 10. Remediation

### 10.1 Primary fix

<The change that removes the weakness. Include a before/after code or configuration
example where it helps.>

### 10.2 Additional hardening

| # | Measure | Addresses |
| --- | --- | --- |
| 1 | <…> | <…> |

### 10.3 Actions taken

| # | Action | Status |
| --- | --- | --- |
| 1 | <…> | `Not started` |

---

## 11. Retest criteria

| # | Criterion | Method | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | <…> | <…> | <…> | ⬜ Not tested |

> A retest is reported as **what was attempted and what happened**, never as a
> verdict on residual strength.

---

## 12. Status

| Field | Value |
| --- | --- |
| Current status | `Open` |
| Verification status | `Documented` |
| Rating status | `<Confirmed \| Provisional>` |
| Evidence artifacts attached | `0` |
| Outstanding to close | <Exactly what is required> |

---

## 13. Confidentiality declaration

- [ ] No credential, key, token, cookie or session value present
- [ ] No patient content reproduced
- [ ] No salary, shareholder or other personal value reproduced
- [ ] Any individual referenced is masked and identified by role only
- [ ] All synthetic content labelled `SYNTHETIC — NOT CLIENT DATA`
- [ ] Root cause stated as probable where source access is absent
- [ ] No client approval or sign-off claimed
