# Milestone 44F — Explicit Root-Backed Fresh-Process Re-entry Verification

Decision: D223

## Product question

44E / D222 explicitly adopts the first changed-basis lineage as this running shell's
35A governed session.

That action deliberately clears ordinary re-entry authority:

```text
44E governed-session adoption
!=
35B fresh-process root-backed re-entry
```

35B / D182 already proves that one root-backed session can be reconstructed in a new
process from an exact prior ordinary 31A plan plus explicit appended-evidence,
changed-basis, root, edge, and declaration locators.

44F asks the next product question:

> Can the researcher explicitly supply those current durable locators from the first
> changed-basis product surface and prove that the exact 44E adopted session is
> reconstructable, without persisting restart configuration yet and without replacing
> whatever governed controller is currently mounted?

44F answers **yes**.

## Core relationship

```text
exact successful 44E adoption
+ exact retained initial ordinary 31A plan
+ explicit appended-member locators
+ explicit changed 20B working-set path
+ explicit changed 21B note path
+ explicit 33B transition path
+ explicit 34A root path
+ explicit first 34B edge path
+ explicit 26B declaration path
→ existing 35B typed plan
→ public 35B fresh reconstruction
→ exact 44E lineage comparison
→ locked verification receipt
```

44F does not introduce a new re-entry plan type or persistence format.

## Why 44F does not persist 35C yet

The 35B plan is intentionally in-memory operational configuration.

35C / D183 separately proves a durable overlay:

```text
pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1
```

but its public persistence boundary requires an already-earned
`ChromiumResearchRootBackedSessionReentryResult` and then re-proves that state before
writing.

Combining 35B verification and 35C persistence into one opaque product action would
hide a real authority boundary already established by the application layer.

Therefore:

```text
44F verify fresh-process reconstructability
!=
44G persist durable root-backed overlay
```

44F has no destination input and writes no restart artifact.

## Retained prior ordinary plan

The first-changed-basis shell lineage begins from an exact
`ChromiumResearchSessionReentryResult`.

The 44-series product retains that launch evidence as:

```text
initial_ordinary_reentry
```

44E later sets the active shell field:

```text
research_reentry = None
```

when the changed-basis controller is adopted. That clearing remains correct: the new
root-backed session has not yet earned restart authority.

44F uses only:

```text
initial_ordinary_reentry.plan
```

as the 35B `prior_session_plan` because it is the exact caller-owned ordinary launch
plan retained by the concrete first-basis product lineage.

This does not make the old plan the active plan for the new session.

## Explicit appended-member locators

Successful 44A preparation already retains the exact appended loaded evidence items in
caller order.

Those application objects determine only which explicit locator fields are necessary:

```text
paragraph note
→ capture_source
→ note_source

exact-range note
→ capture_source
→ note_source

comparison note
→ first_capture_source
→ second_capture_source
→ note_source
```

Every path field begins blank.

No capture/note path is copied from retained verification evidence into the form. The
researcher explicitly supplies the current durable location for every input.

Appending the same loaded evidence more than once remains representable because field
sets are rendered by tuple position, not deduplicated identity.

Thus:

```text
record family determines input shape
!=
record receipt determines locator value
```

## Explicit changed-basis locators

44F also requires six blank path inputs:

1. changed working-set source;
2. changed working-set-note source;
3. 33B transition source;
4. 34A root source;
5. first post-root ordinary edge source; and
6. root-backed declaration source.

Successful 44A–44E output locations may be visible elsewhere as historical receipts,
but they are never copied into these controls.

No directory scan, digest search, sibling lookup, path inference, or current-file
selection occurs.

## Bounded application proof

The 44F application helper accepts exactly:

- one `ChromiumResearchFirstChangedBasisSessionAdoptionResult`;
- the exact initial ordinary `ChromiumResearchSessionReentryResult`;
- one ordered set of explicit appended-member re-entry locators; and
- the six changed-basis/root/declaration paths.

Before constructing 35B it checks that the initial ordinary re-entry still describes
the exact pre-change session retained by the first 44B transition.

It then delegates plan construction and reconstruction to public 35B.

After fresh reconstruction, 44F requires:

```text
fresh prior-session plan
== exact initial ordinary 31A plan

fresh root SHA-256
== exact 44C root SHA-256

fresh declaration SHA-256
== exact 44E declaration SHA-256

fresh endpoint edge SHA-256
== exact 44D first-edge SHA-256

fresh governed presentation
== exact 44E adopted governed presentation
```

These are bounded identity/coherence comparisons. They do not authenticate sources or
establish chronology.

## Fresh proof is not mounted state

The 35B operation constructs a new controller.

44F retains that controller only inside:

```text
ChromiumResearchFirstChangedBasisRootBackedReentryResult
```

The shell snapshots its currently mounted controller and session before verification
and requires those exact objects to remain mounted after successful proof.

Therefore:

```text
fresh reconstructed controller
!=
mounted governed controller
```

and:

```text
44F verification success
!=
automatic branch switch
```

The active shell's `research_reentry` remains `None`.

## Historical target remains stable across later rollover

