"""Find openly licensed photos online, and download the ones the user approved, with their credit.

Two steps, because downloading needs the user's permission first:

    python fetch_image.py search "Marina Bay Sands night" [--n 8] [--source commons|openverse|both] [--min-width 1600]
        Prints candidates: id, size, licence, author, page URL. Downloads nothing.

    python fetch_image.py preview "<id>" ["<id>" ...] --out DIR
        Downloads small thumbnails (about 400 px wide) of the listed ids and puts them on one sheet,
        so you can look before choosing. Ask the user before running this too.

    python fetch_image.py get "<id>" --out DIR [--width 1920]
        Downloads the chosen photo at slide resolution and appends its credit to DIR/credits.json.

Ids look like commons:File:Name.jpg or openverse:<uuid>. Sources: Wikimedia Commons (free
licences and public domain) and Openverse (Creative Commons search across Flickr and other
sites). Only CC0, public domain, CC BY and CC BY-SA results are listed; put the credit line
on the slide that uses the photo ("Photo: Author, CC BY-SA 4.0, Wikimedia Commons").
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = "ppt-maker/1.0 (slide image search; personal use)"
OK_LICENCES = re.compile(r"^(cc0|pdm|public domain|pd|cc[ -]?by(?:[ -]sa)?(?:[ -]\d\.\d)?)", re.I)


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def download(url, dst):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
        f.write(r.read())
    return dst


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search_commons(query, n, min_width, thumb=400):
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": max(n * 3, 15),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": thumb,
    }
    data = http_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
    out = []
    for page in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        lic = strip_html(meta.get("LicenseShortName", {}).get("value", ""))
        if not OK_LICENCES.match(lic) or info.get("width", 0) < min_width:
            continue
        out.append({
            "id": "commons:" + page["title"], "width": info.get("width"), "height": info.get("height"),
            "licence": lic, "author": strip_html(meta.get("Artist", {}).get("value", ""))[:80] or "unknown",
            "page": info.get("descriptionurl"), "thumb": info.get("thumburl"), "full": info.get("url"),
            "source": "Wikimedia Commons",
        })
        if len(out) >= n:
            break
    return out


def search_openverse(query, n, min_width):
    params = {"q": query, "page_size": max(n * 2, 10), "license": "cc0,pdm,by,by-sa", "mature": "false"}
    data = http_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params))
    out = []
    for r in data.get("results", []):
        if (r.get("width") or 0) < min_width:
            continue
        lic = f"CC {r.get('license', '').upper()} {r.get('license_version', '')}".strip()
        if r.get("license") in ("cc0", "pdm"):
            lic = r["license"].upper()
        out.append({
            "id": "openverse:" + r["id"], "width": r.get("width"), "height": r.get("height"), "licence": lic,
            "author": (r.get("creator") or "unknown")[:80], "page": r.get("foreign_landing_url"),
            "thumb": r.get("thumbnail"), "full": r.get("url"), "source": r.get("source", "Openverse"),
        })
        if len(out) >= n:
            break
    return out


def lookup(item_id, width=1920):
    """Full record for one id, with a download URL at about the requested width."""
    kind, key = item_id.split(":", 1)
    if kind == "commons":
        params = {"action": "query", "format": "json", "titles": key, "prop": "imageinfo",
                  "iiprop": "url|size|extmetadata", "iiurlwidth": width}
        page = next(iter(http_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
                         ["query"]["pages"].values()))
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        return {"id": item_id, "url": info.get("thumburl") or info["url"], "thumb": info.get("thumburl"),
                "licence": strip_html(meta.get("LicenseShortName", {}).get("value", "")),
                "author": strip_html(meta.get("Artist", {}).get("value", "")) or "unknown",
                "page": info.get("descriptionurl"), "source": "Wikimedia Commons"}
    r = http_json(f"https://api.openverse.org/v1/images/{key}/")
    lic = f"CC {r.get('license', '').upper()} {r.get('license_version', '')}".strip()
    return {"id": item_id, "url": r["url"], "thumb": r.get("thumbnail"), "licence": lic,
            "author": r.get("creator") or "unknown", "page": r.get("foreign_landing_url"),
            "source": r.get("source", "Openverse")}


def safe_name(item_id):
    """File-system friendly name without the extension."""
    stem = Path(item_id.split(":", 1)[1].replace("File:", "")).stem
    return re.sub(r"[^A-Za-z0-9._-]+", "_", stem)[:80]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--n", type=int, default=8)
    s.add_argument("--source", default="both", choices=["commons", "openverse", "both"])
    s.add_argument("--min-width", type=int, default=1600)
    p = sub.add_parser("preview")
    p.add_argument("ids", nargs="+")
    p.add_argument("--out", required=True)
    g = sub.add_parser("get")
    g.add_argument("id")
    g.add_argument("--out", required=True)
    g.add_argument("--width", type=int, default=1920)
    a = ap.parse_args()

    if a.cmd == "search":
        found = []
        if a.source in ("commons", "both"):
            try:
                found += search_commons(a.query, a.n, a.min_width)
            except Exception as e:
                print(f"Wikimedia Commons search failed: {e}", file=sys.stderr)
        if a.source in ("openverse", "both"):
            try:
                found += search_openverse(a.query, a.n, a.min_width)
            except Exception as e:
                print(f"Openverse search failed: {e}", file=sys.stderr)
        for i, f in enumerate(found, 1):
            print(f"{i:2}. {f['id']}\n    {f['width']}x{f['height']}  {f['licence']}  by {f['author']}\n    {f['page']}")
        print(f"\n{len(found)} candidates, nothing downloaded.")
        return

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "preview":
        from PIL import Image, ImageDraw
        thumbs = []
        for item_id in a.ids:
            rec = lookup(item_id, 400)
            dst = out / f"thumb_{safe_name(item_id)}.jpg"
            download(rec["thumb"] or rec["url"], dst)
            thumbs.append((item_id, dst))
        w, h, cols = 400, 300, 3
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + 10) + 10, rows * (h + 34) + 10), "#999999")
        draw = ImageDraw.Draw(sheet)
        for i, (item_id, path) in enumerate(thumbs):
            im = Image.open(path).convert("RGB")
            im.thumbnail((w, h))
            x, y = 10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 34)
            sheet.paste(im, (x, y))
            draw.text((x, y + h + 4), f"{i + 1}. {item_id[:60]}", fill="#000000")
        sheet.save(out / "image_candidates.png")
        print(out / "image_candidates.png")
        return

    rec = lookup(a.id, a.width)
    ext = Path(urllib.parse.urlparse(rec["url"]).path).suffix or ".jpg"
    dst = out / (safe_name(a.id) + ext)
    download(rec["url"], dst)
    credits_path = out / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else []
    credit = f"Photo: {rec['author']}, {rec['licence']}, {rec['source']}"
    credits = [c for c in credits if c["file"] != dst.name] + [
        {"file": dst.name, "credit": credit, "page": rec["page"], "id": a.id}]
    credits_path.write_text(json.dumps(credits, indent=1))
    print(f"saved {dst} ({dst.stat().st_size // 1024} KB)\ncredit: {credit}")


if __name__ == "__main__":
    main()
