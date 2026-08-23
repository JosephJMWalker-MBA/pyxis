# Milestone 33B — Explicit Cross-Working-Set Transition

Decision: D178

## Product question

33A established a prepared changed evidence basis:

```text
one governed declared session endpoint
+
explicit additional already-relinked evidence
+
explicit human rationale over the changed set
→
new durable 20B working set
+
new durable 21B working-set note
```

33A intentionally stopped before claiming that the changed basis continued the old
research session.

The next researcher action is therefore:

> “Yes. I explicitly choose to continue my research from this exact declared endpoint
> onto this exact changed evidence basis.”

33B makes that relationship explicit and durable without pretending that a
cross-working-set transition is an ordinary same-working-set rationale revision.

## Core distinction

The existing 24B revision-edge format means:

```text
same exact working set
→ revised human note text
```

33B means something different:

```text
old declared endpoint
→ explicitly chosen different working set
→ human note already authored over that changed set
```

Therefore:

```text
same-working-set revision edge
!=
cross-working-set transition
```

33B introduces a distinct record type instead of weakening 24B semantics.

## Public boundaries

33B adds three application modules:

```text
chromium_research_session_working_set_transition.py
chromium_research_session_working_set_transition_persistence.py
chromium_research_session_working_set_transition_load.py
```

The in-memory creation boundary is:

```text
create_chromium_research_session_working_set_transition(
    controller,
    prepared_33a_result,
)
```

It returns:

```text
ChromiumResearchSessionWorkingSetTransitionRecord
```

with exactly:

```text
transition_mode
prior_endpoint
successor_working_set
successor_note
```

The durable transition format is:

```text
pyxis.chromium.research_session_working_set_transition.v1
```

The explicit transition mode is:

```text
caller_explicit_transition_to_changed_research_working_set
```

## Creation authority

33B creation accepts only an exact 29A research-session controller and an exact 33A
prepared-extension result.

The controller is re-presented through 28A and must remain coherent with its retained
26C evidence.

The 33A result must retain:

- the same session presentation;
- the exact controller-declared endpoint object;
- the exact working set attached to that endpoint;
- at least one explicitly appended member;
- the exact prior-members-plus-appended-members order;
- an exact 21A note attached to the changed 20A set;
- persistence receipts retaining those exact 20A/21A objects.

An unadopted 29A write is never consulted.

Thus:

```text
last successful endpoint write
!=
transition prior authority
```

The declared endpoint remains the prior authority.

## No inferred rationale inheritance

33B does not generate successor rationale text.

That text was already explicitly authored in 33A.

If the human chose the exact same words as the old rationale, 33B may bridge them
because the changed-basis note already records that new explicit human action.

Therefore:

```text
identical text across different working sets
!=
implicit semantic inheritance
```

The human action happened in 33A; 33B records the explicit relationship between the
old endpoint and that prepared basis.

## Durable transition record

The durable record stores only four conceptual facts:

```text
transition mode
prior endpoint content identity
successor working-set content identity
successor working-set-note content identity
```

Its canonical record shape is:

```text
{
  prior_endpoint_reference,
  successor_working_set_reference,
  successor_note_reference,
  transition_mode
}
```

Each reference contains only:

```text
format
record_sha256
```

The transition document contains no:

- filesystem paths;
- timestamps;
- revision numbers;
- latest/current/head fields;
- branch names;
- semantic-support fields;
- chronology claims;
- source-authenticity claims.

Therefore:

```text
content identity
!=
locator authority
```

and:

```text
local transition
!=
global research head
```

## Fresh persistence proof

Persistence requires four explicit paths:

```text
prior_edge_source
working_set_source
note_source
destination
```

Before writing the transition, Pyxis freshly re-establishes the referenced durable
records.

The prior endpoint is reopened through public 24C using the exact predecessor object
already retained by the transition's prior endpoint.

The changed basis is reopened through public 21C using the exact successor member
sequence retained by the transition. Public 21C itself freshly establishes public
20C.

The fresh identities must match the in-memory transition before a transition file is
written.

Thus:

```text
retained write receipt
!=
fresh durable bridge proof
```

## Path movement

A focused test moves the old endpoint file, the changed working-set file, and the
changed note file after the application objects already exist.

Persistence succeeds only when the caller explicitly supplies the new locations.

The transition file does not remember or infer the earlier locations.

Therefore:

```text
path = location, not identity
```

remains intact across the cross-working-set boundary.

## No discovery

If any supplied file is wrong, Pyxis does not search nearby locations for a matching
record.

The implementation performs no:

- directory scanning;
- digest search;
- newest-file selection;
- filename inference;
- predecessor discovery;
- successor discovery;
- member discovery.

A wrong but valid edge, working set, note, or member order fails locally.

## Transition self-integrity

