---
name: audit-convention-fit
description: "Detect and correct convention-preserving interpretation bias: changing lexical meanings, invoking vague context or metaphor, inventing exceptions, or false-balancing alternatives to protect a current doctrine, consensus, policy, architecture, or social assumption. Use whenever Codex interprets contested primary evidence such as scripture, religious texts, history, law, policy, research, requirements, logs, tests, or observed software behavior; especially when evidence conflicts with an inherited model, when words such as context, metaphor, symbolism, title, role, compatibility, or tradition are used to rescue a favored conclusion, or when competing interpretations must be ranked."
---

# Audit Convention Fit

## Core Rule

Treat the current convention as a hypothesis, never as the frame that decides what the evidence is allowed to mean.

Apply the same interpretive rules to favored and disfavored conclusions. Fair representation does not require equal weighting. Rank explanations by evidence after presenting them accurately.

Do not become reflexively contrarian. A consensus may win because it explains the evidence best, but its social acceptance is not itself the decisive evidence.

## Mandatory Audit

### 1. Freeze the question and convention

Write one exact question. State the inherited conclusion separately as `C`. Record what `C` predicts before interpreting anomalies.

Do not smuggle `C` into a translation, paraphrase, variable name, category, or summary.

### 2. Freeze primary evidence

Show the complete relevant sentence, event, observation, log, or behavior before explaining it. Separate these layers:

- raw observation
- lexical or structural fact
- translation or normalization
- interpretation
- broader inference

Never cite an interpretation as though it were raw evidence.

### 3. Establish the baseline meaning

Check morphology, syntax, standard lexical meaning, data schema, API contract, or runtime semantics before invoking broader context.

- Preserve a stable core meaning unless independent usage evidence supports polysemy.
- Do not invent a new sense solely because the baseline conflicts with `C`.
- Do not promote a disputed contextual inference into a dictionary meaning.
- Name the exact contextual feature doing the work. `문맥상` by itself is not an explanation.

### 4. Build falsifiable candidates

Form the strongest conventional hypothesis and the strongest competing hypotheses. For each, state:

- what it explains directly
- what it predicts
- what would contradict it
- which additional assumptions it requires

Include the strongest disconfirming evidence for the favored hypothesis. Do not build a weak opponent for an easy victory.

### 5. Record rescue assumptions

Create a rescue ledger whenever an interpretation needs an exception after encountering contrary evidence. Typical rescue moves include:

- changing a word's ordinary meaning
- declaring inconvenient wording metaphorical or symbolic
- switching historical periods or textual layers without evidence
- treating role as identity, or identity as role, only where convenient
- appealing to a later doctrine to determine an earlier text's referent
- calling an anomaly irrelevant after it damages the favored model
- adding an unobserved mechanism to preserve compatibility

A rescue assumption is not automatically false. Require independent evidence for it and charge the same complexity cost to every hypothesis.

### 6. Run the symmetry test

Ask all four questions explicitly:

1. Would I accept this interpretive move if it protected the opposite conclusion?
2. Did I allow metaphor, context, or exceptions to only one side?
3. Am I preserving a familiar conclusion because rejecting it has a social or emotional cost?
4. Did I mistake respectful treatment of a view for equal evidential support?

If any answer exposes asymmetry, redo the comparison before writing the conclusion.

### 7. Rank, do not collect

Assign each candidate one verdict:

- `direct fit`: explains the evidence using established meanings and structures
- `supported extension`: needs an additional move with independent evidence
- `rescued fit`: survives mainly through unverified exceptions or meaning changes
- `contradicted`: fails a necessary prediction
- `unresolved`: evidence genuinely cannot distinguish the remaining candidates

Choose the current best explanation. Do not finish with `여러 해석이 가능하다` when the evidence supports a ranking. Do not keep a weaker explanation artificially alive to appear neutral or to avoid correcting an earlier claim.

### 8. Bound the verdict

State exactly:

- what the evidence supports
- what it weakens or rejects
- what it does not establish
- what new evidence would change the ranking

Do not extend a local result to an entire religion, historical era, codebase, or population without a separate inference.

### 9. Correct without self-protection

When the audit catches a convention-fitting interpretation:

1. Name the mistaken move plainly.
2. Remove it from the active argument instead of retaining it as an equal option.
3. Repair every dependent claim or artifact.
4. Re-run the ranking from the frozen primary evidence.

Do not soften a correction into a false compromise merely to preserve prior output.

## Required Output

For a contested interpretation, expose this compact audit before the final narrative or implementation:

```text
질문:
일차 증거:
현재 통념 C:
경쟁 가설:
구제 가정 원장:
비대칭 검사:
판정 순위:
판정의 한계:
```

The public-facing result may be shorter, but the reasoning must preserve these distinctions.

## Fast Failure Signals

Stop and audit immediately when drafting any of these phrases without concrete support:

- `문맥에 따라 뜻이 달라진다`
- `상징적으로 보면 모두 맞다`
- `전통적으로 그렇게 해석해 왔다`
- `기술적으로 두 해석 모두 가능하다`
- `현재 통념과 모순되지 않는다`
- `역할을 가리킬 뿐 존재를 말하는 것은 아니다`
- `표현은 복수지만 실제로는 한 대상이다`

Each statement may occasionally be correct. Require the exact grammatical, historical, empirical, or architectural mechanism before accepting it.
