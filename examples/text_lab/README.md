# Text Lab

`text_lab` is the permanent minimum executable specification for Repository Zero.

It is intentionally small. The text capabilities are test weights for the architecture, not the long-term Pyxis product domain.

This directory captures one complete first-run Workspace:

```text
human inputs
  ↓
authoring/canonical/workspace.json
  ↓
generated/repository.rir.json
  ↓
generated/generation.manifest.json
  ↓
generated capability + Workspace Python artifacts
  ↓
runtime/sample.json → runtime/expected.json
```

The checked-in authoring, RIR, manifest, and Python files are expected to match the current deterministic `build_workspace()` output byte for byte. Tests rebuild this Workspace through the permanent Pyxis path and compare the result to this directory.

The committed generated Workspace is also executed directly by the test suite against the sample input. This makes the example an executable architectural specification rather than a documentation-only fixture.

To reproduce it through the public CLI:

```bash
pyxis run \
  --name "Text Lab" \
  --description "Permanent executable architectural specification for Repository Zero." \
  --destination ./text_lab \
  --text "  hello   world  "
```

Generated files remain compiler products. `authoring/canonical/workspace.json` remains the authoritative intent for this example.
