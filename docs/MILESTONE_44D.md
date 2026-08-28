# Milestone 44D — explicit first post-root ordinary edge surface

Decision: D221

## Product boundary

Milestone 44D exposes the already-proven 34B one-time bridge from the first changed-basis revision root back into the ordinary revision-edge lineage.

```text
44A prepared changed basis
→ 44B explicit first transition
→ 44C explicit first revision root
→ 44D explicit first ordinary edge after that root
```

44D stops there.

It does not create a sequence declaration, a root-backed governed session, a later evidence-basis epoch, or any current/latest/head state.

## Why 34B is a separate product action

34A and 34B encode different human decisions.

34A records the first explicit rationale revision after the evidence basis changes. 34B then records a new ordinary same-working-set rationale after that root. The latter is not mechanically implied by the former, so Pyxis must not synthesize or copy it.

The user therefore sees the exact 34A root endpoint wording for context and receives a blank editor for the next rationale.

Exact textual no-op remains rejected by the established same-working-set revision boundary.

## Local predecessor rule

34B deliberately narrows durable reconstruction back down to the immediate predecessor.

After a verified 34A root exists, the first post-root edge requires only:

1. the exact loaded 34A root retained by 44C;
2. the caller-supplied current durable root file;
3. the caller-authored next rationale;
4. a caller-supplied no-overwrite edge destination.

The older 33B transition, changed working set, changed-basis note, and pre-transition endpoint are not recursively reopened for 34B persistence.

This is an important authority boundary: local continuation from a verified predecessor is not recursive ancestry traversal.

## Durable format

44D reuses the existing ordinary edge format:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

The written edge records the exact 34A root format and root SHA-256 as its predecessor reference.

The explicit 34B loader then freshly verifies the edge file and reconstructs it against the exact retained loaded root, returning the normal loaded revision-edge type.

Thus:

```text
34A root
→ one explicit 34B bridge
→ ordinary loaded edge type
```

No new edge format or generic root predecessor semantics are introduced.

## Product implementation

44D adds three bounded product pieces:

- `chromium_research_first_changed_basis_root_edge.py`
  - exact 44C result validation;
  - existing 34B extension creation;
  - existing 34B root-file verification and edge persistence;
  - fresh 34B edge relinking;
  - typed product result.

- `chromium_research_first_changed_basis_root_edge_textual.py`
  - exact root identity and root endpoint wording visibility;
  - blank next-rationale editor;
  - blank explicit current-root locator;
  - blank explicit no-overwrite edge destination;
  - locked success receipt.

- `FirstChangedBasisRootEdgeResearchSessionShell`
  - subclasses only the dedicated 44C shell;
  - mounts 44D only after exact 44C success;
  - leaves the mounted governed controller/session unchanged during 34B persistence.

The base `ResearchSessionShell`, existing root-backed shell family, second-epoch shell family, and third-epoch shell family are not modified.

## Historical branch coexistence

A successful 44C root is durable historical evidence. Therefore later continuation of the old-basis mounted session does not invalidate that root or the local 34B edge authored from it.

```text
old-basis continuation

and

persisted 33B transition
→ persisted 34A root
→ persisted 34B first ordinary edge
```

may coexist.

Pyxis does not infer that either branch is newer, preferred, canonical, current, or head.

## What success proves

A successful 44D result proves only that:

- the exact 44C loaded root matched the 44C persisted root identity;
- the caller supplied a durable root file whose bytes verify as that exact root;
- one genuinely new same-working-set revision was created from the root endpoint;
- one existing-format 24B edge was persisted without overwrite;
- that edge records the exact root format and SHA-256 as predecessor identity;
- the edge was freshly relinked through the explicit 34B loader;
- the mounted governed research session did not advance during this operation.

It does not prove authorship, authenticity, trusted time, semantic improvement, evidence support, branch preference, chronology, or current/latest/head status.

## Why 35A remains separate

35A adds a different authority transition: an explicit root-backed sequence declaration can begin at the 34A root, use the 34B bridge for its first member, and enter the governed session controller.

That means:

```text
34B first edge exists
!=
root-backed sequence declared
!=
root-backed governed session adopted
```

44D therefore does not mount 26B declaration or 35A adoption controls. Productizing that authority transition remains a separate frontier decision.

## Prior art / reuse

Internal prior art is sufficient and decisive:

- 34B / D180 — one-time root→ordinary-edge bridge, exact no-op rejection, existing-format persistence, current-root verification, fresh root-specific edge load;
- 44C / D220 — exact first-root product evidence;
- 35A / D181 — evidence that sequence/session adoption is a distinct next authority boundary.

The broader provenance review from 43E/44A remains applicable. Milestone 44D adds no external provenance subsystem.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Non-goals

44D does not add:

- 35A sequence/session adoption;
- root-backed re-entry planning;
- a fourth evidence-basis epoch;
- generic `epoch[n]`;
- arbitrary-depth ancestry traversal;
- a generic root-edge action for later evidence-basis families;
- file or digest discovery;
- path prefill or inference;
- CLI edge syntax;
- browser acquisition;
- chronology, latest, current, or head authority;
- path identity;
- authorship, authenticity, or trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.
