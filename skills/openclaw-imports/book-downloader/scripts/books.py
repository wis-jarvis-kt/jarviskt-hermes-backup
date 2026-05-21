#!/usr/bin/env python3
"""
books.py — Find and download books (epub/pdf) from anywhere on the internet.

Usage:
  python books.py "atomic habits"
  python books.py "atomic habits" --author "james clear"
  python books.py "atomic habits" --format epub
  python books.py "atomic habits" --pick 1
  python books.py "atomic habits" --web
  python books.py "atomic habits" --free-only
  python books.py "atomic habits" --no-verify
  python books.py "atomic habits" --source anna
  python books.py "atomic habits" --tor        # route through Tor (auto-started)
"""

import argparse
import os
import re
import subprocess
import sys
import time
import zipfile
import threading
from pathlib import Path
from urllib.parse import quote_plus, urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install requests beautifulsoup4 lxml -q")
    import requests
    from bs4 import BeautifulSoup

try:
    import PyPDF2
except ImportError:
    os.system(f"{sys.executable} -m pip install PyPDF2 -q")
    try:
        import PyPDF2
    except ImportError:
        PyPDF2 = None

DOWNLOAD_DIR = Path.home() / "Downloads" / "Books"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

TOR_PROXY = "socks5h://127.0.0.1:9050"
SESSION_PROXIES = None  # set at runtime if --tor or --proxy used

results_lock = threading.Lock()


def get_session():
    """Return a requests session with proxy configured if set."""
    s = requests.Session()
    s.headers.update(HEADERS)
    if SESSION_PROXIES:
        s.proxies.update(SESSION_PROXIES)
    return s


