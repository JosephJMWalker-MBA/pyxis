# Milestone 14A — Bounded Python support contract

**Decision D120 — Pyxis package compatibility claims must be bounded by interpreter versions actually proven by the full Repository Zero suite.**

## Product question

Before 14A, `pyproject.toml` declared:

```text
requires-python = ">=3.11"
```

while ordinary CI exercised only Python 3.11. That made package metadata broader than the evidence supporting it.

14A asks a release-contract question rather than an application-architecture question:

> Which Python interpreter range is Pyxis prepared to claim as supported now?

## Change

The package contract is now:

```text
>=3.11,<3.15
```

The Repository Zero workflow runs the same full pytest suite independently on:

```text
3.11
3.12
3.13
3.14
```

The matrix uses `fail-fast: false` so one failing interpreter does not hide evidence from the others.

Python 3.15 and later are not claimed by this contract. A future interpreter line must be added deliberately and proven before the upper bound moves.

## Evidence

Actions run #414 on branch head `a9077e53016de9e90795a30847f6cbf2febb505a` completed successfully in every matrix lane:

- Python 3.11: 214 passed
- Python 3.12: 214 passed
- Python 3.13: 214 passed
- Python 3.14: 214 passed

Each lane installs the package with the existing development dependencies and runs `python -m pytest`; no compatibility-specific tests are skipped or substituted.

## What 14A does not do

14A introduces no compiler, RIR, canonical authoring, revision, runtime, export, measurement, architecture-operation, preview, reconciliation, or UI behavior change.

It also does not claim support for pre-release/future Python versions merely because installation might succeed. Support is a bounded release contract backed by explicit CI evidence.

## Decision

D120 establishes:

**Pyxis should not advertise an open-ended interpreter range. Supported Python versions are the bounded set represented by package metadata and independently proven by the full CI matrix. Expanding that range requires new evidence.**
