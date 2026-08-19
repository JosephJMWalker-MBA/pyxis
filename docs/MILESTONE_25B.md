# Milestone 25B — Durable Persistence of a Loaded-Edge Extension

Decision: D159

## Product question

After 25A creates one new human-authored revision explicitly extending an already-loaded 24C edge, can Pyxis preserve that action using the existing general 24B revision-edge format rather than inventing another file format?

25B answers **yes**.

The researcher action is:

```text
"I loaded this exact durable edge,
changed the rationale again,
and now I want to preserve that new change."
```

25B persists that new action as another:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

record.

No new durable revision schema is introduced.

## Why 25B exists

24B established one general durable edge representation.

24C established one general explicit edge loader.

25A established one general in-memory human extension from an already-loaded edge.

The remaining asymmetry was persistence.

Before 25B, the operational path was:

```text
23C loaded continuation
      ↓
24A extension
      ↓
24B durable edge
      ↓
24C loaded edge
      ↓
25A extension
      ↓
not yet durable
```

25B closes that gap:

```text
23C loaded continuation
      ↓
24A extension
      ↓
24B durable edge v4
      ↓
24C loaded edge v4
      ↓
25A extension v5
      ↓
25B durable edge v5
      ↓
24C loaded edge v5
```

The same 24B edge schema is reused for the second durable edge.

That is the architectural point of the milestone.

## Public API

The new explicit-module API is:

```python
persist_chromium_research_working_set_note_revision_edge_extension(
    extension,
    prior_edge_source,
    destination,
)
```

with:

```python
ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence
```

25B does not broaden the `pyxis.app` root export surface.

## Inputs

25B requires exactly:

```text
one 25A in-memory extension
+
one explicit current durable file for the loaded predecessor edge
+
one destination path
```

It does **not** require the older durable files beneath that loaded edge.

For the first general edge, those older files may include:

- the 23B continuation sidecar;
- the 22B revision sidecar;
- the 21B note sidecar;
- the 20B working-set sidecar;
- individual 17C/18C/19C member sidecars.

Those files may already be gone.

The immediate predecessor edge file itself must still be available for 25B persistence.

## Application action and persistence authority remain separate

25A operates entirely on already-loaded application evidence.

It can succeed after every related durable file has disappeared.

25B deliberately requires more.

Before writing a new durable successor, Pyxis must freshly re-establish that the explicit current predecessor edge file corresponds to the exact loaded edge retained by the 25A extension.

Thus:

```text
valid 25A extension
≠
authority to write a durable successor edge
```

This follows the existing Pyxis pattern:

```text
human action
→
in-memory representation
→
separate durable re-establishment
```

Persistence does not silently inherit authority merely because the application object exists.

## Re-establishing the live 25A contract

25B first reconstructs the caller-supplied extension through public 25A:

```python
create_chromium_research_working_set_note_revision_edge_extension(...)
```

using:

```text
extension.prior_edge
+
extension.revision.revised_note.note_text
```

This re-establishes the in-memory extension boundary before any file is written.

25B then requires the retained extension to preserve:

- the supported 25A extension mode;
- the supported 22A revision mode;
- the supported working-set-note mode;
- the exact predecessor endpoint note object;
- the exact working-set object.

A correctly typed but forged extension wrapper is not sufficient.

Therefore:

```text
25A record shape
≠
coherent live 25A extension
```

## Freshly reopening the immediate durable predecessor

After the 25A contract is re-established, 25B calls public 24C:

```python
load_chromium_research_working_set_note_revision_edge(
    extension.prior_edge.predecessor,
    prior_edge_source,
)
```

This is important.

25B does not merely call the 24B file verifier and trust the already-loaded wrapper.

It freshly reopens the explicit current predecessor edge against the explicit predecessor application object retained by that loaded edge.

That re-establishes:

```text
current predecessor-edge file integrity
+
explicit predecessor attachment
+
actual exact-text local revision
```

for the predecessor edge being used as the durable parent of the new edge.

## Stronger than 25A, but still not whole-history traversal

25A validates the supplied loaded edge's immediate local relationship.

If that edge retains another loaded edge as its predecessor, 25A deliberately does not recursively audit the predecessor's own ancestry.

25B is stronger because it freshly calls 24C on the current predecessor edge file.

24C validates the explicit predecessor object supplied for that reopening.

Therefore one additional local relationship may be re-established as part of the fresh predecessor reopening.

But 25B still does not:

- search for predecessor files;
- follow hashes through directories;
- recursively open older edge files;
- traverse an ancestry graph;
- validate an entire history;
- discover a head;
- enforce linearity.

The distinction is:

```text
fresh local durable predecessor reopening
≠
recursive whole-history audit
```

