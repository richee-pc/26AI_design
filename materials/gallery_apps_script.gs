/**
 * LINKFORGE for Teachers — 작품 갤러리 저장소 (Google Apps Script)
 *
 * 설치 방법 (5분)
 * 1) sheet.new 로 새 구글 시트를 만든다. (이름 예: LINKFORGE 갤러리)
 * 2) 메뉴 [확장 프로그램 → Apps Script] → 기본 코드를 지우고 이 파일 내용을 붙여 넣고 저장.
 * 3) [배포 → 새 배포] → 유형: 웹 앱
 *      - 다음 사용자 인증 정보로 실행: 나
 *      - 액세스 권한이 있는 사용자: 모든 사용자
 *    → [배포] → 권한 승인 → 나오는 "웹 앱 URL"(…/exec)을 복사.
 * 4) htmls/index.html 의 GALLERY_API = '' 안에 그 URL을 넣는다.
 *
 * 관리
 * - 시트의 '숨김' 열에 아무 글자(예: x)나 적으면 그 작품은 갤러리에 보이지 않는다.
 * - 코드를 고친 뒤에는 [배포 → 배포 관리 → 수정 → 새 버전]으로 다시 배포해야 반영된다.
 *
 * 실시간 대결 점수판 (examples/jodae-quiz.html 의 '각자 휴대폰 대결')
 * - '대전' 시트에 방 코드별 참가자 점수를 저장한다. GET ?room=1234 로 순위를 읽는다.
 * - 연수가 끝난 뒤 '대전' 시트의 행은 지워도 된다.
 */
const SHEET_NAME = '갤러리';
const HEADERS = ['id', '등록시각', '이름', '교과', '제목', '소개', '유형', '링크', '삭제키', '숨김'];
const LIMITS = { name: 30, subject: 30, title: 60, desc: 200, type: 30, url: 500 };

function sheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
  }
  return sh;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// 시트 수식으로 해석되지 않도록 앞에 ' 를 붙이고 길이를 자른다
function clean_(v, max) {
  let s = String(v == null ? '' : v).replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

const BATTLE_SHEET = '대전';
const BATTLE_HEADERS = ['방', '참가자id', '닉네임', '점수', '맞힌 수', '푼 문제', '갱신시각'];

function battleSheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(BATTLE_SHEET);
  if (!sh) {
    sh = ss.insertSheet(BATTLE_SHEET);
    sh.appendRow(BATTLE_HEADERS);
    sh.setFrozenRows(1);
  }
  return sh;
}

// 방 코드는 숫자 4~6자리. 시트에서 숫자로 바뀌지 않도록 'r'을 붙여 저장한다
function roomKey_(v) {
  const digits = String(v || '').replace(/\D/g, '').slice(0, 6);
  return digits.length >= 4 ? 'r' + digits : '';
}

function battleBoard_(room) {
  const key = roomKey_(room);
  if (!key) return out_({ ok: false, error: '방 코드는 숫자 4~6자리예요.' });
  const best = {};
  battleSheet_().getDataRange().getValues().slice(1)
    .filter(function (r) { return r[0] === key; })
    .forEach(function (r) {
      const p = { pid: r[1], nick: r[2], score: Number(r[3]) || 0, correct: Number(r[4]) || 0, done: Number(r[5]) || 0, at: r[6] };
      const old = best[p.pid];
      if (!old || p.done > old.done || (p.done === old.done && p.score > old.score)) best[p.pid] = p;
    });
  const players = Object.keys(best).map(function (k) { return best[k]; })
    .sort(function (a, b) { return b.score - a.score || b.correct - a.correct; });
  return out_({ ok: true, room: key.slice(1), players: players });
}

