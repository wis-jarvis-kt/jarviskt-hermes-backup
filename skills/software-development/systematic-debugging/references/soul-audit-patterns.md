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
