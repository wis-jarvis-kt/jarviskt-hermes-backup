# Citation and Back-Link Rules

## Inline Citations (MANDATORY)

Every fact must carry an inline `[Source: ...]` citation.

Three formats:
- **Direct attribution:** `[Source: User, {context}, YYYY-MM-DD]`
- **API/external:** `[Source: {provider} enrichment, YYYY-MM-DD]`
- **Synthesis:** `[Source: compiled from {list of sources}]`

## Source Precedence (highest to lowest)

1. User's direct statements
2. Compiled truth (pre-existing brain synthesis)
3. Timeline entries (raw evidence)
4. External sources (API enrichment, web search)

When sources conflict, note the contradiction with both citations.

## Back-Link Format

When writing about a person or company with a brain page:

> "[Entity name]" → link to their page

The back-link FROM the entity's page TO your page should be created using
the `add_link` tool with relationship type `mentions`.