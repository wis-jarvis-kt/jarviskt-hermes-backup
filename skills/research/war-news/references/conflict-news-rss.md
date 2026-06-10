# Conflict News RSS Sources — Verified 2026-05-27, updated 2026-06-10

## BBC World News Feeds
| Section | URL |
|---------|-----|
| World (top) | `https://feeds.bbci.co.uk/news/world/rss.xml` |
| Europe | `https://feeds.bbci.co.uk/news/world/europe/rss.xml` |
| Middle East | `https://feeds.bbci.co.uk/news/world/middle_east/rss.xml` |
| Asia | `https://feeds.bbci.co.uk/news/world/asia/rss.xml` |
| US & Canada | `https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml` |
| Africa | `https://feeds.bbci.co.uk/news/world/africa/rss.xml` |
| Latin America | `https://feeds.bbci.co.uk/news/world/latin_america/rss.xml` |

**Usage:**
```bash
# All world headlines
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml" | grep -A 3 "<item>" | head -30

# Filter by keyword across feeds
curl -s "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml" | grep -iE "iran|israel|lebanon"

# Multi-feed aggregate (Ukraine + Middle East + Asia)
for feed in world/europe world/middle_east world/asia; do
  curl -s "https://feeds.bbci.co.uk/news/$feed/rss.xml" | grep -A 2 "<item>"
done
```

## Browser Navigation Over RSS (Preferred — 2026-06-10)

BBC RSS provides only top-level `<title>` + `<description>` per item — no article body. Sufficient for a news radar, but full detail requires browser navigation. Use browser section pages as the primary method:

```
https://www.bbc.com/news/world/europe       → Ukraine/Russia headlines
https://www.bbc.com/news/world/middle_east  → Israel, Iran, Gaza
https://www.bbc.com/news/world/asia         → South China Sea, Taiwan (less frequent)
https://www.bbc.com/news/us-canada          → US policy, Iran strikes
```

**Workflow:** Navigate directly to section URL → snapshot gives lead headlines → extract article URLs via JS → navigate directly to articles. This is more reliable than clicking refs from a listing page (refs often fail with "Could not compute box model").

**Tested:** 2026-05-30 and 2026-06-10 — all section URLs loaded cleanly with no anti-bot blocking.

## ISW as Primary Supplement for Middle East (2026-06-10)

ISW's `iran-update-special-report-YYYY-MM-DD` at `understandingwar.org/research/middle-east/` provides in-depth military-strategic coverage of the Hormuz conflict that BBC lacks. ISW is fully accessible with no bot detection. Use it to supplement BBC when covering:
- US-Iran military exchanges and base strikes
- IRGC operational details and capabilities
- Ceasefire monitoring and violations
- Regional axis-of-resistance activity (Hezbollah, Yemen Houthi, Iraqi militias)

**ISW report URL pattern:** `https://understandingwar.org/research/middle-east/iran-update-special-report-<date>/`

## CNBC Feeds
| Feed | URL |
|------|-----|
| US Top News | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114` |
| Full Site | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664` |

**Usage:**
```bash
curl -s "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114" | grep -A 3 "<item>" | head -40
```

## Conflict-Watch Filtering Patterns
```bash
# Ukraine/Russia keywords
grep -iE "ukraine|russia|kyiv|moscow|zelensky|putin|donbas|crimea"

# Middle East keywords
grep -iE "iran|israel|gaza|hamas|lebanon|hezbollah|netanyahu|ceasefire|hormuz"

# South China Sea / Taiwan keywords
grep -iE "taiwan|south china sea|paracel|scarborough|pla|beijing|strait|taipei"

# General conflict/military
grep -iE "strike|attack|war|ceasefire|missile|drone|invasion|troop"
```

## Notes
- BBC RSS provides only top-level `<title>` + `<description>` per item — no article body. Sufficient for a news radar/summary. Full article detail requires browser navigation.
- BBC section pages via browser_navigate give the same top-level summary without needing RSS — use when RSS feels heavyweight or is unavailable.
- CNBC RSS includes wire-service stories with more context on US policy dimensions (Iran strikes, Hormuz closures, tech/sanctions).
- BBC RSS and BBC section pages via browser both returned 200 OK with zero anti-bot challenges in cron job context (2026-05-27, 2026-05-30, 2026-06-10).
- Google News RSS (`news.google.com/rss/search?q=...`) returns empty `<item>` lists in cron jobs — use BBC/Google News browser nav instead.
- Wikipedia article feeds are not useful for live conflict news.