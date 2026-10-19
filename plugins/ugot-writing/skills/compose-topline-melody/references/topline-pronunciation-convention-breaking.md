

# Convention-Breaking Topline and Pronunciation

Use this reference when a chorus remains familiar after changing contour, meter,
range, harmony, instrumentation, or mood. It also applies when pronunciation
should carry part of the hook.

## Diagnose the remaining convention

Techniques such as a falling payoff, opening high point, narrow range, odd phrase
length, or one large leap can be useful. They are not by themselves a new
compositional law. They still assume:

- a melody is a fixed sequence of pitch-duration objects;
- repetition means replaying that sequence with light decoration;
- each phrase resets instead of inheriting state from the previous phrase;
- harmony accompanies a melody whose identity is already complete;
- a syllable is one indivisible note event;
- pronunciation should be uniformly natural, clear, and metrically aligned.

Break one of these representations. Do not merely select more rare intervals.

## Topline as a transformation law

A distinctive hook needs three parts:

1. **Invariant:** the feature a listener can remember after one return.
2. **Operator:** the deterministic change applied on each return.
3. **Closure:** the point at which the transformations resolve or cycle home.

The output is not `A, A, A'`. It is `A, T(A), T²(A)` where the listener can
infer `T`. Keep the operator simpler than the resulting surface.

### Useful replacement laws

Choose one, then adapt it to the lyric rather than stacking several.

**Cadence inheritance**

The unresolved final scale degree of phrase one becomes the center note of
phrase two. Every phrase therefore carries state forward instead of resetting.
The final return closes the accumulated displacement.

**Harmonic-role migration**

Keep one hook pitch or narrow cell stable while the chords change its perceived
role, for example stable tone to suspension to chord tone to leading pressure.
The hook's drama comes from changing meaning, not a higher note.

**Transformational return**

Keep rhythm and vowel frame invariant. On each return, move exactly one boundary
note in the direction implied by the previous cadence. After three returns, the
changed notes form a second hidden contour or return to the starting cell.

**Silence substitution**

Each return removes one expected pitched nucleus but preserves its consonant
attack or breath cutoff. The absent pitch advances through the phrase according
to a fixed rule, then returns in the final chorus.

**Prosodic phase rotation**

Keep pitches nearly fixed while the consonant arrives before, on, then after the
pulse across three returns. The vowel remains the pitch anchor. The listener
recognizes a rotating pronunciation phase rather than a new melody each time.

**Function-preserving mutation**

Let pitches and words change, but preserve a perceptual function vector such as
`held tension / clipped answer / open-vowel release`. This is harder to prompt
and must be verified by listening; surface difference alone is not evidence.

## Topline Invention Card

Write this before choosing notes:

```text
Inherited representation:
Rejected law:
Replacement law:
State carried between phrases:
Stable invariant:
Return operator:
Return 1:
Return 2:
Return 3:
Cycle closure:
Harmony interaction:
Pronunciation interaction:
Predicted listener effect:
Measurable or notatable signature:
Rejection condition:
```

Reject the card when the return operator is merely “sing higher,” “add energy,”
“change it slightly,” or “make it emotional.” An operator must identify what
moves, by what rule, while what remains invariant.

The law must survive transposition and at least two of these changes: key,
tempo, chord palette, instrumentation, lyrical scene, or singer. Otherwise it
is an arrangement trick, not a compositional grammar.

## Escape cross-song topline convergence

Treat “the new melody is the previous contour with different notes” as the
convention to reject. Key, BPM, mode, range, instruments, and a slightly moved
peak do not create a new topline representation.

### Rotate the identity carrier

Before composing a new song, inspect the two most recent accepted toplines.
Choose exactly one identity carrier and forbid reuse of either recent carrier:

- **Interval-state carrier:** let the previous phrase's final interval determine
  the next phrase's opening direction; do not reset to a tonal home gesture.
- **Onset-and-rest carrier:** limit pitch to one to three scale degrees and put
  identity in consonant timing, durations, and rests.
