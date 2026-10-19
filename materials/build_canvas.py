"""htmls/index.html 로 Gemini Canvas에 붙여 넣기 좋은 '한 파일' 버전(canvas/linkforge_canvas.html)을 만든다.

Canvas 안에서는 다른 파일(../examples, ../materials)과 구글 시트(갤러리)에 연결할 수 없으므로
- 작품 갤러리 탭을 빼고
- 상대 경로 링크는 공개 주소로 바꾸고
- 연수 정보·공유 링크(QR)는 맨 위 CONFIG 한 곳에서 고치게 한다.

사용법: python build_canvas.py
"""
import io
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = "https://richee-pc.github.io/26AI_design/"
src = io.open(ROOT / "htmls" / "index.html", encoding="utf-8").read()
s = src


def cut(text, start, end, keep_end=True):
    """start 부터 end 앞(keep_end) 또는 end 포함까지 잘라낸다."""
    a = text.index(start)
    b = text.index(end, a + len(start))
    return text[:a] + (text[b:] if keep_end else text[b + len(end):])


def rep(a, b, count=1):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, count)


# 1) 갤러리: 스타일·탭·패널·스크립트·바로가기 제거
s = cut(s, "/* 작품 갤러리 */", "/* 방식 선택 */")
s = cut(s, "    <!-- 6. 작품 갤러리 -->", "    <!-- 6. 적용·주의 -->")
s = cut(s, "// ---------- 작품 갤러리", "\nloadGallery();\n", keep_end=False)
rep("""<a class="link-btn" href="#" onclick="go('tg');return false;">🖼️ 작품 갤러리</a>""",
    """<a class="link-btn" href="#" onclick="go('t5');return false;">🔗 링크·QR 만들기</a>""")
rep("""        <button type="button" class="tab" data-t="tg">6. 작품 갤러리</button>\n""", "")
rep(">7. 수업 적용·주의</button>", ">6. 수업 적용·주의</button>")

# 2) 연수 자료(원본 연수 PDF·사본 안내) 블록 제거
s = cut(s, '        <div class="section-head"><span></span>📂 연수 자료</div>', '        <div class="section-head"><span></span>어려운 말, 쉽게 보기</div>')

# 3) 상대 경로 → 공개 주소
s = s.replace("'../examples/jodae-quiz.html'", f"'{SITE}examples/jodae-quiz.html'")
s = s.replace('"../examples/jodae-quiz.html"', f'"{SITE}examples/jodae-quiz.html"')

# 4) 연수 정보를 CONFIG에서 채우기
rep("""        <div class="hero-badge">2026학년도 AI중점학교 교원역량 강화 연수 · 코딩 몰라도 따라갈 수 있어요</div>""",
    """        <div class="hero-badge" id="cfgBadge">교원 연수 · 코딩 몰라도 따라갈 수 있어요</div>""")
s = cut(s, "        <!-- ✏️ [사본 만들기] 연수 정보(날짜·장소·강사)는 아래 세 줄을 고치세요 -->", '        </div>\n        <aside class="hero-join"')
rep('        </div>\n        <aside class="hero-join"',
    '        <div class="hero-meta" id="cfgMeta"></div>\n        </div>\n        <aside class="hero-join"')

