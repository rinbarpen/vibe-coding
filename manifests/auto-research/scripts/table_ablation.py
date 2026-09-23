"""Ablation designs and paired contrasts. No scientific causal claims are inferred."""
import statistics
import json

class Invalid(ValueError):pass


def validate(plan):
    a=plan.get('ablation')
    if not a:return
    rows={r['id']:r for r in plan['rows']};factors=a['factors'];keys=[f['parameter'] for f in factors]
    if len(keys)!=len(set(keys)) or len({f['id'] for f in factors})!=len(factors):raise Invalid('Duplicate ablation factors')
    if any(k not in r['parameters'] for r in rows.values() for k in keys):raise Invalid('Missing factor parameter')
    # Control parameters are explicit, top-level fields. No free-form nested lookup.
    control=[{k:v for k,v in r['parameters'].items() if k not in keys} for r in rows.values()]
    if any(c!=control[0] for c in control):raise Invalid('Non-factor parameters differ between ablation rows')
    if len({r['experiment_id'] for r in rows.values()})!=1:raise Invalid('Ablation rows must share experiment_id; vary declared factors only')
    kind=a['kind']
    if kind in ['removal','additive','interaction']:
        if any(type(r['parameters'][k]) is not bool for r in rows.values() for k in keys):raise Invalid('Component factors must be booleans')
    configs=[tuple(json.dumps(r['parameters'][k],sort_keys=True) for k in keys) for r in rows.values()]
    if len(configs)!=len(set(configs)):raise Invalid('Repeated ablation configuration')
    if kind=='removal':
        ref=a.get('reference_row')
        if ref not in rows:raise Invalid('Unknown removal reference')
        if not all(rows[ref]['parameters'][k] for k in keys):raise Invalid('Removal reference must enable all factors')
        if len(rows)!=len(keys)+1:raise Invalid('Removal requires full model and one removal per factor')
        for rid,r in rows.items():
            if rid!=ref and sum(not r['parameters'][k] for k in keys)!=1:raise Invalid('Each removal changes exactly one factor')
    elif kind=='additive':
        ordered=plan['rows']
        if len(rows)!=len(keys)+1 or any(ordered[0]['parameters'][k] for k in keys):raise Invalid('Additive requires all-off base followed by every factor')
        for prev,cur in zip(ordered,ordered[1:]):
            changes=[k for k in keys if prev['parameters'][k]!=cur['parameters'][k]]
            if len(changes)!=1 or not cur['parameters'][changes[0]]:raise Invalid('Additive steps must enable exactly one component')
    elif kind=='choices':
        if len(keys)!=1:raise Invalid('Each choices plan varies one declared factor; use separate plans for separate blocks')
        if a.get('reference_row') not in rows:raise Invalid('Unknown design-choice reference')
        if len(rows)<2:raise Invalid('Choices requires at least two settings')
        if any(isinstance(r['parameters'][keys[0]],(dict,list)) for r in rows.values()):raise Invalid('Design choices must be scalar')
    elif kind=='interaction':
        if len(keys)!=2 or len(rows)!=4:raise Invalid('Interaction requires complete 2 x 2 factorial design')
        if set(tuple(r['parameters'][k] for k in keys) for r in rows.values())!={(False,False),(False,True),(True,False),(True,True)}:raise Invalid('Missing factorial combination')


def contrasts(plan):
    a=plan['ablation'];kind=a['kind'];rows=plan['rows']
    if kind in ['removal','choices']:
        ref=a['reference_row'];return [{'id':'delta-'+r['id'],'label':r['label']+' minus reference','terms':[(r['id'],1),(ref,-1)]} for r in rows if r['id']!=ref]
    if kind=='additive':return [{'id':'step-'+cur['id'],'label':cur['label']+' minus '+prev['label'],'terms':[(cur['id'],1),(prev['id'],-1)]} for prev,cur in zip(rows,rows[1:])]
    keys=[f['parameter'] for f in a['factors']];lookup={tuple(r['parameters'][k] for k in keys):r['id'] for r in rows}
    return [{'id':'interaction','label':'A x B: (11 - 10) - (01 - 00)','terms':[(lookup[(True,True)],1),(lookup[(True,False)],-1),(lookup[(False,True)],-1),(lookup[(False,False)],1)]}]


