# Track A C++20 solution

main.cpp is our new implementation, standard library only, dependency_count=0. Docker compiles statically with digest-allowlisted GCC and copies only the binary into digest-allowlisted Debian. It runs /solution; --data and --out overrides exist for developer tests only.

Fixed-format UTC hour text avoids general date conversion. Exact uint32 latencies are grouped by hour/endpoint and sorted; integer nearest-rank percentiles and floor error ppm match the published contract. Group keys sort as ASCII bytes, including proper prefixes. No input-order bound, deduplication or approximate quantile assumption. Input grammar is the organizer's well-formed ASCII contract, not arbitrary log syntax. Numeric/I/O failures exit nonzero. All input latency values are retained in memory.

The unmodified a_ingest.py/run.py are credited organizer references; our Docker entrypoint runs only compiled main.cpp. Current validation is in root README and PERF.md. Next: verify Linux/container execution, then optimize a measured bottleneck. No SIMD or parallelism until evidence supports the extra code. Do not extrapolate leaderboard ranks from CI host timing.

31 October second candidate: endpoint names interned once, 72 hour slots per endpoint and cached last-hour lookup; final hours/endpoints sorted independently. No per-request compound string allocation. This replaces the first implementation map layout without changing output semantics.
