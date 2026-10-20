"""원본 연수 웹페이지로 '광주제일고등학교' 버전을 만든다.

- 대상: 고등학교 선생님 (중학교·중학생 표현을 고등학교로)
- 첫 화면: 연수명·주제·1기/2기 일시·장소(박종오실)·강사(김효진)
- 예시 퀴즈: examples/jeil-quiz.html (광주제일고 홈페이지 학교소개 기반)
- 작품 갤러리: 같은 Apps Script를 쓰되 board='jeil' 로 구분해 원본 갤러리와 섞이지 않게

사용법: python build_jeil.py <출력 폴더>
"""
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = Path(sys.argv[1])
API = "https://script.google.com/macros/s/AKfycbxokum72etBCOe8i1dDm-gwF5sqGV0ju_HOboKZm6lWtUiaEt9znFxXNJ-QU02a3FzB/exec"

s = io.open(ROOT / "htmls" / "index.html", encoding="utf-8").read()


def rep(a, b, count=1):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, count)


def cut(start, end):
    """start 부터 end 앞까지 잘라낸다."""
    global s
    a = s.index(start)
    b = s.index(end, a + len(start))
    s = s[:a] + s[b:]


# ---------- 제목·첫 화면 ----------
rep("<title>LINKFORGE for Teachers — Gemini로 수업용 웹페이지 만들기</title>",
    "<title>LINKFORGE for Teachers · 광주제일고 — Gemini로 수업용 웹페이지 만들기</title>")
rep('<div class="hero-badge">2026학년도 AI중점학교 교원역량 강화 연수 · 코딩 몰라도 따라갈 수 있어요</div>',
    '<div class="hero-badge">2026 AI·디지털 기반 교육혁신 거점학교 교원연수_광주제일고 · 코딩 몰라도 따라갈 수 있어요</div>')
rep("""            <span>📅 2026. 10. 19.(월) 15:30~</span>
            <span>📍 조선대학교부속중학교 1층 온나누리실</span>
            <span>👩‍🏫 조선대학교부속고등학교 정보 교사 김다은</span>""",
    """            <span>📚 생성형 AI를 활용한 수업자료 제작 실습</span>
            <span>📅 1기 2026. 10. 21.(수) 15:40~18:30</span>
            <span>📅 2기 2026. 10. 24.(토) 9:30~12:20</span>
            <span>📍 광주제일고등학교 박종오실</span>
            <span>🧑‍🏫 조선대학교부속중학교 수학 교사 김효진</span>""")
# 연수명이 길어 휴대폰에서 두 줄이 되므로 배지 모서리를 덜 둥글게
rep("padding: 0.3rem 0.85rem; border-radius: 999px; margin-bottom: 0.85rem; }",
    "padding: 0.3rem 0.85rem; border-radius: 12px; margin-bottom: 0.85rem; line-height: 1.5; }")

# ---------- 완성 예시: 광주제일고 퀴즈 ----------
rep("🍁 우리 학교 조대부중 알아보기 퀴즈", "🍁 우리 학교 광주제일고 알아보기 퀴즈")
rep("교훈·교화·교목·연혁으로 만든 10문항 퀴즈예요.", "교훈·교목·교화·연혁으로 만든 10문항 퀴즈예요.")
rep("🎯 퀴즈 게임에는 <b>조대부중 알아보기 퀴즈</b> 실제 예시가 있어요!",
    "🎯 퀴즈 게임에는 <b>광주제일고 알아보기 퀴즈</b> 실제 예시가 있어요!")
s = s.replace("../examples/jodae-quiz.html", "../examples/jeil-quiz.html")
assert "jodae" not in s

# ---------- 원본 연수 자료(조대부중 연수 PDF·사본 안내) 블록은 빼기 ----------
cut('        <div class="section-head"><span></span>📂 연수 자료</div>', '        <div class="section-head"><span></span>어려운 말, 쉽게 보기</div>')

