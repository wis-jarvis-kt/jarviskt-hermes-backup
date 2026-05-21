# Hermes Dashboard — Web UI

## Starting the Dashboard

```bash
hermes dashboard              # Default: port 9119, localhost only
hermes dashboard --tui       # Includes embedded chat/TUI (PTY-based chat tab)
hermes dashboard --port 8080 # Custom port
hermes dashboard --host 0.0.0.0 --insecure  # Bind to all interfaces (DANGEROUS)
hermes dashboard --no-open   # Don't auto-open browser
hermes dashboard --stop      # Stop all running dashboard processes
hermes dashboard --status    # List running dashboard processes
```

**Default URL:** `http://localhost:9119`

## What `hermes web` does NOT work

```
hermes: error: argument command: invalid choice: 'web' (choose from 'chat', 'model', ...)
```

There is no `hermes web` subcommand. The web interface is always `hermes dashboard`.

## What the Dashboard Provides

The dashboard is a web UI for managing Hermes configuration and sessions:

- **Sessions** — browse, resume, delete past conversation sessions
- **Chat** — embedded web-based chat (when `--tui` flag is used)
- **Models** — model/provider configuration
- **Logs** — gateway and error logs
- **Cron** — scheduled job management
- **Skills** — skill library management
- **Plugins** — plugin system
- **Profiles** — multi-profile configuration
- **Config** — YAML config editor
- **Keys** — API key/credential management
- **Kanban** — multi-agent work queue board
- **Gateway Status** — active sessions count, restart/update controls

## `--tui` Flag

`--tui` embeds a PTY-based terminal chat experience inside the browser, effectively running a full `hermes` session inside the web page. This is required if you want the **Chat** tab to function.

Without `--tui`, the dashboard is configuration/management only — no chat capability.

## Ports

| Flag | Default |
|------|---------|
| `--port` | 9119 |
| `--host` | 127.0.0.1 |

The port check: `lsof -i :9119` or whatever port was chosen.

## Session Observations (KT's environment)

- Dashboard started successfully on port 9119
- WhatsApp platform was shown as connected (last update 8h ago)
- 46 sessions visible in the session list
- Gateway Status: RUNNING, Active Sessions: 2
- Hermes version: v0.14.0