# Convention-Breaking Instrumental Grammar and Timbre

Use this reference when instrumental roles or harmony remain conventional, a
generated voice or instrument sounds generic, or a short Suno or ACE-Step
prompt must carry a distinctive sonic identity.

## Contents

- Break the right timbre convention
- Treat timbre as an event
- Build memory harmony
- Complete the Instrumental Grammar Card
- Write compact generator prompts
- Validate the render

## Break the right convention

Reject the convention that timbre is adequately described by performer type
plus mood and mix position:

```text
female mezzo + warm + emotional + dry + centered
```

That describes voice class, affect, and placement. It leaves the generator free
to choose its most common vocal texture. A usable timbre instruction defines:

1. **Spectral body:** where the voice has weight, such as a firm fundamental,
   rich low mids, hollow mids, or restrained upper harmonics.
2. **Air and harmonicity:** clean periodic tone, breath leakage, noisy air, or
   a controlled balance between them.
3. **Texture location:** when grain, rasp, fry, bow noise, or pick noise appears.
4. **Attack and diction:** soft vowel onset, hard glottal onset, crisp
   consonants, smeared consonants, rounded vowels, or narrow vowels.
5. **Vibrato behavior:** absent, delayed, narrow, wide, slow, or appearing only
   on selected sustained notes.
6. **Formant or vowel posture:** dark rounded vowels, forward narrow vowels, or
   a change between them.
7. **Space:** direct-to-reverb balance, early reflections, width, and distance.

Do not maximize all seven axes. Keep a stable base and invert one inherited
law. Distinctiveness should come from an audible relationship, not adjective
count.

## The key inversion: timbre is an event

The common generator prior treats a voice as one static preset. Break it by
placing one texture change in time:

- firm clean tone through the phrase, slight grain only on the final vowel;
- dark vowel body with crisp consonant attacks;
- almost no vibrato at onset, narrow delayed vibrato after the note settles;
- breathier tone only after the melodic peak, not throughout the song;
- close dry lead during words, short room tail only after completed breaths.

Use one internal contradiction that can coexist acoustically. `Dark vowels +
crisp consonants` works because vowel body and consonant attack occupy different
moments. `Very airy + firm fundamental + maximal rasp everywhere` does not
create a clear governing identity.

## Instrumental grammar: memory harmony

Reject changing only instrument names while preserving these pop defaults:

- a complete vertical chord exists beneath every melodic phrase;
- drums own time, bass owns roots, and keys or guitar own harmony;
- each track forms a continuous, independently sensible part;
- a repeating arpeggio counts as a new harmonic grammar.

Use one replacement law: let successive lyric, phoneme, or phrase events reveal
non-overlapping chord-tone fragments so harmony becomes complete in listener
memory before it becomes complete in the signal.

For phoneme-clocked music, apply this map:

```text
realized onset -> one dry instrumental attack
sung vowel -> one isolated chord tone from one carrier
coda, cutoff, or missing vowel -> remove that tone and leave a gap
planned final closure -> permit one simultaneous complete chord
```

End every instrumental tone before the next vowel begins. Rotate carriers such
as piano, bass, guitar harmonic, bowed tone, or wooden percussion by a simple
repeatable rule; do not let their conventional roles return. Treat carrier
rotation as a consequence of the memory-harmony law, not a second novelty axis.

Distinguish memory harmony from an arpeggio:

- Do not repeat a backing cycle independently of the lyric or phoneme sequence.
- Do not let notes overlap under a sustained pad or hidden chord bed.
- Remove the mapped chord tone when its triggering vowel is absent; do not let
  another instrument substitute for it.
- Let the sequence reveal harmonic function over the phrase rather than
  spelling the same chord rapidly and repeatedly.
- Keep one familiar shell, such as meter, bass register, or a mouth-rhythm hook,
  so the listener can infer the absent whole.

Do not claim this technique has no precedent. Sequential harmony, hocketing, and
pointillistic orchestration exist. The testable grammar is their causal binding
to the lyric or phoneme event map and the moving absence.

## Instrumental Grammar Card

