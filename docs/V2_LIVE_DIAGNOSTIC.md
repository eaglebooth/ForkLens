# ForkLens v2 live diagnostic

Deployment `0x207714cED8C00dEEE02ad39B01CF37753216dB0c` exposed a consensus defect and must not be submitted as a working deployment.

Transaction `0x98aa9123b74eb75ac94a9d88c65c0b448cf0ad379c5fbfedae092ec18229a7f1` assessed the missing-production candidate. Every execution returned `INSUFFICIENT_EVIDENCE`, but the transaction ended `UNDETERMINED` with a 2–3 validator split. Receipts warned that storage classes were read inside nondeterministic mode, and deterministic failure proposals were unnecessarily sent through LLM validation.

ForkLens v3 fixes the cause by copying storage fields into plain snapshots before entering nondeterministic consensus and by validating source-unavailable/path/CI failures with deterministic predicates. A fresh deployment is required.