# ---------- 중학교 → 고등학교 ----------
for a, b in [
    ('placeholder="예) 중2 사회 · 인권과 헌법"', 'placeholder="예) 고1 통합사회 · 인권 보장과 헌법"'),
    ('placeholder="예) 과학 · 중학교 2학년"', 'placeholder="예) 통합과학 · 고등학교 1학년"'),
    ('placeholder="예) 물질의 구성 - 원소와 원자"', 'placeholder="예) 물질의 규칙성 - 원소와 주기율표"'),
    ('placeholder="예) 중2 원소 단원 도입용, 8쌍 카드"', 'placeholder="예) 고1 통합과학 원소 단원 도입용, 8쌍 카드"'),
    ("중학생이 휴대폰으로 보기 편하게", "고등학생이 휴대폰으로 보기 편하게"),
    ("해설을 중학생 눈높이로", "해설을 고등학생 눈높이로"),
    ("각 개념에 중학생이 공감할 수 있는", "각 개념에 고등학생이 공감할 수 있는"),
    ("너는 중학교 수업용 디지털 활동을 설계하는", "너는 고등학교 수업용 디지털 활동을 설계하는"),
    ("2) 모든 글은 한국어, 중학생 눈높이의 쉬운 문장으로 쓴다.", "2) 모든 글은 한국어, 고등학생 눈높이의 명확한 문장으로 쓴다."),
    ("5) 학습 내용은 중학교 교육과정 수준에 맞추고", "5) 학습 내용은 고등학교 교육과정 수준에 맞추고"),
    ("중학교 선생님이 수업 시간에 바로 쓸", "고등학교 선생님이 수업 시간에 바로 쓸"),
    ("너는 중학교 수업용 웹페이지를 만드는", "너는 고등학교 수업용 웹페이지를 만드는"),
    ("너는 중학교 선생님의 학교 업무를 돕는", "너는 고등학교 선생님의 학교 업무를 돕는"),
    ("ex: '수학 일차방정식 · 영어 단어 뜻'", "ex: '수학 이차방정식 · 영어 단어 뜻'"),
    ("ex: '과학 속력-거리-시간 · 수학 일차함수 기울기'", "ex: '물리학 속력-거리-시간 · 수학 이차함수 그래프'"),
    ("Create a survey for 2nd-grade middle school students", "Create a survey for 2nd-grade high school students"),
]:
    rep(a, b)

# 남은 중학교 표현 점검 (학교 이름의 '중학교' 제외 없음 — 모두 바뀌어야 함)
import re
_body = re.sub(r"<script type=\"text/plain\"[\s\S]*?</script>", "", s).replace("조선대학교부속중학교", "")  # 강사 소속은 제외
_left = sorted(set(m.group(0) for m in re.finditer(r"[가-힣]{0,6}중(?:학교|학생|[123] )", _body)))
assert not _left, "중학교 표현이 남아 있어요: " + ", ".join(_left)

# ---------- 작품 갤러리: 같은 시트, 제일고 게시판으로 구분 ----------
rep("const MY_GALLERY_API = '';", f"const MY_GALLERY_API = '{API}';\nconst GALLERY_BOARD = 'jeil'; // 원본 갤러리와 섞이지 않도록 게시판 구분")
rep("const r = await fetch(GALLERY_API + '?t=' + Date.now());",
    "const r = await fetch(GALLERY_API + '?board=' + GALLERY_BOARD + '&t=' + Date.now());")
rep("const r = await fetch(GALLERY_API, { method: 'POST', body: JSON.stringify(data) });",
    "const r = await fetch(GALLERY_API, { method: 'POST', body: JSON.stringify({ ...data, board: GALLERY_BOARD }) });")

# ---------- 출력 ----------
(OUT / "htmls").mkdir(parents=True, exist_ok=True)
io.open(OUT / "htmls" / "index.html", "w", encoding="utf-8").write(s)
print("htmls/index.html", len(s))
