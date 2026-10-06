# Dependency target revision

The verifier API changes from `verify(message, signature)` to `verify(domain, message, signature)`.

`domain` is now mandatory and must bind the protocol identifier and chain identifier before signature verification. Calls that omit the domain or reuse a signature across domains must fail.
