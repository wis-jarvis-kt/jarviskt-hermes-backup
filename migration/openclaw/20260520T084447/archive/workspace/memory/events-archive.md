# Events Archive — Archived from MEMORY.md to reduce file size

## 2026-03-31 (Tuesday)
- Master KT had packed day: XP closes meet (10AM), follow-up with Leng Kah (11AM), Calvin Kong (2:30PM), Roy dinner (6PM)
- Roy Phay dinner/discussion happened (this is the same Roy Phay whose webinar KT analysed)
- Google OAuth token for jarvisktgoo@gmail.com expired — alerted KT, fixed 2026-04-01
- WhatsApp creds.json loop active all day (every ~60s disconnect/reconnect) — ongoing
- War briefing (Middle East/Ukraine/China) queued at 7PM then delivered once WA reconnected

## 2026-04-01 (Wednesday)
- KT met Nixon at WMC Cafe (9:30 AM)
- **Google OAuth FIXED permanently:** Published "Jarvis Access" OAuth app (project: jarvis-access-488903) to Production in Google Cloud Console. Re-authed jarvisktgoo@gmail.com — refresh tokens no longer expire every 7 days. TOOLS.md updated.
- WhatsApp 499 disconnects occurred all day — alerted KT repeatedly (root cause misunderstood as creds.json corruption; clarified 2026-04-02 that 499 = normal keep-alive restart).
- gog gmail + calendar fully operational again after OAuth fix (confirmed 7:18PM)

## 2026-04-02 (Thursday)
- **499 alert rule corrected:** KT clarified that WhatsApp status 499 = normal keep-alive idle restart, NOT creds.json corruption. Wis was wrongly alerting 5+ times. Rule updated: do NOT alert for 499s unless gateway fails to reconnect >5 min. TOOLS.md updated.
- **GitHub "OpenClaw Backup Token" renewed** to no expiration by KT (7:23 AM), after Wis morning alert. GH_TOKEN in .env confirmed working (HTTP 200).
- **Conversion Codex CCS Brain integration COMPLETE** (8:14 PM): brain_content seeded M1-M5 + foundation + campaign, buildSystemPrompt rewritten, Buying Blueprint tracker, 6 integration tables + emit function, LCS trigger handler in wa-webhook.
- **SEMC interviews** (multiple slots) and CY closings scheduled via Google Calendar.
- **HLA policy full pull** for Ganendra A/L Paramasvaran (IC: 810309145801) — 5 policies reviewed, 2 in-force, 1 surrendered, 1 lapsed. Action items: Policy 4 lapsed (needs revival), Policy 5 outstanding RM780.
- **Johan Mohamad** (MHIRA hemp founder) profiled for KT's Expert Elite Mastermind interview.
- Content work: ShuYi AI angle → 3 AHAs for Roy QiMen/BaZi. @sidequesthk Instagram reel analysis (GeoSpy.ai, Turbo.ai).

## 2026-04-03 (Friday)
- Busy afternoon: CY Closing Ng Soo Fien (2PM), CY Closing Jeremy 4pax (2:30PM), Meet Deborah & Wei Zhi (3PM)
- No urgent emails all day.
- Nightly self-improvement run: updated MEMORY.md project timestamp, cleaned Apple ID recovery note, flagged NVIDIA project as unconfirmed, refreshed HEARTBEAT.md backup size note.

## 2026-04-04 (Saturday)
- Calendar: Meeting with Niel (9AM), Meet Ceylyn at house (10:30AM), SEMC Interview Closing — Yip Lye Chun (1PM), CY Closing — Carole 15 pax (2PM)
- No new emails overnight or morning.
- Nightly self-improvement run: fixed FBC group rule date typo (2026-04-06 → 2026-04-03), added April 4 events log, flagged stale Appointment Setting project status.

## 2026-04-13 (Monday)
- **Conversion Codex / test-dashboard export:** KT asked to export test-dashboard code to GitHub. Wis hit `gh repo create --push` issue (no commits detected), then `git push` 404 after repo creation. Status: ⚠️ unresolved — follow up with KT.
- **MEMORY.md size warning:** Bootstrap truncation at ~46%. ⚠️ KT should raise `agents.defaults.bootstrapMaxChars` in openclaw config.
- Geopolitics briefing delivered: US-Iran Hormuz blockade, Ukraine Easter ceasefire collapse, KMT-Xi meeting, Israel-Gaza.
- WhatsApp 499 disconnects throughout day — all normal keep-alive restarts (not alerted per rule).

## 2026-04-14 (Tuesday)
- Nightly self-improvement run: updated current projects timestamp, added test-dashboard unresolved flag, added Anthropic deprecation deadlines.
- Anthropic deprecations flagged: Haiku 3 retires Apr 19, 1M context window retires Apr 30.

## 2026-04-15 (Wednesday)
- Nightly self-improvement run: backed up 6 core files to `self-improve-backups/20260415-010031/`. Removed stale Apple ID recovery note, removed Hume AI free-credit trivia, updated current projects timestamp. Backup 58MB (within limit). ⚠️ Claude Haiku 3 retires Apr 19 (4 days away) — flagged again in WA report.
- **Victor Big Red rules extracted from chat screenshots:** Compiled full Victor trading rules from 3 WhatsApp screenshots (Big Red definition, entry amounts, buy/sell/CALL/PUT rules, Master KT's 4 sell rules). Saved to `investing/VICTOR_RULES.md` as source of truth. Updated MEMORY.md ETF Analysis section with new Big Red Day rules.
