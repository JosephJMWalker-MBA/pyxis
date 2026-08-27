# Milestone 41A — Proven third-epoch shell launch lineage

Status: proposed implementation pending executed test evidence.

Decision: D206

## Question

40B–40D established a concrete persisted third evidence-basis epoch and repeatable ordinary continuation above it while retaining first-, second-, and third-root ancestry.

The next product direction is to make that already-earned three-root state usable from public product surfaces. Before CLI or Textual may carry a third-epoch session, however, Pyxis must avoid a launch-lineage mistake already identified during the second-epoch progression:

```text
caller-owned re-entry object
+
caller-supplied overlay path
!=
proof that the path describes that object
```

41A therefore asks the narrow prerequisite question:

> Can one explicit 40B or 40C/40D overlay location be bound to a fresh matching three-root re-entry as typed in-memory launch authority, without adding UI, CLI, persistence, discovery, or stronger path semantics?

## Decision D206

Pyxis may create proof-carrying third-epoch shell-lineage records only after freshly reconstructing the exact explicitly supplied overlay and matching the complete earned authority relevant to that launch family.

Two public frozen records are introduced:

```text
ChromiumResearchThirdBasisEpochShellLineage
    overlay_source
    reentry

ChromiumResearchThirdBasisEpochContinuationShellLineage
    overlay_source
    reentry
```

Each record carries exactly:

1. one explicit operational location; and
2. the fresh typed re-entry reconstructed from that location during proof.

No arbitrary caller-owned re-entry object is simply attached to a path.

## Public proof boundaries

```text
prove_chromium_research_third_basis_epoch_shell_lineage(...)
prove_chromium_research_third_basis_epoch_continuation_shell_lineage(...)
```

Neither boundary persists data or launches a product surface.

## 40B third-epoch proof

Given:

- one already-earned `ChromiumResearchThirdBasisEpochReentryResult`; and
- one explicit 40B overlay path;

Pyxis:

1. resolves only that explicit path;
2. strictly decodes the 40B locator overlay;
3. freshly re-enters the complete third epoch through the existing public 40A boundary;
4. matches the retained second-epoch continuation presentation;
5. matches the retained second-epoch continuation endpoint durable identity;
6. matches retained first-root durable identity;
7. matches retained second-root durable identity;
8. matches third-root durable identity;
9. matches third-epoch governed presentation;
10. matches third-epoch terminal durable edge identity; and
11. returns the explicit resolved location bound to the fresh re-entry.

The returned `reentry` is the new reconstruction from the supplied path, not the arbitrary caller object and not a previously retained checkpoint object.

## 40C / 40D continuation proof

Given:

- one already-earned `ChromiumResearchThirdBasisEpochContinuationReentryResult`; and
- one explicit 40C-format continuation overlay path;

Pyxis:

1. strictly decodes that exact continuation overlay;
2. freshly re-enters it through the existing public 40C boundary;
3. matches current continuation presentation;
4. matches current continuation terminal durable identity;
5. applies the complete nested 40B three-root proof to the retained third-epoch anchor; and
6. returns the explicit location bound to the fresh continuation re-entry.

40D cumulative checkpoints use the unchanged 40C continuation-overlay format and re-entry family, so no separate cumulative shell-lineage type is introduced.

## Path discipline

The wrapper makes an explicit path usable as launch **location context** only after that location has freshly proven the earned lineage.

Therefore:

```text
different explicit path
!=
automatically different durable session
```

and:

```text
same-looking path/object pair
!=
authority without fresh proof
```

A path-distinct overlay may be accepted only when explicit fresh reconstruction proves the same durable governed state and ancestry.

41A adds no path discovery, moved-file search, directory scan, filename inference, predecessor search, format autodetection, or latest/current/head selection.

## Three-root ancestry remains concrete

41A does not generalize the ancestry representation.

The proof follows the concrete already-earned chain:

```text
first root
   ↓
first-root continuation
   ↓
second root
   ↓
second-root continuation
   ↓
third root
   ↓
third-root session / continuation
```

The new wrappers do not add:

- `epoch[n]`;
- an ancestor array;
- recursive parent overlays;
- a generic lineage walker; or
- an arbitrary-depth claim.

## Failure behavior

Proof fails when:

- the supplied result is the wrong typed family;
- the supplied path is not a `Path`;
- the explicit overlay cannot be decoded;
- any referenced evidence cannot be freshly reconstructed;
- retained first-root evidence is tampered;
- retained second-root evidence is tampered;
- retained third-root evidence is tampered;
- retained second-epoch continuation differs from the earned ancestry;
- current third-epoch presentation or endpoint differs; or
- current continuation presentation or endpoint differs.

Failure grants no discovery fallback or path substitution.

## Why 41A precedes CLI/Textual parity

The second-epoch product progression demonstrated that UI launch lineage should not be reduced to an unverified controller plus path pair.

41A earns the application-layer launch authority first. Later milestones may consume these exact proof-carrying wrappers from CLI or Textual without reintroducing path/object ambiguity.

This also creates a clean prerequisite for a later three-root authority-inspection projection: immutable launch provenance can be based on an already-proven explicit source + fresh re-entry pair rather than reconstructed inside a renderer.

## Integrity discipline

Durable SHA-256 identities used by the existing loaders remain integrity / record-identity facts only.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

## Non-goals

41A does not add:

- CLI third-epoch launch;
- Textual third-epoch launch;
- checkpoint controls;
- in-process handoff behavior;
- three-root authority-inspection UI or JSON report;
- new persistence formats;
- another evidence-basis epoch;
- generic `epoch[n]` lineage;
- arbitrary-depth ancestry;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 41A permits only this statement:

> Pyxis can bind one explicitly supplied persisted third-epoch or post-third-root continuation location to a fresh reconstruction proven to match the already-earned three-root lineage, and can carry that verified location/result pair forward as typed in-memory launch authority. The wrapper makes location context usable without making path or Python object identity durable session identity.
