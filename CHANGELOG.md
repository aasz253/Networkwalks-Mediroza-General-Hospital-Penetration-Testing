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
- Templates: vulnerability report, screenshot caption, daily progress log,
  evidence register, remediation plan.
- Python utilities (standard library only): `evidence_sanitizer.py` for
  defensive, non-destructive sanitization of text-based evidence, and
  `repo_checks.py` for documentation quality assurance.
- Synthetic sample evidence file for demonstrating the sanitizer without using
  client data.
- GitHub Actions documentation-quality workflow (offline; link, CSV, evidence
  and secret-pattern checks).
- GitHub issue templates for vulnerability findings and documentation tasks.
- Repository hardening: `.gitignore` with client-data exclusion patterns,
  `.env.example` with dummy values only, `SECURITY.md` incident process,
  `CONTRIBUTING.md`, `LICENSE` with engagement-specific notices.

### Documentation integrity
- All findings are marked `PENDING VERIFICATION`. Zero findings are claimed as
  confirmed.
- No exploitation result, credential, recovered file content, patient record,
  salary figure or shareholder record is claimed anywhere in the repository.
- No CVSS score is published; the rating policy explicitly prohibits scoring
  without evidence.
- `verified-findings/` is intentionally empty and contains only `.gitkeep`.
- All example content is machine-generated and labelled
  `SYNTHETIC — NOT CLIENT DATA`.

## [0.1.0] — Structure baseline

### Added
- Directory skeleton for `docs/`, `milestones/`, `findings/`, `evidence/`,
  `reports/`, `methodology/`, `risk/`, `diagrams/`, `scripts/`, `templates/`
  and `.github/`.
- Milestone tracking tables with explicit status markers.

### Notes
- This release represents documentation structure only. It asserts no
  engagement results.

[Unreleased]: https://github.com/SifunaCodex/networkwalks-b083-mediroza-pentest/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SifunaCodex/networkwalks-b083-mediroza-pentest/releases/tag/v0.1.0
