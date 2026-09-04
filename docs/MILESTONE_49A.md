# Milestone 49A — durable exact-range selection without note

Decision: **D246**  
Issue: **#215**

## Concrete researcher action

After the 48-series bounded reuse pass, Pyxis stops treating code similarity as the default source of new milestones.

49A returns to a direct researcher action:

> Save this exact already-selected passage for later without forcing me to add interpretation.

Before 49A, Pyxis could create one exact 18A paragraph-text selection in memory, but durable storage of that range existed only inside later note or comparison-note artifacts.

49A makes the range itself durably storable.

## Product boundary

```text
explicit verified loaded capture
→ explicit paragraph ordinal
→ explicit Unicode code-point text range
→ exact 18A selection
→ explicit no-overwrite 49A selection sidecar
→ file-local verification
```

while:

```text
durable selection
!= human note
!= quotation verification
!= citation
!= semantic support
!= source discovery
!= re-anchoring
```

49A ends at file-local verification.

Explicit relinking to supplied source evidence remains a separate later authority action.

## Internal prior art

49A reuses already-proven Pyxis boundaries.

### 17A — explicit paragraph selection

17A selects one caller-specified paragraph ordinal from already-returned paragraph evidence retained by one exact verified loaded capture.

Selection does not upgrade paragraph text into quotation, relevance, truth, or citation authority.

### 18A — exact returned text range

18A refines one exact 17A paragraph selection using:

```text
zero-based
half-open
Unicode code-point
start/end coordinates
```

Its `selected_text` property is derived from the already-returned paragraph text prefix.

The selected source text is not stored as a second field.

### 18C — durable exact-range note

18C already proved that durable range coordinates can be represented using only:

- capture format;
- capture bundle SHA-256;
- paragraph selection mode and ordinal;
- text-range mode;
- Unicode offset unit;
- start/end offsets.

18C also proves an important negative boundary: a structurally valid sidecar is not by itself proof that its coordinates address supplied source evidence.

49A reuses that durable-reference discipline without the note layer.

## External prior art

The W3C Web Annotation Data Model establishes `TextPositionSelector` as a standard representation for a half-open text position range and distinguishes position selectors from selectors that copy quoted text.

Hypothesis provides a first-class highlight action that allows a user to save selected text without attaching a comment or tag. Its web-anchoring stack may combine position, quote, and range selectors to re-anchor against document representations.

Those systems establish that durable “highlight/save this passage” is a mature user action.

They do not replace this exact Pyxis boundary.

49A deliberately does not:

- anchor against an ambient live page;
- discover a current document representation;
- fuzzy-match or silently re-anchor;
- persist exact quote text or prefix/suffix context;
- infer source identity from URL;
- treat a stored range as a quotation, citation, or support claim.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse the selector concepts, not the external execution model.**

## Durable format

49A adds:

```text
pyxis.chromium.research_paragraph_text_selection.v1
```

implemented in:

```text
src/pyxis/app/chromium_research_paragraph_text_selection_persistence.py
```

The deterministic record is:

```text
format

selection_record:
  source_capture:
    format
    bundle_sha256

  selection:
    paragraph:
      mode
      ordinal

    text_range:
      mode
      offset_unit
      start_offset
      end_offset

selection_record_sha256
```

## Deliberately absent source text

The durable record does not serialize:

- the paragraph text prefix;
- the selected text;
- prefix/suffix quote context;
- element id;
- page title;
- page URL;
- Chromium endpoint;
- target id;
- source capture path.

This is intentional.

The sidecar preserves durable source-content identity plus exact caller-owned coordinates, not another copy of source evidence.

## Deliberately absent interpretation

49A also persists no:

- note;
- comment;
- tag;
- question;
- comparison;
- rationale;
- user identity;
- timestamp;
- citation metadata.

A researcher can therefore preserve a passage before deciding what it means or whether it supports anything.

## Persistence result

`ChromiumPageResearchParagraphTextSelectionPersistenceEvidence` is immutable and records:

```text
path
selection_format
selection_record_sha256
byte_count
selection
```

The `selection` field retains the exact caller-supplied 18A object by Python object identity.

## Live validation before write

Persistence requires exactly:

`ChromiumPageResearchParagraphTextSelectionEvidence`

Before writing, 49A delegates range validity back to public 18A:

```python
select_chromium_research_paragraph_text(
    selection.source,
    start_offset=selection.start_offset,
    end_offset=selection.end_offset,
)
```

The temporary result is validation only.

It does not replace the caller's selection object.

49A additionally requires that the retained loaded capture exposes:

```text
capture format:
pyxis.chromium.research_capture.v1

bundle SHA-256:
64 lowercase hexadecimal characters
```

