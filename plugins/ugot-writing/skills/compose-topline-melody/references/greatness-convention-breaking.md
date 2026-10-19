

# Greatness laws: surprise dose, form time, and the limits of prompting

Read this when the goal is not merely "unfamiliar" but *good* — a song people
replay. The rest of this skill breaks conventions about hooks, timbre, topline,
and pronunciation. This file covers the axes those files do not touch: how much
surprise, **where** it goes, when the listener leaves, and which parts of the
"generic AI sound" no prompt can fix.

Every law below is stated as: inherited convention → evidence → replacement law
→ how to execute it in a generator → rejection condition. Treat the evidence as
a constraint, not a formula. None of these findings license a claim that a
particular song will succeed.

## 1. Surprise is a schedule, not a level

**Convention.** More surprise is more interesting; pick a novelty level and
apply it evenly.

**Evidence.** Preference for unpredictability follows an inverted U, but the peak
*moves*: the optimal amount of surprise (information content) shifts with the
local uncertainty (entropy) of the music. Smaller surprises are preferred in
low-entropy passages, larger surprises in high-entropy passages; the two
interact rather than acting independently (Mas-Herrero & Marco-Pallarés, PNAS
2025, e2500494122).

**Replacement law.** Schedule surprise against local entropy:

- In a **low-entropy** passage — steady loop, unambiguous meter, diatonic
  harmony — the payoff is a *small* deviation. One wrong note, one displaced
  attack, one extra beat.
- In a **high-entropy** passage — free rhythm, ambiguous tonality, sparse
  accompaniment — the payoff is a *predictable* landing. Resolve plainly.

