

# Primary-source map

Checked 2026-09-06. This is a compact starting map, not a claim of exhaustive
coverage or of implementing these algorithms. Refresh versions for a new
research decision. Adapted workflow rules below are our methodological choices.

## Predicting from cheap experiments

1. **Tensor Programs V: Tuning Large Neural Networks via Zero-Shot
   Hyperparameter Transfer**, Yang et al., [arXiv 2203.03466v2,
   2022-03-28](https://arxiv.org/abs/2203.03466v2), Table 1 / Appendix A;
   [official implementation](https://github.com/microsoft/mup).
   Supports transferring optimization settings under suitable parameterization.
   It does not prove that a small model outperforms the large model, nor that
   arbitrary architecture rankings transfer. Small-data fine-tuning and
   regularization require separate care. **Rule:** check parameterization and
   coordinate behavior; separate HP transfer from task and architecture claims.

2. **Can Small Training Runs Reliably Guide Data Curation? Rethinking
   Proxy-Model Practice**, [arXiv 2512.24503v2, 2026-04-12,
   ICLR 2026](https://arxiv.org/html/2512.24503v2), Theorem 1 / Appendix D.2.5.
   Reports strong data-recipe rank agreement for early checkpoints under small
   learning rates; warmup measurements are less reliable. Its theory concerns
   random-feature data ranking, not arbitrary new recurrent architectures.
   **Rule:** backtest the exact target, fidelity and training phase. Do not copy
   a tiny learning rate as a universal prescription for a short SFT experiment.

3. **μpscaling Small Models: Principled Warm Starts and Hyperparameter
   Transfer**, Ma et al., [arXiv 2602.10545v1,
   2026-02-11](https://arxiv.org/html/2602.10545v1), Propositions 2.1–2.4,
   Algorithm 1 / Appendix G.
   Derives function/training-trajectory equivalence for coordinated width
   expansion and optimizer rescaling, then uses symmetry breaking for useful
   upscaling. Generalization and joint depth expansion are outside its proven
   scope; Appendix G explicitly does not guarantee universal HP transfer.
   **Rule:** function preservation, trainability and generalization are separate
   gates. Simulate the same upscaling procedure when testing HP transfer.

4. **Scaling Inference-Efficient Language Models**, [arXiv 2501.18107v2,
   2025-06-07, ICML 2025](https://arxiv.org/abs/2501.18107v2).
   The loss model includes width/depth shape as well as parameters and training
   data, and candidate choice includes measured inference cost. In its tested
   model family, omitting shape could reverse model rankings. This is not a
   calibrated law for a new recurrent operator. **Rule:** declare all changed
   fidelity axes and validate forecasts on unseen configurations and hardware.

## Allocating experiments

5. **Deep Adaptive Design: Amortizing Sequential Bayesian Experimental
   Design**, Foster et al., [ICML 2021, PMLR 139](https://proceedings.mlr.press/v139/foster21a.html),
   Equation 1. Optimizes information about specified latent parameters using a
   probabilistic experimental model. **Rule:** prefer observations that separate
   explanations, but do not assign numeric information gain without justified
   likelihoods/priors. Amortization includes an upfront training cost.

6. **Step-DAD: Semi-Amortized Policy-Based Bayesian Experimental Design**,
   Hedman et al., [ICML 2025 / arXiv 2507.14057v1,
   2025-07-18](https://arxiv.org/html/2507.14057v1), Equations 1–6 / Section 3.
   Refines the design policy using observations partway through an experiment.
   It explicitly discusses misspecification of the model used to simulate and
   evaluate designs. **Rule:** revise subsequent experiments from actual
   evidence. A qualitative hypothesis-to-action table is an adaptation of this
   principle, not Step-DAD or calibrated Bayesian inference.

7. **Hyperband: A Novel Bandit-Based Approach to Hyperparameter
   Optimization**, Li et al., [JMLR 18(185),
   2018](https://www.jmlr.org/papers/v18/16-558.html), Sections 3.1–3.2.
   Uses resource brackets and successive halving to balance many cheap trials
   against fewer longer trials. Early loss can remain an unreliable estimate
   of the final value. **Rule:** protect some higher-fidelity coverage when
   early rankings are uncalibrated; a budget rejection is not a universal
   mechanism rejection. Report HPO cost savings separately from model quality.

## Reading the map correctly

No paper above establishes that this skill raises research success probability
by a known amount, or that a new sub-billion-parameter model can beat a frontier
27B model within one day. Those are new empirical claims. Skill validation,
correlation on supplied histories and CPU operator tests cannot establish them.
