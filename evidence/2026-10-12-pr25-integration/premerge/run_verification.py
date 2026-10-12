import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('phase', choices=['premerge', 'postmerge'])
parser.add_argument('revision')
parser.add_argument('checkout')
args = parser.parse_args()
stage = Path('/dev/shm/brandkit-pr25-1955')
root = Path(args.checkout)
out = stage / 'root' / args.phase
out.mkdir(parents=True, exist_ok=False)
python = '/workspace/scratch/3af480cc2b4f/validation/asset-venv/bin/python'
base = 'e254df5444f0bfedd5526b0e148b0cdf36cbd31f'
candidate = 'aa22b3833a7510e1ece215926faab6c6394e5258'
expected_paths = ['docs/architecture/ACCEPTANCE.md', 'docs/architecture/OWNERSHIP.md', 'docs/source-of-truth.md']

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=root, text=True).strip()

def tracked(ref):
    result = {}
    for row in git('ls-tree', '-r', ref).splitlines():
        meta, path = row.split('\t', 1)
        mode, kind, blob = meta.split()
        result[path] = {'mode': mode, 'type': kind, 'blob': blob}
    return result

head = git('rev-parse', 'HEAD')
if head != args.revision or git('status', '--porcelain=v1', '--untracked-files=all'):
    raise SystemExit('Unexpected source revision or dirty checkout')
before = tracked(base)
after = tracked(head)
changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
report = {
    'record_type': 'local Brand documentation verification; not an acceptance schema',
    'repository': 'Jevelopers-neatHack-2026/brand-kit',
    'phase': args.phase,
    'source_revision': head,
    'source_tree': git('rev-parse', 'HEAD^{tree}'),
    'base_revision': base,
    'reviewed_candidate_revision': candidate,
    'reviewed_candidate_tree': git('rev-parse', candidate + '^{tree}'),
    'parents': git('show', '-s', '--format=%P', head).split(),
    'tracked_file_count': len(after),
    'changed_paths_from_prior_main': changed,
    'unchanged_tracked_file_count': sum(before.get(p) == row for p, row in after.items()),
    'clean_before': True,
    'started_at_utc': now(),
    'captured_by': 'brand-kit execution supervisor /root',
    'environment': {
        'cwd': str(root),
        'PYTHON': python,
        'PLAYWRIGHT_BROWSERS_PATH': '/tmp/ticketstub-browser-1194',
        'TMPDIR': str(stage / 'tmp'),
        'npm_config_logs_dir': str(stage / 'npm-logs'),
    },
    'execution_mode': 'local source verification; negative fixture data explicitly synthetic',
    'provider_mode': 'N/A: no font, application, paid, sandbox, or live provider operation',
    'provider_budget_cost': 'N/A for absent provider operations; no product or development-cost claim',
    'storage_note': 'Overlay filesystem is full; isolated checkout, temporary outputs and evidence use available memory-backed storage without deleting other writers files.',
    'commands': [],
    'reused_evidence': {
        'exact_candidate_full_suite': 'https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/04cbe9d6eb6c7cc650fe570a20bc66e6f12fd830/evidence/2026-10-12-bk-mvp/late-owner-aa22/README.md',
        'historical_full_release_gate': 'https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/cd744af6da5b1f89f410383fac5937e1ea8d6705/evidence/2026-10-12-bk10-candidate-binding/postmerge/README.md',
    },
    'not_executed': [
        'Full 17-target release gate: prior run remains pinned to 41001e1 with 14 passes, three failures, 30 blockers and release_approved=false.',
        'Approved-font provider availability, true browser UI zoom, assistive-technology and accountable visual/content acceptance remain missing; no pass inferred.',
        'General external URL probing: local checker reports these unchecked; specific required GitHub targets have separate source observations.',
        'Foreign Product runtime suite: only live GitHub status inspected, not rerun here.',
    ],
    'release_approved': False,
    'master_acceptance_changed': False,
}
env = os.environ.copy()
env.update({k: v for k, v in report['environment'].items() if k != 'cwd'})

