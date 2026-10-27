"""Make smaller AVIF copies of the site photos, at the same pixel size as the JPG.

Run from the repo root after adding or replacing a photo:  python3 tools/make-avif.py
- assets/products, assets/branding, assets/factory: name.avif (same size) + name-480.avif (for small cards)
- assets/hero: name.avif at the same size as the existing name.webp
The JPG stays as the fallback for old browsers and for Google Shopping / share previews.
A copy is skipped when it would not be clearly smaller than the original.
"""
import glob, io, os
from PIL import Image

def save_avif(im, path, quality, compare_to):
    buf = io.BytesIO()
    im.save(buf, 'AVIF', quality=quality, speed=4)
    if len(buf.getvalue()) > 0.92 * os.path.getsize(compare_to):
        if os.path.exists(path): os.remove(path)
        return False
    open(path, 'wb').write(buf.getvalue())
    return True

for folder in ('products', 'branding', 'factory'):
    for jpg in sorted(glob.glob(f'assets/{folder}/*.jpg')):
        base = jpg[:-4]
        im = Image.open(jpg).convert('RGB')
        if not save_avif(im, base + '.avif', 72, jpg):
            print('kept JPG only:', jpg); continue
        if im.width > 600:
            small = im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS)
            save_avif(small, base + '-480.avif', 72, base + '.avif')

for webp in sorted(glob.glob('assets/hero/*.webp')):
    base = webp[:-5]
    size = Image.open(webp).size
    im = Image.open(base + '.jpg').convert('RGB').resize(size, Image.LANCZOS)
    save_avif(im, base + '.avif', 62, webp)