def ensure_tor():
    """Start Tor via brew services if not already running."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--socks5", "127.0.0.1:9050", "--max-time", "5",
             "https://check.torproject.org/api/ip"],
            capture_output=True, text=True, timeout=8
        )
        if '"IsTor":true' in result.stdout:
            return True
    except Exception:
        pass

    print("🧅 Starting Tor...", end="", flush=True)
    try:
        subprocess.run(["brew", "services", "start", "tor"],
                       capture_output=True, timeout=15)
        # Wait up to 20s for Tor to bootstrap
        for _ in range(20):
            time.sleep(1)
            try:
                r = subprocess.run(
                    ["curl", "-s", "--socks5", "127.0.0.1:9050", "--max-time", "3",
                     "https://check.torproject.org/api/ip"],
                    capture_output=True, text=True, timeout=5
                )
                if '"IsTor":true' in r.stdout:
                    print(" ✓ Connected via Tor")
                    return True
                print(".", end="", flush=True)
            except Exception:
                continue
    except Exception as e:
        pass

    print(" ✗ Could not start Tor")
    return False

# Global session — configured with proxy at runtime in main()
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ─────────────────────────────────────────────
# Mirror lists
# ─────────────────────────────────────────────

LIBGEN_MIRRORS = [
    "https://libgen.li", "https://libgen.fun", "https://libgen.vip",
    "https://libgenfrialc.xyz", "https://libgen.rs", "https://libgen.is", "https://libgen.st",
]

ANNA_MIRRORS = [
    "https://annas-archive.se", "https://annas-archive.gs", "https://annas-archive.li",
    "https://annas-archive.org",
]

ZLIB_MIRRORS = [
    "https://z-library.se", "https://singlelogin.re", "https://zlibrary.to",
    "https://z-lib.id",
]

TELEGRAM_CHANNELS = [
    "libgen_scihub",
    "epubcenter",
    "ibookslibrary",
    "Books_WorldWide",
    "booksmania",
    "freebooksepub",
]

# Active mirrors (populated by --test-mirrors or used as-is)
active_libgen_mirrors = list(LIBGEN_MIRRORS)
active_anna_mirrors = list(ANNA_MIRRORS)
active_zlib_mirrors = list(ZLIB_MIRRORS)


def test_mirrors():
    """Test all mirrors and keep only reachable ones."""
    global active_libgen_mirrors, active_anna_mirrors, active_zlib_mirrors

    def check(url):
        try:
            r = SESSION.get(url, timeout=2, allow_redirects=True)
            return r.status_code < 500
        except Exception:
            return False

    def test_list(name, mirrors):
        reachable = []
        for m in mirrors:
            ok = check(m)
            status = "✓" if ok else "✗"
            print(f"   {status} {m}")
            if ok:
                reachable.append(m)
        return reachable

    print("🔌 Testing mirrors (2s timeout each)...\n")

    print("  LibGen:")
    r = test_list("LibGen", LIBGEN_MIRRORS)
    if r:
        active_libgen_mirrors[:] = r

    print("\n  Anna's Archive:")
    r = test_list("Anna", ANNA_MIRRORS)
    if r:
        active_anna_mirrors[:] = r

    print("\n  Z-Library:")
    r = test_list("ZLib", ZLIB_MIRRORS)
    if r:
        active_zlib_mirrors[:] = r

    print(f"\n  Active: {len(active_libgen_mirrors)} LibGen, {len(active_anna_mirrors)} Anna, {len(active_zlib_mirrors)} ZLib\n")


# ─────────────────────────────────────────────
# Metadata Lookup (Open Library API primary, Amazon fallback)
# ─────────────────────────────────────────────

def openlibrary_lookup(title, author=""):
    """Fetch book metadata from Open Library API (free, no scraping)."""
    try:
        query = f"{title} {author}".strip()
        url = (
            f"https://openlibrary.org/search.json?"
            f"q={quote_plus(query)}"
            f"&fields=title,author_name,number_of_pages_median,isbn,publishers,first_publish_year"
            f"&limit=1"
        )
        r = SESSION.get(url, timeout=10)
        data = r.json()
        docs = data.get("docs", [])
        if not docs:
            return None

        doc = docs[0]
        meta = {
            "title": doc.get("title", title),
            "author": ", ".join(doc.get("author_name", [])) or author,
            "pages": doc.get("number_of_pages_median"),
            "isbn": doc.get("isbn", [None])[0] if doc.get("isbn") else None,
            "publisher": ", ".join(doc.get("publishers", [])[:2]) or None,
            "published": str(doc.get("first_publish_year", "")) or None,
        }
        return meta
    except Exception:
        return None


def amazon_lookup(title, author=""):
    """Fetch book metadata from Amazon (fallback — often blocked)."""
    query = f"{title} {author}".strip()
    url = f"https://www.amazon.com/s?k={quote_plus(query)}&i=stripbooks"
    try:
        r = SESSION.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        result = soup.select_one('[data-component-type="s-search-result"]')
        if not result:
            return None

        link_tag = result.select_one("h2 a")
        if not link_tag:
            return None
        book_url = "https://www.amazon.com" + link_tag.get("href", "")

        r2 = SESSION.get(book_url, timeout=10)
        soup2 = BeautifulSoup(r2.text, "lxml")

        meta = {}
        title_tag = soup2.select_one("#productTitle")
        meta["title"] = title_tag.get_text(strip=True) if title_tag else title

        author_tag = soup2.select_one(".author .a-link-normal")
        meta["author"] = author_tag.get_text(strip=True) if author_tag else author

        detail_text = ""
        for row in soup2.select("#detailBullets_feature_div li"):
            detail_text += row.get_text(" ", strip=True) + "\n"
        for row in soup2.select(".detail-bullet-list li"):
            detail_text += row.get_text(" ", strip=True) + "\n"

        pages_match = re.search(r"(\d{2,4})\s*pages?", detail_text, re.I)
        meta["pages"] = int(pages_match.group(1)) if pages_match else None

        isbn_match = re.search(r"ISBN-13[:\s]+([0-9\-]{10,17})", detail_text)
        if not isbn_match:
            isbn_match = re.search(r"ISBN-10[:\s]+([0-9X\-]{9,13})", detail_text)
        meta["isbn"] = isbn_match.group(1).replace("-", "") if isbn_match else None

        pub_match = re.search(r"Publisher[:\s]+([^\n;]+)", detail_text)
        meta["publisher"] = pub_match.group(1).strip() if pub_match else None

        date_match = re.search(r"(\w+ \d{1,2},? \d{4})", detail_text)
        meta["published"] = date_match.group(1) if date_match else None

        meta["amazon_url"] = book_url
        return meta
    except Exception:
        return None


def metadata_lookup(title, author=""):
    """Try Open Library first, fall back to Amazon."""
    meta = openlibrary_lookup(title, author)
    if meta:
        meta["_source"] = "Open Library"
        return meta
    meta = amazon_lookup(title, author)
    if meta:
        meta["_source"] = "Amazon"
        return meta
    return None


# ─────────────────────────────────────────────
# Search: Anna's Archive
# ─────────────────────────────────────────────

def search_anna(title, author="", fmt=""):
    """Search Anna's Archive across multiple mirrors."""
    results = []
    query = f"{title} {author}".strip()
    ext = fmt if fmt in ("epub", "pdf") else ""

    for mirror in active_anna_mirrors:
        try:
            url = f"{mirror}/search?q={quote_plus(query)}"
            if ext:
                url += f"&ext={ext}"

            r = SESSION.get(url, timeout=12)
            soup = BeautifulSoup(r.text, "lxml")

            for item in soup.select("a[href*='/md5/']")[:15]:
                try:
                    href = item.get("href", "")
                    md5 = re.search(r"/md5/([a-f0-9]{32})", href)
                    if not md5:
                        continue
                    md5_hash = md5.group(1)

                    text = item.get_text(" ", strip=True)
                    fmt_match = re.search(r"\b(epub|pdf|mobi|djvu)\b", text, re.I)
                    detected_fmt = fmt_match.group(1).lower() if fmt_match else "?"

                    size_match = re.search(r"(\d+(?:\.\d+)?)\s*(KB|MB)", text, re.I)
                    size = f"{size_match.group(1)}{size_match.group(2)}" if size_match else "?"

                    year_match = re.search(r"\b(19|20)\d{2}\b", text)
                    year = year_match.group(0) if year_match else "?"

                    results.append({
                        "source": "Anna's Archive",
                        "source_key": "anna",
                        "title": title,
                        "author": author,
                        "year": year,
                        "format": detected_fmt,
                        "size": size,
                        "language": "en",
                        "md5": md5_hash,
                        "download_url": f"{mirror}/md5/{md5_hash}",
                        "type": "free",
                    })
                except Exception:
                    continue
            if results:
                break  # got results from this mirror
        except Exception:
            continue
    return results


# ─────────────────────────────────────────────
# Search: Library Genesis
# ─────────────────────────────────────────────

