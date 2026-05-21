---
name: imagegen
description: >
  Generate images for social media, news graphics, infographics, or AI art.
  Supports multiple backends: Pillow (local, free, always works), OpenAI DALL-E 3,
  Replicate (FLUX/Stable Diffusion), and FAL.ai. Trigger when Master KT asks to
  create/generate/make an image, graphic, post visual, infographic, or social media card.
metadata:
  openclaw:
    emoji: 🎨
---

# imagegen Skill

Generate images via the `generate_image.py` script. Always use the **pillow** backend
unless Master KT has added an API key for a generative backend.

## Script Location

```
~/.openclaw/skills/imagegen/scripts/generate_image.py
```

Run with:
```bash
python3 ~/.openclaw/skills/imagegen/scripts/generate_image.py \
  --config '<JSON>' \
  --output /path/to/output.png
```

---

## Backend Selection

| Backend      | Requires               | Quality              | Cost         | Use when                              |
|--------------|------------------------|----------------------|--------------|---------------------------------------|
| `pillow`     | Nothing (built-in)     | Styled text graphic  | Free         | Always available — news cards, infographics |
| `google`     | `GOOGLE_API_KEY`       | AI photorealistic    | Free tier + paid | **Option A** — Google Imagen/Nano Banana via AI Studio |
| `nanobanana` | `NANOBANANA_API_KEY`   | AI photorealistic    | ~$0.02/img   | **Option B** — 50% cheaper than Google direct |
| `openai`     | `OPENAI_API_KEY`       | AI photorealistic    | ~$0.04/img   | When KT adds OpenAI key               |
| `replicate`  | `REPLICATE_API_TOKEN`  | AI art (FLUX)        | ~$0.003/img  | When KT adds Replicate key            |
| `fal`        | `FAL_KEY`              | AI art (fast)        | ~$0.003/img  | When KT adds FAL key                  |

### Option A Setup (Google Imagen / Nano Banana) — FREE tier available
1. Go to https://aistudio.google.com/apikey (sign in as jarvisktgoo@gmail.com)
2. Click *Create API key*
3. Copy the key and run:
   ```bash
   echo 'GOOGLE_API_KEY=YOUR_KEY_HERE' >> ~/.openclaw/.env
   ```
4. Use `"backend": "google"` in your config

### Option B Setup (NanoBanana API) — ~$0.02/image, no free tier
1. Sign up at https://nanobananaapi.ai/
2. Get API key from dashboard
3. Add key:
   ```bash
   echo 'NANOBANANA_API_KEY=YOUR_KEY_HERE' >> ~/.openclaw/.env
   ```
4. Use `"backend": "nanobanana"` in your config

---

## Pillow Config Fields

All fields are optional except `output`.

```json
{
  "backend": "pillow",
  "layout": "news",
  "width": 1200,
  "height": 630,
  "bg_color": "#1a1a2e",
  "accent_color": "#e94560",
  "text_color": "#ffffff",
  "tag": "BREAKING",
  "tag_color": "#cc0000",
  "title": "Main headline here",
  "subtitle": "Supporting line",
  "body": "Body paragraph text here...",
  "footer": "Source: Reuters · wis-jarvis",
  "output": "/tmp/image1.png"
}
```

### Layouts
- `news` — left accent bar, tag pill, bold headline (default, best for news)
- `minimal` — centered, clean, good for quotes or announcements

### Color Presets (reference)
| Theme     | bg       | accent   | Use for         |
|-----------|----------|----------|-----------------|
| Dark navy | #1a1a2e  | #e94560  | Breaking news   |
| Deep red  | #1a0000  | #ff4444  | Conflict/war    |
| Dark blue | #0d1b2a  | #4fc3f7  | Politics/diplomacy |
| Black     | #0a0a0a  | #ffd700  | High-impact     |
| Forest    | #0d1f0d  | #66bb6a  | Economy/trade   |

---

## AI Backend Config Fields

```json
{
  "backend": "openai",
  "prompt": "Dramatic news graphic showing ...",
  "size": "1792x1024",
  "output": "/tmp/image1.png"
}
```

```json
{
  "backend": "replicate",
  "model": "black-forest-labs/flux-schnell",
  "prompt": "...",
  "output": "/tmp/image1.png"
}
```

---

## Workflow for Social Media Images

### Step 1 — Plan the images
Decide layout, color scheme, content for each image.

### Step 2 — Build JSON configs
One config per image. Use descriptive filenames.

### Step 3 — Generate
```bash
python3 ~/.openclaw/skills/imagegen/scripts/generate_image.py \
  --config '{"backend":"pillow","layout":"news",...}' \
  --output ~/Desktop/image1.png
```

### Step 4 — Send to Master KT
Use `message` tool or attach file path in reply.

---

## Facebook Post Best Practices

- **Recommended size:** 1200×630px (landscape, link preview ratio)
- **Portrait option:** 1080×1350px (better feed visibility)
- **Text rule:** Keep text under 20% of image area for best reach
- **2-image set:** Image 1 = hook/headline, Image 2 = detail/CTA

---

## Example: 2-Image News Set

```json
[
  {
    "backend": "pillow",
    "layout": "news",
    "width": 1200, "height": 630,
    "bg_color": "#1a0000",
    "accent_color": "#ff4444",
    "text_color": "#ffffff",
    "tag": "BREAKING",
    "tag_color": "#ff0000",
    "title": "Iran Fires Missiles at Tel Aviv",
    "subtitle": "2 killed in Ramat Gan after Larijani assassination",
    "footer": "Middle East Update · Today",
    "output": "/tmp/news_image1.png"
  },
  {
    "backend": "pillow",
    "layout": "news",
    "width": 1200, "height": 630,
    "bg_color": "#0d1b2a",
    "accent_color": "#4fc3f7",
    "text_color": "#ffffff",
    "tag": "WORLD WATCH",
    "title": "4 Fronts. 1 World on Edge.",
    "body": "Iran-Israel · Gaza · Ukraine · China — what you need to know",
    "footer": "Global Briefing · Today",
    "output": "/tmp/news_image2.png"
  }
]
```

---

## Notes
- Output files default to `/tmp/` — move to Desktop or workspace as needed
- Pillow font fallback: uses system fonts (Helvetica on Mac); works without installing extras
- For best results with AI backends, write vivid, specific prompts
