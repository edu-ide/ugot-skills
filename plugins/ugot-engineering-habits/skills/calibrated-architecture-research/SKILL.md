---
name: calibrated-architecture-research
description: Improve the predictability of language-model architecture research by calibrating cheap experiments against completed runs, checking control learnability, and choosing bounded discriminating experiments from primary papers. Use for one-day architecture research, repeated inconclusive pilots, early-performance prediction, scaling forecasts, or requests to raise research success probability. Does not promise a frontier model or replace implementation and real capability evaluation.
---

# Calibrated architecture research

Make the next research decision more predictable; do not equate predictable
cost or test completion with predictable discovery. Preserve the user's target
model, parameter limit, comparison model, capability and compute constraints.
Use this workflow to produce a tested mechanism and a decisive next measurement,
not just a bibliography or a longer checklist.

## 1. Freeze what is being predicted

Read the current experiment ledger, actual source/checkpoint lineage and raw
outputs. Use historical notes to locate evidence, not as current measurements.
Separate four claims:

| Claim | Necessary evidence |
| --- | --- |
| Run duration and cost | Same-configuration throughput, setup/evaluation/save overhead, resource allocation |
| Task learnability | An executed positive control acquiring the target behavior |
| Architecture effect at this dose | Matched controls, actual generated outputs, uncertainty and retention |
| Larger-scale or frontier superiority | Out-of-sample forecast validation, then the actual target comparison |

Fill [the prediction contract](templates/prediction-contract.md) in the project
before new observations. Specify metric units, direction, minimum useful effect,
exact fidelity, resource cap, data split, stopping looks and outcomes that change
the next action. “10x” must name a denominator: equal-quality latency, error rate,
training compute or something else. Ratios against zero accuracy are undefined.
Use an absolute improvement until a meaningful denominator exists.

Report success probability as **unestimated** unless a relevant reference class,
outcome definition, calibration sample and out-of-sample error support it. Do
not invent a percentage from paper count, enthusiasm or a successful unit test.

## 2. Turn papers into constraints

For a new problem, read [the primary-source map](references/papers.md). Search
current-year work and recent revisions first; retain older foundational work
when it supplies the exact operator. Read the pertinent equation, experiment
and limitation, not only an abstract. Close the search when a concrete candidate,
its nearest prior art and an informative falsifier are available.

For each used paper write: supported claim → required assumptions → project
deviation → falsifying observation. Label an established operator, a published
architecture, a local integration and an untested hypothesis separately. A
workflow inspired by Bayesian design is not an implementation of Step-DAD.

Transfer rules:

- μP/μTransfer: optimization hyperparameter transfer is not architecture-rank or
  capability transfer. Verify the parameterization, coordinate scaling and
  optimizer assumptions. Width evidence does not certify new recurrent depth.
- Scaling laws: fit only declared variables/ranges with enough independent
  observations; reserve unseen configurations. Missing shape, data or recurrent
  compute variables can invalidate a seemingly accurate loss forecast.
- Early/zero-cost proxies: use for defect vetoes until target-rank preservation
  has been backtested. Do not eliminate every slow-starting family from an
  unvalidated early ranking.

## 3. Check the measuring instrument before ranking candidates

Before a capability comparison, check label/token alignment, full-response and
EOS supervision, prompt-only generation, raw decoding, provenance, future-token
and cross-document isolation, finite gradients and actual parameter updates.
Count all parameters, including tables and disconnected tensors. Declare known
disconnections; repairing them makes a new substrate and requires new controls.

If both arms are at the metric floor, or the positive control has not acquired
the checked behavior, mark **CONTROL_UNLEARNED / RANKING_UNRESOLVED**. This is not
a measured zero true effect or impossibility theorem. A degenerate all-tie
bootstrap interval is not certainty. A small training-set memorization check
tests acquisition only, not generalization or broad model quality.

