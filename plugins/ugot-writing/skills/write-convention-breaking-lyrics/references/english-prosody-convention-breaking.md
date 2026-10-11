# English prosody: what to break and how to hear it

Read this when the lyric is in English. The Korean rules in the skill body
assume a syllable-timed mouth; English is stress-timed, so the same intentions
require different levers.

## 1. The unit that governs English text-setting is the stress beat

English compresses and expands unstressed syllables to keep strong beats on the
pulse. Consequences you must design around:

- A line's **stress-beat count**, not its syllable count, decides how it lands.
  `I left the kitchen light on for you` (10 syllables) and `Your mug is upright`
  (5 syllables) can both occupy four beats.
- Therefore varying syllable counts is **not** a broken breath grammar. Ordinary
  English already does that. If the stress-beat vector stays flat while syllable
  counts wobble, you changed nothing. The auditor emits this warning explicitly.
- To change phrasing you must change the **stress-beat vector** (for example
  `4 / 4 / 2 / 5`), the position of stresses against the pulse, or the breath
  boundary — not the syllable count alone.
- Function words (articles, prepositions, auxiliaries, pronouns) carry no
  lexical stress. Putting one on a strong beat is a real, audible deviation; use
  it as the grammatical spotlight, not by accident.

Measure before claiming:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/write-convention-breaking-lyrics/scripts/audit_lyrics.py \
  --lyrics DRAFT.txt --hook "HOOK" --lang en --suno \
  --compare RECENT_1.txt --compare RECENT_2.txt
```

Read `stress=` alongside `syllables=`, and read `stress_shape_similarity` in the
comparison line. A new song with the same stress shape is the same song.

## 2. English-specific conventions worth breaking

Choose **one** primary break. For each, the entry gives the inherited law, the
replacement, the listener effect, and how to confirm it survived generation.

1. **End-rhyme closure law.** Convention: rhyme marks the end of a thought;
   couplets close. Replacement: place the rhyme on an unstressed syllable
   (`water` / `daughter` is conventional; `over` / `pull her` is not), or delay
   the answering rhyme until a later section so the first return sounds
   unfinished. Effect: unresolved forward lean. Confirm: `rhyme_signature`
   should not be a textbook `AABB`/`ABAB` in every section.
2. **Rhyme-as-payoff law.** Convention: the last line rhymes hardest.
   Replacement: leave the final line of the chorus unrhymed and un-landed, and
   pay the rhyme only in the final chorus. Confirm: the rhyme scheme changes
   between chorus returns.
3. **Iambic default.** Convention: weak-strong feet, stress on the downbeat.
   Replacement: set a consistent stressed-syllable-on-the-offbeat pattern, or
   open the hook with two adjacent stresses (a spondee) against the pulse.
   Effect: physical insistence, or the sound of a person interrupting.
4. **Monosyllabic pop-diction law.** Convention: hooks use short Anglo-Saxon
   words. Replacement: put one polysyllabic Latinate word at the emotional peak
   and let its extra syllables crowd the bar. Effect: the speaker sounds like
   they are managing themselves rather than confessing.
5. **Contraction-smoothing law.** Convention: contract everything for flow.
   Replacement: uncontract exactly once at the peak (`I am not asking you`),
   adding a syllable and stiffening the line. Effect: audible formality under
   strain. This is the cheapest reliable break in English.
6. **Open-vowel-on-the-high-note law.** Convention: sustain `ah`, `oh`, `ay`.
   Replacement: sustain a nasal or voiced continuant (`m`, `n`, `ng`, `l`, `v`,
   `z`) or a close vowel on the peak. Effect: the peak sounds swallowed or
   held-in instead of released. Verify in the render, since a generator may
   substitute an open vowel.
7. **Diphthong-glide law.** Convention: long notes take diphthongs, which drift
   (`time` becomes `tah-eem`). Replacement: put a monophthong on the long note
   and the diphthong on a short one, so the sustained vowel stays still.
8. **Second-person dyad law.** Convention: `I` sings to `you` for the whole
   song. Replacement: keep the scene concrete while moving the addressee once —
   to a third party, a plural, an object, or the speaker's earlier self. Keep
   the pronoun aperture traceable to one word.
9. **Present-tense immediacy law.** Convention: everything happens now.
   Replacement: use a future perfect or an anticipated memory (`I will have
   moved it by the time you ask`), anchored to one measurable present detail.
10. **Title-in-the-first-chorus-line law.** Convention: the title lands first
    and loudest. Replacement: withhold the title until the last line of the
    chorus, or until the final chorus, so the earlier returns are questions.
11. **Adjective-front law.** Convention: emotion arrives as adjectives
    (`broken`, `endless`, `golden`). Replacement: ban evaluative adjectives from
    the chorus and let verbs and measurements carry the feeling. Effect: the
    listener judges instead of being told.
12. **Rhyme-family monotony.** Convention: `-ight`, `-ay`, `-ee`, `-art` chains,
    which the model reaches for first. Replacement: build an assonance chain on
    one vowel color with different codas, or a consonance chain on a repeated
    coda with different vowels. Confirm: `dominant_rhyme_tails` should not be
    dominated by one tail.

Combine at most one of these with one melodic exception from
`compose-topline-melody`. Two simultaneous breaks read as incompetence, not
intent.

## 3. Breath inheritance in English

The skill body's breath-inheritance law applies, but the boundary markers
differ. An English breath is unfinished when the line ends on:

- a conjunction or subordinator (`and`, `but`, `because`, `'cause`, `so that`);
- a preposition or particle (`on`, `for`, `into`, `out of`);
- a determiner or possessive (`the`, `my`, `another`);
- an auxiliary awaiting its verb (`I have`, `you were`, `I couldn't`);
- a mid-word cutoff on a hyphen.

