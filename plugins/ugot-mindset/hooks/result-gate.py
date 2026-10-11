#!/usr/bin/env python3
"""PostToolUse hook: when a tool result looks like an experimental verdict (scores, failures, NaN, early verdicts),
inject the multi-axis reminder at the moment the agent would react to the number."""
import json, re, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
out = d.get("tool_response")
text = json.dumps(out, ensure_ascii=False) if not isinstance(out, str) else out
if re.search(r'"em"|\bEM\b|early_negative|early_positive|verdict|\bnan\b|FAIL|failed|rc=[1-9]|best EM|holdout', text or "", re.I):
    print("[다차원 사고 — 결과 게이트] 숫자에 바로 반응하지 말 것. 행동 전에 적어라: 원리(왜 그렇게 되나) · 대안 설명 2개(레시피/자/구현) · 반증(틀렸다면 무엇이 보이나). "
          "세 축 이상이 같은 방향일 때만 설계를 바꾼다; 아니면 '보류'로 기록. 스킬 multi-axis-thinking.")
