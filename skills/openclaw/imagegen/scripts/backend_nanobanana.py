#!/usr/bin/env python3
"""
Option B: nanobananaapi.ai backend (cheaper third-party wrapper around Google Imagen)
OpenAI-compatible REST API — no SDK needed, just requests.
Requires: NANOBANANA_API_KEY in env or cfg
Sign up at: https://nanobananaapi.ai/
"""

import os
import sys
import json
import requests


NANOBANANA_BASE = "https://api.nanobananaapi.ai/v1"


def make_nanobanana_image(cfg: dict, output_path: str):
    api_key = os.environ.get("NANOBANANA_API_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError(
            "NANOBANANA_API_KEY not set.\n"
            "Sign up at https://nanobananaapi.ai/ and add your key:\n"
            "echo 'NANOBANANA_API_KEY=YOUR_KEY' >> ~/.openclaw/.env"
        )

    prompt  = cfg.get("prompt", cfg.get("title", ""))
    model   = cfg.get("model", "nano-banana-2")   # or: nano-banana-pro, nano-banana
    size    = cfg.get("size", "1792x1024")          # 1024x1024, 1792x1024, 1024x1792
    quality = cfg.get("quality", "standard")        # standard | hd
    n       = cfg.get("n", 1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
        "response_format": "url",
    }

    resp = requests.post(
        f"{NANOBANANA_BASE}/images/generations",
        headers=headers,
        json=payload,
        timeout=120,
    )

    if not resp.ok:
        raise RuntimeError(
            f"NanoBanana API error {resp.status_code}: {resp.text}"
        )

    data = resp.json()
    url  = data["data"][0]["url"]

    img_resp = requests.get(url, timeout=60)
    img_resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(img_resp.content)

    print(f"[nanobanana] Saved: {output_path}")

    # Save extra images if n > 1
    if n > 1:
        base, ext = output_path.rsplit(".", 1)
        for i, item in enumerate(data["data"][1:], start=2):
            extra_path = f"{base}_{i}.{ext}"
            r = requests.get(item["url"], timeout=60)
            with open(extra_path, "wb") as f:
                f.write(r.content)
            print(f"[nanobanana] Saved: {extra_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="/tmp/nanobanana_image.png")
    args = parser.parse_args()
    cfg = json.loads(args.config) if args.config.strip().startswith("{") else json.load(open(args.config))
    make_nanobanana_image(cfg, args.output)
    print(args.output)