The next breath must pay that debt before opening a new one. The auditor labels
these `inherited` and warns when a draft of eight or more lines contains none —
that draft resets every breath no matter how the lines are formatted.

Do not split a phrasal verb or a compound noun across a breath unless the
spotlight is the point; English listeners hear that as a mistake rather than as
suspense.

## 4. Singability physics to respect while breaking conventions

- Plosives (`p`, `t`, `k`, `b`, `d`, `g`) cannot be sustained. Never put one on
  the longest note; put it on the attack before it.
- Sibilant stacks (`s`, `sh`, `z`) across a word boundary (`this song's silence`)
  smear at speed and in a generator's phoneme model.
- Four-plus consonant clusters (`strengths`, `sixths`, `glimpsed`) fail on short
  notes. The auditor lists them under `consonant_clusters`.
- Close vowels (`ee`, `oo`) tighten at the top of a singer's range and a
  generator often replaces them with an open vowel. If a close vowel on the peak
  *is* the exception, verify it in the render, not in the prompt.
- Vowel + `r` (`fire`, `hour`, `tired`, `higher`) is elision-ambiguous: sung as
  one or two syllables depending on delivery. The auditor lists these; decide the
  count yourself and write the line so either reading scans.
- Words ending in a voiceless stop lose their coda at high pitch and volume.
  If a load-bearing word must be heard, end it on a vowel or a continuant.

## 5. English generated-lyric tells

Beyond the skill body's list, these phrasings mark machine-written English pop.
Flag, do not auto-ban:

- `chasing shadows`, `breaking free`, `endless night`, `we were young`,
  `nothing left to lose`, `light in the dark`, `pieces of me`, `learn to
  breathe`, `find my way back`, `in the end`;
- `like a` similes whose vehicle never acts again;
- an abstract noun paired with a body part (`the weight of my heart`);
- adverb padding (`slowly`, `softly`, `silently`) that no action needs;
- second-line restatement of the first line in different words;
- a bridge that names the lesson (`and now I finally see`);
- present participles opening three consecutive lines (`standing`, `waiting`,
  `holding`).

Repair by adding ownership, malfunction, measurement, residue, cost, or an
irreversible action — the same repairs as the skill body, applied to a concrete
noun the speaker physically handles.

## 6. English Prosody Card

Fill this before drafting and deliver it with the lyric:

```text
Stress-beat vector per section:
Syllable band per section:
Stress-against-pulse plan: aligned / offbeat / spondee-open
Function word on a strong beat (grammatical spotlight):
Peak syllable and its vowel type: open / close / nasal / diphthong
Sustained note phoneme (must be sustainable):
Rhyme grammar: perfect / weak / assonance chain / consonance chain / withheld
Rhyme scheme per section, and what changes on return:
Breath boundaries and the inherited state at each:
Elision-ambiguous words and the count you chose:
Primary English convention broken (from section 2):
What stays stable for recognition:
Rejection condition:
```

## 7. Sources

- Pat Pattison, prosody as all elements serving one intent:
  https://online.berklee.edu/takenote/prosody-in-music-and-songwriting/
- Smith on prosodic dissonance between spoken and sung prosody:
  https://mtosmt.org/issues/mto.24.30.2/mto.24.30.2.smith.html
- Text-setting typology (unified, music-dominated, lyric-accentuated,
  speech-timed): https://doi.org/10.30535/mto.30.2.6
- Corpus evidence of rising repetition and falling lexical complexity in
  English popular lyrics: https://doi.org/10.1038/s41598-024-55742-x
- Repetition raising processing fluency until word-level repetition cancels it:
  https://doi.org/10.1016/j.jcps.2014.12.004

Do not store or reproduce complete copyrighted lyrics in this skill.
