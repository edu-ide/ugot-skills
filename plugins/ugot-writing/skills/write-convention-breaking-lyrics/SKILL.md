---
name: write-convention-breaking-lyrics
description: Research, design, write, rewrite, and audit original English or Korean song lyrics that remain singable while deliberately breaking one lyrical convention. Use for full-song lyrics, chorus hooks, lyric rewrites, anti-cliche passes, reference-song analysis without copying, English stress-beat prosody, Korean prosody, breath inheritance, cross-song breath-pattern separation, semantic hook repetition, song-form planning, lyrics intended for Suno, ACE-Step, or an existing topline, drafts that feel generic or derivative, and healing lyrics that must avoid advice, cure promises, or forced recovery arcs.
---

# Write Convention-Breaking Lyrics

Write a song, not a page poem. Preserve enough familiar architecture for the
listener to orient, then make one exception audible and meaningful.

Read `references/english-prosody-convention-breaking.md` first whenever the
lyric is in English. English is stress-timed, so the stress-beat vector — not
the syllable count — governs text setting, and the conventions worth breaking
differ from the Korean ones in section 7. Read `references/research.md` for
research evidence or prosody rationale. Read
`references/supplied-song-matrix.md` when the task uses the user's supplied song
set or asks to synthesize lyric and topline devices across references. For Suno
field operation and English rendering failure modes, read
`${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/references/suno-generation-english.md`.

## 1. Set the boundary

- Use references to infer devices, not wording. Do not reproduce or lightly
  paraphrase identifiable lyric lines.
- Keep artist and song names out of generation prompts.
- If a melody or chorus audio exists, use `compose-topline-melody` jointly. Do
  not freeze melody first and force lyrics into it; inherit its measured phrase
  lengths, rests, peak vowel, and density limits, then allow the words to request
  one deliberate melodic revision.
- If no melody exists, state provisional syllable bands rather than pretending
  exact text-setting is known.

## 2. Run the unfamiliarity-risk gate

Do not claim absolute novelty. Reduce convergence on common lyric templates and
the writer's recent drafts. A new topic, object, or set of metaphors is not a
new song mechanism when the information order and hook behavior stay the same.

Before drafting, write:

```text
Frontier stall:
Dense lyric prior being avoided:
Familiar shell retained:
Primary axis changed: architecture / information order / hook syntax /
  semantic mutation / point of view / prosody
Single causal mechanism:
Stable listener handle:
Measurable lyric signature:
Recent-draft comparison:
Randomness guard:
Rejection condition:
```

The lyric signature is:

```text
section-job order | occurrence line counts | syllable and breath vectors |
breath-end roles | carrier type and state changes | hook syntax and position |
refrain mutation | reveal section | pronoun/time pattern | dominant ending grammar
```

Compare against at least the two most recent accepted drafts when available:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/write-convention-breaking-lyrics/scripts/audit_lyrics.py \
  --lyrics DRAFT.txt --hook "HOOK PHRASE" --lang en --suno \
  --compare RECENT_1.txt --compare RECENT_2.txt
