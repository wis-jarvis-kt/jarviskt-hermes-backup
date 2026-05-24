---
name: openclaw-imports
version: 1.0.0
description: |
  Skills migrated from OpenClaw on 2026-05-20. Several reference a `gbrain` MCP
  server not yet reconnected in Hermes — see `references/gbrain-mcp-setup.md`.
triggers:
  - any openclaw-imported skill loaded
  - gbrain brain enrichment brain-first lookup
  - OpenClaw workspace migration
---

# OpenClaw Imports — Umbrella Skill

Skills migrated from OpenClaw on 2026-05-20. Several reference a `gbrain` MCP
server not yet reconnected in Hermes.

## Migrated Skills

| Skill | Status | Notes |
|-------|--------|-------|
| `annual-statement-retrieval` | active | HLA/insurance statement downloads |
| `book-downloader` | active | book file retrieval |
| `consolidate-memory` | active | memory consolidation workflow |
| `deal-hunter` | active | flight/hotel deal hunting |
| `gbrain-brain-ops` | resolved | Convention references fixed 2026-05-25; conventions created under `conventions/` |
| `gbrain-enrich` | resolved | Convention references fixed 2026-05-25; conventions created under `conventions/` |
| `gbrain-signal-detector` | resolved | MCP remains disconnected; no convention references to fix |
| `hla-annual-stmt` | active | HLA Life Insurance statements |
| `imagegen` | active | image generation for social media/news |
| `instagram-extractor` | active | Instagram content extraction |
| `remind` | active | reminder management |
| `research-scout` | active | AI/tech research scout |
| `stock-ai-agent` | active | fundamentals-based stock investing analysis |

## Key Gap: gbrain MCP Server

Three skills (`gbrain-brain-ops`, `gbrain-enrich`, `gbrain-signal-detector`) were designed to run against a `gbrain` MCP server that is not currently connected. The skills are fully documented and non-breaking — they simply won't execute until the MCP is reconfigured. This is a known limitation with no urgent action required. See `references/gbrain-mcp-setup.md` for reconnection steps if ever needed.

## Umbrella Files

- `references/gbrain-mcp-setup.md` — MCP server setup reference, missing convention files, reconnection steps

## Conventions (2026-05-25)

Convention files created to resolve broken references in gbrain skills:

- `openclaw/gbrain-brain-ops/conventions/brain-first.md` — 5-step brain-first lookup protocol
- `openclaw/gbrain-brain-ops/conventions/quality.md` — citation and back-link formatting rules
- `openclaw/gbrain-enrich/conventions/brain-filing-rules.md` — notability gates and entity filing rules

Recreated as functional stubs since original `~/.openclaw/workspace/skills/conventions/` content was not preserved during migration.