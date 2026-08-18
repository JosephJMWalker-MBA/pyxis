# Milestone 19D — Verified Comparison-Note Relinking

## Product question

Can Pyxis take one verified 19C durable comparison-note sidecar plus two explicit caller-supplied loaded captures and re-establish that the sidecar's ordered first/second range references actually address those supplied source-evidence objects before reconstructing the 19A comparison and 19B human note?

19D answers **yes**.

## Why this milestone exists

19C deliberately stopped at file-local integrity:

```text
first durable source/range reference
                     \
                      → human comparison + note → canonical sidecar
                     /
second durable source/range reference
```

A self-consistent 19C file could still contain a structurally valid but source-invalid coordinate such as `end_offset=999`.

19D adds the missing source re-establishment boundary:

```text
caller-supplied loaded capture A ──┐
                                   ├─ verify ordered durable references
19C comparison-note sidecar ───────┤
                                   ├─ reconstruct 17A → 18A on both sides
caller-supplied loaded capture B ──┘
                                   ↓
                         reconstruct 19A comparison
                                   ↓
                         reconstruct 19B human note
```

This closes the 19A–19D comparison durability loop without adding semantic comparison authority.

## Public API

```python
load_chromium_research_paragraph_text_selection_comparison_note(
    first_source,
    second_source,
    note_source,
)
```

returns:

```python
ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord(
    verification=<fresh 19C verification evidence>,
    note=<newly reconstructed 19B comparison note>,
)
```

The returned record is frozen.

## Fresh sidecar verification is mandatory

19D accepts the sidecar path, not a caller-prebuilt verification object.

Every load calls:

```python
verify_chromium_research_paragraph_text_selection_comparison_note(note_source)
```

before relinking.

Therefore a sidecar modified without a matching digest is rejected by the existing 19C integrity boundary before source matching or reconstruction begins.

## Both sources remain explicit

19D does not search for captures by:

- bundle digest;
- source path;
- URL;
- Chromium target ID;
- page title;
- paragraph text;
- selected text;
- note text.

The caller supplies exactly two `ChromiumPageResearchLoadedCaptureEvidence` objects.

Those are the only source-evidence candidates 19D considers.

## Ordered source identity

The durable 19C comparison contains distinct `first` and `second` roles.

19D preserves those roles.

For each side it requires:

```text
persisted capture format == supplied loaded-capture format
persisted bundle_sha256 == supplied loaded-capture bundle_sha256
```

The first persisted reference must match `first_source`; the second must match `second_source`.

Pyxis does not auto-swap them.

Thus:

```text
unordered set of two source identities
≠
recorded human-owned ordered comparison
```

If a sidecar records A→B and the caller supplies B→A, relinking fails even though both captures are individually available.

## Path remains location, not identity

As in 17D and 18D, the loaded capture's filesystem path is not part of durable content identity.

A capture may be supplied from a different path than the one it occupied when the comparison note was created.

If its retained 16B verification evidence has the same supported capture format and bundle SHA-256, the content-identity match may succeed.

19D does not read the capture path while relinking.

## Reconstruction reuses established public boundaries

After both durable source identities match, 19D reconstructs each side independently.

For each side:

```text
caller-supplied loaded capture
    ↓
17A select_chromium_research_capture_paragraph(...)
    ↓
18A select_chromium_research_paragraph_text(...)
```

Then:

```text
first reconstructed 18A range
             \
              → 19A create_chromium_research_paragraph_text_selection_comparison(...)
             /
second reconstructed 18A range
              ↓
19B create_chromium_research_paragraph_text_selection_comparison_note(...)
```

19D does not manually instantiate a comparison or note and does not duplicate 17A/18A/19A/19B validators.

The reconstructed selections retain the exact caller-supplied loaded capture objects and the exact already-returned paragraph objects selected from those captures.

## Falsifiability proof: 19C-valid `end_offset=999` fails here

The 19C acceptance seed becomes the 19D rejection proof.

A sidecar may be changed so that:

```text
second end_offset = 999
```

and then have its record digest recomputed and canonical JSON rewritten.

19C verification still succeeds, as designed.

19D then supplies the referenced second loaded capture and calls the public 18A range selector.

