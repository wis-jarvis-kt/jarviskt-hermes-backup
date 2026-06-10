---
name: apple-notes
description: "Manage Apple Notes via native Notes.app scripting: create, search, edit. (memo CLI is deprecated — do not use)"
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Notes, Apple, macOS, note-taking]
    related_skills: [obsidian]
prerequisites:
  commands: [osascript]
---

# Apple Notes

Use native macOS Notes.app scripting via `osascript` to manage Apple Notes. Notes sync across all Apple devices via iCloud.

## IMPORTANT — memo CLI is DEPRECATED

The `memo` Homebrew package (antoniorodr/memo) was **deprecated and disabled on 2025-07-27** — it is no longer maintained upstream and is not installed on this system. **Do not attempt to use `memo`** in any workflow. All `memo` references in skills and documentation should be updated to use `osascript` with Notes.app instead.

## How to Use Notes.app via osascript

### View Notes

```bash
osascript -e 'tell application "Notes" to name of every folder'
osascript -e 'tell application "Notes" to name of every note'
```

### Create a Note

```bash
osascript -e 'tell application "Notes" to tell account "iCloud" to make new note at folder "Notes" with properties {name:"Title", body:"Content"}'
```

### Search Notes

```bash
osascript -e 'tell application "Notes" to id of every note whose body contains "query"'
```

### Edit/Delete Notes

Use Notes.app UI automation via System Events or direct Notes.app scripting. For interactive editing, bring Notes to front:
```bash
osascript -e 'tell application "Notes" to activate'
```

## When to Use

- User asks to create, view, or search Apple Notes
- Saving information to Notes.app for cross-device access
- Organizing notes into folders
- Exporting notes to text/markdown

## When NOT to Use

- Obsidian vault management → use the `obsidian` skill
- Bear Notes → separate app (not supported here)
- Quick agent-only notes → use the `memory` tool instead
- Complex note editing or formatting → Notes.app is limited; consider Obsidian for rich Markdown

## Limitations

- Cannot edit notes containing images or attachments reliably
- No native export command — use clipboard or third-party tools for full export
- macOS only — requires Apple Notes.app with iCloud sync
- Notes.app scripting is basic; for advanced operations consider AppleScriptGUI or Keyboard Maestro
