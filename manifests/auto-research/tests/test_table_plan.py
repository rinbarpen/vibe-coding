import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import pytest
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import table_plan as tp
import experiment_stats as es

@pytest.fixture
def example(tmp_path):
    plan=tp.load_plan(ROOT/'writing/table-plan.example.yaml');plan['caption']='SYNTHETIC FIXTURE: benchmark integration test'
    runs=[];records=[]
    for row in plan['rows']:
        for ds in plan['datasets']:
            rid=row['id']+'-'+ds['id'];metrics={'accuracy':.85 if row['id']=='candidate' else .8,'error':.15 if row['id']=='candidate' else .2}
            f=tmp_path/(rid+'.json');f.write_text(json.dumps({'metrics':metrics}));(tmp_path/(rid+'.log')).write_text('fixture run')
            runs.append({'run_id':rid,'config_hash':'fixture-hash','experiment_id':row['experiment_id'],'parameters':{},'dataset':ds['source'],'protocol':plan['protocol'],'comparison_group':plan['comparison_group'],'source_kind':plan['source_kind'],'seed':42,'command':['fixture'],'baseline':None})
            records.append({'run_id':rid,'attempt':1,'config_hash':'fixture-hash','status':'completed','audit':'PASS','exit_code':0,'result_path':f.name,'command':['fixture'],'code_revision':'fixture','environment':'fixture','started_at':'2026-09-22T00:00:00','ended_at':'2026-09-22T00:00:01','stdout_path':rid+'.log','stderr_path':rid+'.log'})
    report=es.aggregate({'runs':runs,'metrics':{'accuracy':{'direction':'maximize','unit':'fraction'},'error':{'direction':'minimize','unit':'fraction'}},'plan_hash':'fixture-plan'},records,tmp_path)
    p=tmp_path/plan['statistics'];p.parent.mkdir();p.write_text(json.dumps(report));return plan,report,tmp_path

def test_real_aggregator_to_cells(example):
    p,s,root=example;r=tp.resolve(p,root);assert r['status']=='ready';assert len(r['cells'])==8
    assert all(c['std'] is None and c['n']==1 and c['sources'] for c in r['cells'])
    assert next(c for c in r['cells'] if c['row_id']=='candidate' and c['metric_id']=='error-rate')['display_rank']==1
    assert tp.render(r)==tp.render(tp.resolve(p,root))

@pytest.mark.parametrize('field,value',[('audit','FAIL'),('audit','WARN'),('evidence_status','provisional'),('status','failed')])
def test_bad_evidence_blocks(example,field,value):
    p,s,root=example;s['runs'][0][field]=value;(root/p['statistics']).write_text(json.dumps(s));r=tp.resolve(p,root);assert r['status']=='blocked'
    assert any(c['mean'] is None for c in r['cells'])

def test_raw_hash_mismatch_and_seed_missing(example):
    p,s,root=example;(root/s['runs'][0]['result_path']).write_text('{}');assert tp.resolve(p,root)['status']=='blocked'
    p['seeds']=[42,43];assert all(c['status']=='blocked' for c in tp.resolve(p,root)['cells'])

def test_no_ambiguous_config_or_run(example):
    p,s,root=example;s['runs'].append(copy.deepcopy(s['runs'][0]));(root/p['statistics']).write_text(json.dumps(s))
    with pytest.raises(tp.Invalid):tp.resolve(p,root)

def test_escape_paths_schema(example):
    p,_,root=example;p['statistics']='../outside'
    with pytest.raises(tp.Invalid):tp.resolve(p,root)
    p['version']=2;f=root/'plan.yaml';f.write_text(yaml.safe_dump(p))
    with pytest.raises(tp.Invalid):tp.load_plan(f)
    assert tp.tex('a_b%')==r'a\_b\%'

def test_render_and_manuscript_staleness(example):
    p,_,root=example;r=tp.resolve(p,root);out=root/'tables';out.mkdir()
    for suffix,body in zip(['.tex','-values.tex'],tp.render(r)):(out/(p['id']+suffix)).write_text(body)
    manuscript=root/'main.tex';manuscript.write_text(r'Accuracy: \ResearchValue{table-main:candidate:dataset-a:accuracy}.')
    assert tp.verify(r,root,out,manuscript)['status']=='pass'
    manuscript.write_text(r'\ResearchValue{unknown}');assert tp.verify(r,root,out,manuscript)['status']=='fail'
    manuscript.write_text('85 percent');assert tp.verify(r,root,out,manuscript)['status']=='fail'
    (out/(p['id']+'.tex')).write_text('tampered');assert tp.verify(r,root,out)['status']=='fail'


def test_multiseed_std_and_rounded_ties(example):
    p,s,root=example;p['seeds']=[42,43]
    for r in list(s['runs']):
        clone=copy.deepcopy(r);clone['run_id']+='-43';clone['seed']=43;s['runs'].append(clone)
    (root/p['statistics']).write_text(json.dumps(s));r=tp.resolve(p,root);assert r['status']=='ready';assert all(c['std']==0 for c in r['cells']);assert r'\pm' in tp.render(r)[1]


def test_native_latex_compiles(example):
    if not shutil.which('pdflatex'):pytest.skip('pdflatex not installed')
    p,_,root=example;r=tp.resolve(p,root);body,values=tp.render(r);(root/'table.tex').write_text(body);(root/'values.tex').write_text(values)
    (root/'main.tex').write_text(r'\documentclass{article}\usepackage{booktabs}\begin{document}\input{values}\input{table}\ResearchValue{table-main:candidate:dataset-a:accuracy}\end{document}')
    result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=root,capture_output=True,text=True)
    assert result.returncode==0,result.stdout[-2000:]


def test_metric_direction_and_raw_numbers_checked(example):
    p,s,root=example;p['metrics'][0]['direction']='minimize';assert tp.resolve(p,root)['status']=='blocked'
    p['metrics'][0]['direction']='maximize';s['runs'][0]['metrics']['accuracy']=.99;(root/p['statistics']).write_text(json.dumps(s));assert tp.resolve(p,root)['status']=='blocked'


def test_writing_node_table_link_and_latex_anchor(example):
    import writing_plan as wp
    p,_,root=example;r=tp.resolve(p,root);(root/'plan.yaml').write_text(yaml.safe_dump(p));tp.dump(root/'resolved.json',r);out=root/'tables';out.mkdir()
    for suffix,body in zip(['.tex','-values.tex'],tp.render(r)):(out/(p['id']+suffix)).write_text(body)
    node={'id':'sec-results','presentation':{'tables':[{'table_plan':'plan.yaml','resolved':'resolved.json','output_dir':'tables'}]}}
    text,found=wp.extract_node_text('% auto-research:node sec-results start\n\\begin{table}test\\end{table}\n% auto-research:node sec-results end',node)
    assert found
    result=wp.review_node(node,text,found,{'sec-results':node});wp.review_table_specs(result,node,root);assert result['status']=='pass'
    (out/(p['id']+'.tex')).write_text('altered');wp.review_table_specs(result,node,root);assert result['status']=='fail'
