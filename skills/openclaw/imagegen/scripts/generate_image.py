#!/usr/bin/env python3
"""
imagegen - Multi-backend image generator for OpenClaw/Wis
Backends: pillow (local), openai (DALL-E), replicate, fal
Usage: python3 generate_image.py --config config.json
"""

import argparse
import json
import os
import sys
import textwrap
import math
from pathlib import Path

# ─── PILLOW BACKEND ──────────────────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_pillow_image(cfg: dict, output_path: str):
    from PIL import Image, ImageDraw, ImageFont
    import urllib.request

    width  = cfg.get("width", 1200)
    height = cfg.get("height", 630)
    bg     = cfg.get("bg_color", "#1a1a2e")
    accent = cfg.get("accent_color", "#e94560")
    text_color = cfg.get("text_color", "#ffffff")
    title  = cfg.get("title", "")
    subtitle = cfg.get("subtitle", "")
    body   = cfg.get("body", "")
    tag    = cfg.get("tag", "")
    tag_color = cfg.get("tag_color", accent)
    footer = cfg.get("footer", "")
    layout = cfg.get("layout", "news")  # news | split | minimal

    img  = Image.new("RGB", (width, height), hex_to_rgb(bg))
    draw = ImageDraw.Draw(img)

    # ── Try to load fonts (fall back to default) ──
    def get_font(size, bold=False):
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for c in candidates:
            if Path(c).exists():
                try:
                    from PIL import ImageFont
                    return ImageFont.truetype(c, size)
                except:
                    pass
        from PIL import ImageFont
        return ImageFont.load_default()

    # ── Helper: wrapped text ──
    def draw_wrapped(text, x, y, max_width, font, color, line_spacing=1.3):
        if not text:
            return y
        words = text.split()
        lines = []
        current = []
        for w in words:
            test = ' '.join(current + [w])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current.append(w)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [w]
        if current:
            lines.append(' '.join(current))
        for line in lines:
            draw.text((x, y), line, font=font, fill=hex_to_rgb(color))
            bbox = draw.textbbox((0, 0), line, font=font)
            y += int((bbox[3] - bbox[1]) * line_spacing)
        return y

    pad = 60

    if layout == "news":
        # ── Accent bar left ──
        draw.rectangle([(pad, pad), (pad+8, height-pad)], fill=hex_to_rgb(accent))
        x_start = pad + 28

        # ── Tag pill ──
        y = pad
        if tag:
            tag_font = get_font(22, bold=True)
            bbox = draw.textbbox((0, 0), tag.upper(), font=tag_font)
            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
            draw.rectangle([(x_start, y), (x_start+tw+20, y+th+10)],
                           fill=hex_to_rgb(tag_color))
            draw.text((x_start+10, y+5), tag.upper(), font=tag_font,
                      fill=hex_to_rgb("#ffffff"))
            y += th + 24

        # ── Title ──
        title_font = get_font(58, bold=True)
        y = draw_wrapped(title, x_start, y, width - x_start - pad,
                         title_font, text_color, 1.2)
        y += 16

        # ── Subtitle ──
        if subtitle:
            sub_font = get_font(30)
            y = draw_wrapped(subtitle, x_start, y, width - x_start - pad,
                             sub_font, accent, 1.25)
            y += 20

        # ── Body ──
        if body:
            body_font = get_font(26)
            y = draw_wrapped(body, x_start, y, width - x_start - pad,
                             body_font, "#cccccc", 1.4)

        # ── Footer bar ──
        if footer:
            foot_font = get_font(20)
            draw.rectangle([(0, height-50), (width, height)],
                           fill=hex_to_rgb(accent))
            draw.text((pad, height-36), footer, font=foot_font,
                      fill=hex_to_rgb("#ffffff"))

    elif layout == "minimal":
        # Centered, clean
        y = pad * 2
        if tag:
            tag_font = get_font(24, bold=True)
            bbox = draw.textbbox((0,0), tag.upper(), font=tag_font)
            tw = bbox[2]-bbox[0]
            draw.text(((width-tw)//2, y), tag.upper(), font=tag_font,
                      fill=hex_to_rgb(accent))
            y += 50
        title_font = get_font(64, bold=True)
        y = draw_wrapped(title, pad, y, width-pad*2, title_font, text_color, 1.2)
        y += 20
        if body:
            body_font = get_font(28)
            y = draw_wrapped(body, pad, y, width-pad*2, body_font, "#aaaaaa", 1.4)
        if footer:
            foot_font = get_font(22)
            draw.text((pad, height-50), footer, font=foot_font,
                      fill=hex_to_rgb("#666666"))

    img.save(output_path, quality=95)
    print(f"[pillow] Saved: {output_path}")


# ─── GOOGLE IMAGEN / NANO BANANA (Option A) ──────────────────────────────────

def make_google_image(cfg: dict, output_path: str):
    api_key = os.environ.get("GOOGLE_API_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not set.\n"
            "Get one free at https://aistudio.google.com/apikey\n"
            "Then: echo 'GOOGLE_API_KEY=YOUR_KEY' >> ~/.openclaw/.env"
        )
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    prompt = cfg.get("prompt", cfg.get("title", ""))
    model  = cfg.get("model", "gemini-2.5-flash-image")
    n      = cfg.get("n", 1)

    width  = cfg.get("width", 1200)
    height = cfg.get("height", 630)
    ratio  = width / height
    if ratio > 1.6:
        aspect = "16:9"
    elif ratio > 1.2:
        aspect = "4:3"
    elif ratio > 0.9:
        aspect = "1:1"
    elif ratio > 0.6:
        aspect = "3:4"
    else:
        aspect = "9:16"

    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=n,
            aspect_ratio=aspect,
            output_mime_type="image/png",
        )
    )

    img_data = response.generated_images[0].image.image_bytes
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"[google/imagen] Saved: {output_path}")

    if n > 1:
        base, ext = output_path.rsplit(".", 1)
        for i, gi in enumerate(response.generated_images[1:], start=2):
            extra = f"{base}_{i}.{ext}"
            with open(extra, "wb") as f:
                f.write(gi.image.image_bytes)
            print(f"[google/imagen] Saved: {extra}")


