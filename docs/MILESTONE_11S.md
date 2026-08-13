# Milestone 11S

D114: measurement invalidation notices are transient UI status, not evidence. A notice may appear only after an incoherent supplied measurement snapshot has already been discarded; it carries no measurement object or statistics, adds no control or acquisition path, and expires on the next user operation. Same-RIR and failed operations produce no notice.

Proof: Actions #334 passed on `c7fac05006447c56b7922f2c95603bd7cf6b4c15`; the live tests block measurement acquisition/re-projection, prove successful RIR-changing Apply removes the snapshot before mounting the fixed notice, prove the notice contains no controls or presentation object, and prove the next runtime operation removes only the notice while measurement remains absent.

Next: 11T may permit an already-produced caller-supplied measurement presentation for the current RIR to re-enter the live shell through the existing provenance gate, without renderer-owned measurement acquisition, re-projection, or refresh controls.
