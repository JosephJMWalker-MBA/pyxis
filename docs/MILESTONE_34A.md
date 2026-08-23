# Milestone 34A — Cross-Working-Set Revision Root

Decision: D179

## Product question

33A lets a researcher prepare a changed evidence basis and author a fresh human rationale over it.

33B lets the researcher explicitly and durably say:

```text
this exact old declared endpoint
→ continue onto
this exact changed working set + human rationale
```

But a loaded 33B transition is intentionally not an ordinary revision-chain predecessor.

The next researcher action is:

> “I have explicitly crossed onto this new evidence basis. Now I want to revise the rationale I wrote there without losing the fact that this lineage began at that basis change.”

34A establishes the minimal durable root for that new same-working-set revision lineage.

## Core distinction

33B means:

```text
old working set
→ explicit transition
→ changed working set + human rationale
```

A subsequent rationale revision means:

```text
same changed working set
→ revised human rationale text
```

Those are different relationships.

Therefore 34A does not make the 33B transition itself look like a 24B same-working-set revision edge.

Instead it introduces a distinct root:

```text
verified loaded 33B transition
+
first ordinary 22A revision of the transition successor note
→
34A cross-working-set revision root
```

Thus:

```text
cross-working-set transition
!=
first same-working-set revision after that transition
```

## Public in-memory boundary

34A adds:

```text
chromium_research_session_working_set_transition_revision_root.py
```

with:

```text
ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord
ChromiumResearchSessionWorkingSetTransitionRevisionRootError
create_chromium_research_session_working_set_transition_revision_root(...)
```

The root contains exactly:

```text
root_mode
transition
revision
```

The root mode is:

```text
caller_authored_revision_root_after_changed_research_working_set_transition
```

The `transition` field retains the exact caller-supplied loaded 33B transition.

The `revision` field is created through public 22A over exactly:

```text
transition.successor_note.note
```

The revised note therefore retains the exact changed working-set object.

Exact textual no-ops remain rejected by 22A.

## Why the root needs a durable identity

A purely in-memory wrapper would be insufficient.

If Pyxis created only an ordinary 22B revision, later durable edges could identify the predecessor note/revision but would have no durable identity representing:

```text
this lineage began after this exact cross-working-set transition
```

The basis-crossing could therefore disappear from later durable ancestry.

34A introduces a root format specifically to preserve that fact.

## Durable root format

The durable format is:

```text
pyxis.chromium.research_session_working_set_transition_revision_root.v1
```

The record stores only:

```text
transition_reference:
    format
    record_sha256

root:
    mode
    revision:
        mode
        revised_note:
            mode
            text
```

It does not duplicate:

- the old endpoint identity;
- successor working-set identity;
- successor note identity;
- working-set members;
- source evidence;
- filesystem paths.

Those relationships already belong to the referenced 33B transition.

Thus:

```text
root transition identity
+
first revised human wording
```

is sufficient durable information for this boundary.

## Fresh persistence

Persistence requires explicit current locators for:

```text
prior_edge_source
working_set_source
note_source
transition_source
destination
```

Before root bytes are written, Pyxis freshly relinks the full 33B transition through its public loader.

The fresh transition identity must match the exact transition retained by the in-memory root.

Pyxis then reconstructs the 34A root again over that fresh transition using the same revised human text.

Only after those checks does it write the canonical no-overwrite root file.

Therefore:

```text
retained loaded transition
!=
fresh durable root proof
```

## File-local verification

The root verifier checks only:

- exact canonical document shape;
- supported root format/mode;
- supported revision/note modes;
- valid transition reference shape;
- non-empty human revision text;
- SHA-256 self-integrity;
- canonical UTF-8 JSON bytes.

It does not open the referenced transition.

Therefore:

```text
root self-integrity
!=
transition availability or coherence
```

## Fresh root relinking

34A adds:

```text
load_chromium_research_session_working_set_transition_revision_root(...)
```

The caller explicitly supplies:

- already-loaded old endpoint context;
- complete ordered successor member sequence;
- old endpoint path;
- changed working-set path;
- changed-note path;
- transition path;
- root path.

The loader:

1. freshly verifies the root file;
2. freshly loads the complete 33B transition;
3. requires the root's transition reference to match that fresh transition identity;
4. reconstructs the first 22A revision over exactly the fresh transition successor note;
5. returns one immutable loaded 34A root.

