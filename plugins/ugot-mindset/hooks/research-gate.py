#!/usr/bin/env python3
"""PostToolUse hook for WebSearch / WebFetch: research results must be persisted the same turn (mistake pattern 17)."""
import json, sys
try:
    inp = json.load(sys.stdin)
except Exception:
    sys.exit(0)
name = inp.get("tool_name", "")
if name in ("WebSearch", "WebFetch"):
    print("[기록 게이트: 검색 결과] 방금 얻은 조사 결과(날짜·숫자·출처·우리와의 관계)를 같은 턴에 지식망의 살아 있는 지도 문서와 저장소 SSOT 문서에 한 줄씩 적어라. 대화에만 두면 잊힌다(스킬 persist-everywhere). 적은 뒤에 답하라.")
