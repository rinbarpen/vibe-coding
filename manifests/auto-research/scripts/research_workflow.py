#!/usr/bin/env python3
"""Local research lifecycle ledger. No model calls, deployments or remote Git pushes."""
from __future__ import annotations
import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid

RUNTIME = Path('.auto-research/lifecycle')
STATES = {'started', 'completed', 'failed', 'blocked', 'paused', 'resumed', 'skipped', 'revised'}
TERMINAL = {'completed', 'skipped'}
ACTIVE = {'started', 'resumed', 'revised'}

class Invalid(ValueError):
    pass

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

def save(path, value):
    atomic(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def git(root, *args, check=True):
    p = subprocess.run(['git', '--literal-pathspecs', '-C', str(root), *args], capture_output=True, text=True)
    if check and p.returncode:
        raise Invalid(p.stderr.strip() or p.stdout.strip() or 'Git command failed')
    return p.stdout.strip()

def relative(root, name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] == '.git':
        raise Invalid('Expected a project-relative artifact path: ' + str(name))
    resolved = (root / p).resolve()
    if not resolved.is_relative_to(root): raise Invalid('Artifact escapes project: ' + str(name))
    if (root / p).is_symlink(): raise Invalid('Register the actual artifact, not a symlink: ' + str(name))
    return p.as_posix()

@contextlib.contextmanager
def lock(root):
    path = root / RUNTIME / 'local' / 'lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as f:
        try: fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise Invalid('Another checkpoint writer is active; retry after it finishes')
        try: yield
        finally: fcntl.flock(f, fcntl.LOCK_UN)

def config(root):
    cfg = read(root / RUNTIME / 'settings.json')
    if cfg.get('version') != 1: raise Invalid('Unknown lifecycle version')
    ids = {s['id'] for s in cfg['stages']}
    if len(ids) != len(cfg['stages']): raise Invalid('Duplicate stage ID')
    for s in cfg['stages']:
        if s['level'] not in (1,2,3): raise Invalid('Only three lifecycle levels are supported')
        if s['parent_id'] and s['parent_id'] not in ids: raise Invalid('Missing parent stage')
        if s['parent_id']:
            parent = next(x for x in cfg['stages'] if x['id'] == s['parent_id'])
            if parent['level'] != s['level'] - 1: raise Invalid('Invalid stage hierarchy')
        elif s['level'] != 1: raise Invalid('Non-root stage requires parent')
    return cfg

def events(root):
    p = root / RUNTIME / 'events.jsonl'
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []

def committed(root, checkpoint_id):
    return git(root, 'log', '--all', '--format=%H', '--fixed-strings', '--grep=Checkpoint-ID: ' + checkpoint_id, check=False).splitlines()

def latest(root, cycle):
    result = {}
    for e in events(root):
        if e['cycle'] == cycle: result[e['stage_id']] = e
    return result

def route(cfg, role, actual=None):
    requested = cfg['roles'].get(role)
    binding = cfg.get('bindings', {}).get(role)
    if not requested or not binding or not binding.get('available') or not binding.get('verified_at'):
        raise Invalid('blocked_model_unavailable: explicit verified binding required for ' + role)
    if not binding.get('provider') or not binding.get('model_id'):
        raise Invalid('blocked_model_unavailable: provider/model_id required')
    if binding.get('reasoning_effort') != requested.get('reasoning_effort') or binding.get('service_profile') != requested.get('service_profile'):
        raise Invalid('blocked_model_unavailable: binding does not match requested effort/profile')
    if actual is not None and actual != binding['model_id']:
        raise Invalid('Actual model differs from verified role binding')
    return {'requested': requested, 'binding': binding}

def init(root):
    root.mkdir(parents=True, exist_ok=True)
    repo = git(root, 'rev-parse', '--show-toplevel', check=False)
    if repo and Path(repo).resolve() != root:
        raise Invalid('Initialize at the research Git root, not inside an enclosing repository')
    if not repo: git(root, 'init')
    with lock(root):
        settings = root / RUNTIME / 'settings.json'
        if not settings.exists():
            defaults = Path(__file__).resolve().parents[1] / 'lifecycle/defaults.json'
            save(settings, read(defaults))
        ignore = root / RUNTIME / '.gitignore'
        if not ignore.exists(): atomic(ignore, 'local/\n')
        for d in ['refine-logs/history','logs/runs','results']: (root / d).mkdir(parents=True, exist_ok=True)
    return {'status': 'initialized', 'settings': str(settings), 'models': 'bindings must be verified by execution host'}

SECRET = re.compile(r'(?:sk-[A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY|(?:api[_-]?key|token|password)\s*[=:]\s*["\']?[^\s"\']{8,})', re.I)

def check_text(text):
    if SECRET.search(text): raise Invalid('Potential credential detected; register a redacted copy')

def verify_archive(root, index):
    if index.get('version') != 1 or index.get('kind') != 'archive_index':
        raise Invalid('Expected version 1 archive_index')
    if not index.get('artifacts'): raise Invalid('Archive index is empty')
    for item in index['artifacts']:
        location=item.get('path','')
        if '://' in location: raise Invalid('Remote archive must be mounted locally for verification')
        path=Path(location)
        if not path.is_absolute(): path=root/path
        if not path.is_file(): raise Invalid('Archive is not readable: '+location)
        if item.get('availability') not in {'local_only','archived'}: raise Invalid('Declare archive availability')
        if not item.get('checked_at') or not item.get('created_at'): raise Invalid('Archive timestamps required')
        sha=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024), b''): sha.update(chunk)
        if sha.hexdigest()!=item.get('sha256') or path.stat().st_size!=item.get('bytes'):
            raise Invalid('Archive checksum/size mismatch: '+location)
    return {'valid':True,'verified_artifacts':len(index['artifacts'])}


