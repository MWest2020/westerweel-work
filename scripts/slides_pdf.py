"""PDF of a deck under static/slides/<name>/ for LinkedIn: one page per slide, 1920×1080.

    uv run --with playwright --with pypdf --with pillow scripts/slides_pdf.py context-is-alles --lang nl
    # -> static/slides/<name>/<name>-<lang>.pdf  (commit it; the workshops page links to it)

The decks come from tree-presentations and are plain static files, so this serves
static/ directly (no hugo build). Each slide is photographed at 1920×1080 (JPEG,
without the language switch and the counter) and the photos become the PDF pages
(1440×810 pt). Printing the deck instead gave ~12 MB: Chromium rasterises every
tree background with its CSS filter into a 2000×3000 PNG. LinkedIn shows document
pages as images anyway; links in the PDF are not clickable.
Use BOEKENCLUB_CHROME to point at an existing Chromium, as with boekenclub_pdf.py.
"""
import argparse, functools, http.server, io, os, sys, threading
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
HIDE = "#lang,#counter{display:none!important}"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="the deck, e.g. context-is-alles (static/slides/<name>/)")
    ap.add_argument("--lang", default="nl", help="the deck language to print (nl, en)")
    a = ap.parse_args()
    deck = os.path.join(ROOT, "static", "slides", a.name)
    if not os.path.exists(os.path.join(deck, "index.html")):
        sys.exit(f"no deck at {deck}")
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=os.path.join(ROOT, "static")))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    pdf = os.path.join(deck, f"{a.name}-{a.lang}.pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("BOEKENCLUB_CHROME") or None)
        page = browser.new_page(viewport={"width": W, "height": H})
        url = f"http://127.0.0.1:{httpd.server_port}/slides/{a.name}/?lang={a.lang}"
        page.goto(url, wait_until="networkidle")
        slides = page.locator(".deck.active .slide").count()
        shots = []
        for k in range(1, slides + 1):
            page.goto(f"{url}#{k}", wait_until="networkidle")
            page.reload(wait_until="networkidle")  # the deck reads the hash on load
            page.add_style_tag(content=HIDE)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            shots.append(Image.open(io.BytesIO(page.screenshot(type="jpeg", quality=85))).convert("RGB"))
        browser.close()
    httpd.shutdown()
    shots[0].save(pdf, save_all=True, append_images=shots[1:], resolution=96, quality=85)
    pages = len(PdfReader(pdf).pages)
    if pages != slides:
        sys.exit(f"{pdf}: {pages} pages for {slides} slides")
    print(f"{pdf}: {pages} pages of {W}×{H}, {os.path.getsize(pdf) // 1024} KB")


if __name__ == "__main__":
    main()
