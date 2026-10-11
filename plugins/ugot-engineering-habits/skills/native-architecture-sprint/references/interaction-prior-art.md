# Interaction and memory: distinctions that change experiments

Inspected 2026-09-05. Recheck newer revisions when using these sources later. These papers motivate operators and controls; none proves a project model is better.

1. Kuo et al., *On Decompositions of Multivariate Functions*, Example 2.3, Eq. (2.10b): [author manuscript](https://web.maths.unsw.edu.au/~fkuo/pubs/preprint/ksww09-decomp.pdf). For `G(x,m)=F(x+m)` anchored at zero, the two-block component is `F(x+m)-F(x)-F(m)+F(0)`. Removing anchor-axis effects does **not** guarantee statistical orthogonality under a data distribution or useful information synergy. Test actual trained incremental value rather than declaring the subtraction itself novel.

2. Sharkey, *A Technical Note on Bilinear Layers for Interpretability*, section 2.1 and Eqs. (14)–(15): [primary manuscript](https://arxiv.org/html/2305.03452). Multiplicative FFN features and expansions into self/cross terms already exist. ReLU-squared mixed differences are piecewise quadratic; they are not globally identical to a simple `2ab` product. Test against a joint nonlinear branch with identical projections and against separated features, not only against a smaller baseline.

3. *Conditional Memory via Scalable Lookup*, Eqs. (3)–(4): [Engram primary manuscript](https://arxiv.org/html/2601.07372v1). Hidden-state-dependent gating already produces non-additive context–memory coupling. A new branch cannot claim to introduce interaction for the first time. State its narrower restriction or learning hypothesis and include a faithful gated-memory baseline. Count lookup parameters and disclose shared versus independent memory tables across depths.

For a short architecture sprint, these distinctions prevent three expensive mistakes: claiming an old operator as a discovery, mistaking mathematical cancellation for better learning, and comparing an enlarged model only to a smaller one.
