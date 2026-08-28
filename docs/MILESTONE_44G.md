# Milestone 44G — Persist Verified Root-Backed Restart Overlay

Decision: D224

## Product question

44F / D223 makes the exact first changed-basis 44E session freshly reproducible through
public 35B, but intentionally writes no restart configuration.

35C / D183 already proves the next persistence boundary:

```text
already-earned 35B root-backed re-entry
+ explicit ordinary 31B plan-document source
+ explicit overlay destination
→ decode/match prior plan
→ fresh 35B proof
→ no-overwrite 35C overlay persistence
→ strict round-trip decode
```

44G asks whether that exact persistence boundary can be exposed from the 44F product
without turning a historical restart locator into a claim about whichever controller
is currently mounted.

44G answers **yes**.

## Product chain through 44G

```text
44A prepare changed evidence basis
→ 44B persist explicit 33B transition
→ 44C persist 34A revision root
→ 44D persist first ordinary 34B edge
→ 44E explicitly adopt the 35A root-backed governed session
→ 44F freshly verify 35B reconstructability
→ 44G persist the verified 35C restart overlay
```

Each arrow remains a distinct authority step.

## Exact 44G inputs

44G adds only two durable locator fields.

Both begin blank:

1. the current path to the existing ordinary 31B v1 re-entry-plan document for the
   pre-change session; and
2. a no-overwrite destination for the new 35C root-backed overlay.

The overlay format remains exactly:

```text
pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1
```

No 44A–44F receipt path is copied into either input.

## Why the ordinary plan document is explicit again

The 44F result retains the exact prior 31A typed plan through its 35B plan.

That does **not** authorize Pyxis to choose a 31B document path automatically.

35C deliberately composes:

```text
explicit ordinary plan-document path
→ strict 31B decode
→ require typed-plan equality with earned 35B prior plan
```

Therefore the path to the ordinary plan document remains caller-owned operational
configuration.

```text
known typed prior plan
!=
authorized durable plan-document location
```

## Bounded product application result

44G adds one product wrapper:

```text
ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult
```

It contains:

- the exact successful 44F verification result; and
- the public 35C checkpoint result.

The wrapper delegates persistence to public 35C and then checks only product-level
identity/coherence facts:

- 35C retained the exact 44F fresh re-entry object;
- the checkpoint plan equals the exact 44F plan;
- the mandatory fresh 35C proof presents the same governed session;
- root SHA-256 matches the 44F proof;
- endpoint edge SHA-256 matches the 44F proof; and
- the persisted overlay path equals the explicit requested destination.

No new persistence format or writer is introduced.

## Public 35C remains authoritative

Public 35C still owns:

```text
ordinary 31B decode
→ exact prior-plan equality
→ candidate 35B plan composition
→ fresh 35B reconstruction
→ presentation/root/endpoint agreement
→ exclusive no-overwrite write
→ strict round-trip overlay decode
```

44G does not duplicate those rules.

## Historical target semantics

44F can prove the exact historical 44E session even after the mounted product has
continued through ordinary revision and 30A rollover.

44G preserves that property.

The persistence subject is:

```text
exact 44F verified session
```

not:

```text
whatever controller happens to be mounted when the user presses Persist
```

If the mounted shell has moved to a later continuation, 44G may still persist the
historical 44E/44F restart overlay while leaving the continuation mounted.

Therefore:

```text
44G overlay target
!=
implicit current-session selection
```

## Mounted state does not change

The dedicated 44G shell snapshots:

- `research_controller`;
- `research_session`; and
- `research_reentry`

before the 35C persistence call.

Successful persistence requires all three to remain the same objects afterward.

44G does not:

- replace the mounted controller;
- set a root-backed re-entry result as active state;
- mount generic restart-plan controls;
- relaunch from the overlay; or
- convert the overlay path into global branch state.

## Why 44G does not immediately add a restart button

35C proves durable root-backed operational configuration.

It does not define the product act of choosing that overlay for a new launch from the
current shell.

