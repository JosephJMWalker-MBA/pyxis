# Milestone 44A — Explicit changed-evidence-basis preparation surface

Decision: **D218**

## Product question

Pyxis already proved the changed-working-set application sequence:

```text
33A / D177
exact governed declared endpoint
+ exact already-loaded appended evidence
+ explicit new human rationale
→ durable changed working set + working-set note

33B / D178
explicitly choose to cross onto that prepared basis

34A / D179
create the first distinct revision root above that cross-working-set transition
```

The next product question is intentionally smaller than adoption:

> Can the researcher visibly prepare a changed evidence basis from inside the governed research product without silently crossing onto it or manufacturing another root/epoch?

44A answers **yes for preparation only**.

## Decision D218

One already-governed `ResearchSessionShell` may be explicitly configured, before mounting, with one or more exact already-loaded/relinked 17D/18D/19D application evidence objects.

The shell then exposes one optional preparation form that lets the researcher:

1. inspect those exact appended candidate members;
2. write one exact new human rationale over the changed evidence basis;
3. supply one explicit no-overwrite working-set destination;
4. supply one explicit no-overwrite working-set-note destination; and
5. persist the prepared basis through the already-proven public 33A boundary.

Successful preparation does **not** alter the mounted controller, its declared endpoint, its declared sequence, or any root/epoch lineage.

## Candidate evidence is visibly not declared evidence

44A adds the application projection:

```text
ChromiumResearchChangedBasisCandidatePresentation
```

with mode:

```text
read_only_candidate_appended_research_evidence
```

and role:

```text
candidate_not_yet_working_set_or_adopted
```

The projection contains:

- the current declaration record SHA-256;
- the exact declared endpoint SHA-256 against which the candidate was configured;
- candidate member count; and
- read-only member/excerpt presentations for the exact explicitly supplied loaded items.

It deliberately contains no:

- declared revision position;
- revision-edge identity for the candidate;
- transition record;
- root identity;
- epoch identity;
- adoption state;
- current/latest/head field.

The visible Textual surface says:

```text
CANDIDATE APPENDED MEMBERS — NOT YET WORKING SET / NOT ADOPTED
```

Therefore:

```text
current declared working set
!=
candidate appended members
!=
prepared changed basis
!=
adopted changed basis
```

## Already-loaded evidence boundary

44A does not add candidate-evidence discovery.

`configure_changed_basis_candidate(...)` accepts only exact in-memory items already accepted by the 20A/33A contracts. It performs no:

- sidecar loading;
- directory scan;
- digest search;
- file picker;
- filename inference;
- Chromium acquisition;
- browser navigation;
- CLI locator parsing.

The candidate projection re-establishes the supplied item sequence through the existing 20A constructor and reuses the established read-only member/excerpt projection facts.

An already-loaded item therefore remains presentable even if its original sidecar is no longer available, matching the authority already proven by 33A.

This proves only loaded application coherence, not fresh durable re-entry of that member.

## Human rationale remains explicit

The preparation form begins with one blank `TextArea` for the new rationale.

The previous declared rationale is not copied, suggested, or inherited.

The existing 33A boundary remains responsible for requiring nonblank explicit human text and preserving the submitted text verbatim.

Thus:

```text
old rationale exists
!=
permission to place it on a changed evidence basis
```

## Paths remain explicit operational context

The two persistence inputs begin blank:

```text
prepared working-set destination
prepared working-set-note destination
```

The shell does not prefill, discover, infer, remember, or select either path.

Persistence delegates directly to:

```python
persist_chromium_research_session_working_set_extension(...)
```

so 33A retains ownership of:

- destination parent validation;
- distinct-path validation;
- no-overwrite behavior;
- 20B working-set persistence;
- 21B working-set-note persistence;
- exact appended-member identity/order;
- exact new rationale.

A path remains a location, not research identity or authority.

## Successful preparation remains unadopted

After successful save, the old form locks and shows:

- prepared working-set SHA-256 and destination;
- prepared working-set-note SHA-256 and destination; and
- explicit text that the displayed governed session is unchanged and the prepared basis is not transitioned/adopted/current/latest/head.

The shell additionally proves that the 33A result retains:

- the exact candidate-bound prior endpoint object;
- the exact candidate-bound prior session presentation;
- the exact appended item object identity/order; and
- the same mounted research controller.

No 33B transition button or 34A root action is mounted.

## Staleness is explicit

A candidate is bound at configuration time to:

```text
exact shell controller
+ exact controller.declared_endpoint object
```

That prevents one candidate form from silently changing meaning while it remains visible.

### Unadopted endpoint revision

