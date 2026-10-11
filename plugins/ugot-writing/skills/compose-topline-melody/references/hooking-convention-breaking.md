# Convention-Breaking Listener Hooking

Use this reference when the user asks for a catchy chorus, earworm, immediate
hook, listener retention, or a song that remains memorable without sounding
formulaic.

## Contents

1. [The inversion](#the-inversion)
2. [Mouth-first gate](#mouth-first-gate)
3. [Prediction-debt method](#prediction-debt-method)
4. [Hook carriers](#hook-carriers)
5. [Hooking Card](#hooking-card)
6. [Suno field split](#suno-field-split)
7. [Prompt grammar](#prompt-grammar)
8. [Validation](#validation)

## The inversion

Reject these inherited assumptions:

- hooking means louder, higher, faster, earlier, or denser;
- exact repetition automatically strengthens memory;
- surprise is valuable even when the listener cannot infer its logic;
- the hook is an object contained inside one melodic phrase;
- melody alone owns the hook;
- every expectation should resolve immediately.

The prediction-debt law alone is insufficient. A listener cannot learn a
relation when its seed has no immediate sensory or motor grip. Use this
replacement law:

> A vocal hook first makes the mouth want to reproduce a short phonetic
> gesture. It then leaves one learnable prediction debt that moves across
> returns and closes later.

This is a practical composition heuristic, not a universal neuroscience claim.
Intensity may attract attention, but attention is not evidence that the musical
relation was learned.

## Mouth-first gate

Write the literal lyric fragment before describing genre, mood, harmony, or
production. `One five-syllable hook` is not a seed; it delegates the decisive
choice back to the generator.

For a Korean vocal hook, define:

1. **Actual text:** a natural three-to-seven-heard-syllable phrase.
2. **Motor duration:** usually about 0.8–1.5 seconds before the phrase releases.
3. **Onset pattern:** the consonant sequence that creates taps, drags, or
   pickups.
4. **Vowel path:** a stable sequence of mouth shapes, preferably with one clear
   opening or rounding motion.
5. **Motor contrast:** one bodily change, such as closed-to-open, clipped-to-
   sustained, or tense consonant-to-relaxed vowel.
6. **Pitch inventory:** usually one to three pitches so pronunciation remains
   the reproducible object.
7. **Pitchless test:** the phrase must remain satisfying to speak or chant
   without melody.

Respect natural Korean phonology. Count heard syllables, account for liaison,
and never invent an accent or break a word merely to look unusual. A clever
phoneme diagram cannot rescue an awkward sentence.

Reject the seed when:

- only its syllable count is specified;
- it requires melody or production to feel rhythmic;
- the mouth gesture changes completely on every return;
- the phrase is semantically empty filler;
- a load-bearing word becomes unclear;
- it resembles an identifiable singer's signature diction.

## Prediction-debt method

### 1. Give orientation

Start with one concrete seed that can be encoded after one exposure:

- the literal mouth-first phrase;
- one center pitch or chord role;
- a recognizable cutoff and silence;
- one timbral event at a fixed phrase location.

Do not make every surface unfamiliar. The seed is the listener's handle.

### 2. Create one prediction

Make the first return imply one specific next event: a cadence note, vowel
arrival, consonant attack, bass answer, chord resolution, or onset of silence.
If several predictions compete, the hook has no clear debt.

### 3. Withhold or displace the event

Remove, delay, recontextualize, or transfer the expected event. Do not replace
it with arbitrary surprise. Preserve enough of the seed that the listener can
recognize what was withheld.

### 4. Carry the debt

Make the missing event become the next phrase's state:

- the unresolved ending becomes the next center note;
- the omitted vowel returns as the next phrase's opening vowel;
- the absent kick determines the next entry;
- the same pitch changes harmonic function instead of resolving;
- a coda releases into an unfilled rest that the next phrase inherits.

The relation between returns, not one isolated sound, is the hook.

### 5. Apply a deterministic return operator

Write `A, T(A), T²(A)` rather than `A, A, A'`. State exactly what stays and what
moves. Useful operators include inherit, rotate, migrate, substitute, delay,
remove, and restore.

The operator must be simpler than the resulting music. “Make the third return
more emotional” is not an operator.

### 6. Close or deliberately renew

Name the return on which the listener's debt resolves. Usually two to four
returns are enough to expose the law. Endless withholding becomes vagueness.
If the final return renews the debt instead, make the new prediction explicit.

## Hook carriers

Choose one primary carrier and at most one supporting carrier.

### Melody

Keep a rhythm or vowel frame invariant while one boundary note inherits the
previous cadence. Avoid treating a large leap or high note as sufficient.

### Pronunciation

Rotate onset timing across returns while the vowel remains the pitch anchor.
Preserve the load-bearing word's intelligibility.

### Harmony

Keep one note stable while harmony recasts it as chord tone, extension,
suspension, or leading pressure. The changing function is the event.

### Silence

Advance one absent event through the phrase by a fixed rule. Leave the gap
unfilled so the listener can internally supply it.

### Timbre

Keep the vocal identity stable while one time-localized grain, breath, attack,
or spatial event migrates across returns.

### Lyric meaning

Keep wording stable while cadence or pronunciation changes its implication, or
preserve a sentence frame while one load-bearing word mutates at closure.

Do not combine all carriers. Complexity reduces the probability that a listener
will learn the rule.

## Hooking Card

Write this before generating:

```text
Frontier stall:
Familiar seed:
Hook mode: vocal or instrumental
Primary hook axis:
Stable invariant:
Language:
Actual hook text:
Heard syllable count:
Target duration seconds:
Onset pattern:
Vowel frame:
Motor contrast:
Pitch inventory size:
Speakable-without-pitch test:
Listener's first prediction:
Withheld or displaced event:
Prediction-debt carrier:
Return operator:
Return 1:
Return 2:
Return 3:
Closure return:
Supporting axis: none or one
Predicted listener action:
One-listen reproduction test:
Two-return prediction test:
Matched-loudness control:
Rejection condition:
```

The predicted listener action must be observable: humming the rhythm, clapping
the gap, anticipating the third ending, singing the missing vowel, or noticing
the same pitch's new function. “Feels hooked” is not observable.

Reject the card when:

- a vocal card lacks literal text or a mouth-first motor description;
- the literal phrase does not recur in the supplied lyrics;
- the stable invariant and withheld event are the same object;
- the operator is only exact repetition, escalation, or decoration;
- no return number is assigned to closure;
- more than one supporting axis is required to explain the hook;
- the mechanism disappears after loudness matching;
- only genre, instrumentation, vocal identity, or production remains memorable.

## Suno field split

Do not ask the style field to invent and enforce the hook simultaneously.

1. Write the literal hook and its two or three returns in the lyrics field.
2. Use punctuation, line breaks, and withheld words rather than fake phonetic
   spelling.
3. Put only audible execution rules in `Style of Music`: duration, pitch count,
   cutoff, silence, articulation, stable vocal body, and sparse arrangement.
4. Omit evaluation prose such as `the listener should feel hooked`.
5. Keep the style prompt under the platform limit and preserve space for one
   concrete timbre sentence.

## Prompt grammar

Put the hook law before mood and instrumentation:

```text
Mouth-first hook: sing "[literal text]" as [heard syllables] in [duration] using
[pitch count] pitches; [onset pattern], [vowel path], [motor contrast]. Preserve
that gesture. Return 1 [withholds event], return 2 [carries debt], and return 3
[closes it]. Support only with [zero or one secondary carrier].
```

Compact example:

```text
Sing "입이 또 너래" as a tight five-syllable, one-second cell on three pitches:
natural liaison into a crisp "또," then widen through "너래." Keep its rhythm.
Cut return 1 after "래," cut return 2 after the added "또," and let return 3
complete the withheld meaning. Leave both cutoffs silent.
```

Avoid front-loading a short generator prompt with `catchy`, `earworm`,
`addictive`, `anthemic`, or `instant hook`. Those labels request a prototype;
they do not define the mechanism.

## Validation

Prompt compliance is not evidence. Use the rendered audio.

### Structural audit

Transcribe each return in a separate row. Mark the invariant, predicted event,
withheld event, carried state, operator result, and closure. Reject random
variation that cannot be explained by the card.

### Listener tests

Use small blind comparisons when practical:

1. **One-listen reproduction:** after one exposure, ask for the rhythm, vowel
   frame, gap, or center note without replay.
2. **Two-return prediction:** stop before the planned closure and ask what comes
   next. Test prediction of the rule, not exact pitch naming.
3. **Matched-loudness control:** compare against an exact-repetition version at
   matched loudness and similar duration.
4. **Carrier ablation:** simplify or mute the supporting carrier. The primary
   relation should remain learnable.
5. **Delayed recall:** after unrelated audio, ask which relation or missing
   event remains, not merely which production palette sounded familiar.
6. **Pitchless motor test:** ask the listener to speak or chant the literal hook
   without the recording. Reject it if the mouth gesture disappears with pitch.

Do not claim general listener hooking from the composer's own recognition.
Pre-register the observable action and rejection threshold before choosing the
preferred render.
