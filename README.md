# ✨ LINKFORGE for Teachers — Gemini로 수업용 웹페이지 만들기

2026학년도 AI중점학교 교원역량 강화 연수(조선대학교부속중학교, 2026.10.19.) 실습용 웹 자료입니다.
Gemini Canvas로 수업용 웹페이지를 만들고 링크로 공유하는 35분 내외 실습 연수입니다.

👉 **공개 주소 (GitHub Pages):** https://richee-pc.github.io/26AI_design/

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