```text
Inherited instrumental default:
Familiar orientation shell:
Rejected vertical-harmony law:
Single replacement law:
Event-to-chord-tone sequence:
Tone non-overlap rule:
Carrier rotation operator:
Missing-event consequence:
Independent-loop prevention:
Final closure exception:
Vocal-muted backing prediction:
Predicted listener effect:
Three-song transfer variables:
Generator normalization failure:
Rejection condition:
Compact prompt sentence:
```

Reject a card whose only change is rare instruments, wider stereo, a quieter
drum pattern, or ordinary arpeggiation. Require the same event-to-harmony law to
survive three songs while changing tempo, key, carrier instruments, and lyrical
scene. Until then, call it a proto-genre grammar rather than a genre.

## Timbre Card

Write this before the compact generator sentence:

```text
Inherited default:
Voice base:
Spectral body:
Air and harmonicity:
Grain behavior:
Attack and diction:
Vibrato behavior:
Vowel or formant posture:
Space:
Primary inverted timbre law:
Positive replacement:
Time-varying event:
Stable identity:
Predicted listener effect:
Rejection condition:
Compact prompt sentence:
```

The voice base may contain gender presentation, voice class, register, or chest
versus head dominance. It does not count as the convention break. The primary
inversion must concern an acoustic or articulatory relationship.

Every prohibition needs an affirmative replacement:

```text
Weak: not whispery, not nasal, not childlike
Strong: firm fundamental, little air, dark rounded vowels, crisp adult diction
```

Negative guards are boundaries, not the design. Use no more than two in a short
style prompt unless the generator repeatedly violates a specific constraint.

## Compact prompt grammar

Use this order so the most audible information survives truncation:

```text
[voice base]; [spectral body + air]; [time-localized texture];
[attack/vowels]; [vibrato]; [space].
```

Example:

```text
Close, centered female mezzo with rich low mids, firm fundamental, dark vowels,
little air, slight grain only at phrase ends, crisp consonants, and minimal
delayed vibrato.
```

This deliberately opposes the generic “healing female voice equals airy
whisper” prior. The stable identity is a grounded low-mid body; the audible
exception is clean firmness inside each phrase turning slightly grainy only at
its ending. It makes no medical or frequency-healing claim.

For a 1,000-character Suno style budget, keep the timbre sentence near 140–190
characters. Do not repeat the same property in positive and negative wording.

For a compact memory-harmony instruction:

```text
[Lyric or phoneme events] are the only clock and chord builder: each event
reveals one isolated chord tone, every tone ends before the next event, and a
missing event removes its tone. Let harmony exist only in memory until one
planned final chord; rotate carriers by [operator] without an independent loop.
```

Put this replacement law in the first two style-prompt sentences. State the
stable hook and final closure next, then reserve one compact sentence for vocal
or instrumental timbre. Treat the prompt as a request, not evidence that the
render obeyed the law.

## Reject these drafts

Reject a Timbre Card or generated output when:

- the description stops at voice type, register, mood, or mix placement;
- the only detail is a list of exclusions;
- all textures are continuously active, so no temporal identity is audible;
- the contradiction is physically or perceptually incoherent;
- the special texture obscures Korean consonants or the lyric's key word;
- the generated voice imitates an identifiable singer;
- the prompt claims success but the rendered vocal does not exhibit the event.

## Verify the render

Listen at matched loudness and inspect the vocal stem. Compare phrase bodies
against phrase endings or note onsets against sustains rather than averaging the
whole chorus. Use spectral slope, alpha ratio, Hammarberg index, band ratios,
HNR, attack behavior, and formants as supporting evidence. Treat pitch-sensitive
centroid, jitter, shimmer, and separated-stem artifacts cautiously.

The card passes only when the stable identity and the time-localized exception
are audible in at least two returns. Prompt text alone is never proof.

For memory harmony, inspect the instrumental or separated stems and reject when:

- a complete triad or chord bed overlaps before the planned final closure;
- the same instrumental sequence repeats twice without lyric-event dependence;
- a missing trigger is silently replaced by another carrier;
- any single carrier forms a conventional continuous bass, drum, or chord part;
- the final simultaneous chord is absent or appears before the planned closure.

Accept only when at least two phrase returns preserve the event-to-tone map,
the missing event produces an audible harmonic hole, and the vocal-muted
backing remains intentionally incomplete.
