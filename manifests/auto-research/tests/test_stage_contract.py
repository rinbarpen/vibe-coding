import json
import sys
from pathlib import Path
from types import SimpleNamespace
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import stage_contract as sc
import research_workflow as rw


def test_every_substage_has_specific_contract():
    cfg=json.loads((ROOT/'lifecycle/defaults.json').read_text());nodes=cfg['stages'];ids={s['id'] for s in nodes}
    assert cfg['enforce_stage_contracts'] is True
    assert len([s for s in nodes if s['level']==3])==71
    for s in nodes:
        if s['level']==1:continue
        for field in ['inputs','outputs','activities','acceptance','roles','return_to','approval','handoff']:assert s[field],(s['id'],field)
        assert all(target in ids for target in s['return_to'].values())
        if s['level']==3:assert s['review_path'] and s['failure_policy'] and s['checkpoint']


def setup(root,human=False):
    stage={'id':'startup/scope/question','level':3,'outputs':['answer.json'],'acceptance':['Question is falsifiable'],'review_path':'review.json','approval':'human_confirmation' if human else 'auto'}
    (root/'answer.json').write_text('{"question":"fixture"}')
    initial=sc.check_stage(root,stage)
    report={'stage_id':stage['id'],'contract_hash':sc.contract_hash(stage),'reviewer':'fixture-reviewer','reviewed_at':'2026-09-20','artifacts':initial['artifacts'],'checks':[{'criterion':stage['acceptance'][0],'status':'pass','evidence':'fixture comparison'}]}
    (root/'review.json').write_text(json.dumps(report));return stage,report


def test_missing_outputs_and_review_fail(tmp_path):
    s,_=setup(tmp_path);(tmp_path/'answer.json').unlink();(tmp_path/'review.json').unlink();assert sc.check_stage(tmp_path,s)['status']=='fail'


def test_current_review_passes_and_changed_content_invalidates(tmp_path):
    s,_=setup(tmp_path);assert sc.check_stage(tmp_path,s,{'answer.json','review.json'})['status']=='pass'
    (tmp_path/'answer.json').write_text('{"question":"changed"}');assert sc.check_stage(tmp_path,s)['status']=='fail'


def test_changed_contract_and_missing_registration_fail(tmp_path):
    s,_=setup(tmp_path);assert sc.check_stage(tmp_path,s,set())['status']=='fail'
    s['acceptance'].append('Extra criterion');assert sc.check_stage(tmp_path,s)['status']=='fail'


def test_human_approval_required(tmp_path):
    s,r=setup(tmp_path,True);assert sc.check_stage(tmp_path,s)['status']=='fail'
    r['approval']={'approved':True,'approved_by':'fixture-human','approved_at':'2026-09-20'};(tmp_path/'review.json').write_text(json.dumps(r));assert sc.check_stage(tmp_path,s)['status']=='pass'


def test_traversal_rejected(tmp_path):
    s,_=setup(tmp_path);s['outputs']=['../secret'];assert sc.check_stage(tmp_path,s)['status']=='fail'


def test_checkpoint_enforces_contract_before_git(tmp_path):
    rw.init(tmp_path);cfg=rw.config(tmp_path)
    target=next(s for s in cfg['stages'] if s['id']=='startup/scope/question')
    # Supply active ancestors directly to isolate the completion gate from Git transition tests.
    events=[{'stage_id':id,'state':'started','cycle':'cycle-001','execution_id':id} for id in ['startup','startup/scope',target['id']]]
    (tmp_path/rw.RUNTIME/'events.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
    a=SimpleNamespace(stage=target['id'],state='completed',cycle='cycle-001',artifact=['absent.json'],summary='fixture',next='continue')
    with pytest.raises(rw.Invalid,match='Missing or empty output'):rw.checkpoint(tmp_path,a)


def test_strict_checkpoint_success_and_review_snapshot(tmp_path):
    rw.init(tmp_path);rw.git(tmp_path,'config','user.name','Fixture');rw.git(tmp_path,'config','user.email','fixture@example.test')
    cfg=rw.config(tmp_path);request=cfg['roles']['research'];cfg['bindings']['research']={'provider':'fixture','model_id':'fixture-research','service_profile':request['service_profile'],'reasoning_effort':request['reasoning_effort'],'available':True,'verified_at':'2026-09-20'}
    rw.save(tmp_path/rw.RUNTIME/'settings.json',cfg)
    def cp(id,state,artifacts=()):
        return rw.checkpoint(tmp_path,SimpleNamespace(stage=id,state=state,cycle='cycle-001',role='research',actual_model='fixture-research',summary='FIXTURE contract test',next='continue',artifact=list(artifacts),input=[],run_id=[],command=None,submission_id=None,revision_id=None))
    for id in ['startup','startup/scope','startup/scope/question']:cp(id,'started')
    stage=next(s for s in cfg['stages'] if s['id']=='startup/scope/question')
    for name in stage['outputs']:
        p=tmp_path/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('FIXTURE: scoped falsifiable question, not a research result.')
    report={'stage_id':stage['id'],'contract_hash':sc.contract_hash(stage),'reviewer':'fixture-reviewer','reviewed_at':'2026-09-20','artifacts':sc.check_stage(tmp_path,stage)['artifacts'],'checks':[{'criterion':c,'status':'pass','evidence':'fixture-only attestation'} for c in stage['acceptance']]}
    p=tmp_path/stage['review_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report))
    result=cp(stage['id'],'completed',stage['outputs']+[stage['review_path']])
    assert result['commit']
    assert list((tmp_path/'refine-logs/history').rglob('startup--scope--question.json'))
