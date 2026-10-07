# Threat model

- **Self-authored proof:** callers cannot submit evidence URLs, digests, reports, screenshots, or CI JSON. The contract fetches GitHub APIs itself.
- **Repository substitution:** dependency and consumer must be distinct canonical GitHub slugs, fixed at project registration.
- **Revision substitution:** both compare responses must return the exact registered base and requested head SHAs with `ahead` status.
- **Decorative remediation:** every declared production and regression path must occur in GitHub's actual consumer changed-file set.
- **Fake or stale CI:** at least one completed successful check run, issued by a named GitHub App, must target the exact consumer head SHA.
- **Validator hallucination:** deterministic source predicates run before semantic review; the validator re-fetches sources and recomputes the proof digest.
- **Source outage or truncation:** unavailable/malformed GitHub responses fail closed and create no attestation.
- **Semantic ambiguity:** any verdict other than `COMPATIBLE` with no issues creates no attestation.
- **Unauthorized activation:** activation rechecks owner, project epoch, target revisions, digest, candidate status, and single-use state.
- **Overclaiming:** the gate proves source-level remediation and exact-head CI, not production deployment.
