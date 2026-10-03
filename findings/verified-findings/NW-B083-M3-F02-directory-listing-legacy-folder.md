# NW-B083-M3-F02 — Directory listing enabled on a legacy web root

| Field | Value |
| --- | --- |
| **Finding ID** | `NW-B083-M3-F02` |
| **Milestone** | M3 — Deep Reconnaissance / Critical Data Exposure |
| **Affected component** | `https://medirozahospital.com/old/` |
| **Severity** | 🔴 **Critical** |
| **Rating status** | **Provisional** |
| **Verification status** | Documented |
| **Confidence** | High |
| **OWASP category** | A05 — Security Misconfiguration |
| **CWE** | CWE-548 — Exposure of Information Through Directory Listing |
| **Evidence IDs** | `NW-B083-M3-E03` |
| **Status** | Open |

---

## 1. Description

The legacy path `/old/` disclosed at M1 was reachable and served an automatic
directory listing. Requesting the path returned an index of its contents with file
sizes and modification dates, providing both a location and an inventory. Within that
listing lay a database backup, giving rise to `NW-B083-M3-F03`.

---

## 2. Affected component

| Field | Value |
| --- | --- |
| Location | `/old/` |
| Type | Legacy web root, `apache`/`2.4.58` |
| Authentication to reach it | **None** |
| Disclosed by | `robots.txt` at **M1 Step 1** — and independently by `LAB-PDF-03`'s metadata |
| Contents | A directory index containing at least one database backup |

---

## 3. Preconditions

| # | Precondition | Present in this engagement? |
| --- | --- | --- |
| 1 | Knowledge of the path | ✅ Public in `robots.txt` — no discovery required |
| 2 | Network access to the host | ✅ Yes |
| 3 | Any credential | ❌ **Not required** |

> **The path cost nothing.** An unauthenticated party reading `robots.txt` — the
> very first request of the engagement — obtained everything needed to reach this
> directory.

---

## 4. Technical evidence

### 4.1 Observation

```bash
curl -skI https://medirozahospital.com/old/
```

| Header | Value |
| --- | --- |
| `HTTP` | `301 Moved Permanently` |
| `Location` | `https://medirozahospital.com:443/old/` |

| Evidence ID | Observation | Artifact |
| --- | --- | --- |
| `NW-B083-M3-E03` | Redirect to `/old/` | ❌ Not attached |

On following the redirect, the server returned an **automatic index of the
directory's contents**.

### 4.2 Expected vs. observed

| | Expected | Observed |
| --- | --- | --- |
| **Existence of the path** | Unknown, or absent | Confirmed, and advertised in `robots.txt` |
| **Response** | 403/404, or an application route | `301` → automatic directory listing |
| **Server signature** | Minimised or absent | `Server: Apache/2.4.58` disclosed |

### 4.3 Mechanism

Directory listing is a web server feature enabled when no index file is present in
a directory. Where it is active, the server renders the directory's contents with
sizes and timestamps. It requires no application involvement and no vulnerability —
it is a configuration default left switched on.

The useful property of a listing, to an attacker, is that it removes the need to
guess. Every filename becomes known at once.

**Probable root cause:**

| Probable cause | Confidence | To confirm |
| --- | --- | --- |
| `Options Indexes` enabled globally rather than denied per-directory | High — listing returned | Review the Apache configuration |
| Legacy path retained after migration and never decommissioned | High — corroborated by the metadata note in `NW-B083-M3-F01` | Review the migration process |
| Content under the legacy path not subject to the same review as current paths | Medium | Compare review coverage across paths |
| Backup file placed inside a web-served directory | Medium | Follows from the above — **the more serious defect** |

> **Two configuration weaknesses, one directory.** The listing is the visible
> symptom; the reachable backup is the substantive issue. Both are recorded
> separately, and fixing only the listing would leave the backup reachable if its
> filename were guessed or indexed elsewhere.

---

## 5. Reproduction summary

> Authorized training environment only. **One** request to establish reachability.
> The backup was **not** downloaded under this finding — that is `NW-B083-M3-F03`'s
> evidence.

| Step | Action | Observed result |
| --- | --- | --- |
| 1 | `curl -skI https://medirozahospital.com/old/` | `301` → `https://medirozahospital.com:443/old/` |
| 2 | Follow the redirect | Automatic directory listing returned |

