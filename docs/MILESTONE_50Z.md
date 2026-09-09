# Milestone 50Z — launch first changed-basis product from one saved bare selection

Decision: **D280**  
Issue: **#290**

## Concrete researcher action

50Y exposes the first supported bare-passage save action:

```text
explicit durable capture
→ explicit paragraph/range
→ research-save-selection
→ durable 49A bare-selection sidecar
```

The next researcher action is:

> Reopen one explicit ordinary governed research session, explicitly relink one
> already-saved passage to one explicit matching durable capture, and use that exact
> relinked passage as candidate evidence for the established first changed-basis
> product without writing Python.

## Reuse review

No new annotation, candidate, or changed-basis model is required.

Existing boundaries already own every part of the action:

```text
ordinary --plan
→ 31A fresh ordinary re-entry

explicit capture
→ public 16C loaded capture

explicit 49A sidecar + exact loaded capture
→ public 49B fresh verification + exact relinking
→ ChromiumPageResearchLoadedParagraphTextSelectionRecord

exact relinked bare record
→ existing 44A candidate support
→ existing 44A→44H first changed-basis product
→ established explicit root-backed typed handoff
```

49C already authorizes the relinked bare-selection record as a working-set member
family.

50B already makes changed-basis preparation version-aware for that member.

50E–50I and 44A–44H already prove the concrete first changed-basis product.

The existing 44H runner already preserves explicit handoff semantics.

Therefore 50Z adds only launch composition.

## Decision

Extend `pyxis research-shell` with one exact optional pair:

```text
--candidate-capture <research_capture.v1>
--candidate-selection <research_paragraph_text_selection.v1>
```

The pair is valid only with ordinary:

`--plan`

No candidate flags means the historical ordinary `research-shell --plan` path is
unchanged.

## Exact candidate pair

The flags are all-or-nothing.

Supplying only one fails before any artifact or UI launch is attempted.

Supplying the pair with any nonordinary entry family also fails before that entry
configuration is opened.

50Z does not infer a candidate capture from the selection sidecar's digest and does
not infer a selection from a capture.

## Fresh ordinary authority

For candidate mode, the command still begins with the established ordinary launch:

```text
explicit --plan
→ strict plan document load
→ public ordinary re-entry
→ exact ChromiumResearchSessionReentryResult
```

The candidate does not change or replace ordinary re-entry authority.

## Fresh source load

The explicit candidate capture is opened through public 16C:

`load_chromium_page_research_capture()`

This freshly verifies and rehydrates the caller-supplied durable capture.

No Chromium page is reacquired.

No URL, endpoint, target, current tab, directory, or latest capture is inferred.

## Fresh 49B relinking

The explicit candidate selection path is supplied to public:

`load_chromium_research_paragraph_text_selection()`

together with the exact 16C loaded capture.

Public 49B itself freshly verifies the 49A sidecar bytes, compares exact durable
capture identity, reconstructs public 17A paragraph selection, reconstructs public
18A range selection, and returns the typed loaded bare record.

The CLI does not trust caller-provided selection metadata or duplicate 49B validation.

A sidecar referencing another capture fails before Textual launch.

A file-valid coordinate that does not address the explicit bounded capture likewise
fails through the established 49B/17A/18A path.

## Exact candidate identity at the UI seam

The private CLI handoff seam accepts only exact:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

candidate type.

It lazily loads the established:

`run_first_changed_basis_root_backed_handoff_research_session_shell()`

runner and passes:

```text
exact ordinary re-entry object
+ one-member tuple containing the exact relinked bare record object
```

by identity.

The candidate is not copied, normalized, converted into a note, or wrapped in a new
CLI-specific representation.

## Existing 44A→44H product remains authoritative

Once launched, every changed-basis action remains owned by the existing product:

```text
44A preparation
→ 44B transition
→ root construction / first edge
→ explicit adoption
→ fresh 35B proof
→ 35C persistence
→ explicit 44H typed handoff
```

50Z auto-performs none of those actions.

The existing 44H runner still launches the root-backed receiver only after the
researcher explicitly chooses the already-established handoff action.

## Plain ordinary launch remains unchanged

Without the exact candidate pair:

```text
pyxis research-shell --plan <plan>
```

still calls the original ordinary research-session shell path.

No candidate UI, relinking, or changed-basis runner is introduced into that mode.

## Nonordinary launch families remain closed

50Z does not allow candidate injection into:

- root-backed overlay launch;
- root-backed continuation launch;
- second-basis epoch launch;
- second-basis continuation launch;
- third-basis epoch launch; or
- third-basis continuation launch.

Those product families retain their existing concrete entry semantics.

No generic "candidate on any lineage" abstraction is introduced.

## Optional UI dependency remains lazy

All plan loading, ordinary re-entry, capture loading, and selection relinking happen
without importing Textual.

The first changed-basis runner is imported only after those non-UI proof steps
succeed.

If the optional UI dependency is absent, the command reports the same
`pyxis[ui]` installation boundary rather than moving Textual into Pyxis core.

## No browser authority

Candidate mode works entirely from explicit durable files.

Focused proof confirms no live Chromium paragraph observation is invoked.

50Z adds no:

- target enumeration;
- current-tab inference;
- navigation;
- page acquisition;
- click/interaction authority; or
- browser mutation.

## Executable proof

Executable head:

`3671882bf8b402925388f379c2e675ce9a40a735`

passed Repository Zero on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

on both push and pull-request workflows.

The focused proof demonstrates:

1. one real 50Y-saved sidecar relinks against one explicit matching capture;
2. the exact public-49B record reaches the changed-basis launch seam by identity;
3. the exact ordinary fresh re-entry reaches the same seam by identity;
4. the private seam passes those exact objects to the established 44H runner;
5. plain ordinary launch remains unchanged;
6. partial candidate pairs fail before artifact/UI launch;
7. every nonordinary entry family rejects the candidate pair before UI launch;
8. explicit source mismatch fails inside public 49B before changed-basis UI;
9. candidate loading performs no live Chromium acquisition;
10. Textual remains a lazy optional dependency.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50Z changes only:

- thin CLI parsing/orchestration;
- one focused CLI composition proof;
- this milestone record; and
- compact README continuity.

It changes no:

- application-layer research type;
- 49A format;
- 49B relinking semantics;
- working-set format;
- changed-basis UI implementation;
- 35B/35C behavior;
- 44A–44H behavior;
- browser implementation; or
- authority-inspection format.

## Explicit stop boundary

50Z proves only:

```text
saved bare selection
+ explicit matching capture
+ explicit ordinary plan
→ fresh 49B relink
→ existing first changed-basis product
```

Do not infer:

- multiple candidate sidecars;
- candidate batching;
- automatic 44A persistence;
- automatic transition/root/adoption/re-entry/persistence/handoff;
- candidate injection into later lineage families;
- source discovery;
- browser highlighting or acquisition;
- selection indexing/search;
- quote/citation authority;
- generic Nth-basis launch configuration;
- current/latest/head authority; or
- semantic interpretation.

## Compact result

After 50Z:

```text
research-save-selection
→ durable 49A sidecar
→ research-shell --plan
   + explicit candidate capture
   + explicit candidate selection
→ fresh public 49B relink
→ exact bare candidate
→ established 44A→44H product
```

A researcher can now save one passage and carry it into the first governed
changed-basis workflow entirely through supported product surfaces.
