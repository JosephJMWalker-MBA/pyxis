# Milestone 30A — Explicit Continuation-Session Rollover

Decision: D171

## Product question

29A and 29B deliberately stop after a durable successor is written:

```text
declared session endpoint
→ explicit human revision
→ durable successor edge
→ write receipt
```

The displayed and loaded declared session remains unchanged.

That non-adoption boundary is important, but it creates the next real researcher action:

```text
"I wrote this successor deliberately.
I now want to continue working from this specific successor."
```

30A adds that explicit transition without converting it into a global head or chronology claim.

## Core transition

30A composes existing public boundaries:

```text
old 29A controller
+
explicitly selected successful 29A revision result
+
explicit successor edge path
+
explicit new declaration destination

→ 26A fresh one-edge relinking
→ 26B new durable one-edge declaration
→ 26C fresh declaration relinking
→ new 29A continuation controller
```

The old controller and old declaration are not mutated.

## Why the successful revision result is explicit

29A retains `last_endpoint_revision` as application bookkeeping.

30A does **not** treat that field as selection authority.

A programmatic caller may have written more than one sibling successor from the same declared endpoint. Therefore the rollover call requires the specific successful 29A result to adopt:

```python
rollover_chromium_research_session_to_persisted_successor(
    controller,
    chosen_revision_result,
    successor_edge_source=...,
    declaration_destination=...,
)
```

This means:

```text
controller bookkeeping order
!=
caller continuation choice
```

and:

```text
most recently retained successful write
!=
automatically selected continuation
```

## New declaration shape

30A does not copy the older declared segment into a larger replacement declaration.

If the old declared session is:

```text
starting predecessor → v5 → v6
```

and the explicitly selected successful write is:

```text
v6 → v7
```

then the new declaration is only:

```text
starting predecessor identity = v6
edge identities = [v7]
```

Thus the new declaration says only:

> this explicit continuation session begins from this exact already-loaded predecessor and contains this exact explicitly selected successor.

It does not claim that the new file contains the complete prior history.

## Public boundary

30A adds:

```text
pyxis.app.chromium_research_session_rollover
```

with:

```python
ChromiumResearchSessionRolloverResult
rollover_chromium_research_session_to_persisted_successor(...)
```

The result retains:

```text
prior_controller
prior_revision
explicit_sequence
declaration
loaded_declaration
continuation_controller
```

No result field is named:

```text
latest
current
head
canonical_head
complete_history
truth
```

## Step 1 — selected revision coherence

Before reading the successor file, 30A requires the explicitly selected 29A result to remain locally coherent with the supplied old controller:

- correct result type;
- `revision.prior_session is controller.presentation`;
- `revision.extension.prior_edge is controller.declared_endpoint`;
- `revision.persistence.extension is revision.extension`;
- existing general edge format.

This proves only that the selected result belongs to this exact loaded session endpoint.

It does not prove uniqueness or chronology.

## Step 2 — explicit successor fresh relinking

The caller supplies `successor_edge_source`.

30A calls public 26A with:

```text
starting_predecessor = controller.declared_endpoint
edge_sources = [successor_edge_source]
```

That fresh relinking proves the supplied durable edge is locally attached to the exact loaded old endpoint.

30A then requires the freshly observed successor content identity to equal the content identity recorded by the explicitly selected 29A persistence result.

It also requires the exact reconstructed human wording to equal the wording in the selected revision result.

Therefore:

```text
valid sibling successor from same endpoint
!=
selected successor
```

A different sibling edge may be perfectly valid and still reject because it is not the explicitly selected revision result.

## Path remains location, not identity

The selected 29A persistence result retains the original destination path, but 30A does not require that path to remain current.

The caller may move the successor bytes and explicitly supply the new location.

Identity is established from the freshly reopened durable record, not path equality.

Thus:

```text
original persistence path
!=
required future location
```

and:

```text
path = location, not identity
```

remain intact.

## Step 3 — new durable declaration

After fresh successor identity matches the selected 29A result, 30A persists the one-edge 26A sequence through public 26B.

The destination is explicit and no-overwrite.

The old declaration is not edited, replaced, or deleted.

The new declaration stores only:

- old declared endpoint content identity as starting predecessor;
- selected successor content identity as its sole edge member;
- existing sequence mode and self-integrity.

No paths, timestamps, revision numbers, or head markers are introduced.

## Step 4 — fresh 26C re-entry

30A then freshly loads the just-created declaration through public 26C using:

```text
old loaded endpoint
+
explicit successor path
+
new declaration path
```

The declaration therefore earns the same declaration↔explicit-evidence reconciliation as every other 26C session.

30A does not return a new application controller from merely persisted 26B bytes.

It first requires fresh 26C relinking.

## Step 5 — new continuation controller

Only after 26C succeeds does 30A create:

```text
ChromiumResearchSessionController(new_loaded_declaration)
```

