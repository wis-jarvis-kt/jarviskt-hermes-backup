#!/usr/bin/env python3
"""
Option A: Google Gemini Imagen (Nano Banana) backend
Uses google-genai SDK with the Imagen 3 model.
Requires: GOOGLE_API_KEY in env or cfg
"""

import os
import sys
import base64


def make_google_image(cfg: dict, output_path: str):
    api_key = os.environ.get("GOOGLE_API_KEY") or cfg.get("api_key")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not set. "
            "Get one free at https://aistudio.google.com/apikey\n"
            "Then run: echo 'GOOGLE_API_KEY=YOUR_KEY' >> ~/.openclaw/.env"
        )

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    prompt = cfg.get("prompt", cfg.get("title", ""))
    model  = cfg.get("model", "imagen-3.0-generate-002")

    # Aspect ratio: map width/height to nearest supported ratio
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

    n = cfg.get("n", 1)

    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=n,
            aspect_ratio=aspect,
            output_mime_type="image/png",
        )
    )

    # Save first image
    img_data = response.generated_images[0].image.image_bytes
    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"[google/imagen] Saved: {output_path}")

    # If multiple images requested, save extras with index suffix
    if n > 1:
        base, ext = output_path.rsplit(".", 1)
        for i, gi in enumerate(response.generated_images[1:], start=2):
            extra_path = f"{base}_{i}.{ext}"
            with open(extra_path, "wb") as f:
                f.write(gi.image.image_bytes)
            print(f"[google/imagen] Saved: {extra_path}")


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="/tmp/google_image.png")
    args = parser.parse_args()
    cfg = json.loads(args.config) if args.config.strip().startswith("{") else json.load(open(args.config))
    make_google_image(cfg, args.output)
    print(args.output)
