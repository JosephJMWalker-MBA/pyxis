# Milestone 11Q

D112: Workspace/measurement co-display requires the supplied measurement subject to match the displayed Workspace presentation on Repository ID, Workspace ID, and exact RIR SHA-256. The gate reads existing evidence only and fails before Textual initialization.

Proof: Actions #325 passed on `ac33ae4c5e4ce33c149aa9a9ef19e749d86a7422`; independent Repository, Workspace, and RIR mismatches are rejected before the base Workspace shell initializer can run.

Next: 11R should preserve that co-display invariant across live Workspace state changes: runtime/export updates may keep an exact-RIR measurement snapshot, while a successful architecture Apply that changes RIR must remove the now-incoherent measurement surface without acquiring or recomputing measurement evidence.
