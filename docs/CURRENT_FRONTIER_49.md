# Pyxis Current Frontier — Milestones 49A through 49B

> **Continuity status — implementation through Milestone 49B / D247.**
> **Updated:** 2026-09-04
> This compact record does not replace milestone documents, implementation, tests, executed CI, or earlier frontier files.

## Read this after docs/CURRENT_FRONTIER_48.md

Milestone 48 completed the bounded changed-basis reuse review and deliberately stopped before inventing another authority layer.

Milestone 49 returned development to a direct researcher action:

> save one exact passage without first having to interpret it.

49A makes that exact range durable.

49B proves that the durable range can later be explicitly attached back to one caller-supplied matching source capture.

Together they create a narrow save → verify → relink lifecycle without quote copying, source discovery, fuzzy anchoring, or citation claims.

## Completed 49-series flow

verified loaded capture
→ explicit paragraph ordinal
→ explicit Unicode code-point text range
→ exact 18A in-memory selection
→ 49A deterministic no-overwrite selection sidecar
→ 49A file-local integrity verification
→ explicit caller-supplied loaded capture
→ 49B exact durable source-identity comparison
→ public 17A paragraph reconstruction
→ public 18A exact-range reconstruction
→ linked exact selection over supplied evidence

The two milestones deliberately separate:

file integrity

from:

source attachment validity.

## 49A / D246 — durable exact-range selection without note

Before 49A, an exact 18A range could become durable only as part of a later note-bearing artifact.

49A adds one dedicated format:

pyxis.chromium.research_paragraph_text_selection.v1

Its durable record contains only:

- source capture format;
- source bundle SHA-256;
- paragraph selection mode;
- paragraph ordinal;
- text selection mode;
- Unicode code-point offset unit;
- start offset;
- end offset;
- selection-record SHA-256.

It deliberately contains no:

- selected source text;
- quote prefix or suffix;
- page URL;
- Chromium endpoint;
- target ID;
- source capture path;
- note;
- tag;
- timestamp;
- citation metadata.

The persistence result retains the exact caller-supplied 18A selection object.

File-local verification checks canonical bytes, digest, format, and coordinate-domain shape only.

A self-consistent sidecar may therefore contain an end offset that does not address any actual supplied source and still pass 49A file verification.

That is intentional.

## 49B / D247 — explicit source attachment

49B adds the separate operation:

explicit loaded capture
+ explicit 49A sidecar path
→ fresh 49A verification
→ exact capture format + bundle digest match
→ reconstruct public 17A paragraph
→ reconstruct public 18A range
→ return linked typed record.

The resulting record retains:

- the exact fresh 49A verification produced during the load;
- a newly reconstructed 18A selection;
- the exact caller-supplied loaded capture through that selection's 17A parent.

No source is located by digest, URL, filesystem path, browser endpoint, target ID, current tab, or directory scanning.

## Content identity is not path identity

49A does not persist the source capture path.

49B can therefore relink a selection created from one durable capture location against explicitly supplied loaded evidence for the same exact bundle at another location.

Successful relinking proves the supplied content identity matches.

It does not promote the new path into durable identity.

## Failed coordinates remain visible failures

49B deliberately does not use selector fallback.

If a 49A sidecar is structurally valid but its paragraph or range coordinates do not address the supplied capture's bounded returned evidence, public 17A or 18A rejects.

Pyxis does not then try:

- nearby text;
- quote search;
- another paragraph;
- another capture;
- live Chromium;
- a current document;
- fuzzy re-anchoring.

This differs intentionally from annotation systems designed to keep annotations attached across changing document representations.

## Prior-art result

The W3C Web Annotation Data Model establishes half-open TextPositionSelector ranges and explicitly warns that positional selectors are brittle when a representation changes.

Hypothesis demonstrates broader anchoring that can combine Range, TextPosition, and TextQuote selectors and fall back among them.

Those systems establish mature selector and re-anchoring prior art.

Pyxis reuses the conceptual distinction between selector data and source attachment while choosing a narrower fail-closed model over immutable supplied evidence.

No end-to-end substitute was demonstrated for the exact Pyxis authority contract.

## Executed evidence

49A / PR #216 passed Repository Zero on Python 3.11, 3.12, 3.13, and 3.14 and merged as:

13224b60e38e181ae9f9de992de3edb90d917018

49B / PR #218 passed the same four-lane suite and merged as:

1d641e3fb90cacabac82963b294a7b7664e87cee

Neither milestone required a corrective commit after its submitted reviewed head.

## Existing downstream capabilities already compose with 49B

49B does not require a new note system.

Its reconstructed selection is an ordinary public 18A exact-range selection.

