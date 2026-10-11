---
name: compose-topline-melody
description: Analyze chorus audio references and design, generate, and validate an original mouth-first listener hook, vocal topline, phoneme-level pronunciation or phoneme-triggered accompaniment, instrumental role or memory-harmony grammar, detailed time-varying timbre, or repeatable proto-genre grammar without copying an identifiable melody or singer. Use when a user provides WAV, MP3, MP4, or song references and asks how to hook listeners, create a catchy chorus or earworm, write a singable English or Korean hook or topline melody, break conventional instrumental arrangement, design distinctive pronunciation or timbre, generate an English or Korean song with Suno or ACE-Step, write or fix a Suno style prompt, invent a genre, or escape outputs that feel familiar, derivative, generic, or structurally repetitive.
---

# Compose Topline Melody

Create a chorus from measured melodic and timbral principles rather than averaging or imitating reference songs. Treat topline as pitch contour, rhythm, phrasing, breath, and lyric-vowel design. Treat timbre as spectral shape, harmonicity, attack, texture, and space—not loudness.

Reject “fill the chorus” versus “empty the chorus” as a single global choice.
Map occupancy separately across layers, frequency bands, and time. A strong
section can vacate one dimension while occupying another.

- Read [references/timbre-convention-breaking.md](references/timbre-convention-breaking.md) for instrumental-role or memory-harmony grammar, generic timbre, or short detailed prompts.
- Read [references/topline-pronunciation-convention-breaking.md](references/topline-pronunciation-convention-breaking.md) when contour tricks fail, pronunciation carries the hook, or phonemes govern the accompaniment.
- Read [references/hooking-convention-breaking.md](references/hooking-convention-breaking.md) for catchiness, earworms, retention, or listener-hooking methodology.
- Use `invent-genre-grammar` when the stall is the *genre* itself — every output landing in the same neighborhood, a genre tag returning its prototype, or a request to fuse or create a genre. It owns the genre atlas, the six law axes, and the distance script; this skill owns the topline, timbre, hook, and proto-genre cards it feeds.
- Read [references/greatness-convention-breaking.md](references/greatness-convention-breaking.md) when the goal is a song people replay, not merely an unfamiliar one: it covers how much surprise and where it goes, section-boundary abandonment, the earworm contour/gradient split, syncopation dose, perceptual voice specification, and which parts of the "generic AI sound" no prompt can fix.
- Read [references/suno-generation-english.md](references/suno-generation-english.md) before writing any Suno style prompt, and whenever the lyric is English: it maps the fields, the English rendering failure modes, and the normalization trap.

The audio analysis scripts need `librosa`, `scipy`, `soundfile`, `demucs`,
`torchcrepe`, and `opensmile`; the two text auditors need only the standard
library. Install what a step actually requires before claiming a measurement:

```bash
pip install librosa scipy soundfile demucs torchcrepe opensmile
```

## Workflow

### 1. Set the boundary

- Use only audio the user supplied or is authorized to use.
- Default to timbre/style conditioning. Do not use Cover or Source Audio unless the user explicitly requests preservation of melody or structure.
- Keep artist and song names out of generation prompts. Translate references into abstract attributes.
- Never claim that model conditioning eliminates copyright risk.
- When lyrics or a narrative concept exist, use
  `write-convention-breaking-lyrics` jointly. Do not freeze the topline and ask
  the lyric to fill note slots without one bidirectional revision pass.

### 2. Run the unfamiliarity-risk gate

Do not promise that a song has never been heard before. Reduce convergence on
genre prototypes and the creator's recent outputs with an auditable mechanism.
Novelty is not the number of unusual adjectives in a prompt.

Before composing, write:

```text
Frontier stall:
Dense prior being avoided:
Familiar shell retained:
Primary axis changed: melody / rhythm / harmony / form / lyric / timbre
Single causal mechanism:
Stable listener handle:
Measurable output signature:
Recent-output comparison:
Randomness guard:
Rejection condition:
```

Follow these rules:

- Diagnose the nearest dense prior. Examples include `minor + 4/4 + restrained
  repeated-note hook + late emotional lift`, four equal phrases that peak in
  phrase three, or a sparse-piano chorus whose only contrast is more intensity.
