#!/usr/bin/env python3
"""
instagram_extract.py — Extract image URLs from Instagram posts using instaloader.

Works for both single-image posts and carousel/sidecar posts.
Prints each image URL on its own line.

Usage:
  python3 instagram_extract.py https://www.instagram.com/p/ABC123xyz/
  python3 instagram_extract.py ABC123xyz
  python3 instagram_extract.py --shortcode ABC123xyz
"""

import sys
import re
import argparse


def extract_shortcode(input_str: str) -> str:
    """
    Extract the shortcode from an Instagram URL or return as-is if it's already a shortcode.

    URL formats handled:
      https://www.instagram.com/p/ABC123xyz/
      https://www.instagram.com/p/ABC123xyz/?igsh=...
      https://instagram.com/p/ABC123xyz
      instagram.com/p/ABC123xyz/
    """
    # Try to extract from URL pattern /p/{shortcode}
    match = re.search(r"/p/([A-Za-z0-9_-]+)", input_str)
    if match:
        return match.group(1)

    # If no URL pattern found, assume the whole string is a shortcode
    # (shortcodes are typically alphanumeric + _ -)
    cleaned = input_str.strip().rstrip("/")
    if re.match(r"^[A-Za-z0-9_-]+$", cleaned):
        return cleaned

    raise ValueError(f"Cannot extract shortcode from: {input_str!r}")


def get_post_images(shortcode: str) -> list[str]:
    """
    Retrieve all image URLs for an Instagram post.

    For carousel/sidecar posts: returns one URL per slide.
    For single-image posts: returns a single URL.
    Returns list of URLs (strings).
    """
    try:
        import instaloader
    except ImportError:
        raise ImportError(
            "instaloader is not installed. Run: pip3 install instaloader"
        )

    L = instaloader.Instaloader()

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
    except instaloader.exceptions.LoginRequiredException:
        raise PermissionError(
            "This post requires login (private account or age-restricted content)."
        )
    except instaloader.exceptions.QueryReturnedNotFoundException:
        raise FileNotFoundError(
            f"Post not found. Shortcode may be wrong or post may be deleted: {shortcode!r}"
        )
    except Exception as e:
        raise RuntimeError(f"instaloader error: {e}")

    urls = []

    # Check if it's a sidecar (carousel) post
    try:
        sidecar_nodes = list(post.get_sidecar_nodes())
        if sidecar_nodes:
            for node in sidecar_nodes:
                urls.append(node.display_url)
        else:
            # Single image post
            urls.append(post.url)
    except Exception:
        # Fallback: just get the main post URL
        urls.append(post.url)

    return urls


def fallback_imginn(shortcode: str) -> list[str]:
    """
    Fallback: attempt to scrape image URLs from imginn.com.
    Returns list of URLs found.
    """
    import urllib.request
    import re as _re

    try:
        url = f"https://imginn.com/p/{shortcode}/"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; OpenClaw/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Look for image URLs in common patterns
        patterns = [
            r'https://[^"\'<>\s]+\.(?:jpg|jpeg|png|webp)[^"\'<>\s]*',
        ]
        found = []
        seen = set()
        for pat in patterns:
            for m in _re.findall(pat, html):
                if m not in seen and "instagram" in m or "cdninstagram" in m:
                    found.append(m)
                    seen.add(m)
        return found[:10]  # cap at 10
    except Exception as e:
        print(f"  imginn fallback also failed: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Extract image URLs from an Instagram post."
    )
    parser.add_argument(
        "url_or_shortcode",
        nargs="?",
        help="Instagram post URL or shortcode",
    )
    parser.add_argument(
        "--shortcode",
        "-s",
        help="Explicit shortcode (alternative to positional arg)",
    )
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Also try imginn.com fallback if instaloader fails",
    )
    args = parser.parse_args()

    # Determine input
    raw_input = args.shortcode or args.url_or_shortcode
    if not raw_input:
        parser.print_help()
        sys.exit(1)

    # Extract shortcode
    try:
        shortcode = extract_shortcode(raw_input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Shortcode: {shortcode}", file=sys.stderr)

    # Try instaloader first
    try:
        urls = get_post_images(shortcode)
        if not urls:
            print("No images found.", file=sys.stderr)
            sys.exit(1)

        for i, url in enumerate(urls, 1):
            print(f"Slide {i}: {url}")

        print(f"\nTotal: {len(urls)} image(s)", file=sys.stderr)

    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Access denied: {e}", file=sys.stderr)
        if args.fallback:
            print("Trying imginn.com fallback...", file=sys.stderr)
            fallback_urls = fallback_imginn(shortcode)
            if fallback_urls:
                for i, url in enumerate(fallback_urls, 1):
                    print(f"Slide {i}: {url}")
                print(f"\nTotal (fallback): {len(fallback_urls)} image(s)", file=sys.stderr)
            else:
                print("Fallback also failed. Post may be private or unavailable.", file=sys.stderr)
                sys.exit(1)
        else:
            print("Tip: use --fallback to try imginn.com", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Not found: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.fallback:
            print("Trying imginn.com fallback...", file=sys.stderr)
            fallback_urls = fallback_imginn(shortcode)
            if fallback_urls:
                for i, url in enumerate(fallback_urls, 1):
                    print(f"Slide {i}: {url}")
            else:
                print("Fallback also failed.", file=sys.stderr)
                sys.exit(1)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
