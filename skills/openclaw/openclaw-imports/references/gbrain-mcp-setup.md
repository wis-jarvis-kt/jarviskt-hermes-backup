# gbrain MCP Server — Setup Reference

## What Is gbrain?

The `gbrain` MCP server powered the brain knowledge base in the original OpenClaw
workspace. It provides structured tools for:

- `gbrain search` / `gbrain query` — keyword and hybrid vector search
- `gbrain get_page` / `gbrain put_page` — read/write brain pages
- `gbrain add_link` / `gbrain add_timeline_entry` — graph operations
- `gbrain get_backlinks` — check who references an entity
- `gbrain sync_brain` — sync changes to the index

## Skills Affected by the Gap

These migrated skills reference `gbrain` tools or non-existent conventions files.
Until the MCP is reconnected, they are **aspirational** — they document correct
behavior but will not execute successfully:

| Skill | Broken References |
|-------|-------------------|
| `gbrain-brain-ops` | `skills/conventions/brain-first.md`, `skills/conventions/quality.md` |
| `gbrain-enrich` | `skills/_brain-filing-rules.md` |
| `gbrain-signal-detector` | (assumed same — ambient signal was gbrain-triggered) |

## Missing Convention Files

These files were referenced in the original OpenClaw workspace but were not migrated
or recreated in Hermes:

| File | Referenced By | Original Purpose |
|------|---------------|------------------|
| `skills/conventions/brain-first.md` | gbrain-brain-ops | 5-step brain-first lookup protocol |
| `skills/conventions/quality.md` | gbrain-brain-ops, gbrain-enrich | Citation and back-link formatting rules |
| `skills/_brain-filing-rules.md` | gbrain-enrich | Notability gates, entity filing rules |

## How to Reconnect gbrain

### Step 1: Obtain gbrain MCP Server Details

The gbrain MCP server was hosted as part of the OpenClaw setup. Check:
- Original OpenClaw config at `~/.openclaw/.env` for MCP URL/credentials
- Any `mcpServers` section in `~/.openclaw/workspace/` config files
- The archived workspace at `~/.openclaw/workspace/skills/conventions/` for convention file content

### Step 2: Register the MCP Server

In `~/.hermes/config.yaml`, configure under `mcp:`:
```yaml
mcp:
  provider: auto   # or specific provider
  model: ''        # leave blank unless forced
  base_url: ''     # gbrain MCP server URL
  api_key: ''      # if auth required
  timeout: 30
  extra_body: {}
```

Or use the CLI: `hermes mcp add gbrain <server-url>`

### Step 3: Recreate Convention Files

Obtain from the original OpenClaw workspace at `~/.openclaw/workspace/skills/conventions/`:
- Copy `brain-first.md` → `~/.hermes/skills/conventions/brain-first.md`
- Copy `quality.md` → `~/.hermes/skills/conventions/quality.md`

For `_brain-filing-rules.md`, check `~/.openclaw/workspace/skills/` directory.

### Step 4: Verify

Load any gbrain skill and confirm `gbrain` tool calls return actual data instead
of errors.

## Status History

- **2026-05-20:** OpenClaw → Hermes migration. gbrain MCP NOT reconnected.
- **2026-05-21:** Skills patched with aspirational notes. Setup reference created.