# 그림을 Space 자산으로 남기는 법

visual-first 도구 절의 세부. 그림은 사용자의 이해를 쌓는 자산이다. 호스트(Claude·ChatGPT) 안에만 남는 그림은 대화가 끝나면 사용자 것이 아니다.

## 이 호스트가 Space 위젯을 그리나

- Claude 데스크톱 Code 탭은 **앱이 관리하는 서버**(설정 → 확장의 .mcpb, claude.ai 커넥터)의 위젯만 그린다. Claude Code 설정(`~/.claude.json`·`.mcp.json`)에 등록한 서버의 위젯은 텍스트로 떨어진다. 도구 이름의 접두사(`mcp__Ugot_Brain__…` = 확장, `mcp__brain__…` = 설정 서버)는 등록 위치를 알아보는 표지일 뿐이다.
- Code 탭에서 보려면 `tools/claude-extensions/dist/ugot-brain.mcpb`(모노레포)를 설정 → 확장 → 고급 → 설치로 한 번 넣는다(사용자 몫). 새 세션부터 붙는다.
- 터미널 CLI·Codex는 위젯을 그리지 않는다. Claude.ai·ChatGPT에서 Brain 위젯이 그려지는지는 아직 실측하지 않았다.

## 저장 형식과 경로

- 위젯 📌와 같은 형식: `brain_artifact_ops save`, session_id `ugot-visuals`(세션이 없을 때), artifact_type `visuals/<slug>.html`. 내용은 `<style id="ugot-theme">:root{…테마 변수…}</style>`를 품은 문서다. 캔버스가 열 때 이 블록을 현재 테마로 바꿔 끼운다.
- `artifact_type`은 vault 기준 상대 경로다. 노트는 `Projects/<프로젝트>/<제목>.md`, 보드는 JSON Canvas를 `<경로>/<이름>.canvas`로 저장한다(file 카드에 `visuals/*.html`을 넣으면 샌드박스로 그려진다). 그다음 Space에서 연다.
- 색은 위젯 테마 변수(`--color-text-primary` 등)만 쓴다. 고정 색을 쓰면 다크 보드에서 흰 상자가 된다.

## 긴 설명·보고서

Space 노트·캔버스를 먼저 쓴다. claude.ai Artifact는 Space를 볼 수 없는 사람에게 공유해야 할 때만 쓰고, 그때도 사본은 vault에 둔다.