- **Harmonic-role carrier:** keep pitches nearly fixed while their chord roles
  migrate through stable tone, suspension, tension, and release.
- **Vowel-and-absence carrier:** keep a vowel frame while a pitched nucleus or
  silence moves by a deterministic return operator.
- **Register-relay carrier:** alternate phrase fragments between two register
  shelves; neither shelf alone contains the complete contour.
- **Cadence-inheritance carrier:** make each unresolved ending become the center
  of the next phrase and allow closure only at the planned final return.

Keep the non-carrier axes deliberately simple. Do not combine multiple carriers
to manufacture difference. The convention break is that pitch contour is only
one possible identity layer, not that every layer becomes unusual.

Write an explicit relative skeleton before mood or genre adjectives:

```text
phrase | heard syllables | relative degrees | duration ratios | rest slots |
peak position | ending direction | state passed forward
```

Use scale degrees relative to the current key so transposition cannot disguise
reuse. Record interval direction, phrase-length vector, peak zone, ending
direction, rest path, and identity carrier. Reject the draft when at least four
of these six fields match either of the two recent accepted toplines.

### Portfolio Separation Card

```text
Recent carrier 1:
Recent carrier 2:
Current forbidden contour family:
New identity carrier:
Stable listener handle:
Relative-degree skeleton:
Duration-ratio skeleton:
Rest or absence path:
Phrase state transition:
Peak zone and ending direction:
Fields changed from each recent song:
Generator normalization failure:
Rejection condition:
```

If three renders still collapse to the same arch, repeated-note hook, or late
lift, stop changing descriptive adjectives. Change the identity carrier and the
lyric's heard-syllable or breath structure. For Suno, treat exact degrees as
directional guidance; if control remains weak, use a sung, MIDI, or audio
conditioning path rather than claiming the style prompt solved it.

## Pronunciation as composition

Reject the convention that a syllable is a single attack attached to one note.
For musical planning, split it into:

```text
onset consonant | vowel nucleus | final consonant or release
초성 | 중성 | 종성 또는 끊김
```

Assign different jobs:

- **Onset consonant:** pickup, syncopation, percussive identity, or delayed drag.
- **Vowel nucleus:** perceived pitch, sustain, formant color, and melodic beat.
- **Coda or release:** cutoff rhythm, residue, liaison, or preparation for rest.

This does not authorize arbitrary mispronunciation. Preserve the phonemic
identity of every load-bearing word. Follow natural Korean liaison,
palatalization, nasalization, and tensification unless a requested character or
dialect justifies otherwise.

### Pronunciation replacement laws

Choose one primary law:

- **Consonant leads, vowel lands:** place the onset slightly before the beat
  while the vowel owns the beat and pitch.
- **Delayed semantic arrival:** let a function word or harmless onset arrive on
  time but delay the load-bearing vowel, so meaning lands after expectation.
- **Vowel trajectory:** begin a sustained vowel dark and compact, then open it
  only after pitch stabilizes; do not change the recognized word.
- **Articulation mutation:** repeat the same words and notes, but progress from
  clipped to connected to open articulation according to the narrative.
- **Coda-to-silence handoff:** make the final consonant or cutoff define the
  following rest; accompaniment must not fill that rest.
- **Selective clarity:** keep semantic anchors fully intelligible while a
  secondary connective syllable supplies texture or rhythmic blur.

Uniform slurring, fake accents, random consonant deletion, and spelling tricks
are not convention-breaking laws. They are loss of control.

## Phoneme-triggered arrangement

Use **phoneme-clocked pop** or **입박자 팝** as a provisional proto-genre label,
not proof that a genre exists. Reject the conventional law that accompaniment
keeps a complete clock and the singer fits inside it. Replace it with one causal
law: realized vocal phoneme events gate the backing.

```text
onset consonant -> trigger one short instrumental attack
vowel nucleus -> open and sustain harmony for the vowel's duration
coda, cutoff, or breath -> mute the backing and determine the following gap
```

