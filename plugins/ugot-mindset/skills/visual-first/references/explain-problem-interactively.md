# explain-problem-interactively (2026-10-17에 `visual-first`로 흡수)

원래 설명: Use when explaining a real engineering problem you solved (a bug, an incident, a design choice) to someone who will judge the reasoning — an interviewer, a portfolio reader, a teammate, a client — or when the person asks to visualize, illustrate or teach how something works and why it was fixed that way ('시각화 해줘', '이해가 안 된다', '포트폴리오에 넣자', 'CS 질문 대비').

# explain-problem-interactively (기본 지식으로 현실 문제를 설명하는 시각화)

## Why

A fix shown as code alone says "I changed this". A reader who must judge you needs: do you know the
fundamental, did you see what it caused, did you weigh the options, and how do you know it worked. Born
2026-10-12 preparing a CS-heavy interview: the gap-lock deadlock was first told as "retried it", and only when
laid out as *why gap locks exist (phantom reads) → what that caused (two inserts waiting on each other's gap) →
the ways out (retry, READ COMMITTED + row-lock serialization, a queue) → proof (real MySQL repro)* did it show
understanding instead of a patch.

## The five panels (one explanation = these, in this order)

1. **Fundamental — why the mechanism exists.** The textbook concept with its purpose, not just its name:
   "a gap lock exists to stop phantom reads under REPEATABLE READ". Name it with the standard term
   (전위 순회, 갭 락, close-on-exec) so the reader can look it up; never coin a label and present it as a term.
2. **The real situation — what it caused.** A step-through timeline of the actual case (who did what, in what
   order, where it broke). The failing step is visibly marked.
3. **The ways out — compared.** Mitigation vs root fix vs at-scale option, each with what it costs. Say which
   was applied and which is still in progress. A mitigation is never presented as the fix
   (see the `incident-root-fix` skill).
4. **Code — pseudo-code first, real code one click away.** Pseudo-code is for understanding; the real excerpt
   (file path + the lines) is the proof it was really done. Never invent "old" code as history: if a before-state
   is reconstructed for comparison, say so.
5. **Proof — numbers.** What was measured and against what (e.g. "0 / 400 vs 357 / 400 on the real library",
   "failed before with the production error, passes after"). Only checked claims; anything unverified is
   labelled or left out.

## Build rules

- **Interactive where order matters**: a stepper ("다음 →") that moves the concept diagram, the code line and
  the result together, with a mode switch for the alternative (pre-order vs in-order, RR vs RC, retry vs root).
- **Self-contained HTML**: own color tokens for light and dark (no host CSS variables), no external loads.
- **Readable with scripts blocked**: every SVG shape has a default fill (an unset `fill` renders black), the
  first frame (concept, code, empty result, caption) is in the markup, and a notice shown only when scripts are
  blocked says where the steps work. Check it once with JavaScript disabled and once in dark mode.
- **Fits where it goes**: portfolio section (light, matches the site's tokens), Space canvas card
  (`visuals/*.html`, `sandbox="allow-scripts"`, select the card to interact), or an artifact. Size the frame to
  the content height; run the site's own tests (overflow at 320 px is the usual break).
- **Public vs private**: a public page carries no employer-specific judgments (company finances, salary notes,
  doubts). Make a separate interviewer-facing version instead of sharing a prep board.

## Why-chain (recommended for interviews)

Under the case, list the "why?" an interviewer would ask next, questions visible and answers opening on click (native
details), textbook background as ↳ branches under the answer that raised it. Build the ladder itself by the
`incident-root-fix` skill's step 3b (why of the previous answer, the "what changed?" question, down to a cause in our
code/build/process) — do not restate that rule here. Only claims the visual verified.

## Done means

- the five panels exist and each claim in them traces to code, a test or a measurement,
- it reads with scripts blocked and in dark mode,
- it is placed where the reader will see it, and anything still in progress is labelled as such.

## 유래·사례 (description에서 이동, 2026-10-17)

Builds one interactive explanation that goes from the fundamental concept (why the mechanism exists) to what it caused in the real case, the ways to fix it compared, pseudo-code with the real code one click away, and the numbers that prove it — as a self-contained HTML that still reads with scripts blocked, placed where it will be seen (portfolio site, Space canvas, artifact).
