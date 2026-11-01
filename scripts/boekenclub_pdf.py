"""Maak de LinkedIn-PDF van één boekenclub-deck: één pagina per slide, 1080×1350.

    uv run --with playwright --with pypdf scripts/boekenclub_pdf.py becoming-sre
    # -> boekenclub-pdf/becoming-sre.pdf (en met --shots ook PNG's per slide: 1080 px, en op een
    #    geëmuleerde telefoon van 390 px breed)

Chromium rondt de paginahoogte af (1013,04 pt); daarna zet pypdf elke pagina op precies
1080×1350 CSS-px = 810×1012,5 pt. Bouwt de site met hugo in een tijdelijke map, serveert die lokaal en laat Chromium
de pagina afdrukken met de print-CSS van het deck. Eenmalig: `uv run --with playwright
playwright install chromium`, of wijs BOEKENCLUB_CHROME naar een bestaande Chromium.
"""
import argparse, functools, http.server, os, subprocess, sys, tempfile, threading
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1350
PT_W, PT_H = W * 0.75, H * 0.75  # 1 CSS-px = 0,75 pt


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = functools.partial(Quiet, directory=directory)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def exact(pdf):
    """Zet elke pagina op precies 810×1012,5 pt; het strookje dat Chromium onderaan toevoegt, valt weg."""
    reader, writer = PdfReader(pdf), PdfWriter()
    for page in reader.pages:
        top = float(page.mediabox.top)
        for box in (page.mediabox, page.cropbox):
            box.lower_left = (0, top - PT_H)
            box.upper_right = (PT_W, top)
        writer.add_page(page)
    with open(pdf, "wb") as f:
        writer.write(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="het boek, bijvoorbeeld becoming-sre")
    ap.add_argument("--out", default=os.path.join(ROOT, "boekenclub-pdf"))
    ap.add_argument("--shots", action="store_true", help="ook een PNG per slide, op 1080 en op 390 px breed")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    with tempfile.TemporaryDirectory() as public:
        subprocess.run(["hugo", "--gc", "--quiet", "-d", public], cwd=ROOT, check=True)
        path = f"boekenclub/{a.slug}/"
        if not os.path.exists(os.path.join(public, path, "index.html")):
            sys.exit(f"geen deck op /{path}: bestaat content/nl/boekenclub/{a.slug}.md?")
        httpd = serve(public)
        url = f"http://127.0.0.1:{httpd.server_port}/{path}"
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get("BOEKENCLUB_CHROME") or None)
            page = browser.new_page(viewport={"width": W, "height": H})
            page.goto(url, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            slides = page.locator(".slide").count()
            # Geen tekst over de voettekst: in afdrukweergave staan alle slides onder elkaar.
            page.emulate_media(media="print")
            clash = page.evaluate("""() => [...document.querySelectorAll('.slide')].map((s, k) => {
                const foot = s.querySelector('.foot'); if (!foot) return null;
                const top = foot.getBoundingClientRect().top, sTop = s.getBoundingClientRect().top;
                const over = [...s.children].filter(c => c !== foot)
                    .some(c => c.getBoundingClientRect().bottom > top - 8 || c.getBoundingClientRect().top < sTop);
                return over ? k + 1 : null }).filter(Boolean)""")
            if clash:
                sys.exit(f"tekst loopt over de rand of de voettekst op slide {clash}: maak de tekst korter")
            pdf = os.path.join(a.out, f"{a.slug}.pdf")
            page.pdf(path=pdf, width=f"{W}px", height=f"{H}px", print_background=True,
                     prefer_css_page_size=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            exact(pdf)
            pages = len(PdfReader(pdf).pages)
            if pages != slides:
                sys.exit(f"{pdf}: {pages} pagina's voor {slides} slides")
            print(f"{pdf}: {slides} slides, {pages} pagina's van {W}×{H}")
            if a.shots:
                for width in (W, 390):
                    phone = width < W  # een echte telefoon: mobiele viewport en touch, zoals de LinkedIn-app
                    shot = browser.new_page(viewport={"width": width, "height": 844 if phone else H},
                                            is_mobile=phone, has_touch=phone, device_scale_factor=3 if phone else 1)
                    for k in range(1, slides + 1):
                        shot.goto(f"{url}#{k}", wait_until="networkidle")
                        shot.evaluate("document.fonts.ready")
                        shot.reload(wait_until="networkidle")
                        shot.screenshot(path=os.path.join(a.out, f"{a.slug}-{width}-{k:02d}.png"))
                    shot.close()
            browser.close()
        httpd.shutdown()


if __name__ == "__main__":
    main()
