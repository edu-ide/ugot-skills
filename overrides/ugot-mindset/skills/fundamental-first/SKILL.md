---
name: fundamental-first
description: >
  Invoke BEFORE adopting any WORKAROUND that AVOIDS a problem instead of solving its ROOT — segregation (reserve a
  subspace / separate module), gating (a conditional adapter or gate), a frozen add-on installed after training,
  route-dispatch instead of in-flow, special-casing, or "X is needed because Y can't be done." Also when asked "is this fundamental? / 꼭 이렇게
  해야됨? / 근본 해결 맞아?" The recurring failure (2026-06-25, user "그건 근본 해결이 아니잖아", "근본 first 방식으로
  해"): reaching for a FAMILIAR workaround (because it feels safe / has worked before) WITHOUT first DIAGNOSING
  whether the fundamental problem is actually unsolvable — assuming-impossible and accumulating a stack of workarounds
  that each avoid the SAME unsolved root. Concretely: proposing to reserve a separate subspace (a hidden split) to
  dodge a conflict between two training goals, when nobody had MEASURED whether unified training fails for a
  FUNDAMENTAL reason or just an OPTIMIZATION one (fixable by warmup/curriculum). A workaround chosen before the root
  is diagnosed is debt, and it ENTRENCHES the unsolved root.
contract:
  trigger: "문제를 피하는 우회(격리·게이트·post-base 설치·라우트·특수처리)를 채택하려는 순간"
  procedure: "근본 원인을 측정으로 진단(FUNDAMENTAL vs UNOPTIMIZED) → 근본 수정 시도 → 우회는 측정 후 최후"
  exit_check: "진단 측정 결과와 \"우회가 아닌 이유/우회인 이유\" 한 줄이 있다"
  evidence: "진단 측정 명령·출력"
  failure_modes: [6, 13, 15]
  validator: ["tool_use:Bash", "reply_contains:우회 || reply_contains:근본"]
principle: self
---

# fundamental-first

When a conflict/limit/erosion blocks you, the momentum move is the familiar WORKAROUND (gate it, route it, reserve a
subspace, install it post-base, special-case it). That AVOIDS the root instead of solving it — and stacks debt. STOP and
do the root diagnosis FIRST.

## The rule (do these IN ORDER, before adopting any workaround)

1. **NAME the fundamental problem** — the actual root conflict/limit in one sentence (e.g. "diversity ⊥ deterministic
   next-token on shared params", "add a capability to a full-rank body without eroding the rest", "the body's raw forward
   can't do arith"). Not the symptom ("bpb got worse"), the ROOT.
2. **CLASSIFY the proposed fix: solves-root vs avoids-root.** A workaround is anything that *segregates* (reserve/separate
   module/growth), *gates* (conditional path), *routes* (dispatch instead of in-flow), *defers* (post-base install), or
   *special-cases*. If it avoids the root, it is a workaround — say so out loud.
3. **DIAGNOSE whether the root is genuinely intractable — by MEASUREMENT, not assumption.** The key question is almost
   always: *is this a FUNDAMENTAL limit (irreducible — e.g. complexity-theoretic, no-null-space) or merely a HARD /
   UNOPTIMIZED one (fixable by better training: warmup, curriculum, regularization, gradient surgery, scale)?* Run the
   cheapest experiment that separates the two (a proxy gate, an A/B). Do NOT skip to the workaround because the root
   "feels" impossible — that is exactly the assume-impossible trap.
4. **Prefer the root solution.** Adopt a workaround ONLY after the diagnosis MEASURES the root intractable — and then LOG
   it explicitly as a workaround (debt) carrying the root-diagnosis, so it isn't mistaken for the fundamental answer.

## Why (the cost of skipping it)

Workarounds compound: each one that avoids the root makes the root harder to see and the system more fragmented (a stack
of gates/routes/reserves/installs). Worse, an *undiagnosed* workaround is often unnecessary — the root was solvable and
nobody checked. The fundamental solution is usually simpler, more general, and removes a whole class of future
workarounds at once. "근본 first" = pay the diagnosis cost up front to avoid an entrenched workaround forever.

## The diagnostic test that resolves most cases

For "can't do X in the unified/in-flow/from-scratch way" → build a PROXY (small, minutes) that pits the unified approach
(with the obvious training fixes: warmup / curriculum / regularization) against the workaround, and MEASURE. If the
unified approach matches → the workaround was avoidance, drop it. If it still fails → the limit is fundamental, the
workaround is justified, and now you can prove it. Either outcome is a win: you stop guessing.

## Sibling skills
- `no-waste` (don't re-pay for done work) — this is the QUALITY sibling: don't patch when you could solve.
- `multi-axis-thinking` — before choosing a fix, check goal, mechanism, evidence and alternatives together.
- Scaling up, adding a separate module, or growing new capacity are also workarounds; fundamental-first says
  diagnose the root FIRST, and use them only when the root is measured intractable.
