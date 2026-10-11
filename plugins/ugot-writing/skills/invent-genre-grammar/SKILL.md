---
name: invent-genre-grammar
description: Diagnose why generated songs keep landing in the same genre, measure genre distance across six constitutive law axes, deliberately sample a far genre, invert one genre-defining law while keeping recognizability, hybridize two genres by swapping laws instead of blending sounds, and build a new proto-genre from one replacement law. Use when outputs feel like the same genre every time, when a genre tag produces a prototype instead of a design, when asked to create or invent a genre, break genre conventions, fuse genres, study or choose a genre, escape an indie/pop or lo-fi default, or pick a style prompt that is genuinely far from recent work.
---

# Invent Genre Grammar

A genre is not a mood, a palette, or a tag. It is a set of **laws** about how time,
density, harmony, form, voice, and production are organized. Two songs with
different instruments and the same six laws are the same genre; two songs with
the same instruments and one different law are not.

That is why "try a different genre" usually fails: swapping adjectives and
instrument nouns leaves all six laws untouched, so the generator returns to the
same neighborhood.

Read [references/genre-atlas.md](references/genre-atlas.md) for the law values of
about forty genres grouped by time law, plus each genre's inviolable element and
the single law worth inverting. Use `compose-topline-melody` for the topline,
timbre, hook, and proto-genre cards this skill feeds, and
`write-convention-breaking-lyrics` for the words.

## The six law axes

Every genre choice, distance measurement, and hybrid in this skill is expressed
on these axes. Never describe a genre without filling all six.

1. **Time law** — what organizes time: isochronous backbeat, asymmetric timeline
   or clave, additive/aksak cells, nested colotomic cycles, cyclic tala,
   free/rubato, breath-clocked, speech-clocked, hyper-tempo.
2. **Density law** — where subdivision energy sits: straight, swung, offbeat
   hats, bass-punctuation (log drum), triple-against-duple, blast-density,
   negative-density.
3. **Harmony law** — functional diatonic, modal loop, static drone or one chord,
   two-chord vamp, borrowed-chord surprise, non-Western scalar system, quartal or
   planing, riff-as-harmony.
4. **Form law** — verse–chorus, riddim plus versions, cyclic with no chorus,
   colotomic gong cycle, call-and-response, build–drop, through-composed,
   loop-with-mutation.
5. **Voice law** — belted, melismatic/portamento, spoken or MC-led, shouted,
   whispered close, choral unison, processed-as-instrument, absent.
6. **Production law** — dry and close, desk-as-instrument, distortion-as-texture,
   space-as-content, lo-fi artifact, hyper-clean, mono-forward.

## Workflow

### 1. Diagnose the neighborhood you are stuck in

Before choosing anything, write out the six law values of your last two or three
accepted outputs. Do not write genre names; write laws. The typical stall looks
like this:

```text
time: isochronous backbeat | density: straight | harmony: functional diatonic
form: verse-chorus | voice: whispered close | production: dry and close
```

If those six values repeat, the problem is not the tag, the tempo, the key, or
the instrument list. Note also **whose** prior it is: your own writing habit, the
generator's center of mass, or a reference set you keep re-reading. All three
pull toward the same streaming-indie center.

### 2. Measure the distance instead of trusting your sense of novelty

Write the candidate spec as JSON with the six axes, then:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/invent-genre-grammar/scripts/genre_distance.py \
  --spec CANDIDATE.json \
  --compare RECENT_1.json --compare RECENT_2.json