# 5) 첫 화면 QR: 원본 주소 대신 CONFIG.SHARE_URL (비어 있으면 카드 숨김)
s = cut(s, "// 첫 화면 입장 QR (공개 주소 고정)", "function openJoin()")
rep("function openJoin()", """// 첫 화면: 연수 정보와 입장 QR (CONFIG 에서 채움)
(function () {
    document.getElementById('cfgBadge').textContent = CONFIG.연수명 + ' · 코딩 몰라도 따라갈 수 있어요';
    document.getElementById('cfgMeta').innerHTML = [['📅', CONFIG.날짜], ['📍', CONFIG.장소], ['👩‍🏫', CONFIG.강사]]
        .filter(x => x[1]).map(x => `<span>${x[0]} ${esc(x[1])}</span>`).join('');
    const join = document.querySelector('.hero-join');
    if (!/^https?:\\/\\//.test(CONFIG.SHARE_URL)) { join.style.display = 'none'; return; }
    const shown = CONFIG.SHARE_URL.replace(/^https?:\\/\\//, '').replace(/\\/$/, '');
    const a = document.getElementById('heroUrl'); a.href = CONFIG.SHARE_URL; a.textContent = shown;
    document.getElementById('joinFullUrl').textContent = shown;
    if (!window.QRCode) return;
    new QRCode(document.getElementById('heroQR'), { text: CONFIG.SHARE_URL, width: 120, height: 120, correctLevel: QRCode.CorrectLevel.M });
    new QRCode(document.getElementById('joinFullQR'), { text: CONFIG.SHARE_URL, width: 512, height: 512, correctLevel: QRCode.CorrectLevel.M });
})();
function openJoin()""")

# 6) 맨 위 CONFIG
rep("<script>\n// ---------- 데이터 ----------", """<script>
// ✏️ 여기만 고치면 돼요! Gemini에게 "맨 위 CONFIG의 날짜를 ○○로 바꿔 줘"처럼 부탁해도 됩니다.
//    SHARE_URL: Canvas [공유]로 만든 링크를 넣으면 첫 화면에 입장 QR이 생겨요. (비우면 QR 카드가 숨겨져요)
const CONFIG = {
    연수명: '교원 역량 강화 연수',
    날짜: '2026. ○○. ○○.(○) ○○:○○~',
    장소: '○○학교 ○○실',
    강사: '○○학교 ○○ 교사 ○○○',
    SHARE_URL: ''
};
// ---------- 데이터 ----------""")

# 7) Gemini에 붙여 넣을 때 줄 맨 앞의 '* '가 마크다운 글머리표(- )로 바뀌는 문제 피하기
#    - CSS 전체 선택자는 공백 없이 시작
#    - 프롬프트 아키텍트 원문은 한 줄짜리 JS 문자열로 보관
rep("* { box-sizing: border-box; }", "*,*::before,*::after { box-sizing: border-box; }")
m = re.search(r'<script type="text/plain" id="architectText">\n([\s\S]*?)\n</script>', s)
assert m, "architectText"
import json
s = s[:m.start()] + "<script>\n// 프롬프트 아키텍트 원문 (줄바꿈은 \\n 으로 보관)\nconst ARCHITECT_TEXT = " + json.dumps(m.group(1), ensure_ascii=False) + ";\n</script>" + s[m.end():]
rep("document.getElementById('architectText').textContent.trim()", "ARCHITECT_TEXT.trim()")
_bul = [l[:40] for l in s.split("\n") if re.match(r"^\s*[*+] ", l)]
assert not _bul, "글머리표로 바뀔 줄이 남아 있어요: " + " | ".join(_bul)

# 8) 남은 갤러리 흔적·상대 경로 점검 (프롬프트 아키텍트 원문은 제외)
for word in ["loadGallery", "GALLERY_API", "data-t=\"tg\"", "id=\"tg\"", "IS_ORIGINAL_SITE"]:
    assert word not in s, word
_body = re.sub(r"<script type=\"text/plain\"[\s\S]*?</script>", "", s)
_left = [_body[max(0, m.start() - 50):m.start() + 30] for m in re.finditer(r"\.\./", _body)]
assert not _left, "상대 경로가 남아 있어요: " + " | ".join(_left)

title = "LINKFORGE for Teachers — Gemini로 수업용 웹페이지 만들기 (Canvas판)"
s = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", s, count=1)

out = ROOT / "canvas" / "linkforge_canvas.html"
out.parent.mkdir(exist_ok=True)
io.open(out, "w", encoding="utf-8").write(s)
ko = sum(1 for c in s if "가" <= c <= "힣")
print(out.name, "chars", len(s), "est_tokens", int(ko + (len(s) - ko) / 3.5))
