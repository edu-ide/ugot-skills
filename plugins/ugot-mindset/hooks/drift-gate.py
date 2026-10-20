#!/usr/bin/env python3
"""drift-gate (0.8.35): the MID-TURN noticing channel — "am I still doing the right thing?" asked while working, not only
at the start (question-the-task-first) or the end (critic-gate).

One script, two hook events (branch on hook_event_name):
  UserPromptSubmit  store the user's words as this session's GOAL (first 240 chars), reset the tool counter.
  PostToolUse       count tool calls; every DRIFT_EVERY (default 8) calls — or at once when the tool input shows a
                    drift smell (a `cd`/path into a different repository than the first calls of the turn) — print the
                    noticing block: the goal line + three questions (same thing? ruler measures the goal? would I start
                    this today?) + the one-line report rule.  Never blocks.  Fail-open on any error.

State: $DRIFT_STATE_DIR (default ~/.cache/ugot-mindset/drift-gate)/<session>.json. Skill: notice-the-drift.
Mistake pattern 5 ("the rule exists but does not switch on at that moment") is the reason this is a hook, not a rule.
"""
import json
import os
import re
import sys
import time

STATE = os.path.expanduser(os.environ.get("DRIFT_STATE_DIR", "~/.cache/ugot-mindset/drift-gate"))
EVERY = max(2, int(os.environ.get("DRIFT_EVERY", "8") or 8))
ACK = r"^\s*(응|ㅇㅇ|네|예|ok|okay|yes|계속|continue|고마워|감사|좋아|됐어|그래|ㅋ+|ㅎ+)[\s.!~]*$"
REPO_RE = re.compile(r"(?:cd\s+|^|\s|[\"'=(])(/(?:home|mnt|srv|opt|var|tmp)/[^\s\"';|&)]+)")


def _path(session):
    return os.path.join(STATE, f"{session or 'default'}.json")


def _load(session):
    try:
        with open(_path(session), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"goal": "", "count": 0, "repos": [], "ts": 0}


def _save(session, st):
    try:
        os.makedirs(STATE, exist_ok=True)
        with open(_path(session), "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False)
    except Exception:
        pass


def repo_of(text):
    """Top two path segments of the first absolute path in a tool input (``/home/u/proj/x`` -> ``/home/u/proj``)."""
    m = REPO_RE.search(text or "")
    if not m:
        return ""
    parts = [p for p in m.group(1).split("/") if p]
    return "/" + "/".join(parts[:3]) if len(parts) >= 3 else ""


def block(goal, count, reason):
    g = goal.replace("\n", " ").strip()
    g = (g[:160] + "…") if len(g) > 160 else g
    why = "도구 호출 %d번째" % count if reason == "cadence" else reason
    return ("[알아차림 — 방향 게이트, %s] 지금 하는 일을 처음 목표와 대 보라(스킬 notice-the-drift). 목표(사용자 말): \"%s\"\n"
            "  ① 같은 일인가 — 지금 손에 든 것이 그 목표의 임계 경로인가, 아니면 곁가지(도구·정리·재측정·설명)인가?\n"
            "  ② 자가 맞나 — 지금 보고 있는 숫자·로그가 그 목표를 재는가, 아니면 재기 쉬운 것을 재고 있나?\n"
            "  ③ 오늘 처음이라면 — 지금까지 한 것을 지우고 시작한다면 이 다음 행동을 고르겠나?\n"
            "  셋 다 '예'면 그대로 계속(아무 말 안 해도 됨). 하나라도 '아니오'면 멈추고 사용자에게 한 줄(무엇이 어긋났고 어디로 돌아가나)을 보고한 뒤 돌아간다.\n"
            "  창자: 이 턴에 새 아이디어 1개(무엇·메커니즘·선례·싼 시험) 적었나? 없으면 지금 한 줄(스킬 create-every-moment)."
            % (why, g))


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return
    ev = d.get("hook_event_name", "")
    session = d.get("session_id", "")
    if ev == "UserPromptSubmit":
        p = (d.get("prompt") or "").strip()
        st = _load(session)
        if len(p) >= 4 and not re.match(ACK, p, re.I):
            st["goal"] = p[:240]
        st["count"], st["repos"], st["ts"] = 0, [], time.time()
        _save(session, st)
        return
    if ev != "PostToolUse":
        return
    st = _load(session)
    st["count"] = int(st.get("count", 0)) + 1
    ti = d.get("tool_input") or {}
    text = json.dumps(ti, ensure_ascii=False) if not isinstance(ti, str) else ti
    repo = repo_of(text)
    reason = ""
    if repo:
        repos = st.get("repos") or []
        if not repos:
            repos = [repo]
        elif repo not in repos:
            repos.append(repo)
            reason = "다른 저장소로 이동(%s → %s)" % (repos[0], repo)
        st["repos"] = repos[-4:]
    if not reason and st["count"] % EVERY == 0:
        reason = "cadence"
    _save(session, st)
    if reason and st.get("goal"):
        print(block(st["goal"], st["count"], reason))


if __name__ == "__main__":
    main()
