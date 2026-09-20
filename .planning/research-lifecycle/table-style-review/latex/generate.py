from pathlib import Path
import json,re,subprocess,shutil
R=Path(__file__).parent;data=json.loads((R/'fixtures.json').read_text());T=data['tables']
def esc(s):
 return str(s).replace('–','--').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
def textcell(s,align='c'):return r'\multicolumn{1}{'+align+'}{'+esc(s)+'}'
preamble=r'''\usepackage{booktabs,siunitx,threeparttable,longtable,array,xcolor}
\sisetup{detect-weight=true,detect-family=true,retain-explicit-plus=true}
% In a venue manuscript, inherit its class font and caption settings.
\newcommand{\TabSetup}{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.12}}
'''
(R/'table-packages.tex').write_text(preamble)
for t in T:
 if t['id'].startswith('09-'):continue
 rows=t['rows'];n=len(t['headers']);numeric=[all(re.fullmatch(r'[+-]?\d+(\.\d+)?',row[j]) or row[j]=='NA' for row in rows) for j in range(n)]
 def col(j):
  if not numeric[j]:return 'l' if j==0 or (t['id']=='04-design-ablation' and j==1) else 'c'
  vals=[v for v in [row[j] for row in rows] if v!='NA'];sign='+' if any(v[0] in '+-' for v in vals) else '';digits=max(len(v.lstrip('+-').split('.')[0]) for v in vals);dec=max(len(v.split('.')[1]) if '.' in v else 0 for v in vals)
  return 'S[table-format='+sign+str(digits)+('.'+str(dec) if dec else '')+']'
 spec='@{}'+''.join(col(j) for j in range(n))+'@{}';lines=[r'\begin{tabular}{'+spec+'}',r'\toprule']
 if t['groups']:
  groupby={lo:(hi,label) for lo,hi,label in t['groups']};cells=[];j=0
  while j<n:
   if j in groupby:
    hi,label=groupby[j];cells.append(r'\multicolumn{'+str(hi-j)+'}{c}{'+esc(label)+'}');j=hi
   else:cells.append(textcell(''));j+=1
  lines+=[' & '.join(cells)+r' \\',' '.join(r'\cmidrule(lr){'+str(lo+1)+'-'+str(hi)+'}' for lo,hi,_ in t['groups'])]
 heads=[]
 for h in t['headers']:
  # Units and qualifiers on second line rather than shrinking the entire table.
  h=esc(h);h=h.replace(' (%)',r'\\(\%)').replace(' (pp)',r'\\(pp)').replace(' (ms)',r'\\(ms)').replace(' (GB)',r'\\(GB)').replace(' (M)',r'\\(M)').replace(', n',r'\\$n$')
  heads.append(r'\multicolumn{1}{c}{\shortstack{'+h+'}}')
 lines+=[' & '.join(heads)+r' \\',r'\midrule']
 for i,row in enumerate(rows):
  if i in t['blocks']:lines.append(r'\addlinespace')
  cells=[]
  for j,v in enumerate(row):
   if numeric[j]:cells.append(textcell('---') if v=='NA' else v)
   else:
    value=esc(v)
    if j==0 and i==t['reference']:value=r'\textbf{'+value+'}'
    cells.append(value)
  lines.append(' & '.join(cells)+r' \\')
 lines +=[r'\bottomrule',r'\end{tabular}']
 (R/'bodies'/f"{t['id']}.tex").write_text('\n'.join(lines))
 notes=[n.replace('NA = not applicable','--- = not applicable') for n in t['notes']]
 if t['reference'] is not None:notes.append('Bold row labels indicate the reference, not statistical significance.')
 if t['id']=='11-style-review':notes=['Same fixture data as component removal. LaTeX publication variant is monochrome; heat shading is omitted.']
 env='table' if t['id'] in ['05-interaction-ablation','10-style-reference'] else 'table*'
 out=[r'\begin{'+env+'}[t]',r'\centering',r'\begin{threeparttable}',r'\caption{'+esc(t['title'])+'. Synthetic layout fixture, not experimental evidence.}',r'\label{tab:'+t['id']+'}',r'\TabSetup',r'\input{bodies/'+t['id']+'.tex}',r'\begin{tablenotes}[flushleft]',r'\footnotesize']+[r'\item '+esc(note) for note in notes]+[r'\end{tablenotes}',r'\end{threeparttable}',r'\end{'+env+'}']
 (R/'tables'/f"{t['id']}.tex").write_text('\n'.join(out))
