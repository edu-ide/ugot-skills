---
name: incident-root-fix
description: "Use when fixing a production or runtime failure — an error in logs, a 500, a deadlock, a timeout, a crash, a flaky test, a leaked process or port, a full disk — and especially the moment you are about to add a retry, a sleep or backoff, a longer timeout, a catch-and-ignore, a raised limit, a cleanup cron, or a skipped test. Separates stopping the bleeding (mitigation) from removing the cause (root fix): names which one a change is, finds the mechanism in primary sources (vendor manual, man page, RFC, the library's source), asks why until the cause is in your own code, build or process, reproduces it against the real dependency (not an in-memory stand-in), removes the cause, keeps the mitigation only as a safety net, checks whether it is a recurrence, and never reports a mitigation as solved. Also on 'is this fundamental? / 근본 해결 맞아? / 정석이야? / 재시도가 최선이야?'."
---

# incident-root-fix (장애는 수습과 근본 수정을 나눈다)

## The failure this kills

A payment webhook returned 500 in production. Two webhooks for one new subscription ran `SELECT … FOR UPDATE`
on a row that did not exist yet; under REPEATABLE READ each took a gap lock, each INSERT waited on the other's
gap, InnoDB killed one (1213). The fix that shipped: rerun the transaction up to three times. Correct and
documented — and only a safety net. The cause (locking reads on absent keys take gap locks) stayed, and nobody
asked whether two *different* new subscriptions landing in one index gap hit the same mechanism. It was reported
as "fixed".

A mitigation is not wrong. Calling it the fix is.

## Rule

1. **Name the change.** Before writing it, say which it is:
   - *mitigation* — the failure still happens, its effect is absorbed (retry, backoff, timeout, catch, restart,
     cleanup job, bigger limit, skip);
   - *root fix* — the mechanism that produces the failure no longer runs.
2. **Mitigate first if users are hurting**, then keep going in the same task. A mitigation alone ends the task
   only when the person says so; otherwise continue to the root fix.
3. **Find the mechanism in primary sources.** Read the vendor manual / man page / RFC / dependency source for the
   exact behaviour and quote it (e.g. MySQL "InnoDB Locking", "Locks Set by Different SQL Statements",
   "How to Minimize and Handle Deadlocks"; `fcntl(2)`, `execve(2)`; the library's own code). Ask: under what
   *other* inputs could the same mechanism fire? (Here: two different new subscriptions in one gap.) Test it.
3b. **Keep asking why until the cause is yours.** The mechanism is not the root. Ask why of the *previous answer*
   each time (5 Whys — never drift to a neighbouring concept), and ask the change question at least once: **"why did
   it work before / what changed?"** Look in the before-state's records, not only the fixing commit: the previous
   build tool, pre-merge repositories, earlier commits, old instructions and runbooks. Stop only at a cause in your
   own code, build, test or process — "Kotlin classes are final by default" is a fact, not the root; "the
   Gradle→Bazel move dropped the Spring plugin Gradle had applied implicitly, and each Spring library had to
   remember it" is. The root fix acts at that level (a shared build macro, a corrected instruction, a spawn helper
   every caller goes through), not only on the one file that broke.
4. **Reproduce against the real thing.** An in-memory or mocked stand-in that lacks the mechanism proves nothing
   (H2 has no gap locks). Use the real engine (Docker MySQL, the real OS call, the real browser) and force the
   interleaving. The test must fail before the fix with the production error, for every case found in step 3.
5. **Remove the cause; keep the net.** Change the mechanism (isolation level for that transaction, lock an
   existing row to serialize, insert-first, close-on-exec at the spawn point, remove the temp dir in the step
   that made it…). Keep the retry/backoff as defence in depth, documented as such.
6. **Check the blast radius.** Lock-order with every other writer of the same rows; every other spawn point;
   every other caller of the same helper. Same mechanism elsewhere = same fix there, or a listed follow-up.
7. **Report honestly.** One line each: what was mitigated, what root fix landed (with the before/after test),
   what is left and why. If only a mitigation landed, the report says so ("mitigated only — the root cause is …,
   next …") and a tracked follow-up holds the root plan. Never "fixed" for a mitigation.
8. **Is it a recurrence? Classify the cause once, by ID.** Keep one list of your own causes (the bottom of
   step 3b) — a file, a table, an issue label. Reuse an existing cause ID; add a new one (label + one-line
   definition) only when none fits. Then look up earlier incidents with that cause and the guards (tests, gates,
   build rules) added for them. If a guard for that cause already existed, this **is a recurrence**: write one
   sentence on why that guard did not stop it (usually: it covered only the path that broke last time), and make
   the new guard act on the cause, not just this path.
9. **Record it so it can be counted.** One note per incident: title, date, cause IDs, fix commits, the
   recurrence sentence when step 8 says so, and two lines up front — **root cause** in one sentence ("our cause
   → what happened") and **root fix** in one sentence (acting on that cause). One note per guard: kind (test,
   gate, build rule), commit, path, cause IDs, and an honest `scope` — what it really blocks ("this path only").
   Write each sentence once and link to it; do not copy it into several places.
10. **Widen the concept net.** Every technical term the why-ladder leans on (gap lock, detached entity, CGLIB
    proxy…) gets a short glossary entry: a definition, why it exists (its parent concept), and a primary source
    you checked is reachable. No dead ends: the parent must have an entry too.
11. **Make it a case.** The incident note leads with the root-cause and root-fix lines so a reader (or a later
    agent) gets the lesson without reading the whole story.

## Smells that mean you are mitigating

retry loop · `sleep`/backoff · longer timeout · `catch { }` or log-and-continue · raising a pool/heap/disk limit ·
restart-on-failure · cron that cleans up after a leak · `@Disabled`/skip · "it converged on the provider's
retry" · "rare, so fine".

When one appears, write the step-3 question down before going further.

## Done means

- the mechanism is named with a quoted primary source, and the why-ladder reached a cause in your code/build/process
  (including what changed from the state that worked),
- a real-dependency test failed before and passes after, covering the other inputs found in step 3,
- the mitigation (if kept) is labelled as the safety net,
- the report states mitigation vs root fix and anything left,
- the cause has an ID; recurrence checked (and the why-the-old-guard-missed sentence written if it is one); the
  incident and guard notes exist with root cause / root fix lines; the why-ladder's terms are in the glossary.