| Bound | Limit |
| --- | --- |
| Requests required | 1–2 |
| Authentication required | None |
| Side effects | **None.** No file retrieved or modified |

**Explicitly not performed:**

| Action | Reason |
| --- | --- |
| Downloading the backup here | Recorded under `NW-B083-M3-F03`, which is where it belongs |
| Crawling or recursing the directory | Single directory only |
| Enumerating sibling legacy paths | Out of scope; a single request established the control weakness |
| Brute-forcing filenames | The listing removed any need to guess |
| Extended historical review of the migration | Documented as the probable cause |

---

## 6. Security impact

| Dimension | Assessment |
| --- | --- |
| Confidentiality | **Severe.** An index of a legacy directory, including a database backup, disclosed without authentication |
| Integrity | None directly |
| Availability | None |
| Data sensitivity | Depends entirely on the listing's contents — here, 🔴 because they included a database backup |
| Business consequence | Unauthenticated inventory of infrastructure that should not exist post-migration; direct enabler of the engagement's only 100% confirmed data exposure |
| Detection likelihood | **Low.** A single unauthenticated request; only detectable if web-request logging is monitored |

### 6.1 Cross-finding effect

| Relationship | Detail |
| --- | --- |
| **Enabled by** `NW-B083-M3-F01` | The metadata note named `/old/`, confirming it as a location to check |
| **Corroborated by** `NW-B083-M1-F01` | `robots.txt` disclosed the same path at the very first step of the engagement |
| **Enabled** `NW-B083-M3-F03` | The listing identified the backup file |
| **Fixing it does not fix** `NW-B083-M3-F03` | A backup inside a web root is a defect whether or not a listing is displayed |

> **A convergence worth recording.** Two independent weaknesses — a public
> `robots.txt` entry at M1 and a metadata comment at M3 — pointed at the same path.
> Neither alone would have been notable. Together they made the path unavoidable.

---

## 7. Severity

| Attribute | Value |
| --- | --- |
| Band | 🔴 **Critical** |
| Rationale | Unauthenticated information disclosure that exposed a legacy directory inventory including a database backup. Critical rather than High because the disclosure is what made the subsequent Critical data exposure reachable without any guessing. |
| Confidence | High that the listing was served; **medium** on the band's precision, because the rating depends on what else the directory holds |
| Rating status | **Provisional** |
| Provisional reason | The listing's full contents are not enumerated in the record. The rating assumes the contents are equivalent in sensitivity to the backup already identified. A directory containing further sensitive material would raise the impact; a directory containing nothing sensitive would lower it — **though in that case this finding would not warrant Critical and the backup must be moved regardless.** |

### 7.1 The honest caveat

**Directory listing on its own is rarely Critical.** It is normally Medium or High:
an index of filenames, with no content disclosed. This finding is rated Critical
because of what the index contained.

| Condition | Appropriate rating |
| --- | --- |
| Listing exposes only static assets | 🟠 Medium |
| Listing exposes a database backup | 🔴 Critical |

The rating is therefore **coupled to the directory's contents**, which is why it is
provisional. If a reviewer reads this finding in isolation without `NW-B083-M3-F03`,
a Medium rating is defensible. That disagreement is recorded rather than resolved by
choosing the more dramatic number.

---

## 8. CVSS v4.0

**Vector (provisional):** `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N`

**Base score:** `PENDING — compute with the FIRST CVSS v4.0 calculator`

| Metric | Value | Justification | Certainty |
| --- | --- | --- | --- |
| AV | `N` | Single unauthenticated HTTP request | Certain |
| AC | `L` | No conditions; the path was already known | Certain |
| AT | `N` | No deployment prerequisite | Certain |
| PR | `N` | No authentication required | Certain |
| UI | `N` | No human must act | Certain |
| VC | `H` | Filenames, sizes and dates of a legacy directory were disclosed, **including a database backup**. `H` is assigned because of the backup's presence, not because a directory index is inherently high-impact | ⚠️ **Provisional** — depends on directory contents |
| VI | `N` | Listing is read-only; nothing was modified | Certain |
| VA | `N` | No availability effect | Certain |
| SC | `N` | No subsequent system affected by the listing itself | Certain |
| SI | `N` | — | Certain |
| SA | `N` | — | Certain |

