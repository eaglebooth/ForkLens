# Test resource and evidence manifest

## Local regression resources

Unit tests mock GitHub compare/check-run responses and LLM output. Repository files under `fixtures/` are synthetic local test inputs. Neither is acceptable live evidence.

## Required live sources

A submission-grade run must use:

1. A public dependency repository containing a real base-to-head breaking change.
2. A different public consumer repository containing a real base-to-head remediation in production code and regression tests.
3. A GitHub Actions (or other GitHub App) check run completed successfully on the exact consumer head.
4. GitHub API responses for both compare endpoints and the consumer head's check-runs endpoint, fetched by the contract—not supplied by a wallet.

The two repositories must not be forks or paths inside this ForkLens repository used only to manufacture evidence. Their commit history and check run must remain independently inspectable.

## Current authoritative source pair

- Dependency: `eaglebooth/forklens-dependency`
  - base: `6cc2c3bf8aad0c0c23515e9ac01530c0d08243af`
  - head: `59e9de2b40b74f287c0ad9cf2d1ccebf3b74b846`
- Consumer: `eaglebooth/forklens-consumer`
  - base: `1f22697154ae777b723b81df4fe043ae95d3a9d6`
  - head: `5113a6eac492e3d135601b2981f858803d094ae5`
  - required production paths: `src/vault-approval.js`, `package.json`
  - required regression path: `test/vault-approval.test.js`

The consumer head pins the dependency head and contains a GitHub Actions workflow. On 2026-10-07, GitHub's public API reported check `regression` as `completed` / `success`, issued by `github-actions`, with `head_sha` exactly `5113a6eac492e3d135601b2981f858803d094ae5`. This remains revalidated by the contract at assessment time rather than trusted from this statement.

## Required live scenarios

- happy path: authoritative paths + exact-head CI + compatible semantic result, then activation;
- failure: missing production path;
- failure: missing regression path;
- failure: absent/non-successful/wrong-head check run;
- failure: unavailable authoritative source;
- conflict: authoritative files exist but semantic remediation is incompatible;
- authorization: non-owner cannot activate;
- integrity: wrong digest cannot activate;
- replay: consumed attestation cannot activate twice.

For every write, record transaction hash, finality/consensus status, caller, exact arguments, and authoritative post-transaction readback. Failed writes require unchanged-state readback. UI success may appear only after finality and matching readback.
