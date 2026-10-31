"""Same-host development measurements; this does not produce official scores."""
import argparse
import hashlib
import json
import pathlib
import platform
import statistics
import subprocess
import sys
import tempfile
import time

p = argparse.ArgumentParser()
p.add_argument('--exe', required=True)
p.add_argument('--reference-root', required=True)
p.add_argument('--data', required=True)
p.add_argument('--report', required=True)
a = p.parse_args()
exe, ref, data = (pathlib.Path(x).resolve() for x in (a.exe, a.reference_root, a.data))
results = {}
expected_hash = None
with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    for name, command in [('reference', [sys.executable, str(ref / 'reference/a_ingest.py')]),
                          ('candidate', [str(exe)])]:
        samples = []
        for i in range(5):
            output = root / f'{name}-{i}'
            timing = root / 'time.txt'
            start = time.perf_counter()
            subprocess.run(['/usr/bin/time', '-f', '%e %M', '-o', str(timing),
                            *command, '--data', str(data), '--out', str(output)], check=True)
            elapsed, memory = timing.read_text().split()
            digest = hashlib.sha256((output / 'summary.txt').read_bytes()).hexdigest()
            if expected_hash is None:
                expected_hash = digest
            assert digest == expected_hash, f'{name}: output changed'
            samples.append({'wall_seconds': float(elapsed), 'peak_rss_kib': int(memory),
                            'outer_seconds': time.perf_counter() - start, 'sha256': digest})
        middle = sorted(s['wall_seconds'] for s in samples)[1:-1]
        results[name] = {'runs': samples, 'middle_three_mean_seconds': statistics.mean(middle),
                         'maximum_peak_rss_kib': max(s['peak_rss_kib'] for s in samples)}
result = {'scope': 'Native same-host development only; not official hardware, cgroup memory or leaderboard scoring',
          'platform': platform.platform(), 'python': sys.version, 'data_sha256': hashlib.sha256((data / 'requests.log').read_bytes()).hexdigest(),
          'measurements': results}
target = pathlib.Path(a.report)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
