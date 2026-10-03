# Diagrams

Mermaid `.mmd` sources for the figures used across the report set.

| Source | Figures |
| --- | --- |
| [`attack-chain.mmd`](./attack-chain.mmd) | Global attack chain across M1–M3 |
| [`evidence-workflow.mmd`](./evidence-workflow.mmd) | Evidence handling and publication decision |
| [`severity-model.mmd`](./severity-model.mmd) | Rating hierarchy and remediation priority mapping |

Rendered diagrams are embedded inline in the Markdown rather than committed as
image files. See [`../evidence/README.md`](../evidence/README.md) §5 for why no
rasterised artifacts are tracked.

---

## Conventions

| Rule | Reason |
| --- | --- |
| Mermaid source only, no committed PNG or SVG | Keeps the repository free of binary artifacts that may embed text |
| No client data, no credential, no personal identifier | Diagrams are the easiest place for an unredacted value to slip through |
| Node labels carry class and count, never values | Same rule as every other table in this repository |
| One diagram per `.mmd` file | Keeps diffs reviewable |
| Filenames describe content, not finding IDs | A filename is often the first thing copied out of context |

---

## Rendering locally

```bash
npx --yes @mermaid-js/mermaid-cli \
  -i diagrams/attack-chain.mmd \
  -o /tmp/attack-chain.svg
```

Rendering is optional and is never part of the quality gate: the committed sources
are the authoritative form, and a failure to render is a tooling issue, not a
documentation defect.

---

## What these diagrams deliberately do not show

| Omitted | Reason |
| --- | --- |
| Real request payloads | Publishing a working payload against a named target is out of scope |
| Server versions, hostnames or internal paths | Unnecessary disclosure and possible misdirection |
| Database schema details | Recorded as class and column count only |
| Any recovered value | Nothing recovered may be reproduced |