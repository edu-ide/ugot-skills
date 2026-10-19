---
name: disclose-implementation-fidelity
description: >
  PROACTIVELY disclose when you implement a SIMPLIFIED / proxy / cheap / partial version instead of the full,
  faithful method — at delivery time, NOT when asked. Whenever you take a shortcut for tractability/speed, you
  MUST surface (a) that it IS a shortcut, (b) how it differs from the ideal, (c) its limitation, (d) when it's
  insufficient + the upgrade path. Invoke whenever you choose a simpler implementation than the obvious-best, or
  before presenting any built thing as "done". Sibling of precheck-and-premortem (calibrate claims) and
  spec-first (no hidden gaps at "done").
principle: faithful-first
---

# Disclose Implementation Fidelity (no silent shortcuts)

## The failure this kills (real, 2026-06-22)

Asked for "RLPT-blend", I implemented the CHEAP version (REINFORCE on single-token correctness) which is largely
CE-REDUNDANT — and presented it as "RLPT-blend ✅ RUNNING" WITHOUT flagging that it was a weak proxy. The user only
discovered the gap by asking "what's the reward function?" → "isn't this redundant?". Had they not asked, a training
run would have been WASTED on a near-useless method, presented as if it were the real thing. That silent-shortcut is
the failure: shipping a lazy implementation as if it were faithful, leaving the user to discover the gap by chance.

## Why it happens (and why it's not OK)

Under time/scope pressure, the tractable shortcut is tempting (single-token reward is 5 lines; real info-gain needs a
rollout). Taking the shortcut can be FINE — but **hiding that you took it is not**. The user is making decisions
(spend a GPU-run? promote it?) on the assumption you built the real thing. A buried simplification corrupts those
decisions and erodes trust. "It technically runs" ≠ "it does what was asked."

## The rule (proactive, at delivery)

WHENEVER you implement something simpler than the obvious-best/faithful version, state — UPFRONT, unprompted, in the
same message you deliver it:
1. **THIS IS A SHORTCUT** — name it: "this is the cheap/proxy/partial version, not the full method."
2. **HOW IT DIFFERS** — one line: what the faithful version does that this doesn't (e.g. "single-token correctness ≈
   CE-redundant; real RLPT rewards generated-reasoning info-gain").
3. **THE LIMITATION** — what it can't do / where it's weak (e.g. "adds little signal beyond CE").
4. **WHEN IT'S INSUFFICIENT + UPGRADE PATH** — "if X shows no gain → upgrade to Y (cost Z)."
Then let the user choose cheap-now vs faithful-now. Default to the FAITHFUL method for anything that will be
MEASURED/PROMOTED (a weak proxy wastes the measurement); the shortcut is only for a throwaway smoke.

## Decision rule (one line)

Took a shortcut? SAY SO in the delivery message — shortcut-flag + diff + limitation + upgrade-path — before the user
has to ask. For anything measured/promoted, build the faithful version by default; never present a proxy as the real
method. Silent simplification = the failure.

## Anti-patterns

- Presenting a proxy/cheap version as "✅ done / RUNNING" with no fidelity caveat — THE failure.
- Burying the limitation until asked ("정직한 한계: ..." only after a probe) — too late; §3 is proactive.
- Choosing the shortcut for a MEASURED/PROMOTED artifact (wastes the run) — use the faithful version there.
- Conflating "it runs" with "it does what was asked" — runs ≠ faithful.

## Relationship to sibling skills

- `precheck-and-premortem` — calibrate CLAIMS (VERIFIED vs unverified) before asserting.
- `spec-first` — enumerate what is missing before calling anything done.
- `disclose-implementation-fidelity` (this) — proactively flag a SHORTCUT/proxy implementation at delivery, before asked.

