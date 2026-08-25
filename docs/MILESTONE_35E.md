# Milestone 35E — Cumulative Post-Root Continuation Checkpointing

Decision: D185

## Product question

35D makes the first ordinary continuation after one persisted root-backed session
restartable without recursive configuration ancestry.

After that continuation is revised and rolled over again, Pyxis still needs a durable
restart configuration for the new endpoint.

35E asks:

> Can later ordinary continuations remain anchored directly to the same 35C
> root-backed overlay, without 35D→35D recursion and without flattening the original
> 33B→34A lineage?

35E answers **yes** by making the ordinary post-root declared segment cumulative.

## Fixed ancestry anchor

The original root-backed region remains owned by:

```text
ordinary 31B plan
→ 35C overlay
→ 35B root-backed session
→ terminal root-backed endpoint E1
```

35E never rewrites that region.

All later checkpoints remain directly anchored to the same 35C overlay:

```text
35C → E1
       ↓
       E2 → E3 → ... → En
```

The current 35D plan stores the complete ordered post-root edge tuple:

```text
declared_edge_sources = (E2, E3, ..., En)
```

and one cumulative 26B declaration for exactly that ordinary segment.

## Why this is not recursive overlay ancestry

35E does not create:

```text
35C → 35D → 35D → 35D
```

Each new overlay is still an ordinary 35D document whose
`prior_root_backed_overlay_source` points directly to the same 35C overlay.

The previous 35D overlay is an explicit input to checkpointing so Pyxis can verify
what continuation is being extended, but it is not referenced by the next overlay.

## Checkpoint flow

Given one supplied current 35D re-entry result, its explicit overlay path, and one
chosen 30A rollover to a new successor, 35E performs:

```text
current 35D overlay
→ strict decode
→ fresh 35D re-entry
→ require current presentation + endpoint SHA + root SHA agreement

chosen 30A rollover
→ require prior presentation + endpoint SHA agreement

fresh 35C/root-backed anchor E1
+ current declared_edge_sources
+ explicit chosen successor edge
→ public 26A ordered relinking
→ require terminal edge SHA + exact text match chosen rollover
→ persist new cumulative 26B declaration

same 35C overlay
+ cumulative edge tuple
+ new cumulative declaration
→ existing 35D plan
→ fresh 35D re-entry
→ require terminal edge SHA + exact text match chosen rollover
→ persist new 35D overlay
→ round-trip decode
```

## Cumulative presentation versus one-hop rollover presentation

The new cumulative controller intentionally has a different declared-segment
presentation from the one-hop 30A controller.

For example:

```text
30A controller: E2 → E3
35E cumulative controller: E1 → E2 → E3
```

Therefore whole-presentation equality would be the wrong authority test.

35E instead requires the two controllers to identify the same terminal durable edge
and exact final human wording.

This establishes the chosen continuation endpoint while allowing the cumulative
configuration to expose more ordinary post-root context.

## Existing declarations remain durable

35E does not delete, overwrite, or invalidate the older one-hop declarations created
by 30A or the earlier cumulative declarations.

A new cumulative declaration is a new durable artifact describing an explicitly
relinked ordinary sequence from E1 through the newly chosen endpoint.

Thus:

```text
new operational checkpoint
!=
deletion or falsification of earlier declarations
```

## Repeated extension

The same 35E operation can extend a previously cumulative 35D checkpoint again.

If the current plan contains:

```text
(E2, E3)
```

and the next chosen successor is E4, the next plan becomes:

```text
(E2, E3, E4)
```

while retaining the same direct 35C ancestry anchor.

This gives repeated restartable continuation without recursive overlay traversal.

## Destination discipline

The cumulative declaration destination and next overlay destination must be distinct.

Both are preflighted for no-overwrite before any new artifact is written. The actual
persistence boundaries also retain their exclusive-write behavior.

## Path and content identity

As throughout Pyxis:

```text
path = explicit location
path != durable content identity
```

35E uses caller-supplied paths only to locate artifacts. Chosen continuation authority
is established by freshly relinked durable edge identity and exact human text, not by
filename or directory.

## Authority boundaries

35E does not infer or claim:

- global latest/current/canonical head;
- complete history;
- chronology;
- branch identity;
- unique successor;
- semantic improvement;
- evidentiary support for rationale text;
- source authenticity;
- authorship;
- citation authority;
- path identity;
- directory scanning;
- digest-based discovery;
- predecessor discovery;
- browser reacquisition; or
- autonomous research.

The cumulative declaration is scoped only to the explicit ordinary post-root segment.
It does not absorb the 34A root-backed declaration.

## Falsifiability

Focused 35E coverage proves:

1. one current 35D continuation can be extended into a cumulative post-root edge
   tuple while preserving the same 35C anchor;
2. the next overlay uses the existing 35D format and does not reference the previous
   35D overlay;
3. the cumulative controller may expose a longer segment than the chosen one-hop 30A
   controller while retaining the same terminal edge identity and exact text;
4. older overlays and one-hop declarations remain untouched;
5. the next overlay round-trips through the existing 35D decoder and fresh re-entry;
6. a cumulative checkpoint can itself be extended again without recursive overlays;
7. a wrong current overlay rejects before new writes;
8. a wrong explicit successor is not replaced by a decoy file;
9. an existing next-overlay destination prevents cumulative declaration creation;
10. an existing cumulative-declaration destination prevents overlay creation; and
11. tampered current root-backed ancestry rejects before either new artifact is
    written.

## Scope

35E adds only:

- `src/pyxis/app/chromium_research_root_backed_session_continuation_checkpoint_extension.py`;
- `tests/test_app_chromium_research_root_backed_session_continuation_checkpoint_extension.py`; and
- this milestone document.

35E does not change:

- ordinary 31A/31B/32A/32B;
- 33A/33B;
- 34A/34B;
- 35A/35B;
- the 35C overlay format;
- the 35D overlay format;
- generic 24C;
- CLI;
- Textual UI;
- Chromium acquisition;
- research-control-plane state; or
- Repository Zero.

## What successful 35E proves

Successful 35E establishes only:

> From one explicit current 35D continuation overlay and one explicitly chosen next
> ordinary rollover, Pyxis can produce and prove a new cumulative post-root
> continuation declaration plus a new 35D overlay anchored directly to the same 35C
> ancestry, repeatedly and without recursive overlay traversal, ancestry flattening,
> filesystem discovery, or global head/semantic authority.
