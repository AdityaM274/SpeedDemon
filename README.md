# Speed Demon — Track A specialist entry

Team: AdityaM274 Solo. New C++ solution started 31 October 2026 inside the coding window. OpenAI Codex generated code, tests and documentation under Aditya Mittal's direction. Organizer starter, MIT license and unmodified reference credited as pre-existing: https://github.com/hackathon-raptors/speed-demon-starter . Reference pinned at 38936f6c901f44d3cdcda9551fe9df2c84212d2b in https://github.com/hackathon-raptors/speed-demon-2026 .

Stream valid ASCII requests, keep fixed UTC hour text rather than date objects, parse integers with from_chars, group by exact hour/endpoint, retain uint32 latencies, sort for exact nearest-rank percentiles, and emit keys in byte order. No SQL/dataframe engine, approximation, seed-specific answer cache or runtime dependency. Empty input produces an empty summary; numeric and I/O failures exit nonzero. All latencies remain in memory; memory is not constant.

## Verify

    g++ -std=c++20 -O3 -Wall -Wextra -Werror track-a/main.cpp -o solution
    python3 tests/differential.py --exe ./solution --reference-root /path/to/organizer-reference

Windows: seven differential cases and three negative checks passed, covering five organizer seeds, nearest-rank boundaries, ordering, duplicates, month rollover, uint32 maximum and empty input. Published tiny hash matches. Linux/container/full-size checks subsequently passed; see the final results below.

GitHub Actions uses only a standard free public-repository Ubuntu runner. It tests native Linux correctness, prefetches allowlisted pinned images, builds offline and checks a full seed-1 hash in a network-disabled/read-only/non-root container. Five same-host native runs per program produce development timing/RSS only, not official scoring or cgroup memory. No paid runner or cloud model is used.

## Container and submission

Build context track-a; prefetch Dockerfile images, then docker build --network=none. Read /data/requests.log; write exactly /out/summary.txt. Static executable in digest-allowlisted Debian. See track-a/PERF.md. Publishing a repo is not submission. Organizer board GitHub App is installed read-only for this repo and the Track A Tally form was confirmed submitted on 31 October. No board score or rank claimed. Deadline 2 November 2026 15:00 UTC / 20:30 IST.

First Linux run completed successfully: offline Docker full-size correctness and native differential tests pass. Native same-host development measurements: 23.5533 s reference versus 0.7000 s candidate, RSS 218336 versus 44656 KiB. See track-a/PERF.md and measurements/v1-linux.json for the substantial runtime/hardware caveats. These are not official board results. The endpoint-interning candidate also passed; its final native same-host reference ratio is 43.34x (16.6133 s versus 0.383333 s), with 8.01x lower maximum RSS. Full caveats and raw measurements are in track-a/PERF.md and measurements/v2-linux.json.
