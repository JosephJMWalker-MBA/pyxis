# Pyxis Current Frontier — Milestones 35A through 36D

> **Continuity status — implementation through Milestone 36D / D189.**  
> **Updated:** 2026-08-25  
> This file is an additive continuation of `docs/CURRENT_FRONTIER.md`, which intentionally summarizes implementation through 34B / D180. It does not replace the milestone records, implementation, tests, or central architecture documents.

## Read this after `docs/CURRENT_FRONTIER.md`

The prior frontier ends with the durable relationship:

```text
33B cross-working-set transition
→ 34A revision root
→ 34B first ordinary edge
→ existing ordinary edge revision machinery
```

Milestones 35A–36D answer the next product question:

> Once a changed evidence basis has crossed back into ordinary edge lineage, can that root-backed ancestry become durable, restartable, repeatedly continuable, and usable from the standalone research product without collapsing path, identity, presentation, or authority boundaries?

The answer through 36D is yes, within the explicit boundaries summarized below.

## Current root-backed product flow

The implemented path now supports:

```text
changed evidence basis
→ 33B transition
→ 34A root
→ 34B first ordinary edge
→ 35A root-backed declared session
→ 35B fresh typed re-entry
→ 35C persisted root-backed restart overlay
→ 36A public research-shell launch
→ inspect / revise
→ explicit 30A rollover
→ 36B first 35D checkpoint
→ explicit user-chosen 36D in-process handoff
→ 36C cumulative continuation shell
→ revise
→ rollover
→ lock
→ 35E cumulative checkpoint
→ visibly adopt fresh cumulative controller
→ unlock
→ repeat
```

A process exit is also valid at the durable boundaries. The researcher can later relaunch explicitly from the saved 35C or 35D/35E overlay rather than using the 36D in-process handoff.

No step above creates a global latest/current/head relationship.

---

## 35A / D181 — Root-Backed Declared-Session Adoption

34B proved that ordinary edge revision can resume above a 34A root, but the existing explicit sequence/session machinery still assumed an ordinary edge predecessor at the beginning of a declared sequence.

35A extends only the explicit sequence start boundary:

```text
34A root
→ explicit first 34B edge
→ ordinary later edges
→ existing sequence declaration / verification
```

The 26A sequence loader can accept the 34A root as the explicitly supplied starting predecessor and dispatch the first hop through the dedicated 34B root-edge loader. Later hops return to the ordinary generic edge loader.

The existing durable sequence declaration format remains unchanged. The root format and SHA-256 identity can serve as the declared start identity without creating a second declaration schema.

35A does not make generic ordinary edge loading accept a root directly. The root-specific transition remains explicit and one-time.

## 35B / D182 — Fresh-Process Re-entry for Root-Backed Declared Sessions

35B makes a root-backed declared session reconstructable in a fresh process from explicit locators.

Its typed plan composes:

```text
explicit prior ordinary 31A plan
+ explicit appended working-set members
+ changed working-set / note locators
+ 33B transition locator
+ 34A root locator
+ explicit root-backed ordinary edge locators
+ declaration locator
```

Fresh reconstruction deliberately reuses the established public application loaders rather than trusting previously loaded Python objects.

The resulting root-backed re-entry retains both:

- the freshly reconstructed governed declared session controller; and
- the freshly reconstructed 34A root / changed-basis ancestry.

### Authority correction learned here

Two independently loaded objects may represent the same durable content identity without being the same Python object:

```text
same durable edge/root identity
!=
same Python object identity
```

Object identity is therefore not authority.

## 35C / D183 — Persisted Root-Backed Re-entry Overlay

35B's typed plan becomes durable through a small operational overlay:

```text
pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1
```

The overlay references the existing ordinary 31B plan document plus only the root-backed changed-basis locators needed to reconstruct the 35B plan.

It does not embed or duplicate the full ordinary plan schema.

Persistence is proof-gated. Before writing, Pyxis freshly decodes the referenced prior plan, reconstructs the candidate root-backed session, and verifies the earned session's governed presentation, endpoint durable identity, and root durable identity. The destination is no-overwrite and the written overlay must round-trip to the exact typed plan.

The overlay is operational configuration, not evidence, a branch pointer, or a head record.

## 35D / D184 — First Ordinary Continuation Above Persisted Root-Backed Ancestry

After a 35C session is reopened, a normal 29A revision plus 30A rollover creates a new ordinary continuation above the root-backed declared endpoint.

That new one-hop declaration does not begin at the 34A root. Rewriting the 35C overlay as though every later declaration were root-started would misrepresent the durable structure.

35D therefore introduces a compositional continuation overlay:

```text
pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1
```

with only:

```text
prior_root_backed_overlay_source
declared_edge_sources
declaration_source
```

