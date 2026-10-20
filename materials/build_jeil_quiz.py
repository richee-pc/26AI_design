"""조대부중 예시 퀴즈로 광주제일고 예시 퀴즈(examples/jeil-quiz.html)를 만든다.

문제는 광주제일고등학교 홈페이지 학교소개에서 확인한 내용만 사용
- 학교상징: https://ilgo.jge.hs.kr/sub/page.php?page_code=intro_06
- 학교연혁: https://ilgo.jge.hs.kr/sub/page.php?page_code=intro_04_10_05

사용법: python build_jeil_quiz.py <출력 폴더>
"""
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = Path(sys.argv[1])
API = "https://script.google.com/macros/s/AKfycbxokum72etBCOe8i1dDm-gwF5sqGV0ju_HOboKZm6lWtUiaEt9znFxXNJ-QU02a3FzB/exec"

s = io.open(ROOT / "examples" / "jodae-quiz.html", encoding="utf-8").read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("<title>조대부중 알아보기 퀴즈 🍁</title>", "<title>광주제일고 알아보기 퀴즈 🍁</title>")
rep("<h1>우리 학교 <span>조대부중</span> 알아보기 퀴즈</h1>", "<h1>우리 학교 <span>광주제일고</span> 알아보기 퀴즈</h1>")
rep("placeholder=\"예) 교화가 동백꽃이고, 꽃말이 '겸손한 아름다움'이라는 것\"",
    "placeholder=\"예) 1929년 광주학생독립운동이 우리 학교 학생들의 주도로 시작되었다는 것\"")
s = re.sub(r'<p class="src">문제 출처:.*?</p>',
           '<p class="src">문제 출처: <a href="https://ilgo.jge.hs.kr/sub/page.php?page_code=intro_06" target="_blank" rel="noopener">광주제일고등학교 홈페이지 학교소개(학교상징</a> · '
           '<a href="https://ilgo.jge.hs.kr/sub/page.php?page_code=intro_04_10_05" target="_blank" rel="noopener">학교연혁)</a><br>'
           '연수용 예시예요. 실시간 대결은 닉네임과 점수만 저장하고, 그 밖의 개인정보는 받지 않아요.</p>', s, count=1, flags=re.S)
rep("const MY_API = '';", f"const MY_API = '{API}';")
rep("'🏆 만점! 조대부중 박사 인증!'", "'🏆 만점! 광주제일고 박사 인증!'")

QUESTIONS = """const QUESTIONS = [
    { q: '광주제일고의 교훈 "다하라 ○○ · 이어라 ○○ · 길러라 ○○"에 들어가지 않는 것은?', o: ['충효(忠孝)', '전통(傳統)', '협동(協同)', '실력(實力)'], a: 2,
      e: '교훈은 "다하라 忠孝(충효) · 이어라 傳統(전통) · 길러라 實力(실력)"이에요.' },
    { q: '교훈 "길러라 ○○"의 빈칸에 들어갈 말은?', o: ['인성', '실력', '체력', '협동'], a: 1,
      e: '"길러라 實力(실력)"이에요. 다하라 충효, 이어라 전통과 함께 세 가지 교훈을 이뤄요.' },
    { q: '"절의(節義)"를 뜻하는 광주제일고의 교목(학교 나무)은?', o: ['은행나무', '소나무', '느티나무', '벚나무'], a: 1,
      e: '교목은 소나무예요. 굳은 절개와 의리, "절의"를 뜻해요.' },
    { q: '"겸손"을 뜻하는 광주제일고의 교화(학교를 상징하는 꽃)는?', o: ['동백꽃', '개나리', '무궁화', '장미'], a: 0,
      e: '교화는 동백꽃이에요. "겸손"을 뜻해요.' },
    { q: '"평화"를 뜻하는 광주제일고의 교색(학교 색)은?', o: ['빨강', '초록', '파랑', '노랑'], a: 2,
      e: '교색은 파랑이에요. "평화"를 뜻해요.' },
    { q: '광주제일고의 개교기념일은?', o: ['3월 2일', '5월 1일', '11월 3일', '10월 9일'], a: 1,
      e: '1920년 5월 1일 광산관을 빌려 개교했고, 이날을 개교기념일로 정했어요. 11월 3일은 학생독립운동 기념일이에요.' },
    { q: '1920년 설립 인가를 받을 때 광주제일고의 처음 학교 이름은?', o: ['광주고등보통학교', '광주서공립중학교', '광주사범학교', '광주농업학교'], a: 0,
      e: '1920년 4월 "사립 광주고등보통학교"로 설립 인가를 받았어요. 광주서공립중학교는 1938년에 바뀐 이름이에요.' },
    { q: '1929년 11월 3일, 광주제일고 학생들의 주도로 일어난 일은?', o: ['3·1운동', '6·10만세운동', '광주학생독립운동', '4·19혁명'], a: 2,
      e: '1929년 11월 3일 본교 학생들의 주도로 광주학생독립운동이 일어났어요. 학교는 1999년 학생독립운동 발상지로 문화재(광주시 기념물 제26호)에 지정되었어요.' },
    { q: '2024년 3월, 광주제일고가 지정된 것은?', o: ['마이스터고', '자율형 공립고 2.0', '국제고', '예술고'], a: 1,
      e: '2024년 3월 1일 "자율형 공립고 2.0"으로 지정되었어요. 2011학년도부터 자율형 공립고로 운영해 왔어요.' },
    { q: '2025년 10월 제106회 전국체육대회에서 광주제일고가 우승한 종목은?', o: ['축구', '야구', '농구', '배구'], a: 1,
      e: '2025년 10월 23일 제106회 전국체육대회 야구에서 우승했어요. 2024년에는 야구부 창단 100주년 기념식도 열었어요.' }
];"""
s = re.sub(r"const QUESTIONS = \[[\s\S]*?\n\];", lambda m: QUESTIONS, s, count=1)

for word in ["조대부중", "조선대학교부속중", "chosun.jge"]:
    assert word not in s, word

(OUT / "examples").mkdir(parents=True, exist_ok=True)
io.open(OUT / "examples" / "jeil-quiz.html", "w", encoding="utf-8").write(s)
print("examples/jeil-quiz.html", len(s))