```

Use `--lang ko` for Korean and drop `--suno` when the target is not Suno. The
auditor reports both a heard-syllable vector and, for English, a stress-beat
vector; compare the vector that governs the target language.

If two recent drafts share at least 85% form similarity, switch architecture or
information order. If they also reuse the same semantic engine—such as denial
becoming confession, an ordinary object revealing the truth, or a final pronoun
swap—change that engine before changing imagery.

Keep one stable handle: a singable phrase, recurring action, vowel frame, or
concrete carrier. Reject novelty that cannot explain its emotional cause and
effect, loses all recognition across returns, or exists only as strange
word choice. Theme replacement, synonym replacement, and metaphor replacement
do not count as a mechanism switch.

## 3. Name the song's contradiction

Write one sentence containing both things that are true:

```text
The speaker wants ___, but keeps doing ___ because ___.
```

Then choose:

- one physical carrier: a specific object, place, action, time, or bodily
  sensation;
- one withheld fact that changes how an earlier line is heard;
- one listener-facing effect: recognition, dread, relief, shame, or unresolved
  tenderness.

Reject a carrier that is merely decorative. It must change state, cause an
action, or reveal information.

## 4. Choose one primary broken convention

Use one primary exception. Add a prosodic exception only when a melody supports
it.

- **Meaning-mutating refrain:** repeat the same hook, but change its implied
  subject, time, or intention through new surrounding lines.
- **Effect before cause:** open with physical evidence; disclose what happened
  only in verse two or the bridge.
- **Object betrayal:** let an ordinary object contradict the narrator's claim.
- **Refusal hook:** make the chorus a command or denial whose repetition proves
  the opposite.
- **Unresolved chorus:** let the chorus pose the central problem instead of
  summarizing the verses.
- **Pronoun aperture:** leave one relationship or addressee open to multiple
  readings while keeping the scene concrete.
- **Anti-climax peak:** place the bluntest, smallest sentence at the emotional
  high point instead of the grandest metaphor.
- **Prosodic fracture:** misalign one spoken phrase with the meter to enact
  hesitation, interruption, or obsession; repeat the fracture so it sounds
  intentional.
- **Breath inheritance:** reject self-contained lines that reset after every
  inhale. Let each breath resolve an unfinished syntactic or semantic state from
  the prior breath, then leave one new state for the next. Close the debt only
  at the planned final landing.
- **Delayed self-correction:** let a repeated hook begin as admiration,
  confidence, or refusal, then disclose evidence that turns the same phrase
  into inspection, doubt, or confession.
- **Low-status gravity:** make a comic, domestic, cheap, or unprestigious noun
  carry a serious consequence without winking away the emotion.
- **Anticipated memory:** grieve a future memory or a time never personally
  lived, while anchoring the paradox in one measurable present detail.
- **Malfunctioning symbol:** use a familiar symbol only after making it fail at
  its expected job: a guide causes getting lost, shelter exposes, or a clock
  prevents knowing the time.
- **Unwithdrawn belonging:** leave the pain unresolved and make care audible by
  preserving the person's place while removing one recovery demand. Do not
  require explanation, speed, usefulness, cheerfulness, or closure as the price
  of staying connected.

Do not confuse novelty with randomness. Preserve a clear emotional cause and
effect even when chronology or point of view is displaced.

Use a ledger:

```text
Expected convention:
Axis being inverted:
Stable element retained:
Concrete carrier:
Withheld fact:
Listener-facing effect:
Rejection condition:
```

When the intent is healing, reject the default arc `pain -> advice -> hope ->
recovery`. Healing may instead mean that belonging is not withdrawn while the
person remains unwell.

Use one concrete carrier whose state proves care: an unremoved chair, an upright
cup, reheated soup, a charged phone, a dimmed light, or another ordinary object
that the speaker actually handles. Make the speaker change the environment,
wait, or reduce a demand. Do not let the speaker diagnose, rescue, take over the
other person's agency, or promise a cure.

Use a Non-Corrective Care Card:

```text
Pain left unresolved:
Recovery demand removed:
Place or object preserved:
Concrete care action:
Agency retained:
What the speaker refuses to promise:
Final-refrain change:
Rejection condition:
```

Do not imply that professional care, medicine, or treatment is unnecessary.
Lyrics can offer recognition and companionship; they cannot establish that a
frequency, relationship, or song medically heals the body.

## 5. Co-design lyric and topline

Reject both "finish the lyrics, then add melody" and "finish the melody, then
fill syllables." Alternate short constraint passes:

1. Write the chorus as two to four **semantic slots**, not polished lines:
   setup, contradiction, withheld word, and landing.
2. Sing nonsense vowels to discover the rhythmic cell, breath points, and
   comfortable peak vowel.
3. Fit only the load-bearing words. Revise either pitch or text when natural
   speech and musical stress disagree.
4. Decide whether one mismatch communicates the song better than alignment.
5. Complete particles, endings, and connective text last.

Choose at most one primary lyric-topline exception:

- **Melody as unreliable narrator:** the words claim calm or certainty while
  register, breath, or cadence exposes strain.
- **Semantic contour inversion:** hopeful language descends or a refusal rises;
  use the conflict to change interpretation, not as random irony.
- **Grammatical spotlight:** place one normally weak particle, ending, or
  pronoun on the long or high note so dependency, delay, or inability to finish
  becomes audible.
- **Withheld landing:** leave the expected answer as a rest; reveal the word on
  a later refrain.
- **Contour-stable mutation:** keep the hook rhythm and contour while changing
  one pronoun, tense, or certainty word, so melody remembers what language
  revises.
- **Text-stable mutation:** repeat the exact lyric while changing cadence,
  register, or breath; the first return asserts, the later one doubts or
  accepts.
- **Negative-density sentence:** let the most important lyric contain fewer
  notes and more silence than its setup.
- **Vowel-frame variation:** preserve the hook's vowel colors and rhythmic
  identity while replacing the actual words and pitch direction.

Do not place every important noun on a high note. Predictable alignment makes
the melody illustrate the lyric instead of interpreting it. Keep ordinary
speech prosody as the baseline, then make one audible violation carry meaning.

Use a joint card:

```text
Hook's semantic job:
Hook's melodic job:
Load-bearing word:
Phrase syllable slots:
Peak syllable and vowel:
Word-to-peak relation: aligned / inverted / displaced
Meaning of the main rest:
Return mutation: word / contour / cadence / breath
Breath vector and inherited state:
Primary lyric-topline exception:
What remains stable for recognition:
Rejection condition:
```

## 6. Build the architecture

Assign each section a job before drafting. Do not make every section explain the
same feeling.

- **Verse 1:** observable evidence and a specific action; withhold diagnosis.
- **Pre-chorus:** narrow choices or increase pressure; avoid a second verse.
- **Chorus:** shortest language, clearest mouth-feel, title or hook, and the
  central contradiction.
- **Verse 2:** change the carrier's state or reveal the speaker caused part of
  the problem.
- **Bridge:** disclose the withheld fact, switch the implied addressee, or make
  one plain admission. Do not write a moral.
- **Final chorus:** retain enough words to be recognized; alter one decisive
  word, pronoun, tense, or neighboring line so the refrain changes meaning.

Assigning jobs is not the same as surviving the boundaries between them. Streaming
listeners abandon songs in a surge about 3.5 seconds *after* a section boundary,
so an announced seam is a permission to leave. Carry an unfinished state across
every section label, and start the next section's identity element — its rhythmic
cell, vowel frame, or first word — before the previous section has finished. The
evidence and the full boundary law are in
`${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/references/greatness-convention-breaking.md`.

This is a diagnostic default, not a mandatory pop form. For through-composed or
short songs, preserve the same jobs without forcing labels.

## 7. Write for the mouth

The mouth rules are language-specific. Use the subsection for the lyric's
language; do not carry one language's rhyme or stress logic into the other.

### English

English is stress-timed. Read
`references/english-prosody-convention-breaking.md` and apply it in full. The
three rules that most often decide whether an English draft is actually new:

- Design the **stress-beat vector**, not the syllable count. Varying syllable
  counts at a constant stress count is ordinary English, not a new phrasing.
- Do not let end-rhyme carry closure by default. Weak rhyme, an assonance or
  consonance chain, or a withheld rhyme are the available replacements.
- Never put a plosive or a four-consonant cluster on the longest note, and treat
  vowel-plus-`r` words (`fire`, `hour`, `tired`) as elision-ambiguous: write the
  line so either sung count scans.

### Korean

- Count heard syllables, not written word count.
- Prefer one syntactic action per line. Move particles and auxiliary endings to
  weak or short notes when a melody exists.
- Put the semantic load and an open vowel such as `아`, `어`, or `오` on long
  or high notes when natural. Break this once only when the mismatch is the
  chosen lyric-topline exception.
- Do not force English-style vowel-plus-coda rhyme. Korean listeners can group
  onset-plus-vowel bodies; use vowel color, onset echoes, phrase rhythm, and
  parallel syntax as alternatives.
- Avoid identical grammatical endings merely to simulate rhyme.
- Keep neighboring lines within a workable syllable band, then allow one
  deliberate short or long line where the narrative fractures.
- Read every line aloud in ordinary Korean. If speech stress must be distorted,
  make the distortion carry meaning.

### Break the breath-reset law (English and Korean)

This law applies to both languages; only the boundary markers differ. In Korean,
a breath is unfinished at a connective ending; in English, at a conjunction,
preposition, determiner, or dangling auxiliary. The English marker list and the
`inherited` audit label are in
`references/english-prosody-convention-breaking.md`.

Do not treat random line-length variation as a new breath grammar. Reject the
default that every lyric line completes one sentence, takes one breath, and
starts fresh on the next bar.

Use breath inheritance as one deterministic law:

1. End a breath at a natural connective ending, withheld predicate, correction,
   or semantic hinge.
2. Begin the next breath by paying that unfinished state before opening another.
3. Preserve one recognizable mouth-rhythm handle while breath capacities follow
   a planned asymmetric vector such as `short / long / clipped / medium`.
4. Let a refrain return move one breath boundary while words or vowel frame stay
   recognizable.
5. Permit a fully self-contained breath only at the intended closure.

Do not cut randomly inside a Korean word, detach particles without a clear
spotlight effect, or make every line an exhausting run-on. In English, do not
split a phrasal verb or compound noun across a breath unless the spotlight is
the point. The inherited state must remain understandable when spoken normally.

Write a Breath Inheritance Card:

```text
Rejected breath-reset pattern:
Recent breath vector 1:
Recent breath vector 2:
Current heard-syllable vector:
Breath-end roles: closed / connective / withheld / cutoff
State inherited at each boundary:
Stable mouth-rhythm handle:
Boundary moved on return:
Final debt payment:
Predicted listener effect:
Generator normalization failure:
Rejection condition:
```

Compare heard-syllable buckets and breath-end roles with the two most recent
accepted lyrics. Reject when both the vector and boundary-role sequence closely
match either recent song, even if the words, topic, BPM, or melody differ.
Formatting only requests a breath; verify the rendered singer actually carries
the state across the boundary.

## 8. Make repetition gain information

Phrase repetition improves recognition; indiscriminate word repetition can
erase novelty.

- Repeat one hook phrase two to four structurally important times.
- Change the evidence around it so each return answers a different question.
- Prefer an exact refrain with semantic mutation over many unrelated catchphrases.
- In the final return, change at most one or two load-bearing words unless the
  intended effect is collapse.
- Do not require both text and melody to mutate at once. Preserve one identity
  layer—wording, rhythmic cell, vowel frame, or contour—so the listener can
  hear what the other layer changed.

## 9. Remove generated-lyric tells

Run an interchangeability test: if a line can move unchanged into thousands of
breakup songs, rewrite it.

Flag, but do not automatically ban:

- uncaused rooms, windows, shadows, stars, seasons, names, light, and tears;
- stacked pretty metaphors that never affect an action;
- abstract declarations immediately followed by a redundant image;
- symmetrical four-line stanzas with identical sentence logic;
- bridge lines that explain the song's lesson;
- adjectives that can be deleted without changing the scene;
- a narrator who only observes and never makes a choice.

Repair a generic image by adding ownership, malfunction, measurement, residue,
cost, or an irreversible action.

## 10. Audit before delivery

Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/write-convention-breaking-lyrics/scripts/audit_lyrics.py \
  --lyrics DRAFT.txt --hook "HOOK PHRASE" --lang en --suno \
  --compare RECENT_1.txt --compare RECENT_2.txt
```

Add `--healing-intent` when the song is meant to feel healing. Treat its
assurance and medical-claim warnings as revision prompts, not automatic bans.

Treat its output as diagnostics, not a quality score. Then verify manually:

- the listener can name the scene after verse one;
- the lyric signature does not near-match two consecutive accepted drafts;
- the primary difference changes architecture, information order, hook
  behavior, semantics, point of view, or prosody—not just topic or imagery;
- one stable listener handle remains easy to recognize;
- the chorus is easier to sing than the verse;
- the primary convention break is audible without explanation;
- the concrete carrier changes state at least once;
- the final refrain means something the first refrain did not;
- no reference phrase or distinctive sequence was copied;
- syllable shape, rests, and peak vowels fit the topline when one exists.
- the breath vector and boundary roles do not near-match recent accepted songs;
- each non-final inherited breath audibly passes unfinished state forward, and
  the planned final breath closes it;
- the joint exception is audible in the singing, not merely explainable on
  paper;
- at least one of wording, rhythm, vowel frame, or contour remains stable at
  every mutated return.
- for healing lyrics, care is shown through a concrete action rather than a
  generic assurance;
- pain may remain unresolved without belonging, agency, or access to treatment
  being withdrawn;
- the song makes no medical, frequency-healing, or guaranteed-recovery claim.

For English, additionally verify:

- the stress-beat vector, not only the syllable count, differs from recent drafts;
- the rhyme grammar is a decision, not a default `AABB`/`ABAB` template, and the
  auditor reports no single dominant rhyme tail;
- at least one line ends on an unfinished syntactic state when breath
  inheritance is the chosen mechanism;
- no plosive or dense consonant cluster sits on the longest note;
- every elision-ambiguous word scans under both possible sung counts;
- when the target is Suno, the `--suno` checks are clean or consciously accepted.

## 11. Deliver

Provide:

1. title and complete sectioned lyrics;
2. the convention and unfamiliarity ledgers, including the lyric signature;
3. the joint lyric-topline card and provisional syllable bands;
4. melody-fit notes naming the peak syllable, meaningful rests, and return
   mutation;
5. a model-appropriate Suno style description or ACE-Step caption and a
   `[Section]` lyrics block when generation is requested;
6. the Non-Corrective Care Card when healing intent is requested;
7. the English Prosody Card from
   `references/english-prosody-convention-breaking.md` when the lyric is English.

Keep the explanation shorter than the lyrics.
