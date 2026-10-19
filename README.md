# ✨ LINKFORGE for Teachers — Gemini로 수업용 웹페이지 만들기

2026학년도 AI중점학교 교원역량 강화 연수(조선대학교부속중학교, 2026.10.19.) 실습용 웹 자료입니다.
Gemini Canvas로 수업용 웹페이지를 만들고 링크로 공유하는 35분 내외 실습 연수입니다.

👉 **공개 주소 (GitHub Pages):** https://richee-pc.github.io/26AI_design/

📦 **내 연수용 사본 만들기:** [사본 만들기 안내](https://richee-pc.github.io/26AI_design/copy-guide.html) · 이 저장소는 템플릿이라 **Use this template → Create a new repository**로 바로 복사할 수 있어요. 고칠 곳은 파일에서 `✏️ [사본 만들기]`를 찾으세요.

## 연수 흐름 (35분)

1. 오늘 할 일 — 완성 예시, 왜 수업용 웹페이지인가 (5분)
2. 아이디어 — 퀴즈·개념 카드·시뮬레이션·활동 안내·수업 도구·출구티켓 (5분)
3. 프롬프트 — 빈칸을 채우면 부탁문 자동 완성 (3분)
4. 화면 만들기 — Gemini Canvas로 생성, 고치기 부탁문으로 수정 (14분)
5. 공유하기 — Canvas 공유 링크 → QR 만들기 (3분)
6. 수업 적용·주의사항, 심화(GitHub + Streamlit 배포) 안내 (5분)

## 구성

| 경로 | 설명 |
|------|------|
| `app.py` | Streamlit 실행 파일 (`htmls/index.html`을 화면에 표시) |
| `htmls/index.html` | 실습 웹페이지 (탭 1~6 + 심화) |
| `materials/AI_lesson_slides.pdf` | 발표 슬라이드 (16:9, 8장) |
| `materials/slides_src.html`, `materials/build_slides.py` | 슬라이드 원본과 PDF 생성 스크립트 |
| `materials/AI_lesson_design_script.pdf` | 강의 원고 (A4 8쪽, 강의 멘트 포함) |
| `materials/lecture_print.html` | 강의 원고 PDF 원본 |

## 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 작품 갤러리 연결 (Google Sheets + Apps Script)

6번 탭 "작품 갤러리"는 구글 시트에 작품 목록을 저장합니다. 연결 전에는 "준비 중"으로 표시됩니다.

1. [sheet.new](https://sheet.new)로 새 구글 시트 만들기
2. **확장 프로그램 → Apps Script** → `materials/gallery_apps_script.gs` 내용을 붙여 넣고 저장
3. **배포 → 새 배포 → 웹 앱** (실행: 나 / 액세스: 모든 사용자) → 권한 승인 → 웹 앱 URL(`…/exec`) 복사
4. `htmls/index.html`의 `const GALLERY_API = '';`에 URL을 넣고 커밋

관리: 시트의 `숨김` 열에 `x`를 적으면 그 작품이 갤러리에서 숨겨집니다.
