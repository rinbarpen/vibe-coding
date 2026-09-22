"""Structural stage completion checks; scientific approval is an explicit attestation."""
from pathlib import Path
import argparse
import hashlib
import json


def contract_hash(stage):
    return hashlib.sha256(json.dumps(stage,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def local_file(root, name):
    root=Path(root).resolve(); path=(root/name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Contract path leaves project: '+name)
    return path


def check_stage(root, stage, registered=None):
    errors=[]; evidence=[]
    for name in stage.get('outputs',[]):
        try:
            p=local_file(root,name)
            if not p.is_file() or p.stat().st_size==0:
                errors.append('Missing or empty output: '+name); continue
            if registered is not None and name not in registered:errors.append('Output not registered in checkpoint: '+name)
            if p.suffix=='.json':json.loads(p.read_text())
            evidence.append({'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        except (OSError,ValueError) as exc:errors.append(str(exc))
    name=stage.get('review_path')
    try:
        if not name:raise ValueError('Stage has no review_path')
        report=json.loads(local_file(root,name).read_text())
        if registered is not None and name not in registered:errors.append('Review not registered in checkpoint: '+name)
        if report.get('stage_id')!=stage['id']:errors.append('Review stage ID mismatch')
        if report.get('contract_hash')!=contract_hash(stage):errors.append('Stale contract review')
        if not report.get('reviewer') or not report.get('reviewed_at'):errors.append('Review identity and date required')
        if report.get('artifacts')!=evidence:errors.append('Review output hashes mismatch')
        checks=report.get('checks',[])
        for rule in stage['acceptance']:
            if not any(c.get('criterion')==rule and c.get('status')=='pass' and c.get('evidence') for c in checks):errors.append('Unconfirmed criterion: '+rule)
        if stage.get('approval')=='human_confirmation':
            approval=report.get('approval',{})
            if approval.get('approved') is not True or not approval.get('approved_by') or not approval.get('approved_at'):errors.append('Human confirmation required')
    except (OSError,ValueError,TypeError,AttributeError) as exc:errors.append('Invalid review: '+str(exc))
    return {'stage_id':stage['id'],'status':'fail' if errors else 'pass','contract_hash':contract_hash(stage),'artifacts':evidence,'errors':errors,'scope':'File/hash and attestation checks only; scientific truth and identity are not independently verified.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project-root',type=Path,default=Path('.'));p.add_argument('--stage',required=True);a=p.parse_args()
    try:
        cfg=json.loads((a.project_root/'.auto-research/lifecycle/settings.json').read_text());s=next(s for s in cfg['stages'] if s['id']==a.stage)
        result=check_stage(a.project_root,s);print(json.dumps(result,ensure_ascii=False,indent=2));return int(result['status']!='pass')
    except (ValueError,StopIteration) as exc:print(json.dumps({'error':str(exc)}));return 1
    except OSError as exc:print(json.dumps({'error':str(exc)}));return 2


if __name__=='__main__':raise SystemExit(main())