Choose the smallest target-faithful acquisition diagnostic with a fixed dose
and cap. Do not silently extend it after failure. Inspect whole generated
answers: lower teacher-forced loss, better termination or token overlap alone
does not establish correct answers. If existing evidence already isolates an
implementation defect in the checked behavior, fix and verify that defect
before another training run. A reported unused parameter or suspicious path is
not by itself the cause of task failure; do not repair the substrate implicitly.
Such changes need a separate contract and fresh matched controls.

## 4. Calibrate the cheap measurement itself

When completed comparable runs exist, freeze proxy definition, fidelity,
directions and acceptance thresholds on calibration families, then evaluate
on independent confirmation families. Group correlated variants/seeds and
checkpoint lineage together. Do not split sibling checkpoints into “unseen”
models or pool unrelated tasks without a declared common target.

Use `scripts/calibrate_proxy.py` for a dependency-free diagnostic on a CSV with
`id,family,split,proxy,target`, where split is `calibration` or `confirmation`.
Run `python scripts/calibrate_proxy.py --help` for options. It computes heldout
rank agreement, strict pair reversals, ties and top-k retention, not a fitted
predictor or confidence certificate. Input measurements require external raw
evidence; the script cannot authenticate a CSV or infer actual independence.

Also inspect individual reversals, near-ties, top-candidate misses and the
small-to-large generalization gap. Confidence intervals, if used, must respect
the actual independent unit. Pre-register a calibration criterion and minimum
effective sample for the application; no universal correlation threshold is a
frontier guarantee. Missing or floor-limited histories mean **UNCALIBRATED**:
use proxies to debug, not to assign success odds. Reserve part of the declared
budget for an unpruned or higher-fidelity check when early ranking is uncertain.

## 5. Select a discriminating experiment and execute the authorized part

List a few competing explanations and write an outcome-to-action table before
running. Prefer a bounded experiment whose possible outcomes distinguish the
important explanations over one that merely improves a proxy. Include the
possibility that all outcomes remain inconclusive; redesign such a test if
feasible. Select on decision relevance and measured cost, not invented EIG.

Formal expected information gain requires a justified prior, likelihood,
posterior computation and model-misspecification checks. Without these, use an
explicit qualitative decision table. Include inference, model-fitting and
design overhead in cost; amortized selection is not free policy training.

If the next decision is acquisition or measurement integrity, keep the substrate
fixed; do not add a new mechanism to that diagnostic. When an architecture
candidate is explicitly requested or the next decision tests its effect,
implement one mechanism in the actual native state-to-logits path. A parallel
candidate prototype must not replace or confound the acquisition control. Freeze its
equations, causality, credit assignment, exact controls and algebraic invariants
before implementation. Test these on CPU where possible; label reduced width
or substituted kernels. Mathematical contraction or a smaller solver residual
does not imply more correct answers. Inspect gradient reachability; an identity
initialization can leave a zero-gated branch permanently dead.

Admit GPU work only after checking actual ownership, free resources, measured
configuration cost and abort conditions. Do not evict unrelated services. Match
initial tensors, data order, capacity and the compute relevant to the claim;
equal decoder calls, FLOPs and wall time are different matches. Same-LR A/B tests
one recipe, not each architecture's attainable optimum. If bounded recipe
calibration is needed, do it on development data and freeze a fresh comparison.

Use prospective stopping looks or a valid sequential method, then fresh seeds
and an untouched confirmation panel. Repeatedly inspected panels are development
data. Preserve negative results and the original ruler. If the budget ends,
state “not resolved within this budget,” not “cannot work.” Update the next
experiment from the evidence without restarting an unlimited search.

## 6. Handoff evidence, not a frontier label

Save the contract, source URLs/version dates, source/config/data hashes, raw
outputs, commands, actual runtime and decision in the project. Distinguish:
**specified → implemented → integrity-tested → learned → independently better →
target-scale verified**. A skill validation or synthetic fixture verifies only
the tool/workflow behavior. It does not measure better research success rates.
Report the next deciding gate and its resource cap separately from any ETA.
Do not update personal memories unless explicitly requested.