def search_libgen(title, author="", fmt=""):
    """Search Library Genesis across multiple mirrors."""
    results = []
    query = f"{title} {author}".strip()

    for mirror in active_libgen_mirrors:
        try:
            # libgen.li uses index.php, others use search.php
            if "libgen.li" in mirror or "libgen.fun" in mirror or "libgen.vip" in mirror:
                url = f"{mirror}/index.php?req={quote_plus(query)}&res=25&view=simple&column=def"
            else:
                url = f"{mirror}/search.php?req={quote_plus(query)}&res=25&view=simple&phrase=1&column=def"
            r = SESSION.get(url, timeout=15)
            soup = BeautifulSoup(r.text, "lxml")

            # Find result table — libgen.li uses id="tablelibgen", others use "searchresults"
            table = (soup.find("table", {"id": "tablelibgen"}) or
                     soup.find("table", {"id": "searchresults"}) or
                     soup.find("table", class_="c"))
            if not table:
                continue

            # Try JSON API first for libgen.li (more reliable)
            json_link = soup.find("a", href=re.compile(r"json\.php\?object=f&ids="))
            if json_link and "libgen.li" in mirror:
                try:
                    json_url = mirror + "/" + json_link.get("href", "").lstrip("/")
                    jr = SESSION.get(json_url, timeout=12)
                    books = jr.json()
                    for b in books[:15]:
                        ext = b.get("extension", "").lower()
                        if fmt and ext != fmt.lower():
                            continue
                        md5 = b.get("md5", "").lower()
                        results.append({
                            "source": "LibGen",
                            "source_key": "libgen",
                            "title": b.get("title", title)[:100],
                            "author": b.get("author", author),
                            "year": b.get("year", "?"),
                            "format": ext,
                            "size": b.get("filesize", "?"),
                            "language": b.get("language", "en"),
                            "md5": md5,
                            "download_url": f"https://libgen.li/ads.php?md5={md5}" if md5 else None,
                            "type": "free",
                        })
                    if results:
                        break
                except Exception:
                    pass

            rows = table.find_all("tr")[1:]  # skip header
            for row in rows:
                try:
                    cols = row.find_all("td")
                    if len(cols) < 4:
                        continue

                    # Extract all text and links from row
                    row_text = row.get_text(" ", strip=True)
                    row_html = str(row)

                    # Find MD5 anywhere in row
                    md5_match = re.search(r"md5=([a-f0-9]{32})", row_html, re.I)
                    if not md5_match:
                        md5_match = re.search(r"/ads\.php\?md5=([a-f0-9]{32})", row_html, re.I)
                    md5 = md5_match.group(1).lower() if md5_match else None

                    # Extract fields — column order varies by mirror
                    auth = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                    ttl_tag = cols[2] if len(cols) > 2 else cols[0]
                    ttl = ttl_tag.get_text(strip=True)[:100]

                    # Find format (epub/pdf) in row
                    fmt_match = re.search(r"\b(epub|pdf|mobi|djvu)\b", row_html, re.I)
                    ext = fmt_match.group(1).lower() if fmt_match else "?"

                    if fmt and ext != fmt.lower():
                        continue

                    # Year
                    year_match = re.search(r"\b(19|20)\d{2}\b", row_text)
                    year = year_match.group(0) if year_match else "?"

                    # Size
                    size_match = re.search(r"(\d+(?:\.\d+)?)\s*(KB|MB)", row_text, re.I)
                    size = f"{size_match.group(1)}{size_match.group(2)}" if size_match else "?"

                    results.append({
                        "source": "LibGen",
                        "source_key": "libgen",
                        "title": ttl,
                        "author": auth,
                        "year": year,
                        "format": ext,
                        "size": size,
                        "language": "en",
                        "md5": md5,
                        "download_url": f"https://libgen.li/ads.php?md5={md5}" if md5 else None,
                        "type": "free",
                    })
                except Exception:
                    continue
            if results:
                break  # got results from this mirror, stop
        except Exception:
            continue

    return results


# ─────────────────────────────────────────────
# Search: Z-Library
# ─────────────────────────────────────────────

def search_zlibrary(title, author="", fmt=""):
    """Search Z-Library across multiple mirrors."""
    results = []
    query = f"{title} {author}".strip()

    for zlib_base in active_zlib_mirrors:
        try:
            url = f"{zlib_base}/s/{quote_plus(query)}"
            if fmt:
                url += f"?extensions[]={fmt.upper()}"

            r = SESSION.get(url, timeout=12)
            soup = BeautifulSoup(r.text, "lxml")

            for item in soup.select(".book-item, .bookRow, [itemtype*='Book']")[:10]:
                try:
                    title_tag = item.select_one("h3 a, .title a, a[href*='/book/']")
                    if not title_tag:
                        continue
                    ttl = title_tag.get_text(strip=True)
                    href = title_tag.get("href", "")
                    if href and not href.startswith("http"):
                        href = zlib_base + href

                    auth_tag = item.select_one(".authors, .book-author")
                    auth = auth_tag.get_text(strip=True) if auth_tag else ""

                    prop_text = item.get_text(" ", strip=True)
                    fmt_match = re.search(r"\b(epub|pdf|mobi)\b", prop_text, re.I)
                    detected_fmt = fmt_match.group(1).lower() if fmt_match else "?"

                    year_match = re.search(r"\b(19|20)\d{2}\b", prop_text)
                    year = year_match.group(0) if year_match else "?"

                    size_match = re.search(r"(\d+(?:\.\d+)?)\s*(KB|MB)", prop_text, re.I)
                    size = f"{size_match.group(1)}{size_match.group(2)}" if size_match else "?"

                    results.append({
                        "source": "Z-Library",
                        "source_key": "zlib",
                        "title": ttl,
                        "author": auth,
                        "year": year,
                        "format": detected_fmt,
                        "size": size,
                        "language": "en",
                        "md5": None,
                        "download_url": href,
                        "type": "free",
                    })
                except Exception:
                    continue
            if results:
                break  # got results from this mirror
        except Exception:
            continue
    return results


