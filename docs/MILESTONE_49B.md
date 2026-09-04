# Milestone 49B — explicit exact-range selection relinking

Decision: **D247**
Issue: **#217**

## Concrete researcher action

49A made one exact 18A text-range selection durably storable without requiring a note.

Its deliberate stopping point was file-local verification.

49B answers the next researcher action:

> Given one durable exact-range selection and one explicit loaded source capture, prove that the selection actually attaches to that supplied evidence and reconstruct the exact range over it.

This is a source-attachment proof. It is not fuzzy re-anchoring, source discovery, quotation verification, or citation authority.

## Product boundary

Explicit caller-supplied loaded capture + explicit caller-supplied 49A sidecar path
→ fresh 49A file verification
→ exact durable capture-identity comparison
→ public 17A paragraph reconstruction
→ public 18A exact-range reconstruction
→ linked typed result.

Successful relinking is not source authentication, live-page equivalence, quotation certification, citation authority, or semantic support.

## Internal prior art

The existing exact-range-note loader already proves the intended fail-closed sequence for a note-bearing artifact:

explicit source + explicit sidecar path
→ fresh sidecar verification
→ source digest match
→ 17A paragraph reconstruction
→ 18A range reconstruction
→ typed relinked record.

The durable comparison-note loader applies the same principle to two ordered sources.

49B reuses those established public authority boundaries rather than inventing another anchoring engine.

## External prior art

The W3C Web Annotation Data Model defines TextPositionSelector as a half-open start/end selector and explicitly warns that positional selectors are brittle when the selected resource representation changes.

Hypothesis demonstrates a broader web-annotation anchoring strategy that can combine or fall back among Range, TextPosition, and TextQuote selectors.

49B deliberately remains narrower. Pyxis does not search an ambient document, infer a current page, try multiple selector families, copy quote text into the 49A artifact, fall back to fuzzy matching, or silently accept a changed representation.

The caller supplies exact evidence, and mismatch fails closed.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse the attachment concepts while retaining Pyxis's explicit supplied-evidence model.**

## Application boundary

49B adds:

src/pyxis/app/chromium_research_paragraph_text_selection_load.py

with public:

ChromiumResearchParagraphTextSelectionSourceMismatchError

ChromiumPageResearchLoadedParagraphTextSelectionRecord

load_chromium_research_paragraph_text_selection(...)

## Fresh sidecar verification

The caller supplies one selection_source Path.

The loader itself calls verify_chromium_research_paragraph_text_selection(selection_source).

The API does not accept a caller-constructed verification dataclass as a substitute.

This preserves the sequence:

persisted bytes → fresh 49A file-local verification → source attachment.

## Explicit source authority

The caller separately supplies one ChromiumPageResearchLoadedCaptureEvidence.

No source is discovered by URL, digest search, source path, directory scan, browser endpoint, target ID, current page, or latest/current/head semantics.

The supplied source object is the authority subject for relinking.

## Durable identity comparison

Before paragraph reconstruction, 49B verifies the supplied source retains:

- capture format pyxis.chromium.research_capture.v1;
- bundle SHA-256 with 64 lowercase hexadecimal characters.

The freshly verified 49A sidecar must reference the same capture format and exact bundle digest.

The digest comparison uses hmac.compare_digest, consistent with existing durable relinking boundaries.

A different bundle fails before coordinate reconstruction.

## Source path is not identity

49A deliberately does not persist the source capture path.

49B therefore permits a selection created from capture content at path A to relink against caller-supplied equivalent loaded evidence for the same exact bundle at path B.

The resulting 18A selection retains the exact caller-supplied path-B loaded capture object.

This demonstrates that content identity is not filesystem location.

## Public 17A reconstruction

After source identity matches, 49B calls the public select_chromium_research_capture_paragraph function with the verified paragraph ordinal.

This re-establishes the existing paragraph-selection boundary against the actual supplied capture.

It therefore inherits 17A fail-closed behavior for nonexistent observed paragraph ordinals, coordinates outside a bounded returned paragraph prefix, incoherent paragraph evidence, and unsupported source selection structure.

The reconstructed paragraph selection mode must equal the verified 49A mode.

## Public 18A reconstruction

49B then calls the public select_chromium_research_paragraph_text function with the verified start and end offsets.

