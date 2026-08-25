# Pyxis Current Frontier

> **Continuity status — implementation through Milestone 34B / D180.**  
> **Updated:** 2026-08-25  
> This file is a compact continuity layer over the milestone records. It does not replace `README.md`, `docs/CURRENT_STATE.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/DEVELOPMENT_ARCHIVE.md`, or any milestone document.

## Why this file exists

`README.md` and `docs/CURRENT_STATE.md` currently describe the high-level frontier only through Milestone 25A / D158 even though `main` has advanced through Milestone 34B / D180.

The large central documents are deliberately preserved rather than rewritten wholesale. This file closes the continuity gap without pretending that a summary is stronger authority than the implementation, tests, decisions, or milestone records it summarizes.

Use this file to answer one question quickly:

> What does Pyxis already prove after 25A, and where is the current decision frontier?

## Recommended read order for a new development session

1. `README.md` — product identity, authority philosophy, Repository Zero spine, and browser-research foundation.
2. `docs/CURRENT_FRONTIER.md` — compact map from 25B through 34B and the post-34B research control-plane design boundary.
3. `docs/MILESTONE_25B.md` through `docs/MILESTONE_34B.md` — authoritative milestone-specific implementation narratives.
4. `docs/RESEARCH_CONTROL_PLANE.md` — documentation-only boundary recorded after 34B; not a runtime milestone.
5. `docs/CURRENT_STATE.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, and `docs/DEVELOPMENT_ARCHIVE.md` when deeper historical or architectural context is required.

The central documents remain valuable foundations. Their older status headers should not be interpreted as evidence that later milestone work is absent.

## Current product shape

Pyxis now has two connected proven spines:

```text
architecture intent
→ canonical Workspace state
→ RIR
→ deterministic compiler
→ generated products
→ runtime evidence
→ governed architecture revision / export / verification
```

and:

```text
explicit caller-owned Chromium evidence
→ durable verified research capture
→ explicit human selections / notes / comparisons / working sets
→ durable rationale revisions
→ explicit ordered revision segments
→ inspectable governed research sessions
→ explicit mutation / continuation / restart
→ explicit evidence-basis change
→ ordinary revision resumed without erasing the basis-change ancestry
```

The second spine does not weaken the first. Pyxis still treats intent, canonical state, generated artifacts, observed evidence, human interpretation, durable references, and presentation as distinct authorities.

## 25B–26C — make revision continuity repeatable and durable

### 25B / D159 — Durable Persistence of a Loaded-Edge Extension

25B completes the repeatable ordinary revision loop after 25A. A human-authored revision that explicitly extends one already-loaded durable edge can be persisted using the existing general revision-edge format rather than creating another schema.

The important result is:

```text
loaded durable edge
→ explicit human revision
→ another ordinary durable edge
```

without introducing a parallel revision system.

### 26A / D160 — Explicit Ordered Revision-Edge Sequence Relinking

26A removes repeated caller ceremony when the researcher already knows the exact durable edges to reopen. The caller supplies one starting predecessor and an explicit ordered list of edge files; Pyxis relinks that declared sequence in one application operation.

Order remains caller-owned. Pyxis does not infer chronology, completeness, or a global history.

### 26B / D161 — Durable Explicit Revision-Edge Sequence Declaration

26B makes one explicitly reopened ordered segment durable. It preserves the researcher's declaration of starting identity and ordered edge identities without claiming that the segment is the only history, the complete history, or the current branch.

### 26C / D162 — Verified Explicit Revision-Edge Sequence Declaration Relinking

26C closes the restart loop for that declaration. A caller can supply the durable declaration plus the explicit application/file evidence being reopened now, and Pyxis verifies/relinks the declared segment rather than discovering history by scanning.

The governing pattern is:

```text
explicit durable declaration
+
explicit supplied evidence
→ verified reopened segment
```

not:

```text
filesystem contents
→ inferred history
```

## 27A–28B — make verified research sessions inspectable without semantic promotion

### 27A / D163 — Read-Only Presentation of a Verified Declared Revision-Edge Segment

27A introduces a bounded presentation object so UI code does not need to understand deep authority-bearing revision internals directly.

Presentation remains downstream of verified evidence. It does not invent labels such as "latest revision" or "current rationale."

### 27B / D164 — Independent Research Segment Textual Panel

27B renders the 27A presentation in the existing Pyxis Textual experience. The UI displays application-owned evidence rather than rediscovering or reinterpreting it.

### 27C / D165 — Read-Only Working-Set Context for One Declared Rationale

27C lets a researcher inspect the exact working-set context attached to one caller-selected declared rationale position.

This answers:

```text
What evidence context was this human rationale attached to?
```

It does not answer:

```text
Does that evidence prove the rationale?
```

### 27D / D166 — Textual Inspection of Attached Rationale Working-Set Context

27D makes that bounded working-set context visible inside the Textual shell, including the source context and human notes attached to the selected rationale position, without browser reacquisition or source-support inference.

### 28A / D167 — Complete Research Session Presentation

28A composes one immutable complete presentation from the verified declared rationale segment plus the bounded working-set context for each declared position. This removes caller-side assembly ceremony while keeping all underlying authority boundaries visible.

### 28B / D168 — Complete Research Session Textual Input

28B lets the Textual shell consume the complete 28A research-session presentation directly. Presentation composition becomes an application concern instead of UI reconstruction logic.

## 29A–32B — turn the evidence model into a governed restartable research product

### 29A / D169 — Research Session Declared-Endpoint Revision Controller

29A adds the first application-owned mutation action over a loaded declared research session.

The researcher explicitly chooses the declared endpoint they are continuing from, authors revised rationale, supplies the current endpoint file, and chooses a destination for the durable successor.

No global "current head" is inferred.

### 29B / D170 — Textual Declared-Endpoint Rationale Revision

29B exposes that explicit governed revision action in the Textual shell. The UI can now move from inspection into one deliberate human-authored mutation while preserving the same application boundaries.

### 30A / D171 — Explicit Continuation-Session Rollover

29A/29B intentionally stop after writing a durable successor. 30A adds the separate adoption decision: one successful successor may be explicitly chosen and rolled into a new durable declaration for continued research.

Writing a successor and adopting it are distinct actions.

### 30B / D172 — Textual Explicit Continuation-Session Rollover

30B exposes that explicit adoption/rollover action in the Textual workflow. The researcher can revise, persist, then deliberately adopt one successor rather than having a write silently become the new session authority.

### 31A / D173 — Explicit Durable Research-Session Re-entry

31A proves the governed loop can survive process exit. A fresh process can reconstruct one session from explicitly named durable artifacts without directory scanning, digest discovery, Chromium reacquisition, or a global-head model.

### 31B / D174 — Standalone Governed Research Shell + Public CLI Entry

31B turns that fresh-process capability into a public executable product surface:

```text
pyxis research-shell ...
```

The research workflow is no longer only a Python-library proof. It is directly launchable while retaining explicit locator and authority rules.

### 32A / D175 — Explicit Continuation Re-entry Plan

32A makes one explicitly chosen continuation restartable by constructing and proving a new locator plan for the next process entry.

The restart plan records explicit locations/identities. It does not authorize ambient discovery.

### 32B / D176 — Standalone Restart-Plan Checkpoint

32B closes the standalone shell loop by allowing the researcher to checkpoint a proven restart plan from inside the governed research experience.

By 32B the durable product loop is:

```text
launch from explicit plan
→ inspect
→ revise rationale
→ persist successor
→ explicitly adopt continuation
→ prove/save restart plan
→ exit
→ re-enter explicitly
```

## 33A–34B — change the evidence basis without destroying revision ancestry

### 33A / D177 — Explicit Working-Set Extension Preparation

33A addresses a new research reality: sometimes the rationale should change because the evidence basis itself changes.

A researcher can explicitly combine the governed declared-session endpoint with additional already-relinked evidence and author a new human rationale over that changed working set. The result is a new durable working set plus a new durable working-set note.

Preparation alone does not rewrite the existing revision lineage.

### 33B / D178 — Explicit Cross-Working-Set Transition

33B records the explicit transition from the exact old declared endpoint onto the exact changed working set and its human rationale.

This transition is not silently treated as an ordinary same-working-set revision edge.

That distinction preserves the fact that the evidence basis changed.

### 34A / D179 — Cross-Working-Set Revision Root

34A gives the first rationale revision after that changed evidence basis its own durable root.

The 33B transition remains a distinct transition object rather than being coerced into the ordinary revision predecessor model.

### 34B / D180 — Resume Ordinary Revision After Evidence-Basis Change

34B adds one explicit bridge from the 34A cross-working-set revision root back into the existing ordinary revision-edge system.

The proven relationship is:

```text
33B cross-working-set transition
→ 34A revision root
→ 34B first ordinary edge
→ existing ordinary edge revision machinery
```

This achieves both goals:

```text
basis-change ancestry preserved
+
ordinary revision behavior resumed
```

without creating a second long-lived revision system.

The root-specific bridge is needed only at the transition back into ordinary edges. Once the first root-backed ordinary edge exists, the established ordinary edge-to-edge path resumes.

## Post-34B design boundary — Research Control Plane

`docs/RESEARCH_CONTROL_PLANE.md` was merged after 34B as a documentation-only architectural note. It does not define a new milestone, runtime feature, schema, permission, provider, or research mode.

It records one important rule for future orchestration:

```text
human-readable research intent
!=
machine-enforced research state
```

Prompt-semantic instructions may explain what research should occur. Trusted application state must own any actual research requirement, source policy, tool permissions, connected-data access, resource ceilings, escalation decisions, and completion state.

Likewise:

```text
model recommendation
!=
authorization
```

and:

```text
model says "research complete"
!=
execution evidence proves required research completed
```

Retrieved or generated content that resembles control syntax remains untrusted content unless it arrived through a trusted control channel explicitly defined by Pyxis.

The note records a parser-vs-prompt experiment as a useful future benchmark, but does not authorize implementation.

## Authority boundaries that remain intentionally absent

Through 34B, Pyxis still does **not** claim or infer:

- a globally current/latest/canonical research head;
- complete revision history;
- unique successor relationships;
- global chronology from local durable references;
- semantic improvement between rationale revisions;
- truth or evidentiary support from human notes;
- quotation/citation authority from exact-text selection alone;
- source authenticity from SHA-256 self-integrity;
- source discovery from durable digest matching;
- browser navigation or interaction authority from observation capability;
- autonomous research authority from the standalone shell;
- permission escalation from model output or prompt-looking control strings; or
- research completion merely because a model or UI says it is complete.

These absences are product constraints, not missing implementation accidents.

## Current decision frontier

The implemented milestone frontier is **34B / D180**.

The post-34B control-plane note adds a design constraint but intentionally does not choose the next runtime milestone.

Therefore the next implementation should begin with an explicit product question rather than silently turning the control-plane note into code.

Candidate questions that are now structurally available include:

- Should a declared research session gain typed machine-owned research-control state?
- Should Pyxis run the documented parser-vs-prompt benchmark before introducing any control schema?
- Should sequence/restart authority be extended across the 34A root boundary, or remain edge-started?
- Should evidence-basis extension become available through the standalone research shell, and if so, what explicit user action owns that transition?

None of those questions is authorized merely by appearing here.

## Continuity rule

For future development sessions:

```text
implementation + tests + milestone record
> compact continuity summary
> presentation wording
```

If this file and a milestone record ever disagree, inspect the implementation/tests and the milestone-specific decision evidence before changing behavior.

Pyxis should continue to prefer explicit authority, falsifiable evidence, and narrow earned capability over convenient inference.
