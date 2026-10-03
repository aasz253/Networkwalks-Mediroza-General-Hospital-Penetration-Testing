# Changelog

All notable changes to this documentation repository are recorded here.

This project follows a documentation-oriented variant of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning tracks
**documentation maturity**, not software features — and critically, it does
**not** track engagement findings, because no finding is verified yet.

## [Unreleased]

### Added
- Initial public repository structure for Networkwalks B083 — Mediroza General
  Hospital Penetration Testing (Week 4 final project).
- Engagement governance documentation: project overview, authorization and scope,
  rules of engagement, methodology, testing timeline, tools and technologies,
  ethical considerations, glossary.
- M1 Initial Access milestone documentation: reconnaissance, attack-surface
  inventory, vulnerability analysis, proof-of-concept standard.
- M2 Data Extraction / File Security milestone documentation for the three
  project-supplied PDF test files (`LAB-PDF-01` … `LAB-PDF-03`).
- M3 Critical Data Exposure milestone documentation covering the reported staff
  salary and shareholder information exposure, with redaction standards.
- M4 Final Report milestone documentation: executive summary, scope and
  methodology, technical findings, risk assessment, remediation plan, conclusion,
  appendices.
- Reusable methodology procedures: reconnaissance, web application testing,
  authentication assessment, input validation, file security, access control,
  reporting.
- Risk framework: CVSS v4.0-based rating methodology, scoring policy, and CSV
  risk register.
- Evidence management system: ID scheme `NW-B083-<MS>-E<nn>`, CSV evidence
  register, sensitivity / redaction / verification status fields, evidence
  handling policy.
- Templates: extended vulnerability report, single remediation action, full
  remediation plan, daily progress log, evidence caption, evidence register
  skeleton, plus `templates/README.md` stating the rules that apply to all of
  them.
- Seven extended finding records under `findings/verified-findings/` — three
  Critical, two High, two Medium — each with preconditions, negative controls,
  explicit non-performance, probable root cause, CVSS v4.0 vector and retest
  criteria.
- `findings/README.md` register defining the Confirmed / Provisional / UNKNOWN /
  HYPOTHESIS rating-status model.
- Mermaid diagram sources under `diagrams/`: attack chain, evidence workflow and
  the severity-versus-priority rating model.
- Standalone report deliverables: consolidated technical report, two-page
  management summary, and a 39-action remediation tracker.
- Python utilities (standard library only): `evidence_sanitizer.py` for
  defensive, non-destructive sanitization of text-based evidence, and
  `repo_checks.py` for documentation quality assurance.
- Synthetic sample evidence file for demonstrating the sanitizer without using
  client data.
- GitHub Actions documentation-quality workflow (offline; link, CSV, evidence
  and secret-pattern checks).
- GitHub issue templates for finding-record updates and documentation tasks,
  both of which block the publication of client data in the issue body.
- Repository hardening: `.gitignore` with client-data exclusion patterns,
  `.env.example` with dummy values only, `SECURITY.md` incident process,
  `CONTRIBUTING.md`, `LICENSE` with engagement-specific notices.

### Documentation integrity
- Seven findings are recorded: four Confirmed and three Provisional. Confirmed
  means the core rating inputs are evidenced; Provisional means a metric input is
  inferred, and the inference is named in the record.
- Every finding has verification status `Documented`. Nothing is claimed as
  verified, because zero evidence artifacts are published. The
  `evidence/screenshots/` directories contain manifests, not images.
- No exploitation result, credential, recovered document key, file content,
  patient record, salary figure, shareholder record or database row is present
  anywhere in the repository.
- No CVSS base score is published. Vectors are derived with metric-by-metric
  justification, and scoring is deferred to the official FIRST v4.0 calculator.
- Root causes are labelled probable throughout: no source or infrastructure
  access was available.
- All example content is machine-generated and labelled
  `SYNTHETIC — NOT CLIENT DATA`.
- `python3 scripts/evidence_sanitizer.py --self-test` and
  `python3 scripts/repo_checks.py` both exit 0.

### Known gaps carried forward
- Batch identity: the source record says B082, the project brief says B083. The
  repository uses `NW-B083` and records the discrepancy rather than resolving it.
- No client review, risk acceptance, sign-off, remediation owner or target date
  exists; all such fields read `UNASSIGNED` or `PENDING`.

## [0.1.0] — Structure baseline

### Added
- Directory skeleton for `docs/`, `milestones/`, `findings/`, `evidence/`,
  `reports/`, `methodology/`, `risk/`, `diagrams/`, `scripts/`, `templates/`
  and `.github/`.
- Milestone tracking tables with explicit status markers.

### Notes
- This release represents documentation structure only. It asserts no
  engagement results.

[Unreleased]: https://github.com/aasz253/Networkwalks-Mediroza-General-Hospital-Penetration-Testing/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/aasz253/Networkwalks-Mediroza-General-Hospital-Penetration-Testing/releases/tag/v0.1.0
