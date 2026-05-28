---
name: openclaw-imports
version: 1.1.0
description: |
  Skills migrated from OpenClaw on 2026-05-20. Several reference a `gbrain` MCP
  server not yet reconnected in Hermes — see `references/gbrain-mcp-setup.md`.
  Active skills live under `openclaw/` subdirectories; archived duplicates live
  under `.archive/openclaw-imports/`.
triggers:
  - any openclaw-imported skill loaded
  - gbrain brain enrichment brain-first lookup
  - OpenClaw workspace migration
---

# OpenClaw Imports — Umbrella Skill

Skills migrated from OpenClaw on 2026-05-20. Several reference a `gbrain` MCP
server not yet reconnected in Hermes.

## Active Skills (in openclaw/ subdirectories)

| Skill | Status | Notes |
|-------|--------|-------|
| `openclaw-imports` | active | This umbrella — index of all migrated skills |
| `stock-analysis-victor-framework` | active | Victor's P/E vs 5Y avg + Fear & Greed investing framework; supersedes archived `stock-ai-agent` |

## Archived Skills (in .archive/openclaw-imports/)

These skills were consolidated here — their content lives under this umbrella.

| Archived Skill | Was Absorbed Into | Reason |
|---------------|-------------------|--------|
| `deal-hunter` | `openclaw-imports` | Identical content to `openclaw/deal-hunter` — kept canonical copy |
| `hla-annual-stmt` | `openclaw-imports` | Identical content to `openclaw/hla-annual-stmt` — kept canonical copy |
| `imagegen` | `openclaw-imports` | Identical content to `openclaw/imagegen` — kept canonical copy |
| `remind` | kept in `openclaw/` | v1.2.0 in openclaw/ (newer than v1.1.0 in import); archived the import copy |
| `stock-ai-agent` | `openclaw-imports` | Two near-identical copies; canonical is `openclaw/stock-ai-agent` |
| `gbrain-brain-ops` | `openclaw-imports` | gbrain MCP is disconnected; kept `openclaw/gbrain-brain-ops` (has conventions/) |
| `gbrain-enrich` | `openclaw-imports` | gbrain MCP is disconnected; kept `openclaw/gbrain-enrich` (has conventions/) |
| `gbrain-signal-detector` | `openclaw-imports` | gbrain MCP is disconnected; kept `openclaw/gbrain-signal-detector` |
| `annual-statement-retrieval` | `openclaw-imports` | Older version of hla-annual-stmt workflow — archived |
| `book-downloader` | `openclaw-imports` | Standalone utility — archived as narrow-but-valid |
| `consolidate-memory` | `openclaw-imports` | Standalone utility — archived as narrow-but-valid |
| `instagram-extractor` | `openclaw-imports` | Standalone utility — archived as narrow-but-valid |
| `research-scout` | `research/research-scout` | Active skill — archived duplicate; canonical is `research/research-scout` |

## Key Gap: gbrain MCP Server

Three skills (`gbrain-brain-ops`, `gbrain-enrich`, `gbrain-signal-detector`) were designed
to run against a `gbrain` MCP server that is not currently connected. The skills are fully
documented and non-breaking — they simply won't execute until the MCP is reconfigured.
This is a known limitation with no urgent action required.
See `references/gbrain-mcp-setup.md` for reconnection steps if ever needed.

## Umbrella Files

- `references/gbrain-mcp-setup.md` — MCP server setup reference, missing convention files, reconnection steps

## Conventions (2026-05-25)

Convention files created to resolve broken references in gbrain skills (live in
`openclaw/gbrain-brain-ops/conventions/` and `openclaw/gbrain-enrich/conventions/`):

- `openclaw/gbrain-brain-ops/conventions/brain-first.md` — 5-step brain-first lookup protocol
- `openclaw/gbrain-brain-ops/conventions/quality.md` — citation and back-link formatting rules
- `openclaw/gbrain-enrich/conventions/brain-filing-rules.md` — notability gates and entity filing rules

Recreated as functional stubs since original `~/.openclaw/workspace/skills/conventions/`
content was not preserved during migration.
