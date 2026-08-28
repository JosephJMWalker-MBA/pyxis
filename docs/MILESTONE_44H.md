# Milestone 44H — Explicit In-Process Handoff Into Proven Root-Backed Product

Decision: D225

## Product question

44G / D224 persists the exact historical changed-basis session freshly proven by 44F through the established 35C proof-gated overlay boundary.

That successful 44G result contains two deliberately distinct fresh-process facts:

```text
44F fresh_reentry
→ retained as 35C checkpoint.reentry

35C mandatory fresh reconstruction
→ checkpoint.fresh_reentry
```

44H asks whether the researcher may explicitly leave the current 44-series shell and continue immediately with the exact **35C mandatory fresh proof** without reloading the just-written overlay and without treating successful persistence itself as mode promotion.

44H answers **yes**.

## Product chain through 44H

```text
44A prepare changed evidence basis
→ 44B persist explicit 33B transition
→ 44C persist 34A revision root
→ 44D persist first 34B post-root edge
→ 44E explicitly adopt the 35A root-backed governed session
→ 44F freshly verify 35B reconstructability
→ 44G persist the verified session through 35C
→ 44H explicitly hand the exact 35C fresh proof into the established root-backed product
```

Every arrow remains a separate authority step.

## Exact handoff subject

44H transfers exactly:

```text
last_first_changed_basis_root_backed_reentry_overlay
    .checkpoint
    .fresh_reentry
```

That object is already a `ChromiumResearchRootBackedSessionReentryResult` freshly earned by the public 35C persistence boundary.

44H deliberately does **not** transfer:

- the overlay destination path;
- the earlier 44F `verification_result.fresh_reentry` merely because it represents equivalent durable state;
- whichever controller is currently mounted;
- a newly reconstructed object loaded from the just-written overlay.

Therefore:

```text
exact 35C fresh typed proof
!=
persisted overlay path authority
```

## Successful persistence is not automatic handoff

The dedicated 44H shell subclasses only the concrete 44G shell.

Before exact successful 44G persistence:

- no 44H notice exists;
- no 44H handoff button exists.

After one new successful 44G persistence:

- the 44G form remains locked as the persistence receipt;
- the currently mounted controller/session/re-entry remain unchanged;
- one explicit notice appears;
- one explicit `Continue with verified changed-basis session` button appears.

The shell does not exit during persistence.

Only pressing that button exits the Textual application with the exact retained `checkpoint.fresh_reentry` object.

Normal close remains a valid non-handoff choice.

## Product runner closes the handoff loop

Returning a typed object from the 44H shell is necessary but is not by itself a complete product transition.

44H therefore also exposes one narrow UI-level runner:

```text
run_first_changed_basis_root_backed_handoff_research_session_shell(...)
```

Its behavior is exactly:

```text
run 44H shell
→ None on normal close: stop
→ exact ChromiumResearchRootBackedSessionReentryResult on explicit handoff
→ validate exact result family
→ pass that same object to create_root_backed_research_session_shell(...)
→ run the existing RootBackedResearchSessionShell
```

The runner does not inspect or reopen the persisted 35C overlay. It receives no overlay path argument and owns no persistence or ancestry proof.

This orchestration seam is the product act of “continue immediately”; the button press remains the authority that permits it.

## No overlay reload

44H performs no persistence, decode, file read, locator proof, directory search, digest search, format guessing, or overlay reconstruction.

The just-written 35C overlay remains useful for later explicit process relaunch through the already-proven root-backed overlay route, but it is not needed for the in-process handoff.

The handoff remains valid even if the just-written overlay file is no longer present after 44G success because the authority being transferred is the already-earned typed 35C proof object.

```text
successful durable persistence
+ explicit typed handoff
!=
reopen the durable file during handoff
```

## Receiving product remains existing root-backed behavior

44H introduces no second root-backed shell implementation.

The returned object is the exact input already accepted by:

```text
RootBackedResearchSessionShell
```

