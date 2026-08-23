# Milestone 33A — Explicit Working-Set Extension Preparation

Decision: D177

## Product question

By 32B, the standalone governed research loop is durable across process exits:

```text
launch from explicit plan
→ inspect
→ revise rationale
→ persist successor
→ explicitly adopt continuation
→ prove/save restart plan
→ continue
```

That loop intentionally keeps every rationale revision attached to the **same exact
research working set**.

The next real researcher action is different:

> “I found additional evidence. I want to carry my existing evidence forward, add
> this new material explicitly, and write what I now think about the changed evidence
> basis.”

Before 33A, Pyxis had the lower-level primitives needed to create another 20A/20B
working set and another 21A/21B human note, but no session-level application boundary
stated what it means to prepare that changed evidence basis from one governed declared
session.

33A establishes that boundary without pretending that an evidence-set change is an
ordinary rationale revision.

## Core distinction

Every 22A through 32B revision edge preserves one exact working set.

Changing membership changes the object the human is reasoning about.

Therefore:

```text
rationale revision over same working set
!=
reasoning over a changed working set
```

33A does not extend the existing revision-edge format to cross that boundary.

Instead it prepares a new durable evidence basis first.

## Public application boundary

33A adds:

```text
pyxis.app.chromium_research_session_working_set_extension
```

with:

```text
ChromiumResearchSessionWorkingSetExtensionPersistenceResult
ChromiumResearchSessionWorkingSetExtensionError
persist_chromium_research_session_working_set_extension(...)
```

The operation accepts:

```text
one exact governed research-session controller
+
one or more explicit already-relinked 17D/18D/19D members
+
explicit human rationale text for the changed set
+
explicit no-overwrite 20B destination
+
explicit no-overwrite 21B destination
```

and produces:

```text
new 20A working set
→ durable 20B working-set sidecar
→ new 21A human note over that exact changed set
→ durable 21B working-set-note sidecar
```

## Declared session is the basis

33A starts from:

```text
controller.declared_endpoint
```

and specifically from the exact working set retained by that endpoint's human note.

It does **not** use:

```text
controller.last_endpoint_revision
```

as selection authority.

That field records only the last successful unadopted 29A write.

A focused test deliberately creates an unadopted v7 successor, then invokes 33A. The
prepared evidence basis still reports the declared v6 edge as its prior endpoint.

Thus:

```text
last successful write
!=
adopted reasoning state
!=
evidence-extension basis
```

## Exact prior-member preservation

The new working set is constructed as:

```text
exact prior declared working-set members
+
exact explicit appended members
```

Prior members remain first and retain exact Python object identity.

Explicit appended members follow in the exact caller-supplied order and also retain
exact object identity.

Pyxis does not sort, cluster, rank, deduplicate, or infer semantic relation.

Duplicates remain allowed because 20A already established:

```text
repeated membership
!=
accidental duplication
```

A focused test appends multiple members including an intentional duplicate and proves
exact order/identity retention.

## Explicit new human rationale

The changed working set does not inherit the declared endpoint rationale
automatically.

The caller must provide:

```text
rationale_text
```

which is delegated to public 21A and preserved verbatim.

This prevents Pyxis from silently implying:

> “the old interpretation still applies to this different evidence basis.”

Therefore:

```text
old rationale exists
!=
permission for Pyxis to copy it onto a changed working set
```

The caller may deliberately provide the exact same words.

That is allowed because the authority comes from the new explicit human action, not
from textual difference.

Thus:

```text
same text by explicit human choice
!=
machine-inferred inheritance
```

## Evidence membership does not support rationale

33A preserves the established evidence/human-interpretation split.

Adding a member means only that the human chose to carry that already-relinked record
inside the new ordered working set.

It does not mean the member:

- supports the new rationale;
- contradicts the new rationale;
- is more relevant than another member;
- authenticates another source;
- establishes citation authority;
- is representative or complete.

Therefore:

```text
member added to changed working set
!=
member semantically supports the new human rationale
```

## Already-loaded evidence boundary

33A accepts only already-relinked 17D/18D/19D application evidence.

It does not open member sidecars, reacquire Chromium pages, search for captures, or
perform fresh source verification.

Public 20A re-establishes the in-memory member contracts and public 20B records the
retained durable member identities.

