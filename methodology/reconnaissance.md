# Procedure 1 — Reconnaissance

How public-facing discovery was performed, and what was deliberately not done.

> **Authorisation precondition.** Passive and low-impact discovery of an in-scope
> target under written authorisation. Discovery of paths is in scope; discovery of
> *other people's* data is not.

---

## 1. Objective

Establish the smallest useful map of the target: what is publicly discoverable,
which entry points exist, and which of them deserve attention first.

---

## 2. Order of work

| # | Step | Action | Output |
| --- | --- | --- | --- |
| 1 | Confirm scope in writing | Target, permitted techniques, timing | Recorded scope |
| 2 | Review disclosure files | `robots.txt`, `sitemap.xml`, security-related headers | Candidate paths |
| 3 | Normalise and classify findings | Group by function, not by URL | Attack-surface inventory |
| 4 | Rank entry points | Which unauthenticated surfaces exist? | Test order |
| 5 | Record negatives | What was found not to exist | Coverage record |
| 6 | Note what was **not** done | Scope boundaries and judgement calls | Limitations register |

> Step 5 matters. "We looked and found nothing" is a result. Without it, an
> unreviewed surface is indistinguishable from an absent one.

---

## 3. Disclosure files

`robots.txt` is authored by someone who knows the application. Its directives
describe paths that exist.

### 3.1 What the engagement found

| Directive type | Observation |
| --- | --- |
| `Disallow` entries | Three application paths disclosed |
| Named directories | A patient area, a staff area, and a legacy-looking path |
| Cross-reference | One path later proved to contain a database backup |

> The legacy-looking path was recorded on Day 1, not acted upon, and only became
> material in M3. **Reconnaissance compounds; a disclosure set aside is not
> discarded, it is deferred.**

### 3.2 Handling rules

| Rule | Reason |
| --- | --- |
| Treat `Disallow` as *information*, not as permission | It is not access control |
| Never treat it as a prohibition | It is not a control either — it is documentation |
| Record exact directives | Needed for the report's traceability |
| Do not report "weak robots.txt" as a finding | A `robots.txt` exists to guide crawlers; hiding paths in it is not a defect |
| Report the *consequences* instead | The finding is what the disclosed path leads to, not its existence |

> The engagement reported no finding for the `robots.txt` content itself. The
> findings were the authentication bypass, the exposed documents and the reachable
> backup — all of which it merely pointed toward.

### 3.3 Response headers

| Header | Handling |
| --- | --- |
| `Server` and version | Recorded as an observation. Version disclosure alone is not a finding; it assists the error-based inference in `M1-F02` |
| Cookie attributes | Noted for the authentication assessment |
| Security headers | Recorded as an observation for the hardening backlog |
| Anything identifying infrastructure | Recorded; **internal hostnames are redacted** from any published artifact |

---

## 4. Passive techniques used

| Technique | Purpose |
| --- | --- |
| Disclosure-file review | Path discovery |
| Manual navigation | Functional understanding |
| Response-header inspection | Technology inference |
| Reading application error output | Stack identification — the injection was confirmed from a returned error rather than by fingerprinting |

**Not used:** search-engine querying for the target, certificate-transparency
mining, DNS enumeration, third-party breach databases, or any source of data about
the organisation obtained from outside the authorisation. Where such sources are
used in other engagements, that use must be stated explicitly in scope.

---

## 5. Active techniques deliberately excluded

| Excluded | Reason |
| --- | --- |
| Port or host scanning | Off-target risk; unnecessary for the objective |
| Vulnerability scanners | Noise, unbounded requests, no manual correlation |
| Directory brute-forcing | Listing and disclosure files provided the paths |
| Crawlers on non-public areas | Scope boundary |
| Subdomain enumeration | No requirement; not authorised in this engagement |

---

## 6. Recording format

Each recon observation gets an evidence ID and a one-line description.

```
NW-B083-M1-E01 · M1 · Step 1 · robots.txt returned three path disclosures
```

| Field | Requirement |
| --- | --- |
| Neutral description | "Directory listing served", not "attacker got everything" |
| Linked finding | Finding ID, or `n/a` for pure observations |
| Data class | Whether the artifact would contain sensitive data once captured |

Full register: [`../evidence/evidence-register.csv`](../evidence/evidence-register.csv)

---

## 7. Common mistakes

| Mistake | Consequence | Practice used here |
| --- | --- | --- |
| Treating discovery as a phase that ends | Missed the deferred legacy path | Re-check deferred items each milestone |
| Not recording untested surfaces | False impression of coverage | Negative and untested results logged |
| Assuming a disclosed path is safe | It led to the Critical findings | Every path assessed on its own merits |
| Over-collecting during recon | Unnecessary handling risk | Discovery stopped at paths and headers |
| Reporting disclosure files as findings | Inflated severity count | Consequences reported, not the file |

---

## 8. Engagement application

| Output | Where recorded |
| --- | --- |
| Disclosure-file review | [`../milestones/M1-initial-access/reconnaissance.md`](../milestones/M1-initial-access/reconnaissance.md) |
| Path inventory and ranking | [`../milestones/M1-initial-access/attack-surface.md`](../milestones/M1-initial-access/attack-surface.md) |
| Deferred-item tracking | [`../milestones/M1-initial-access/vulnerability-analysis.md`](../milestones/M1-initial-access/vulnerability-analysis.md) |
| Reuse of the M1 recon in M3 | [`../milestones/M3-critical-data-exposure/exposure-analysis.md`](../milestones/M3-critical-data-exposure/exposure-analysis.md) |

---

## 9. Checklist

- [ ] Written authorisation recorded before any active step
- [ ] Disclosure files reviewed and exact directives recorded
- [ ] Response headers inspected; identifying values redacted
- [ ] Entry points ranked, unauthenticated surfaces first
- [ ] Negative results recorded
- [ ] Deferred items logged for later review, not discarded
- [ ] Excluded techniques and the reason for exclusion documented
- [ ] Each observation given an evidence ID