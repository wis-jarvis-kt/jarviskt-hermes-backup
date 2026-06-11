# War News — Session Observations Log

Chronological record of verified technical findings from cron job runs. Migrated from SKILL.md session observations to keep the skill file clean.

---

## 2026-06-11 (Today)

- **USNI News confirmed accessible** via Google News search results. The query `south+china+sea+taiwan+strait+2026` surfaced USNI as a source for "Chinese Flotilla Surges East of Taiwan" — direct nav confirmed working.
- **ISW "Jump to" combobox confirmed** — all three ISW theater reports (China/Taiwan, Russia/Ukraine, Middle East/Iran) have a "Jump to" dropdown with sections: Toplines, Key Takeaways, [region subsections]. The combobox is an efficient navigation tool on ISW pages.
- **BBC Europe URL `cy73dr081p8o`** confirmed as the article about Indian sailors killed in US tanker strike — appeared in both Europe and Middle East sections simultaneously (Gulf of Oman is geographically Asia/Oceania but news categorization varies).
- **BBC article overlap across sections** — the same article (e.g. tanker strike) can appear in multiple BBC section pages. Deduplicate by article ID when merging lists from Europe + Middle East + Asia.
- **ISW Russia/Ukraine reports confirmed** — `russian-offensive-campaign-assessment-YYYY-MM-DD` URL pattern confirmed working. The Toplines section at the top of the article body is the quick-read; the full text follows below. The report structure was confirmed across three consecutive days (June 8, 9, 10).

---

## 2026-06-10

- ISW homepage navigation confirmed: ISW TEAMS section with region cards (CHINA & TAIWAN, RUSSIA & UKRAINE, MIDDLE EAST) is the primary homepage entry point. From any listing page, extract `research/` URLs via JS (`Array.from(document.querySelectorAll('a[href*="/research/"]')).map(a => a.href).filter(...)`), then navigate directly to the full report. The homepage click lands on a listing page, not the full report.
- ISW Middle East same-day supplement: `iran-update-special-report-YYYY-MM-DD` at `understandingwar.org/research/middle-east/` confirmed as go-to for Hormuz conflict depth.
- Google News result display confirmed: Each result shows source name + relative time (e.g. "ISW — 4 days ago", "Reuters — 5 days ago") directly inline above the headline. No need to click "More" for source/recency. Headlines and bylines fully visible without expansion.
- BBC article URL slug vs. heading mismatch confirmed: URL slug does not always match visible headline. JS URL extraction is correct method — don't infer URLs from headline text.
- All prior anti-bot patterns (Reuters/DataDome, SCMP/404, The Diplomat/Cloudflare, U.S. News/protocol error) remain confirmed active.

---

## 2026-06-08

- Google News JS URL extraction: `Array.from(document.querySelectorAll('a[href*="/news/articles/"]')).map(a => a.href).filter((v,i,a) => a.indexOf(v) === i)` confirmed reliable pattern for both BBC section pages and Google News search results. Deduplicates with `indexOf` trick. Working on both.
- ISW China/Taiwan full report URL format: `understandingwar.org/research/china-taiwan/china-taiwan-update-<date>/` confirmed. "Toplines" section at top is the quick-read.

---

## 2026-06-07

- ISW URL `www.` prefix confirmed broken; bare `understandingwar.org` is correct.
- ISW "Toplines" section confirmed as primary quick-read on full report pages — jump to it first.
- Iran ceasefire stall confirmed: US requested changes to terms; Iran said US keeps "changing its views and putting forward new or contradictory demands."
- New diplomatic exception: US granted visas to Iran's World Cup football team (Los Angeles, June 15) despite active strikes — first such host-nation exception.
- Taipei Times URL inference still risky; correct IDs must be extracted from Google News snippets. Inferred URL `…/2000106928` returned 404 on 2026-06-07.

---

## 2026-06-05

- ISW (Institute for the Study of War) confirmed fully accessible — no bot detection, substantive China/Taiwan analysis. Elevated to go-to fallback for SCS/Taiwan.
- The Diplomat: Cloudflare challenge page confirmed active (bot detection, not DataDome). Different mitigation path — use Google News signposting.
- U.S. News direct nav: `net::ERR_HTTP2_PROTOCOL_ERROR` — different failure from DataDome/Cloudflare. Google News headline + byline extraction works fine.
- Reuters DataDome confirmed distinct block mechanism from Cloudflare; distinguish in anti-bot notes.

---

## 2026-06-04

- Google News JS href extraction (the `WYjbwe` class) remains unreliable — verified still broken.
- Reuters DataDome block confirmed still active.
- SCMP 404s confirmed still active.
