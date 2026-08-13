# Milestone 11R

D113: live measurement co-display remains only while its Repository, Workspace, and RIR identity matches the current Workspace presentation. Same-RIR and failed operations keep the supplied snapshot; successful RIR-changing Apply clears it after the existing Apply path completes.

Proof: Actions #331 passed on `cfdac7c3cfd7e35a2faf563aa4712672371f67f8`; 200 tests passed without measurement acquisition or re-projection.

Next: 11S should show a non-evidence UI notice when a prior measurement snapshot is cleared after RIR change, with no stale evidence, remeasurement, or new controls.
