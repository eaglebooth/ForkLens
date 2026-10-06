# Test resource manifest

Local GenVM tests use synthetic repository URLs and mocked LLM outputs to exercise contract invariants. They are not evidence that external code or CI exists.

A live StudioNet run must use commit-pinned public fixtures and record: exact deployment, source commit, two non-deployer wallets, every transaction hash, consensus/finality, complete pre/post readback for rejected calls, and final project/candidate state. The fixture matrix must include report-only, stale CI, production-only, correct implementation plus regression, cross-project substitution, stale epoch and replay.