18A rejects the coordinate because it falls outside the already-returned paragraph text evidence.

Therefore:

```text
file integrity
≠
source-range validity
```

and:

```text
19C file verification
≠
19D source relinking
```

This is the principal authority distinction closed by the milestone.

## Same-source and same-selection comparisons remain legal

19A intentionally permits a researcher to compare one exact selection with itself without Pyxis judging significance.

19C can persist that comparison.

19D therefore permits the same loaded capture to be supplied as both `first_source` and `second_source` when both durable references identify that same capture.

It reconstructs both sides through the same public boundaries and does not infer whether self-comparison is useful.

## What successful relinking proves

Successful 19D loading proves only that:

1. the caller supplied two loaded capture-evidence objects in explicit first/second roles;
2. the comparison-note sidecar freshly passes 19C file-integrity verification;
3. the first durable capture identity matches the supplied first source;
4. the second durable capture identity matches the supplied second source;
5. each recorded paragraph ordinal is addressable through the existing 17A bounded-selection rule;
6. each recorded Unicode exact range is addressable through the existing 18A bounded-range rule;
7. the recorded 19A comparison can be reconstructed from those two validated ranges;
8. the recorded 19B note can be reconstructed with the persisted verbatim human text.

It proves **attachment coherence** between one durable human comparison note and two explicit supplied source-evidence objects.

## What successful relinking does not prove

19D does **not** prove:

- either source is authentic;
- either source is true or reliable;
- either capture came from a particular browser session;
- either capture path is authoritative;
- the human author is authenticated;
- when the comparison or note was created;
- chain of custody;
- that the passages are similar or different;
- contradiction, entailment, corroboration, or support;
- relevance or significance;
- that the note is correct;
- quotation or citation validity;
- source provenance beyond the already-retained Pyxis content identity;
- any machine agreement or interpretation.

Digest agreement remains content identity/self-integrity evidence, not authentication.

## Focused tests

Seven focused tests cover:

1. successful relinking of two distinct captures, preserving exact supplied capture objects, exact returned paragraph objects, selected text, and verbatim note;
2. successful relinking after both capture filesystem paths change while durable content identities remain the same;
3. rejection of swapped source order, unsupported source format, and wrong source type;
4. mandatory fresh 19C sidecar verification before relinking;
5. rejection of a file-valid recomputed-digest `second end_offset=999` when 18A re-establishes actual source bounds;
6. successful same-selection comparison relinking when the same capture is explicitly supplied twice;
7. public `pyxis.app` exposure.

## Explicit non-goals

19D adds no:

- automatic source discovery;
- capture-file reads or rehydration;
- browser acquisition, navigation, or control;
- comparison-note mutation or persistence changes;
- note revision history;
- similarity or distance scoring;
- contradiction, entailment, or corroboration detection;
- claim/support model;
- source ranking;
- relevance or confidence judgment;
- quotation/citation verification;
- source authentication;
- author identity or trusted timestamps;
- embeddings or LLM work;
- notebook, collection, or generic annotation framework;
- researcher UI.

## Decision — D142

**Pyxis may reopen one verified 19C durable comparison-note sidecar only when the caller explicitly supplies both loaded capture-evidence objects in the sidecar's recorded first/second order. The sidecar must be freshly verified from its path; each durable capture format plus bundle SHA-256 must match the corresponding supplied loaded capture; each paragraph and Unicode exact-range reference must then be re-established through the existing public 17A and 18A boundaries; and the human-owned comparison and verbatim human note must be reconstructed through the existing public 19A and 19B boundaries. Source order must not be auto-swapped, filesystem paths must remain location rather than identity, and the same source may occupy both roles when the durable record says so. A 19C-valid self-consistent sidecar containing an out-of-bounds coordinate such as `end_offset=999` must fail during 19D source-range reconstruction, proving again that file integrity does not establish source-reference validity. Successful relinking proves attachment coherence only; it does not establish source authentication, provenance verification, authorship, trusted time, quotation/citation validity, semantic relation, claim support, relevance, reliability, truth, or machine agreement. Source evidence, human selection, human juxtaposition, human interpretation, durable representation, and explicit source re-establishment remain separate authority layers.**
