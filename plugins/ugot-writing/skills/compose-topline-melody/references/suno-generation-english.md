# Generating English songs with Suno

Read this when the target generator is Suno and the lyric is English. It covers
field-by-field operation, the failure modes that silently restore convention,
and the rejection discipline.

Field names, character budgets, and control names change between Suno releases.
Confirm the live limits in the UI before generating, and treat every number here
as "verify, then use."

## 1. Field map and what each field can actually do

- **Lyrics field.** The only field that controls *time*. Section labels alone do
  not create a form: if the hook must return three times, the literal hook text
  must appear three times. Everything the singer says must be typed here.
- **Style / Style of Music.** Controls timbre, instrumentation, delivery, and —
  weakly — compositional grammar. This is a *request*, not a constraint. Put the
  replacement law in the first two sentences; anything after roughly the first
  third of the field is increasingly ignored.
- **Exclude Styles.** The correct home for negative guards. Move every "no X"
  out of the style prompt and into this field. A negative inside the style
  prompt often summons the excluded thing.
- **Persona / voice reuse.** Locks vocal identity across generations, which is
  what you want when comparing two composition laws: hold the voice constant so
  the difference is the law, not the singer.
- **Advanced sliders (weirdness / style influence / audio influence, names vary).**
  Raising weirdness produces surface deviation — unusual instruments, odd mixes.
  It does **not** produce a new compositional law. Do not use a slider as your
  primary axis; it is a parameter variation under the unfamiliarity gate.

## 2. Style-prompt order for a convention-breaking English song

Write the style field in this order. Under a 1,000-character budget this fits
comfortably; do not spend the budget on adjectives.

0. **Sentence 0: era and ensemble**, in plain descriptive words — decade, place,
   room, and the instrument list. The generator grounds its sound here, and a law
   with no palette to live in gets rendered onto the model's default palette.
1. **Sentence 1–2: the replacement law**, stated as a rule the arrangement must
   obey. Name the mixed phrase-length or beat cycle explicitly, and name the
   silence the arrangement must not fill. Keep imperatives for the
   non-negotiables only; see the rule-versus-description note in
   `${CLAUDE_PLUGIN_ROOT}/skills/invent-genre-grammar/SKILL.md` §6.
2. **Sentence 3: what stays stable for recognition** — one hook rhythm, one
   vowel frame, one pulse.
3. **Sentence 4: one compact timbre sentence** — spectral body, air, texture
   location, articulation, vibrato, space. Prefer time-localized behavior
   ("grain only at phrase endings") over static adjectives.
4. **Sentence 5: language and delivery** — `English lyrics`, accent or diction
   register if it matters, and the enunciation demand ("consonants fully
   articulated at the phrase end").
5. **At most two negative guards**, each paired with a positive replacement.
   Everything else goes to Exclude Styles.

Keep artist and song names out of every field. Translate references into
abstract attributes. Never claim that prompt wording eliminates copyright risk.

## 3. English-specific rendering failure modes

Check the render against each of these before accepting a take:

| Failure | What you hear | Fix in the lyric or prompt |
| --- | --- | --- |
| Coda drop at pitch | load-bearing word loses its final consonant | end the word on a vowel or a continuant, or move it off the peak |
| Cluster smear | `strengths`, `glimpsed` become mush | move clusters off short notes; the auditor lists them |
| Numeral misreading | `3` sung as "three-oh" or skipped | spell numerals out |
| Symbol voicing | `&`, `/`, `%` read literally or dropped | spell them out |
| Caps shouting | ALL-CAPS words come out barked | lowercase unless the shout is intended |
| Tag leakage | a bracket tag is sung aloud | reduce tag count; keep tags short and structural |
| Internal-rhyme rap drift | dense internal rhyme flips delivery to rap | thin the internal rhyme or state the delivery explicitly |
| Elision surprise | `fire`, `tired`, `hour` take one syllable where you wrote two | write the line so either count scans |
| Hyphen cutoff ignored | a deliberate mid-word cut is smoothed over | repeat the cutoff so it reads as intentional, and verify |
| Diphthong drift | a sustained `time` becomes `tah-eem` | put a monophthong on the long note |

Run the lyric-side checks with:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/write-convention-breaking-lyrics/scripts/audit_lyrics.py \
  --lyrics LYRICS.txt --hook "HOOK" --lang en --suno
```

## 4. The normalization failure mode

Suno's strongest prior is the four-bar loop with a late lift. It will normalize
a mixed-length or breath-governed law back into that loop and express your
"novelty" as instrumentation instead. Symptoms:

- the phrase-length cycle you specified is audibly even;
- the breath gaps you reserved are filled with a fill, pad, ad-lib, or reverb
  tail;
- the only difference from your last generation is the instrument palette;
- the chorus differs from the verse only by being louder.

When you see these, do not add adjectives and do not raise weirdness. Change the
law or change the axis, per the unfamiliarity gate in the skill body. Then audit
the prompt and card:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/scripts/audit_unfamiliarity.py \
  --prompt PROMPT.txt --lyrics LYRICS.txt --card CARD.json \
  --compare-card RECENT_1.json --compare-card RECENT_2.json
```

## 5. Control experiments

When several generations feel the same, isolate the cause instead of guessing:

- **Prompt-only control:** same lyrics, stripped style prompt. If the sameness
  survives, the lyric form or the model's form prior dominates.
- **Lyrics-only control:** same style prompt, different lyric architecture. If
  the sameness survives, the style prompt dominates.
- **Persona-held pair:** same voice, two different replacement laws. Whatever
  differs is attributable to the law.

Label controls as controls. Never present one as a finished candidate.

## 6. Save this per accepted generation

Reproducibility is what makes the next comparison meaningful:

```text
Date and Suno model version:
Style prompt (exact text):
Exclude Styles (exact text):
Lyrics file path:
Persona or voice reference:
Advanced control values:
Unfamiliarity ledger and output signature:
Joint Hook Card / Topline Card / Timbre Card:
Proto-genre card, when applicable:
Which take was kept, and why the rejected takes failed:
```

Without the rejected-take reason you will re-run the same failure next week.

## 7. Delivery checks specific to Suno English output

- the hook is recognizable from rhythm or contour after one listen;
- every word of the load-bearing line is intelligible without the lyric sheet;
- the mixed phrase-length or breath law is audible in actual entrances and gaps;
- the reserved silence is still silent;
- the final chorus mutation is audible as a change of meaning, not a new song;
- no bracket tag was sung;
- the take is not a near-duplicate of the two most recent accepted takes on the
  saved signature.