- Retain one familiar shell so the listener can orient: a pulse, short verbal
  hook, vowel frame, or recurring rhythmic cell.
- Change one primary causal mechanism, not every surface trait. Use at most one
  supporting timbral exception.
- Mood, genre, and instrument tags do not count as a mechanism. Changing seed,
  key, BPM, adjectives, or instrument nouns while preserving phrase logic is a
  parameter variation.
- Reject an exception that has no predicted listener effect, no stable handle,
  or no audible/measurable signature. Surprise without causality is randomness.

Write a compact signature for every accepted draft:

```text
meter | tempo band | chorus bars | phrase-length vector | peak zone |
contour | core range | identity carrier | ending direction | density delta |
timbre transformation
```

Compare with at least the two most recent accepted drafts when available. If
two consecutive drafts match at least 75% of populated signature fields, stop
changing prompt decoration and switch the primary axis or causal mechanism.
Do not deliberately make every signature field different.

Audit a candidate prompt and its mechanism card:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/scripts/audit_unfamiliarity.py \
  --prompt PROMPT.txt --lyrics LYRICS.txt --card CARD.json \
  --compare-card RECENT_1.json --compare-card RECENT_2.json
```

Warnings are rejection evidence, not a novelty score. A high adjective count
cannot be offset by adding more adjectives.

If the sameness is at the genre level — the same time, density, harmony, form,
voice, and production laws under different tags — diagnose it with
`invent-genre-grammar` first and measure the distance mechanically before
inventing anything. A new proto-genre built on your unexamined defaults is still
your old neighborhood.

If different prompts still produce the same musical grammar, stop naming new
styles and define a proto-genre. A genre name, lore, frequency, mood, instrument
swap, or negative-prompt list is not a new grammar.

Use one replacement law from which all audible invariants follow:

```text
Proto-genre name:
Frontier stall:
Inherited genre shell:
Rejected compositional law:
Replacement law:
Predicted listener effect:
Audible invariant 1:
Audible invariant 2:
Audible invariant 3:
Allowed variations:
Stable listener handle:
Three-song transfer test:
Generator failure mode:
Rejection condition:
```

Require three substantially different songs to preserve the invariants while
changing at least tempo, key, instrumentation, or lyrical scene. Until then,
call it a proto-genre, not an established genre. Reject it if listeners identify
only the tag or palette while the phrase, meter, harmony, and section logic
remain conventional.

Examples:

- **Breath-responsive pop:** accompaniment waits for completed vocal breaths;
  mixed phrase lengths and unfilled breath gaps follow from that single law.
- **Phoneme-clocked pop:** onset consonants trigger attacks, vowel nuclei sustain
  harmony, and codas or cutoffs mute it and set the gap. Reject an independent
  backing loop. Use the pronunciation reference for its card and transfer test.

### 3. Locate the real chorus

Do not equate loudness with chorus.

1. Extract MP4 audio to 48 kHz stereo WAV with `ffmpeg`.
2. Rank repeated beat-aligned regions on the vocal stem:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/scripts/find_repeated_sections.py \
  --audio /tmp/topline-demucs/htdemucs/TRACK/vocals.wav \
  --window-beats 16,24,32,48,64
```

3. Treat the output as candidates, not chorus labels. Confirm the lyric role,
   arrangement boundary, and at least one recurrence elsewhere in the song.
4. Separate vocals when pitch analysis of the full mix could follow bass or guitar:

```bash
python3 -m demucs.separate --two-stems vocals -n htdemucs --device cuda -o /tmp/topline-demucs INPUT.wav
```

Assign a structural confidence:

- **Confirmed recurring refrain:** long-window recurrence plus matching lyric role.
- **Probable refrain:** recurrence and arrangement agree, but lyrics are unavailable.
- **Excerpt hook only:** the source is too short to prove recurrence. Never relabel it as a chorus.
- **Live chant/outro:** repeated words or crowd singing alone do not make a compositional chorus.

### 4. Measure the topline

Run the bundled analyzer on the separated vocal:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/scripts/analyze_topline.py \
  --audio /tmp/topline-demucs/htdemucs/TRACK/vocals.wav \
  --start CHORUS_START --end CHORUS_END --device cuda