# ─── NANOBANANA API (Option B - cheaper 3rd party) ────────────────────────────

def make_nanobanana_image(cfg: dict, output_path: str):
    api_key = os.environ.get("NANOBANANA_API_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError(
            "NANOBANANA_API_KEY not set.\n"
            "Sign up at https://nanobananaapi.ai/ then:\n"
            "echo 'NANOBANANA_API_KEY=YOUR_KEY' >> ~/.openclaw/.env"
        )
    import requests as req
    prompt  = cfg.get("prompt", cfg.get("title", ""))
    model   = cfg.get("model", "nano-banana-2")
    size    = cfg.get("size", "1792x1024")
    quality = cfg.get("quality", "standard")
    n       = cfg.get("n", 1)

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "n": n, "size": size,
               "quality": quality, "response_format": "url"}

    resp = req.post("https://api.nanobananaapi.ai/v1/images/generations",
                    headers=headers, json=payload, timeout=120)
    if not resp.ok:
        raise RuntimeError(f"NanoBanana API error {resp.status_code}: {resp.text}")

    data = resp.json()
    url  = data["data"][0]["url"]
    img  = req.get(url, timeout=60)
    img.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(img.content)
    print(f"[nanobanana] Saved: {output_path}")

    if n > 1:
        base, ext = output_path.rsplit(".", 1)
        for i, item in enumerate(data["data"][1:], start=2):
            extra = f"{base}_{i}.{ext}"
            r = req.get(item["url"], timeout=60)
            with open(extra, "wb") as f:
                f.write(r.content)
            print(f"[nanobanana] Saved: {extra}")


# ─── OPENAI DALL-E BACKEND ────────────────────────────────────────────────────

def make_openai_image(cfg: dict, output_path: str):
    import openai, urllib.request
    api_key = os.environ.get("OPENAI_API_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    prompt = cfg.get("prompt", cfg.get("title", ""))
    size   = cfg.get("size", "1792x1024")
    resp   = client.images.generate(model="dall-e-3", prompt=prompt,
                                    size=size, quality="standard", n=1)
    url    = resp.data[0].url
    urllib.request.urlretrieve(url, output_path)
    print(f"[dall-e] Saved: {output_path}")


# ─── REPLICATE BACKEND ────────────────────────────────────────────────────────

def make_replicate_image(cfg: dict, output_path: str):
    import replicate, urllib.request
    api_key = os.environ.get("REPLICATE_API_TOKEN") or cfg.get("api_key")
    if not api_key:
        raise ValueError("REPLICATE_API_TOKEN not set")
    os.environ["REPLICATE_API_TOKEN"] = api_key
    prompt = cfg.get("prompt", cfg.get("title", ""))
    model  = cfg.get("model", "black-forest-labs/flux-schnell")
    output = replicate.run(model, input={"prompt": prompt})
    url    = output[0] if isinstance(output, list) else output
    urllib.request.urlretrieve(str(url), output_path)
    print(f"[replicate] Saved: {output_path}")


# ─── FAL BACKEND ─────────────────────────────────────────────────────────────

def make_fal_image(cfg: dict, output_path: str):
    import fal_client, urllib.request
    api_key = os.environ.get("FAL_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError("FAL_KEY not set")
    os.environ["FAL_KEY"] = api_key
    prompt  = cfg.get("prompt", cfg.get("title", ""))
    model   = cfg.get("model", "fal-ai/flux/schnell")
    result  = fal_client.submit(model, arguments={"prompt": prompt}).get()
    url     = result["images"][0]["url"]
    urllib.request.urlretrieve(url, output_path)
    print(f"[fal] Saved: {output_path}")


# ─── ROUTER ──────────────────────────────────────────────────────────────────

BACKENDS = {
    "pillow":      make_pillow_image,
    "google":      make_google_image,
    "imagen":      make_google_image,       # alias
    "nanobanana":  make_nanobanana_image,   # Option B
    "openai":      make_openai_image,
    "replicate":   make_replicate_image,
    "fal":         make_fal_image,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="JSON config file or inline JSON")
    parser.add_argument("--output", default=None, help="Output file path (overrides config)")
    args = parser.parse_args()

    # Accept inline JSON or file path
    if args.config.strip().startswith("{"):
        cfg = json.loads(args.config)
    else:
        with open(args.config) as f:
            cfg = json.load(f)

    output = args.output or cfg.get("output", "/tmp/imagegen_output.png")
    backend = cfg.get("backend", "pillow")

    if backend not in BACKENDS:
        print(f"[error] Unknown backend: {backend}. Options: {list(BACKENDS.keys())}", file=sys.stderr)
        sys.exit(1)

    BACKENDS[backend](cfg, output)
    print(output)  # last line = path for shell capture

if __name__ == "__main__":
    main()
