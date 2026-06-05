# Conflict News — Source Outlet Notes (Updated 2026-06-05)

## Outlet Accessibility Matrix

| Outlet | Direct Nav | Via Google News | Notes |
|--------|-----------|-----------------|-------|
| BBC News | ✅ | N/A | Most reliable; no anti-bot on section pages |
| Al Jazeera | ✅ | ✅ | Good for Middle East; accessible directly |
| Institute for the Study of War | ✅ | N/A | **Go-to fallback for China/Taiwan** when other outlets blocked; substantive, no bot detection |
| The Diplomat | ⚠️ Cloudflare | ⚠️ Cloudflare | Cloudflare challenge page blocks direct nav; Google News headline extraction works |
| US Naval Institute | ✅ | N/A | Defence/strategy; useful for Taiwan Strait analysis |
| Taipei Times | ✅ | ✅ | Taiwan and South China Sea; reliable |
| Reuters | ❌ DataDome | ⚠️ sometimes works | DataDome device-check iframe (different block from Cloudflare); use Google News signposting |
| SCMP | ⚠️ 404s common | ⚠️ mixed | Many article URLs return 404; don't rely on SCMP for breaking news |
| U.S. News & World Report | ⚠️ protocol error | ✅ works | `net::ERR_HTTP2_PROTOCOL_ERROR` on direct nav; Google News extraction of headline + byline works |
| NPR | ✅ | ✅ | Alternative for US-policy dimension |

## Google News Search URLs (Verified 2026-06-05)

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
3. Look for known-good outlets appearing in results: **Taipei Times, The Diplomat, USNI News, ISW, Al Jazeera**
4. If a Reuters or U.S. News result is the only fresh item, extract headline + byline and skip direct nav; note it in the report
5. For Taipei Times articles, use the direct URL pattern: `https://www.taipeitimes.com/News/taiwan/archives/YYYY/MM/DD/NumericID`
6. **ISW** (`understandingwar.org`) is a reliable, fully accessible source for China/Taiwan updates — use when other outlets are blocked

## BBC Asia Limitation

BBC Asia section page rarely carries Taiwan Strait or South China Sea breaking news. It covers: China, India, Japan, Korea, Southeast Asia broadly. Taiwan and SCS stories appear on BBC World Europe or World pages only when US/Western policy is involved. Always supplement with Google News search for Taiwan/SCS.

## Blocking Mechanism Reference

Three distinct mechanisms observed:

| Mechanism | Outlets | Symptom |
|-----------|---------|---------|
| DataDome iframe (device-check) | Reuters | Navigation appears to load, then blocked; iframe overlay |
| Cloudflare challenge | The Diplomat | "Just a moment..." page with security verification |
| HTTP/2 protocol error | U.S. News | `net::ERR_HTTP2_PROTOCOL_ERROR` — different from bot detection, direct nav fails |
| 404 on article pages | SCMP | URLs return 404; not a bot block but article unavailability |