```

Record:

- robust and core pitch range;
- eight-part register contour;
- high-point position and separated high-zone episodes;
- start-to-end and high-zone-to-end pitch change;
- second-half register lift relative to the first half;
- stable-note density and duration, including first-to-second-half change;
- repeated-note, step, and leap proportions.

Run the same measurement on an equal-duration preceding section. Compare the
floor (`p05`), median, ceiling (`p95`), range, density, and repetition rather
than reporting chorus values without a baseline.

Treat values as estimates. Verify structural conclusions across repeated choruses and do not trust isolated pitch frames or a single separated stem.

### 5. Measure timbre, not loudness

Compare the preceding section and chorus at matched RMS. Analyze stems separately so arrangement changes are not mislabeled as vocal timbre:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/scripts/analyze_timbre.py \
  --mix INPUT.wav --vocal vocals.wav --instrumental no_vocals.wav \
  --before-start VERSE_START --before-end VERSE_END \
  --target-start CHORUS_START --target-end CHORUS_END
```

Use three evidence layers:

1. **Interpretable signal descriptors**
   - spectral centroid, slope, flatness, contrast, and flux;
   - low, warmth, presence, and air-band energy;
   - crest factor, attack behavior, stereo side-to-mid ratio, and correlation.
2. **Vocal quality descriptors**
   - eGeMAPS alpha ratio, Hammarberg index, spectral slopes, HNR, formants, jitter, and shimmer;
   - treat jitter and shimmer cautiously on singing and separated stems.
3. **Music timbre embeddings**
   - prefer a disentangled timbre head such as MERIT when testing similarity independently of melody and rhythm;
   - do not call raw MERT or CLAP cosine “timbre-only.”

Use AudioCommons hardness, depth, brightness, roughness, warmth, sharpness, boominess, and reverb only as secondary perceptual labels. Its public model was trained mainly on non-musical sound effects and is no longer maintained.

Do not reduce timbre to one brightness number:

- Spectral centroid moves with sung pitch as well as spectral envelope. When the
  median register moves by more than about three semitones, cross-check alpha
  ratio, Hammarberg index, band ratios, and the instrumental stem.
- A darker centroid can coexist with more presence or high-frequency harmonic
  energy. Describe that as a split result, not a contradiction to hide.
- Compare equal-duration sections. If a chorus changes direction internally,
  compare its first and second halves again to detect a timbral handoff.
- Raw RMS is a section-energy control, not a timbre descriptor.
- Gender, voice class, register, `warm/bright`, and `dry/centered` locate a
  performer or mix; they do not by themselves specify a distinctive timbre.
- Prefer time-localized behavior such as grain appearing only at phrase endings
  or vibrato entering late over a pile of static adjectives.
- Match every negative guard with a positive acoustic or articulatory
  replacement. `Not whispery` becomes `firm fundamental with little air`.

### 6. Co-design lyric and topline

Reject "melody carries emotion while lyrics carry meaning." Pitch, duration,
breath, phoneme timing, vowel trajectory, syntax, and silence jointly determine
what the listener hears. Use the pronunciation reference for phoneme-level work.

Build the hook in alternating passes:

1. Ask the lyric skill for two to four semantic slots: setup, contradiction,
   withheld word, and landing.
2. Hum a rhythmic cell and open-vowel frame without final words.
3. Fit load-bearing words and measure heard syllables, breath points, and peak
   vowel.
4. Permit one word to request a melodic revision and one melodic event to
   request a textual revision.
5. Choose what stays invariant across returns: wording, rhythmic cell, vowel
   frame, or contour.

Choose at most one primary coupling exception:

- **Melody as unreliable narrator:** stable words claim certainty while cadence,
  breath, or register exposes doubt.
- **Semantic contour inversion:** hopeful text falls or refusal rises, with a
  clear listener-facing reason.
- **Grammatical spotlight:** a pronoun, particle, or ending—not the grand noun—
  receives the high or long note.
- **Withheld landing:** the expected answer is a rest in the first chorus and a
  sung word later.
