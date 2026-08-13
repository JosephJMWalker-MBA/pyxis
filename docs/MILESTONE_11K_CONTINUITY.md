# Milestone 11K Continuity — Exact Work-Context Arithmetic Mean

Milestone 11K extends the Repository Zero measurement path by adding arithmetic mean as a separate immutable evidence layer over the already-proven Milestone 11J median evidence.

## Architectural delta

The measurement chain now continues:

```text
BuildAndRunMeasurementDurationEnvelopeEvidence
    ↓
create_build_and_run_measurement_median()
    ↓
BuildAndRunMeasurementMedianEvidence
    ↓
create_build_and_run_measurement_mean()
    ↓
BuildAndRunMeasurementMeanEvidence
```

`src/pyxis/app/measurement_mean.py` defines frozen `StageWorkContextMeanEvidence`, `MeasurementStageMeanEvidence`, and `BuildAndRunMeasurementMeanEvidence`.

Each `StageWorkContextMeanEvidence` retains the exact source `StageWorkContextMedianEvidence` object. The top-level `BuildAndRunMeasurementMeanEvidence` retains the exact source `BuildAndRunMeasurementMedianEvidence` and preserves the same ordered stage/group contract.

The retained median is provenance context, not an input to the arithmetic calculation. `mean_seconds` is recomputed independently from the raw durations reachable through:

```text
StageWorkContextMedianEvidence
    ↓ exact object
StageWorkContextDurationEnvelopeEvidence
    ↓ exact object
StageWorkContextGroupEvidence
    ↓
raw StageSampleObservationEvidence durations
```

Direct construction revalidates the arithmetic mean against those raw observations and rejects an equal-but-distinct median evidence object where exact source identity is required.

## D106

D106 — **Arithmetic mean remains attached to exact median/source evidence** — is recorded in `docs/DECISIONS.md` and is normative.

Mean and median are separate descriptive central-tendency facts for one exact recorded work context. Agreement or disagreement between them is not a distribution model, performance score, outlier policy, steady-state estimate, efficiency claim, or causal explanation.

Milestone 11K adds no variance, standard deviation, confidence interval, additional quantile/percentile, trend, semantic work-state label, performance score, persistence, UI, full Execution Ledger, cross-work-context aggregation, causal interpretation, or Preview/Apply/Export measurement.

## Executed proof

The acceptance path uses five real measured build/run cycles under one exact cohort condition. It proceeds through the permanent chain:

```text
measurements
→ cohort
→ raw stage samples
→ exact work-context partition
→ count/min/max envelope
→ median
→ arithmetic mean
```

The repeated-work fixture deliberately makes mean and median differ:

- build repeated-work mean: `0.9375`; median: `0.875`
- runtime repeated-work mean: `0.6875`; median: `0.625`

The singleton groups remain build `4.0` and runtime `2.0` for both central-tendency values.

The proof also verifies frozen evidence, exact source median object identity, rejection of incorrect mean values, rejection of equal-but-distinct median source objects, and rejection of reordered stage contracts.

GitHub Actions run #302 completed successfully on implementation/test head `fca80017a0a55ebe32fa59f14e01ce7e5813ff0c`, including installation and the complete pytest suite on Python 3.11.

## Continuity note

`docs/ARCHITECTURE.md` and `docs/DEVELOPMENT_ARCHIVE.md` remain authoritative through Milestone 11J. The GitHub connector rejected the large whole-file replacements needed to fold 11K into those continuity documents. They were deliberately left unchanged rather than risking truncation or historical rewrite. This addendum plus D106 carries the 11K delta until a safe patch primitive is available.

For future sessions, treat Milestones 11A through 11K as complete once the final documentation-locked head is verified. The permanent measurement path is now:

```text
individual observation
→ descriptive pairwise comparison
→ exact repeated-measurement cohort
→ raw stage samples retaining exact BuildWorkEvidence
→ exact work-context partition
→ count/min/max envelope
→ source-linked median
→ source-linked arithmetic mean
```

Every summary remains inspectable back to exact raw evidence, and no work context is recombined across the partition boundary.

## Next narrow step — Milestone 11L

Add exactly one descriptive dispersion value: **population standard deviation over the complete recorded observations in each exact work-context group**.

Retain the exact 11K mean evidence as source context. Derive squared deviations from the raw durations and the exact retained arithmetic mean. A singleton group reports `0.0` because there is no observed dispersion inside that complete recorded group.

The term “population standard deviation” here describes the denominator used over the complete recorded group; it does not claim the observations represent an inferred statistical population or support generalization beyond the recorded evidence.

Do not add sample standard deviation, variance as a second public statistic, confidence intervals, inferential population claims, extra quantiles, outlier/warmup labels, scores, persistence, UI, cross-work-context aggregation, causal interpretation, or broader operation measurement in 11L.