The exact 44E adopted session is durable historical state.

After 44E, the researcher may perform an ordinary 29A revision and 30A rollover before
running 44F.

That later continuation changes the mounted controller, but it does not retarget the
44F controls. They retain the exact 44E adoption result that caused them to mount.

Thus the product may simultaneously hold:

```text
historical 44E adopted root-backed session
fresh 44F reconstruction proof of that session
currently mounted later 30A continuation
```

without claiming that any one is a global head or chronologically preferred branch.

## Textual behavior

44F is exposed only by the dedicated:

```text
FirstChangedBasisRootBackedReentryResearchSessionShell
```

which subclasses the concrete 44E shell.

Existing base, root-backed, second-epoch, and third-epoch shells are unchanged.

The 44F controls mount only after one new exact 44E adoption success.

The surface shows:

- exact root SHA-256;
- exact declaration SHA-256;
- exact first-edge SHA-256;
- appended-member count;
- each appended member's record family and human note text;
- blank locator fields appropriate to each member family;
- the six blank changed-basis locator fields; and
- an explicit verification button stating that the mounted session will not change.

After success, every locator input and the verification button lock.

The receipt states that fresh-process reconstruction succeeded, the mounted session was
unchanged, and no 35C overlay was written.

## Prior art and reuse

Internal prior art is decisive:

- 31A owns explicit ordinary-session locator plans;
- 35B owns root-backed typed plans and fresh reconstruction;
- 44E owns the exact first changed-basis adoption product evidence;
- 35C owns later proof-gated durable overlay persistence.

External workflow/reproducibility systems provide useful comparison points:

- Temporal resumes durable workflows through recorded Event History replay;
- Prefect maintains orchestrated flow-run state and resume/retry state through a
  server control plane;
- DVC restores versioned project/experiment state from Git/DVC metadata.

Those are mature solutions for their own models, but they rely on stronger ambient
history, run-state, or version-selection authority than Pyxis grants. Importing those
models as governing restart semantics would conflict with explicit caller-owned
locators, fresh local proof, and the absence of global latest/current/head authority.

Conclusion remains:

> **no end-to-end substitute demonstrated in this review**

## Authority boundaries

44F does not infer or claim:

- global current/latest/canonical head;
- complete history;
- chronology;
- branch preference;
- unique successor;
- path identity;
- locator discovery;
- digest-based lookup;
- source authenticity;
- authorship;
- trusted time;
- evidence relevance or completeness;
- semantic support for human rationale;
- citation authority;
- browser reacquisition;
- autonomous research;
- durable restart configuration;
- automatic relaunch; or
- active-controller replacement.

## Falsifiability

Focused 44F coverage proves:

1. the application helper freshly reconstructs the exact 44E state through public
   35B;
2. the fresh controller is a distinct application object whose governed presentation
   equals the exact 44E adopted presentation;
3. root, declaration, and endpoint content identities match the exact 44C/44E/44D
   lineage;
4. a moved appended capture works only through its explicitly supplied new path;
5. a wrong appended member rejects without creating any new restart artifact;
6. a wrong declaration rejects without creating any new restart artifact;
7. 44F controls are absent before exact 44E success;
8. paragraph-note field shape is rendered with blank capture + note locators and no
   comparison-only fields;
9. all six changed-basis locators begin blank;
10. there is no overlay destination control;
11. successful UI verification leaves the mounted controller/session unchanged and
    keeps `research_reentry` unset;
12. failure leaves the mounted controller unchanged and the form retryable;
13. an ordinary rollover after 44E does not retarget the historical 44F proof target;
14. successful verification after such rollover leaves the later continuation mounted;
15. a plain 44E shell never gains the 44F controls; and
16. no existing base/root-backed/epoch product surface is modified.

## Scope

44F adds only:

- `src/pyxis/app/chromium_research_first_changed_basis_root_backed_reentry.py`;
- `src/pyxis/ui/chromium_research_first_changed_basis_root_backed_reentry_textual.py`;
- `src/pyxis/ui/first_changed_basis_root_backed_reentry_research_session_shell.py`;
- focused application/UI tests;
- this milestone document; and
- the narrow `pyxis.ui` export for the dedicated shell/factory.

44F does not change:

- 31A/31B ordinary plan semantics;
- 35B re-entry semantics;
- 35C overlay semantics;
- 44A–44E product semantics;
- `ResearchSessionShell`;
- root-backed continuation shells;
- second-epoch shells;
- third-epoch shells;
- CLI;
- Chromium acquisition;
- research-control-plane state; or
- Repository Zero.

## What successful 44F proves

Successful 44F establishes only:

> From the exact first changed-basis product lineage through 44E, the exact retained
> ordinary 31A launch plan, and explicit current durable locators for every appended
> evidence member plus the changed working set, changed note, 33B transition, 34A
> root, first 34B edge, and 26B declaration, Pyxis can freshly reconstruct the same
> root-backed governed session through the existing 35B boundary and visibly retain
> that reconstruction as proof without replacing the mounted session, writing durable
> restart configuration, discovering files, or granting global
> head/chronology/semantic authority.