No path discovery, digest search, directory scanning, member discovery, chronology inference, branch selection, history traversal, or current-head selection occurs.

## Path movement

Moved byte-identical prior-edge, working-set, note, and transition files remain usable only when the caller supplies their new explicit locations.

The root file does not store or recover those locations.

Therefore:

```text
path = location, not identity
```

continues to hold.

## Human revision semantics

The first root revision is an ordinary same-working-set human revision.

It is not generated by Pyxis.

The human must supply exact new text, and public 22A requires that text to differ exactly from the transition successor note.

34A does not infer:

- why the rationale changed;
- whether it improved;
- whether evidence supports it;
- whether the changed working set is complete;
- whether the new text is semantically different beyond exact textual inequality.

Thus:

```text
textual revision after evidence-basis change
!=
semantic improvement or evidence support
```

## Loaded evidence survives locator loss

After successful fresh root loading, the durable old edge, changed working set, changed note, transition, and root files may be removed.

The already-loaded root remains available as application evidence.

This proves only retained loaded state.

It does not prove a future process can reconstruct the root without those durable inputs.

## No ordinary edge adoption yet

34A deliberately does not change:

```text
chromium_research_working_set_note_revision_edge_load.py
chromium_research_working_set_note_revision_edge_sequence_load.py
chromium_research_working_set_note_revision_edge_persistence.py
```

A loaded 34A root is therefore rejected if supplied directly to today's ordinary 24C edge loader or 26A sequence loader.

This is intentional.

The next boundary must explicitly answer:

> “May an ordinary same-working-set revision edge name this exact 34A root as its predecessor?”

That future change should widen the predecessor union deliberately and preserve the root's own format/content identity.

Therefore:

```text
loaded 34A root
!=
already-supported ordinary revision-edge predecessor
```

## No head/session authority

The root file contains no:

- `latest`;
- `current_head`;
- `canonical_head`;
- branch name;
- timestamp;
- revision number;
- session declaration;
- chronology claim;
- semantic-support field.

A root means only:

> This first ordinary rationale revision was authored after this exact verified cross-working-set transition.

It does not mean the root is globally newest, unique, canonical, or adopted into a declared research session.

## Falsifiability

Focused 34A coverage proves:

1. root creation retains the exact loaded 33B transition;
2. the first revision's prior note is exactly the transition successor note;
3. the revised note retains the exact changed working set;
4. exact-text no-ops reject through public 22A;
5. wrong root input type rejects;
6. persistence freshly records the exact transition identity;
7. fresh root loading reconstructs the root through the exact durable transition;
8. moved identical durable inputs work only via explicit new paths;
9. a different valid transition rejects root persistence;
10. a different valid changed basis rejects root persistence;
11. root persistence is no-overwrite;
12. tampered root bytes fail file-local verification;
13. root bytes contain no duplicated basis/head/chronology/semantic-support authority;
14. a fresh load rejects a different valid transition;
15. an already-loaded root survives later locator loss as application evidence;
16. Unicode/whitespace revised text is preserved exactly;
17. today's ordinary edge loader rejects a loaded 34A root;
18. today's ordered sequence loader rejects a loaded 34A root.

The test module contains 16 collected tests; several tests cover multiple related assertions above.

## Scope

34A adds only:

- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root_persistence.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root_load.py`;
- `tests/test_app_chromium_research_session_working_set_transition_revision_root.py`;
- this milestone document.

It does not change:

- 20A–21C evidence-basis semantics;
- 22A–23C same-working-set revision semantics;
- 24B/24C revision-edge semantics or predecessor union;
- 26A–32B sequence/session/re-entry/restart behavior;
- 33A preparation semantics;
- 33B transition semantics;
- Chromium acquisition;
- CLI;
- Textual UI;
- Repository Zero;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 34A proves

Successful 34A establishes only:

> From one freshly verified 33B cross-working-set transition, Pyxis can accept one explicit human revision of the new-basis rationale, preserve the exact changed working set, durably bind that first revision to the exact transition identity, and freshly reconstruct that root from explicit durable inputs without treating the transition as an ordinary same-working-set edge or granting head/history/semantic authority.

It does not yet prove that ordinary 24B/24C revision edges may continue from that root.