> **What the vector does not capture.** The listing discloses *filenames*, not
> content. `VC:H` therefore rests on the sensitivity of the filenames and the
> knowledge they grant — not on bulk data exposure, which belongs to
> `NW-B083-M3-F03`. Rating both findings at `VC:H` for the same backup would be
> double-counting. Here the impact is *knowledge of the target*; there it is *the
> data itself*.

---

## 9. Remediation

### 9.1 Primary fix

| # | Action | Priority |
| --- | --- | --- |
| 1 | **Remove the backup from every web-served path.** Disable listing and move the file | **P0** |
| 2 | **Decommission the legacy path.** If `/old/` is retired, delete it and its contents | **P0** |
| 3 | **Deny indexing explicitly** — `Options -Indexes` — at every level, not only where it was noticed | **P0** |
| 4 | Serve only through an allow-listed set of document roots; deny everything else by default | P1 |
| 5 | Remove `Server` and version tokens: `ServerTokens Prod`, `ServerSignature Off` | P2 |

```apache
# Deny indexing globally — set at the top, not per-directory
<Directory />
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>

ServerTokens Prod
ServerSignature Off
```

> `Require all granted` above is shown only to illustrate the directive context.
> In production, deny by default and allow specific paths explicitly.

### 9.2 Process controls — the part that actually prevents recurrence

| # | Control | Addresses |
| --- | --- | --- |
| 1 | Ban backups, dumps and exports inside any web-served directory | The root cause |
| 2 | Make backup storage a separate, non-public destination by design | Prevents by architecture |
| 3 | Add a CI check that fails on large or binary files under web roots | Detects automatically |
| 4 | Require decommissioning sign-off after a migration | `/old/` is a migration artefact |
| 5 | Review every legacy path, not just the disclosed one | Only one path was checked |
| 6 | Retain an inventory of intended public paths | Detects drift |
| 7 | Monitor 4xx/3xx responses for probing of non-existent paths | Detection |

> **Point 7 deserves emphasis.** `/old/` was disclosed in `robots.txt`, and the
> request drew no attention that the record notes. A retired path returning `200`
> or `301` instead of `404` is a cheap, high-signal check.

---

## 10. Retest criteria

| # | Criterion | Method | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | Legacy path removed | Request `/old/` | `404` |
| 2 | No listing anywhere | Request each known directory path | No directory index rendered |
| 3 | Indexing denied by configuration | Review server configuration | `Options -Indexes` set at the top level |
| 4 | **No backups under web roots** | Search all web-served paths for dumps, `.sql`, `.bak`, archives | **Zero matches** |
| 5 | Deny by default | Attempt access outside intended paths | `403` or `404` |
| 6 | No version disclosure | Request any path | No `Apache/2.4.58` in headers |
| 7 | `robots.txt` reviewed | Review its contents | Contains no sensitive or retired paths |
| 8 | CI check in place | Push a test backup file to a web root | Build fails |
| 9 | Migration sign-off process | Review process documentation | Decommissioning is a tracked step |

> **Criterion 4 is the one that matters.** Criteria 1–3 can all pass while a backup
> remains reachable at a filename nobody has guessed yet.

---

## 11. Status

| Field | Value |
| --- | --- |
| Status | **Open — P0** |
| Verification status | **Documented** |
| Rating status | **Provisional** — `VC` coupled to directory contents |
| Evidence artifacts attached | 0 of 1 |
| Outstanding to close | 1. Capture and sanitise `E03`. 2. **Remove the backup from the web root and confirm with a search, not a spot check.** 3. Enumerate the full directory contents to finalise `VC`. 4. Confirm whether other legacy paths exist. 5. Decide whether a reclassification to Medium is appropriate once contents are known. |

---

## 12. Confidentiality declaration

- [x] No credential present
- [x] **No backup content reproduced** — not part of this finding
- [x] Directory listing screenshot **not published**; filenames withheld
- [x] Individual referenced by role, not by name
- [x] Root cause stated as probable — no server or configuration access
- [x] No automation or recursive crawler provided
- [x] No client approval or sign-off claimed