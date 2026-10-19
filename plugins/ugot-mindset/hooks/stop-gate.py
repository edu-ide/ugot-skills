#!/usr/bin/env python3
"""Stop hook: if the final assistant message ends the turn with a permission question although nothing
irreversible is at stake, block the stop so the agent keeps going (mistake patterns 10 and 18)."""
import json, re, sys
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
ASK = r"(할까요|진행할까|해도 될까요|해 ?드릴까요|원하시(면|나요)|어느 (쪽|것)을|선택해 ?주|알려 ?주시면|확인해 ?주시면|어떻게 할까요|괜찮을까요|shall I|would you like me|which (one|option))"
IRREVERSIBLE = r"(삭제|지우|결제|송금|발송|보내도|배포|publish|deploy|rm -rf|force|되돌릴 수 없|비밀번호|password|계정 생성|탈퇴)"
if re.search(ASK, tail) and tail.rstrip().endswith(("?", "？")) and not re.search(IRREVERSIBLE, tail, re.I):
    print(json.dumps({"decision": "block", "reason": "[중단 게이트] 허락 질문으로 턴을 끝내려 했다. 권한은 있다: 가장 가능성 높은 쪽을 고르고 가정을 한 줄로 말한 뒤 같은 턴에서 계속 실행하라(스킬 keep-going). 되돌릴 수 없는 일(삭제·결제·외부 발송·배포)일 때만 확인을 요청한다."}, ensure_ascii=False))
    sys.exit(0)
# 0.5.1 — 완료 선언 게이트 (실수 패턴 16): "완료/끝났다/통합했다"고 말하면서 빠진 것을 밝히지 않으면 한 번 되돌린다.
DONE = r"(완료했|완료됐|완료입니다|끝냈|마쳤|다 했|모두 했|전부 했|반영했|적용했|배포했|통합했|정리했|해결했|\bdone\b|completed|integrated|finished)"  # 0.5.2: first-person work claims only — a status line like '학습이 끝났다' is not a completion claim
OMIT = r"(빠진 ?것|누락|남은 ?것|남은 ?일|못 ?한 ?것|미완|보류|remaining|omitted|left out|not done|skipped)"
body = last.strip()
if re.search(DONE, body[-400:], re.I) and not re.search(OMIT, body, re.I):
    print(json.dumps({"decision": "block", "reason": "[완료 선언 게이트] 완료라고 말하면서 빠진 것을 밝히지 않았다. 요구 항목(사용자 요청·대화 중 추가된 것·내가 약속한 것)을 열거해 결과물과 대조하고, 마지막 보고에 '빠진 것: 없음' 또는 '빠진 것: 무엇(이유·언제)'을 한 줄로 넣어라(스킬 spec-first). 열거 없이 '완료'는 거의 틀린다."}, ensure_ascii=False))

# 0.7.6 — 무-외상 게이트 (실수 패턴 25): "반은 아니다/나중에/다음 설계 카드"라고 말하면서 이 턴에 만든 것이 없으면 되돌린다.
DEFER = r"(반은 (그렇|맞|예|해결)|반은 아니|절반은 아니|나중에 (하|만들|고치)|다음 (설계 카드|단계|턴|라운드)(로|에서) (하|만들|다루|넘기)|설계 카드 대상|미뤄|보류합니다)"
if re.search(DEFER, body):
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
    if not worked:
        print(json.dumps({"decision": "block", "reason": "[무-외상 게이트] '반은 아니다/나중에/다음 설계 카드'라고 말하면서 이 턴에 만든 것이 없다. 아닌 반은 지금 고쳐라: 구조 구멍이면 같은 턴에서 코드·카드로 만들고, 정말 물리적 취득 시간이나 순서 의존이면 그 이유를 한 줄로 적어라(스킬 keep-going·predictability-first; CLAUDE.md 무-외상 대전제)."}, ensure_ascii=False))
        sys.exit(0)
