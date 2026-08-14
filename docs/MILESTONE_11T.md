# Milestone 11T

D115: an already-produced caller-supplied measurement presentation may re-enter a live Workspace shell only through the existing Repository/Workspace/RIR provenance gate and only while no measurement snapshot is currently mounted. Successful re-entry mounts the exact supplied read-only presentation and clears any prior transient removal notice. Mismatched evidence or an attempted replacement fails before shell evidence changes.

The re-entry boundary does not acquire measurements, re-project measurement evidence, add measurement controls, infer current measurements from Workspace state, or change the existing 11R invalidation rule. A later RIR-changing Apply still removes the supplied snapshot when its provenance no longer matches current Workspace evidence.

Proof: Actions #338 passed on `36facd74db3a3e36300175d8d97b565da37a7073`; the full Repository Zero suite passed with acceptance tests that block measurement acquisition/re-projection, prove coherent current-RIR re-entry, reject mismatched evidence before UI mutation, reject replacement of an already-mounted snapshot, preserve the existing non-measurement control set, and clear the prior 11S notice only after successful re-entry.

Continuity: `CURRENT_STATE.md` is the current Repository Zero front door through 11T. It consolidates the post-11J architectural/decision deltas without replacing the large historical central documents through a connector that cannot safely apply line-level patches.

Next: choose the next implementation milestone from a concrete Pyxis product requirement rather than automatically adding measurement statistics or generalized abstractions.
