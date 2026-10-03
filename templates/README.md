# Templates

Reusable document formats. Copy, fill, delete what does not apply — but never
delete a section that would otherwise record an absence.

| Template | Use |
| --- | --- |
| [`vulnerability-report-template.md`](./vulnerability-report-template.md) | Extended finding / vulnerability report |
| [`remediation-template.md`](./remediation-template.md) | One remediation action with retest criteria |
| [`remediation-plan-template.md`](./remediation-plan-template.md) | A full remediation plan |
| [`daily-progress-template.md`](./daily-progress-template.md) | Daily engagement log |
| [`screenshot-caption-template.md`](./screenshot-caption-template.md) | Evidence caption and sanitization record |
| [`evidence-register-template.csv`](./evidence-register-template.csv) | Evidence register skeleton |

Related: [`../findings/finding-template.md`](../findings/finding-template.md) is
the compact per-finding structure used inside this repository.

---

## Rules that apply to every template

| Rule | Reason |
| --- | --- |
| Never delete a section to hide an absence | Write `Not tested`, `UNKNOWN` or `PENDING — <what is needed>` |
| Record what was **not** done in every test procedure | Prevents false assurance |
| Confidence and rating status are separate fields | A sound rating can rest on an unevidenced metric |
| Every fix gets an observable retest criterion | "Improves security" is not testable |
| Redaction follows the two-channel standard | Internal report vs public repository differ |
| No score, date, owner or approval is invented | `UNASSIGNED` is an acceptable value; a guess is not |
| Synthetic content is labelled at the point of use | `SYNTHETIC — NOT CLIENT DATA` |

Full policy: [`../methodology/reporting.md`](../methodology/reporting.md)

---

## Placeholder tokens

| Token | Meaning |
| --- | --- |
| `{{ID}}` | Finding or evidence identifier |
| `PENDING` | Required input not available; the exact need must be stated beside it |
| `UNKNOWN` | Not recorded and not inferable |
| `UNASSIGNED` | No owner exists — a real gap, not an oversight |
| `NONE` | Tested, and nothing was found |
| `NOT TESTED` | Deliberately or practically out of the performed set |
| `SYNTHETIC — NOT CLIENT DATA` | Fabricated example content |
| `j.m***` | Masked individual |
| `<REDACTED>` | Value withheld by policy |

> `NONE` and `NOT TESTED` are different claims and must never be used
> interchangeably. The first is a result; the second is a gap.