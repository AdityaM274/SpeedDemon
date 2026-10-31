# Performance/correctness log

## 31 October 2026 — first candidate

Hypothesis: avoid per-line datetime parsing and Python object overhead through C++ streaming, integer parsing and exact sorting. No official speedup claimed.

Windows development: five official tiny seeds, custom rank-boundary/prefix-order/duplicate/month-rollover fixture and empty file all byte-identical to reference; three negative error-path checks pass. Seed-1 tiny input hash a99dd14856a3e6e408097dabc1b3ad5ac5a3801fb12f388bacb2802c8591339f; output c24fa507c963eaeac9224fd8435019b4f4e8c002ece7e32f316681a3957eb92f. No timing inferred from correctness tests.

Linux CI/container/full-size validation and repeated timing pending first run. Save run URL, commit, raw timings, memory method, runtime/compiler and input hash after execution. Native host timing/RSS are not official hardware measurements or cgroup memory. No board run ID, official K or rank yet.

Rejected/deferred: approximate percentiles violate the contract; early group flushing is unsafe with unbounded input disorder; SIMD/parallelism add unproven complexity. Exact full sorting is the starting point. Consider selection only if measurement justifies it and differential checks still pass.

## First Linux run — 0543f76

Run: https://github.com/AdityaM274/SpeedDemon/actions/runs/41185145686 . Native Linux checks and offline Docker build/full-size sandbox hash passed. Published full seed-1 hash matched all ten benchmark outputs and the container output. Raw results: measurements/v1-linux.json.

Five runs on one standard Ubuntu 24.04 runner: reference middle-three mean 23.5533 s, maximum RSS 218336 KiB; candidate 0.7000 s, 44656 KiB. That is 33.65x lower wall time and 4.89x lower peak RSS on that development host. Reference used CPython 3.12.3, not the organizer's CPython 3.13; native candidate used runner GCC, not the static Docker binary. No official score/cgroup-memory comparison or calibrated hardware claim.

## Second candidate — endpoint interning

Hypothesis: per-request compound string keys and per-group map nodes are avoidable overhead. Intern each endpoint once, retain 72 hour slots per endpoint, and reuse the last-hour ID while still accepting arbitrary hour order. No timestamp-to-calendar assumptions; distinct hour strings are sorted before emission. Exact percentile sorting unchanged. Windows differential checks pass. Linux repeated measurement pending; keep the first candidate in Git for comparison/reversion.
