# Conflict News — Source Outlet Notes (Updated 2026-06-11)

## Outlet Accessibility Matrix

| Outlet | Direct Nav | Via Google News | Notes |
|--------|-----------|-----------------|-------|
| BBC News | ✅ | N/A | Most reliable; no anti-bot on section pages |
| Al Jazeera | ✅ | ✅ | Good for Middle East; accessible directly |
| Institute for the Study of War | ✅ | N/A | **Go-to for China/Taiwan and Middle East**; no bot detection, substantive analysis across all three conflict theaters |
| The Diplomat | ⚠️ Cloudflare | ⚠️ Cloudflare | Cloudflare challenge page blocks direct nav; Google News headline extraction works |
| US Naval Institute | ⚠️ Cloudflare | ⚠️ Cloudflare | Defence/strategy; useful for Taiwan Strait naval activity; confirmed blocked by Cloudflare challenge (2026-06-12); Google News extraction of headline + byline works as fallback |
| Taipei Times | ✅ | ✅ | Taiwan and South China Sea; reliable |
| Reuters | ❌ DataDome | ⚠️ sometimes works | DataDome device-check iframe (different block from Cloudflare); use Google News signposting |
| SCMP | ⚠️ 404s common | ⚠️ mixed | Many article URLs return 404; don't rely on SCMP for breaking news |
| U.S. News & World Report | ⚠️ protocol error | ✅ works | `net::ERR_HTTP2_PROTOCOL_ERROR` on direct nav; Google News extraction of headline + byline works |
| NPR | ✅ | ✅ | Alternative for US-policy dimension |

## Google News Search URLs (Verified 2026-06-10)

```
Taiwan + South China Sea:
https://news.google.com/search?q=south+china+sea+taiwan+strait+2026&hl=en-US&gl=US&ceid=US:en

China SCS patrols specifically:
https://news.google.com/search?q=china+patrols+south+china+sea+disputed+2026&hl=en-US&gl=US&ceid=US:en
```

## Finding Taiwanese / SCS Articles via Google News

When BBC Asia is thin on Taiwan/SCS coverage (which is frequent):

1. Navigate to the Google News search URL above
2. Scan the visible headline list — don't rely on JS-based href extraction (WYjbwe class is unreliable)
3. Each result shows source name + relative time (e.g. "ISW — 4 days ago", "Reuters — 5 days ago") directly inline, above the headline. No need to click "More" for source/recency. Headlines and bylines are fully visible without expansion.
4. Look for known-good outlets appearing in results: **Taipei Times, The Diplomat, USNI News, ISW, Al Jazeera**
5. If a Reuters or U.S. News result is the only fresh item, extract headline + byline and skip direct nav; note it in the report
6. For Taipei Times articles, use the direct URL pattern: `https://www.taipeitimes.com/News/taiwan/archives/YYYY/MM/DD/NumericID`
7. **ISW** (`understandingwar.org`) is a reliable, fully accessible source for China/Taiwan updates — use when other outlets are blocked

## BBC Asia Limitation

BBC Asia section page rarely carries Taiwan Strait or South China Sea breaking news. It covers: China, India, Japan, Korea, Southeast Asia broadly. Taiwan and SCS stories appear on BBC World Europe or World pages only when US/Western policy is involved. Always supplement with Google News search for Taiwan/SCS.

## ISW URL Navigation (Updated 2026-06-10)

ISW uses two distinct URL patterns for its reports:

- **Summary page** (from homepage listing click): `https://understandingwar.org/backgrounder/china-taiwan/update-june-5-2026`
- **Full report** (direct nav): `https://understandingwar.org/research/china-taiwan/china-taiwan-update-june-5-2026`

**Important:** Do NOT use `www.` prefix. The correct bare domain is `https://understandingwar.org` — adding `www.` produces a broken page.

When you land on a `backgrounder/` URL from a homepage click, you have a summary card — not the full analysis. Navigate to the `research/` path for the complete report text. This applies to China/Taiwan, Russia/Ukraine, and Middle East ISW reports.

**ISW page structure:** On the full report page, the "Toplines" section is the most important quick-read section — it summarizes the 3–5 most critical developments. Jump to it first via the combobox dropdown if available, or scroll to the top of the article body.

**ISW homepage navigation (2026-06-11 confirmed):** The ISW homepage has an "ISW TEAMS" section with clickable region cards (e.g. "RUSSIA & UKRAINE", "MIDDLE EAST", "CHINA & TAIWAN"). Clicking a region card lands on a listing page — not a full report. Extract `research/` URLs via JS before navigating:

```javascript
Array.from(document.querySelectorAll('a[href*="/research/"]'))
  .map(a => a.href)
  .filter(h => h.match(/understandingwar\.org\/research\/[^/]+\/[^/]+\//))
```

**ISW Middle East reports (2026-06-10):** ISW publishes `iran-update-special-report-YYYY-MM-DD` at `understandingwar.org/research/middle-east/`. These are the go-to supplement for Hormuz/Iran conflict coverage when BBC is thin on military-strategic detail. Same navigation pattern — extract `research/` URL and navigate directly.

**ISW report URL patterns (Updated 2026-06-12):**
- China/Taiwan: `understandingwar.org/research/china-taiwan/china-taiwan-update-<month-name>-<day>-<year>/`
  - Example: `china-taiwan-update-june-5-2026` ✅ — month name format
  - Example: `china-taiwan-update-2026-06-05` ❌ — YYYY-MM-DD format 404s
- Russia/Ukraine: `understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-<month-name>-<day>-<year>/`
- Middle East/Iran: `understandingwar.org/research/middle-east/iran-update-special-report-<month-name>-<day>-<year>/`

## Blocking Mechanism Reference

| Mechanism | Outlets | Symptom |
|-----------|---------|---------|
| DataDome iframe (device-check) | Reuters | Navigation appears to load, then blocked; iframe overlay |
| Cloudflare challenge | The Diplomat | "Just a moment..." page with security verification |
| HTTP/2 protocol error | U.S. News | `net::ERR_HTTP2_PROTOCOL_ERROR` — different from bot detection, direct nav fails |
| 404 on article pages | SCMP | URLs return 404; not a bot block but article unavailability |