# Actual longtable with repeat headings and continuation footer, for a one-column supplement.
rows=sum([t['rows'] for t in T if t['id'].startswith('09-')],[])
lt=[r'\begingroup\TabSetup',r'\begin{longtable}{@{}l S[table-format=2] S[table-format=2.1] l S[table-format=3]@{}}',r'\caption{Complete fixture ledger. Invented values; no experiments executed.}\label{tab:ledger}\\',r'\toprule',r'Configuration & {Seed} & {Accuracy (\%)} & Status & {Test $n$} \\',r'\midrule',r'\endfirsthead',r'\multicolumn{5}{l}{\tablename\ \thetable\ (continued)}\\',r'\toprule',r'Configuration & {Seed} & {Accuracy (\%)} & Status & {Test $n$}\\',r'\midrule',r'\endhead',r'\midrule\multicolumn{5}{r}{Continued on next page}\\',r'\endfoot',r'\bottomrule',r'\multicolumn{5}{l}{\footnotesize --- = no reported value; status identifies the reason.}\\',r'\endlastfoot']
for row in rows:lt.append(' & '.join(textcell('---') if v=='NA' else esc(v) for v in row)+r' \\')
lt +=[r'\end{longtable}',r'\endgroup'];(R/'tables/09-appendix-longtable.tex').write_text('\n'.join(lt))
keys=[t['id'] for t in T if not t['id'].startswith('09-')]
base=r'\documentclass[10pt]{article}'+'\n'+r'\usepackage[a4paper,margin=18mm]{geometry}'+'\n'+r'\input{table-packages}'+'\n'
cat=base+r'\begin{document}'+'\n'+r'\section*{Research tables: native LaTeX catalog}'+'\n'+r'All values are synthetic fixtures. No significance claims. Each page retains editable LaTeX text and numbers.'+'\n'
for key in keys:cat+='\n'+r'\input{tables/'+key+'}\clearpage'
cat+='\n'+r'\input{tables/09-appendix-longtable}\end{document}';(R/'catalog.tex').write_text(cat)
two=base.replace('[10pt]','[10pt,twocolumn]')+r'\begin{document}'+'\n'+r'\section*{Two-column integration test}'+'\n'+r'Generic article harness, not an official venue template. Narrow tables use table; wide tables use table*. No forced scaling.'+'\n'
for key in keys:two+='\n'+r'\input{tables/'+key+'}\clearpage'
(R/'two-column.tex').write_text(two+r'\end{document}')
(R/'supplement.tex').write_text(base.replace('a4paper,margin=18mm','paperwidth=210mm,paperheight=160mm,margin=18mm')+r'\begin{document}\input{tables/09-appendix-longtable}\end{document}')
# Size audit independent of float placement.
audit=base+r'\newsavebox{\auditbox}\begin{document}'+'\n'
for key in keys:
 width='85mm' if key in ['05-interaction-ablation','10-style-reference'] else r'\textwidth'
 audit+=r'\sbox{\auditbox}{\TabSetup\input{bodies/'+key+r'.tex}}\typeout{TABLEWIDTH '+key+r' = \the\wd\auditbox}\ifdim\wd\auditbox>'+width+r'\errmessage{Table too wide: '+key+r'}\fi'+'\n'
audit+=r'Width checks passed.\end{document}';(R/'width-check.tex').write_text(audit)
records=[]
for name in ['catalog','two-column','supplement','width-check']:
 for run in range(2):
  cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build',name+'.tex'];p=subprocess.run(cmd,cwd=R,text=True,capture_output=True);records.append({'command':cmd,'pass':run+1,'exit_status':p.returncode,'stdout':p.stdout});(R/'verification.json').write_text(json.dumps(records,indent=2))
  if p.returncode:print(p.stdout[-2200:]);raise SystemExit(p.returncode)
 log=(R/'build'/f'{name}.log').read_text(errors='replace');print(name, 'overfull=',len(re.findall('Overfull',log)))
 shutil.copy2(R/'build'/f'{name}.pdf',R/f'{name}.pdf')
print('Compiled all 4 documents twice.')