This re-tests the durable range against the actual already-returned paragraph text evidence.

The reconstructed result must retain the verified text selection mode, Unicode code-point offset unit, start offset, and end offset.

A file-locally valid end_offset of 999 can therefore pass 49A verification and still fail 49B relinking.

That distinction is intentional.

## Linked result

49B returns immutable ChromiumPageResearchLoadedParagraphTextSelectionRecord with:

- verification: the exact fresh 49A verification result produced during this load;
- selection: a newly reconstructed public 18A result over the exact caller-supplied loaded capture.

The selection.selected_text property remains derived from the supplied capture evidence.

No selected text is copied into the linked record.

## What successful relinking proves

A successful 49B result proves:

1. the explicit 49A sidecar freshly passed canonical file-local verification;
2. its durable source capture identity matches the explicit supplied loaded capture;
3. its paragraph ordinal is valid in the supplied capture's returned evidence;
4. its Unicode code-point range is valid inside that returned paragraph text;
5. the reconstructed selection retains the exact supplied loaded capture.

## What it still does not prove

49B does not prove source authorship, source authenticity, trusted publication time, chain of custody, live-web equivalence, formal quotation status, bibliographic citation correctness, semantic relevance, claim support, or that a changed capture should be accepted.

## No selector fallback

If exact source identity or coordinates fail, 49B stops.

It does not try TextQuoteSelector, prefix/suffix matching, nearby text, another paragraph, another capture, live Chromium, URL lookup, or a current document.

This is a deliberate divergence from more forgiving annotation systems.

For Pyxis, failed exact attachment remains visible evidence of a mismatch rather than a reason to silently relocate the selection.

## Failure ordering

The implemented sequence is:

1. reject the wrong source authority family;
2. freshly verify the explicit 49A sidecar;
3. reject malformed supplied capture format or digest;
4. reject different durable capture identity;
5. confirm verified selector modes;
6. reconstruct public 17A paragraph;
7. compare reconstructed paragraph mode;
8. reconstruct public 18A range;
9. compare reconstructed range mode, unit, and coordinates;
10. return the linked result.

## Focused falsification

49B tests demonstrate:

- successful relinking retains the exact caller-supplied loaded capture;
- selected text is derived from that supplied capture;
- the fresh 49A verification is retained;
- a nonexistent source capture path is never read;
- the same exact content identity can relink from a different filesystem location;
- wrong source authority family rejects;
- malformed supplied bundle digest rejects;
- different valid bundle digest rejects;
- unsupported supplied capture format rejects;
- a tampered sidecar is freshly rejected before attachment;
- a recomputed file-valid out-of-source range passes 49A verification but fails 49B reconstruction;
- a recomputed file-valid unknown paragraph ordinal fails against supplied evidence;
- bounded returned paragraph evidence is not expanded;
- unsupported persisted selector mode fails during fresh 49A verification;
- public pyxis.app exports expose the new boundary.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49B changes no 49A persistence format, 49A persistence semantics, 49A file-local verification, 16A–16C capture behavior, 17A paragraph selection, 18A range selection, note/comparison artifacts, browser behavior, working-set behavior, governed research continuity, CLI, or UI.

## Non-goals

49B adds no new persistence format, source discovery, source path inference, URL lookup, browser acquisition, live-page comparison, quote-text persistence, TextQuoteSelector, fuzzy matching, selector fallback, automatic re-anchoring, note/comment/tag, citation export, quotation verification, semantic-support claim, authorship/authenticity/trusted-time claim, CLI command, or Textual surface.

## Next boundary

49A + 49B now provide:

save exact passage → verify saved selection file → explicitly relink exact passage to supplied evidence.

The next milestone should not automatically add citation or semantic-support authority.

A subsequent researcher-facing step must be justified separately.

One plausible question is whether a researcher needs a durable collection of independently saved exact selections before interpretation, but that should be demonstrated as an actual workflow need rather than inferred from numbering.

## Acceptance statement

49B permits only this statement:

> One freshly verified durable exact-range selection can be explicitly relinked to one caller-supplied matching loaded capture by exact durable source identity and public paragraph/range reconstruction. Pyxis fails closed on source or coordinate mismatch and does not discover, fuzzy-reanchor, quote-certify, cite, or semantically interpret the selection.