## Falsifiability proof — 25A can succeed while 25B rejects

The focused proof builds:

```text
loaded edge A
      ↓
loaded edge B
```

Then only edge A's relationship to its predecessor beneath A is forged.

Edge A's own content identity and endpoint note remain unchanged.

Edge B's local reference to A also remains unchanged.

Therefore edge B remains locally coherent for the exact 25A action:

```text
"extend this loaded edge B"
```

25A accepts and creates the new in-memory revision.

25B then attempts to persist that extension using edge B's current durable file.

To do so, it freshly calls 24C on B with the explicit retained edge-A object.

24C re-establishes A's immediate local relationship and detects the forged predecessor identity.

25B rejects before creating destination bytes.

This proves:

```text
valid in-memory extension
≠
sufficient durable predecessor authority
```

and also:

```text
fresh durable predecessor reopening
≠
blind trust in retained Python state
```

## Exact predecessor content identity

After 24C successfully reopens the current predecessor edge, 25B compares:

```text
freshly_loaded_prior.verification.edge_format
```

against:

```text
extension.prior_edge.verification.edge_format
```

and compares:

```text
freshly_loaded_prior.verification.edge_record_sha256
```

against:

```text
extension.prior_edge.verification.edge_record_sha256
```

using constant-time digest comparison.

A different but independently valid durable edge is rejected.

Therefore:

```text
valid durable edge
≠
correct durable predecessor for this extension
```

## Path remains location, not identity

The predecessor edge may be moved before 25B persistence.

The caller supplies its new path explicitly.

If the contents still verify and their content identity still matches the exact edge retained by the extension, 25B succeeds.

No persisted path is written into the successor edge.

Thus:

```text
filesystem location
≠
predecessor identity
```

## Immediate predecessor durability is required

25A can continue after the predecessor edge file disappears.

25B cannot persist a durable successor without a current durable predecessor edge file to re-establish.

If `prior_edge_source` no longer exists, 25B fails before destination creation.

This makes the authority boundary explicit:

```text
ability to continue in memory
≠
ability to create a new durable attachment
```

## Older sidecars are not required

Although the immediate predecessor edge file is required, older sidecars beneath the already-loaded predecessor are not.

The focused proof removes:

- member sidecars;
- working-set sidecar;
- note sidecar;
- first revision sidecar;
- continuation sidecar;

while retaining only:

```text
already-loaded application evidence
+
current predecessor edge sidecar
```

25B still succeeds.

No older durable file is discovered or reread.

Therefore:

```text
current immediate predecessor durability
≠
requirement to retain the entire durable ancestry on disk
```

## Persisted schema

25B writes the exact existing 24B format:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision_edge.v1",
  "edge_record": {
    "predecessor_reference": {
      "format": "pyxis.chromium.research_working_set_note_revision_edge.v1",
      "record_sha256": "<exact prior edge record digest>"
    },
    "edge": {
      "mode": "caller_authored_research_working_set_note_revision_edge",
      "revision": {
        "mode": "caller_authored_revision_of_research_working_set_note",
        "revised_note": {
          "mode": "caller_authored_note_on_research_working_set",
          "text": "<verbatim new human wording>"
        }
      }
    }
  },
  "edge_record_sha256": "<sha256 of canonical edge_record>"
}
```

The predecessor format is now the edge format itself.

This is the first creator path that writes the same-format predecessor shape 24B verification already allowed structurally.

## No predecessor content duplication

The successor edge does not copy:

- predecessor note wording;
- earlier note wording;
- source evidence;
- member records;
- working-set membership;
- browser observations;
- filesystem paths;
- timestamps;
- revision numbers.

It stores only:

```text
predecessor edge format
+
predecessor edge record SHA-256
+
new verbatim human wording
```

That is enough for later explicit 24C relinking when the caller supplies the predecessor application object.

## Existing 24B verifier remains authoritative for file integrity

25B does not add another verifier.

The output is verified by the unchanged public function:

```python
verify_chromium_research_working_set_note_revision_edge(...)
```

Therefore the same integrity boundary remains in force.

A valid 25B-created edge file proves only its own canonical structure and self-integrity.

It still does not prove:

- that the referenced predecessor exists;
- that the predecessor digest is correct;
- that the new wording differs from the real predecessor wording;
- that the edge belongs to a unique history;
- that the edge is later in time;
- that the human wording is true.

Thus:

```text
25B-created file integrity
=
24B file integrity
```

not stronger authority.

## Existing 24C loader reopens 25B output

A central acceptance proof is:

```text
loaded prior edge
+
25B successor file
→
existing 24C loader
→
loaded successor edge
```

No 25C loader is needed.

The unchanged 24C API can load the successor because 24B/24C were genuinely generalized.

Successful loading preserves:

```text
loaded_successor.predecessor
is
loaded_prior
```

and:

```text
loaded_successor.revision.prior_note
is
loaded_prior.revision.revised_note
```

The new note text equals the exact verbatim 25A wording.

This closes the reusable operational loop.

## Reusable loop

After 25B, the same application and durable operations may repeat:

```text
loaded edge N
      ↓