# ─────────────────────────────────────────────
# Search: PDFDrive
# ─────────────────────────────────────────────

def search_pdfdrive(title, author="", fmt=""):
    """Search PDFDrive."""
    if fmt and fmt.lower() == "epub":
        return []  # PDFDrive is PDF only
    results = []
    try:
        query = f"{title} {author}".strip()
        url = f"https://www.pdfdrive.com/search?q={quote_plus(query)}&pagecount=&pubyear=&searchin=&em=1"
        r = SESSION.get(url, timeout=12)
        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select(".file-left, .book-img-box")[:8]:
            try:
                parent = item.find_parent("a") or item.select_one("a")
                if not parent:
                    continue
                href = parent.get("href", "")
                if not href.startswith("http"):
                    href = "https://www.pdfdrive.com" + href

                title_tag = item.select_one("h2, .title")
                ttl = title_tag.get_text(strip=True) if title_tag else ""
                if not ttl:
                    ttl = parent.get("title", "")

                info = item.get_text(" ", strip=True)
                pages_match = re.search(r"(\d+)\s*pages?", info, re.I)
                pages = pages_match.group(1) if pages_match else "?"

                results.append({
                    "source": "PDFDrive",
                    "source_key": "pdfdrive",
                    "title": ttl,
                    "author": author,
                    "year": "?",
                    "format": "pdf",
                    "size": f"~{pages}pp" if pages != "?" else "?",
                    "language": "en",
                    "md5": None,
                    "download_url": href,
                    "type": "free",
                })
            except Exception:
                continue
    except Exception:
        pass
    return results


# ─────────────────────────────────────────────
# Search: OceanOfPDF
# ─────────────────────────────────────────────

def search_oceanofpdf(title, author="", fmt=""):
    """Search OceanOfPDF — good for newer books."""
    results = []
    try:
        query = f"{title} {author}".strip()
        url = f"https://oceanofpdf.com/?s={quote_plus(query)}"
        r = SESSION.get(url, timeout=12)
        soup = BeautifulSoup(r.text, "lxml")

        for article in soup.select("article")[:10]:
            try:
                title_tag = article.select_one("h2 a, h3 a, .entry-title a")
                if not title_tag:
                    continue
                ttl = title_tag.get_text(strip=True)
                book_url = title_tag.get("href", "")

                # Detect format from title/URL
                fmt_match = re.search(r"\b(epub|pdf)\b", ttl + book_url, re.I)
                detected_fmt = fmt_match.group(1).lower() if fmt_match else "pdf"

                if fmt and detected_fmt != fmt.lower():
                    # Try to find both formats listed — keep if matches or unknown
                    if "epub" in ttl.lower() and fmt == "epub":
                        detected_fmt = "epub"
                    elif "pdf" in ttl.lower() and fmt == "pdf":
                        detected_fmt = "pdf"

                results.append({
                    "source": "OceanOfPDF",
                    "source_key": "oceanofpdf",
                    "title": ttl[:80],
                    "author": author,
                    "year": "?",
                    "format": detected_fmt,
                    "size": "?",
                    "language": "en",
                    "md5": None,
                    "download_url": book_url,
                    "type": "free",
                })
            except Exception:
                continue
    except Exception:
        pass
    return results


# ─────────────────────────────────────────────
# Search: Telegram Public Channels
# ─────────────────────────────────────────────

def search_telegram(title, author="", fmt=""):
    """Search public Telegram book channels via their web interface."""
    results = []
    title_lower = title.lower()
    author_lower = author.lower()

    for channel in TELEGRAM_CHANNELS:
        try:
            url = f"https://t.me/s/{channel}"
            r = SESSION.get(url, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "lxml")

            # Each post is a .tgme_widget_message
            for msg in soup.select(".tgme_widget_message"):
                try:
                    text_el = msg.select_one(".tgme_widget_message_text")
                    msg_text = text_el.get_text(" ", strip=True) if text_el else ""
                    msg_text_lower = msg_text.lower()

                    # Check if this post mentions the book title
                    if title_lower not in msg_text_lower:
                        # Try matching individual significant words (3+ chars)
                        words = [w for w in title_lower.split() if len(w) >= 3]
                        if not words or sum(1 for w in words if w in msg_text_lower) < len(words) * 0.6:
                            continue

                    # If author specified, prefer posts mentioning the author
                    if author_lower and author_lower not in msg_text_lower:
                        # Still include but with lower priority (don't skip)
                        pass

                    # Extract post URL
                    post_link = msg.get("data-post", "")
                    if post_link:
                        post_url = f"https://t.me/{post_link}"
                    else:
                        post_url = url

                    # Check for file attachments
                    doc_el = msg.select_one(".tgme_widget_message_document")
                    filename = ""
                    if doc_el:
                        title_el = doc_el.select_one(".tgme_widget_message_document_title")
                        if title_el:
                            filename = title_el.get_text(strip=True)

                    # Detect format from filename or message text
                    detected_fmt = "?"
                    check_text = filename + " " + msg_text
                    fmt_match = re.search(r"\b(epub|pdf|mobi|djvu)\b", check_text, re.I)
                    if fmt_match:
                        detected_fmt = fmt_match.group(1).lower()

                    if fmt and detected_fmt != "?" and detected_fmt != fmt.lower():
                        continue

                    # Look for direct download links in the post
                    direct_url = None
                    for a in msg.select("a[href]"):
                        href = a.get("href", "")
                        if re.search(r"\.(epub|pdf|mobi)\b", href, re.I):
                            direct_url = href
                            break

                    # Preview of the post text
                    preview = msg_text[:120] + "..." if len(msg_text) > 120 else msg_text

                    results.append({
                        "source": f"Telegram @{channel}",
                        "source_key": "telegram",
                        "title": filename if filename else title,
                        "author": author,
                        "year": "?",
                        "format": detected_fmt,
                        "size": "?",
                        "language": "?",
                        "md5": None,
                        "download_url": direct_url or post_url,
                        "type": "free",
                        "telegram_post_url": post_url,
                        "telegram_channel": channel,
                        "telegram_preview": preview,
                        "telegram_has_file": bool(doc_el),
                        "telegram_direct": bool(direct_url),
                    })
                except Exception:
                    continue
        except Exception:
            continue

    return results


