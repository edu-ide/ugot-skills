---
name: native-architecture-sprint
description: Design, implement, and experimentally triage a native language-model architecture within a user-specified short research budget, using paper equations and matched trained controls. Use for architecture breakthroughs or one-day model research, not application scaffolds or pretrained-model selection alone.
principle: sprout-loop
---

# Native architecture sprint

Turn a short deadline into an executable architecture decision, not a claim that a new module is already a frontier model. Preserve the user's actual target capability and method constraints. A roughly one-day budget covers invention, implementation, and bounded evidence collection; it does not guarantee sufficient pretraining or world-leading performance.

## Restore the frontier before inventing

Read the latest relevant conversation handoff, source code, experiment ledger, and actual checkpoint/result metadata. Distinguish proposals, completed measurements, superseded diagnoses, and production state. Find the latest unsolved failure on the user's target metric, not an attractive old proxy. Inspect active compute and storage before scheduling; occupied serving hardware is not spare merely because one utilization sample is low.

Admit a training run only after recording the device allocation and time window, existing process ownership, free VRAM/storage, and measured throughput/memory on the actual configuration. Include compilation, evaluation, and checkpoint costs in the budget. Define abort conditions for nonfinite loss, memory exhaustion, and exceeding the agreed time/resource limit. Do not stop, evict, or degrade unrelated serving jobs without explicit authority.

## Paper-to-mechanism compression

Choose one falsifiable failure hypothesis and one mechanism that changes it. Search primary literature, including the current year and newest revisions/corrections. Read equations and actual implementations where available. Separate:

- established mathematical operation;
- published architecture or optimization principle;
- project-specific integration difference;
- untested causal claim and the exact observation that would refute it.

Use the mechanism itself in the native state-to-logits path. Imported modules in sequence are an assembly, not automatically a unified mechanism. Search outside language modeling when it gives a precise operator or invariant, but do not rename a standard construction as a discovery. For interaction/memory designs, read [the paper-to-decision reference](references/interaction-prior-art.md).

Before code or training, save a repo-local contract: state, causal inputs, output delivery, training credit, compute/storage costs, missing-input/causality invariants, comparison arms, target data and metrics, effect-size floor, and kill/promotion criteria. Keep unknowns explicit. Performance thresholds belong in this experiment contract, not a universal skill constant.

For inherited implementations, do not retroactively call the earlier work preregistered. Mark it exploratory, then freeze a prospective confirmation contract before new observations. Record the contract hash and its registration time with run metadata when practical.

## Spend the budget on decisions

An example allocation for 24 hours is 2 h evidence/literature, 3 h native implementation and integrity tests, 9 h matched pilots, 7 h fresh-seed repeats and task checks, 3 h decision and handoff. Reallocate using measured throughput and variance. This is a budget template, not an ETA assertion. Parallelize independent literature, code, and evaluation reviews with disjoint file ownership. Limit concurrent hypotheses; do not turn failure into an unbounded LR/width sweep.

Use a staged evidence ladder:

1. **Integrity:** future perturbation, document/state isolation, shapes, exact/reference equivalence, initialization identity if intended, finite gradients, actual optimizer updates, serialization. Zero-output projection plus zero residual gate can silently kill a branch. Match shared-body initial tensors, not merely random seed labels.
2. **Real-corpus diagnostic:** exercise the actual logits and loss on disjoint train/validation data. Small CPU models or changed kernels are diagnostic only; disclose width/context/vocabulary/table/optimizer deviations. Check partial parameter updates, not just decreasing loss.
3. **Matched pilot:** keep device, library/kernel versions, precision, compilation, microbatch, optimizer, data order, tokenizer, and token budget fixed. Match extra capacity and active computation with an appropriate control. Equal matrix multiplication count is not equal measured wall time. Include all table/static parameters in total model size.
4. **Replication:** fresh paired seeds and an untouched confirmation panel; report individual deltas and uncertainty. Selecting on repeated validation evaluations does not make that panel a final test set. Compare equal tokens and equal wall time when making efficiency claims.
5. **Mechanism and capability:** ablate only the new path; use a causal, non-invertible sham when alignment is claimed. Whole-sequence memory shuffling can leak the future, while a fixed channel permutation can be learned away. Validate the task capability actually claimed, not retrieval hit rate or an initialization certificate.

Kill or revise a mechanism when its preregistered causal or performance condition fails. If controls have not learned the target behavior or the budget cannot resolve the chosen effect size, label the outcome **inconclusive**, not evidence of architectural impossibility. Preserve the negative result; do not silently change the ruler or omit controls. A surviving small pilot buys a larger comparison, not a frontier title. If compute or evaluation is unavailable, deliver the tested artifact, exact unexecuted gate, and measured resource constraint without silently stopping a user service.

## Handoff

Persist source/config/data identifiers, executable commands, raw per-arm metrics, parameter/update checks, timings, hardware state, checkpoint provenance, and a decision in the repository. Label implementation fidelity: faithful operator, partial architectural prototype, small trained pilot, scaled trained winner, or production-verified model. Clearly distinguish newly written code, actually executed tests, and planned experiments. Do not update personal memories unless separately requested.
