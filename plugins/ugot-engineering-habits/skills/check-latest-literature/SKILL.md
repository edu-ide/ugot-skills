---
name: check-latest-literature
description: "Use BEFORE proposing/choosing a METHOD or architecture, before calling an idea \"novel/신논문급/best/SOTA\", or whenever you reach for a familiar named technique (MLM, DPR, pointer-generator, Procrustes, RETRO, BERT, LoRA, PPO, beam search, ...). In a fast-moving field the default-from-memory method is usually 2017-2021 vintage and a CURRENT-YEAR (last ~18 months) version is often strictly better or the actual SOTA. Search the current literature FIRST (WebSearch or a paper-search tool on arXiv + the present year), prefer/ground in the latest work, and distinguish \"old-but-still-foundational\" from \"superseded\". Triggers on: proposing a method, \"신논문급/novel/최신/latest/SOTA/state-of-the-art\", naming any classic technique, \"옛날거/old approach\", recipe/architecture/objective design."
contract:
  trigger: "방법·아키텍처를 고르기 전, \"novel/SOTA/신논문급\"을 말하기 전, 익숙한 기법 이름을 꺼내는 순간"
  procedure: "현재 연도(최근 18개월) 문헌 검색 → 최신 형태 채택 또는 \"여전히 기초\"로 구분 → 출처 기록"
  exit_check: "최근 18개월 출처 ≥1이 답에 링크되어 있다"
  evidence: "검색 결과·출처 링크가 든 문서/장부 줄"
principle: reference-first
---

# Check Latest Literature (don't default to old methods)

> 이 스킬은 `reference-first`(ugot-mindset)의 ② 분야-최신 갈래다. 어떤 작업이든 손대기 전 네 갈래(우리 기록·분야 최신·1차 문서·기준 제품) 참고 줄을 먼저 쓰는 원칙은 그쪽에 있다.

## The failure this kills

Reaching into memory for a method gives you the version you learned — usually **2017-2021**. The field moves fast; a
**current-year** variant is often strictly better, faster, or the real SOTA. Proposing the old one (and worse, calling
it "신논문급/novel") is the recurring miss. This is the EXTERNAL-recall sibling of `recall-before-reinvent` (which checks
the PROJECT's own history).

## The rule

**You may NOT propose a method, pick an architecture/objective, or call anything "novel/latest/SOTA/best" until you have
searched the CURRENT-YEAR literature for it.** Default to assuming your remembered method has a newer successor.

## Procedure (fast, ~2-4 searches)
1. **Search the field for {method} + {problem}, current year.** Use `WebSearch` (or any paper-search tool you have)
   with the present year in the query (e.g. "... 2025 2026", "arxiv 2026", "SOTA <task> <year>"). Prefer arXiv/scholarly.
   Save hits worth keeping to `sources/` or cite the arXiv id inline.
2. **Map old → current.** For each classic primitive you were about to use, find its modern form. Examples (verify, don't
   trust this list — it ages too): MLM/BERT → ModernBERT (2024)/MaBERT (2026); attention → linear-attention/SSM
   (Mamba-2, gated-delta-net, RWKV-7); RETRO → long-context RAG / Self-RAG; DPR → late-interaction/modern dense; LoRA →
   DoRA/newer PEFT; PPO → GRPO/DPO-family. The point is the HABIT of checking, not any fixed mapping.
3. **Classify the old method**: (a) **superseded** → adopt the current SOTA instead; (b) **still-foundational** (the
   modern work still builds on it, e.g. MLM inside ModernBERT) → keep it but GROUND in the modern paper + recipe, and say
   so ("MLM, still load-bearing in <2026 paper>"); (c) **genuinely no successor found** → only then call it current,
   framed "not found newer in <venues searched>".
4. **Your contribution is the ADAPTATION**, not the invention — name the current paper(s) you're grounding in.

## Calibration

- "I remember method X" is NOT evidence X is current. Search before asserting.
- "Works on our system" ≠ "novel" ≠ "latest" — three different claims; never conflate.
- Architecture/objective/recipe decisions especially: a 1-search check often flips the choice (e.g. "is there a 2025/26
  hybrid-SSM encoder?" → yes, MaBERT 2603.03001 — which may BE your design, validating it as current not antique).
- Cheap insurance: even when you end up using the old primitive, the search either upgrades it or lets you ground it
  honestly in the modern lineage. Skipping it is how you ship 2018 ideas labelled "신논문급".

## The TREADMILL trap (2026-06-21): "find the newest" is the WRONG target — "best-fit-to-constraint" is

A fast field ALWAYS has a newer method (papers daily; one merge survey lists 50+). If you "search for the latest" you'll
ALWAYS surface yet another one — an infinite treadmill — and you'll keep swapping without converging. Two failures cause it:
1. **Incremental search from memory** (the real miss): grabbing the method YOU know (e.g. DARE-TIES, 2023-24) first, then
   only searching "newer than X" when challenged. That guarantees the "oh, there's a newer one" loop. FIX: search the
   **SURVEY / taxonomy ONCE** (e.g. "model merging survey 2026", "awesome-X list") to map the WHOLE space up front, not the
   one method you remember.
2. **Optimizing for RECENCY instead of FIT.** Newest ≠ best. Recency is not quality. Pick by **fit to YOUR hard
   constraint**, not chronology. (Example: an OLDER merge method beat every newer one [DELLA/Breadcrumbs/EMR/
   layer-wise] because only it could PROVE zero erosion of existing skills, which was our hard constraint. The newest
   merges were best-effort. Chasing "newer merge" was the treadmill; the right move was matching the CONSTRAINT.)
**STOP rule:** once you've (a) mapped the space via a survey and (b) found a method that MEETS your hard constraint, STOP —
do NOT keep searching for "even newer". A newer one existing does NOT mean you need it. Re-search only if the constraint
changes or the chosen method fails. Map-once → select-by-constraint → stop ≠ chase-newest-forever.

## After searching

End with a one-line "grounded in <papers/arXiv ids> (searched <venues>, <year>)" so the provenance is explicit. If the
search changed your method, say what you swapped and why. Persist durable findings to the repo (ledger/sources), not memory.

