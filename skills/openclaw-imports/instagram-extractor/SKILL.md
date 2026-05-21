---
name: instagram-extractor
description: "Extract image URLs and video from Instagram posts (single, carousel, or Reels) using instaloader and yt-dlp."
tags: ["instagram", "scraper", "video", "reels"]
related_skills: []
---

# instagram-extractor

**Purpose:** Extract image URLs and video from Instagram posts (single, carousel, or Reels) using `instaloader` and `yt-dlp`, then analyze with vision tools.

**Trigger phrases:** "extract Instagram post", "get images from Instagram", "analyze this Instagram post", "read this IG post", "download Instagram reel", "save Instagram video", "extract reel video", "get video from Instagram", "what app is in this Reel", "Mac apps in this video"

**WhatsApp communication:** After completing extraction and analysis, reply with only the identified content — no tool output, no working steps, no frame numbers. E.g. "The Reel featured: Rectangle (rectangleapp.com), TablePlus, and Raycast."

---

## Quick Command (copy-paste ready)

Replace `SHORTCODE` with the part after `/p/` in the URL:

```bash
python3 -c "import instaloader; L = instaloader.Instaloader(); post = instaloader.Post.from_shortcode(L.context, 'SHORTCODE'); [print(f'Slide {i+1}: {n.display_url}') for i, n in enumerate(post.get_sidecar_nodes())]"
```

### Single-image post (no carousel):

```bash
python3 -c "import instaloader; L = instaloader.Instaloader(); post = instaloader.Post.from_shortcode(L.context, 'SHORTCODE'); print(post.url)"
```

### Reels (video) — use yt-dlp (more reliable than instaloader for video):

```bash
yt-dlp -o "/tmp/reel.%(ext)s" "https://www.instagram.com/reel/SHORTCODE/"
```

---

## Full Script

```bash
python3 /Users/ktoclaw/.openclaw/workspace/scripts/instagram_extract.py <URL_or_shortcode>
```

### Examples

```bash
# With full URL
python3 /Users/ktoclaw/.openclaw/workspace/scripts/instagram_extract.py https://www.instagram.com/p/ABC123xyz/

# With shortcode only
python3 /Users/ktoclaw/.openclaw/workspace/scripts/instagram_extract.py ABC123xyz

# Reel video
yt-dlp -o "/tmp/reel.%(ext)s" "https://www.instagram.com/reel/DYdv_bOI_FA/"
```

---

## How to Extract Shortcode from URL

Given: `https://www.instagram.com/p/C9xYzABC123/` or `https://www.instagram.com/reel/DYdv_bOI_FA/`

Shortcode = segment after `/p/` or `/reel/` — e.g. `C9xYzABC123` or `DYdv_bOI_FA`

---

## Step-by-Step Workflow

1. **Get URL** from the user
2. **Extract shortcode** — split on `/p/` or `/reel/`, take next segment, strip trailing `/`
3. **For images:** Run instaloader command to get image URLs
4. **For Reels/video:** Use `yt-dlp` — more reliable than instaloader for video
5. **Extract frames:** For Reels, use `ffmpeg -i video.mp4 -vf "select=eq(n\,0)+eq(n\,30)+..." frame_%03d.png` to get key frames
6. **Analyze:** Pass frame paths to `vision_analyze` tool
7. **Fallback if vision not configured:** Tell user to run `hermes setup` to enable vision

---

## Fallback: imginn.com

If instaloader fails (private account, rate limited, or login required):

```bash
curl -sL "https://imginn.com/p/SHORTCODE/" | grep -oP 'https://[^"]+\.(jpg|png)'
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `LoginRequiredException` | Private account | Use imginn fallback |
| `QueryReturnedNotFoundException` | Post deleted or wrong shortcode | Double-check URL |
| `TooManyRequestsException` | Rate limited by Instagram | Use `yt-dlp` instead (more resilient) or wait 10 min |
| `ImportError: instaloader` | Not installed | `pip3 install instaloader` |
| Video URL returns "URL signature mismatch" | instLoader video URL expired | Use `yt-dlp` instead — it handles URL refresh automatically |

---

## Vision Setup

If `vision_analyze` fails with "No LLM provider configured for task=vision":

```bash
hermes setup
```

Choose a vision-capable provider (MiniMax, OpenAI, etc.) when prompted. After setup, `vision_analyze` will work on downloaded frames.

---

## Notes

- Works for **public posts and Reels** without Instagram login
- `yt-dlp` is more reliable than `instaloader` for Reel video — use it for video content
- Carousel posts return multiple slide URLs (Slide 1, Slide 2, ...)
- instLoader video URLs expire quickly — don't cache them, download immediately
- No Instagram account or credentials needed for public posts
- Both `yt-dlp` and `instaloader` are already installed in this environment