def search_telegram_bot(title, author=""):
    """Generate links to Telegram book finder bots for manual search."""
    query = f"{title} {author}".strip()
    encoded = quote_plus(query)
    return [
        {
            "source": "Telegram Bot @BookFinderBot",
            "source_key": "telegram_bot",
            "title": title,
            "author": author,
            "year": "?",
            "format": "?",
            "size": "?",
            "language": "?",
            "md5": None,
            "download_url": f"https://t.me/BookFinderBot?start={encoded}",
            "type": "free",
            "telegram_post_url": f"https://t.me/BookFinderBot?start={encoded}",
            "telegram_channel": "BookFinderBot",
            "telegram_preview": "Open in Telegram to search via bot",
            "telegram_has_file": False,
            "telegram_direct": False,
        },
    ]


# ─────────────────────────────────────────────
# Search: Web (DuckDuckGo dorking)
# ─────────────────────────────────────────────

def search_web(title, author="", fmt=""):
    """Search DuckDuckGo for direct download links."""
    results = []
    fmt_q = fmt if fmt else "epub OR pdf"

    queries = [
        f'"{title}" "{author}" filetype:{fmt or "epub"}' if author else f'"{title}" filetype:{fmt or "epub"}',
        f'"{title}" {fmt_q} download site:drive.google.com OR site:mediafire.com OR site:dropbox.com',
        f'"{title}" epub download -amazon -goodreads -audible',
    ]

    seen_urls = set()
    for q in queries[:2]:
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(q)}"
            r = SESSION.get(url, timeout=12)
            soup = BeautifulSoup(r.text, "lxml")

            for a in soup.select(".result__a")[:5]:
                href = a.get("href", "")
                # DDG wraps links
                real_url_match = re.search(r"uddg=([^&]+)", href)
                if real_url_match:
                    from urllib.parse import unquote
                    href = unquote(real_url_match.group(1))

                if href in seen_urls or not href.startswith("http"):
                    continue
                seen_urls.add(href)

                # Detect format from URL/text
                link_text = a.get_text(strip=True)
                fmt_match = re.search(r"\b(epub|pdf)\b", href + link_text, re.I)
                detected_fmt = fmt_match.group(1).lower() if fmt_match else fmt or "?"

                # Categorize host
                host = urlparse(href).netloc
                source_label = "Web"
                if "drive.google.com" in host:
                    source_label = "Google Drive"
                elif "mediafire.com" in host:
                    source_label = "MediaFire"
                elif "dropbox.com" in host:
                    source_label = "Dropbox"
                elif "t.me" in host or "telegram" in host:
                    source_label = "Telegram"
                elif "reddit.com" in host:
                    source_label = "Reddit"

                results.append({
                    "source": f"Web ({source_label})",
                    "source_key": "web",
                    "title": link_text[:80],
                    "author": author,
                    "year": "?",
                    "format": detected_fmt,
                    "size": "?",
                    "language": "?",
                    "md5": None,
                    "download_url": href,
                    "type": "free",
                })
            time.sleep(1)  # be polite
        except Exception:
            continue

    return results


# ─────────────────────────────────────────────
# Paid fallback links
# ─────────────────────────────────────────────

def paid_links(title, author=""):
    query = quote_plus(f"{title} {author}".strip())
    return [
        {
            "source": "Amazon Kindle",
            "source_key": "amazon",
            "title": title,
            "author": author,
            "year": "?",
            "format": "kindle",
            "size": "?",
            "language": "en",
            "md5": None,
            "download_url": f"https://www.amazon.com/s?k={query}&i=digital-text",
            "type": "paid",
        },
        {
            "source": "Google Play Books",
            "source_key": "google",
            "title": title,
            "author": author,
            "year": "?",
            "format": "ebook",
            "size": "?",
            "language": "en",
            "md5": None,
            "download_url": f"https://play.google.com/store/search?q={query}&c=books",
            "type": "paid",
        },
    ]


# ─────────────────────────────────────────────
# Download
# ─────────────────────────────────────────────

def resolve_anna_download(md5):
    """Resolve actual download URL from Anna's Archive md5 page."""
    for mirror in active_anna_mirrors:
        try:
            url = f"{mirror}/md5/{md5}"
            r = SESSION.get(url, timeout=12)
            soup = BeautifulSoup(r.text, "lxml")

            for a in soup.select("a[href]"):
                href = a.get("href", "")
                if "library.lol" in href or "libgen" in href or "/download" in href.lower():
                    return href

            for a in soup.select("a"):
                text = a.get_text(strip=True).lower()
                if "download" in text or "fast" in text:
                    href = a.get("href", "")
                    if href.startswith("http"):
                        return href
        except Exception:
            continue
    return None


