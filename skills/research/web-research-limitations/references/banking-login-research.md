# Banking Login Research — Anti-Bot Patterns (2026-06-11)

## Core Finding

Banking websites (tested: Hong Leong Bank — hlb.com.my) have extremely aggressive bot detection that makes automated login attempts via browser tools unreliable in a cron job environment.

## What Was Tried (HLB Connect)

| Approach | Result |
|----------|--------|
| Direct URL `/login`, `/hlb-connect/login`, `/user/login`, `/signin` | "Something went wrong" error page — URL routing requires JS |
| Click "Connect" → "PERSONAL / SOLE PROPRIETOR" | Loads HLB Connect **info page**, not a login form |
| Click "Connect" → follow link ref | Same — info page, no login form |
| Navigate to known login URL via browser | Error page (JS-routed, requires real browser session) |
| Google search for login URL | Blocked by CAPTCHA |
| Bing search for login URL | Blocked by CAPTCHA |
| DuckDuckGo search | Blocked by duck CAPTCHA |

## Root Cause

The HLB login is behind JavaScript-based SPA routing. The actual login form loads only when:
1. A real browser session is established
2. The user clicks through the "Connect" dropdown
3. The page renders via client-side JS routing

Direct URL navigation (even to correct-looking paths) returns error pages because the server-side routing doesn't recognize paths that the JS router handles client-side.

## What Works

**Manual browser access only.** The user must open their browser and navigate to:
1. https://www.hlb.com.my
2. Click **Connect** (top-right button)
3. Select **PERSONAL / SOLE PROPRIETOR**
4. The login form loads via JS — this cannot be automated

## Implication for Cron Jobs

Any cron job task that requires "log into my bank" cannot be fulfilled via browser automation. The task must be deferred to manual user action, or the skill owner must accept they need to check their bank manually.

## Pattern for Other Banks

If attempting to automate login for other banks:
- Assume all major bank websites use JS-based SPA routing for login pages
- Assume all have aggressive bot detection without residential proxies
- Assume the "Connect" or "Login" button in nav is the only real entry point — no discoverable login URL
- Do not try to construct login URLs from inspection of the main site — the routing is internal

## Session Context

- Task: "Try logging into Hong Leong Bank now" — reminder cron job
- Environment: macOS, no residential proxy, running as cron job
- Outcome: Failed to access login page; recommended manual browser access