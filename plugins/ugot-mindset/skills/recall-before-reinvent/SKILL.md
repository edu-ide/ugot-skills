---
name: recall-before-reinvent
description: 기록 먼저 — 새 실험·스크립트·설계를 만들기 전, 몸·엔진 계열 교체나 외부 구조 비교 전(설계 법칙 표), 또는 "없다/안 됐다/불가능"이라 말하기 전에 이전 대화(Claude·Codex·Grok·Cursor 기록)·장부·기존 코드를 grep해 이미 있는지 확인한다. 2026-06~10 가장 많은 프로젝트에서 반복된 지적("이전 대화 확인해봐", "이미 했던 거 또?", "왜 전에 만들었던 거 비슷하게 또 만드는 느낌이지?").
contract:
  trigger: "새 실험·스크립트·설계를 만들기 전, 몸·엔진 계열 교체·외부 구조 비교 전, \"없다/안 됐다/불가능\"을 말하기 전"
  procedure: "이전 대화·장부·기존 코드 grep → 있으면 인용하고 그 위에서 시작, 없으면 검색어와 함께 \"기록에 없음\"; 교체·비교면 법칙별 지킴/어김 표"
  exit_check: "인용된 기록 경로 또는 \"기록에 없음(검색어 …)\" 한 줄이 답에 있다(교체·비교면 법칙 표)"
  evidence: "grep/검색 명령과 결과가 든 대화 줄"
  failure_modes: [8]
  validator: ["tool_use:Grep || tool_use:Bash~(grep|rg|git log|git grep) || tool_use:mcp__brain__brain_session_ops || tool_use:mcp__brain__brain_memory_ops || tool_use:mcp__brain__brain_context_ops || tool_use:mcp__ccd_session_mgmt__search_session_transcripts"]
principle: self
---

# 기록 먼저, 재발명 금지

**켜지는 순간**: 새로 만들기 직전 · "안 됐다/없다/불가능"이라 말하기 직전 · 일을 넘겨받을 때 · 사용자가 "이전에/이미/했잖아/확인해봐"라고 할 때 · 몸·엔진 계열을 바꾸거나 외부 구조와 비교·설계 카드를 쓰기 직전(기록된 설계 법칙별 지킴/어김 표). 남의 공개 구현 구조를 이식할 때 그쪽 요소의 대조는 `parity-spec` 구조 이식 모드가 맡는다(같은 대조의 반대 방향). 측정된 병의 처방으로 외부 사례·논문 구조를 올리기 직전에도 켠다: 그 저장소의 증상 조회(예: 증상 문구로 검색하는 진단 스크립트)나 보류 장부로 꺼 둔 우리 장치부터 찾는다.

## 절차 (5분)

1. **어디에 기록이 있나** — 프로젝트 장부·docs·README, 규칙 파일(CLAUDE.md·AGENTS.md), 이전 세션 기록(`~/.claude/projects`, `~/.codex/sessions`, `~/.grok/sessions`, Cursor), UGOT Space 지식망, Work 작업 기록.
2. **키워드 3개로 grep** — 기능 이름·파일 이름·사용자가 쓴 단어.
3. **찾았으면 인용하고 그 위에서 시작** — 결과·실패 이유·남은 것을 한 줄로 적고 이어서 한다.
4. **못 찾았으면 한 줄로 남긴다** — "기록에 없음(검색어: a, b, c)". 이 한 줄이 없으면 안 찾은 것이다.

## 금지

- 기억만으로 "안 했다/없다/실패했다" 단정.
- 비슷한 것을 새 이름으로 또 만들기(같은 기능 둘 = 하나로 합친다).
- 넘겨받은 틀 안에서만 찾기 — 기록 **전체**에서 효과가 가장 컸던 것부터 본다(question-the-task-first).
