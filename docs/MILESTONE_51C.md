# Milestone 51C — initial governed session root over an existing loaded working-set note

Decision: **D283**  
Issue: **#300**  
Pull request: **#301**

## Research question

51B completes the supported no-Python path from one already-open caller-owned Chromium
page to one durable bare exact-passage selection.

50Z already proves that such a saved passage can enter the established first
changed-basis product when an ordinary governed research session already exists.

The remaining entry problem was earlier:

> What is the smallest truthful Pyxis application state for the first governed
> research session, before any revision history exists?

The architecture review in #299 explicitly tried to falsify the need for a new genesis
artifact before adding one.

## Falsification result — no genesis durable format is earned

Existing public boundaries already provide the complete durable root:

```text
explicit relinked research members
→ research_working_set.v1 or .v2
→ research_working_set_note.v1 or .v2
→ fresh public 20C + 21C relink
```

For a basis containing a bare `exact_range_selection`, the existing v2 pair already
retains:

- the exact caller-owned ordered evidence membership; and
- one exact human-authored rationale over that working set.

There is no predecessor revision because none happened.

Existing public 22A/22B then already own the next truthful event:

```text
loaded working-set note
+ genuinely different human wording
→ working-set-note revision
```

Public 22A rejects exact text equality because equality is not a revision event.

Therefore 51C adds **application state over existing evidence**, not a
`research_session_genesis.v1` file and not fabricated history.

## Initial-session presentation

51C adds:

`ChromiumPageResearchInitialSessionPresentation`

and:

`present_chromium_research_initial_session(...)`

The input is exactly one already-loaded public-21C
`ChromiumPageResearchLoadedWorkingSetNoteRecord`.

The presentation re-establishes retained in-memory coherence only. It checks the
note/working-set v1 or v2 format pair, retained parent record identity, note mode and
text, exact loaded working-set object attachment, working-set mode, and exact ordered
member identity.

It then reuses the established working-set member projection from declared
revision-edge presentation.

For a bare saved passage this preserves:

```text
member_kind = exact_range_selection
human_note_text = None
```

No note is invented merely because the member is presented inside a governed root.

## No history-shaped fields

The initial presentation intentionally contains only:

- presentation mode;
- note format and note-record SHA-256;
- working-set format and working-set-record SHA-256;
- exact human rationale text;
- working-set mode; and
- ordered existing member/excerpt presentations.

It contains no:

- declaration identity;
- edge identity;
- declared position;
- revision number;
- timestamp;
- predecessor;
- current/latest/head marker; or
- semantic source-support claim.

The word "initial" therefore names the application mount point supplied by the caller.
It does not claim globally earliest history.

## No file or browser I/O during presentation

The presentation boundary consumes the already-loaded 21C object only.

Focused proof deletes the working-set file, note file, and already-loaded member
sidecars after fresh 21C loading, then successfully rebuilds the initial presentation
and controller.

The bounded source excerpts remain available because the exact loaded application
objects retain them in memory.

No browser reacquisition, path lookup, digest search, source discovery, or durable
file read occurs.

## Initial-session controller

51C adds:

`ChromiumResearchInitialSessionController`

The controller retains:

- the exact supplied public-21C loaded root by identity;
- one immutable initial-session presentation; and
- an optional last successful first-revision persistence result.

Construction itself writes nothing and does not create a history event.

## First genuine revision

The controller exposes one narrow mutation:

`persist_first_revision(...)`

The caller must provide:

- genuinely different revised human text;
- explicit working-set source path;
- explicit prior-note source path; and
- explicit no-overwrite revision destination.

Revision semantics remain unchanged public 22A:

`create_chromium_research_working_set_note_revision(...)`

Durability remains unchanged public 22B, selected only from the mounted root's exact
format:

```text
working_set_note.v1 root
→ existing research_working_set_note_revision.v1 writer

working_set_note.v2 root
→ existing research_working_set_note_revision.v2 writer
```

The existing writer freshly relinks the durable predecessor before writing, including
exact ordered member identity checks.

51C adds no new persistence format.

## Mounted root does not self-promote

A successful first-revision write is returned separately as:

`ChromiumResearchInitialSessionFirstRevisionPersistenceResult`

The result retains:

- the exact prior initial-session presentation;
- the exact public-22A revision object; and
- the exact existing 22B persistence evidence.

The controller records that result as `last_revision`, but its mounted root and
presentation remain unchanged.

Persisting a successor therefore does not mean:

- adopt successor;
- current revision;
- head revision;
- continuation;
- revision edge;
- declared sequence; or
- ordinary-session transition.

Those remain separate authority actions.

## Executable proof

Executable head:

`51375e86548b302a95354559ce2578c7c2f35856`

passed the full Repository Zero matrix on both push and pull-request workflows:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

Push run: **2093**  
Pull-request run: **2094**

The executable proof demonstrates:

1. a public-21C v2 root containing a bare exact-range selection is accepted without
   conversion;
2. the exact loaded root object is retained by the controller;
3. bare member presentation preserves `human_note_text=None`;
4. the initial presentation exposes no declaration/edge/revision/current/latest/head
   field;
5. presentation succeeds after the durable working-set, note, and member files
   disappear;
6. one genuine v2 human wording change uses unchanged revision-v2 durability;
7. one genuine v1 human wording change uses unchanged frozen revision-v1 durability;
8. the exact prior 21C note remains the revision predecessor object;
9. exact text equality fails before a file is created;
10. a different but individually valid durable predecessor note fails before
    destination mutation;
11. an existing destination remains byte-for-byte unchanged on failure; and
12. a successful write leaves the mounted root presentation unchanged.

The documentation-complete head must pass the same matrix before merge.

## Scope

51C adds only:

- one initial-session presentation module;
- one initial-session controller module;
- focused executable proof;
- this milestone record; and
- compact README continuity.

It changes no durable evidence schema and no existing 20C, 21C, 22A, or 22B contract.

It adds no CLI, Textual surface, Chromium action, locator file, restart plan,
continuation, revision edge, declaration, sequence, or automatic session adoption.

## Stop boundary

51C proves only:

```text
fresh public-21C loaded working-set note
→ honest initial governed application state
→ optional first genuine revision through unchanged 22A/22B
```

The next review should follow the next actual researcher action:

> How is this root created and freshly reopened through supported product surfaces
> without making a locator/configuration file into stronger evidence authority?

Creation, durable restart configuration, UI, and later promotion into ordinary
revision-edge/declaration lineage remain separate earned boundaries.
