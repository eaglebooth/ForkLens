# ForkLens v3 live diagnostic

Deployment `0xdB9f31F35F45f56522dF0B5F8d49647e8643dE20` fixed the v2 consensus split but exposed a semantic false positive and must not be submitted as a working deployment.

Candidate `vault-1338499110.semantic-conflict` used consumer commit `8c39cbad349adc8c0971f441a6c0f67d76aacba6`. The patch ignored the requested protocol/chain inputs and hard-coded `vault:1`. Its tests merely approved that hard-coded behavior. Nevertheless, transaction `0xaf18e73af6b5fcefedca716013434781bd5dba96bd24aab8dada5b4bccd50735` finalized with verdict `COMPATIBLE` and created an attestation.

The attestation was never activated. ForkLens v4 strengthens both leader and validator criteria: green CI proves execution only; hard-coded dynamic values, ignored input, unconditional success, weakened verification, and tests that codify unsafe behavior must be rejected.
