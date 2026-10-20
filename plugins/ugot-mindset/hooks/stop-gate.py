#!/usr/bin/env python3
"""Stop hook: if the final assistant message ends the turn with a permission question although nothing
irreversible is at stake, block the stop so the agent keeps going (mistake patterns 10 and 18).
0.7.7: the gates collect their reasons and print one JSON object; a dated commitment the user stated but no tool
saved to the Space calendar also blocks, once per commitment (calendar_coverage.py)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    inp = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if inp.get("stop_hook_active"):
    sys.exit(0)  # already continuing because of this hook; never loop
path = inp.get("transcript_path")
if not path:
    sys.exit(0)
last = ""
try:
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") != "assistant":
                continue
            c = (d.get("message") or {}).get("content")
            if isinstance(c, list):
                t = "".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
            elif isinstance(c, str):
                t = c
            else:
                t = ""
            if t.strip():
                last = t
except Exception:
    sys.exit(0)
tail = last.strip()[-240:]
reasons, notices = [], []
ASK = r"(할까요|진행할까|해도 될까요|해 ?드릴까요|원하시(면|나요)|어느 (쪽|것)을|선택해 ?주|알려 ?주시면|확인해 ?주시면|어떻게 할까요|괜찮을까요|shall I|would you like me|which (one|option))"
IRREVERSIBLE = r"(삭제|지우|결제|송금|발송|보내도|배포|publish|deploy|rm -rf|force|되돌릴 수 없|비밀번호|password|계정 생성|탈퇴)"
asked = re.search(ASK, tail) and tail.rstrip().endswith(("?", "？")) and not re.search(IRREVERSIBLE, tail, re.I)
if asked:
    reasons.append("[중단 게이트] 허락 질문으로 턴을 끝내려 했다. 권한은 있다: 가장 가능성 높은 쪽을 고르고 가정을 한 줄로 말한 뒤 같은 턴에서 계속 실행하라(스킬 keep-going). 되돌릴 수 없는 일(삭제·결제·외부 발송·배포)일 때만 확인을 요청한다.")
# 0.5.1 — 완료 선언 게이트 (실수 패턴 16): "완료/끝났다/통합했다"고 말하면서 빠진 것을 밝히지 않으면 한 번 되돌린다.
# 0.8.15 — 알림으로 강등(사용자 승인 2026-10-17 "요구 ID 게이트가 대신 막는다"): 산문 정규식은 구조 검사가 아니라 법이 될 수 없다
# (설계 카드 §2 I3 예외 등록부). 누락은 ledger-gate의 요구 ID 커버리지가 막고, 이 검사는 사용자에게 보이는 systemMessage만 남긴다.
DONE = r"(완료했|완료됐|완료입니다|끝냈|마쳤|다 했|모두 했|전부 했|반영했|적용했|배포했|통합했|정리했|해결했|\bdone\b|completed|integrated|finished)"  # 0.5.2: first-person work claims only — a status line like '학습이 끝났다' is not a completion claim
OMIT = r"(빠진 ?것|누락|남은 ?것|남은 ?일|못 ?한 ?것|미완|보류|remaining|omitted|left out|not done|skipped)"
body = last.strip()
if not asked and re.search(DONE, body[-400:], re.I) and not re.search(OMIT, body, re.I):
    notices.append("[완료 선언 알림] 완료라고 말하면서 '빠진 것' 줄이 없다. 요구 항목(사용자 요청·대화 중 추가된 것·내가 약속한 것)을 열거해 결과물과 대조하고, 마지막 보고에 '빠진 것: 없음' 또는 '빠진 것: 무엇(이유·언제)'을 한 줄로 넣어라. 열거 없이 '완료'는 거의 틀린다 — 다음부터는 첫 도구 호출 전에 '요구: R1 …' 블록을 쓰고 장부 met/left-out으로 닫아 장부 게이트가 대조하게 하라(스킬 spec-first).")

# 0.7.6 — 무-외상 게이트 (실수 패턴 25): "반은 아니다/나중에/다음 설계 카드"라고 말하면서 이 턴에 만든 것이 없으면 되돌린다.
DEFER = r"(반은 (그렇|맞|예|해결)|반은 아니|절반은 아니|나중에 (하|만들|고치)|다음 (설계 카드|단계|턴|라운드)(로|에서) (하|만들|다루|넘기)|설계 카드 대상|미뤄|보류합니다)"
# 0.8.36 — 진단-시정 게이트 (알아차림의 반쪽, 2026-10-20 사용자 "반만 맞게 하고 있습니다 — 이러면 즉시 행동으로 맞게 수정하는 스킬이 없어?
# 말만 하지 말고 시정을 해야지"): 내 답이 방향이 어긋났다고 스스로 진단하면서 이 턴에 만든 것(도구 호출)이 없으면 한 번 되돌린다.
DRIFT = r"(반만 (맞|하고)|절반만 (맞|하고)|제자리|곁가지|곁길|딴 길|엉뚱한 (곳|일|방향)|방향이 (틀|어긋|얇|잘못)|잘못된 방향|맞는 길이 아니|임계 경로가 아니|시간을 (낭비|허비)|(절반|반) ?넘게 .{0,12}(스킬|플러그인|도구)에 썼)"
if not asked and (re.search(DEFER, body) or re.search(DRIFT, body)):
    worked = False
    try:
        with open(path, errors="ignore") as f:
            lines = f.readlines()
        # scan back from the end to the last user message; look for Write/Edit/Bash/Agent tool uses in this turn
        for line in reversed(lines):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "user":
                c = (d.get("message") or {}).get("content")
                if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)):
                    break
            if d.get("type") == "assistant":
                c = (d.get("message") or {}).get("content") or []
                if any(isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") in ("Write", "Edit", "Bash", "Agent", "NotebookEdit") for x in c):
                    worked = True; break
    except Exception:
        worked = True
    if not worked and re.search(DRIFT, body) and not re.search(DEFER, body):
        reasons.append("[진단-시정 게이트] 방향이 어긋났다고 스스로 진단해 놓고 이 턴에 시정 행동이 없다. 알아차림은 말이 아니라 행동이다(스킬 notice-the-drift): 같은 턴에서 임계 경로의 다음 걸음을 실제로 하라 — 카드·코드·발사·중단·재배열 중 하나를 도구로 만들고, 답에는 '시정: 무엇을 했고 다음 판정이 언제인지' 한 줄을 넣어라. 진단만 적고 끝내는 것은 '반은 아니다'와 같은 외상이다.")
    elif not worked:
        reasons.append("[무-외상 게이트] '반은 아니다/나중에/다음 설계 카드'라고 말하면서 이 턴에 만든 것이 없다. 아닌 반은 지금 고쳐라: 구조 구멍이면 같은 턴에서 코드·카드로 만들고, 정말 물리적 취득 시간이나 순서 의존이면 그 이유를 한 줄로 적어라(스킬 keep-going·predictability-first; CLAUDE.md 무-외상 대전제).")

# 0.8.37 — 창자 게이트 (2026-10-20 사용자 "너는 창자야 — 매 순간마다 새로운 아이디어를 내게"): 작업 턴(이 턴의 도구 호출 ≥ IDEA_MIN_TOOLS)의
# 마지막 답에 '아이디어:' 줄이 없으면 한 번 되돌린다. IDEA_GATE_MODE=block(기본)|notice|off.
IDEA_MODE = os.environ.get("IDEA_GATE_MODE", "block")
if not asked and IDEA_MODE != "off" and not re.search(r"아이디어\s*[:：]", body):
    ntools = 0
    try:
        with open(path, errors="ignore") as f:
            lines = f.readlines()
        for line in reversed(lines):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "user":
                c = (d.get("message") or {}).get("content")
                if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)):
                    break
            if d.get("type") == "assistant":
                c = (d.get("message") or {}).get("content") or []
                ntools += sum(1 for x in c if isinstance(x, dict) and x.get("type") == "tool_use")
    except Exception:
        ntools = 0
    if ntools >= int(os.environ.get("IDEA_MIN_TOOLS", "5") or 5):
        msg = ("[창자 게이트] 작업 턴인데 마지막 답에 새 아이디어가 없다(스킬 create-every-moment). 네 생성기(구조/병명/이론/확장) 중 둘을 돌려 "
               "'아이디어: 무엇 · 메커니즘 · 선례(없으면 없음(검색어 …)) · 시험(시간)' 한 줄을 넣고, 아이디어 장부(IDEA-LEDGER.md)에 추가하라. "
               "물려받은 줄기의 재측정은 아이디어가 아니다.")
        (reasons if IDEA_MODE == "block" else notices).append(msg)

# 0.7.7 — 일정 커버리지 게이트 (Space 기능 커버리지): 날짜 있는 약속을 말했는데 일정 저장이 없으면 약속마다 한 번 되돌린다.
try:
    import calendar_coverage
    r = calendar_coverage.check(path)
    if r:
        reasons.append(r)
except Exception:
    pass
out = {}
if reasons:
    reason = "\n\n".join(reasons)
    try:  # 0.8.27 — the reply to this block becomes the final answer: ask to restate the answer first (final_answer.py)
        import final_answer
        reason = final_answer.with_contract(reason)
    except Exception:
        pass
    out.update({"decision": "block", "reason": reason})
if notices:
    out["systemMessage"] = "\n\n".join(notices)
if out:
    print(json.dumps(out, ensure_ascii=False))
