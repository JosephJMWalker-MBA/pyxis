# Milestone 51D — CLI creation of one initial governed session root

Decision: **D284**  
Issue: **#304**  
Pull request: **#305**

## Research question

51C established the first truthful governed application state over one already-loaded
`research_working_set_note.v1` or `.v2` root. It deliberately did not provide a
product surface for creating that root.

For the concrete path earned by 51B, the next researcher action was therefore:

> How can one explicit saved bare passage plus one first human rationale become the
> first durable governed-session root without inventing a genesis format, locator
> registry, current/head authority, or a second validation layer?

The architecture and prior-art review in #303 falsified the need for a new durable
root format or generic application service before implementation.

## Product surface

51D adds one thin command:

```text
pyxis research-start \
  --capture <research_capture.v1> \
  --selection <research_paragraph_text_selection.v1> \
  --rationale <human text> \
  --working-set-destination <research_working_set.v2> \
  --note-destination <research_working_set_note.v2>
```

The command supports exactly one already-saved bare `exact_range_selection` member.
It does not generalize to arbitrary member families, multiple members, projects,
notebooks, tags, search, or ambient discovery.

## Existing authority composition

51D introduces no new evidence constructor or persistence schema. The command
composes existing public boundaries in this exact order:

```text
explicit durable capture
→ fresh public 16C capture load
→ fresh public 49B bare-selection relink
→ public 20A one-member working set
→ public 21A first human rationale
→ existing 20B v2 working-set persistence
→ existing 21B v2 note persistence
→ fresh public 21C root reopening
→ 51C initial-session controller
→ deterministic operation receipt
```

The durable products remain exactly:

```text
pyxis.chromium.research_working_set.v2
pyxis.chromium.research_working_set_note.v2
```

No `research_session_genesis` document is introduced.

## Rationale validation before durable mutation

A useful implementation correction emerged from following the existing boundaries
rather than duplicating them.

Public 21A already owns the rule that a working-set note must contain non-whitespace
caller-authored text while preserving the accepted text verbatim. Because 21A is a
pure in-memory application operation, 51D constructs the 21A note **before** the first
durable write.

Therefore an invalid whitespace-only rationale fails with neither output file
created, while the CLI still does not become a second note-validation authority.

## Output preflight

Before source loading or the first durable write, the command requires:

- explicit `Path` destinations for both durable outputs;
- distinct resolved working-set and note paths;
- an existing directory parent for each destination; and
- neither destination to already exist.

This preflight prevents predictable partial creation. The existing persistence
boundaries remain the actual no-overwrite authority.

## Honest partial-write semantics

Creating the two-file root is not represented as an atomic transaction.

The note writer must freshly relink the already-persisted working set, so a valid
working-set file can exist before an unpredictable later note-stage failure occurs.
If that happens, 51D does not delete the valid working-set evidence merely to make
the operation appear atomic.

Instead:

- the command fails;
- no successful root receipt is emitted;
- the valid working-set artifact may remain; and
- cleanup or retry remains caller-owned.

The same rule applies if fresh 21C reopening fails after both writes: no success
receipt is emitted, and already-created evidence is not silently rolled back.

## Fresh reopening before success

A successful operation is not reported from persistence return values alone.

After both writes, the command freshly reopens the root through public 21C using the
exact already-relinked bare member and the explicit just-written paths. It then
constructs `ChromiumResearchInitialSessionController` from that fresh loaded root.

The receipt is emitted only after this re-entry proof succeeds.

This preserves the distinction:

```text
path = caller-supplied location context
fresh verification + relinked content identity = earned application authority
```

## Receipt boundary

The deterministic receipt reports only operation-context paths and identities needed
to explain what was created, including:

- capture input path as context only;
- saved-selection input path as context only;
- working-set output path, format, and freshly reopened record SHA-256;
- note output path, format, and freshly reopened record SHA-256; and
- initial-session presentation mode.

It explicitly identifies itself as:

`operation_receipt_not_evidence_or_session_head_authority`

The receipt does not echo:

- selected source text;
- the human rationale text;
- source-authentication claims;
- semantic-support claims;
- chronology or trusted-time claims; or
- current/latest/head authority.

## Executable proof

Executable head:

`ecadac6923d3464b0e34319400c4cf82d3771a1c`

passed the full Repository Zero matrix on both push and pull-request workflows:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

Push run: **2101**  
Pull-request run: **2102**

The executable proof demonstrates:

1. one valid 49A bare selection creates exactly a v2 working set and v2
   working-set note;
2. the exact freshly relinked bare member survives through public 20A, fresh 21C,
   and the 51C controller;
3. the receipt derives root identity from fresh reopening and omits rationale and
   selected source text;
4. a wrong capture for the saved selection fails before either destination exists;
5. whitespace-only rationale fails through public 21A before the first durable
   write;
6. same resolved output path fails before mutation;
7. missing working-set parent fails before mutation;
8. missing note parent fails before mutation;
9. an existing working-set destination remains unchanged and prevents note creation;
10. an existing note destination remains unchanged and prevents working-set creation;
11. a simulated note-stage failure after valid working-set persistence leaves that
    working-set artifact intact and emits no success receipt;
12. a simulated fresh-21C failure after persistence emits no false success receipt;
13. no new durable format is introduced; and
14. the CLI surface contains no browser control, discovery, revision, continuation,
    declaration, sequence, or current/latest/head option.

## Scope

51D adds only:

- one narrow `research-start` CLI composition module;
- wiring into the existing top-level CLI;
- focused executable proof; and
- this milestone record.

It changes no existing browser authority, 16C/49B relink semantics, 20A/20B evidence
contract, 21A/21B note contract, 21C relink contract, or 51C application semantics.

It adds no Textual initial-session UI, fresh-process restart locator, revision UI,
ordinary-session adoption, browser acquisition, citation model, project container,
search/index, rollback transaction, or global session pointer.

## Stop boundary

51D proves only creation:

```text
one explicit saved bare selection
+ one first human rationale
→ existing durable working_set.v2
→ existing durable working_set_note.v2
→ fresh public 21C proof
→ 51C initial governed application state
```

The next product review should follow the next actual researcher action:

> After process exit, what is the minimum explicit-path product surface that freshly
> reopens this initial root without prematurely introducing a locator/configuration
> file or promoting filesystem location into current/latest/head authority?
