import copy
import json
import sys
from pathlib import Path
import pytest
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import writing_plan as wp

def plan():
    return yaml.safe_load((ROOT/'writing/writing-plan.composition.yaml').read_text())

def test_example_inheritance_and_render():
    p=plan();assert wp.validate_plan(p)==[]
    r=wp.resolve_plan(p);nodes={n['id']:n for n in r['nodes']}
    assert nodes['sec-results']['style']['strategy']=='observation_then_interpretation'
    assert nodes['sec-results']['style']['paragraph_rules']==p['defaults']['style']['paragraph_rules']
    assert 'composition' not in nodes['tab-main']
    assert 'tab:main' in wp.render_plan(r)
    assert wp.resolve_plan(p)==r

@pytest.mark.parametrize('field,value',[('node_id','missing-node'),('first_reference','tab-main'),('discuss_in',['missing-node']),('label','fig:wrong')])
def test_bad_links(field,value):
    p=plan();p['nodes'][1]['composition']['assets'][0][field]=value
    assert wp.validate_plan(p)

@pytest.mark.parametrize('field,value',[('span','three_columns'),('max_height_fraction',1.5),('placement_preference','guaranteed_page_2')])
def test_bad_layout_schema(field,value):
    p=plan();p['nodes'][1]['composition']['assets'][0][field]=value
    assert wp.validate_plan(p)[0]['code']=='schema_error'

def test_duplicate_asset_and_label():
    p=plan();p['nodes'][1]['composition']['assets']*=2
    assert any(e['code']=='duplicate_asset' for e in wp.validate_plan(p))

def test_packet_and_approval_invalidation(tmp_path):
    p=plan();p['nodes'][1]['approval']='before_write';p['nodes'][2]['approval']='auto';r=wp.resolve_plan(p)
    with pytest.raises(wp.PlanInvalid):wp.writer_packet(r,'sec-results')
    n=next(n for n in r['nodes'] if n['id']=='sec-results')
    p['approvals']={'sec-results':{'status':'approved','resolved_plan_hash':n['resolved_plan_hash'],'approved_by':'fixture','approved_at':'2026-09-23T00:00:00Z'}}
    r=wp.resolve_plan(p);packet=wp.writer_packet(r,'sec-results')
    assert packet['execution_status']=='prepared_not_written'
    assert packet['assets'][0]['asset_plan']['id']=='tab-main'
    # A child writer also respects the ancestor writing gate.
    assert wp.writer_packet(r,'tab-main')['node_id']=='tab-main'
    for field in ['style','layout']:
        changed=copy.deepcopy(p)
        if field=='style':changed['nodes'][1]['style']['strategy']='protocol_first'
        else:changed['nodes'][1]['composition']['assets'][0]['span']='one_column'
        stale=wp.resolve_plan(changed)
        with pytest.raises(wp.PlanInvalid):wp.writer_packet(stale,'tab-main')
    r['nodes'][1]['composition']['page_budget']=99
    with pytest.raises(wp.PlanInvalid):wp.writer_packet(r,'sec-results')

def source(root,ref=True,label=True):
    text='% auto-research:node sec-results start\nResults '+(r'\ref{tab:main}' if ref else '')+'\n% auto-research:node sec-results end\n'
    text+='% auto-research:node tab-main start\n'+r'\begin{table}\caption{Synthetic fixture}'+(r'\label{tab:main}' if label else '')+r'\end{table}'+'\n% auto-research:node tab-main end\n'
    (root/'main.tex').write_text(text)

@pytest.mark.parametrize('ref,label',[(True,True),(False,True),(True,False)])
def test_review_source_checks_and_visual_pending(tmp_path,ref,label):
    r=wp.resolve_plan(plan());source(tmp_path,ref,label)
    report=wp.review_plan(r,tmp_path);checks=next(n for n in report['nodes'] if n['node_id']=='sec-results')['checks']
    assert any(c['category']=='layout_review' and c['status']=='warning' for c in checks)
    assert any(c['category']=='asset_reference' for c in checks)==(not ref)
    assert any(c['category']=='asset_label' for c in checks)==(not label)

def test_comment_does_not_satisfy_reference(tmp_path):
    source(tmp_path,False,True)
    f=tmp_path/'main.tex';f.write_text(f.read_text().replace('Results ',r'% \ref{tab:main}'))
    report=wp.review_plan(wp.resolve_plan(plan()),tmp_path)
    assert any(c['category']=='asset_reference' for n in report['nodes'] for c in n['checks'])

def test_packet_cli(tmp_path):
    r=wp.resolve_plan(plan());f=tmp_path/'resolved.json';f.write_text(json.dumps(r));out=tmp_path/'packet.json'
    assert wp.main(['packet',str(f),'--node','sec-results','--output',str(out)])==0
    first=out.read_bytes();assert wp.main(['packet',str(f),'--node','sec-results','--output',str(out)])==0
    assert first==out.read_bytes()
    assert wp.main(['packet',str(f),'--node','missing','--output',str(out)])==1
    assert first==out.read_bytes()