```

It reports per-axis matches, a distance in [0,1], tempo and palette proximity,
and — most useful — the **unused law inventory**: the axis values in the atlas
that none of your specs have ever used. Require at least three of six axes to
differ from every recent spec. Two axes is a variation; one is a re-skin.

The script is a convergence detector, not a taste judge. A distant spec can still
be bad; a close spec is reliably repetitive.

### 3. Choose one of four moves

Pick exactly one. Mixing moves produces mush.

- **Sample far.** Take a genre from an unused time-law family in the atlas and
  adopt all six of its laws honestly, including the ones that are uncomfortable.
  This is the fastest cure for sameness and the easiest to render.
- **Invert one law.** Keep a genre recognizable on five axes and invert the sixth
  — specifically the one its listeners treat as inviolable. The atlas names that
  element and the inversion for each genre.
- **Swap laws (hybridize).** Take the time and density laws from genre A and the
  harmony, form, or voice law from genre B. See below.
- **Replace a law (invent).** Define a new law that no existing genre uses, then
  derive three audible invariants from it. This is `compose-topline-melody`'s
  proto-genre procedure; use its card and its three-song transfer test rather
  than duplicating them here.

### 4. Hybridize by law swap, not by sound blending

"Genre A meets genre B" prompts produce an average, and averages sound generic.
Instead assign each axis to exactly one parent and write the assignment down:

```text
time law:        from A
density law:     from A
harmony law:     from B
form law:        from B
voice law:       from A
production law:  from B
Which parent wins a conflict:
What is lost by the assignment (name it, do not pretend nothing is lost):
```

Two rules make the difference between a hybrid and a mess:

- **Time and density should come from the same parent.** They are physically
  coupled; splitting them usually yields a rhythm that neither parent's players
  could perform.
- **Never split an axis.** "Half dembow, half backbeat" is not a law.

Then check the hybrid for **law collision**: if parent B's form law requires a
section boundary where parent A's time law has no cadence point, one of them
must yield. Say which, in the prompt.

### 5. Keep one handle so the listener can orient

An unfamiliar law needs a familiar anchor or it reads as incompetence. Retain one
of: a recognizable pulse, a short verbal hook, a vowel frame, a rhythmic cell, or
a conventional chorus. Per the contrastive-surprise law in
`${CLAUDE_PLUGIN_ROOT}/skills/compose-topline-melody/references/greatness-convention-breaking.md`,
the anchor is usually best placed in the chorus while the strangeness lives
elsewhere.

### 6. Execute in the generator

The atlas gives, for each genre, the concrete surface a generator responds to:
era, instrument names, articulation, tempo band. Use those words, not the axis
names.

There is an unresolved tension here, and you should treat it as unresolved:
practitioner guides report that Suno responds well to era, mood, instrument
names, and structural tags, and **poorly to music-theory vocabulary and to
instructions phrased as rules** — which is the opposite of the law-first prompt
that `compose-topline-melody` prescribes. Both cannot be fully right.

Resolve it by test, not by preference:

- **Take R (rule form):** the law stated as an imperative, first two sentences.
- **Take D (description form):** the same law expressed only as audible surface —
  what enters when, what stays silent, which instrument plays which figure, era
  and articulation words — with no imperative and no theory terms.
- Hold everything else constant, including the lyrics and the voice.
- Judge which take actually obeys the law, not which sounds nicer.

Record the winner per law type; some laws (entrance timing, phrase length) may
need description form while others (what must not be filled) survive as rules.

**Observation so far (n = 1, highlife, 2026-07-26):** the rule form was preferred
on musical satisfaction. Two cautions before generalizing it. First, that is a
different measurement from law compliance, which the practitioner claim was
actually about — a take can sound better while obeying less. Second, the
description take in that pair also contained quality-degrading words
(`slightly boxy`, `unpolished`, `live to tape`), so form and fidelity were
confounded; one pair cannot separate them, and Suno's take-to-take variance is
large enough that a single pair is weak evidence either way.

**Default until more data exists: the hybrid form.** Keep imperatives for the
non-negotiable constraints — what must stay audible, what must never be filled,
what must not answer — and use description for era, ensemble, and palette, which
is what the generator grounds the sound in. Never spend description budget on
words that degrade fidelity (`boxy`, `cheap`, `unpolished`, `lo-fi`) unless the
degradation is the design; they read as instructions to sound worse.

When comparing forms, generate at least two takes per form so variance does not
decide the verdict for you.

Also useful and low-risk:

- Raise the weirdness control only for genres whose identity is disorder — glitch,
  IDM, hyperpop, deconstructed club. For everything else it adds surface noise,
  not a new law.
- Use the exclude field for the instruments a genre tag habitually drags in: an
  acoustic prompt attracting electric guitar and synth pads, a "pop" prompt
  attracting a four-on-the-floor kick.
- Prefer a specific subgenre and era over a family name. A family name returns the
  family's center of mass, which is exactly the prototype you are escaping.

### 7. Validate

- all six law values are stated, and none is a mood word;
- the distance script shows at least three axes differing from every recent spec;
- for an inversion, the inverted law is the one the genre's listeners treat as
  inviolable, and the other five are intact;
- for a hybrid, time and density come from one parent and no axis is split;
- for an invention, three audible invariants follow from one replacement law and
  survive the three-song transfer test;
- one orientation handle is present and identifiable after one listen;
- the render actually exhibits the law in attacks, entrances, and gaps — not only
  in the prompt text;
- the genre is not identifiable **only** by its palette. Strip the signature
  instrument mentally: if nothing genre-defining remains, you chose a costume.

## Deliver

The six-axis spec, the chosen move, the hybrid assignment or inversion ledger,
the distance report, both prompt forms when the R-versus-D question is still
open, the orientation handle, and a named loss — what this genre choice gives up.
