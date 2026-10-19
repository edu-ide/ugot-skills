---
name: design-turn-first
description: "Invoke BEFORE the first feature of any new module, service, engine replacement or \"전면 재구성\", and whenever a feature request would add code to a file that already holds many unrelated functions."
contract:
  trigger: "새 모듈·엔진 교체·전면 재구성의 첫 기능 전, 이미 많은 기능이 든 파일에 기능을 더하려는 순간"
  procedure: "3개월 뒤 깨질 것 ≤5 → 불변식 1-3 → 각 불변식의 기계 검사(지금 값/목표) → 배치·의존 방향·기능 X에 바뀌는 파일"
  exit_check: "불변식마다 기계 검사가 있고 \"기능 X에 바뀌는 파일\" 표가 있다"
  evidence: "설계 카드 파일(docs/…/DESIGN-*.md 또는 architecture/*.md)"
  failure_modes: [18, 25]
  validator: ["file_changed:*architecture/*.md || file_changed:*DESIGN*.md || file_changed:*/specs/*/plan.md || file_changed:*design*.md"]
principle: self
---

# design-turn-first

The agent owns the design decision even when the user asks only for a feature. Recognize the triggers above,
inspect the existing owners and constraints, and perform the design turn without waiting for the user to supply
architectural principles. Infer the user's quality criteria from the task and prior decisions; ask only for a
missing product constraint that materially changes the design, while continuing independent work.

The Storytold comparison motivates this workflow. It is not proof that every model or task will produce the same
architecture. Show the actual structure and verification for the current project.

## The rule — three turns, in this order, never skipped

1. **Design turn** (before feature code). The agent performs these steps proactively; inspect relevant existing code when available:
   - "This will be extended by agents at dozens of commits a day for three months. List ≤5 things that WILL break
     (conflicting forces, where copies appear, where the easiest path is the wrong path)."
   - "Derive 1–3 invariants that make ALL of them impossible at once." (Compression is the point — six symptoms →
     six patches; "one rule that forbids all six" → a generative principle such as *every edit is one Op path*.)
   - "For each invariant, a machine check: pseudocode or one shell line, with the number it must be, and the number
     it is now."
   - Then: module layout, dependency direction, and "which files change for feature X" — the last one exposes a bad
     design: if unrelated modules must change, explain the shared contract or revise the boundary.
2. **Install the checks** in CI / the Bazel gate BEFORE the first feature. Start as a ratchet (record today's number,
   fail if it grows) so the current tree stays green. An invariant that lives only in a chat answer or a memory file
   decays by the next commit.
3. **Feature turn**. Only changes that pass the checks. Route each capability through its chosen domain owner
   and use-case path. Use a command/Op registry when the design calls for one; do not duplicate the same policy
   or state mutation in parallel paths.

## Design for the next change, not just the current feature

Use the existing repository and libraries first. Before editing, make these choices concrete enough to inspect:

- **Responsibilities and state owners:** name the owner of each domain concept and mutable state, its allowed write path, and who regenerates derived values or caches. Trace one real
  user action from its entry point through policy, state change and persistence. Put an invariant at the boundary
  that owns it, rather than repeating validation and state updates in each UI, MCP or CLI adapter.
- **Dependency direction:** keep domain policy independent of UI, transport and storage implementation details.
  Put ports at a boundary only when they isolate an actual external dependency or change axis. Adapters translate
  inputs and outputs; they do not grow a second domain engine. Folder names, interface count and layer count do not
  prove a clean architecture. Do not force a repository's working architecture into a generic layer template.
- **Two concrete extensions:** select two likely next changes from the request, roadmap or observed history and
  list which modules/files each would touch. Mark assumptions when no roadmap exists. If an unrelated format,
  surface or shared state owner must change, explain why or revise the design. Do not invent speculative features
  to justify abstractions.
- **Less repeated work:** identify registrations, mappings, boilerplate and checks repeated across those changes.
  Prefer an existing library, one shared command/use-case path, a declarative registry, or generation from an
  existing authoritative schema when it actually reduces repetition. Count the manual edits or duplicated paths
  before and after. Do not automate a duplicated design unchanged or create a second generator/source of truth.
- **Executable boundaries:** select checks for this design's risks: forbidden imports or dependency cycles,
  multiple state/write owners, repeated registrations, or the same operation producing different results through
  different adapters. Reuse existing checks and install the missing high-value ones. Report commands, observed
  values and limits; a proposed check is not a passing check.

Keep the design proportional: a small local change needs a short boundary review, not a new framework. For a
larger change, give a compact responsibility/dependency map, the two extension traces and the check results.
Implement one representative end-to-end capability, compare the actual diff with the predicted change boundary, investigate unexplained spread, then extend it. Keep unimplemented extension traces labelled as predictions.
Repeated work becoming harder is evidence to revisit the structure, not a reason to ask the user for more rules.

## What the human supplies (and what they don't)

- NOT the principles. The agent invents "one engine per format", "everything is a command", "stable node IDs only".
- YES the ruler: what counts as damage (fidelity vs the real target app, duplicate count, lines per file, write paths
  per format).
- The agent applies the compression demand ("one invariant that forbids all of these") proactively; the human need not remember to ask.
- YES evidence access when the codebase already exists (git log --numstat, commit verb histogram feat:refactor, grep
  counts). Given our broken code, an agent produced three installable rulers: write functions per format = 1 (was
  docx 26 · pptx 9 · hwpx 8 · rhwp 19), collaboration functions inside format modules = 0 (was 63), hand-registered
  MCP tools = 0 (was 443; 218 of 226 write tools lacked a revision token).

## Signs you skipped the design turn

- The request names a feature and the first tool call is Edit on a file > 3,000 lines.
- Commit verbs over the module are feat ≫ refactor (ours: 39:1).
- The same concept exists once per format (collab × docx/pptx/hwp/hwpx), or once per surface (UI engine ≠ MCP engine).
- "Where does feature X go?" has more than one honest answer.

## Pairs with

- A subtractive spec is the design turn's *target* — name the reference app and version, enumerate its catalog, keep
  a gaps list, measure per commit. Subtractive specs expose what is missing; additive specs never do.
- `fundamental-first`, `multi-ruler`, `predictability-first` (state the prediction before running the design
  experiment; ours was wrong — spec alone sufficed — and that was the finding).

## 유래·사례 (description에서 이동, 2026-10-17)

Structure is decided by the SHAPE OF THE QUESTION, not by the model: measured 2026-10-14 — given only a product spec and no file access, Fable 5.1, Sonnet and Haiku all produced a Storytold-grade architecture (one format-neutral IR + one Op path, thin UI/MCP/CLI, one-way layers, dependency lint), while the same Fable 5 family, asked for a FEATURE ("close the agent-freedom gaps"), appended +9,186 lines to one file (doc-mcp server.py, 24ff0cfd5e) and grew it to 11,295 lines with 443 hand-registered tools and 63 copied collaboration functions. Rules are not what was missing — a DESIGN TURN was: nobody asked "what breaks in three months?" before "add this". Also on 규칙 없이 구조 / 구조가 왜 개판 / 설계부터 / 어떻게 구조를 잡지 / 클린 아키텍처 / 반복 작업을 줄이는 구조 / 내가 원칙을 알려주기 전에 설계해.
