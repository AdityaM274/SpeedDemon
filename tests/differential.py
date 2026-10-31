"""Compare our executable to the pinned organizer reference, not a copied algorithm."""
import argparse
import hashlib
import json
import pathlib
import random
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--exe', required=True)
p.add_argument('--reference-root', required=True)
p.add_argument('--report')
a = p.parse_args()
exe = str(pathlib.Path(a.exe).resolve())
ref = pathlib.Path(a.reference_root).resolve()
results = []


def compare(data, root, label):
    expected, actual = root / 'expected', root / 'actual'
    subprocess.run([sys.executable, str(ref / 'reference/a_ingest.py'),
                    '--data', str(data), '--out', str(expected)], check=True)
    subprocess.run([exe, '--data', str(data), '--out', str(actual)], check=True)
    x, y = (expected / 'summary.txt').read_bytes(), (actual / 'summary.txt').read_bytes()
    assert x == y, f'{label}: output differs'
    results.append({'case': label, 'bytes': len(y), 'sha256': hashlib.sha256(y).hexdigest()})


with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    for seed in [1, 2, 17, 101, 20261031]:
        case = root / f'tiny-{seed}'
        data = case / 'data'
        subprocess.run([sys.executable, str(ref / 'generators/a_ingest.py'),
                        '--seed', str(seed), '--scale', 'tiny', '--out', str(data)], check=True)
        compare(data, case, f'official-tiny-seed-{seed}')
    case = root / 'edges'
    data = case / 'data'
    data.mkdir(parents=True)
    lines = []
    rng = random.Random(317)
    for n in [1, 2, 3, 4, 49, 50, 99, 100, 101, 199, 200, 201]:
        for endpoint in ['/', '/v2/orders', '/v2/orders-export', '/v2/orders.csv',
                         '/v2/orders/{id}', '/v2/ordersByDate', '/A', '/a']:
            for i in range(n):
                stamp = '2026-10-31T23' if n % 2 else '2026-11-01T00'
                latency = [0, 1, 4294967295, rng.randrange(2**32)][i % 4]
                status = [100, 200, 499, 500, 599][i % 5]
                lines.append(f'{stamp}:59:59.999999Z GET {endpoint}/{n} {status} {latency}\n')
    lines += lines[:9]  # Duplicate requests must count, not disappear.
    rng.shuffle(lines)
    (data / 'requests.log').write_bytes(''.join(lines).encode('ascii'))
    compare(data, case, 'rank-boundaries-prefix-order-rollover-duplicates')
    (data / 'requests.log').write_bytes(b'')
    compare(data, case, 'empty-input')
    for bad in [b'broken\n', b'2026-10-30T18:00:00.000000Z GET / 200 4294967296\n']:
        (data / 'requests.log').write_bytes(bad)
        result = subprocess.run([exe, '--data', str(data), '--out', str(case / 'invalid')],
                                capture_output=True)
        assert result.returncode != 0, 'invalid input silently accepted'
    missing = subprocess.run([exe, '--data', str(root / 'missing')], capture_output=True)
    assert missing.returncode != 0, 'missing input silently accepted'
report = {'differential_cases': results, 'negative_cases_passed': 3,
          'scope': 'Development correctness checks, not official scoring or real-user validation'}
if a.report:
    target = pathlib.Path(a.report)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