**Execution.** Write the entropy map before composing: which sections are
certain, which are ambiguous. Then place each deviation in the section whose
entropy calls for that size. State the pairing in the style prompt as a rule
("the free-time verse resolves plainly; the steady chorus takes one displaced
beat").

**Rejection.** Reject a draft whose deviations are the same size everywhere, or
which piles maximum strangeness onto its most ambiguous section.

## 2. Contrast across sections beats surprise inside the chorus

**Convention.** The chorus should be the most surprising, most harmonically
interesting part of the song.

**Evidence.** In a corpus comparison of preferred versus non-preferred songs,
what separated them was the **variation** of harmonic surprise across sections,
not its average — preferred songs showed significantly greater section-to-section
variation (Contrastive-Surprise Hypothesis; Miles, Rosen & Grzywacz, Frontiers in
Human Neuroscience 2021). Press coverage of related work described the pattern as
rare chords in the verse followed by a conventional, catchy chorus; the published
analysis used algorithmically detected sections and did **not** assign surprise to
verse versus chorus, so treat that specific assignment as unconfirmed.

**Replacement law.** Put the harmonic strangeness in a **non-chorus** section and
let the chorus be plainly singable. The payoff is the *drop* in surprise, which
is felt as relief and makes the chorus easier to remember.

**Execution.** Name the surprise contour by section in the style prompt: which
section carries the rare harmony, and that the chorus must return to a
conventional progression. Do not ask for "unusual chords throughout."

**Rejection.** Reject when every section is equally strange, or when the chorus
is the strangest thing in the song and nothing resolves.

## 3. Yesterday's surprise is today's baseline

**Convention.** A device that sounded fresh is a reusable signature.

**Evidence.** Harmonic surprise rose across decades in both preferred and
non-preferred songs, but roughly three times faster in the preferred ones
(+0.096 vs +0.032 bits/year, 1958–1991; Inflationary-Surprise Hypothesis, same
paper). Expectations are built from the previous generation's music.

**Replacement law.** Treat every accepted device as **decaying**. Log the date a
device was first used and retire it once it appears in two consecutive accepted
drafts. This is the historical version of the unfamiliarity gate: your own
catalogue inflates the listener's baseline too.

**Rejection.** Reject a "signature" that has survived three drafts unchanged.

## 4. The melody's global shape should be ordinary

**Convention.** A memorable melody needs an unusual shape.

**Evidence.** Tunes reported as earworms had **more common global melodic
contours** but **less common average gradients between melodic turning points**,
and faster tempi than non-earworm tunes (Jakubowski, Finkel, Stewart & Müllensiefen,
*Psychology of Aesthetics, Creativity, and the Arts*, 2017).

**Replacement law.** Split the melody into two layers and make them disagree:

- **Global contour:** archetypal. Rise-and-fall, arch, descending staircase —
  something the listener can recognize after one pass.
- **Local gradients:** unusual. Make the *interval sizes and directions between
  turning points* atypical — an unexpectedly large step into a turning point, an
  unexpectedly flat approach out of it.

This is the opposite of the usual instinct, which invents a weird overall shape
out of ordinary steps. Combine with a slightly faster tempo than the mood
suggests.

**Execution.** Specify both layers separately in the Topline Card: the contour
archetype, then the gradient anomaly and where it occurs.

**Rejection.** Reject a topline whose novelty is its silhouette. Reject one whose
gradients are all steps and repeats.

## 5. Every section boundary is an exit, not just the intro

**Convention.** Shorten the intro, get to the chorus fast, and make transitions
clearly signposted.

**Evidence.** Average instrumental intros in top-10 singles fell from 20–25 s in
the mid-1980s to about 5 s by 2015 (Léveillé Gauvin, 2018). But abandonment is
not concentrated at the start: a quarter of streamed songs are skipped within the
first five seconds, only about half are heard in full, and skips **surge roughly
3.5 seconds after a section boundary** — boundaries are predictable enough from
skip profiles that a model can locate them from skips alone (Montecchio, Roy &
Pachet, PLOS ONE 2020).

**Replacement law.** Stop treating a boundary as a place to announce a change.
Treat it as the moment you must have already given a reason to stay:

- **Elide the boundary:** start the new section's identity element — its rhythmic
  cell, vowel frame, or bass figure — one or two beats *before* the old section
  ends, so no clean seam exists to leave at.
- **Carry a debt across every boundary:** an unfinished syntactic state, an
  unresolved interval, or a withheld word. The listener stays for the payment.
- **Put the new information immediately after the boundary,** not four bars
  later, because the 3.5-second window is where the decision happens.

**Execution.** In the lyrics field this is breath inheritance across the section
label, which the lyric skill's auditor labels `inherited`. In the style prompt,
forbid the transition markers that announce a seam — riser, cymbal crash,
drop-out bar, silence before the chorus — and name the element that crosses the
seam instead.

**Rejection.** Reject a take whose section changes are marked by a fill, a riser,
or a bar of silence, and whose first post-boundary bar contains nothing new.

## 6. Groove needs a medium dose, placed where the listener must fill in

**Convention.** More syncopation is groovier; straight is safe.

**Evidence.** Pleasure and the urge to move follow an inverted U over
syncopation: high syncopation blocks beat prediction, low syncopation offers
nothing to violate, and medium syncopation gives the optimal mix of realised and
violated predictions, inviting the listener to enact the missing beats (Witek,
Clarke, Wallentin, Kringelbach & Vuust, PLOS ONE 2014; extended in later
active-inference work on motor engagement and rhythmic prediction error).

**Replacement law.** Choose one **medium** syncopation dose for the song, then
spend it unevenly: put the syncopation exactly where you removed a layer, so the
listener's body fills the hole you made. Density and syncopation move in opposite
directions.

**Execution.** State the dose and its location as a rule, not as a genre tag:
which beats are displaced, which layer is absent while they are.

**Rejection.** Reject a take that is either metronomically straight or so
displaced that the pulse is unfindable — both kill the fill-in reflex.

## 7. Voice is judged perceptually; acoustic optimization does not transfer

**Convention.** A distinctive voice can be specified with spectral numbers, and
there is a best voice for the song.

**Evidence.** Listener ratings of **perceptual** vocal attributes — articulation,
breathiness, pitch accuracy, loudness, tempo — predicted about 43% of liking for
pop voices, while computationally extracted acoustic and MIR features explained
almost none (Merrill et al., *Scientific Reports* 2024). Voice appreciation is
also highly idiosyncratic, with robust average preferences emerging only weakly
across large individual differences (*Royal Society Open Science* 2024).

**Replacement law.** Specify the voice in **articulatory and perceptual** terms
that a singer could act on — how consonants are released, where breath enters,
whether pitch is centred or slightly under, how effort changes across the phrase
— and never as a spectral target. Then accept idiosyncrasy: choose one listener
you are writing for instead of averaging.

**Note.** This does not retire the timbre measurements in this skill. Those exist
to *verify* that a described change actually happened between sections. They are
instruments, not objectives.

**Rejection.** Reject a Timbre Card whose vocal fields are numbers or adjectives
with no articulatory behavior attached.

## 8. Part of the "AI sound" is architectural, not promptable

**Convention.** If the output sounds generic or synthetic, the prompt was not
good enough.

**Evidence.** Neural audio generators leave systematic spectral artifacts —
regularly spaced peaks traceable to deconvolution layers, plus high-frequency
shimmer and sample-rate signatures — that are architecture-dependent and appear
regardless of the prompt or training weights. A 10,000-parameter classifier
detects them with over 99% accuracy on raw output; accuracy falls to roughly
85–93% after re-encoding or DAW processing (ISMIR/TISMIR 2025 work on detecting
AI-generated music).

**Replacement law.** Separate the two causes of "this sounds generic":

- **Compositional genericness** — four-bar loops, late lift, even phrase
  lengths, chorus-by-volume. This *is* prompt-and-law addressable, and it is what
  the rest of this skill attacks.
- **Signal-level sheen** — the metallic top end and micro-artifacts. No adjective
  removes these. If they bother you, they are a mixing problem: render, then
  treat the top octave, re-amp or re-record the load-bearing layer, or replace
  the lead vocal with a human take.

Stop spending prompt budget on the second problem, and stop concluding that a
composition law failed when what you are hearing is codec sheen.

**Disclosure.** State that a track is AI-generated when you release or submit it.
Nothing in this file is a method for hiding that; post-processing is for sound
quality, and detectability is not a design goal in either direction.

## 9. Honest ceiling on audio-only optimization

Hit-song-science surveys and multimodal models consistently find that intrinsic
audio features alone are weak predictors: performance improves substantially only
when lyrics, artist prior popularity, publisher support, and social-network
effects are added. Some acoustic descriptors help, but the audio contribution is
modest.

**Operational rule.** Optimize the song for the listener you named, not for a
predicted chart position, and never claim that a measured audio property implies
success. When the song is good and unheard, the missing variable is usually not
the mix.

## Surprise Schedule Card

Fill this before generating, and deliver it with the take:

```text
Entropy map by section: certain / ambiguous
Deviation size per section, matched to that entropy:
Section carrying the harmonic strangeness:
Section that must stay conventional:
Surprise contrast direction across the form:
Global contour archetype:
Gradient anomaly and its location between turning points:
Tempo relative to the mood's expectation:
Syncopation dose and the layer removed underneath it:
Boundary elision element and how many beats early it enters:
Debt carried across each section boundary:
New information inside the first 3.5 seconds after each boundary:
Device retirement log (device, first used, drafts survived):
Vocal specification in articulatory terms:
Named target listener:
Rejection condition:
```

## Sources

- Mas-Herrero & Marco-Pallarés, "Predictive processes shape individual musical
  preferences," PNAS 2025: https://www.pnas.org/doi/10.1073/pnas.2500494122
- Miles, Rosen & Grzywacz, "What to Expect When the Unexpected Becomes Expected:
  Harmonic Surprise and Preference Over Time in Popular Music," Frontiers in
  Human Neuroscience 2021:
  https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.578644/full
- Jakubowski, Finkel, Stewart & Müllensiefen, "Dissecting an Earworm: Melodic
  Features and Song Popularity Predict Involuntary Musical Imagery," 2017:
  https://research.gold.ac.uk/id/eprint/19405/
- Montecchio, Roy & Pachet, "The skipping behavior of users of music streaming
  services and its relation to musical structure," PLOS ONE 2020:
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0239418
- Witek, Clarke, Wallentin, Kringelbach & Vuust, "Syncopation, Body-Movement and
  Pleasure in Groove Music," PLOS ONE 2014:
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0094446
- "Active Inference in Music Perception: Motor Engagement to Syncopation
  Modulates Rhythmic Prediction Error":
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12287993/
- Merrill et al., "Perceptual (but not acoustic) features predict singing voice
  preferences," Scientific Reports 2024:
  https://www.nature.com/articles/s41598-024-58924-9
- "Appreciation of singing and speaking voices is highly idiosyncratic," Royal
  Society Open Science 2024:
  https://royalsocietypublishing.org/rsos/article/11/11/241623/92393/
- "The AI Music Arms Race: On the Detection of AI-Generated Music," TISMIR 2025:
  https://transactions.ismir.net/articles/10.5334/tismir.254
- "Hit song science: a comprehensive survey and research directions," 2023:
  https://www.researchgate.net/publication/375787044
