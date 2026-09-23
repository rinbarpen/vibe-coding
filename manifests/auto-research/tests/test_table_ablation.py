"""Synthetic fixtures only: exercise actual aggregation and native LaTeX."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import table_plan as tp
import experiment_stats as es
KINDS=['removal','additive','choices','interaction']

def fixture(root,kind,seeds=(42,43)):
    p=tp.load_plan(ROOT/f'writing/table-plan.ablation-{kind}.yaml');p['seeds']=list(seeds)
    p['caption']='SYNTHETIC TEST ONLY: '+kind;p['datasets']=p['datasets'][:1]
    runs=[];records=[]
    for i,row in enumerate(p['rows']):
        for seed in seeds:
            rid=f'fixture-{i}-{seed}';v=(1,2,4,8)[i]+(seed-42)*2
            file=root/(rid+'.json');file.write_text(json.dumps({'accuracy':v,'error':-v}))
            (root/(rid+'.log')).write_text('Synthetic fixture; no training performed')
            runs.append(dict(run_id=rid,config_hash='fixture',experiment_id=row['experiment_id'],parameters=row['parameters'],dataset=p['datasets'][0]['source'],protocol=p['protocol'],comparison_group=p['comparison_group'],source_kind=p['source_kind'],seed=seed,command=['fixture'],baseline=None))
            records.append(dict(run_id=rid,attempt=1,config_hash='fixture',status='completed',audit='PASS',exit_code=0,result_path=file.name,command=['fixture'],code_revision='fixture',environment='fixture',started_at='2026-09-23T00:00:00',ended_at='2026-09-23T00:00:01',stdout_path=rid+'.log',stderr_path=rid+'.log'))
    for m in p['metrics']:m['scale']=1
    report=es.aggregate({'runs':runs,'metrics':{'accuracy':{'direction':'maximize','unit':'score'},'error':{'direction':'minimize','unit':'score'}},'plan_hash':'fixture'},records,root)
    f=root/p['statistics'];f.parent.mkdir(exist_ok=True);f.write_text(json.dumps(report));return p,report

@pytest.mark.parametrize('kind',KINDS)
def test_paired_contrasts_compile_and_reference(tmp_path,kind):
    p,_=fixture(tmp_path,kind);r=tp.resolve(p,tmp_path)
    assert r['status']=='ready';assert all(c['std']>0 for c in r['cells'])
    expected={'removal':[1,3],'additive':[1,2],'choices':[1,3],'interaction':[3]}[kind]
    for c in r['derived_cells']:
        index=[x for x in r['derived_cells'] if x['metric_id']==c['metric_id']].index(c)
        assert c['mean']==expected[index]*(1 if c['metric_id']=='accuracy' else -1)
        assert c['std']==0 and c['n']==2 and len(c['paired_runs'])==2
        assert c['terms'] and all(x['run_ids'] for x in c['paired_runs'])
    body,values=tp.render(r);assert (body,values)==tp.render(tp.resolve(p,tmp_path))
    (tmp_path/'table.tex').write_text(body);(tmp_path/'values.tex').write_text(values)
    manuscript=tmp_path/'main.tex';manuscript.write_text(r'\documentclass{article}\usepackage{booktabs}\begin{document}\input{values}\input{table}\ResearchValue{'+r['derived_cells'][0]['id']+r'}\end{document}')
    assert tp.verify(r,tmp_path,manuscript=manuscript)['status']=='pass'
    if shutil.which('pdflatex'):
        proc=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=tmp_path,capture_output=True,text=True)
        assert proc.returncode==0,proc.stdout[-2000:]
        assert 'Overfull' not in proc.stdout
    manuscript.write_text(r'\ResearchValue{table:derived:unknown}')
    assert tp.verify(r,tmp_path,manuscript=manuscript)['status']=='fail'

@pytest.mark.parametrize('kind',KINDS)
def test_single_seed_and_ineligible_dependency(tmp_path,kind):
    p,report=fixture(tmp_path,kind,(42,));r=tp.resolve(p,tmp_path)
    assert all(c['std'] is None for c in r['derived_cells'])
    report['runs'][0]['audit']='FAIL';(tmp_path/p['statistics']).write_text(json.dumps(report))
    r=tp.resolve(p,tmp_path);assert r['status']=='blocked'
    assert any(c['status']=='blocked' and c['mean'] is None for c in r['derived_cells'])

@pytest.mark.parametrize('kind',KINDS)
def test_control_drift_rejected(tmp_path,kind):
    p,_=fixture(tmp_path,kind);p['rows'][1]['parameters']['width']=64
    with pytest.raises(ValueError,match='Non-factor'):tp.validate_plan(p)

@pytest.mark.parametrize('kind',KINDS)
def test_incomplete_design_rejected(tmp_path,kind):
    p,_=fixture(tmp_path,kind)
    if kind=='choices':p['ablation']['reference_row']='missing'
    else:p['rows'].pop()
    with pytest.raises(ValueError):tp.validate_plan(p)

def test_stale_raw_missing_seed_and_invalid_order(tmp_path):
    p,report=fixture(tmp_path,'additive');r=tp.resolve(p,tmp_path)
    (tmp_path/report['runs'][0]['result_path']).write_text('{}')
    assert tp.verify(r,tmp_path)['status']=='fail'
    assert any(c['status']=='blocked' for c in tp.resolve(p,tmp_path)['derived_cells'])
    p['seeds'].append(44);assert all(c['status']=='blocked' for c in tp.resolve(p,tmp_path)['derived_cells'])
    p['rows'].reverse()
    with pytest.raises(ValueError):tp.validate_plan(p)

def test_factor_schema(tmp_path):
    p,_=fixture(tmp_path,'interaction');p['ablation']['reference_row']='config-0'
    with pytest.raises(ValueError):tp.validate_plan(p)
    del p['ablation']['reference_row'];p['ablation']['factors'][1]['parameter']='a'
    with pytest.raises(ValueError):tp.validate_plan(p)
