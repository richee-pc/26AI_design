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

function doGet() {
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
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
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
