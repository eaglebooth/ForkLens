# Threat model

- A self-authored migration report cannot replace dependency diff, consumer diff, regression or CI slots.
- Evidence must bind the candidate's exact dependency or consumer target commit.
- Required non-report evidence URLs must contain the full target SHA.
- Candidate fields become immutable at sealing.
- Semantic failure, ambiguity and malformed consensus fail closed without attestation.
- Activation rechecks owner, project epoch and exact attestation digest.
- Cross-project substitution, stale candidates and replay cannot advance active revisions.
- The contract does not infer production deployment from GitHub evidence.