The transition file uses canonical deterministic JSON plus SHA-256 self-integrity.

File-local verification proves only:

```text
these transition bytes are canonical and internally self-consistent
```

It does not open the referenced prior endpoint, working set, or note.

Therefore:

```text
transition self-integrity
!=
referenced-record availability or coherence
```

Referenced coherence is earned only by explicit relinking.

## Fresh transition relinking

The public load boundary is:

```text
load_chromium_research_session_working_set_transition(
    prior_endpoint,
    successor_items,
    prior_edge_source=...,
    working_set_source=...,
    note_source=...,
    transition_source=...,
)
```

The caller supplies every locator and the complete ordered successor member sequence.

The loader:

1. freshly verifies the transition file;
2. freshly reopens the old endpoint through 24C;
3. requires the supplied old endpoint identity to match that fresh edge;
4. requires the transition prior reference to match that fresh edge;
5. freshly reopens the successor 20B/21B basis through 21C;
6. requires both successor identities in the transition to match the fresh 20C/21C
   evidence;
7. returns one immutable loaded transition record.

The loaded record contains:

```text
verification
prior_endpoint
successor_note
```

The `prior_endpoint` is freshly reconstructed 24C evidence.

The `successor_note` is freshly reconstructed 21C evidence, which retains its fresh
20C working set.

## What the loaded transition means

A successful loaded transition establishes only:

> The caller supplied one exact durable prior edge, one exact ordered changed working
> set, one exact human note attached to that changed set, and one exact transition
> file whose recorded identities agree with all three freshly reconstructed durable
> records.

It does not establish:

- complete ancestry before the old endpoint;
- unique succession after the old endpoint;
- chronology;
- a branch name;
- current/latest/canonical head;
- semantic relevance;
- evidence support for the human rationale;
- source authenticity;
- citation authority.

Therefore:

```text
verified local cross-working-set relationship
!=
complete research history
```

## Loaded evidence survives locator loss

After successful transition relinking, a focused test deletes:

- the old endpoint file;
- the changed working-set file;
- the changed-note file;
- the transition file.

The already-loaded transition object remains available as application evidence.

This does not mean a future fresh process can reconstruct it without those durable
inputs.

Thus:

```text
already-loaded verified application evidence
!=
fresh durable re-entry capability
```

## No session adoption yet

33B deliberately does not modify:

```text
ChromiumResearchSessionController
```

and does not change the 24C predecessor union.

The loaded transition is therefore not yet a normal revision-chain predecessor.

That boundary is intentionally left explicit for the next milestone.

The next product question becomes:

> “Given one freshly verified 33B cross-working-set transition, what is the minimal
> new chain-root representation that lets the researcher revise the new rationale
> without pretending the transition itself was a same-working-set revision edge?”

That question should be answered separately rather than smuggled into the transition
format.

## Falsifiability

Focused 33B coverage proves:

1. creation retains the exact declared endpoint and exact 33A changed basis;
2. a prepared basis from another governed session rejects;
3. persistence freshly records the exact old-edge, new-working-set, and new-note
   identities;
4. fresh load reconstructs the exact local bridge from explicit durable inputs;
5. moved identical durable inputs work only through their explicitly supplied new
   locations;
6. a wrong old edge rejects without writing a transition;
7. a wrong successor working set rejects without writing a transition;
8. a wrong successor note rejects without writing a transition;
9. transition persistence is no-overwrite;
10. tampered transition bytes fail file-local verification;
11. wrong successor-member order fails fresh relinking;
12. transition bytes contain no locator/head/chronology/semantic-support fields;
13. explicitly re-authored identical rationale text remains eligible;
14. an unadopted 29A write never becomes transition prior authority;
15. an already-loaded transition remains application evidence after its durable files
    are removed.

## Scope

33B adds only:

- `src/pyxis/app/chromium_research_session_working_set_transition.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_persistence.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_load.py`;
- `tests/test_app_chromium_research_session_working_set_transition.py`;
- this milestone document.

It does not change:

- 20A/20B/20C semantics;
- 21A/21B/21C semantics;
- 24B/24C edge semantics;
- the 24C predecessor type union;
- 29A controller semantics;
- 30A rollover semantics;
- 31A re-entry semantics;
- 32A/32B restart-plan semantics;
- Chromium acquisition;
- CLI behavior;
- Textual UI;
- Repository Zero behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 33B proves

Successful 33B establishes only:

> From one exact governed declared endpoint and one exact 33A prepared changed
> evidence basis, Pyxis can record an explicit cross-working-set transition as a
> distinct canonical no-overwrite identity relationship, freshly re-establish the old
> endpoint and changed 20B/21B basis before writing it, and later freshly relink that
> transition from entirely explicit locators and successor member order without
> inventing revision-edge equivalence, discovery, chronology, semantic support, or
> global-head authority.