- **Contour-stable mutation:** the melody remains recognizable while one
  load-bearing lyric word changes.
- **Text-stable mutation:** exact words recur while contour, cadence, or breath
  changes their meaning.
- **Negative-density sentence:** the key sentence has fewer notes and more
  silence than the setup.
- **Vowel-frame variation:** the vowel colors and rhythm persist while words and
  pitch direction change.

Treat natural speech prosody as a baseline, not a prison. A mismatch is valid
only when repeated or contrasted enough to sound intentional and when it
intensifies the song's central contradiction.

Use a Joint Hook Card:

```text
Hook's semantic job:
Hook's melodic job:
Load-bearing word:
Phrase syllable slots:
Breath vector and inherited state:
Peak syllable and vowel:
Word-to-peak relation: aligned / inverted / displaced
Meaning of the main rest:
Return mutation: word / contour / cadence / breath
Stable identity layer:
Primary lyric-topline exception:
Rejection condition:
```

### 7. Choose the broken melodic and timbral convention

A named melodic exception is still a conventional technique. For a genuinely
unfamiliar topline, define a return-to-return transformation law from the
topline-pronunciation reference. Choose one primary melodic law and one primary
timbral exception at most.

Melodic exceptions:

- **Falling payoff:** reach the peak near the middle, then finish lower.
- **Narrow hook:** keep most notes within 4–6 semitones and let duration carry the hook.
- **Anchor and jump:** chant around one center note, then use one exceptional fourth, fifth, or sixth.
- **Delayed lift:** repeat the rhythmic cell twice before raising its register.
- **Late staircase:** repeat tones inside each phrase, raise the phrase center in small steps, place the high zone at 68–82%, and finish only 1–3 semitones below it.
- **Asymmetric breath:** preserve the motif while changing one phrase length or pickup.
- **Breath-governed meter:** let the completed vocal breath determine the next
  accompaniment entrance. Plan an audible mixed-length cycle such as
  `4 + 5 + 3 + 6` beats, keep one hook rhythm stable, and leave the breath gap
  unfilled instead of decorating it.
- **Raised floor:** move the low floor and median upward while barely moving the
  ceiling, so the chorus becomes higher but narrower.
- **Opening summit:** place the high zone in the first third, then let a
  7–12-semitone fall become the payoff instead of building to a late peak.
- **Two-shelf refrain:** alternate between two stable register bands several
  times instead of using a staircase or one exceptional leap.
- **Negative-density hook:** keep the center and range nearly unchanged while
  reducing note density; let longer gaps, vowels, or attacks identify the hook.

Timbral exceptions:

- **Subtractive close-up:** remove layers at the chorus, keep the vocal dry and centered, and create intensity through proximity.
- **Dark crest:** let pitch rise while vocal spectral tilt darkens instead of brightening.
- **Soft-impact hook:** use slower attacks and less hardness at the emotional peak.
- **Split space:** keep the vocal narrow and dry while the instruments become wide and wet, or invert that relationship.
- **Texture reveal:** expose breath, pick, fret, bow, or room noise instead of polishing the chorus smoother.
- **Static palette:** keep instrumentation and brightness stable; make articulation or phrasing carry the section change.
- **Asymmetric occupancy:** empty one layer, band, or time slot while another
  fills it; for example, let the backing gain energy while the vocal recedes or
  let note density fall while spectral width grows.
- **Two-ended spectrum:** add low-end weight and upper presence together. The
  centroid may stay flat or fall even though the spectrum feels larger.
- **Timbral handoff:** let the vocal carry brightness or tension in the first
  half, then darken or fall while the instruments take over width and motion.
- **Still-weight impact:** increase sustained low-end mass while reducing
  spectral flux, attack activity, or vocal roughness.

Do not combine every observed trait. Give the new chorus one governing melodic idea and one governing timbral idea.

Use these as diagnostic signatures, not universal composition laws:

- **Raised floor:** the floor rises more than the ceiling and robust range
  contracts by roughly 1.5 semitones or more.
- **Opening summit:** the high point lands before 35% and the ending sits at
  least about 7 semitones below the high zone.
- **Two-shelf refrain:** three or more separated returns to a high register
  alternate with a stable lower band.
