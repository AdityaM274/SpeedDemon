# Verification — 31 October 2026

Actual current candidate: 1f474b743b16a766a3c68e7614075a1ff2caa5bf. Evidence: https://github.com/AdityaM274/SpeedDemon/actions/runs/41185472564 .

- Windows and Linux: seven byte-for-byte differential cases, including five official seeds and rank/order/duplicate/month-rollover/empty fixtures; three error-path checks pass.
- Full seed-1 input 238836234 bytes, 3100000 records. Input and output hashes match the published spec. All ten native benchmark outputs and the static container output match.
- Digest-allowlisted multi-stage Docker build ran with --network=none. Runtime non-root, no network, read-only root, data read-only, out writable, 8 GiB cap, 512 pids, /tmp 1 GiB. Exactly one output file. Passed.
- Five raw native runs each for reference/candidate, compiler/CPU/runtime/commit captured in measurements/v2-linux.json. Development ratio 43.34x time and 8.01x RSS, not official scoring/cgroup memory. No real-user or production validation claimed.
- CLI engineering task: responsive/mobile UI tests are not applicable. Independent oracle is the organizer reference plus published hashes, not our implementation mirrored in a test. Test cases explicitly retain duplicate requests and unsigned 32-bit extremes.
- Main code directly inspectable, MIT starter/reference attribution retained, actual Codex role disclosed. Root .gitignore excludes generated data, binaries and local result directories. No credentials or private user files committed.
- Completed subsequently: GitHub Board App read-only single-repository installation and organizer Tally receipt on 31 October. Remaining: official board run/holdout judging and final source/dependency axes. Actual human understanding/presentation is not asserted; WALKTHROUGH.md explains the design for review.
