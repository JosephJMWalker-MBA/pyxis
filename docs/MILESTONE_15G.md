# Milestone 15G — read-only Chromium list evidence

## Product question

Can Pyxis expose authored ordered/unordered list structure for research inspection without flattening nested lists, repairing numbering, or promoting DOM nesting into semantic hierarchy?

15G answers **yes**.

## Boundary

```text
explicit Chromium DevTools endpoint
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('ol,ul')
    ↓
bounded global DOM-order OL/UL evidence
    ↓
direct LI children + mechanical nesting coordinates
```

`pyxis.browser.read_chromium_page_lists()` reads only existing `OL` and `UL` elements from the selected page. Every returned list preserves:

- a 1-based global DOM ordinal among matching `ol,ul` elements;
- literal `OL` or `UL` tag identity;
- the raw authored `start` attribute string, or `None` when absent;
- the nearest ancestor list's global ordinal when nested;
- the direct parent item's ordinal within that ancestor list when nested;
- a bounded prefix of only the list's direct `LI` children;
- the complete direct-item count so item truncation remains mechanical.

Every returned direct `LI` preserves:

- its 1-based ordinal among that list's direct `LI` children;
- the raw authored `value` attribute string, or `None` when absent;
- bounded direct-list text evidence;
- the complete Unicode code-point count of that direct-list text.

`pyxis.app.observe_chromium_page_lists()` reuses the established endpoint normalization and exact target-selection authority and projects the transport snapshot into frozen application evidence.

## Direct-list text

A parent list item's normal `innerText` includes text from nested lists. That would flatten two distinct DOM structures into one apparent passage.

15G therefore uses a fixed `TreeWalker` over text nodes and retains a text node only when the node's nearest `ol,ul` ancestor is the list currently being observed. Descendant-list text is excluded from the parent item's text evidence and remains available through the descendant list's own record.

For example:

```html
<li>Parent<ul><li>Nested</li></ul> tail</li>
```

is represented mechanically as:

```text
parent item direct text:  "Parent tail"
nested list item text:    "Nested"
nested parent location:   list 1 / item 2
```

This is structure preservation, not semantic interpretation. Pyxis does not claim that the nested list is a subargument, substep, dependency, priority level, or conceptual hierarchy.

## Authored numbering attributes

15G records `start` and `value` with `getAttribute(...)` rather than normalizing them through browser numeric properties.

That choice is deliberate. The raw authored strings remain evidence even when the markup is unusual or invalid for a particular element. A `start` attribute authored on a `UL`, or a `value` attribute authored on one of its items, is preserved rather than silently discarded, corrected, parsed, or promoted into a valid numbering model.

15G does not calculate displayed list numbers, repair discontinuities, normalize roman/alphabetic styles, infer counters from CSS, or decide whether the markup is conforming HTML.

## Real Chromium proof

15G adds an independent real-browser acceptance test rather than rewriting earlier browser fixtures.

The disposable page contains:

```html
<ol start="3">
  <li value="7">Alpha 😀 item</li>
  <li>Parent<ul start="99"><li value="42">Nested</li></ul> tail</li>
  <li>Third</li>
</ol>
<ul><li>Separate</li></ul>
```

With:

```text
list_limit = 2
item_limit = 2
text_limit = 7
```

Pyxis proves:

- three matching lists yield two returned records plus `list_count=3` and collection truncation;
- the first list remains literal `OL` with raw `start="3"`;
- three direct items yield two returned items plus `item_count=3` and item truncation;
- the first item's raw `value="7"` is preserved;
- `Alpha 😀 item` is bounded to `Alpha 😀` while retaining its complete Unicode code-point count;
- the parent item's direct text excludes `Nested`, retaining the direct text `Parent tail` mechanically;
- the nested list remains literal `UL` with raw authored `start="99"`;
- the nested list points to parent list ordinal 1 and parent item ordinal 2;
- the nested item's raw `value="42"` and text `Nested` remain separate evidence;
- the third independent list is represented by the complete list count/truncation fact;
- no numbering repair, flattening, semantic hierarchy inference, navigation, scrolling, activation, or other browser control occurs.

## Validation

Implementation head:

- `5f3f5fbdefc2b27d1d54395cce69e7044c4ec60b`
- Actions #517
- Python 3.11: full suite passed
- Python 3.12: full suite passed
- Python 3.13: full suite passed
- Python 3.14: full suite passed
- inspected Python 3.11 log: **254 tests collected and 254 passed**
- the established Chromium integrations and the new real Chromium list integration all passed

## Non-goals

15G adds no:

- list-number calculation or repair;
- validation of authored `start` / `value` attributes;
- CSS counter/style interpretation;
- flattening of nested lists;
- semantic outline or hierarchy inference;
- task/substep/dependency interpretation;
- ranking, recommendation, or priority inference;
- passage summarization or classification;
- citation or locator authority;
- scrolling or viewport ownership;
- navigation or link following;
- active-tab inference;
- clicks or form submission;
- target creation or closure;
- arbitrary DevTools commands;
- caller-supplied JavaScript;
- persistence;
- LLM interpretation;
- autonomous research workflow;
- browser UI.

## Decision D127

**Literal ordered/unordered list structure is valid read-only research evidence, but DOM nesting and authored numbering attributes are not semantic hierarchy or corrected numbering. Pyxis may expose bounded DOM-order `OL`/`UL` records from one explicitly selected existing Chromium page, including raw authored `start`/`value` attributes, direct `LI` children, direct-list text evidence that excludes descendant-list text, and mechanical parent-list/item ordinals, while granting no list repair, semantic grouping, ranking, interpretation, navigation, or browser-control authority.**