def derive(plan,result,seed_values):
    if 'ablation' not in plan:return
    cells={c['id']:c for c in result['cells']};derived=[]
    for contrast in contrasts(plan):
        for ds in plan['datasets']:
            for m in plan['metrics']:
                terms=[{'cell_id':':'.join([plan['id'],rid,ds['id'],m['id']]),'weight':weight} for rid,weight in contrast['terms']]
                deps=[cells[t['cell_id']] for t in terms];good=all(c['status']=='eligible' for c in deps)
                values=[];pairs=[]
                if good:
                    for seed in sorted(plan['seeds']):
                        values.append(sum(t['weight']*seed_values[t['cell_id']][seed] for t in terms))
                        pairs.append({'seed':seed,'run_ids':[next(s['run_id'] for s in c['sources'] if s['seed']==seed) for c in deps]})
                    # Avoid non-finite arithmetic even when inputs themselves are finite.
                    import math
                    good=all(math.isfinite(v) for v in values)
                cell={'id':':'.join([plan['id'],'derived',contrast['id'],ds['id'],m['id']]),'row_id':contrast['id'],'label':contrast['label'],'dataset_id':ds['id'],'metric_id':m['id'],'status':'eligible' if good else 'blocked','n':len(values) if good else 0,'mean':statistics.mean(values) if good else None,'std':statistics.stdev(values) if good and len(values)>1 else None,'terms':terms,'paired_runs':pairs,'issues':[] if good else ['Blocked input evidence or non-finite paired contrast'],'definition':'Weighted within-seed contrast; not a significance test'}
                derived.append(cell)
                if not good:result['issues'].append({'cell':cell['id'],'reason':cell['issues'][0]})
    result['derived_cells']=derived


def render_extra(plan,result,tex,cell_text):
    """Separate native factor and contrast tables, sharing the normal value-macro file."""
    a=plan['ablation'];factors=a['factors'];metric_map={m['id']:m for m in plan['metrics']};env='table*' if plan['layout']=='double_column' else 'table'
    def begin(suffix,caption):return [r'\begin{'+env+'}[t]',r'\centering\caption{'+tex(caption)+'}',r'\label{tab:'+plan['id']+'-'+suffix+'}',r'\begingroup\small\setlength{\tabcolsep}{3pt}']
    def end():return [r'\endgroup',r'\end{'+env+'}']
    lines=begin('factors','Ablation configuration: '+a['kind'])
    lines += [r'\begin{tabular}{@{}l'+'c'*len(factors)+'@{}}',r'\toprule','Configuration & '+' & '.join(tex(f['label']) for f in factors)+r' \\\midrule']
    for row in plan['rows']:
        vals=[row['parameters'][f['parameter']] for f in factors]
        lines.append(tex(row['label'])+' & '+' & '.join(tex('On' if v is True else 'Off' if v is False else v) for v in vals)+r' \\')
    lines += [r'\bottomrule\end{tabular}']+end()
    lines += begin('contrasts','Paired ablation contrasts (current minus previous)' if a['kind']=='additive' else 'Paired ablation contrasts (variant minus reference)')
    if a['kind']=='interaction':lines[-3]=r'\centering\caption{Paired interaction: (11 - 10) - (01 - 00)}'
    count=len(plan['datasets'])*len(plan['metrics']);lines +=[r'\begin{tabular}{@{}l'+'r'*count+'@{}}',r'\toprule','Contrast & '+' & '.join(tex(d['label']+' / '+m['label']) for d in plan['datasets'] for m in plan['metrics'])+r' \\\midrule']
    derived=result['derived_cells'];lookup={(c['row_id'],c['dataset_id'],c['metric_id']):c for c in derived}
    for contrast in contrasts(plan):
        vals=[r'\ResearchValue{'+lookup[(contrast['id'],d['id'],m['id'])]['id']+'}' for d in plan['datasets'] for m in plan['metrics']]
        lines.append(tex(contrast['label'])+' & '+' & '.join(vals)+r' \\')
    note='Raw signed differences in the displayed metric unit; percentage-valued metrics give percentage-point differences. '
    note+='For lower-is-better metrics, negative differences indicate reduction; interaction signs do not establish synergy. '
    if a['kind']=='additive':note+='Sequential gains depend on component order. '
    note+='SD, when shown, is computed from within-seed contrasts, not from marginal SDs. No significance claim.'
    lines +=[r'\bottomrule\end{tabular}\par\smallskip',r'\parbox{\linewidth}{\footnotesize '+tex(note)+'}']+end()
    defs=[]
    for c in derived:defs.append(r'\expandafter\def\csname rv@'+c['id']+r'\endcsname{'+cell_text(c,metric_map[c['metric_id']],plan['display'])+'}')
    return '\n'.join(lines)+'\n','\n'.join(defs)+'\n'
