from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from handwriting_v2.models import RenderRequest
from handwriting_v2.presets import PAPER_PRESETS, STYLE_PRESETS


HTML = """<!doctype html>
<html><head><meta charset='utf-8'><title>Handwriting Studio V2</title>
<style>
body{font-family:system-ui;margin:2rem;background:#f4f4f4;color:#222}
.card{max-width:1000px;margin:auto;background:white;padding:1rem 1.25rem;border-radius:12px;box-shadow:0 8px 26px rgba(0,0,0,.08)}
textarea{width:100%;height:120px} select,input,button{padding:.5rem;margin:.25rem 0}
img{max-width:100%;border:1px solid #ddd;border-radius:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
</style></head><body><div class='card'>
<h2>Handwriting Studio V2</h2>
<form method='POST' action='/generate'>
<label>Text</label><br><textarea name='text'>{text}</textarea><br>
<div class='grid'>
<div><label>Style</label><br><select name='style'>{style_options}</select></div>
<div><label>Paper</label><br><select name='paper'>{paper_options}</select></div>
<div><label>Seed</label><br><input type='number' name='seed' value='{seed}'></div>
</div>
<button type='submit'>Generate</button></form>
{result}
</div></body></html>"""


class App(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        if self.path.startswith('/outputs/'):
            return self._serve_file(Path(self.path.lstrip('/')))
        self._render_page()

    def do_POST(self) -> None:
        if self.path != '/generate':
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        data = parse_qs(body)

        text = data.get('text', ['Hello from V2'])[0]
        style = data.get('style', ['balanced-cursive'])[0]
        paper = data.get('paper', ['college-lined'])[0]
        seed = int(data.get('seed', ['42'])[0])

        output = Path('outputs') / 'webapp_latest.png'
        req = RenderRequest(text=text, style=style, paper=paper, seed=seed, output_path=str(output))
        try:
            from handwriting_v2.pipeline import HandwritingStudio
            HandwritingStudio().generate(req)
            result = "<h3>Result</h3><img src='/outputs/webapp_latest.png' alt='result'>"
        except ModuleNotFoundError as exc:
            result = f"<p><b>Missing dependency:</b> {exc}. Install requirements first.</p>"
        self._render_page(text=text, style=style, paper=paper, seed=seed, result=result)

    def _serve_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'image/png')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _render_page(self, text: str = 'The quick brown fox jumps over the lazy dog.', style: str = 'balanced-cursive', paper: str = 'college-lined', seed: int = 42, result: str = '') -> None:
        style_options = ''.join(f"<option value='{k}' {'selected' if k==style else ''}>{k}</option>" for k in sorted(STYLE_PRESETS))
        paper_options = ''.join(f"<option value='{k}' {'selected' if k==paper else ''}>{k}</option>" for k in sorted(PAPER_PRESETS))
        html = HTML.format(text=text, style_options=style_options, paper_options=paper_options, seed=seed, result=result)

        payload = html.encode('utf-8')
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    server = ThreadingHTTPServer(('0.0.0.0', 8000), App)
    print('Serving on http://localhost:8000')
    server.serve_forever()


if __name__ == '__main__':
    main()