That existing product remains authoritative for:

- governed root-backed inspection;
- ordinary endpoint revision;
- explicit 30A rollover;
- the first 35D continuation checkpoint; and
- the later explicit 36D cumulative handoff.

44H adds only the typed bridge and narrow runner from the first changed-basis authoring flow into that established product family.

## Historical-target behavior

44G already permits persistence of the exact historical 44E/44F target after the mounted 44-series shell has rolled to a later ordinary continuation.

44H preserves that meaning.

If the shell currently mounts a later controller, successful 44G persistence leaves it mounted. The 44H handoff button then explicitly selects the exact historical session freshly proven by 35C.

That explicit button press is the branch-changing authority.

It is not described as discovery of the latest, current, preferred, or canonical branch.

If the researcher does not press the button, no handoff occurs and the product runner launches no receiver.

## Textual dispatch boundary

The 44H shell follows the correction already learned in 44G: Textual dispatches inherited message handlers through the MRO.

The 44H `on_button_pressed` handler therefore owns only the new 44H button and does not manually call the parent handler for inherited actions.

This avoids duplicate scheduling of 44A–44G button behavior.

## Prior art and reuse

Internal prior art is decisive:

- 36D / D189 proves an explicit typed in-process handoff after successful root-backed checkpointing without carrying path authority forward;
- 41E / D210 independently proves the same distinction for third-epoch continuation;
- 44G / D224 owns exact 35C persistence and retains `checkpoint.fresh_reentry`;
- `RootBackedResearchSessionShell` already owns receiving root-backed behavior.

44H therefore introduces no new persistence, replay, ancestry, restart schema, or generic orchestration subsystem. Its runner is bounded to this exact proven product transition.

Conclusion remains:

> **no end-to-end substitute demonstrated in this review**

## Falsifiability

Focused 44H coverage proves:

1. no handoff notice/button exists before successful 44G persistence;
2. successful 44F verification alone does not expose handoff;
3. failed/retryable 44G persistence does not expose handoff;
4. successful 44G persistence still leaves mounted controller/session/re-entry unchanged;
5. successful persistence does not automatically exit the shell;
6. the explicit 44H action returns the exact `checkpoint.fresh_reentry` object;
7. the handoff does not return the earlier 44F fresh object merely because it describes equivalent durable state;
8. deleting the just-written overlay after successful 44G persistence does not prevent the typed in-process handoff;
9. the existing `RootBackedResearchSessionShell` accepts and retains that exact object and exposes its established revision/rollover surface;
10. after a later mounted rollover, explicit 44H handoff still returns the historical 44G/35C target rather than the later mounted controller;
11. a plain 44G shell never gains 44H controls;
12. the 44H runner passes the exact returned typed object directly into the existing root-backed shell and runs that receiver;
13. normal close returns `None` and launches no receiver; and
14. an untyped 44H shell return is rejected before receiver launch.

## Scope

44H changes only:

- `src/pyxis/ui/first_changed_basis_root_backed_handoff_research_session_shell.py`;
- narrow `pyxis.ui` exports;
- focused mounted-UI/integration tests;
- focused product-runner tests; and
- this milestone document.

44H does not change:

- 35B reconstruction;
- 35C persistence or overlay format;
- 35D continuation checkpointing;
- `RootBackedResearchSessionShell`;
- cumulative root-backed shells;
- second- or third-epoch shells;
- CLI locator syntax;
- application-layer persistence or reconstruction;
- browser behavior;
- persistence formats; or
- evidence formats.

## What successful 44H proves

Successful 44H establishes only:

> After one exact successful 44G persistence, the researcher may explicitly transfer the exact freshly proven 35C `ChromiumResearchRootBackedSessionReentryResult` from the current changed-basis shell into the already-established root-backed product family, and the bounded 44H runner can launch that existing receiver with the exact typed object, without reloading the persisted overlay, promoting its path to current authority, automatically changing modes at persistence time, discovering a branch, or creating global latest/current/head authority.
