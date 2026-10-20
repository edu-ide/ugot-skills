---
name: route-by-situation
description: "Invoke at the start of EVERY new request (the hook reminds you): read what UGOT Space already knows about it, classify the situation on the development flow, and write ONE routing line (\"상황 → 스킬 경로\") before the first tool call — then follow that route. Hooks only inject Space search hits and generic gates; nobody decided which skills apply to THIS request, so the 300+ skills stayed unused while the agent improvised ."
contract:
  trigger: "새 요청을 받을 때마다(한 줄 답 제외)"
  trigger_when: ["always"]
  procedure: "Space 읽기 → 세 갈림길·단계 판정 → \"상황 → 스킬 경로\" 한 줄 + 첫 도구 호출로 장부 declare → 그 스킬을 실제로 켬 (요구 선언과 닫기는 spec-first)"
  exit_check: "경로가 글 또는 장부 declare로 첫 작업 도구 전에 선언돼 있고, 경로 스킬마다 닫는 줄(met --skills 또는 applied/skipped)이 있다"
  evidence: "skill-ledger JSONL의 route/applied/skipped 줄"
  failure_modes: [5]
  validator: ["reply_contains:경로 || ledger:declare", "ledger:applied || ledger:met || ledger:skipped"]
principle: self
---

# route-by-situation

## 1. Read your project's records first (what, not whether)

Before classifying, read what already exists about this request: earlier decisions, files and preferences on the
topic; past measurements or benchmarks before re-measuring; open work and its owner before starting a parallel
version. Where those live depends on your setup (a knowledge base, a wiki, bench result files, an issue tracker).
The internal UGOT cut reads UGOT Space (memory, knowledge graph, work records) through MCP tools and writes the
decision back at the end; the rule is the same without them: read first, write back after, never only to chat.

## 2. Classify on the flow, then write the routing line

Answer the three forks, pick the stage, and emit one line before acting, e.g.
`상황: 기준 제품 있음(Premiere)·엔진 교체 → 경로: craft-spec → design-turn-first → parity-spec → TDD → multi-ruler`

<!-- skill-graph:dev begin -->
_생성 블록 — 정본은 내부 마켓의 `tools/skill-graph.json`(dev 흐름). 공개판에는 이 저장소에 있는 스킬만 표시했고, 내부판 표에는 개발·연구 스킬이 더 있다._

| 단계 | 물음·켜지는 순간 | 후보 스킬 |
|---|---|---|
| 0. 요청 받음 | 목표를 먼저 고정 — 첫 도구 호출 전에 요구를 ID로(요구: R1..Rn). 보고 요청≠중단 요청 | `route-by-situation` · `spec-first` · `question-the-task-first` · `read-the-intent` · `visual-first` · `speak-human` · `human-understands` · `multi-axis-thinking` · `set-the-persona` · `set-the-lens` · `set-the-kpis` · `five-w-one-h` · `set-the-format` · `set-the-constraints` · `every-means-now` |
| 1. 기록부터 | 목표·확정 결정·열린 작업·정본·스킬 관계 확인 · 문제 규칙은 개선안 제안 | `reference-first` · `improve-governing-rules` · `recall-before-reinvent` · `pick-the-sources` |
| 기준 제품·API·표준·공개 구현이 있나? | "X급·X 같은"이거나, 남의 모델·논문·저장소 구조를 이식하거나 다시 만들면 예 | — |
| 2a. 빼기 스펙 | 대상 버전·카탈로그·gaps·축별 %·자 | — |
| 2b. 기능 스펙 | 시나리오·요구사항만. 숫자 지어내지 않음 | `audit-convention-fit` · `use-fundamental-terms` |
| 새 모듈·엔진 교체·책임 혼재·반복 작업을 줄일 구조 변경? | 하나라도 예면 설계 턴 | — |
| 3. 설계 턴 | 소유권·의존·다음 변경→불변식→검사 설치→기능 | `design-turn-first` · `solve-first` · `architecture-consultation` · `model-real-cardinality` · `check-latest-literature` · `native-architecture-sprint` · `calibrated-architecture-research` · `harvest-to-shorten` · `explain-the-intent` |
| 외부 엔진·라이브러리 채택? | Storytold처럼 가져올 때 | — |
| 4. 실측·수용 검사 | 통과 포맷만 교체. 포크·rev 고정 | `predictability-first` · `build-right-the-first-time` |
| 5. 구현 | 선택한 기능 완성. 설계한 소유자·처리 경로로 연결 | `add-without-breaking` · `one-source-of-truth` · `faithful-first` · `build-right-the-first-time` · `human-understands` · `keep-going` · `no-waste` · `safe-process-control` · `sprout-loop` · `every-means-now` |
| 6. 버그·장애 | 왜 사슬→원인 ID→근본 해결→사고·장치 기록 | `incident-root-fix` · `fundamental-first` · `solve-first` · `every-means-now` |
| 7. 검증 | 자 하나로 판정 금지. 직접 본 뒤 보고 | `blame-the-instrument-first` · `real-input-real-check` · `multi-ruler` · `pro-quality` · `doubt-and-verify` · `disclose-implementation-fidelity` · `precheck-and-premortem` |
| 8. 완료 선언 전 | 요구 ID마다 met/left_out — 장부 게이트가 대조, 빠진 것은 보고에 밝힘 | `spec-first` · `mistake-review` · `human-understands` · `honest-eta` · `explain-the-intent` |
| 9. 기록 | 확정 결정→정본 갱신→Space·Work 연결→재조회 | `persist-everywhere` |
<!-- skill-graph:dev end -->

Skills attached to a graph node are candidates, not a mandatory checklist. Read each selected skill’s actual scope; similarly named skills may target different domains.

Rules: the routing line is one line, in the user's language, and it is the first thing in the reply. If a
fork cannot be answered from Space + the request, say which one and make the smallest safe assumption
(`keep-going`); never ask the user to pick a skill. Re-route when the situation changes mid-task (a feature
request turns into an engine replacement → go back to F2/F3). A skill named in the route is invoked, not
merely mentioned.

## 3. What this is not

Not a checklist to recite. The value is the decision: which fork this request sits on. If the request is a
one-line answer ("몇 시야", "그 파일 어디"), the route is `read-the-intent` → answer; do not inflate it.

## 4. Leave the route where something can check it

A skill named in the routing line is not "applied" because you said so. Keep the route where a check can read it
later: the routing line itself is the minimum record, and the final report says which routed skills were applied
(with the file or output that proves it) and which were skipped, with one of four reasons — 해당없음 (not
applicable), 이미됨 (already done), 측정없음 (nothing to measure), 시간 (no time).

The internal UGOT cut goes further: a skill ledger (JSONL) records the route and each requirement with its
evidence, and a Stop hook compares the two before the turn may end. That ledger and gate are not in this public
cut yet; the rule is the same without them. Verdicts on a skill (타당·약함·틀림) come from an independent critic,
never from the author.

## 유래·사례 (description에서 이동, 2026-10-17)

(2026-10-15, user: "대화 시작할 때 Space 읽기 → 문맥 파악 → 어떤 스킬 쓸지 자체 판단 → 후속 스킬, 이런 식으로 되는 거 아니야?") The flows' single source of truth is `tools/skill-graph.json` in ugot-claude-plugins (6 flows: dev, research, writing, product, space, ops — every shipped skill hangs on a node, checked by `tools/skill_graph.py --check`); the vault folder `knowledge-network/skill-flows/` holds the generated notes and canvases. The table below is the dev flow's copy for machines without either. Also on 어떤 스킬 써 / 스킬 경로 / 문맥 파악부터 / Space 먼저.
