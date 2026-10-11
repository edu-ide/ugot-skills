---
name: precheck-and-premortem
description: "Use BEFORE claiming \"this works / no problem / it's done / it'll be fine\" OR before committing to a plan/build. Forces a theoretical PRE-CHECK (recall + read + reason against the laws) and a PRE-MORTEM (enumerate failure modes + plan the fix in advance) FIRST, then a CALIBRATED claim (VERIFIED vs EXPECTED-but-unverified). Prevents the flip-flop where you assert \"no problem\" then reverse later. Triggers on: about to say works/fine/no-problem/done/should-work, about to launch a build/experiment, \"이론상 문제 없는지\", \"말이 자꾸 달라\", planning a multi-step or expensive action."
---

# Pre-check + pre-mortem before claiming

**The failure this prevents (2026-06-19, real, repeated):** I said "works / no problem" then reversed it again and again
in one session — a method "works"→blocked (a stage was never scripted); dataset "wrong, fix it"→actually right (and
better); a feature "not applied"→already integrated; A/B "fixed"→still asserted. Every reversal happened because I
CLAIMED before CHECKING. The user: "넌 분명 문제 없다 했는데 자꾸 말이 달라져서." Confidence is not consistency;
verification is.

## The mandate (do this BEFORE any "works/no-problem/done" claim or plan commitment)
1. **PRE-CHECK theoretical soundness.**
   - RECALL: read the project's status table + grep the ledger for this exact thing (is it already done / already rejected / already measured?).
   - READ: open the actual code/script/config — do not assume what it does.
   - REASON: walk the mechanism against the project's written rules and architecture contracts, and against past rejections. Does it violate a known rule? Has this been blocked before?
2. **PRE-MORTEM (imagine it already failed — why?).**
   - Enumerate the concrete failure modes: missing dependency/stage, stale reference, dilution, leakage, index/shape bug, regression of existing capabilities, GPU/process collision, etc.
   - For each plausible one, plan the check or fix IN ADVANCE (a probe, a guard, a fallback). A cheap probe before an expensive build is the whole point.
3. **CALIBRATE the claim to evidence.** State which it is:
   - **VERIFIED** — "ran/read/proved: <evidence>" → confident claim OK.
   - **EXPECTED but UNVERIFIED** — "should work because <reason>; RISK = <X>; PLAN = <probe/fix Y>" → do NOT say "no problem".
   Never assert "no problem / it works" on an unverified thing. If unchecked, the honest output is the risk + plan, not a yes.

## Why this gives consistency
The story stops changing when the claim is anchored to a check, not to optimism. A pre-mortem surfaces the blocker
BEFORE you assert success, so you don't have to retract it later. Cheap-probe-before-expensive-commit also saves the
multi-hour build that would have failed at an unchecked stage.

## Pairs with
`recall-before-reinvent` (check the record before claiming) · `doubt-and-verify` (verify before asserting) ·
`multi-axis-thinking` (when checks converge negative, question the frame).
This skill is the umbrella: pre-check + pre-mortem + calibrate, BEFORE the claim — every time.
