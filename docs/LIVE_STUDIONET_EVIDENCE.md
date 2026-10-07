# ForkLens V4 live StudioNet evidence

This document is the human-readable index for the machine-readable report in [`live-evidence/studionet-v4-1340299001.json`](live-evidence/studionet-v4-1340299001.json).

## Deployment and actors

- Network: GenLayer StudioNet, chain ID `61999`
- Contract: [`0xbA4A7b2A758993E1934657CB505dC2a7a97df091`](https://explorer-studio.genlayer.com/address/0xbA4A7b2A758993E1934657CB505dC2a7a97df091)
- Schema: `github-authoritative-dependency-gate-v4`, version `4`
- Wallet A / project owner: `0xeb57bc7125fa60d7482CE12058397369AB3581f8`
- Wallet B / independent assessor: `0x2da5393d7BBb9A037dc3abB56DbbC5C150fc843f`
- All behavioral transactions in this run were sent by the two test actors listed above.

## Result summary

- 20 transactions, all `FINALIZED`
- 33 assertions passed, 0 failed
- Every transaction in the JSON report records caller, exact arguments, expected and actual execution, and authoritative before/after readback.
- Expected `ERROR` transactions are negative controls. They finalized with an execution error and unchanged contract state.
- Happy candidate `vault-1340299001.happy`: `COMPATIBLE` and `ACTIVATED`
- Project after activation: epoch `2`, activated count `1`, open attestations `0`
- Missing production, missing regression, missing exact-head checks, unavailable source, and semantic-conflict candidates remained blocked without attestations.

## Finalized transaction index

| # | Scenario | Actor | Expected execution | Finality | Transaction |
|---:|---|---|---|---|---|
| 1 | Register authoritative source pair | Wallet A | `SUCCESS` | `FINALIZED` | [`0xe58a…48d4d`](https://explorer-studio.genlayer.com/tx/0xe58a0e077401b1b2f3314262ae081c8a4cbe6178a82a54e3812b7b37cff48d4d) |
| 2 | Open happy candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0xaf5b…d875b`](https://explorer-studio.genlayer.com/tx/0xaf5b73ec1ff4e04fc28103c47b985d29d64b3ee8f24c34cf8481381a694d875b) |
| 3 | Open missing-production candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0x2547…6e7b3`](https://explorer-studio.genlayer.com/tx/0x25473c14653eea0badfdbb878ea92f7e888decbbee307504367b03173766e7b3) |
| 4 | Open missing-tests candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0x8b5c…0c8cb1`](https://explorer-studio.genlayer.com/tx/0x8b5c22c2f88c8d9e5f6fcf53eb0f006e4c2cd7835173886e4467e0623f0c8cb1) |
| 5 | Open missing-checks candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0xa720…25bcb`](https://explorer-studio.genlayer.com/tx/0xa720be15a7bf6d663b4e87cfeed116da8b47748b4c2b0353dcb1c0cd13925bcb) |
| 6 | Open semantic-conflict candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0xb6ca…4f66c`](https://explorer-studio.genlayer.com/tx/0xb6cab1dbc2eec67a03a407681893903b346d1fbd0adde4034b319a376ee4f66c) |
| 7 | Assess missing production | Wallet B | `SUCCESS` | `FINALIZED` | [`0x275a…86ae9`](https://explorer-studio.genlayer.com/tx/0x275ae955adb7997ce2da3b8a2ef6aa7f0850b13f618c56be626061cc41e86ae9) |
| 8 | Assess missing regression tests | Wallet B | `SUCCESS` | `FINALIZED` | [`0xcfc6…9c62c0`](https://explorer-studio.genlayer.com/tx/0xcfc6f49fc43006ca97c12a8c03e2efc997c656320657a12e5a5f1b3dd89c62c0) |
| 9 | Assess absent exact-head checks | Wallet B | `SUCCESS` | `FINALIZED` | [`0x260f…eb107`](https://explorer-studio.genlayer.com/tx/0x260fccdd479311ad8fd4cc880187803324c012006610c2b29484bd02412eb107) |
| 10 | Assess semantic conflict; authoritative source transiently unavailable and failed closed | Wallet B | `SUCCESS` | `FINALIZED` | [`0xa517…deb99`](https://explorer-studio.genlayer.com/tx/0xa517532d224a3c1a73e8ae9afea66176b58d7553c37687930b02d0af796deb99) |
| 11 | Open fresh semantic-conflict retry candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0x4a31…bde80`](https://explorer-studio.genlayer.com/tx/0x4a31a205a7be66446346449ef46b4d6e20451a87379e526263f7bfa5d35bde80) |
| 12 | Assess semantic-conflict retry; candidate blocked | Wallet B | `SUCCESS` | `FINALIZED` | [`0xc03a…1b35a6`](https://explorer-studio.genlayer.com/tx/0xc03a4a5a758629278f0643a8a74855bdf9bb0c3895f08bfad73670f1191b35a6) |
| 13 | Register unavailable-source project | Wallet A | `SUCCESS` | `FINALIZED` | [`0xb082…b9a88`](https://explorer-studio.genlayer.com/tx/0xb082a1317c599cefc0fdb0a9ebe30b5f1dace6693b5c74f1d07fd84917ab9a88) |
| 14 | Open unavailable-source candidate | Wallet A | `SUCCESS` | `FINALIZED` | [`0x5dc9…6c7877`](https://explorer-studio.genlayer.com/tx/0x5dc9343e9f2c5d6235ba38fd42a2921de15e4e936957e4d2905a4a74d56c7877) |
| 15 | Assess unavailable source; candidate blocked | Wallet B | `SUCCESS` | `FINALIZED` | [`0x22d6…68950`](https://explorer-studio.genlayer.com/tx/0x22d6bc768b2252e9d8e0001958c080e553663d21a78e77f2c7967b7846668950) |
| 16 | Assess happy candidate; exact attestation created | Wallet B | `SUCCESS` | `FINALIZED` | [`0x5bcb…dd07f`](https://explorer-studio.genlayer.com/tx/0x5bcb76c1e77dc38a55062e931ba41abcc4b678c23ec18a4d4b677eb3bf4dd07f) |
| 17 | Non-owner activation rejected; state unchanged | Wallet B | `ERROR` | `FINALIZED` | [`0x46bf…9a700`](https://explorer-studio.genlayer.com/tx/0x46bf0503f2fc2e0855dca086af138f257a0aae921b29a9ccf6e84aaff619a700) |
| 18 | Wrong attestation digest rejected; state unchanged | Wallet A | `ERROR` | `FINALIZED` | [`0xfcc5…f2e79`](https://explorer-studio.genlayer.com/tx/0xfcc50339d19854dfdefa8a5384de8f67ee6eaf6adc2cb21c97cb3eacb08f2e79) |
| 19 | Activate exact revision-bound attestation | Wallet A | `SUCCESS` | `FINALIZED` | [`0xfa74…394b5`](https://explorer-studio.genlayer.com/tx/0xfa74c2487408a410c3694e279ba9b7ec742fe8e9dd94455eb8891d91287394b5) |
| 20 | Replay consumed attestation rejected; state unchanged | Wallet A | `ERROR` | `FINALIZED` | [`0xdd18…988da`](https://explorer-studio.genlayer.com/tx/0xdd1843b690c6a35d014fab8cf618b2d6881cf38840d4aee224bd2b71528988da) |

## Authoritative public sources

- [Dependency repository](https://github.com/eaglebooth/ForkLens-Dependency)
- [Consumer repository](https://github.com/eaglebooth/ForkLens-Consumer)
- [Compatible consumer head](https://github.com/eaglebooth/ForkLens-Consumer/commit/5113a6eac492e3d135601b2981f858803d094ae5)
- [Semantic-conflict head](https://github.com/eaglebooth/ForkLens-Consumer/commit/44d9f604b202661a5dd8cbf3554df2dcf8dd9ab4)
- [Head with no exact-head check-run](https://github.com/eaglebooth/ForkLens-Consumer/commit/842d09e63591ee09ba9a1f96d8913f37da775fee)
- [Resource and evidence manifest](TEST_RESOURCE_MANIFEST.md)

The Markdown index is intentionally a navigation aid. The JSON report remains the canonical artifact for exact arguments and complete before/after contract state.
