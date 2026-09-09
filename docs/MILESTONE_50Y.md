# Milestone 50Y — CLI save one exact passage from one durable capture

Decision: **D279**  
Issue: **#288**

## Concrete researcher action

50X closes the long three-basis bare-selection continuity proof.

The next deliberately different researcher action returns to the entry point:

> Given one explicit already-persisted Pyxis Chromium capture, save one exact paragraph
> passage without writing Python and without first attaching interpretation.

Before 50Y, every application boundary required for that action already existed, but
there was no supported product command composing them.

## Existing authority path

The established application sequence is:

```text
explicit durable capture path
→ public 16C capture load
→ explicit 17A paragraph ordinal
→ explicit 18A Unicode code-point text range
→ public 49A no-overwrite selection persistence
→ public 49A file-local verification
```

50Y exposes exactly that sequence through one thin CLI action.

No validator or persistence rule is reimplemented by the command.

## Prior-art / reuse review

External annotation systems already establish the human workflow:

```text
select text
→ save highlight without note
→ interpret later
```

Hypothesis explicitly distinguishes a highlight from a note-bearing annotation.

Zotero likewise supports creating a highlight from selected text without requiring a
note.

The W3C Web Annotation model establishes zero-based half-open text-position selectors.

Those are strong precedents for the user action and coordinate model.

They are not substitutes for Pyxis's own:

- durable capture content identity;
- bounded returned evidence;
- exact 16C rehydration;
- fail-closed 17A/18A selection;
- no-overwrite 49A sidecar;
- file-local canonical verification; or
- later explicit source relinking.

Conclusion:

**no end-to-end substitute demonstrated in this review; reuse the existing Pyxis
boundaries rather than inventing another selection model.**

## Decision

Add one CLI command:

```text
pyxis research-save-selection \
  --capture <capture> \
  --paragraph <ordinal> \
  --start <offset> \
  --end <offset> \
  --destination <sidecar>
```

All five inputs are explicit.

## Capture input

`--capture` must identify one existing durable:

`pyxis.chromium.research_capture.v1`

file.

The command calls public:

`load_chromium_page_research_capture()`

so canonical bytes, SHA-256 self-integrity, typed rehydration, and bounded evidence
coherence remain owned by 16B/16C.

The command does not:

- discover captures;
- scan a directory;
- infer a URL;
- infer an endpoint;
- infer a target;
- connect to Chromium; or
- treat the capture path as durable source identity.

The resolved capture path appears only in the operation receipt as context.

## Paragraph input

`--paragraph` is a required 1-based integer.

The command delegates to public:

`select_chromium_research_capture_paragraph()`

No paragraph indexing, fallback, reacquisition, or semantic passage choice is
reimplemented in the CLI.

A paragraph outside the returned bounded evidence fails closed.

## Range input

`--start` and `--end` are required integer Unicode code-point offsets.

The command delegates to public:

`select_chromium_research_paragraph_text()`

The range remains zero-based and half-open:

`[start, end)`

A coordinate outside the already-returned paragraph text fails closed.

CLI syntax such as `True` or `False` does not parse as an integer coordinate.

## Persistence

`--destination` is an explicit no-overwrite path.

The command delegates directly to:

`persist_chromium_research_paragraph_text_selection()`

The durable format remains unchanged:

`pyxis.chromium.research_paragraph_text_selection.v1`

The sidecar continues to contain only:

- source capture format;
- source bundle SHA-256;
- paragraph mode + ordinal;
- text-range mode;
- Unicode offset unit;
- start/end offsets; and
- selection-record SHA-256.

It still contains no selected source text and no source capture path.

## Fresh post-write verification

After persistence succeeds, 50Y immediately calls public:

`verify_chromium_research_paragraph_text_selection()`

against the newly written path.

The CLI checks that persistence and fresh verification agree on:

- path;
- format;
- record SHA-256; and
- byte count.

This is a post-write operational consistency check.

It does not reopen the source or promote file-local verification into source-range
authentication.

## Deterministic receipt

Successful execution emits deterministic sorted JSON.

The receipt contains only:

- `receipt_role = operation_receipt_not_source_evidence`;
- resolved capture input path as operation context only;
- resolved selection output path;
- selection format;
- selection-record SHA-256;
- source capture format;
- source bundle SHA-256;
- paragraph ordinal;
- offset unit;
- start/end offsets; and
- byte count.

The receipt deliberately does **not** include:

- selected text;
- page body text;
- URL;
- Chromium endpoint;
- target ID;
- note text;
- tags;
- citation metadata; or
- semantic claims.

The receipt is not a second source-evidence representation.

## No browser authority

50Y works entirely from an existing durable capture.

It does not call any Chromium observation operation.

The command therefore adds no:

- browser discovery;
- navigation;
- target selection;
- live-page observation;
- current-tab inference; or
- browser mutation.

## Failure behavior

Focused proof establishes fail-closed behavior for:

- missing capture;
- invalid paragraph ordinal;
- range outside returned paragraph evidence;
- non-integer coordinate syntax;
- existing destination;
- invalid underlying capture/selection state.

An existing destination remains byte-for-byte unchanged.

Failures before persistence create no selection file.

## Thin-command delegation proof

A focused test replaces the public application functions with exact sentinels and
proves the command call order is:

```text
16C
→ 17A
→ 18A
→ 49A persist
→ 49A verify
```

The command does not recreate those contracts internally.

## Repository Zero proof

Executable head:

`ba72a133648107583efe5905aad231e9dc1e9009`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50Y changes only:

- the thin CLI;
- one focused CLI proof module;
- this milestone record; and
- compact README continuity.

It changes no:

- capture format;
- selection format;
- public 16C;
- public 17A;
- public 18A;
- public 49A;
- browser behavior;
- working-set behavior;
- governed-session behavior; or
- semantic authority.

## Explicit stop boundary

50Y proves only:

```text
explicit durable capture
→ explicit paragraph/range
→ durable bare selection sidecar
→ deterministic operation receipt
```

Do not infer:

- CLI capture acquisition;
- live browser highlighting;
- selection relinking command;
- automatic changed-basis candidate injection;
- batch selection;
- note creation;
- tags;
- search/indexing;
- quote verification;
- citation export;
- source discovery;
- fuzzy re-anchoring;
- current/latest/head authority; or
- semantic interpretation.

The next researcher-action review should ask how a researcher uses this saved sidecar
through a supported product surface.

## Compact result

After 50Y:

```text
pyxis research-save-selection
→ explicit 16C capture
→ explicit 17A paragraph
→ explicit 18A range
→ unchanged 49A sidecar
→ fresh unchanged 49A verification
→ deterministic operation receipt
```

The first bare-passage save action is now accessible without custom Python code.
