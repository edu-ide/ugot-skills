---
name: one-source-of-truth
description: "정본 하나 — 도메인 무관(빌드 스크립트·레지스트리·설정·문서·스킬·데이터 생성기), 같은 것을 만드는 두 번째 생산자·사본·체인을 만들지 않는다. 새 기능은 정본을 확장(단계·옵션·필드)하고, 사본이 꼭 필요하면 생성물로 만들어 드리프트를 검사한다. 도메인 결합: ssot-extend-not-fork(빌드·체인), registry-ssot(능력 레지스트리), fork-discipline(코어/클라이언트 경계), skill_graph --sync(스킬 표 생성). (2026-10-17)"
principle: self
contract:
  trigger: "새 스크립트·레시피·설정 파일·표·생성기를 '하나 더' 만들려는 순간; 'X를 재현 가능하게/조립' 요청"
  trigger_when: ["tool_use:Write~file_path\": \"(?!/tmp/)[^\"]*\\.(py|sh|mjs|ts)\""]
  procedure: "정본이 있나 찾기(검색어 기록) → 있으면 그 위에 단계/옵션으로 확장 → 사본이 필요하면 생성물 + 드리프트 검사 → 없을 때만 새로 만들고 정본으로 등록"
  exit_check: "diff가 정본 1개의 확장이거나, 새 정본이 등록되고 같은 역할의 다른 파일이 없다"
  evidence: "확장된 정본의 diff, 또는 드리프트 검사 결과"
  failure_modes: [14]
  validator: ["tool_use:Grep || tool_use:Glob || tool_use:Bash~(grep|rg|git log|git grep|find )"]
---

# one-source-of-truth — 정본 하나

**원칙**: 같은 역할의 파일이 둘이면 반드시 갈라진다(세 개의 코퍼스 생성기가 서로 다른 능력을 빠뜨린 기록, 라우터 표가 SSOT와 갈라진 기록). 해법은 규율이 아니라 구조: 정본 하나 + 확장 + 생성물 + 드리프트 검사.

- 연구: 챔피언 빌드 체인에 단계 추가, 새 from-scratch 스크립트 금지.
- 코드: 코어/클라이언트 경계, 설정은 병합이지 대체가 아님.
- 문서·스킬: 표·목록은 데이터에서 생성(`--sync`), 손 편집은 드리프트로 실패.
