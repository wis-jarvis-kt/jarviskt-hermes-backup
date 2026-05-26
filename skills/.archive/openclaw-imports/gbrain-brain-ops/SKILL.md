---
name: brain-ops
version: 1.0.0
description: |
  Brain knowledge base operations. The core read/write cycle: brain-first lookup,
  read-enrich-write loop, source attribution, ambient enrichment, back-linking.
  Read this before any brain interaction.
triggers:
  - any brain read/write/lookup/citation
tools:
  - search
  - query
  - get_page
  - put_page
  - add_link
  - add_timeline_entry
  - get_backlinks
  - sync_brain
mutating: true
---

# Brain Operations — The Ambient Context Layer

The brain is not an archive. It is a live context membrane that every interaction
flows through in both directions.

> **Note:** `skills/conventions/brain-first.md` and `skills/conventions/quality.md`
> referenced in this skill were part of the original OpenClaw brain system. The brain
> MCP server (`gbrain`) is not currently connected — these conventions are aspirational
> until the MCP is reconfigured.

## Contract

This skill guarantees:
- Brain is checked BEFORE any external API call (brain-first lookup)
- Every inbound signal triggers the READ → ENRICH → WRITE loop
- Every outbound response checks brain for relevant context
- Source attribution on every fact written (inline `[Source: ...]` citations)
- User's direct statements are highest-authority data
- Back-links maintained on every brain write (Iron Law)

## Iron Law: Back-Linking (MANDATORY)

Every mention of a person or company with a brain page MUST create a back-link
FROM that entity's page TO the page mentioning them. An unlinked mention is a
broken brain.
*(Note: The `skills/conventions/quality.md` formatting rule referenced here was part
of the original OpenClaw brain system — aspirational until gbrain MCP is reconfigured.)*

## Phases

### Phase 1: Brain-First Lookup (MANDATORY)

Before using ANY external API to research a person, company, or topic:

1. `gbrain search "name"` — keyword search for existing pages
2. `gbrain query "natural question about name"` — hybrid search for context
3. `gbrain get <slug>` — if you know the slug, read the full page
4. Check backlinks: who references this entity?
5. Check timeline: recent events involving this entity

The brain almost always has something. External APIs fill gaps, not start from scratch.

### Phase 2: On Every Inbound Signal (READ → ENRICH → WRITE)

Every message, meeting, email, or conversation that references a person or company:

1. **Detect entities** — people, companies, deals mentioned
2. **Load brain pages** — read existing pages for context before responding
3. **Identify new information** — what does this signal tell us that the page doesn't know?
4. **Write it back** — update the brain page with new info + timeline entry + source citation
5. **Create if missing** — if notable and no page exists, create via enrich skill

**User's direct statements are the highest-value data source.** Write them to brain
pages immediately with attribution `[Source: User, YYYY-MM-DD]`.

### Phase 2.5: Structured Graph Updates (automatic)

Every `put_page` call automatically extracts entity references and writes them
to the graph (`links` table) with inferred relationship types. Stale links
(refs no longer in the page text) are removed in the same call. This is
"auto-link" reconciliation.

- No manual `add_link` calls needed for ordinary page writes.
- Inferred link types: `attended` (meeting -> person), `works_at`, `invested_in`,
  `founded`, `advises`, `source` (frontmatter), `mentions` (default).
- The `put_page` MCP response includes `auto_links: { created, removed, errors }`
  so the agent can verify outcomes.
- To disable: `gbrain config set auto_link false`. Default is on.
- Timeline entries with specific dates still need explicit `gbrain timeline-add`
  (or batch via `gbrain extract timeline --source db`).

### Phase 3: On Every Outbound Response (READ → PULL → RESPOND)

Before answering any question about a person, company, or topic:

1. **Check the brain** — read relevant pages
2. **Pull context** — use compiled truth + recent timeline
3. **Respond with context** — the brain makes every answer better

Don't answer from general knowledge when a brain page exists.

### Phase 4: Ambient Enrichment

This is not a special mode. This is the default. Everything the user says is an
ingest event.

- Person mentioned → check brain, create/enrich if needed (spawn background)
- Company mentioned → same
- Link shared → ingest it (delegate to idea-ingest)
- Data shared → delegate to appropriate skill

**Rules:**
- Never interrupt the conversation to do enrichment
- Spawn sub-agents for anything that would slow down the response
- Never announce "I'm enriching the brain" — just do it silently

## Output Format

No separate output. Brain-ops is an always-on behavior layer, not a report generator.
The output is updated brain pages and enriched responses.

## Anti-Patterns

- Answering questions about people/companies without checking the brain first
- Using external APIs before checking the brain
- Writing facts without inline `[Source: ...]` citations
- Blocking the response to do enrichment
- Overwriting user's direct statements with lower-authority sources
- Creating brain pages for non-notable entities

## Tools Used

- `search` — keyword search
- `query` — hybrid vector+keyword search
- `get_page` — read a brain page
- `put_page` — create/update brain pages
- `add_link` — cross-reference entities
- `add_timeline_entry` — record events
- `get_backlinks` — check who references an entity
- `sync_brain` — sync changes to the index