function battleUpsert_(d) {
  const key = roomKey_(d.room);
  if (!key) return out_({ ok: false, error: '방 코드는 숫자 4~6자리예요.' });
  const pid = 'p' + String(d.pid || '').replace(/[^a-zA-Z0-9]/g, '').slice(0, 24);
  const nick = clean_(d.nick, 12) || '익명';
  const score = Math.max(0, Math.min(100000, Math.round(Number(d.score) || 0)));
  const correct = Math.max(0, Math.min(100, Math.round(Number(d.correct) || 0)));
  const done = Math.max(0, Math.min(100, Math.round(Number(d.done) || 0)));
  const sh = battleSheet_();
  const last = sh.getLastRow();
  const values = last > 1 ? sh.getRange(2, 1, last - 1, 6).getValues() : [];
  for (let i = values.length - 1; i >= 0; i--) {
    if (values[i][0] === key && values[i][1] === pid) {
      // 늦게 도착한 예전 기록이 최신 점수를 덮어쓰지 않도록 푼 문제 수가 줄어드는 갱신은 무시한다
      // 단, 푼 문제 0(다시 입장)은 새 게임 시작이므로 덮어쓴다
      if (done > 0 && done < (Number(values[i][5]) || 0)) return out_({ ok: true, skipped: true });
      sh.getRange(i + 2, 3, 1, 5).setValues([[nick, score, correct, done, new Date()]]);
      return out_({ ok: true });
    }
  }
  // 새 참가자 줄 추가만 짧게 잠근다 (동시에 들어온 두 사람이 같은 줄에 쓰지 않도록)
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(8000)) return out_({ ok: false, error: '입장하는 사람이 많아요. 잠시 후 다시 시도해 주세요.' });
  try {
    const n = sh.getLastRow();
    const again = n > 1 ? sh.getRange(2, 1, n - 1, 2).getValues() : [];
    for (let j = again.length - 1; j >= 0; j--) {
      if (again[j][0] === key && again[j][1] === pid) {
        sh.getRange(j + 2, 3, 1, 5).setValues([[nick, score, correct, done, new Date()]]);
        return out_({ ok: true });
      }
    }
    sh.appendRow([key, pid, nick, score, correct, done, new Date()]);
    return out_({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  if (e && e.parameter && e.parameter.room) return battleBoard_(e.parameter.room);
  const rows = sheet_().getDataRange().getValues().slice(1);
  const items = rows
    .filter(function (r) { return r[0] && !String(r[9]).trim(); })
    .map(function (r) {
      return { id: r[0], at: r[1], name: r[2], subject: r[3], title: r[4], desc: r[5], type: r[6], url: r[7] };
    })
    .reverse();
  return out_({ ok: true, items: items });
}

function doPost(e) {
  let body;
  try { body = JSON.parse((e && e.postData && e.postData.contents) || '{}'); }
  catch (err) { return out_({ ok: false, error: '잘못된 요청이에요.' }); }
  if (body.action === 'battle') {
    try { return battleUpsert_(body); } catch (err) { return out_({ ok: false, error: String(err) }); }
  }
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return out_({ ok: false, error: '접속이 많아요. 잠시 후 다시 시도해 주세요.' });
  try {
    const d = body;
    const sh = sheet_();

    if (d.action === 'delete') {
      const values = sh.getDataRange().getValues();
      for (let i = 1; i < values.length; i++) {
        if (values[i][0] === d.id && values[i][8] && values[i][8] === d.key) {
          sh.deleteRow(i + 1);
          return out_({ ok: true });
        }
      }
      return out_({ ok: false, error: '삭제할 작품을 찾지 못했어요.' });
    }

    const url = String(d.url || '').trim();
    if (!/^https:\/\/\S+$/.test(url)) return out_({ ok: false, error: '링크는 https:// 로 시작해야 해요.' });
    if (!String(d.title || '').trim()) return out_({ ok: false, error: '작품 제목을 적어 주세요.' });
    if (d.website) return out_({ ok: true, id: 'skip' }); // 자동 등록 봇 차단용 빈칸

    const id = 'g' + Utilities.getUuid().slice(0, 8); // 숫자로 바뀌지 않도록 글자로 시작
    const key = clean_(d.key, 40);
    sh.appendRow([
      id, new Date(),
      clean_(d.name, LIMITS.name), clean_(d.subject, LIMITS.subject), clean_(d.title, LIMITS.title),
      clean_(d.desc, LIMITS.desc), clean_(d.type, LIMITS.type), clean_(url, LIMITS.url),
      key, ''
    ]);
    return out_({ ok: true, id: id });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}
