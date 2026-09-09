# Milestone 51B — interactive exact-passage save from one durable capture

Decision: **D282**  
Issue: **#295**  
Pull request: **#296**

## Concrete researcher action

51A closes the supported browser-to-capture entry seam:

```text
already-open caller-owned Chromium page
→ research-capture
→ durable research_capture.v1
```

50Y already closes the exact durable save seam when the researcher knows coordinates:

```text
explicit durable capture
+ paragraph ordinal
+ Unicode [start,end) offsets
→ research-save-selection
→ durable 49A bare-selection sidecar
```

The remaining product friction was therefore not a missing evidence model.

It was one human coordinate-entry action:

> Open one explicit durable Pyxis capture, inspect only its bounded returned paragraph
> evidence, directly select one exact returned text range, and save the unchanged 49A
> sidecar without manually calculating paragraph ordinals and Unicode offsets.

## Reuse review

No new browser reader, selector model, application selection type, or durable format is
required.

Existing public boundaries already own the semantic path:

```text
explicit capture path
→ public 16C load_chromium_page_research_capture()
→ exact loaded bounded paragraph evidence
→ public 17A select_chromium_research_capture_paragraph()
→ public 18A select_chromium_research_paragraph_text()
→ public 49A persist_chromium_research_paragraph_text_selection()
→ public 49A verify_chromium_research_paragraph_text_selection()
```

51B adds only a direct human input surface over those unchanged boundaries.

## Product decision

Extend the existing command rather than create a second save command:

```text
pyxis research-save-selection \
  --capture <research_capture.v1> \
  --destination <new selection sidecar> \
  --interactive
```

The historical coordinate-explicit form remains supported:

```text
pyxis research-save-selection \
  --capture <capture> \
  --paragraph <ordinal> \
  --start <offset> \
  --end <offset> \
  --destination <sidecar>
```

Interactive mode and explicit coordinate arguments are mutually exclusive.

Without `--interactive`, all three coordinate arguments remain required together.

## Durable evidence is loaded before UI authority exists

The interactive path begins with public 16C:

```text
explicit capture path
→ strict capture verification
→ exact typed rehydration
→ ChromiumPageResearchLoadedCaptureEvidence
```

Only after that succeeds does the CLI lazily import Textual.

Therefore:

- missing or invalid capture evidence fails before UI launch;
- coordinate-explicit mode still requires no Textual import;
- the optional UI dependency remains outside Pyxis core behavior; and
- the UI never receives a live Chromium endpoint as its source authority.

## Bounded paragraph choice

The Textual surface receives the exact already-loaded 16C object.

Its paragraph picker contains only:

`source.bundle.paragraphs.paragraphs`

—the bounded returned paragraph tuple already present in the capture.

If the persisted observation reports more paragraphs than were returned, the UI states
that the collection is truncated.

It does not:

- reacquire omitted paragraphs;
- query Chromium;
- scan another capture;
- infer a paragraph from text;
- search by quote; or
- expand the capture's bounded evidence.

Each paragraph choice delegates to unchanged public 17A.

The app retains the exact resulting
`ChromiumPageResearchParagraphSelectionEvidence`.

## Read-only exact text surface

The selected paragraph's exact:

`paragraph.text_prefix`

is loaded into one Textual `TextArea` configured with:

`read_only=True`.

The UI displays whether the parent paragraph itself was text-truncated.

A researcher may select only text that is already present in that returned prefix.

51B does not expose or reconstruct text beyond it.

## Text identity veto

Before any Textual selection becomes public-18A evidence, the UI requires:

```text
TextArea.text == exact source paragraph.text_prefix
```

and also requires the TextArea still to be read-only.

This is a fail-closed coordinate-domain boundary.

Textual documents preserve one line-separator convention. A source containing mixed line
endings may therefore normalize when loaded into a TextArea.

If any such normalization changes the Python string, 51B refuses to derive coordinates
rather than silently selecting against a different representation.

## Textual location → Pyxis coordinate mapping

Textual selections are location pairs:

```text
(row, column) → (row, column)
```

and may run in either direction.

51B uses the Textual document's established:

`Document.get_index_from_location()`

for both endpoints.

It then sorts the two flat indexes into:

```text
start_offset < end_offset
```

and requires a non-empty range.

The UI also requires:

```text
TextArea.selected_text
==
source paragraph.text_prefix[start_offset:end_offset]
```

before calling public 18A.

The public 18A selector remains the final application authority for the exact range.

## Unicode coordinate compatibility

The durable 49A format records:

`offset_unit = unicode_code_point`.

The pre-existing Chromium paragraph reader already constructs bounded text with
JavaScript `Array.from(text)`, so supplementary-plane characters are counted/truncated
by Unicode code point rather than UTF-16 code unit.

