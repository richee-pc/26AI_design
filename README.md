# 생성형 AI 수업 설계 — 중학교 선생님 실습 가이드

2026학년도 AI중점학교 교원역량 강화 연수 (조선대학교부속중학교, 2026.10.19.) 실습용 웹 자료입니다.

## 구성

| 경로 | 설명 |
|------|------|
| `app.py` | Streamlit 실행 파일 (`htmls/index.html`을 화면에 표시) |
| `htmls/index.html` | 실습 웹페이지 (설계 5단계, 프롬프트 복사, 교과별 사례, 수업 설계 캔버스) |
| `materials/AI_lesson_design_script.pdf` | 강의 원고 (A4 8쪽, 강의 멘트 포함) |
| `materials/lecture_print.html` | 강의 원고 PDF 원본 |

## 실행

```bash
pip install streamlit
streamlit run app.py
```

## 강의 원고 PDF 재생성

Chrome에서 `materials/lecture_print.html`을 열고 인쇄 → PDF로 저장(여백 없음, 배경 그래픽 켜기)하거나 headless Chrome의 `--print-to-pdf`를 사용합니다.