## Persistence semantics

The caller supplies one `pathlib.Path` destination.

49A preserves the established Pyxis persistence contract:

- parent directory must already exist;
- destination is no-overwrite;
- output is canonical UTF-8 JSON;
- keys are sorted;
- compact separators are used;
- NaN is forbidden;
- exactly one trailing newline is written.

The SHA-256 covers the complete canonical `selection_record`.

It is file self-integrity evidence only.

It proves no authorship, authentication, trusted time, or chain of custody.

## File-local verification

49A adds:

```python
verify_chromium_research_paragraph_text_selection(source)
```

and immutable:

`ChromiumPageResearchParagraphTextSelectionVerificationEvidence`

Verification reads only the caller-supplied selection sidecar.

It verifies:

- UTF-8;
- JSON;
- exact top-level shape;
- supported format;
- lowercase SHA-256 shape;
- digest over canonical selection record;
- canonical complete file bytes;
- capture-reference shape;
- paragraph selection mode;
- positive paragraph ordinal;
- text selection mode;
- Unicode code-point offset unit;
- non-negative start offset;
- end offset greater than start offset.

## File-local verification is intentionally insufficient

A recomputed self-consistent sidecar may claim:

```text
end_offset = 999
```

and still pass 49A file-local verification if the sidecar is structurally valid and its digest matches.

That is not a defect.

49A verification has no source capture and therefore has no authority to decide whether offset 999 addresses actual supplied source evidence.

The separate future relinking boundary must re-test coordinates against explicit source evidence.

This keeps:

```text
file integrity
!= source attachment validity
```

visible in the product model.

## Public application exports

The application package exposes:

```python
ChromiumPageResearchParagraphTextSelectionPersistenceEvidence
ChromiumPageResearchParagraphTextSelectionVerificationEvidence
ChromiumResearchParagraphTextSelectionIntegrityError
persist_chromium_research_paragraph_text_selection
verify_chromium_research_paragraph_text_selection
```

No UI or CLI surface is added in 49A.

## Focused falsification

Focused tests demonstrate:

1. canonical no-overwrite persistence from one exact live 18A selection;
2. persistence result retains exact selection object identity;
3. selected source text is absent from persisted JSON;
4. source capture path is absent;
5. URL, endpoint, target id, and paragraph element id are absent;
6. note/tag/citation fields are absent;
7. capture format + bundle digest are the only durable source-content identity fields;
8. paragraph ordinal and Unicode range coordinates round-trip exactly;
9. existing destination is preserved;
10. missing parent rejects;
11. public 18A range validation is reused before write;
12. invalid source bundle digest rejects before write;
13. wrong authority family rejects;
14. digest mismatch rejects;
15. non-canonical but semantically equivalent JSON rejects;
16. malformed capture format/digest, paragraph mode/ordinal, range mode/unit, and coordinate domains reject;
17. verification succeeds without a source capture file;
18. a recomputed structurally valid out-of-source range can pass file-local verification, proving 49A does not silently claim source-range authentication;
19. public `pyxis.app` exports preserve the boundary.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49A changes no:

- browser observation;
- capture format;
- capture verification;
- loaded-capture behavior;
- 17A paragraph selection;
- 18A text-range selection;
- 18B/18C note behavior;
- comparison behavior;
- working-set behavior;
- governed research continuity;
- CLI behavior;
- UI behavior.

## Non-goals

49A adds no:

- source relinking or rehydration;
- source discovery;
- source capture read during verification;
- source path persistence;
- quote-text persistence;
- `TextQuoteSelector` representation;
- prefix/suffix quote context;
- fuzzy anchoring;
- automatic re-anchoring;
- note/comment/tag;
- edit history;
- citation export;
- quotation verification;
- semantic-support claim;
- authorship/authenticity/trusted-time claim;
- browser navigation or interaction;
- CLI command;
- Textual surface.

## Next boundary

If 49A is demonstrated, the next concrete question is intentionally separate:

> Can one freshly verified 49A sidecar be explicitly relinked to one caller-supplied matching loaded capture, with the persisted coordinates re-tested through the existing public 17A and 18A selectors?

That would be a source-attachment proof, not file-local verification.

It should not discover the source capture by path, URL, digest, browser state, or “current page,” and it should not fuzzy-reanchor or grant quotation/citation authority.

## Acceptance statement

49A permits only this statement:

> A researcher can durably save one exact caller-owned text range without adding interpretation. Pyxis preserves only durable source-content identity plus explicit paragraph/range coordinates, verifies the sidecar's own canonical integrity, and deliberately refuses to treat that file-local record as self-validating source, quotation, citation, or semantic-support authority.
