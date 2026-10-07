# ForkLens v4

ForkLens is a GenLayer dependency-upgrade gate. It permits a consumer revision to become active only when authoritative GitHub data proves that an exact dependency upgrade is accompanied by changed production code, changed regression tests, and a successful check run bound to the exact consumer head.

## Why GenLayer

Deterministic contract logic fetches and binds GitHub compare responses, changed paths, exact commit identities, and exact-head check runs. Only after these hard predicates pass do validators judge whether the consumer change semantically remediates the dependency change. Removing intelligent consensus would reduce the product to path and CI presence checks.

## Trust boundary

- Repository identities are GitHub `owner/repo` slugs, and dependency and consumer repositories must differ.
- Base and head are full 40-character commit SHAs returned by GitHub's API.
- Production and regression paths must occur in the consumer's actual changed-file set.
- At least one completed, successful GitHub check run from an identified GitHub App must target the exact consumer head.
- A user-authored report, URL, digest, fixture, screenshot, or claim is never accepted as implementation or CI proof.
- GitHub source failure, missing paths, missing CI, semantic ambiguity, or validator disagreement fails closed.
- A compatible verdict creates a revision-bound, epoch-bound, single-use attestation. Only the project owner may activate it.
- The deployer has no administrator or testing role.

## Workflow

1. Register distinct dependency and consumer GitHub repositories with their active commits.
2. Open a candidate with exact base/head pairs and required production/test paths.
3. Any wallet calls `assess_candidate`.
4. Validators independently fetch GitHub compare and check-run APIs, enforce deterministic predicates, then perform semantic review.
5. The project owner consumes the exact attestation once to advance active revisions.

## Verification

```powershell
python -m pytest -q -p no:cacheprovider
python -X utf8 -m genvm_linter.cli check contracts\fork_lens.py
npm run lint
npm run build
```

Local tests use mocked GitHub responses only to exercise invariants; they are not submission evidence. Valid live evidence requires two independently hosted public repositories, real changed production/test files, and a real successful GitHub check on the exact consumer head. See [`docs/TEST_RESOURCE_MANIFEST.md`](docs/TEST_RESOURCE_MANIFEST.md).

## StudioNet deployment

ForkLens v4 is deployed at [`0xbA4A7b2A758993E1934657CB505dC2a7a97df091`](https://explorer-studio.genlayer.com/address/0xbA4A7b2A758993E1934657CB505dC2a7a97df091). Direct readback confirms schema `github-authoritative-dependency-gate-v4`, version `4`.

The finalized two-wallet run is indexed in [`docs/LIVE_STUDIONET_EVIDENCE.md`](docs/LIVE_STUDIONET_EVIDENCE.md), with every transaction hash linked to the explorer. Its canonical machine-readable report is [`docs/live-evidence/studionet-v4-1340299001.json`](docs/live-evidence/studionet-v4-1340299001.json): 20 transactions, 33 passing assertions, and zero failed assertions. Every transaction includes caller, exact arguments, finality, execution result, and authoritative before/after readback. It covers authoritative happy-path activation; missing production, regression, and exact-head checks; source outage; adversarial verification bypass; wrong actor; wrong digest; replay; final counters; and exact readback. Transient GitHub source failures were recorded separately and failed closed; scenario-specific claims passed only after authoritative source retrieval succeeded.

V2 and V3 remain deprecated for the documented reasons. See [`docs/V2_LIVE_DIAGNOSTIC.md`](docs/V2_LIVE_DIAGNOSTIC.md) and [`docs/V3_LIVE_DIAGNOSTIC.md`](docs/V3_LIVE_DIAGNOSTIC.md).

The earlier v1 address and its fixture-derived run remain invalid and must not be submitted. See [`docs/DEPRECATED_V1_EVIDENCE.md`](docs/DEPRECATED_V1_EVIDENCE.md).
