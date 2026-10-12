import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/workspace/scratch/3af480cc2b4f/postmerge-docs-e254df5')
OUT = Path('/workspace/scratch/3af480cc2b4f/validation/resume-20261012-1832/postmerge-e254df5')
PYTHON = '/workspace/scratch/3af480cc2b4f/validation/asset-venv/bin/python'
EXPECTED = 'e254df5444f0bfedd5526b0e148b0cdf36cbd31f'
PRIOR = '41001e1875c544d21ad6b481cfe98c9283b0c58c'
CANDIDATE = '1603948d569ae2eb48693d7f4a40cce45b8111b1'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def tracked(ref):
    result = {}
    for line in git('ls-tree', '-r', ref).splitlines():
        meta, path = line.split('\t', 1)
        mode, kind, sha = meta.split()
        result[path] = {'mode': mode, 'kind': kind, 'blob': sha}
    return result

OUT.mkdir(parents=True, exist_ok=False)
head = git('rev-parse', 'HEAD')
if head != EXPECTED or git('status', '--porcelain=v1'):
    raise SystemExit('Refuse to test an unexpected or dirty source revision')
before = tracked(PRIOR)
after = tracked(head)
changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
report = {
    'record_type': 'local repository postmerge verification; not an acceptance schema',
    'repository': 'Jevelopers-neatHack-2026/brand-kit',
    'issue_refs': ['Refs #5', 'Refs #28'],
    'acceptance_ids': 'N/A: documentation and local package verification; no master acceptance decision',
    'source_revision': head,
    'source_tree': git('rev-parse', 'HEAD^{tree}'),
    'merged_candidate_revision': CANDIDATE,
    'merged_candidate_tree': git('rev-parse', CANDIDATE + '^{tree}'),
    'prior_verified_revision': PRIOR,
    'prior_immutable_evidence': 'https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/cd744af6da5b1f89f410383fac5937e1ea8d6705/evidence/2026-10-12-bk10-candidate-binding/postmerge/README.md',
    'tracked_file_count': len(after),
    'changed_paths_from_prior_main': changed,
    'unchanged_tracked_file_count': sum(before.get(p) == item for p, item in after.items()),
    'source_index_sha256': digest((ROOT / 'docs/source-of-truth.md').read_bytes()),
    'clean_before': True,
    'started_at_utc': now(),
    'captured_by': 'brand-kit execution supervisor /root; postmerge command evidence only',
    'environment': {
        'cwd': str(ROOT),
        'PYTHON': PYTHON,
        'PLAYWRIGHT_BROWSERS_PATH': '/tmp/ticketstub-browser-1194',
    },
    'evidence_origin': 'fresh local execution against exact committed public repository source; negative-test inputs are independently synthetic fixtures',
    'execution_mode': 'local/offline source checks and synthetic unit tests',
    'provider_mode': 'N/A: no font, paid, live or sandbox provider request',
    'provider_budget_cost_usage': 'N/A: no provider operation occurred; no claim about product costs',
    'access_class': 'public repository command evidence, subject to publication review',
    'commands': [],
    'not_rerun': [
        'Full 17-target BK-10 release gate: code and all fixtures unchanged; the actual 41001e1 gate result remains historical BLOCKED with 30 blockers, 14 passes and 3 failures.',
        'Actual approved-font available/unavailable, real browser UI 200% zoom, assistive technology and manual visual/channel/claims acceptance: required inputs/owners still absent; no pass inferred.',
        'External navigation URLs: not probed by local link checker; separately scoped GitHub target diagnostics are separate records.',
    ],
    'release_approved': False,
}

env = os.environ.copy()
env.update(report['environment'])
env.pop('cwd', None)

def run(label, argv, expected=0):
    index = len(report['commands']) + 1
    start = now()
    timer = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    stdout_name = f'{index:02d}-{label}.stdout.txt'
    stderr_name = f'{index:02d}-{label}.stderr.txt'
    (OUT / stdout_name).write_bytes(result.stdout)
    (OUT / stderr_name).write_bytes(result.stderr)
    item = {
        'label': label, 'argv': argv, 'cwd': str(ROOT),
        'source_revision': head, 'started_at_utc': start,
        'finished_at_utc': now(), 'elapsed_seconds': round(time.monotonic() - timer, 6),
        'expected_exit_code': expected, 'actual_exit_code': result.returncode,
        'outcome': 'pass' if result.returncode == expected else 'fail',
        'stdout': stdout_name, 'stdout_sha256': digest(result.stdout),
        'stderr': stderr_name, 'stderr_sha256': digest(result.stderr),
    }
    report['commands'].append(item)
    (OUT / 'execution.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'label': label, 'exit_code': result.returncode, 'elapsed_seconds': item['elapsed_seconds']}), flush=True)
    return result.returncode

run('python-version', [PYTHON, '-VV'])
run('asset-library-versions', [PYTHON, '-c', 'import importlib.metadata,json; print(json.dumps({n:importlib.metadata.version(n) for n in ("fonttools","uharfbuzz","Pillow")},sort_keys=True))'])
run('inkscape-version', ['inkscape', '--version'])
run('diff-check', ['git', 'diff', '--check', PRIOR, head])
run('make-check', ['make', 'check'])
run('check-package', ['make', 'check-package'])
report['clean_after'] = git('status', '--porcelain=v1') == ''
report['final_source_revision'] = git('rev-parse', 'HEAD')
report['finished_at_utc'] = now()
report['candidate_tree_matches_main'] = report['source_tree'] == report['merged_candidate_tree']
report['checks_passed'] = all(c['outcome'] == 'pass' for c in report['commands'])
report['postmerge_verification_passed'] = all([
    report['checks_passed'], report['clean_after'],
    report['final_source_revision'] == EXPECTED,
    report['candidate_tree_matches_main'],
    changed == ['docs/source-of-truth.md'],
])
(OUT / 'execution.json').write_text(json.dumps(report, indent=2) + '\n')
(OUT / 'source-tree.json').write_text(json.dumps(after, indent=2, sort_keys=True) + '\n')
(OUT / 'changed-source.diff').write_text(subprocess.check_output(['git','diff',PRIOR,head,'--','docs/source-of-truth.md'],cwd=ROOT,text=True))
print(json.dumps({'postmerge_verification_passed': report['postmerge_verification_passed'], 'clean_after': report['clean_after'], 'source_revision': head, 'execution_sha256': digest((OUT / 'execution.json').read_bytes())}), flush=True)
sys.exit(0 if report['postmerge_verification_passed'] else 1)
