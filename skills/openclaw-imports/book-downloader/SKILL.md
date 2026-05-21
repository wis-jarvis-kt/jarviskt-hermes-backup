# book-downloader Skill

Find and download ebooks (EPUB/PDF) from the internet using the `books.py` script.

## When to Use
Use this skill when the user asks to:
- Download a book, ebook, or PDF
- Find a book online
- Search for an epub or pdf of a title
- Get a specific book for free

## Script Location
`scripts/books.py` (relative to this skill's directory)

Full path: `~/.openclaw/workspace/skills/book-downloader/scripts/books.py`

## Sources (in priority order)
1. **OceanOfPDF** — good for newer/popular books, always search first
2. **Anna's Archive** — huge catalogue, great epub coverage
3. **LibGen** — academic and older titles, very reliable
4. **Z-Library** — broad coverage
5. **PDFDrive** — PDF-only
6. **Telegram** — public channels (libgen_scihub, epubcenter, etc.)
7. **Web (DDG)** — extended search via `--web` flag

## Usage

### Basic — search and show results
```bash
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title"
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --author "author name"
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --format epub
```

### Auto-download best result (non-interactive)
```bash
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --pick 1
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --author "author name" --format epub --pick 1
```

### Specific source only
```bash
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --source oceanofpdf
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --source anna
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --source libgen
```

### Extended web search (DDG dorking)
```bash
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "book title" --web
```

## Default Behavior (agent-driven downloads)

When the user asks to download a specific book:

1. Run with `--pick 1` to auto-select the best result (non-interactive)
2. Prefer `--format epub` unless the user specifies PDF
3. If the first attempt fails or returns nothing, retry with `--source anna` then `--source libgen`
4. Files are saved to `~/Downloads/Books/`
5. After download, send the file to the user via WhatsApp

### Example agent flow
```bash
# Step 1: Try OceanOfPDF first (best for newer books)
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "Atomic Habits" --author "James Clear" --format epub --source oceanofpdf --pick 1

# Step 2: If that fails, try Anna's Archive
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "Atomic Habits" --author "James Clear" --format epub --source anna --pick 1

# Step 3: Fall back to LibGen
python3 ~/.openclaw/workspace/skills/book-downloader/scripts/books.py "Atomic Habits" --author "James Clear" --format epub --pick 1
```

## Sending the File to the User

After a successful download, send via WhatsApp using exec:
```bash
openclaw message send --channel whatsapp --to "+60173333550" --file "~/Downloads/Books/FILENAME.epub"
```

Or for the current chat, use the `message` tool with the file path.

## Flags Reference
| Flag | Description |
|------|-------------|
| `--author` / `-a` | Author name |
| `--format` / `-f` | `epub` or `pdf` (default: any) |
| `--pick N` | Auto-pick result N (1-based), non-interactive |
| `--source` | Search specific source only |
| `--web` | Enable DDG web search (slower, wider) |
| `--free-only` | Skip paid purchase links |
| `--no-verify` | Skip post-download verification |
| `--tor` | Route all requests through Tor |
| `--test-mirrors` | Test mirror reachability first |

## Notes
- Downloads are saved to `~/Downloads/Books/`
- The script auto-installs required Python packages (requests, beautifulsoup4, lxml, PyPDF2)
- File verification catches fake/corrupt downloads (HTML error pages, stubs)
- For books not found anywhere, the script offers paid fallbacks (Amazon, Google Play)
- OceanOfPDF is the best source for recent bestsellers; Anna's Archive for older/academic titles