Python string indexing used by public 18A is also code-point based.

Textual v8.2.8—the minimum version already allowed by Pyxis's `ui` extra—contains the
same `TextArea.selected_text`, read-only mode, and
`Document.get_index_from_location()` APIs used by 51B.

Focused proof covers:

- non-ASCII BMP characters;
- a supplementary-plane emoji;
- a combining mark;
- forward and reverse selections; and
- a selection crossing a line break.

No new offset convention is introduced.

## Exact UI seam identity

The interactive runner returns only:

`ChromiumPageResearchParagraphTextSelectionEvidence | None`.

The CLI additionally requires a successful returned selection to retain the exact 16C
loaded capture object supplied to that UI.

A valid 18A selection over another separately loaded capture—even one with matching
content—is rejected at this seam.

This keeps the interactive product path tied to the exact explicit operation input.

## Persistence remains unchanged public 49A

A successful UI selection is passed directly to the same persistence path used by
coordinate-explicit 50Y:

```text
exact public 18A object
→ public 49A persist
→ public 49A fresh verify
→ persistence/verification agreement checks
→ deterministic operation receipt
```

The durable format remains exactly:

`pyxis.chromium.research_paragraph_text_selection.v1`.

The receipt remains the same operation-boundary receipt and still excludes selected
source text.

No selected text, capture path, URL, endpoint, target ID, note, tag, citation metadata,
or semantic claim is added to the sidecar.

## No-overwrite and cancellation

The existing public 49A no-overwrite boundary remains authoritative.

Focused proof confirms interactive mode preserves pre-existing destination bytes if
persistence refuses an existing path.

Cancelling the Textual selection surface returns no selection, writes no sidecar, emits
no success receipt, and exits the command cleanly.

Cancellation does not create a durable event merely because the UI was opened.

## Executable proof

Executable head:

`6a72507963183872e48d97a0e0a80f630468b46b`

passed the full Repository Zero matrix on both push and pull-request workflows:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

Push run: **2076**  
Pull-request run: **2077**

The executable proof demonstrates:

1. coordinate-explicit 50Y behavior remains compatible;
2. interactive mode is mutually exclusive with explicit coordinate inputs;
3. partial coordinate mode fails before capture loading;
4. interactive mode freshly loads through public 16C before UI import;
5. coordinate-explicit mode never loads the Textual runner;
6. the app exposes only bounded returned paragraph evidence;
7. the displayed source text is read-only;
8. the app changes paragraphs through public 17A;
9. forward and reverse Textual selections map to the same public-18A range;
10. Unicode code-point coordinates survive emoji and combining-mark content;
11. multi-line Textual locations map to exact flat Python indexes;
12. empty selection fails closed;
13. editable or source-mismatched TextArea state fails closed;
14. mixed-line-ending normalization is refused if it changes exact source text;
15. the headless real Textual app can select a second returned paragraph and return the
    exact public-18A object;
16. the CLI rejects an interactive result retaining a different loaded capture;
17. interactive cancellation creates no file;
18. interactive no-overwrite failure preserves existing bytes; and
19. successful persistence remains unchanged public 49A.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

51B changes only:

- `research-save-selection` input parsing/orchestration;
- one lazily loaded Textual capture-selection surface;
- focused CLI proof;
- focused Textual/Unicode proof;
- this milestone record; and
- compact README continuity.

It changes no:

- public 16A browser acquisition;
- public 16B capture format;
- public 16C loading;
- public 17A paragraph selection;
- public 18A exact-range selection;
- public 49A durable format/persistence/verification;
- public 49B relinking;
- working-set format;
- changed-basis product;
- Chromium navigation authority; or
- source/citation semantics.

## Explicit stop boundary

51B proves only:

```text
explicit durable capture
→ bounded returned paragraph browse
→ direct human exact-range selection
→ unchanged 17A → 18A → 49A
```

Do not infer:

- browser-side highlighting;
- capture-and-select atomicity;
- live DOM selection;
- automatic source discovery;
- multiple or batch selections;
- note creation;
- automatic changed-basis launch;
- capture search/indexing;
- quote verification;
- citation export;
- fuzzy re-anchoring;
- current/latest/head authority; or
- semantic interpretation.

## Compact result

After 51B the supported human path is:

```text
already-open caller-owned Chromium page
→ research-capture
→ durable research_capture.v1
→ research-save-selection --interactive
→ durable bare-selection sidecar
→ research-shell --plan
   + explicit candidate capture
   + explicit candidate selection
→ fresh public 49B relink
→ established first changed-basis product
```

The remaining human no-Python entry path no longer requires manual paragraph/offset
arithmetic, while browser navigation and every stronger source/semantic judgment remain
outside the new authority.
