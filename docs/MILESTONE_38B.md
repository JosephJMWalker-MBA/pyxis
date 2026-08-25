# Milestone 38B — Proven second-epoch shell launch lineage

## Decision D195

Checkpoint-aware UI authority must not arise from an unverified pair of an in-memory re-entry object and a filesystem path.

38B introduces proof-carrying shell-lineage records for the persisted second-basis-epoch families. Each record binds one explicit overlay location to the **fresh re-entry reconstructed from that location during proof**.

The caller-supplied re-entry is treated only as already-earned authority that the fresh reconstruction must match.

## Public types

```text
ChromiumResearchSecondBasisEpochShellLineage
  overlay_source
  reentry

ChromiumResearchSecondBasisEpochContinuationShellLineage
  overlay_source
  reentry
```

The records intentionally carry only:

- explicit operational location context; and
- the fresh typed re-entry proven from that context.

They contain no current/latest/head marker, discovered source, checkpoint state, rollover state, chronology, or semantic-support claim.

## Public proof boundaries

```text
prove_chromium_research_second_basis_epoch_shell_lineage(...)
prove_chromium_research_second_basis_epoch_continuation_shell_lineage(...)
```

Neither function persists data or launches UI.

## 37B proof

Given:

- one already-earned `ChromiumResearchSecondBasisEpochReentryResult`; and
- one explicit 37B overlay path;

Pyxis:

1. resolves only the explicitly supplied source path;
2. strictly decodes that 37B overlay;
3. freshly re-enters it through the existing 37A boundary;
4. requires retained prior continuation presentation equality;
5. requires retained prior continuation terminal durable edge identity equality;
6. requires retained first-root durable identity equality;
7. requires second-root durable identity equality;
8. requires second-epoch governed presentation equality;
9. requires second-epoch terminal durable edge identity equality;
10. returns a shell-lineage record containing the resolved explicit path and the **fresh** re-entry.

The caller-supplied re-entry object is never simply attached to the supplied path.

## 37C / 37D proof

Given an already-earned `ChromiumResearchSecondBasisEpochContinuationReentryResult` and one explicit 37C/37D overlay path, Pyxis:

1. strictly decodes the explicit continuation overlay;
2. freshly re-enters it through the existing 37C boundary;
3. requires current continuation presentation equality;
4. requires current continuation terminal edge identity equality;
5. applies the same nested second-epoch ancestry proof used for 37B;
6. returns the explicit path bound to the fresh continuation re-entry.

A cumulative 37D overlay requires no separate lineage type because it is the same 37C format and re-entry family.

## Path remains location, not identity

38B deliberately allows a path-distinct configuration to prove the same earned lineage when:

- the path is explicitly supplied;
- that path freshly reconstructs a valid session; and
- all required durable ancestry/session relationships match.

Therefore:

```text
different explicit path
!=
automatically different session authority
```

but also:

```text
caller supplies path + object together
!=
proof that the path describes that object
```

The proof boundary resolves that gap.

## Fresh result is the carried authority

The wrapper's `reentry` field is the newly reconstructed result from the explicit source.

This avoids carrying two potentially divergent representations such as:

```text
caller_owned_reentry
+
overlay_path
```

Future UI can consume one coherent object:

```text
proven overlay_source
+
fresh reentry from that source
```

without treating Python object identity as durable authority.

## Proven behavior

The 38B tests cover:

- 37B path proof retaining a new fresh second-epoch result;
- 37C path proof retaining a new fresh continuation result;
- cumulative 37D proof through the same continuation lineage type;
- path-distinct but durably equivalent 37B configuration;
- path-distinct but durably equivalent 37C configuration;
- rejection of genuinely different 37B and 37C configurations;
- second-root tamper rejection;
- retained first-root tamper rejection;
- strict result-family type rejection before path work;
- wrapper shape limited to explicit source plus fresh re-entry.

## What 38B does not authorize

38B does **not** add:

- Textual checkpoint controls;
- CLI behavior changes;
- persistence writes or formats;
- automatic handoff between second-epoch shell families;
- a third basis-change epoch;
- locator discovery or path inference;
- format autodetection;
- current/latest/head authority;
- chronology or branch semantics;
- semantic-support, truth, authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

After 38B, Pyxis may say only:

> Pyxis can prove that one explicit persisted second-epoch launch configuration freshly reconstructs the same earned lineage, and can carry that verified path/result pairing forward as typed in-memory shell authority. The wrapper binds location context to a fresh reconstruction without treating path or Python object identity as durable session identity.