Therefore a caller who later decides to interpret the passage can already use the established exact-range note constructor and persistence flow.

Likewise, two explicitly relinked selections can already participate in the established exact-range comparison constructor.

The 49-series therefore does not duplicate note or comparison logic merely because the selection was persisted and reopened first.

This is an important reuse result.

## What 49A–49B do not add

The 49-series does not add:

- source authentication;
- authorship;
- trusted time;
- chain of custody;
- quotation certification;
- citation metadata;
- bibliographic resolution;
- semantic relevance;
- claim support;
- automated ranking;
- browser navigation;
- fuzzy anchoring;
- live-page equivalence;
- automatic source discovery.

Exact text selection remains provenance about what the caller chose from supplied evidence, not proof of what that evidence means.

## Strongest compact statement through 49B

> Pyxis can durably save one exact caller-owned paragraph text range independently from interpretation, verify that sidecar's own canonical integrity, and later explicitly relink it to one caller-supplied matching loaded capture by exact durable content identity and existing public paragraph/range reconstruction, while failing closed rather than discovering or fuzzy-reanchoring source evidence.

## Current product gap discovered by the 49 review

A new concrete question is now visible.

The established 20A research working set accepts three relinked, note-bearing record families:

- paragraph note;
- exact-range note;
- comparison note.

A bare 49B relinked exact-range selection is not currently a valid working-set member.

That means a researcher can now save and reopen several exact passages without interpretation, but cannot yet place those bare selections into the established ordered research working-set lifecycle unless each is first wrapped in a note-bearing artifact.

This is a genuine workflow distinction.

It is not automatically a defect.

The original working-set lifecycle was built around interpreted research records, and downstream presentation currently assumes each member has human-note text.

## Why the next step is not automatic

Simply adding a fourth member kind to pyxis.chromium.research_working_set.v1 would affect more than one type alias.

It would require an explicit compatibility decision across:

- 20A in-memory member validation;
- 20B durable member-kind validation;
- 20C explicit member relinking;
- working-set note persistence;
- revision and rationale presentation;
- Textual presentation of a member that intentionally has no per-member note;
- old-reader versus new-writer format expectations.

That is a product and format decision, not a mechanical extension.

Likewise, creating a separate selection-set format would duplicate much of the already-proven working-set machinery.

The correct next step is therefore a decision review, not immediate implementation.

## Next decision frontier

The strongest candidate researcher question is:

> Should explicitly relinked bare exact-range selections be allowed to participate directly in the established research working-set lifecycle before the researcher writes per-selection interpretation?

If the answer is yes, the design review must decide whether to:

1. extend the existing working-set contract and versioning safely; or
2. demonstrate a materially different job that justifies a separate selection-collection artifact.

The review should prefer reuse unless preserving the semantic distinction between uninterpreted selections and interpreted working-set members requires a separate boundary.

Before implementation, inspect external annotation/highlight collection models and the internal 20A–20C plus presentation dependencies.

Do not infer a 49C merely because a new letter is available.

## Other candidate actions that are not yet authorized

The following are plausible but not yet demonstrated requirements:

- public CLI commands for save/relink;
- a Textual highlight-saving surface;
- export to bibliographic citation formats;
- quote-verification authority;
- semantic claim-support modeling;
- live-page change detection;
- fuzzy re-anchoring.

Each would add a new authority or product surface and needs its own concrete researcher requirement and prior-art review.

## Authority boundaries still intentionally absent

Through 49B, Pyxis still does not infer or claim:

- a global current/latest source;
- source identity from path equality;
- source identity from URL equality;
- quotation truth from exact-range coordinates;
- citation correctness from capture metadata;
- semantic support from working-set membership;
- authorship or trusted time from hashes;
- browser interaction authority from observation capability;
- changed-document equivalence through fuzzy matching;
- automatic promotion from a saved selection into a working set or rationale.

## Continuity rule

For future development sessions:

implementation + executed tests + milestone record
> compact frontier continuity summary
> README/current-status wording.

Read the compact chain in order:

1. docs/CURRENT_FRONTIER.md
2. docs/CURRENT_FRONTIER_35_36.md
3. docs/CURRENT_FRONTIER_37_38.md
4. docs/CURRENT_FRONTIER_39_40.md
5. docs/CURRENT_FRONTIER_41_43.md
6. docs/CURRENT_FRONTIER_44.md
7. docs/CURRENT_FRONTIER_46.md
8. docs/CURRENT_FRONTIER_47.md
9. docs/CURRENT_FRONTIER_48.md
10. this file, docs/CURRENT_FRONTIER_49.md

If a compact summary conflicts with implementation, tests, executed CI, or milestone-specific records, inspect the stronger evidence before changing behavior.
