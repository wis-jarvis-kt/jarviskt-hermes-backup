# Drive Search Reference

## Default search: fullText contains (content, not filenames)

```bash
GAPI="python3 ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI drive search "quarterly report"
```

Wraps query as: `fullText contains 'quarterly report'`

**What it searches**: File content (Docs body text, Sheets cell values, PDF text, etc.) — NOT filenames.

**What it returns**: Files whose *content* matches the query.

## Filename search: use --raw-query with name contains

```bash
$GAPI drive search --raw-query "name contains 'quarterly'" --max 10
```

**What it searches**: Filenames only.

## Quick decision guide

| You want... | Use |
|-------------|-----|
| Find a file by its name | `--raw-query "name contains '...'"` |
| Find a file by content inside it | Default (fullText contains) |
| Find spreadsheets with specific data | Default (searches cell values) |
| Find a document you named "Q4 Report" | `--raw-query "name contains 'Q4 Report'"` |

## Gotchas

- `fullText` does NOT include folder names — only file content.
- Drive's `name contains` is case-insensitive.
- Shared drives files may require `--raw-query "visibility='anyone'"` or additional filters.
- If `--raw-query` returns 400 "Invalid Value", the query syntax is wrong — check quotes and escaping.