def resolve_libgen_download(md5):
    """Try multiple LibGen download mirrors — libgen.li first via ads.php."""
    # Primary: libgen.li ads.php -> get.php?key=...
    try:
        ads_url = f"https://libgen.li/ads.php?md5={md5}"
        r = SESSION.get(ads_url, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if "get.php" in href and "key=" in href:
                return "https://libgen.li/" + href.lstrip("/")
    except Exception:
        pass

    # Fallback: library.lol and others
    urls = [
        f"https://library.lol/main/{md5}",
        f"https://libgen.rs/get.php?md5={md5}",
        f"https://libgen.is/get.php?md5={md5}",
    ]
    for url in urls:
        try:
            r = SESSION.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(r.text, "lxml")
            for a in soup.select("a[href]"):
                href = a.get("href", "")
                if re.search(r"\.(epub|pdf|mobi|djvu)(\?|$)", href, re.I):
                    if not href.startswith("http"):
                        href = urljoin(url, href)
                    return href
            if r.headers.get("Content-Type", "").startswith("application/"):
                return url
        except Exception:
            continue
    return None


def download_file(url, title, fmt, progress=True):
    """Download file with progress bar."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_title = re.sub(r'[<>:"/\\|?*]', "", title)[:80]
    filename = f"{safe_title}.{fmt}"
    dest = DOWNLOAD_DIR / filename

    # Handle duplicate filenames
    counter = 1
    while dest.exists():
        dest = DOWNLOAD_DIR / f"{safe_title} ({counter}).{fmt}"
        counter += 1

    try:
        r = SESSION.get(url, stream=True, timeout=30, allow_redirects=True)
        r.raise_for_status()

        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 8192

        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress and total:
                        pct = downloaded / total * 100
                        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                        print(f"\r  [{bar}] {pct:.0f}% ({downloaded//1024}KB)", end="", flush=True)

        if progress:
            print()

        # Sanity check — min 5KB
        if dest.stat().st_size < 5000:
            print("  ⚠️  Downloaded file is suspiciously small — may be corrupted.")

        return dest

    except Exception as e:
        print(f"\n  ❌ Download failed: {e}")
        return None


# ─────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────

def verify_download(path, expected_pages=None):
    """Verify downloaded file integrity — content inspection, not just size.
    
    Catches:
    - HTML error pages disguised as PDFs/EPUBs (very common with bad sources)
    - PDFs with too few pages (stubs/placeholders)
    - EPUBs missing .opf manifest or chapter files
    - Truncated/corrupt downloads
    """
    if not path or not path.exists():
        return "❌ File not found"

    size = path.stat().st_size
    if size < 5000:
        return "❌ Suspicious (file too small — likely corrupted)"

    ext = path.suffix.lower()
    actual_pages = None

    try:
        # ── Read file header for content sniffing ──
        with open(path, "rb") as f:
            header = f.read(2000)

        # Check it's not an HTML error page disguised as a book file
        stripped = header.strip()
        if stripped.startswith(b"<!DOCTYPE") or stripped.startswith(b"<html") or stripped.startswith(b"<!doctype"):
            return "❌ FAKE: HTML page disguised as a book file (download failed silently)"

        if ext == ".epub":
            try:
                with zipfile.ZipFile(path, "r") as z:
                    names = z.namelist()
                    # Must have an OPF manifest
                    if not any(n.endswith(".opf") for n in names):
                        return "❌ Invalid EPUB: missing .opf manifest (not a real book)"
                    # Must have actual chapter content
                    html_files = [n for n in names if n.endswith((".html", ".xhtml", ".htm"))]
                    if len(html_files) < 5:
                        return f"❌ Suspicious EPUB: only {len(html_files)} content files (expected 5+ chapters)"
                    actual_pages = len(html_files) * 8  # rough: ~8 pages per chapter file
            except zipfile.BadZipFile:
                return "❌ FAKE: Not a valid ZIP/EPUB archive (corrupt or wrong file type)"

        elif ext == ".pdf":
            # Must start with %PDF-
            if not header.startswith(b"%PDF-"):
                return "❌ FAKE: Not a real PDF (bad header — likely an HTML error page)"

            if PyPDF2:
                with open(path, "rb") as f:
                    try:
                        reader = PyPDF2.PdfReader(f)
                        actual_pages = len(reader.pages)
                    except Exception:
                        pass
            if actual_pages is None:
                # Fallback: count /Page objects in first 200KB
                with open(path, "rb") as f:
                    content = f.read(200000)
                    matches = re.findall(rb"/Type\s*/Page[^s]", content)
                    if matches:
                        actual_pages = len(matches)

            # A real book PDF should have at least 50 pages
            if actual_pages is not None and actual_pages < 50:
                return f"❌ Suspicious PDF: only {actual_pages} pages detected (real books have 100+)"

    except Exception as e:
        return f"⚠️  Could not verify ({e})"

    if expected_pages and actual_pages:
        tolerance = 0.20  # 20% for epub estimation
        if ext == ".epub":
            tolerance = 0.40  # epub chapter counting is rough
        ratio = actual_pages / expected_pages
        if ratio < (1 - tolerance) or ratio > (1 + tolerance):
            return f"❌ Suspicious — expected ~{expected_pages} pages, got ~{actual_pages}"
        else:
            return f"✅ Verified — ~{actual_pages} pages (expected ~{expected_pages})"
    elif actual_pages:
        return f"✅ Valid file — ~{actual_pages} pages detected"
    else:
        return f"⚠️  Unverified — file looks OK ({size//1024}KB) but couldn't count pages"


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Find and download books (epub/pdf) from anywhere on the internet."
    )
    parser.add_argument("title", help="Book title to search for")
    parser.add_argument("--author", "-a", default="", help="Author name")
    parser.add_argument("--format", "-f", default="", choices=["epub", "pdf", ""], help="Preferred format")
    parser.add_argument("--pick", "-p", type=int, help="Auto-pick result number (1-based)")
    parser.add_argument("--web", action="store_true", help="Enable extended web search (DDG dorking)")
    parser.add_argument("--free-only", action="store_true", help="Skip paid purchase links")
    parser.add_argument("--no-verify", action="store_true", help="Skip post-download verification")
    parser.add_argument("--source", choices=["anna", "libgen", "zlib", "pdfdrive", "oceanofpdf", "web", "telegram"], help="Search specific source only")
    parser.add_argument("--proxy", default="", help="Proxy URL (e.g. socks5://127.0.0.1:1080)")
    parser.add_argument("--tor", action="store_true", default=False, help="Force Tor for all requests")
    parser.add_argument("--no-tor", action="store_true", default=False, help="Disable auto-Tor fallback")
    parser.add_argument("--test-mirrors", action="store_true", help="Test which mirrors are reachable before searching")
    args = parser.parse_args()

    # Configure proxy / Tor
    if args.proxy:
        SESSION.proxies = {"http": args.proxy, "https": args.proxy}
        print(f"🔗 Using proxy: {args.proxy}")
    elif args.tor:
        # Force Tor mode
        if ensure_tor():
            SESSION.proxies = {"http": TOR_PROXY, "https": TOR_PROXY}
            print(f"🧅 Routing through Tor (forced)")
        else:
            print("⚠️  Tor unavailable — continuing without proxy")
    elif not args.no_tor:
        # Auto mode: try direct first, fall back to Tor if blocked
        print("🔍 Checking connectivity...", end="", flush=True)
        try:
            test = SESSION.get("https://libgen.li/index.php?req=test&res=1", timeout=6, allow_redirects=True)
            # Check we got actual LibGen content, not a block page
            if "libgen" in test.text.lower() or "library" in test.text.lower():
                print(" ✓ Direct OK")
            else:
                raise Exception("Got block page")
        except Exception:
            print(" ✗ Blocked — switching to Tor")
            if ensure_tor():
                SESSION.proxies = {"http": TOR_PROXY, "https": TOR_PROXY}
                print(f"🧅 Routing through Tor")

    # Test mirrors if requested
    if args.test_mirrors:
        test_mirrors()

    title = args.title
    author = args.author
    fmt = args.format

    print(f"\n🔍 Searching for: \"{title}\"" + (f" by {author}" if author else "") + "\n")

    # ── Metadata lookup (Open Library → Amazon fallback) ──
    book_meta = None
    print("📦 Fetching book details...", end="", flush=True)
    book_meta = metadata_lookup(title, author)
    if book_meta:
        src = book_meta.get("_source", "?")
        print(f" ✓ ({src})")
        print(f"\n📖 {book_meta.get('title', title)} — {book_meta.get('author', author)}")
        details = []
        if book_meta.get("publisher"):
            details.append(f"Publisher: {book_meta['publisher']}")
        if book_meta.get("pages"):
            details.append(f"Pages: {book_meta['pages']}")
        if book_meta.get("isbn"):
            details.append(f"ISBN: {book_meta['isbn']}")
        if book_meta.get("published"):
            details.append(f"Published: {book_meta['published']}")
        if details:
            print(f"   {' | '.join(details)}")
        print()
    else:
        print(" ✗ (not found, continuing anyway)\n")

    # ── Search all sources in parallel ──
    all_results = []
    search_fns = []

    if args.source:
        source_map = {
            "anna": search_anna,
            "libgen": search_libgen,
            "zlib": search_zlibrary,
            "pdfdrive": search_pdfdrive,
            "oceanofpdf": search_oceanofpdf,
            "web": search_web,
            "telegram": search_telegram,
        }
        search_fns = [source_map[args.source]]
    else:
        search_fns = [search_oceanofpdf, search_anna, search_libgen, search_zlibrary, search_pdfdrive, search_telegram]
        if args.web:
            search_fns.append(search_web)

    print("🌐 Searching sources in parallel...")

    def run_search(fn):
        try:
            found = fn(title, author, fmt)
            with results_lock:
                all_results.extend(found)
                src = found[0]["source"] if found else fn.__name__
                if found:
                    print(f"   ✓ {src}: {len(found)} result(s)")
                else:
                    src_name = {"search_anna": "Anna's Archive", "search_libgen": "LibGen",
                                "search_zlibrary": "Z-Library", "search_pdfdrive": "PDFDrive",
                                "search_web": "Web", "search_telegram": "Telegram"}.get(fn.__name__, fn.__name__)
                    print(f"   ✗ {src_name}: no results")
        except Exception as e:
            pass

    threads = [threading.Thread(target=run_search, args=(fn,)) for fn in search_fns]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Add Telegram bot links as additional option
    telegram_channel_results = [r for r in all_results if r.get("source_key") == "telegram"]
    if not telegram_channel_results:
        all_results.extend(search_telegram_bot(title, author))

    # Add paid fallback if not free-only and nothing found (or always show at bottom)
    if not args.free_only:
        all_results.extend(paid_links(title, author))

    if not all_results:
        print("\n❌ No results found. Try --web for a wider search.")
        sys.exit(1)

    # ── Display results ──
    print(f"\n{'─'*60}")
    current_source = None
    numbered = []

    # Group by source
    free_results = [r for r in all_results if r["type"] == "free"]
    paid_results = [r for r in all_results if r["type"] == "paid"]

    for r in free_results + paid_results:
        numbered.append(r)

    for i, r in enumerate(numbered, 1):
        src = r["source"]
        if src != current_source:
            if r["type"] == "paid":
                prefix = "💰"
            elif r.get("source_key") in ("telegram", "telegram_bot"):
                prefix = "📱"
            else:
                prefix = "📚"
            label = "[FREE - Telegram]" if r.get("source_key") in ("telegram", "telegram_bot") else f"[{src}]"
            print(f"\n{prefix} {label}")
            current_source = src

        fmt_str = r["format"].upper() if r["format"] != "?" else "?"
        print(f"  {i:2}. {r['title'][:55]}")
        if r.get("source_key") in ("telegram", "telegram_bot"):
            channel = r.get("telegram_channel", "")
            preview = r.get("telegram_preview", "")
            has_file = "📎 File attached" if r.get("telegram_has_file") else "🔗 Post link"
            print(f"      @{channel} | {fmt_str} | {has_file}")
            if preview:
                print(f"      \"{preview[:70]}\"")
        else:
            print(f"      {r['author'] or '(unknown)'} | {r['year']} | {fmt_str} | {r['size']}")

    print(f"\n{'─'*60}")
    if not args.pick and not numbered:
        sys.exit(0)

    # ── Pick ──
    if args.pick:
        choice = args.pick
    else:
        try:
            raw = input(f"\nPick a number to download (1-{len(numbered)}), or q to quit: ").strip()
            if raw.lower() == "q":
                sys.exit(0)
            choice = int(raw)
        except (ValueError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(0)

    if choice < 1 or choice > len(numbered):
        print(f"Invalid choice: {choice}")
        sys.exit(1)

    selected = numbered[choice - 1]

    # Paid source — open browser
    if selected["type"] == "paid":
        print(f"\n💰 Opening {selected['source']} in your browser...")
        os.system(f"open '{selected['download_url']}'")
        sys.exit(0)

    # Telegram bot link — open in browser
    if selected.get("source_key") == "telegram_bot":
        print(f"\n📱 Opening Telegram bot in your browser...")
        os.system(f"open '{selected['download_url']}'")
        sys.exit(0)

    # Telegram post without direct file — open in browser
    if selected.get("source_key") == "telegram" and not selected.get("telegram_direct"):
        post_url = selected.get("telegram_post_url", selected["download_url"])
        print(f"\n📱 This Telegram post may contain the book file.")
        print(f"   Opening in browser: {post_url}")
        os.system(f"open '{post_url}'")
        sys.exit(0)

    # ── Resolve download URL ──
    print(f"\n⬇️  Resolving download link...")
    dl_url = selected["download_url"]
    md5 = selected.get("md5")

    if selected["source_key"] == "anna" and md5:
        resolved = resolve_anna_download(md5)
        if resolved:
            dl_url = resolved
        else:
            # Try libgen fallback with same md5
            resolved = resolve_libgen_download(md5)
            if resolved:
                dl_url = resolved

    elif selected["source_key"] == "libgen" and md5:
        resolved = resolve_libgen_download(md5)
        if resolved:
            dl_url = resolved

    elif selected["source_key"] == "oceanofpdf":
        # Follow book page to find actual download link
        try:
            r = SESSION.get(dl_url, timeout=12)
            soup = BeautifulSoup(r.text, "lxml")
            for a in soup.find_all("a", href=True):
                href = a.get("href", "")
                txt = a.get_text(strip=True).lower()
                if re.search(r"\.(epub|pdf)(\?|$)", href, re.I) or "download" in txt and re.search(r"epub|pdf", txt):
                    dl_url = href
                    break
            # If no direct file link, open in browser
            if "oceanofpdf.com" in dl_url:
                print(f"   Opening in browser: {dl_url}")
                os.system(f"open '{dl_url}'")
                sys.exit(0)
        except Exception:
            pass

    if not dl_url:
        print("❌ Could not resolve a direct download link.")
        print(f"   Try opening manually: {selected['download_url']}")
        sys.exit(1)

    print(f"   URL: {dl_url[:80]}...")

    # ── Download ──
    dl_fmt = selected["format"] if selected["format"] in ("epub", "pdf", "mobi") else (fmt or "epub")
    dl_title = selected["title"] or title
    print(f"\n📥 Downloading \"{dl_title}\" ({dl_fmt.upper()})...")

    path = download_file(dl_url, dl_title, dl_fmt)

    if path:
        print(f"\n✅ Saved to: {path}")

        # ── Verify ──
        if not args.no_verify:
            expected_pages = book_meta.get("pages") if book_meta else None
            print("🔍 Verifying download...")
            verdict = verify_download(path, expected_pages)
            print(f"   {verdict}")
    else:
        print("\n❌ Download failed.")
        print(f"   Try opening the source manually: {selected['download_url']}")
        if selected["source_key"] in ("anna", "libgen") and md5:
            print(f"   Or try: https://library.lol/main/{md5}")


if __name__ == "__main__":
    main()
