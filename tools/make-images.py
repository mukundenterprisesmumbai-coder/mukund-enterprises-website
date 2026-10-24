"""Make the fast-loading WebP copies of every site photo.

Run after adding or replacing any .jpg photo:
    python3 tools/make-images.py

For each assets/<folder>/<name>.jpg it writes, next to it:
    <name>.webp     same size as the JPEG (used on big screens)
    <name>-sm.webp  half width (used on phones)
The .jpg originals stay: Google Shopping, Merchant Center and link previews use them.
Only missing or outdated WebP files are rebuilt.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent / "assets"
FOLDERS = ["products", "branding", "factory", "hero"]
QUALITY = 78
HERO_QUALITY = 62  # home-page banner photos sit under a dark film, so they can be compressed harder


def save(im, path, quality=QUALITY):
    im.save(path, "WEBP", quality=quality, method=6)


def main():
    made = 0
    for folder in FOLDERS:
        for jpg in sorted((ROOT / folder).glob("*.jpg")):
            full, small = jpg.with_suffix(".webp"), jpg.with_name(jpg.stem + "-sm.webp")
            if full.exists() and small.exists() and min(full.stat().st_mtime, small.stat().st_mtime) >= jpg.stat().st_mtime:
                continue
            im = Image.open(jpg).convert("RGB")
            q = HERO_QUALITY if folder == "hero" else QUALITY
            save(im, full, q)
            w, h = im.size
            save(im.resize((w // 2, round(h * (w // 2) / w)), Image.LANCZOS), small, q)
            made += 1
            print(f"{jpg.relative_to(ROOT.parent)}: {jpg.stat().st_size // 1024} KB jpg -> "
                  f"{full.stat().st_size // 1024} KB webp, {small.stat().st_size // 1024} KB small webp")
    print(f"done, {made} photo(s) converted")


if __name__ == "__main__":
    main()
