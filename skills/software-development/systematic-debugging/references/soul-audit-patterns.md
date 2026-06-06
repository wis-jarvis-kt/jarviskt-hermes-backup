# Skill Audit Patterns

Reference for performing systematic audits of Hermes config, skills, cron jobs, and memory files.

## When to Audit

- Regular maintenance cron (`hermes-self-improve-2am`) runs this every night
- After any skill migration or large refactor
- When stale entries are suspected

## Audit Order

### 1. Snapshot the live state

From `~/.hermes/memories/MEMORY.md`:
- "Active Cron Workflows" section → job name → skill/file mapping
- "Conventions" section → current directory structure

From `~/.hermes/cron/jobs.json`:
- All recurring jobs + their `last_status`, `next_run_at`
- One-shot jobs with future dates (reminders, trips)

### 2. Audit umbrella/archive skills

Umbrella skills (e.g. `openclaw-imports`) maintain an **archived skills table** listing absorbed/skipped skills. For each entry:

| Field | What to verify |
|-------|---------------|
| "Was Absorbed Into" target | Target skill actually exists under `~/.hermes/skills/` |
| "Reason" | Reason still accurate vs current state |

**Error pattern to catch:** archived entry says "standalone utility — archived" but the skill is actually **active** and running. This happened with `research-scout` — it was listed as archived in `openclaw-imports` but actually runs twice daily at `research/research-scout/`.

**Fix:** Update the archived entry to point to the live canonical location.

### 3. Cross-check cron job skills

A cron job with `skill: null` and an inline prompt is fine if it's a simple script. But if a recurring workflow has a named skill elsewhere, the job should link to it via `skills: ["skill-name"]`.

### 4. Verify gbrain MCP gap stays documented

Skills referencing a disconnected MCP server are fine if they document the gap clearly and won't auto-trigger in normal usage.

## This session's fix

- **File:** `openclaw-imports` archived skills table
- **Entry:** `research-scout` listed as absorbed into `openclaw-imports` as a "standalone utility"
- **Actual:** `research-scout` is an active skill at `research/research-scout/` running 2x/day
- **Fix:** Updated entry → `research/research-scout` (active skill — archived duplicate; canonical is `research/research-scout`)
- **Backup:** `SKILL.md.bak-20260529`

## Audit findings (2026-06-07)

### MEMORY.md — "Skill Locations" section

Two stale entries found and fixed:

1. **`openclaw/stock-analysis-victor-framework` reference was ambiguous**
   - Both the archived wrapper and canonical skill share the `openclaw/` path prefix — naming only the skill name is ambiguous without the full sub-directory path
   - Fix: clarified as `openclaw/openclaw-stock-analysis-victor-framework` (archived) absorbed into `openclaw/stock-analysis-victor-framework` (canonical: Victor Entry Signals + Stock Radar + Weekly Victor Study)
   - **Lesson:** Always use the full sub-directory path in references when two skills share a path prefix.

2. **gbrain MCP note was vague**
   - Previous: "gbrain MCP server skills (3) are aspirational — disconnected since OpenClaw migration"
   - Fix: Named all 3 skills explicitly (gbrain-brain-ops, gbrain-enrich, gbrain-signal-detector) and pointed to `openclaw/openclaw-imports/references/gbrain-mcp-setup.md` for reconnection steps
   - **Lesson:** "N skills are aspirational" without naming them and linking to setup doc leaves future agents unable to identify what to fix.

### SOUL.md and config.yaml

- **SOUL.md:** All paths correct — `~/.hermes/memories/` fix was already applied in a prior session.
- **config.yaml:** No stale references found. `model_catalog` URL, `honcho`, `onboarding` flags all current.

### war-news and web-research-limitations skills

Both fully current with anti-bot patterns verified through 2026-06-06 session. No updates needed.

### Audit pattern confirmed

The audit procedure in this reference file correctly identifies stale entries. Key checks:
- MEMORY.md "Skill Locations" → verify skill paths resolve to actual files
- MEMORY.md "Active Cron Workflows" → verify skill name matches what exists
- Umbrella skill archived tables → verify "absorbed_into" targets exist
- gbrain skills → check they document the MCP gap clearly (not just "aspirational")