def checkpoint(root, a):
    with lock(root):
        pending = root / RUNTIME / 'local/pending.json'
        if pending.exists(): raise Invalid('Pending checkpoint exists; run resume before creating another')
        cfg = config(root)
        check_text(json.dumps(cfg))
        stages = {s['id']: s for s in cfg['stages']}
        if a.stage not in stages: raise Invalid('Unknown stage: ' + a.stage)
        if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}', a.cycle): raise Invalid('Invalid cycle ID')
        st = stages[a.stage]; state = latest(root, a.cycle); prior = state.get(a.stage)
        if a.state == 'started' and prior: raise Invalid('Stage already exists in cycle; resume or use a new cycle')
        if a.state not in {'started','skipped'} and not prior and not (a.state == 'blocked' and a.summary.startswith('blocked_model_unavailable')): raise Invalid('Record started before this transition')
        if prior and prior['state'] in TERMINAL: raise Invalid('Terminal stage requires a new cycle')
        if a.state == 'resumed' and prior['state'] not in {'paused','failed','blocked'}: raise Invalid('Resume requires paused/failed/blocked state')
        if a.state not in {'started','skipped','resumed'} and prior and prior['state'] not in ACTIVE:
            raise Invalid('Resume inactive stage before further transitions')
        if st['parent_id'] and state.get(st['parent_id'],{}).get('state') not in ACTIVE:
            raise Invalid('Start/resume parent stage first')
        if a.state == 'completed':
            children = [s for s in cfg['stages'] if s['parent_id'] == a.stage]
            if any(state.get(s['id'],{}).get('state') not in TERMINAL for s in children):
                raise Invalid('Complete or explicitly skip all child stages first')
            if st.get('required_evidence') and not a.artifact: raise Invalid('Receipt/decision evidence required')
        if not a.summary or not a.next: raise Invalid('Summary/reason and next action are required')
        # A missing model is itself recordable; all other events need verified execution identity.
        model = {'requested': cfg['roles'].get(a.role), 'actual_model': a.actual_model}
        if a.state == 'blocked' and a.summary.startswith('blocked_model_unavailable'):
            pass
        else:
            model.update(route(cfg, a.role, a.actual_model))
            if not a.actual_model: raise Invalid('Actual execution model is required')
        if git(root, 'diff', '--name-only', '--diff-filter=U'): raise Invalid('Resolve Git conflicts before checkpointing')
        for key in ('user.name','user.email'):
            if not git(root,'config','--get',key,check=False): raise Invalid('Configure project Git ' + key)
        registered = sorted(set(relative(root,n) for n in a.artifact))
        records=[]; cp='cp-' + uuid.uuid4().hex
        snapshot=[]
        for name in registered:
            p=root/name
            if not p.is_file(): raise Invalid('Missing artifact: '+name)
            if p.stat().st_size > cfg['max_git_file_bytes']: raise Invalid('Large artifact: register an archive index instead: '+name)
            try: content=p.read_text(encoding='utf-8')
            except UnicodeError: raise Invalid('Binary artifact: register archive index instead: '+name)
            check_text(content)
            if p.suffix == '.json':
                try: candidate=json.loads(content)
                except json.JSONDecodeError: candidate=None
                if isinstance(candidate,dict) and candidate.get('kind')=='archive_index': verify_archive(root,candidate)
            records.append({'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
            if a.state == 'revised' or p.suffix in {'.md','.json','.yaml','.yml','.toml'}:
                dest=f'refine-logs/history/{a.cycle}/{cp}/{name}'
                snapshot.append((dest,content))
        event={'checkpoint_id':cp,'stage_id':a.stage,'parent_id':st['parent_id'],'level':st['level'],
               'execution_id':prior['execution_id'] if prior else 'exec-'+uuid.uuid4().hex,
               'cycle':a.cycle,'state':a.state,'time':now(),'role':a.role,'model':model,
               'summary':a.summary,'next':a.next,'inputs':a.input,'artifacts':records,
               'command':a.command,'run_ids':a.run_id,'submission_id':a.submission_id,'revision_id':a.revision_id}
        check_text(json.dumps(event))
        paths=registered+[str(RUNTIME/'events.jsonl'),str(RUNTIME/'settings.json'),str(RUNTIME/'.gitignore')]+[p for p,_ in snapshot]
        # Existing unrelated index entries remain untouched: commit --only uses an explicit pathspec.
        msg=f'research[{a.stage}]: {a.state}\n\nCheckpoint-ID: {cp}\nCycle: {a.cycle}\n{a.summary}'
        journal={'checkpoint_id':cp,'paths':paths,'message':msg,'event':event,'snapshots':snapshot}
        save(pending,journal)
        return finish_pending(root,journal)

def finish_pending(root,journal):
    cp=journal['checkpoint_id']; p=root/RUNTIME/'events.jsonl'
    commits=committed(root,cp)
    if not commits:
        for name,content in journal['snapshots']: atomic(root/name,content)
        old=p.read_text(encoding='utf-8') if p.exists() else ''
        if not any(e['checkpoint_id']==cp for e in events(root)):
            atomic(p,old+json.dumps(journal['event'],ensure_ascii=False,sort_keys=True)+'\n')
        paths=journal['paths']
        for record in journal['event']['artifacts']:
            artifact=root/record['path']
            if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest()!=record['sha256']:
                raise Invalid('Pending artifact changed; restore recorded artifact before resume: '+record['path'])
        git(root,'add','--',*paths)
        git(root,'commit','--only','-m',journal['message'],'--',*paths)
        commits=committed(root,cp)
    if not commits: raise Invalid('Checkpoint commit not found')
    (root/RUNTIME/'local/pending.json').unlink(missing_ok=True)
    return {'checkpoint_id':cp,'commit':commits[0],'status':'committed'}

def status(root,cycle):
    cfg=config(root); state=latest(root,cycle)
    pending=root/RUNTIME/'local/pending.json'
    return {'cycle':cycle,'pending_checkpoint':read(pending)['checkpoint_id'] if pending.exists() else None,
            'stages':[{'id':s['id'],'parent_id':s['parent_id'],'level':s['level'],
                       'state':state.get(s['id'],{}).get('state','not_started')} for s in cfg['stages']]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--project-root',type=Path,default=Path('.'))
    sub=p.add_subparsers(dest='action',required=True)
    sub.add_parser('init')
    ap=sub.add_parser('archive-check'); ap.add_argument('index',type=Path)
    for name in ['status','resume']:
        sp=sub.add_parser(name); sp.add_argument('--cycle',default='cycle-001')
    rp=sub.add_parser('route'); rp.add_argument('role',choices=['research','planner','executor','writer'])
    cp=sub.add_parser('checkpoint')
    cp.add_argument('--stage',required=True); cp.add_argument('--state',choices=sorted(STATES),required=True)
    cp.add_argument('--cycle',default='cycle-001'); cp.add_argument('--role',choices=['research','planner','executor','writer'],required=True)
    cp.add_argument('--actual-model'); cp.add_argument('--summary',required=True); cp.add_argument('--next',required=True)
    for key in ['artifact','input','run-id']: cp.add_argument('--'+key,action='append',default=[])
    for key in ['command','submission-id','revision-id']: cp.add_argument('--'+key)
    a=p.parse_args(argv); root=a.project_root.resolve()
    try:
        if a.action=='init': result=init(root)
        elif a.action=='archive-check': result=verify_archive(root,read(a.index))
        elif a.action=='route': result=route(config(root),a.role)
        elif a.action=='status': result=status(root,a.cycle)
        elif a.action=='checkpoint': result=checkpoint(root,a)
        else:
            with lock(root):
                pending=root/RUNTIME/'local/pending.json'
                result=finish_pending(root,read(pending)) if pending.exists() else status(root,a.cycle)
                result['resume_instruction']='Reconcile recorded run IDs with live process/queue and output files before launching; do not infer completion from tracker alone.'
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (Invalid, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)},ensure_ascii=False)); return 1
    except OSError as exc:
        print(json.dumps({'status':'tool_error','error':str(exc)},ensure_ascii=False)); return 2

if __name__=='__main__': sys.exit(main())