- **Negative-density hook:** pitch median changes by less than about 2 semitones
  while stable-note density falls by roughly 15% or more.
- **Asymmetric occupancy:** vocal and instrumental energy move in opposite
  directions, or note density falls while width or spectral motion grows.
- **Two-ended spectrum:** low-band and presence-band ratios both rise while
  centroid stays flat or falls.
- **Still-weight impact:** low-band energy or RMS rises while spectral flux does
  not rise.

Choosing an exception is not the same as dosing it. Before writing the ledger,
fill the Surprise Schedule Card in
[references/greatness-convention-breaking.md](references/greatness-convention-breaking.md):
match each deviation's size to its section's entropy, put the harmonic
strangeness outside the chorus, keep the global contour archetypal while the
gradients between turning points are unusual, and elide every section boundary
instead of announcing it.

Use a convention ledger before writing:

```text
Expected convention:
Axis being inverted:
Measured evidence:
Listener-facing effect:
Generation instruction:
Rejection condition:
```

Reject a proposed exception if it only changes loudness, lacks a measurable
contrast from the setup, or merely reproduces an identifiable reference phrase.

### 8. Write design cards

Define this before generation:

```text
Core register:
Total range:
Rhythmic cell:
Hook carrier / cross-song identity carrier:
Repeat plan:
Exceptional interval:
High-point position:
Phrase lengths:
Phrase-length law and mixed-meter cycle:
Breath gaps the arrangement must not fill:
Phoneme-to-arrangement trigger map:
Ending direction:
High-zone-to-ending distance:
Later-chorus variation:
Lyric vowel at the peak:
Joint Hook Card:
Primary broken convention:
Baseline-to-chorus floor / median / ceiling change:
Baseline-to-chorus density change:
High-zone episode count:
```

Use these defaults only when the references do not argue otherwise:

- Place about 80% of pitched material inside a 4–6-semitone core.
- Keep the total range within an octave.
- Repeat one rhythmic cell three times; alter pitch or cadence on the third.
- Use at most one 4–7-semitone leap. Omit it when phrase-level register steps carry the lift.
- Put the high point around 55–75% for an explosive payoff or 68–82% for an intimate late crest.
- Let repeated notes carry 35–55% of stable-note transitions when rhythm is the hook carrier.
- Keep later choruses in the same range; create escalation by moving the crest earlier, shortening note values, or tightening pickups.
- On sustained high notes prefer an open vowel — Korean `아`, `어`, `오`, or
  English `ah`, `aw`, `oh` — and never a plosive or a consonant cluster. In
  English also avoid a diphthong on the longest note unless the drift is the
  intended effect; use a monophthong instead.

Define timbre separately:

```text
Vocal harmonicity and spectral tilt:
Vocal attack and breath:
Instrument hardness and roughness:
Low, warmth, presence, and air balance:
Vocal space and width:
Instrument space and width:
Occupancy map by layer / frequency / time:
Section transformation:
First-half to second-half handoff:
Primary broken timbre convention:
```

Complete the Timbre Card and, when relevant, Instrumental Grammar Card in
[references/timbre-convention-breaking.md](references/timbre-convention-breaking.md).
The voice base, register, and mix position are context fields, not the timbral
exception. Keep one stable identity while one acoustic behavior changes in a
named part of the phrase.

### 9. Protect originality

- Write new lyrics and a new pitch-rhythm contour.
- Do not transcribe, hum, or reconstruct the reference melody.
- If a draft resembles a reference, change at least two of: rhythmic cell, interval direction, phrase boundary, peak location, or cadence.
- Use balanced reference excerpts for timbre. Match their RMS levels so one source does not dominate.
- Avoid cloning a distinctive singer. Prefer instrumental stems for reference conditioning when only the band timbre is needed.

### 10. Generate with Suno or ACE-Step

For Suno, work from
[references/suno-generation-english.md](references/suno-generation-english.md)
for the field map, the style-prompt order, the English rendering failure modes,
and the control experiments. The essentials:

- Put the replacement law in the first two sentences of `Style of Music`.
- Move every negative guard into `Exclude Styles`; a negative stated inside the
  style prompt often summons the excluded thing.
