---
name: build-right-the-first-time
description: >-
  Invoke BEFORE launching ANY build / train / corpus-compose / eval / download / large run, OR the moment you
  reach for the FAMILIAR/OLD/QUICK option (the dataset you used last time, the version you remember), OR when
  you're about to say "baseline first, improve later / 다음 iteration에 / next build에서 fold-in". The recurring,
  expensive failure (user caught REPEATEDLY 2026-06-29: "왜 최신으로 안했어 한번 할때 제대로 하는 스킬좀 만들어",
  and the whole synthetic→real / hand-assembled→SSOT / old→latest chain): shipping a version you ALREADY KNOW is
  suboptimal — OLD datasets when the registry lists newer ★ ones (GSM8K-2021 when Nemotron-Math-v2-2025-12 exists;
  SQuAD-2016 when the registry has newer), a hand-picked shard list instead of the SSOT, a synthetic toy instead
  of real data — then the user catches it and you REDO the whole expensive run. Each "quick then redo" is 2-5×
  the work AND burns a multi-hour GPU run on a known-suboptimal artifact. The fix: consult the registry / SSOT /
  latest-literature for the BEST/LATEST inputs and use them THE FIRST TIME. Sibling of check-latest-literature,
  recall-before-reinvent, spec-first, no-waste.
principle: predictability-first
---

# build-right-the-first-time — consult the registry/SSOT for the BEST input, don't ship known-suboptimal

The pattern this kills: build a "quick" version on the OLD/FAMILIAR/SYNTHETIC input → user catches it → redo the
whole run on the right input. The redo is the waste. Do it right ONCE.

## THE PRE-BUILD CHECKLIST (run before any build/train/corpus/eval/download)

1. **STOP — do not reach for the familiar input.** The dataset you used last time / remember is probably NOT
   the best. Name what you're about to use and WHY.
2. **Consult the source of truth for the BEST/LATEST:**
   - **Datasets** → the project's dataset registry (the per-capability ★ picks + the RECENCY PRIORITY: 2026 > 2025 >
     older). If the registry names a newer dataset than the one in your hand, USE THE NEWER ONE.
   - **Method/arch** → `check-latest-literature` (the current-year SOTA, not the 2020 default you remember).
   - **Corpus composition** → the project's single source of truth for data composition, never hand-assembled.
   - **Capabilities to include** → `spec-first` (enumerate ALL, not the subset you remember).
3. **Write the "done RIGHT" checklist** — latest datasets ✓, all capabilities ✓, real data ✓, real-benchmark
   measure ✓, best method ✓. Each item = the BEST available, verified BEFORE launch.
4. **If any item is the OLD/QUICK/PARTIAL option → fix it NOW, before launching.** "I'll use GSM8K now and
   Nemotron-Math later" is the exact trap — the rebuild costs more than doing it right once. A multi-hour GPU
   run on known-suboptimal data is pure waste.
5. **Partial is allowed ONLY if EXPLICITLY a disclosed baseline** — state "this is a baseline on X; the latest
   Y/Z are deferred because <reason>", proactively, so it is a deliberate stage, not a silent shortcut the user
   has to catch.

## RED FLAGS (you're about to ship known-suboptimal)

- You picked a dataset from memory without opening the dataset registry to check for a newer ★.
- You're using a 2016-2021 dataset and haven't checked what 2025-2026 covers it.
- You think "let me get a quick version running, I'll improve the data later."
- You hand-assembled a shard list instead of composing from the SSOT.
- You're launching a >30-min run and have NOT verified every input is the best available.

## WHY

The iterate-and-fix loop (synthetic→real→latest→SSOT, each caught by the user) is the single biggest time sink:
every redo re-pays the full run cost AND erodes trust. The registry/SSOT/latest-literature EXIST so the best
input is one lookup away — the failure is not consulting them under momentum ("just get it running"). This skill
makes "consult for the best, then build once" a required pre-step. Do it right the first time. Sibling:
check-latest-literature, recall-before-reinvent, spec-first, no-waste.
