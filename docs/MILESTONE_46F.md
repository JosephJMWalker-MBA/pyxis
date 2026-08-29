# Milestone 46F — Persist Verified Second-Basis Epoch Restart Overlay

Decision: D233

## Product question

46E / D232 proves that one exact historical 46D second-basis session can be freshly
reconstructed through public 37A, but intentionally writes no durable second-epoch
restart configuration.

37B / D191 already owns the proof-gated persisted form of an earned second-basis epoch.

46F asks only:

> Can the exact successful 46E proof be persisted through public 37B from a newly
> explicit current prior-continuation-overlay path and one explicit no-overwrite 37B
> destination, while leaving mounted governed state and immutable launch provenance
> unchanged?

## Decision

Add one concrete persistence bridge:

```text
exact 46E verification
+ explicit current prior 35D/35E continuation overlay
+ explicit no-overwrite 37B destination
→ public 37B fresh two-layer proof
→ strict 37B overlay write
→ strict round-trip decode
→ locked persistence receipt
```

while:

```text
46F persistence
!= second-epoch relaunch
!= mounted-controller replacement
!= launch-provenance mutation
!= later continuation checkpoint
!= global current/latest/head authority
```

## Prior art and reuse

Internal prior art is decisive:

- 44G / D224 is the first-basis product precedent for persisting an exact historical
  fresh-reentry proof without conflating it with whichever controller is mounted;
- 37B / D191 owns the second-basis locator-only overlay format, explicit prior-overlay
  re-supply, mandatory two-layer fresh proof, no-overwrite write, and round-trip decode;
- 46E / D232 owns the exact historical fresh 37A proof selected for persistence; and
- 45A / D226 keeps immutable launch provenance distinct from mutable current governed
  state.

46F introduces no new writer, overlay format, re-entry grammar, or generic epoch model.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Exact authority subject

The application wrapper requires exactly:

`ChromiumResearchSecondChangedBasisEpochReentryResult`

It passes exactly:

`verification_result.fresh_reentry`

to public `persist_chromium_research_second_basis_epoch_reentry_plan_document()`.

The product layer does not manufacture a replacement 37A result and does not widen
public 37B.

## Explicit locator discipline

46F adds exactly two durable path inputs:

1. the current prior 35D/35E continuation-overlay source; and
2. one new no-overwrite 37B destination.

Both fields begin blank.

The prior overlay must be supplied again even though 46E previously used one. The path
inside the historical 46E plan proves where one earlier verification looked; it is not
perpetual current-location authority.

Therefore:

```text
historical 46E locator
!=
authorized current 46F locator
```

Neither field is inferred or prefilled from:

- the 46E plan;
- persisted 35D/35E launch provenance;
- raw 36D launch context;
- 46A–46E receipts;
- directory contents;
- filenames; or
- displayed hashes.

## Public 37B remains authoritative

Public 37B receives the exact earned 46E fresh result plus the newly explicit prior
continuation-overlay source and destination.

It then:

1. builds a candidate plan using the newly explicit prior-overlay location and the
   earned second-epoch locator layer;
2. freshly reconstructs both ancestry layers through public 37A;
3. compares prior first-root continuation presentation, endpoint identity, and retained
   first-root identity;
4. compares second-root identity, governed presentation, and final endpoint identity;
5. writes the locator-only overlay with no overwrite; and
6. strictly round-trip decodes the persisted document.

46F does not duplicate those rules.

## Bounded product checks

After public 37B succeeds, the 46F wrapper additionally requires:

- `checkpoint.reentry` is the exact 46E `fresh_reentry` object;
- the public candidate plan uses the explicitly re-supplied prior-overlay location;
- every other second-epoch locator field is unchanged from the earned 46E plan;
- the mandatory fresh 37B proof matches the earned result across both ancestry layers;
- the persisted path equals the explicit destination; and
- strict loading of the persisted overlay equals the public candidate plan.

These checks establish bounded product coherence only. They do not establish source
authenticity, chronology, trusted time, or semantic support.

## Historical target semantics

46F persists the exact 46E verification that mounted its controls.

It does not ask which controller happens to be mounted when persistence occurs.

A researcher may therefore:

```text
prove exact 46E historical second-basis session
→ continue the mounted 46D product through an ordinary rollover
→ persist the exact earlier 46E proof through 46F
```

without retargeting the overlay to the later mounted controller.

The shell snapshots and requires unchanged across persistence:

- `research_controller`;
- `research_session`;
- `research_reentry`; and
- retained first-root continuation re-entry.

## Product surface

`SecondChangedBasisEpochReentryOverlayResearchSessionShell` subclasses the 46E shell.

It overrides the 46E verification action only to detect one newly successful exact 46E
result and mount one 46F persistence form.

The form contains:

- the verified first-root identity;
- verified second-root identity;
- verified declaration and endpoint identities;
- one authority notice;
- one blank current prior-continuation-overlay input;
- one blank no-overwrite 37B destination input;
- one explicit persistence button; and
- one status/receipt surface.

Successful persistence locks both inputs and the button.

No restart or relaunch control is added.

## Raw 36D launch behavior

Inspectable raw 36D continuation handoff products inherit 46F.

A raw launch may use an explicitly supplied persisted 35D/35E continuation overlay as
one 46F input because public 37B freshly proves durable ancestry through that path.

That path still does not become launch provenance.

After successful 46F persistence:

- the exact immutable raw launch-provenance object remains unchanged;
- its launch-location context remains `None`;
- current governed-state projection remains unchanged by 46F itself; and
- the mounted controller remains unchanged.

## Textual dispatch rule

The 46F shell handles only its own persistence button and deliberately does not call a
parent `on_button_pressed()` for unhandled events.

Textual dispatches inherited handlers through the MRO. Manual parent dispatch would
schedule inherited actions twice, reproducing the defect caught during 46D CI.

## Falsifiability

Focused coverage proves at minimum:

1. exact 46E result type is required;
2. successful 46F persistence retains the exact 46E fresh result as public 37B's earned
   re-entry;
3. the persisted overlay strictly decodes to the public 37B candidate plan;
4. a wrong prior-overlay source rejects before destination write;
5. an existing destination remains byte-for-byte untouched;
6. 46F controls do not exist before successful 46E;
7. both 46F path inputs begin blank;
8. successful persistence leaves mounted governed state unchanged;
9. persistence after a later mounted ordinary rollover still targets the exact earlier
   46E verification; and
10. raw 36D launch provenance remains object-identical and pathless while current-state
    inspection remains unchanged by 46F.

Repository Zero remains the full-suite gate on Python 3.11–3.14.

## Non-goals

46F adds no second-epoch relaunch button, no later second-epoch continuation checkpoint,
no adoption of the fresh 37A proof into current mounted state, no third/fourth basis
change, no arbitrary-depth ancestry, no generic Nth-epoch persistence helper, no
locator discovery/prefill, no launch-path backfill, no CLI flag, no new persistence
format, no inspection schema, no browser reacquisition, no global
current/latest/head/chronology authority, no path identity, no authorship/authenticity
or trusted-time authority, no semantic-support/citation authority, and no autonomous
research behavior.

## Earned statement

A successful 46F establishes only:

> From one exact successful historical 46E fresh reconstruction, one explicitly
> re-supplied current prior 35D/35E continuation-overlay location, and one explicit
> no-overwrite destination, Pyxis can use the existing public 37B boundary to freshly
> re-prove both ancestry layers and persist strict second-basis restart configuration
> for that exact historical session without replacing the mounted governed session,
> mutating launch provenance, relaunching from the overlay, discovering files, or
> claiming global branch, chronology, or semantic authority.