25A human extension
      ↓
25B durable successor edge N+1
      ↓
24C explicit load
      ↓
loaded edge N+1
      ↓
25A human extension
      ↓
25B durable successor edge N+2
      ↓
24C explicit load
      ↓
...
```

The important point is what this loop does **not** imply.

It does not create automatic iteration.

The caller still explicitly supplies each predecessor object and file.

Thus:

```text
repeatable explicit operation
≠
automatic traversal
```

## Determinism and no-overwrite

For the same exact 25A extension and the same exact durable predecessor identity, 25B produces deterministic canonical bytes.

The edge-record SHA-256 is deterministic.

Different destination paths receive identical bytes.

Persistence uses exclusive creation.

An existing destination is never silently overwritten.

Thus the existing persistence safety properties continue to hold.

## Integrity still does not become authority

25B does not modify the existing 24B verifier's deliberate weakness.

A caller may still construct a self-consistent edge file with a wrong predecessor digest, recompute its outer digest, and pass file-only 24B verification.

A caller may still construct a self-consistent edge file whose new wording equals the real predecessor wording and pass file-only verification.

Those relationships are recovered only through explicit 24C loading.

Therefore:

```text
self-integrity
≠
predecessor correctness
≠
actual human revision relative to predecessor
```

25B does not blur that separation.

## No new history semantics

25B does not establish:

- a global revision history;
- a current head;
- a preferred successor;
- uniqueness of successor;
- linearity;
- chronology;
- trusted time;
- revision numbering;
- ancestry discovery;
- filesystem traversal;
- cycle detection;
- cycle absence;
- branch semantics;
- merge semantics;
- whole-history validation;
- semantic improvement;
- semantic difference beyond exact text inequality already earned by 22A;
- source truth;
- claim support;
- authorship authentication.

Multiple valid successor edges could be created from the same predecessor edge.

25B does not rank or reconcile them.

That would be a different product capability.

## Authority boundary

25B preserves the following separation:

```text
24C loaded edge evidence
≠
25A human decision to revise again
≠
25B durable representation of that revision
≠
24B file integrity
≠
24C future relinking
≠
whole-history authority
≠
semantic truth
```

Successful 25B persistence establishes only:

> One exact coherent 25A human extension was durably represented in the existing general 24B edge format after the immediate predecessor edge was freshly reopened and matched by content identity.

Nothing stronger is implied.

## Focused test contract

The 25B focused tests prove:

1. the existing 24B format is reused unchanged with an edge-format predecessor reference;
2. only predecessor content identity and new human wording are stored;
3. moved predecessor paths work because location is not identity;
4. a different independently valid predecessor edge is rejected before write;
5. the immediate predecessor edge file is required for durable persistence;
6. older 17C/18C/19C/20B/21B/22B/23B sidecars are not required;
7. the live 25A extension contract is re-established before write;
8. a 25A extension that remains valid in memory can still be rejected by 25B's stronger fresh-24C durability gate;
9. ordinary tampering of the current predecessor edge file is rejected before write;
10. 25B output reloads through the unchanged public 24C loader;
11. deterministic bytes, no-overwrite behavior, explicit-module importability, and wrong-type rejection remain intact.

## Scope exclusions

25B makes no changes to:

- the 24B edge format;
- the 24B verifier;
- the 24C loader;
- the 25A extension constructor;
- root exports;
- README;
- `docs/CURRENT_STATE.md`;
- browser acquisition;
- Chromium DevTools behavior;
- source capture;
- source authenticity;
- claims;
- citations;
- LLM behavior;
- repository compiler/RIR/runtime/export behavior;
- measurement behavior;
- researcher UI;
- digest search;
- directory scanning;
- recursive file loading;
- automatic history traversal;
- chronology;
- timestamps;
- current-head semantics;
- branch or merge semantics.

## Result

25B turns the 24B/24C generalization into a genuinely reusable write/read cycle.

Pyxis can now repeatedly perform:

```text
explicit loaded edge
→
explicit human revision
→
explicit durable edge
→
explicit verified reload
```

without inventing a new application class or durable schema for each revision depth.

The cycle remains caller-driven, local, falsifiable, content-addressed, and deliberately weaker than a history engine.
