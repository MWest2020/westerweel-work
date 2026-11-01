"""Maak de LinkedIn-PDF van één boekenclub-deck: één pagina per slide, 1080×1350.

    uv run --with playwright scripts/boekenclub_pdf.py seeking-sre
    # -> boekenclub-pdf/seeking-sre.pdf (en met --shots ook PNG's per slide, 1080 en 390 px breed)

Bouwt de site met hugo in een tijdelijke map, serveert die lokaal en laat Chromium
de pagina afdrukken met de print-CSS van het deck. Eenmalig: `uv run --with playwright
playwright install chromium`, of wijs BOEKENCLUB_CHROME naar een bestaande Chromium.
"""
import argparse, functools, http.server, os, subprocess, sys, tempfile, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1350


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = functools.partial(Quiet, directory=directory)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="het boek, bijvoorbeeld seeking-sre (of 'index' voor de boekenclub zelf)")
    ap.add_argument("--out", default=os.path.join(ROOT, "boekenclub-pdf"))
    ap.add_argument("--shots", action="store_true", help="ook een PNG per slide, op 1080 en op 390 px breed")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    with tempfile.TemporaryDirectory() as public:
        subprocess.run(["hugo", "--gc", "--quiet", "-d", public], cwd=ROOT, check=True)
        path = "boekenclub/" if a.slug == "index" else f"boekenclub/{a.slug}/"
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
            pdf = os.path.join(a.out, f"{a.slug}.pdf")
            page.pdf(path=pdf, width=f"{W}px", height=f"{H}px", print_background=True,
                     prefer_css_page_size=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print(f"{pdf}: {slides} slides")
            if a.shots:
                for width in (W, 390):
                    shot = browser.new_page(viewport={"width": width, "height": round(width * H / W)})
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
