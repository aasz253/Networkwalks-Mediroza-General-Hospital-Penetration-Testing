# CVSS v4.0 assessment

Vector derivation for all seven findings, with a per-metric rationale, plus the
policy that governs numeric base scores.

> **No base score is published in this repository.** Vectors are derived; the
> numbers are deliberately left pending. §4 explains why, and specifies the exact
> input required to close them.

---

## 1. Documents

| Document | Purpose |
| --- | --- |
| **This file** | Metric-by-metric derivation and the scoring policy |
| [`risk-rating-methodology.md`](./risk-rating-methodology.md) | Bands, modifiers, confidence, prioritisation rules |
| [`risk-register.csv`](./risk-register.csv) | One row per finding |
| [`../findings/README.md`](../findings/README.md) | Rating-status definitions |
| [`../findings/verified-findings/`](./../findings/verified-findings/) | The finding records, each with its own vector |

---

## 2. Vectors

| ID | Severity | Vector | Rating |
| --- | --- | --- | --- |
| `NW-B083-M1-F01` | 🟠 Medium | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` | Confirmed |
| `NW-B083-M1-F02` | 🔴 Critical | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:N/SA:N` | Confirmed |
| `NW-B083-M1-F03` | 🔴 High | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N` | **Provisional** |
| `NW-B083-M2-F01` | 🔴 High | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` | **Provisional** |
| `NW-B083-M3-F01` | 🟠 Medium | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` | Confirmed |
| `NW-B083-M3-F02` | 🔴 Critical | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` | **Provisional** |
| `NW-B083-M3-F03` | 🔴 Critical | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` | Confirmed |

`M1-F01` and `M3-F01` share a vector and differ only in context — one is reached
over the network unauthenticated, the other requires a document in hand. CVSS
cannot express "requires a separate finding first"; that dependency is recorded in
the narratives instead.

---

## 3. Metric decisions that are not obvious

### 3.1 `SC` on `M1-F02` is `H`; on `M3-F03` it is `N`

This is the most commonly botched pair of decisions in this engagement.

| Finding | `SC` | Reason |
| --- | --- | --- |
| `M1-F02` | `H` | Compromising the authentication component extends to the whole application. The document store is a **subsequent system** reached *through* the bypass |
| `M3-F03` | `N` | The leaked artifact **is** data from the affected system, not a path into another one. The database is not compromised *via* something else |

> The distinction is *path versus payload*. Content belonging to a system is not a
> subsequent system; a system reached by using a compromised one is.

### 3.2 `VI` is only `H` where it was demonstrated

| Finding | `VI` | Reason |
| --- | --- | --- |
| `M1-F02` | `H` | A write primitive on an authentication query implies write capability. **Inferred, not demonstrated** — flagged as the one inferred metric in the engagement |
| `M1-F03` | `L` | Download-only path exercised; replacement in the same directory is plausible but untested |
| `M3-F02` | `N` | Directory listing is read-only |
| `M3-F03` | `N` | No modification was performed **or attempted** |

`M3-F03` reveals a schema that would assist tampering. That is impact *enabled*,
not impact *executed*, and CVSS measures execution. It is written up in
§6.1 of the finding rather than inflating the vector.

### 3.3 `PR` where a prerequisite is another finding

`M1-F03`, `M2-F01` and `M3-F01` all depend on a separate weakness being exploited
first. CVSS has no metric for "requires another finding".

| Finding | Metric chosen | Alternative framing | Where the dependency is recorded |
| --- | --- | --- | --- |
| `M1-F03` | `PR:L` — a session was required | `PR:N/AT:P` — no privilege, but a document must be located | Narrative + provisional rating |
| `M2-F01` | `PR:L` — a copy was required | `PR:N/AT:P` — key strength needs no privilege | §8.1 of the finding |
| `M3-F01` | `PR:N` — reading metadata needs no privilege | `AT:P` would flag the acquisition dependency | Narrative |

Both framings appear where the choice is contestable. A reviewer preferring the
other reading is given the alternative explicitly rather than being left to guess.

### 3.4 `VA:L` on `M1-F02`

No availability effect was observed. `L` rather than `N` because write access to
an authentication store raises the possibility of account lockout or destruction —
untested, and therefore not claimed as demonstrated.

### 3.5 `UI:N` everywhere

No finding requires a second party to act. The one arguable case is `M1-F03`: a
legitimate user would have to be tricked into requesting a document. That is not
what happened — an anonymous party requested it directly, so `UI:N` is correct.

---

## 4. Scoring policy — why no base score is printed

> **Rule: a numeric base score is computed only from the official FIRST CVSS v4.0
> calculator and recorded in [`risk-register.csv`](./risk-register.csv). It is never
> estimated, recalled, or produced by hand.**

| Reason | Detail |
| --- | --- |
| Accuracy | v4.0 scoring is a lookup-table computation. A mis-remembered value is indistinguishable from a correct one to the reader |
| Traceability | A printed number invites the question "where did this come from?" — the honest answer today is "not yet computed" |
| Avoids false precision | A score to one decimal place implies more precision than a provisional metric set can support |
| Reproducibility | Anyone can paste a vector into the official calculator and get the same number, without trusting this repository |

**To close this gap:** paste each vector from §2 into the official calculator at
<https://www.first.org/cvss/calculator/4.0>, then record
`cvss_v4_base_score` and the calculation date in
[`risk-register.csv`](./risk-register.csv).

### 4.1 What the severity bands *are* based on

| Band | Basis |
| --- | --- |
| 🔴 Critical | Demonstrated unauthenticated path to sensitive data, or full defeat of the authentication control |
| 🔴 High | Practical path to confidential documents or recoverable credentials |
| 🟠 Medium | Information disclosure that materially assists other attacks, or no independent data-compromise path |
| 🟢 Low | Hardening item with no demonstrated compromise path |

Full definitions and modifiers: [`risk-rating-methodology.md`](./risk-rating-methodology.md).

> The band and the vector answer different questions. The band is an
> impact-and-likelihood judgement in the engagement's own vocabulary; the vector is
> a standardised encoding. Where they appear to disagree — as with `M3-F02`, where
> a reviewer might argue Medium for directory listing in isolation — the
> disagreement is recorded in the finding rather than resolved silently.

---

## 5. Provisional findings

Three vectors depend on an untested input.

| Finding | Provisional input | If resolved |
| --- | --- | --- |
| `M1-F03` | `PR:L` assumed from the testing path; direct unauthenticated access untested | `PR:N` → band rises to Critical |
| `M2-F01` | `PR`/`AT` framing; key-reuse scope and mutation result unknown | Band unlikely to fall below High |
| `M3-F02` | `VC:H` coupled to the listing's contents, which were never fully enumerated | Could move either way; the backup's presence is what makes it Critical |

> **A provisional rating is an incomplete measurement, not a conservative one.**
> Two of the three could become worse.

---

## 6. Retest-driven re-rating

Any retest that changes a metric input requires a re-rating, not an adjustment.

| Trigger | Affected | Action |
| --- | --- | --- |
| Document reachable with no session | `M1-F03` | `PR:N`, recompute, re-band |
| Rule-based mutation recovers additional keys | `M2-F01` | Confidence and scope updated; vector likely unchanged |
| `/old/` contents found to be non-sensitive | `M3-F02` | Reconsider `VC` and the band — **after** the backup is still remediated |
| Third-party retrieval of the backup confirmed | `M3-F03` | Confidence raised; vector unchanged; notification scope widens |
| Safe demonstration of write capability via the injection | `M1-F02` | `VI:H` becomes evidenced rather than inferred |

---

## 7. Consistency rules

| Rule | Reason |
| --- | --- |
| One vector per finding, repeated identically in every document | Divergent copies are how ratings become untrustworthy |
| Vectors live in the finding record, this file and the register | Any reader can cross-check |
| A vector never changes without a note explaining which metric moved | Ratings are auditable |
| Severity bands are never raised to match a score, or vice versa | They measure different things |
| A `Provisional` flag is cleared only by evidence | Not by re-reading the existing reasoning |

Enforcement: [`../scripts/repo_checks.py`](../scripts/repo_checks.py) validates
that every vector in this file matches the finding records and the register.