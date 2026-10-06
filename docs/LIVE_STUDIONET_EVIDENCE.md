# ForkLens V1 — Live StudioNet Evidence

## Scope

- Contract: [`0x81066BDd259507f1bba56579864AD8cef6aB63dD`](https://explorer-studio.genlayer.com/address/0x81066BDd259507f1bba56579864AD8cef6aB63dD)
- Network: GenLayer StudioNet (`61999`)
- Run: `1280471390`
- Project: `forklens-1280471390`
- Baseline commit: [`429231825b3e69782d1463f15b3a528d8bdc0308`](https://github.com/eaglebooth/ForkLens/commit/429231825b3e69782d1463f15b3a528d8bdc0308)
- Target commit: [`ca8e1efedfd0b4a238f851fc41a3c8699c049252`](https://github.com/eaglebooth/ForkLens/commit/ca8e1efedfd0b4a238f851fc41a3c8699c049252)
- Wallet A / project owner: `0xeb57bc7125fa60d7482CE12058397369AB3581f8`
- Wallet B / independent review trigger: `0x2da5393d7BBb9A037dc3abB56DbbC5C150fc843f`
- Deployer involvement after deployment: none
- Machine-readable record: [`live-evidence/studionet-1280471390.json`](live-evidence/studionet-1280471390.json)

## Finalized transaction trail

All 16 transactions reached `FINALIZED` and matched their predeclared success/error outcome.

| Scenario | Execution | Explorer |
|---|---|---|
| Wallet A registers project | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xc31b986abb9e73bbed6f043b22abb475502998903cdd67079cba27fafbb8619e) |
| Wallet B cannot open owner candidate | ERROR | [tx](https://explorer-studio.genlayer.com/tx/0x99c35af80528976ea093eead06a2cf7ba8a084410ddbb8b0815ee6a490a50827) |
| Wallet A opens report-only candidate | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x82b622778069e291d06d4c9325383d32821e9afd6aeada6bde5a6181dbe17787) |
| Wallet A adds contextual migration note | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x8e6d5b7b56b209d13ae4503c295965561022de8c9d9c6b015fe37fcaa010375f) |
| Report-only candidate cannot seal | ERROR | [tx](https://explorer-studio.genlayer.com/tx/0x2b333a8e060d6f74a7f5ef6ebc314e54bc8601bbed4c1fee41d34243c37931cb) |
| Wallet A opens compatible candidate | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x3a0d080069bf0c0db663e69e9d22a3b886c8660f34aa5a7d0239d4c036d637ed) |
| Record dependency diff | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x8e8f61f74c90e36f892a45f856ae31632489a0abd858d2fcd6ea228af5865f8e) |
| Record consumer diff | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x593784a3894f5c35d0a25f944c9e233ae847e23deb7c06cd1e4aeac44f4555a4) |
| Record regression tests | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x6c42ed551ff01dd8159654b178ce1fc2883c1503d3c66a735579a2da0bc9c541) |
| Record CI fixture | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xb584c976b05db5b3a49ff587e6c931a3afaf232bad000dd5012c4b8b3498ae25) |
| Seal exact evidence packet | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd5f07805201518abc98261b87c1f00fea2ad70235264a3e314abe3cd40666fbd) |
| Wallet B triggers compatibility review | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd2c16a53fc705b9cfb9682ee5026892f3ae4614d2321b2f8d754d0d28caac38a) |
| Wallet B cannot activate owner project | ERROR | [tx](https://explorer-studio.genlayer.com/tx/0x19359a3554cbc3a033f7989ed233c1add2f2ae4978c7b537fab9a5f2b1a8f278) |
| Wrong attestation digest rejected | ERROR | [tx](https://explorer-studio.genlayer.com/tx/0x280715653060169f5618c5410947d1e85356b0a013ecf88e14ec80110c05c8eb) |
| Wallet A activates reviewed revision | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x1b4aaae77c2b227c008e8fa7788f279abb046dcc95649fe43dc5f3af2f14585e) |
| Activation replay rejected | ERROR | [tx](https://explorer-studio.genlayer.com/tx/0xe82b944c4c0cc25181fd60bdcac66238d25cf4c6a967a6f00cd12d136990d393) |

## Authoritative outcome

- `24/24` machine-readable assertions passed.
- Report-only candidate stayed `EVIDENCE_OPEN`; failed sealing preserved its complete state.
- Exact four-slot candidate reached `COMPATIBLE`, then `ATTESTED`.
- Wrong actor and wrong attestation digest both failed with complete candidate state preserved.
- Exact owner activation advanced both active revisions from baseline to target and incremented project epoch from `1` to `2`.
- Candidate became terminal `ACTIVATED`; replay failed without mutation.
- Final open attestation count is `0`.

## Evidence boundary

The repository fixture is synthetic and intentionally co-locates two logical source trees. The run demonstrates commit/revision binding, typed evidence topology, semantic review, authorization and single-use activation state. Its CI JSON is explicitly a fixture; this evidence does not claim independently hosted CI or production deployment of the reviewed consumer.
