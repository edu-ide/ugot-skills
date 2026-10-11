---
name: model-real-cardinality
description: Preserve the real 0/1/N cardinality of domain relationships across storage, domain models, APIs, and UI. Use when adding or reviewing fields such as app registrations, memberships, plans, roles, owners, devices, providers, sources, tags, or any scalar foreign key, enum, or boolean that may actually allow multiple simultaneous values or historical associations.
---

# Model Real Cardinality

Model relationships from explicit business invariants instead of choosing a scalar because the first example has one value. Carry the chosen cardinality through every system boundary and prove it with boundary tests.

## Workflow

### 1. State the relationship before editing

Name both entities and classify the relationship as exactly one, zero or one, zero or many, one or many, or many to many.

Search requirements, existing data, sibling products, and write paths for counterexamples. Ask whether the same entity can hold two values simultaneously, revisit a value later, or retain history after the current value changes.

Distinguish concepts that are often incorrectly collapsed:

- origin or first association
- current or primary association
- all active associations
- historical associations
- evidence inferred from another subsystem

### 2. Choose the smallest truthful model

Use a scalar only when a real invariant enforces a maximum of one and the code or database protects that invariant.

For multiple values, choose deliberately:

- a set for unique unordered membership
- a list only when order or duplicates carry meaning
- a join entity when the relationship has metadata, state, dates, provenance, or lifecycle
- an event or history table when changes themselves must remain observable

Do not replace a multi-valued fact with comma-separated text, repeated booleans, or a single primary field unless those are explicitly derived views.

### 3. Define lifecycle semantics

Specify:

- how a value is added
- whether repeated writes are idempotent
- whether and when a value is removed
- how current and historical membership differ
- how duplicate and concurrent writes behave
- which system is authoritative

When an operation contributes one value, keep that command or request singular even if the stored aggregate is plural. For example, one login identifies one application while the account accumulates a set of registered applications.

### 4. Trace every boundary

Follow the relationship end to end:

- database schema and constraints
- persistence mapping
- domain type and update methods
- commands, events, and service logic
- API DTO and serialization
- client normalization and legacy compatibility
- filtering, counting, labels, and detail views

A plural backend with a scalar DTO or equality-only frontend filter is still a scalar design bug.

### 5. Migrate without erasing evidence

Backfill only facts justified by an explicit operational rule or existing evidence. Make future writes populate the new model so the backfill is not a recurring repair job. Preserve old readers temporarily when a rolling deployment requires compatibility, and make migration uniqueness constraints match set semantics.

### 6. Test the cardinality boundaries

At minimum cover:

- zero values
- one value
- two distinct values
- the same value written twice
- legacy or missing data
- filtering for each associated scope
- removal and history, when supported
- concurrent writes, when lost updates are plausible

Assert the stored, domain, and API value plus the user-visible filtering or label. Do not stop at a mapper-only test.

## Completion Check

Before declaring the work complete, state:

- the chosen cardinality and invariant
- the add, deduplicate, and remove semantics
- the storage representation and migration rule
- the boundaries updated
- the tests proving zero, one, and multiple values

If the domain rule is unknown and either scalar or plural would materially change behavior, surface the ambiguity before making a destructive migration. Do not generalize unrelated relationships merely because they could hypothetically become plural.