- Hold the voice constant with a persona when comparing two laws, so the
  difference is attributable to the law rather than the singer.
- Do not use a weirdness or style-influence slider as the primary axis. It
  produces surface deviation, not a new compositional law.
- For English lyrics, run the lyric-side Suno checks before generating:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/write-convention-breaking-lyrics/scripts/audit_lyrics.py \
  --lyrics LYRICS.txt --hook "HOOK" --lang en --suno
```

- State the beat or phrase-length cycle explicitly and name what must remain
  stable for recognition.
- Write the literal mouth-first hook before the style prompt. Put at least two
  returns in the lyrics field and pass that file to the audit; do not rely on
  section labels alone to create timing.
- Treat the prompt as a request, not proof of compliance. Reject outputs that
  normalize the law into a standard four-bar loop or express novelty only
  through instrumentation.
- Under a 1,000-character style budget, reserve one compact timbre sentence for
  spectral body, air, texture location, articulation, vibrato, and space. Use
  one audible contradiction and at most two negative guards.
- Keep artist names out of the prompt. Save the exact style prompt, lyrics, and
  proto-genre card for comparison across generations.

For ACE-Step:

- Build a 30-second reference from equal-length excerpts.
- Prefer stable `no_vocals` excerpts for instrumental timbre design; reject stems with obvious separation artifacts.
- Use `task_type="text2music"` with `reference_audio`; do not pass `src_audio`.
- Supply only `[Chorus]` lyrics for a chorus-only result.
- Generate 28–40 seconds with the turbo checkpoint at 8 steps.
- Describe vocal delivery, instrumentation, dynamics, and mix in the prompt without naming artists or songs.
- State one hook carrier, one broken melodic convention, and one broken timbral convention. Do not ask the model to maximize every measured trait.
- State one lyric-topline exception only when lyrics are present.
- Save the seed, unfamiliarity ledger, signature, Joint Hook Card, Topline Card,
  and Timbre Card.
- When repeated generations stay alike, render one diagnostic control without
  reference audio. If the sameness remains, the prompt or form prior dominates;
  if it disappears, reference conditioning dominates. Label this as a control,
  not a finished candidate.

### 11. Validate and deliver

Verify:

- correct duration, sample rate, stereo channels, and decodable WAV/MP3;
- no unintended silence longer than one second;
- no clipping above the chosen ceiling;
- generated contour follows the Topline Card;
- the hook is recognizable from rhythm or contour after one listen;
- the draft passes its unfamiliarity-ledger rejection condition;
- its signature is not a near-duplicate of two consecutive accepted drafts;
- its primary difference is a causal mechanism rather than seed, key, tempo,
  genre adjective, or instrument substitution;
- one stable listener handle survives the convention break;
- for a proto-genre, all three audible invariants derive from the same
  replacement law;
- its invariants survive the three-song transfer test instead of reproducing
  one arrangement three times;
- a claimed breath- or phoneme-governed result is heard in actual attacks,
  sustains, entrances, and gaps, not inferred from prompt text;
- the lyric-topline exception is audible in the performance, not only
  explainable from the cards;
- every mutated return preserves at least one identity layer: wording, rhythmic
  cell, vowel frame, or contour;
- the exceptional interval occurs once or sparingly;
- the ending creates the intended closure or residue;
- the claimed convention break has a baseline measurement and a rejection threshold;
- timbre comparisons are loudness-matched and stem-specific;
- the intended spectral, texture, and space directions are present;
- pitch-sensitive centroid claims agree with at least one spectral-envelope descriptor;
- if MERIT is available, timbre similarity moves toward the target while melody similarity does not.

For an English Suno take, also run the delivery checks in section 7 of
[references/suno-generation-english.md](references/suno-generation-english.md):
intelligibility of the load-bearing line, silence that stayed silent, no sung
bracket tag, and a saved record of why the rejected takes failed.

Deliver the MP3, WAV, seed, lyrics, unfamiliarity ledger and signature, Joint
Hook Card, Topline Card, Timbre Card, the proto-genre card when applicable, and
a concise explanation of which lyric-topline, melodic, timbral, or generative
grammar convention was broken.
