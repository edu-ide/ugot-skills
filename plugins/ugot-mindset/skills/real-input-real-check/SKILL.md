---
name: real-input-real-check
description: "진짜 입력·진짜 확인 — 도메인과 무관하게, 내가 만든 가짜(템플릿 데이터·픽스처·내부 점수표·자기 채점)로는 \"된다\"를 말하지 않는다. 실제 입력(공개 데이터·실제 사용자 파일·실제 요청)으로 돌리고, 지표가 아니라 실제 출력(생성문·화면·파일·응답)을 눈으로 본다. 도메인 결합: prefer-real-corpus-over-synthetic(학습 데이터), validate-on-real-benchmark(능력 주장), check-actual-output(모델 출력), pro-quality(화면·문서). (2026-10-17)"
principle: self
contract:
  trigger: "'된다/통과/해결/X.XX'를 말하기 전; 테스트·데이터·점수표를 내가 직접 만든 순간"
  trigger_when: ["tool_use:Bash~\\b(pytest|unittest|playwright test|cargo test|npm test|pnpm test|bazel test)\\b"]
  procedure: "입력을 실제 것으로 바꾸고(공개 벤치·실제 파일·실제 요청) → 지표 옆에 실제 출력 표본을 직접 열어 보고 → 자기 제작 점수표는 '연기 시험'으로만 표기"
  exit_check: "주장마다 실제 입력의 출처와 열어 본 출력 표본(경로·캡처·인용)이 붙어 있다"
  evidence: "실제 출력 표본 파일/캡처, 공개 벤치 결과 파일"
  failure_modes: [9]
  validator: []
---

# real-input-real-check — 진짜 입력, 진짜 확인

**원칙**: 내가 만든 자로 나를 재지 않는다. 입력은 실제 것, 확인은 지표가 아니라 출력 그 자체.

- 연구: 합성 게이트 23/23이 공개 벤치에서 무작위 수준이었던 기록이 이 원칙의 출생지다. 공개 데이터로 재고, 생성문을 print해서 본다.
- 소프트웨어: 픽스처로 초록불이어도 실제 사용자 파일 하나로 다시 돌린다. 스크린샷·실제 응답을 보기 전에는 "고쳤다"가 아니다.
- 문서·제품: 양식 미리보기·실제 렌더를 열어 기준과 대조한다.

자기 제작 점수표가 쓸모없다는 뜻이 아니다 — 그것은 **연기 시험**이고, 주장은 실제 입력에서만 나온다.
