"""slides_src.html에 QR을 넣어 slides.html을 만들고, Chrome으로 16:9 PDF를 출력합니다.

사용법: python build_slides.py [출력 PDF 경로]
"""
import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import qrcode
import qrcode.image.svg

URL = "https://richee-pc.github.io/26AI_design/"
HERE = Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def qr_svg(px: int) -> str:
    buf = io.BytesIO()
    qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathImage, border=1).save(buf)
    svg = re.sub(r"<\?xml[^>]*\?>", "", buf.getvalue().decode()).strip()
    return re.sub(r'width="[^"]*" height="[^"]*"', f'width="{px}" height="{px}"', svg, count=1)


def main() -> None:
    src = (HERE / "slides_src.html").read_text(encoding="utf-8")
    html = src.replace("{{QR200}}", qr_svg(200)).replace("{{QR96}}", qr_svg(96))
    out_html = HERE / "slides.html"
    out_html.write_text(html, encoding="utf-8")

    out_pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "AI_lesson_slides.pdf"
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--virtual-time-budget=15000", f"--user-data-dir={profile}",
            f"--print-to-pdf={out_pdf}", out_html.as_uri(),
        ], check=True, capture_output=True)
    print(out_pdf)


if __name__ == "__main__":
    main()