Fresh re-entry resolves the explicit 35C overlay, freshly reconstructs the prior root-backed session, then relinks the explicitly supplied ordinary continuation declaration from that prior endpoint.

### Authority correction learned here

A different filesystem path does not imply a different durable session or edge identity:

```text
different path
!=
different durable content identity
```

Paths are locations. Durable record identity is content-bound evidence. Tests therefore accept path-distinct but content-identical evidence and reject genuinely different durable content.

## 35E / D185 — Cumulative Post-Root Continuation Checkpointing

Naively extending 35D could create recursive configuration:

```text
35C
→ 35D(E2)
→ 35D(E3)
→ 35D(E4)
→ ...
```

35E rejects that shape.

Instead every later continuation overlay keeps the same fixed direct 35C ancestry anchor while the ordinary post-root declared segment grows cumulatively:

```text
35C → E1
       ↓
       E2 → E3 → ... → En
```

The existing 35D overlay format is reused unchanged:

```text
prior_root_backed_overlay_source = same 35C overlay
declared_edge_sources = (E2, E3, ..., En)
declaration_source = new cumulative declaration
```

Older overlays and declarations remain durable and untouched. No 35D overlay points to another 35D overlay.

Checkpoint extension is proof-gated and no-overwrite. The full cumulative ordinary edge tuple is freshly relinked from the explicitly reconstructed root-backed endpoint, the chosen terminal continuation is verified, a new cumulative declaration is written, and the next existing-format overlay is freshly proven.

### Authority correction learned here

The one-hop rollover controller and cumulative re-entry controller intentionally present different declared segment shapes:

```text
same chosen terminal continuation
!=
same declared-segment presentation
```

For example:

```text
one-hop rollover:       E3
cumulative declaration: E2 → E3
```

Terminal equivalence is therefore proven by durable terminal edge identity plus exact human wording, not by whole-presentation equality.

---

## 36A / D186 — Public Root-Backed Research-Shell Launch

36A makes the established root-backed restart formats directly launchable through the public CLI.

The `research-shell` command accepts three explicit mutually exclusive entry families:

```text
--plan
--root-backed-overlay
--root-backed-continuation-overlay
```

Each path is interpreted only through its matching strict loader. The CLI does not guess the format, scan a directory, or select a head.

36A initially proves public launch and fresh reconstruction without adding new persistence semantics.

## 36B / D187 — First Root-Backed Continuation Checkpoint in Textual

A session launched from a 35C root-backed overlay retains its exact fresh 35B typed re-entry in a dedicated Textual shell.

After one explicit revision and 30A rollover, further revision is locked until the first root-backed continuation is explicitly checkpointed through the existing 35D application boundary.

The checkpoint form requires four blank caller-supplied locations:

1. current 35C overlay path;
2. current chosen successor edge path;
3. current one-hop continuation declaration path;
4. new no-overwrite 35D overlay destination.

The shell does not prefill launch-time or rollover-time paths as though earlier use established continuing location authority.

After successful 35D proof, revision remains locked. 36B by itself does not silently promote the session into cumulative mode.

## 36C / D188 — Repeatable Cumulative Post-Root Checkpointing in Textual

A session launched from a persisted 35D/35E overlay retains the exact typed continuation re-entry in a separate cumulative shell family.

After each explicit revision and 30A rollover:

```text
one-hop continuation mounted
→ revision lock
→ four blank 35E checkpoint fields
→ explicit 35E cumulative proof/persistence
```

The four fields are:

1. current 35D/35E overlay path;
2. current chosen successor edge path;
3. new cumulative declaration destination;
4. new continuation-overlay destination.

Every cycle starts blank. A prior path used or written by the shell is a fact about an earlier operation, not current path authority.

### Visible controller promotion

Successful 35E checkpointing must visibly adopt the fresh cumulative controller before revision can continue:

```text
one-hop mounted controller
→ successful 35E proof
→ remove one-hop presentation
→ typed lineage = result.fresh_reentry
→ live controller = result.fresh_reentry.controller
→ mount cumulative presentation
→ unlock next revision
```

This is necessary because the cumulative declared segment may be longer than the one-hop rollover presentation by design.

The loop is repeatable while keeping the same direct 35C ancestry anchor and without recursive overlay configuration.

## 36D / D189 — Explicit In-Process Handoff Into Cumulative Mode

36D removes unnecessary process ceremony between the first 35D checkpoint and the already-proven 36C cumulative shell without weakening explicit user agency.

After a successful 35D checkpoint, the 36B shell remains locked and exposes one explicit action:

```text
Continue in cumulative mode
```

If the researcher chooses it:

```text
exact successful checkpoint
→ exact checkpoint.fresh_reentry object
→ exit 36B Textual app with typed result
→ CLI validates type
→ launch existing 36C shell with that same exact object
```

No continuation overlay is reloaded during this handoff and no path text is reinterpreted.

