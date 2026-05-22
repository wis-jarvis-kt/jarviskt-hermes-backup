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
| `gbrain-brain-ops` | **aspirational** | MCP not connected — see `references/gbrain-mcp-setup.md` |
| `gbrain-enrich` | **aspirational** | MCP not connected — see `references/gbrain-mcp-setup.md` |
| `gbrain-signal-detector` | **aspirational** | MCP not connected — see `references/gbrain-mcp-setup.md` |
| `hla-annual-stmt` | active | HLA Life Insurance statements |
| `imagegen` | active | image generation for social media/news |
| `instagram-extractor` | active | Instagram content extraction |
| `remind` | active | reminder management |
| `research-scout` | active | AI/tech research scout |
| `stock-ai-agent` | active | fundamentals-based stock investing analysis |

## Key Gap: gbrain MCP Server

Three skills (`gbrain-brain-ops`, `gbrain-enrich`, `gbrain-signal-detector`) were
designed to run against a `gbrain` MCP server that is not currently connected. The
skill files have been patched to note this, but they cannot execute until the MCP
is reconfigured. See `references/gbrain-mcp-setup.md` for setup instructions.

## Umbrella Files

- `references/gbrain-mcp-setup.md` — MCP server setup reference, missing convention files, reconnection steps