Derive all arrangement decisions from this map:

- Do not let drums, bass, strumming, or an arpeggiator maintain an independent
  continuous pattern through the vocal phrase.
- Attach salient accompaniment attacks to vocal onsets. Rotate which layer
  answers each onset instead of stacking every instrument on every syllable.
- Let vowel length control sustain rather than placing a fixed pad underneath.
- Leave planned codas, cutoffs, and breath gaps unfilled.
- Permit a familiar pulse or meter as an orientation shell, but do not let the
  backing articulate a self-sufficient loop.
- Trigger from the realized Korean sound after liaison, nasalization,
  palatalization, or tensification, not mechanically from each written block.

This is not ordinary side-chain ducking. The instrumental event must be absent
or differently timed when its phoneme trigger is absent. Muting the vocal should
therefore leave an intentionally incomplete backing, not a normal pop track with
an empty vocal lane.

Complete this card:

```text
Proto-genre label:
Familiar orientation shell:
Rejected clock:
Onset-to-attack map:
Vowel-to-sustain map:
Coda/cutoff-to-gap map:
Layers allowed to rotate:
Stable mouth-rhythm handle:
Natural Korean sound changes:
Vocal-muted backing prediction:
Three-song transfer variables:
Generator normalization failure:
Rejection condition:
```

Pass the transfer test only when the same trigger map remains audible in three
songs while at least tempo, key, instrumentation, and lyrical scene change
across the set. Reject three arrangements that merely reuse the same hook,
palette, or stop-start effect.

## Pronunciation Card

```text
Lyric fragment:
Load-bearing word:
Natural spoken baseline:
Intelligibility anchor:
Phoneme split:
Displaced element:
Timing rule:
Vowel trajectory:
Consonant role:
Coda or release role:
Return transformation:
Semantic effect:
Rejection condition:
```

The pronunciation law must recur at least twice. If it appears once, listeners
will hear an accident or performance mannerism rather than a hook.

Reject the render if:

- the load-bearing word becomes another word or cannot be understood;
- the singer applies the same smear or accent to every syllable;
- consonant timing obscures the pulse instead of creating a repeatable relation;
- the vowel trajectory changes pitch accuracy or sounds like a model artifact;
- pronunciation decoration does not follow the declared return operator;
- an identifiable singer's accent or signature diction is being cloned.

## Compact generator grammar

For a short style prompt:

```text
Topline law: preserve [invariant]; on each return [operator]; close after
[count]. Pronunciation law: [onset/coda timing], while [vowel behavior] carries
pitch; keep [load-bearing word] fully intelligible.
```

Example:

```text
Preserve one five-syllable rhythm and vowel frame; each return moves one ending
note toward the prior cadence, closing on return three. Let onset consonants
lead the beat while vowels land on pitch; keep the hook word fully intelligible.
```

For phoneme-clocked accompaniment:

```text
The singer's phonemes, not an independent backing loop, control the arrangement:
each onset triggers one short attack, each vowel sustains harmony only for its
duration, and each coda or cutoff mutes the instruments and sets the next gap.
Keep [mouth-rhythm hook] invariant; imply [pulse/meter] only as orientation.
```

Treat this as a generation request, not evidence. Suno and ACE-Step may
normalize phoneme timing or the transformation rule. Verify the rendered vocal
and reject noncompliant candidates.

## Validation

Transcribe three returns into separate rows. Mark pitch, duration, onset
consonant, vowel landing, coda release, chord role, and silence. The result
passes only when:

- one invariant is audible across all returns;
- the declared operator, not random variation, explains each change;
- closure occurs at the planned return;
- pronunciation behavior reinforces the same law;
- the hook remains singable and the lyric remains intelligible.

For phoneme-triggered arrangements, also annotate salient instrumental attacks,
sustain endings, and breath gaps. Pass only when most salient attacks have a
declared phoneme trigger, planned gaps stay empty, and a vocal-muted audition
does not reveal two consecutive repetitions of a self-sufficient backing loop.
