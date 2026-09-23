# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7", "jsonschema>=4.23,<5"]
# ///
"""Traceable benchmark Table Plan: audited runs -> cells -> native LaTeX.
No job launching or scientific significance inference. All paths are project-relative.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import math
import re
import statistics
from pathlib import Path
import yaml
import jsonschema
import table_ablation
from research_workflow import atomic, relative

RESOURCE=Path(__file__).resolve().parents[1]/'writing'
class Invalid(ValueError):pass

def digest_bytes(data):return hashlib.sha256(data).hexdigest()
def digest(value):return digest_bytes(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(path):return json.loads(Path(path).read_text())
def dump(path,value):atomic(Path(path),json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def path(root,name):
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise Invalid('Path outside project: '+str(name))
    return p

def load_plan(file):
    return validate_plan(yaml.safe_load(Path(file).read_text()))

def validate_plan(p):
    errors=sorted(jsonschema.Draft202012Validator(read(RESOURCE/'table-plan.schema.json')).iter_errors(p),key=lambda e:str(e.path))
    if errors:raise Invalid('; '.join(e.message for e in errors))
    for group in ['rows','datasets','metrics']:
        ids=[v['id'] for v in p[group]]
        if len(ids)!=len(set(ids)):raise Invalid('Duplicate '+group+' IDs')
    if len({d['source'] for d in p['datasets']})!=len(p['datasets']):raise Invalid('Duplicate dataset source')
    if any(not finite(m['scale']) for m in p['metrics']):raise Invalid('Non-finite metric scale')
    selections=[digest({k:r[k] for k in ['experiment_id','parameters']}) for r in p['rows']]
    if len(selections)!=len(set(selections)):raise Invalid('Duplicate row selection')
    table_ablation.validate(p)
    return p

def finite(v):return type(v) in (float,int) and math.isfinite(v)

def source_values(file):
    if file.suffix=='.csv':
        rows=list(csv.DictReader(io.StringIO(file.read_text())))
        if len(rows)!=1:raise Invalid('Raw CSV must have exactly one result row')
        return {k:float(v) for k,v in rows[0].items()}
    v=read(file);return v.get('metrics',v)

def resolve(plan,root):
    validate_plan(plan)
    stats_path=path(root,plan['statistics']);raw=stats_path.read_bytes();report=json.loads(raw)
    if report.get('version')!=1 or not isinstance(report.get('runs'),list):raise Invalid('Unknown statistics format')
    runs=report['runs'];ids=[r['run_id'] for r in runs]
    if len(ids)!=len(set(ids)):raise Invalid('Duplicate run IDs')
    result={'version':1,'plan':plan,'plan_hash':digest(plan),'statistics_sha256':digest_bytes(raw),'experiment_plan_hash':report.get('plan_hash'),'cells':[],'issues':[]}
    seed_values={}
    for row in plan['rows']:
        for dataset in plan['datasets']:
            selected=[r for r in runs if r.get('experiment_id')==row['experiment_id'] and r.get('parameters')==row['parameters'] and r.get('dataset')==dataset['source'] and r.get('protocol')==plan['protocol'] and r.get('comparison_group')==plan['comparison_group'] and r.get('source_kind')==plan['source_kind']]
            seeds=[r['seed'] for r in selected]
            if len(seeds)!=len(set(seeds)):raise Invalid('Ambiguous run selection: '+row['id']+'/'+dataset['id'])
            for metric in plan['metrics']:
                cid=':'.join([plan['id'],row['id'],dataset['id'],metric['id']]);issues=[];values=[];provenance=[]
                seed_values[cid]={}
                definitions=[s for s in report.get('summary',[]) if s.get('experiment_id')==row['experiment_id'] and s.get('parameters')==row['parameters'] and s.get('dataset')==dataset['source'] and s.get('protocol')==plan['protocol'] and s.get('comparison_group')==plan['comparison_group'] and s.get('source_kind')==plan['source_kind'] and s.get('metric')==metric['source']]
                if len(definitions)!=1 or definitions[0].get('direction')!=metric['direction']:
                    issues.append('Missing/ambiguous metric definition or direction mismatch')
                expected=plan['seeds'];chosen=sorted(selected,key=lambda r:r['seed'])
                if set(seeds)!=set(expected):issues.append('Expected seed set is incomplete or contains unexpected seeds')
                for run in chosen:
                    proof={k:run.get(k) for k in ['run_id','seed','attempt','config_hash','status','audit','evidence_status','result_path','result_sha256']};provenance.append(proof)
                    if run.get('status')!='completed':issues.append('Run is '+str(run.get('status')));continue
                    if run.get('audit')!='PASS' or run.get('evidence_status')!='eligible':issues.append('Run is not audited eligible evidence')
                    file=path(root,run.get('result_path',''))
                    if not file.is_file():issues.append('Missing raw result');continue
                    if digest_bytes(file.read_bytes())!=run.get('result_sha256'):issues.append('Raw result hash mismatch');continue
                    values_raw=source_values(file);v=values_raw.get(metric['source'])
                    if not finite(v) or v!=run.get('metrics',{}).get(metric['source']):issues.append('Raw and reported metric differ or are non-finite');continue
                    scaled=v*metric['scale']
                    if not finite(scaled):issues.append('Scaled metric is non-finite');continue
                    values.append(scaled)
                    seed_values[cid][run['seed']]=scaled
                valid=not issues and len(values)==len(expected)
                cell={'id':cid,'row_id':row['id'],'dataset_id':dataset['id'],'metric_id':metric['id'],'status':'eligible' if valid else 'blocked','n':len(values),'mean':statistics.mean(values) if valid else None,'std':statistics.stdev(values) if valid and len(values)>1 else None,'sources':provenance,'issues':sorted(set(issues))}
                result['cells'].append(cell)
                result['issues'] += [{'cell':cid,'reason':x} for x in cell['issues']]
    # Rank displayed values, preserving rounded ties and metric direction. Blocked cells never ranked.
    for d in plan['datasets']:
        for m in plan['metrics']:
            cells=[c for c in result['cells'] if c['dataset_id']==d['id'] and c['metric_id']==m['id'] and c['status']=='eligible']
            vals=sorted({round(c['mean'],m['precision']) for c in cells},reverse=m['direction']=='maximize')
            for c in cells:c['display_rank']=vals.index(round(c['mean'],m['precision']))+1
    table_ablation.derive(plan,result,seed_values)
    result['status']='blocked' if result['issues'] else 'ready'
    return result

def tex(s):
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(s))

def cell_text(c,m,disp):
    if c['status']!='eligible':return r'\textemdash{}'
    value=f"{c['mean']:.{m['precision']}f}"
    if disp=='mean_sd' and c['std'] is not None:value+=r' $\pm$ '+f"{c['std']:.{m['precision']}f}"
    return value

def render(resolved):
    p=resolved['plan'];metrics={m['id']:m for m in p['metrics']};cells={c['id']:c for c in resolved['cells']}
    vals=[r'\providecommand{\ResearchValue}[1]{\ifcsname rv@#1\endcsname\csname rv@#1\endcsname\else\PackageError{table-plan}{Unknown cell #1}{Regenerate table values}\fi}']
    for c in resolved['cells']:vals.append(r'\expandafter\def\csname rv@'+c['id']+r'\endcsname{'+cell_text(c,metrics[c['metric_id']],p['display'])+'}')
    env='table*' if p['layout']=='double_column' else 'table';columns=len(p['datasets'])*len(p['metrics'])
    lines=[r'% Requires booktabs; input the sibling values file before this table.',r'\begin{'+env+'}[t]',r'\centering',r'\caption{'+tex(p['caption'])+'}',r'\label{tab:'+p['id']+'}',r'\begingroup\small\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{@{}l'+'r'*columns+'@{}}',r'\toprule',r'Method & '+' & '.join(r'\multicolumn{'+str(len(p['metrics']))+'}{c}{'+tex(d['label'])+'}' for d in p['datasets'])+r' \\']
    lines.append(' '.join(r'\cmidrule(lr){'+str(2+i*len(p['metrics']))+'-'+str(1+(i+1)*len(p['metrics']))+'}' for i in range(len(p['datasets']))))
    lines.append(' & '+' & '.join(tex(m['label'])+(' $\\uparrow$' if m['direction']=='maximize' else ' $\\downarrow$') for d in p['datasets'] for m in p['metrics'])+r' \\\midrule')
    for row in p['rows']:
        entries=[]
        for d in p['datasets']:
            for m in p['metrics']:
                c=cells[':'.join([p['id'],row['id'],d['id'],m['id']])];v=r'\ResearchValue{'+c['id']+'}'
                if p['highlight']=='best' and c.get('display_rank')==1:v=r'\textbf{'+v+'}'
                entries.append(v)
        lines.append(tex(row['label'])+' & '+' & '.join(entries)+r' \\')
    note='Values trace to audited runs. Dash means blocked or missing evidence, not zero. '
    note+=('Mean and sample SD across '+str(len(p['seeds']))+' seeds. ' if p['display']=='mean_sd' and len(p['seeds'])>1 else 'Mean across '+str(len(p['seeds']))+' seed(s); no uncertainty displayed. ')
    if p['highlight']=='best':note+='Bold marks best displayed mean (ties included), not significance.'
    lines +=[r'\bottomrule\end{tabular}\par\smallskip',r'\parbox{\linewidth}{\footnotesize '+tex(note)+'}',r'\endgroup',r'\end{'+env+'}']
    extra,defs=table_ablation.render_extra(p,resolved,tex,cell_text) if 'ablation' in p else ('','')
    return '\n'.join(lines)+'\n'+extra,'\n'.join(vals)+'\n'+defs

def verify(resolved,root,output_dir=None,manuscript=None):
    errors=[]
    current=resolve(resolved['plan'],root)
    if current!=resolved:errors.append('Resolved inputs or provenance changed; resolve and render again')
    if current['status']!='ready':errors.append('Table contains blocked evidence')
    if output_dir:
        expected=render(resolved)
        for suffix,body in zip(['.tex','-values.tex'],expected):
            f=Path(output_dir)/(resolved['plan']['id']+suffix)
            if not f.is_file() or f.read_text()!=body:errors.append('Missing or changed rendered file: '+f.name)
    used=[]
    if manuscript:
        content=Path(manuscript).read_text()
        # Ignore normal LaTeX comments; escaped percent is retained.
        content=re.sub(r'(?<!\\)%[^\n]*','',content)
        used=re.findall(r'\\ResearchValue\{([^{}]+)\}',content)
        known={c['id']:c for c in resolved['cells']+resolved.get('derived_cells',[])}
        for cid in used:
            if cid not in known or known[cid]['status']!='eligible':errors.append('Unknown or blocked manuscript cell: '+cid)
        if not used:errors.append('No traceable ResearchValue references in manuscript')
    return {'status':'fail' if errors else 'pass','errors':errors,'value_references':used,'scope':'Checks explicit ResearchValue references and generated files only; freehand numbers, semantic claims and TeX include trees require separate review.'}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate');v.add_argument('plan',type=Path)
    r=sub.add_parser('resolve');r.add_argument('plan',type=Path);r.add_argument('--content-root',type=Path,required=True);r.add_argument('--output',type=Path,required=True)
    r=sub.add_parser('render');r.add_argument('resolved',type=Path);r.add_argument('--content-root',type=Path,required=True);r.add_argument('--output-dir',type=Path,required=True)
    r=sub.add_parser('review');r.add_argument('resolved',type=Path);r.add_argument('--content-root',type=Path,required=True);r.add_argument('--output-dir',type=Path,required=True);r.add_argument('--manuscript',type=Path);r.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(argv)
    try:
        if a.command=='validate':load_plan(a.plan);result={'status':'pass'}
        elif a.command=='resolve':result=resolve(load_plan(a.plan),a.content_root.resolve());dump(a.output,result)
        elif a.command=='render':
            resolved=read(a.resolved);checked=verify(resolved,a.content_root.resolve())
            if checked['status']!='pass':raise Invalid('; '.join(checked['errors']))
            a.output_dir.mkdir(parents=True,exist_ok=True)
            for suffix,body in zip(['.tex','-values.tex'],render(resolved)):atomic(a.output_dir/(resolved['plan']['id']+suffix),body)
            result={'status':'pass','table_id':resolved['plan']['id']}
        else:
            result=verify(read(a.resolved),a.content_root.resolve(),a.output_dir,a.manuscript);dump(a.output,result)
        print(json.dumps(result,ensure_ascii=False,indent=2));return int(result.get('status') in ['blocked','fail'])
    except (ValueError,KeyError,TypeError,yaml.YAMLError) as exc:print(json.dumps({'status':'fail','error':str(exc)}));return 1
    except OSError as exc:print(json.dumps({'status':'tool_error','error':str(exc)}));return 2

if __name__=='__main__':raise SystemExit(main())
