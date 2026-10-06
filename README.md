# ForkLens

ForkLens is a GenLayer dependency-upgrade acceptance gate. It verifies whether a Web3 consumer actually changed production code and regression coverage for an exact dependency revision before allowing that revision to become active.

## Why GenLayer

Deterministic logic binds repository identities, full commit SHAs, required evidence slots, candidate epoch and single-use activation. Validators then judge the semantic relationship between the dependency breaking change, consumer remediation and regression evidence. Removing semantic consensus would reduce the product to a file-presence checker.

## Authority and consequence

The deployer receives no administrator role. Any reviewer wallet may register a unique project namespace. That authenticated sender owns only its namespace. A `COMPATIBLE` verdict produces an exact attestation; `activate_candidate` consumes it and advances the project's active dependency and consumer revisions. Reports, missing evidence, stale CI and non-positive verdicts create no activation capability.

## Workflow

1. Register a project and its current revisions.
2. Open a candidate for exact dependency and consumer targets.
3. Fill four typed, commit-bound evidence slots.
4. Seal the immutable packet.
5. Trigger semantic compatibility review from any wallet.
6. Project owner consumes the exact attestation once.

## Proof boundary

ForkLens demonstrates revision-bound source review and on-chain activation state. A synthetic fixture must be labelled synthetic. Source or test evidence does not prove a production deployment occurred, and ForkLens does not claim to deploy the reviewed software.

## Verify

```powershell
python -m pytest -q -p no:cacheprovider
python -X utf8 -m genvm_linter.cli check contracts\fork_lens.py
npm run lint
npm run build
```

StudioNet deployment: [`0x81066BDd259507f1bba56579864AD8cef6aB63dD`](https://explorer-studio.genlayer.com/address/0x81066BDd259507f1bba56579864AD8cef6aB63dD).
