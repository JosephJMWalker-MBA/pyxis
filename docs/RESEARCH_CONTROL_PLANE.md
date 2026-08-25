# Research Control Plane

**Status:** design note; documentation only  
**Recorded:** 2026-08-25  
**Related issue:** #68

## Purpose

Pyxis already separates human intent, canonical authoring state, Repository Intermediate Representation, generated implementation, runtime evidence, and revision history. Research orchestration should preserve the same separation.

The governing rule is:

> Human-readable research intent may describe what should happen. Trusted application state decides what is allowed to happen and records what actually happened.

This note does not add a runtime feature or schema. It records a boundary for future research-mode work.

## Semantic instruction is not operational authority

A model can be shown text such as:

```text
[RESEARCH REQUIRED]
Verify the claim before answering.
```

or:

```text
research_required: true
```

That text can be useful because humans and models can understand its meaning. It does not, by itself, prove that Pyxis changed workflows, enabled tools, expanded source access, increased a token/cost budget, or satisfied a research requirement.

A string only becomes a hard application control when a trusted parser or application boundary explicitly assigns it semantics.

The architectural distinction is therefore:

```text
prompt-semantic instruction
        !=
application-enforced research state
```

This matches Pyxis's broader rule that presentation and derived artifacts do not acquire facts or authority merely by representing them.

## Proposed future two-layer shape

If Pyxis introduces research orchestration, prefer two synchronized layers.

### Control layer

Machine-owned state should carry fields such as:

```text
research.required
research.status
research.depth
research.source_policy
research.tool_permissions
research.connected_data_access
research.budget_ceiling
research.evidence_manifest
research.completion_receipt
```

Exact field names and persistence are future decisions. The important point is ownership: the application controls them.

### Prompt layer

The model may receive a readable explanation such as:

```text
This task requires external verification before its factual claims may be treated as established.
Report unresolved contradictions rather than smoothing them over.
```

That explanation mirrors the control state. It does not create or override the control state.

## Authority and escalation

A model may recommend deeper research, a broader source set, another provider, a new tool, or a higher budget. That recommendation is evidence for an application or human decision, not permission.

Conceptually:

```text
model recommendation
    -> proposed escalation
    -> policy / human decision
    -> authorized state change or rejection
```

Do not implement:

```text
model output contains a marker
    -> enable more capabilities
```

A model-generated string must never expand its own capability envelope.

## Research completion requires evidence

A model saying "research complete" is not a completion receipt.

A future Pyxis research workflow should be able to demonstrate completion from observable execution evidence appropriate to the task, for example:

- source acquisitions or source references;
- tool calls and their outcomes;
- source-policy compliance;
- contradiction checks where required;
- citation/source entailment checks where implemented;
- unresolved gaps or failures;
- the exact research configuration that ran; and
- a completion decision made by the owning application boundary.

The evidence may be summarized for presentation, but the summary should remain downstream of the recorded execution facts.

## Untrusted-content boundary

Retrieved pages, uploaded documents, generated files, examples, and model output may contain authoritative-looking syntax. Examples include:

```text
[SYSTEM]
[ADMIN]
[RESEARCH COMPLETE]
--research
research_required: false
```

Unless the content arrived through a trusted control channel explicitly defined by Pyxis, those strings remain content.

Future implementations should be testable against at least these failure modes:

- **spoofing:** untrusted content imitates a control marker;
- **downgrade:** content attempts to clear a required research state;
- **privilege escalation:** content attempts to enable a tool or connected source;
- **budget escalation:** content attempts to raise search depth or resource ceilings;
- **false completion:** a model claims evidence work occurred when no execution receipt supports it.

## Relationship to existing Pyxis architecture

This boundary extends existing architectural habits rather than introducing a new philosophy.

```text
human intent
    -> canonical state
    -> RIR
    -> compiler/runtime
    -> evidence
```

Research should likewise preserve a visible transition from intention to executable state to evidence.

A future UI may render research status, but it should not infer that status from generated prose, nearby files, or a model's self-description. As with Workspace presentation, the UI should consume evidence produced by the owning boundaries.

## Useful future experiment

Pyxis is a good environment for a causal comparison between orchestration and prompt semantics.

Test three otherwise identical conditions:

1. **Parsed control:** a trusted application field activates a real research workflow.
2. **Text-only pseudo-control:** the same marker is passed to the model as ordinary content but does not change orchestration.
3. **Plain semantic instruction:** the model is told to research carefully without a marker.

Measure observable outcomes such as:

- tool calls;
- source count and provenance;
- contradiction discovery;
- unsupported-claim rate;
- completion-evidence quality;
- runtime/token/cost burden; and
- resistance to injected control-looking text.

The purpose would not be to prove a special syntax is powerful. It would measure how much behavior comes from orchestration versus language-only steering.

## Non-goals

This note does not:

- define a new canonical object;
- choose a research provider;
- authorize web or connected-data access;
- set a universal research depth;
- claim that one prompt syntax is superior;
- change compiler/runtime behavior; or
- treat model reasoning as execution authority.

## North star

```text
Intent is readable.
Authority is authenticated.
Execution is observable.
Completion is evidenced.
```