An ordinary 29A successor write does not replace `controller.declared_endpoint`.

Therefore it does **not** stale 44A candidate preparation.

This matches the existing 33A rule:

```text
last successful endpoint write
!=
adopted reasoning state
!=
evidence-extension basis
```

### Adopted rollover

A successful 30A rollover replaces the shell's governed controller and declared endpoint.

Before the visible shell advances, any unsaved 44A form is locked and marked stale with explicit wording that it will not be silently retargeted.

A researcher must configure new candidate evidence against the newly governed session rather than accidentally carrying an old candidate action across an adoption boundary.

If the candidate was already successfully persisted, its success receipt remains a truthful historical statement about the earlier prepared basis and is not rewritten as stale or current.

## Product integration boundary

44A adds only an opt-in method on the existing base shell:

```python
configure_changed_basis_candidate(...)
```

No constructor or CLI entry changes are required.

Therefore ordinary, root-backed, second-epoch, and third-epoch shell types may retain their established stronger launch/re-entry/inspection semantics while inheriting the same preparation-only capability. The candidate configuration itself adds no lineage authority.

Default shells that are not explicitly configured mount exactly the pre-44A research controls and no changed-basis form.

## Why 44A stops before transition

33B and 34A are real, proven lower-level operations, but exposing them generically across every current shell would assert more product semantics than Pyxis has earned.

In particular, a generic “adopt changed basis” action launched from the currently concrete third epoch could silently become a fourth evidence-basis epoch by implementation symmetry alone.

44A refuses that jump.

The next milestone must separately decide which already-proven concrete lineage family, if any, may own a visible transition/adoption action and how that action proves its resulting ancestry.

Therefore:

```text
ability to prepare changed basis everywhere
!=
authority to adopt changed basis everywhere
```

## Prior art and reuse

The frontier review preceding 44A already compared adjacent mature provenance models including W3C PROV/PROV-O, RO-Crate, and event sourcing.

Those models remain useful interoperability/reference patterns, but none replaces Pyxis's explicit-locator, locally proven, non-global-head authority model end to end. Importing generic DAG/event-log semantics would risk granting chronology or history assumptions Pyxis deliberately does not infer.

Internal prior art is decisive for 44A:

- 33A owns changed-basis preparation semantics and persistence;
- 29A/30A prove the difference between successful write and explicit adoption;
- `ResearchSessionShell` already owns visible explicit-path mutations;
- prior Pyxis UI decisions keep proposed/candidate state visibly separate from current evidence.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Falsifiability

Focused 44A coverage proves:

1. candidate presentation preserves supplied order, duplicates, member notes, and bounded excerpts;
2. candidate presentation has no declared-position/transition/root/epoch fields;
3. an already-loaded candidate remains presentable after its source note sidecar is removed;
4. configured candidate object identity/order is retained by the shell;
5. visible rationale and both destination inputs begin blank;
6. candidate UI is explicitly labeled not-yet-working-set / not-adopted;
7. successful save delegates to 33A and preserves exact rationale plus exact explicit destinations;
8. successful preparation leaves the mounted controller/session/declared endpoint unchanged;
9. successful preparation locks the old form and shows both durable output identities/locations;
10. an unadopted endpoint successor write does not stale the candidate;
11. a successful ordinary rollover visibly stales and disables an unsaved candidate form;
12. the stale form is not silently rebound to the continuation controller;
13. no transition/adoption controls are introduced; and
14. an unconfigured default shell mounts no 44A surface.

The existing 33A application suite remains the stronger behavioral authority for working-set/note persistence semantics. The existing standalone/root/epoch shell suites remain regression authority for their already-earned research behavior.

## Non-authorities

44A adds no:

- 33B transition productization;
- 34A root creation;
- fourth evidence-basis epoch;
- generic `epoch[n]`;
- arbitrary-depth ancestry;
- generic shell lineage;
- generic authority inspection;
- candidate file discovery or resolver;
- CLI candidate-evidence locator;
- browser acquisition/navigation;
- automatic adoption;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship, authenticity, or trusted-time authority;
- semantic support or citation authority;
- autonomous research behavior.

## Acceptance statement

If the complete supported test matrix succeeds, 44A permits only this statement:

> Pyxis can visibly prepare and durably persist one explicitly changed research evidence basis from exact already-loaded candidate evidence inside the governed research product while keeping candidate evidence distinct from declared evidence, retaining the mounted session unchanged after preparation, and refusing to silently retarget an unsaved candidate across a later explicit session rollover. The prepared basis remains unadopted and grants no new root/epoch, discovery, chronology, semantic, or head authority.