Its `declared_endpoint` is the exact freshly loaded chosen successor edge.

Its complete 28A presentation contains the one newly declared continuation member and the same retained working-set context attached to that rationale.

This is the first explicit session-state adoption boundary.

But its authority is bounded:

```text
explicitly adopted continuation session
!=
global current revision
!=
latest revision
!=
canonical head
```

## Old state remains immutable

A successful rollover does not mutate:

```text
old controller.loaded
old controller.presentation
old controller.declared_endpoint
old controller.last_endpoint_revision
old durable declaration bytes
```

The continuation controller is a separate application object over a separate durable declaration.

Thus:

```text
new session adoption
!=
old session mutation
```

## Older durable files may disappear

After the selected successor has already been persisted, 30A requires only:

```text
old endpoint retained as loaded application evidence
+
explicit durable selected successor file
+
new declaration destination
```

The old declaration and prior edge files may be absent.

This does not prove the older durable ancestry exists.

It preserves the established rule that already-loaded verified application evidence may remain useful after older sidecars disappear.

## Continuation can continue again

The returned `continuation_controller` is a normal 29A controller.

Therefore after rollover:

```text
new declared endpoint v7
→ explicit v8 revision via 29A
→ later explicit rollover again if chosen
```

This creates a repeatable governed research loop without any automatic traversal or head pointer:

```text
inspect
→ revise explicitly
→ persist successor
→ explicitly choose rollover
→ new declared continuation session
→ inspect/revise again
```

## Failure behavior

30A rejects before declaration persistence when:

- controller type is wrong;
- selected revision type is wrong;
- selected revision belongs to another controller/session;
- selected revision does not extend the exact old endpoint;
- selected persistence/extension wrapper is incoherent;
- explicit successor cannot freshly relink to the old endpoint;
- explicit successor identity differs from the selected result;
- explicit successor exact human text differs from the selected result.

26B retains no-overwrite behavior for the new declaration destination.

If the destination already exists, existing bytes remain unchanged.

## Explicit sibling choice without branch semantics

30A permits the caller to explicitly choose one valid sibling successor result if multiple were created programmatically.

This does **not** add a branch model.

Pyxis does not:

- enumerate siblings;
- discover alternative successors;
- rank successors;
- label a branch;
- merge branches;
- infer a preferred branch;
- assert uniqueness.

The caller already possesses the exact successful result and exact durable file they choose to continue from.

Therefore:

```text
explicit choice among caller-known successors
!=
automatic branch semantics
```

## No UI change yet

30A is application-only.

29B remains intentionally locked after one successful UI successor write.

A later UI milestone may expose an explicit rollover action using the exact successful 29A receipt and explicit declaration destination, then replace the displayed research controller only after 30A returns a verified continuation controller.

That UI transition should preserve the same language:

```text
continue from this successor
```

rather than:

```text
make latest/current/head
```

## Falsifiability

Focused tests prove:

1. valid rollover creates a new one-edge declaration and new controller over the exact selected successor;
2. an explicitly selected earlier sibling succeeds even when `controller.last_endpoint_revision` refers to another later-written sibling;
3. a different valid sibling file rejects when paired with the selected revision result;
4. moved identical successor bytes remain usable from an explicitly supplied new path;
5. declaration destination is no-overwrite;
6. old controller state and old declaration bytes remain unchanged;
7. old declaration and prior edge files may disappear before rollover once the endpoint remains loaded and successor is durable;
8. returned continuation controller can author the next explicit successor through existing 29A;
9. cross-controller or forged selected revision evidence rejects before new declaration creation;
10. new declaration records exactly the old endpoint identity followed by exactly one chosen successor identity;
11. result surface adds no global-head authority and the module remains explicit rather than package-root broadened.

## What successful 30A proves

Successful 30A establishes only:

> Given one coherent loaded research-session controller, one explicitly selected successful 29A endpoint-revision result belonging to that controller, one explicitly supplied durable successor file whose fresh content identity matches that selected result, and one explicit no-overwrite declaration destination, Pyxis can create and freshly re-establish a new one-edge declared continuation session anchored to the old declared endpoint and return a new controller whose declared endpoint is exactly that selected successor, while leaving the old session and old declaration unchanged.

## What 30A does not prove or do

30A does **not** establish:

- latest revision;
- global current revision;
- canonical head;
- complete history;
- chronology;
- unique successor;
- branch discovery;
- branch ranking;
- branch merging;
- automatic successor choice;
- directory scanning;
- digest search;
- path discovery;
- recursive ancestry traversal;
- old-declaration mutation;
- old-session mutation;
- semantic improvement;
- truth;
- source authenticity;
- citation authority;
- semantic support;
- browser acquisition;
- Textual rollover controls.

The core boundary is:

```text
explicitly selected durable successor
→ new explicitly declared continuation session
!=
global/latest/current/canonical head
```