A focused test loads a new paragraph-note member, deletes that member's durable
sidecar, and then successfully prepares the changed working set.

That proves only:

```text
already-relinked application evidence
can participate in new 20A/20B membership
```

It does not prove the deleted member sidecar can be freshly reopened later.

Thus:

```text
loaded evidence coherence
!=
fresh member-file verification
```

## Durable persistence

33A delegates persistence to the existing public boundaries:

```text
20B persist_chromium_research_working_set(...)
21B persist_chromium_research_working_set_note(...)
```

No new research persistence format is introduced.

The application boundary preflights both explicit destinations before the first
write:

- each must be a `pathlib.Path`;
- each parent directory must already exist;
- neither destination may already exist;
- the two destinations must be distinct.

This prevents predictable partial writes such as discovering only after 20B succeeds
that the requested 21B destination already exists.

Filesystem writes are still not claimed to be transactional. A genuinely unexpected
I/O failure after the first successful durable write is not rolled back or deleted by
Pyxis.

## Fresh durable relinking proof

A focused test takes the 33A outputs and freshly runs:

```text
20C load working set
→ 21C load working-set note
```

using the exact new member sequence and explicit durable paths.

The fresh relink must recover:

- the exact ordered member identities;
- the exact new working-set identity;
- the exact human rationale text.

This proves the prepared basis is durable and internally coherent.

It does not adopt it into the old revision chain.

## No adoption

After successful 33A:

```text
controller.loaded
controller.presentation
controller.declared_endpoint
controller.declared_endpoint.revision.revised_note.working_set
```

all remain unchanged.

The new working set and note exist separately as prepared durable application output.

The result contains no fields named:

```text
latest
current_head
canonical_head
adopted
continuation
transition
semantic_support
```

This is deliberate.

Therefore:

```text
prepared changed evidence basis
!=
adopted continuation session
```

## Why 33A stops here

Connecting an old declared session to a new working set is a qualitatively different
authority claim from revising text over the same set.

A future milestone must answer explicitly:

> What durable statement is allowed to say that a human chose to continue research
> from this exact prior declared endpoint onto this exact different working set and
> human rationale?

That future bridge must not be smuggled into 20B or 21B because neither format means
“continuation from another working set.”

33A therefore earns only the preparation state first.

## Falsifiability

Focused 33A coverage proves:

1. exact prior members are preserved first and one explicit new member is appended;
2. multiple appended members preserve exact caller order and intentional duplicates;
3. Unicode, whitespace, and multiline human rationale text survive exactly;
4. identical old/new rationale wording is allowed only through explicit caller input;
5. empty appended membership rejects before any durable write;
6. unsupported member types reject before any durable write;
7. whitespace-only rationale rejects before any durable write;
8. an existing working-set destination rejects without changing either output;
9. an existing note destination rejects before the working-set write occurs;
10. one path cannot be used for both outputs;
11. fresh 20C/21C relinking recovers the exact new basis and rationale;
12. the original governed session remains unchanged and unadopted;
13. the result shape carries no head/adoption/transition authority fields;
14. an unadopted 29A successor is not treated as the evidence-extension basis;
15. an already-loaded new member remains eligible even after its sidecar is deleted.

## Scope

33A adds only:

- `src/pyxis/app/chromium_research_session_working_set_extension.py`;
- `tests/test_app_chromium_research_session_working_set_extension.py`;
- this milestone document.

It does not change:

- 20A/20B/20C semantics;
- 21A/21B/21C semantics;
- 22A through 32B revision/rollover/restart semantics;
- research persistence formats;
- Chromium acquisition;
- standalone or Workspace Textual UI;
- CLI behavior;
- Repository Zero compiler/runtime/export/measurement behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 33A proves

Successful 33A establishes only:

> From one exact governed declared research session, Pyxis can preserve that
> endpoint's exact ordered working-set members, append one or more explicitly supplied
> already-relinked research members without semantic inference or deduplication,
> require a new explicit human rationale for the changed evidence basis, and persist
> the resulting 20B working set and 21B note through existing no-overwrite durable
> boundaries without mutating or adopting the original session.

It does not prove that the new evidence supports the rationale, that the changed set
is complete, that any source is authentic, or that the prepared basis is a
continuation/latest/head of the prior session.