def save():
    (out / 'execution.json').write_text(json.dumps(report, indent=2) + '\n')

def run(label, argv, cwd=None, expected=0, acceptance_failure=False):
    began = now()
    clock = time.monotonic()
    result = subprocess.run(argv, cwd=cwd or root, env=env, capture_output=True)
    index = len(report['commands']) + 1
    stdout_name = f'{index:02d}-{label}.stdout.txt'
    stderr_name = f'{index:02d}-{label}.stderr.txt'
    (out / stdout_name).write_bytes(result.stdout)
    (out / stderr_name).write_bytes(result.stderr)
    item = {
        'label': label, 'argv': argv, 'cwd': str(cwd or root),
        'source_revision': head, 'started_at_utc': began, 'finished_at_utc': now(),
        'elapsed_seconds': round(time.monotonic() - clock, 6),
        'expected_exit_code': expected, 'actual_exit_code': result.returncode,
        'outcome': 'passed' if result.returncode == 0 else 'failed',
        'expected_missing_acceptance_observed': acceptance_failure and result.returncode == expected,
        'stdout': stdout_name, 'stdout_sha256': sha256(result.stdout),
        'stderr': stderr_name, 'stderr_sha256': sha256(result.stderr),
    }
    report['commands'].append(item)
    save()
    print(json.dumps({k: item[k] for k in ['label', 'actual_exit_code', 'outcome', 'elapsed_seconds']}), flush=True)

run('python-version', [python, '-VV'])
run('asset-library-versions', [python, '-c', 'import importlib.metadata,json; print(json.dumps({n:importlib.metadata.version(n) for n in ("fonttools","uharfbuzz","Pillow")},sort_keys=True))'])
run('diff-check', ['git', 'diff', '--check', base, head])
if args.phase == 'premerge':
    run('affected-documentation-checks', ['make', 'check-inventory', 'check-links', 'check-governance', 'check-guidelines'])
else:
    run('inkscape-version', ['inkscape', '--version'])
    run('node-version', ['node', '--version'])
    run('npm-version', ['npm', '--version'])
    run('make-check', ['make', 'check'])
    run('check-package', ['make', 'check-package'])
    run('install-pinned-tailwind-offline', ['npm', 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=root / 'tools/tokens-dev')
    run('check-consumers-local', ['make', 'check-consumers-local'])
    run('check-provenance', ['make', 'check-provenance'], expected=2, acceptance_failure=True)
    run('package-brand', ['make', 'package-brand'], expected=2, acceptance_failure=True)
    run('check-consumers', ['make', 'check-consumers'], expected=2, acceptance_failure=True)
report['finished_at_utc'] = now()
report['clean_after'] = git('status', '--porcelain=v1', '--untracked-files=all') == ''
report['final_source_revision'] = git('rev-parse', 'HEAD')
report['candidate_tree_matches_source'] = report['source_tree'] == report['reviewed_candidate_tree']
report['documentation_verification_passed'] = all([
    all(c['actual_exit_code'] == c['expected_exit_code'] for c in report['commands']),
    report['clean_after'], head == report['final_source_revision'],
    report['candidate_tree_matches_source'], changed == expected_paths,
])
save()
(out / 'source-tree.json').write_text(json.dumps(after, indent=2, sort_keys=True) + '\n')
(out / 'changed-source.diff').write_bytes(subprocess.check_output(['git', 'diff', base, head, '--', *expected_paths], cwd=root))
print(json.dumps({'phase': args.phase, 'documentation_verification_passed': report['documentation_verification_passed'], 'release_approved': False, 'execution_sha256': sha256((out / 'execution.json').read_bytes())}), flush=True)
raise SystemExit(0 if report['documentation_verification_passed'] else 1)
