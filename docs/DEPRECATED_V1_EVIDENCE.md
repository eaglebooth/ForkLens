# Deprecated v1 deployment and evidence

Contract `0x81066BDd259507f1bba56579864AD8cef6aB63dD` implemented ForkLens v1. Its live run accepted caller-submitted evidence metadata and a repository-hosted synthetic CI result. That model does not meet the authoritative-source rule and is therefore deprecated.

The address, transactions, assertion counts, and fixture output from that run must not be used in a submission or described as proof of consumer migration. ForkLens v2 requires contract-fetched GitHub compare/check-run data and a fresh deployment.
