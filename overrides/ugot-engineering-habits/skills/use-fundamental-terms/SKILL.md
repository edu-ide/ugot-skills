---
name: use-fundamental-terms
description: Use when naming, renaming, explaining, or documenting a concept, capability, mechanism, law, benchmark target, or architecture primitive, especially when the user asks for a more fundamental term or says a term feels surface-level.
contract:
  trigger: "개념·능력·메커니즘·법칙·지표를 이름 짓거나 설명할 때, 용어가 표면적이라 느껴질 때"
  procedure: "표면 용어 → 근본 원리 용어로 바꾸고 이유 한 줄"
  exit_check: "바뀐 용어와 이유가 문서에 있다"
  evidence: "용어 변경 diff"
principle: fundamental-first
---

# Use Fundamental Terms

Always prefer the deepest correct term that still predicts implementation and evaluation.

## Ladder

For any proposed term, climb until the next level would stop being operational:

1. Surface artifact: what appears in data/output (`span`, EM/F1, prompt row).
2. Behavior: what the model does (`answer boundary`, `state carry`).
3. Latent state: what must exist inside the model (`answer state`, path state).
4. Information principle: what selects/compresses information (sufficient statistic, information bottleneck).
5. Project law: a short reusable sentence the team already uses to explain the principle.

## Rule

- If using a surface or benchmark term, label it as surface and immediately give the fundamental project term.
- Do not choose decorative jargon. A fundamental term must explain the mechanism, predict the next intervention, and not conflict with the project's written laws or glossary.
- Prefer Korean plus technical pairs, such as `정보 병목 (information bottleneck)`, `충분 통계량 (sufficient statistic)`.
- If unsure, check whether the term still predicts what to build and what to measure before adopting it.

## Response Pattern

When asked for a term:

`표면 용어: X. 더 근본 용어: Y. 최상위 프레임: Z. 이유: ...`

## Examples

- `span` -> `answer boundary` -> `answer state` -> `information bottleneck`.
- `multihop` -> `chained evidence lookup` -> `state carried across reasoning steps`.
- `verifier-guided answer` -> `evidence-grounded sufficient-state selection`.