A normal close returns no handoff and does not launch 36C. Successful persistence is therefore not automatic mode promotion.

The subsequent 36C checkpoint fields still begin blank, so transferring typed in-memory lineage does not convert an earlier path into persistent current-location authority.

---

## Four distinct concepts that must remain separate

The 35–36 milestone series repeatedly depends on keeping these concepts distinct:

### 1. Path

A filesystem location supplied for the current operation.

```text
path = location
```

A changed path does not necessarily mean changed durable content, and prior path use does not guarantee the artifact is still there.

### 2. Durable identity

Content-bound identity verified by the established record format and SHA-256 relationships.

```text
durable identity != authenticity / authorship / trusted time
```

SHA-256 self-integrity is not a signature or provenance authority beyond the relationships Pyxis actually verifies.

### 3. Typed in-memory lineage

A freshly reconstructed application result that has already passed the relevant public loader/controller boundary.

Typed lineage can be passed in-process when the product explicitly chooses to do so, as in 36D. It does not make the paths used to construct it permanently authoritative.

### 4. Presentation

A bounded view of verified application state.

Presentation shape can intentionally differ even when two controllers terminate at the same durable continuation. Presentation equality must therefore be required only where the semantics actually call for it.

---

## Current proven standalone behavior

Through 36D, the standalone research product can now do all of the following with explicit durable authority:

- freshly reopen an ordinary declared research session;
- revise its declared endpoint;
- persist a successor without automatically adopting it;
- explicitly roll over to a chosen continuation;
- save an ordinary restart plan;
- reopen a session whose lineage crossed a changed evidence basis through a 34A root;
- persist that root-backed restart configuration;
- publicly launch it through `pyxis research-shell`;
- checkpoint its first post-root ordinary continuation;
- explicitly hand that freshly proven continuation into cumulative mode without reloading it;
- reopen persisted post-root continuation overlays directly;
- repeatedly revise, roll over, checkpoint, and visibly adopt cumulative post-root declarations;
- preserve the fixed changed-basis/root ancestry while the ordinary post-root segment grows.

None of these capabilities creates ambient discovery or a global research head.

## Authority boundaries still intentionally absent

Through 36D, Pyxis still does **not** claim or infer:

- a globally current/latest/canonical research session;
- complete revision history;
- unique successor relationships;
- chronology from filenames, paths, or filesystem timestamps;
- semantic improvement between human rationale revisions;
- evidentiary support merely because a human note is attached to evidence;
- quotation/citation authority from exact-text selection alone;
- source authenticity, authorship, or trusted time from SHA-256 integrity;
- durable identity from path equality;
- distinct durable identity merely because two paths differ;
- authority from Python object identity;
- whole-presentation equality where only terminal continuation equivalence is required;
- browser navigation or autonomous interaction authority from read-only observation;
- research-control-plane escalation from prompt text or model output;
- research completion merely because a model or UI says research is complete.

These remain deliberate product constraints.

## Current decision frontier after 36D

The implementation frontier is **36D / D189**.

The root-backed continuation/restart product loop is now substantially closed. The next runtime milestone should therefore start from a new explicit product question rather than adding another wrapper to the same checkpoint path.

Structurally available questions include:

### A. Initiating another evidence-basis change from the standalone product

33A–34B establish the application boundaries for changing the working-set evidence basis, but the standalone research product still needs an explicit product decision about whether and how a researcher initiates that transition from an ordinary or root-backed live session.

Questions include:

- What explicit action owns preparation of the changed working set?
- Which artifact paths must be supplied blank/current rather than retained from earlier operations?
- At what point should ordinary revision controls lock?
- How does the UI distinguish "new evidence basis" from "ordinary rationale revision"?

### B. A second changed-evidence-basis transition above already root-backed ancestry

The first root-backed restart plan composes an ordinary prior 31A plan with one changed-basis/root region. A later evidence-basis change above an already root-backed cumulative continuation may require a new compositional ancestry model.

That should not be assumed to work merely because the live controller type is reusable.

### C. Machine-owned research control state

`docs/RESEARCH_CONTROL_PLANE.md` remains a design constraint, not an implemented control schema. A future milestone could choose to benchmark or implement typed application-owned research state, but prompt wording alone still cannot authorize it.

### D. Product usability around explicit paths

The current path discipline is intentionally strict. Future usability work may reduce typing ceremony only if it can do so without silently turning previously used locations into ambient authority.

None of these questions is authorized merely by appearing in this continuity document.

## Continuity rule

For future development sessions:

```text
implementation + executed tests + milestone record
> frontier continuity summary
> presentation wording
```

Read `docs/CURRENT_FRONTIER.md` first for 25B–34B, then this file for 35A–36D.

If a continuity summary ever conflicts with implementation, tests, or a milestone-specific decision record, inspect the stronger evidence before changing behavior.
