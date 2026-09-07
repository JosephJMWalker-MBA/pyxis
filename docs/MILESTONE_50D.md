# Milestone 50D — root v2-backed transitions through the existing root-v1 format

Decision: **D258**  
Issue: **#244**

## Concrete researcher action

50C permits one explicit changed-basis transition-v1 whose successor basis is the established:

```text
research_working_set.v2
+
research_working_set_note.v2
```

The next existing researcher action is to author the first same-working-set rationale revision after that exact verified evidence-basis change and preserve the basis crossing as a durable lineage root.

50D carries that action through public 34A without introducing a parallel root format.

## Internal design decision

The durable root format remains:

`pyxis.chromium.research_session_working_set_transition_revision_root.v1`

Its record stores only:

```text
transition_reference:
  format
  record_sha256

root:
  mode
  revision:
    mode
    revised_note:
      mode
      text
```

It does not store:

- successor working-set format;
- successor working-set-note format;
- working-set members;
- selected source text;
- predecessor note text;
- transition payload;
- durable paths.

The v1-only restriction before 50D lived in the in-memory 34A validator, not in the root-v1 durable representation.

50C already established the supported successor-pair contract for a loaded transition-v1. 50D reuses that exact contract.

Conclusion: **no root v2.**

## 34A version-aware validation

Public 34A still accepts only one actual loaded transition-v1.

It continues to require:

- supported transition format and mode;
- exact prior endpoint format and content identity;
- exact successor working-set/note formats and identities as reported by the transition;
- exact successor note mode;
- exact note/working-set object relationship;
- exact successor note text reconstruction.

The only widened rule is the successor format gate.

Instead of requiring only:

```text
working_set.v1 + working_set_note.v1
```

34A now accepts either exact successor pair already authorized by 33B:

```text
working_set.v1 + working_set_note.v1
working_set.v2 + working_set_note.v2
```

Cross-version pairs remain invalid.

A hand-constructed loaded-transition object with a forged v2/v1 pairing therefore still fails closed at 34A creation even though a real public 33B loader would never produce that state.

## Human revision semantics are unchanged

The first root revision is still created by public 22A over exactly:

```text
transition.successor_note.note
```

Therefore:

- the prior note is exact;
- the changed working-set object is exact;
- bare selections remain ordinary retained working-set members;
- exact textual no-ops remain rejected;
- revised human wording remains verbatim.

50D adds no interpretation, migration, note synthesis, or semantic-support inference.

## Root persistence remains root-v1

Existing root persistence already freshly reloads the complete 33B transition from caller-supplied locators before writing root bytes.

Because public 33B is version-aware after 50C and public 34A is version-aware after 50D, the unchanged root persistence path can now re-establish a v2-backed transition and write the same root-v1 representation.

The root records:

```text
exact transition-v1 identity
+
first revised human wording
```

and nothing from the successor basis is duplicated.

## Fresh root relinking remains explicit

Existing root loading still requires:

- the already-loaded old endpoint context;
- complete ordered successor member sequence;
- prior-edge path;
- working-set path;
- working-set-note path;
- transition path;
- root path.

It freshly reloads public 33B and reconstructs public 34A.

No locator discovery, ancestry traversal, digest search, chronology, or current/head selection is added.

## Member sidecars remain unnecessary

The focused 50D proof removes already-loaded sidecars for retained and appended working-set members before transition/root persistence.

The v2 basis, transition, and root remain reconstructable from:

- caller-supplied loaded member application evidence;
- explicit working-set/note files;
- explicit transition/root files.

No browser reacquisition is introduced.

## Existing 34B is already general over root-v1

The established 34B bridge does not independently declare successor working-set/note versions.

It validates one loaded root-v1, uses that root's exact endpoint note, and persists the first ordinary existing-format revision edge whose predecessor reference is:

```text
root.v1 format
+
root.v1 record_sha256
```

50D therefore changes **no 34B code**.

The executable proof demonstrates:

```text
v2 working-set/note basis
→ transition-v1
→ root-v1
→ unchanged 34B
→ edge-v1
→ ordinary 25A/25B continuation
```

The first root-backed edge returns the standard loaded edge type. Once that edge exists, the ordinary edge-to-edge path requires no v2, transition, or root special case.

## Generic 24C remains narrow

50D does not make a loaded root a generic 24C input.

The established one-time root-specific 34B bridge remains necessary:

```text
loaded root-v1
→ 34B root-specific bridge
→ ordinary loaded edge-v1
→ generic edge continuation
```

This preserves the architectural distinction between a basis-change root and an ordinary same-working-set edge predecessor.

## Superseded test boundary

50C deliberately ended with an executable assertion that 34A rejected a v2-backed loaded transition.

That assertion was correct at D257.

D258 intentionally supersedes that single stop rule, so the obsolete assertion is retired. All other 50C persistence, pairing, digest, and relinking falsification remains intact.

## Focused falsification

50D tests prove:

1. a real 50C v2-backed transition-v1 creates a 34A root;
2. the first root revision prior note is exactly the transition successor note;
3. the revised note retains the exact v2 changed working-set object;
4. root persistence writes root-v1;
5. root verification reports the exact transition-v1 identity;
6. root bytes do not copy v2 format strings, selected source text, or predecessor rationale text;
7. fresh root loading reconstructs the exact v2-backed transition and root;
8. loaded member sidecars are unnecessary after preparation;
9. a hand-forged cross-version loaded transition fails 34A;
10. unchanged 34B creates, persists, and loads the first root-backed edge as edge-v1;
11. that root-backed result is the ordinary loaded edge record type;
12. ordinary 25A/25B continuation succeeds from the first root-backed edge;
13. generic 24C still rejects a loaded root directly;
14. existing v1/v1 root behavior remains covered by the unchanged historical 34A/34B suite.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50D adds no:

- root v2;
- transition format change;
- working-set or note format change;
- generic 24C root input;
- direct root sequence start;
- recursive ancestry traversal;
- automatic transition or adoption;
- browser interaction;
- source discovery;
- tags, search, or export;
- chronology, current/latest/head authority;
- citation or semantic-support authority.

## Acceptance statement

50D permits only this statement:

> One exact v2-backed transition-v1 can root its first explicit same-working-set human rationale revision in the existing root-v1 representation, freshly reconstruct that root from explicit durable inputs, and pass through the unchanged root-specific 34B bridge back into ordinary edge-v1 continuation without widening generic 24C or introducing a new durable format.