That remains a separate authority question because the shell may already represent a
later continuation by the time 44G runs.

A restart button that silently assumed the persisted historical overlay represented
"current" would introduce branch preference not earned by 35C.

## Relationship to 35D

35D / D184 owns a different problem:

> checkpoint one chosen first ordinary continuation above a persisted 35C root-backed
> session.

Its format is:

```text
pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1
```

44G does not write or prepare that format.

The distinction remains:

```text
35C / 44G
persist the verified root-backed session itself

35D
persist one later chosen ordinary continuation above that root-backed ancestry
```

## Textual surface

The 44G controls mount only after one exact successful 44F verification.

They show:

- the verified root identity;
- declaration identity;
- endpoint identity;
- an authority notice explaining historical-session persistence;
- blank ordinary 31B plan-document input;
- blank 35C overlay destination input; and
- one explicit persistence button.

After success both inputs and the button lock.

The receipt states that:

- the 35C overlay was persisted;
- it belongs to the exact verified historical session;
- the mounted governed session was not replaced;
- no global current/latest/head state was created; and
- no 35D continuation checkpoint was created.

## No-overwrite and failure behavior

All write semantics remain public 35C behavior.

An existing overlay destination is never replaced.

A mismatched ordinary plan document rejects before write.

Changed-basis/root/declaration tampering after 44F proof is detected by the mandatory
fresh 35B reconstruction before write.

UI failure leaves the form unlocked and the mounted governed state unchanged.

## Prior art and reuse

Internal prior art is decisive:

- 35C / D183 owns the durable overlay format and proof-gated writer;
- 44F / D223 owns the exact fresh 35B proof selected for persistence; and
- 35D / D184 owns the later first-continuation checkpoint boundary.

The external replay/resume/version-management review performed for 44F remains the
relevant comparison set. 44G introduces no new external persistence subsystem.

Conclusion remains:

> **no end-to-end substitute demonstrated in this review**

## Falsifiability

Focused 44G coverage proves:

1. the application wrapper persists exact 44F proof through public 35C;
2. the persisted overlay round-trips to the exact 44F 35B plan;
3. root and endpoint durable identities match the 44F proof;
4. a different valid ordinary 31B plan document rejects before overlay write;
5. an existing overlay destination remains byte-for-byte untouched;
6. root tampering after 44F proof rejects during mandatory fresh proof before write;
7. 44G controls do not mount before exact 44F success;
8. both 44G locator inputs begin blank;
9. successful UI persistence leaves mounted controller/session/re-entry unchanged;
10. no generic restart controls appear after 44G;
11. 44G may persist the historical 44F target after a later mounted rollover without
    retargeting to that continuation;
12. failed UI persistence remains retryable;
13. a plain 44F shell never gains 44G controls; and
14. no 35D continuation overlay is created.

## Scope

44G adds only:

- `src/pyxis/app/chromium_research_first_changed_basis_root_backed_reentry_overlay.py`;
- `src/pyxis/ui/chromium_research_first_changed_basis_root_backed_reentry_overlay_textual.py`;
- `src/pyxis/ui/first_changed_basis_root_backed_reentry_overlay_research_session_shell.py`;
- focused application and UI tests;
- this milestone document; and
- narrow `pyxis.ui` exports.

44G does not change:

- 35B fresh re-entry;
- 35C overlay format or persistence semantics;
- 35D continuation semantics;
- `ResearchSessionShell`;
- established root-backed continuation shells;
- second- or third-epoch shells;
- CLI;
- browser acquisition;
- inspection projections; or
- research evidence formats.

## What successful 44G proves

Successful 44G establishes only:

> From one exact successful 44F fresh root-backed reconstruction, one explicitly
> selected matching ordinary 31B plan document, and one explicit no-overwrite overlay
> destination, Pyxis can expose the existing 35C proof-gated persistence boundary and
> create durable root-backed restart configuration for that exact historical verified
> session without replacing the mounted governed state, checkpointing a later
> continuation, discovering files, or claiming global head/chronology/semantic
> authority.
