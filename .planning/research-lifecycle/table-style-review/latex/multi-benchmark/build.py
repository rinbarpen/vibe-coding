from pathlib import Path
import json,subprocess,re,zipfile
import numpy as np
R=Path(__file__).parent
rng=np.random.default_rng(101);methods=[f'Baseline {chr(65+i)}' for i in range(8)]+['Candidate'];datasets=['Dataset A','Dataset B','Dataset C','Dataset D'];metrics=['Accuracy','Macro-F1','ECE'];directions=[1,1,-1]
v=np.round(rng.uniform(65,90,(9,4,3)),1);v[:,:,2]=np.round(rng.uniform(2,10,(9,4)),1)
# Intentional ties exercise rank styling; rankings are per dataset/metric.
v[0,0,0]=v[1,0,0]=95.;v[2,0,0]=93.
(R/'data.json').write_text(json.dumps({'synthetic':True,'n_seeds':1,'methods':methods,'datasets':datasets,'metrics':metrics,'directions':directions,'values':v.tolist()},indent=2))
packages=r'''\usepackage{booktabs,siunitx,threeparttable,longtable,array}
\sisetup{detect-weight=true,detect-family=true}
\newcommand{\best}[1]{\textbf{#1}}
\newcommand{\second}[1]{\underline{#1}}
'''
(R/'packages.tex').write_text(packages)
notes=r'''\begin{tablenotes}[flushleft]\footnotesize
\item All numbers are invented layout fixtures, not benchmark results. One run per configuration; no cross-seed uncertainty is reported. Metric units are percent.
\item Bold indicates the best displayed value; underline indicates the second distinct value within each dataset/metric. Ties share rank. Neither denotes statistical significance. Accuracy and Macro-F1: higher is better; ECE: lower is better.
\item ECE denotes expected calibration error. Real results must specify the binning protocol and common evaluation settings. Method names are placeholders, not literature baselines.
\end{tablenotes}'''
marked=[]
def value(i,d,m):
 x=v[i,d,m];vals=sorted(set(v[:,d,m]),reverse=directions[m]>0);s=f'{x:.1f}'
 if x==vals[0]:marked.append((i,d,m,'best'));return r'\multicolumn{1}{r}{\best{'+s+'}}'
 if x==vals[1]:marked.append((i,d,m,'second'));return r'\multicolumn{1}{r}{\second{'+s+'}}'
 return s
# Broad double-column table: dataset groups, three repeated metric headers.
lines=[r'\begin{tabular}{@{}l*{12}{S[table-format=2.1]}@{}}',r'\toprule','Method & '+' & '.join(r'\multicolumn{3}{c}{'+d+'}' for d in datasets)+r' \\', ' '.join(r'\cmidrule(lr){'+str(2+3*d)+'-'+str(4+3*d)+'}' for d in range(4)),' & ' + ' & '.join([r'{Acc. $\uparrow$}',r'{F1 $\uparrow$}',r'{ECE $\downarrow$}']*4)+r' \\',r'\midrule']
for i,name in enumerate(methods):
 if i==8:lines.append(r'\addlinespace')
 lines.append(name+' & '+' & '.join(value(i,d,m) for d in range(4) for m in range(3))+r' \\')
lines +=[r'\bottomrule',r'\end{tabular}'];(R/'wide-body.tex').write_text('\n'.join(lines))
caption='Multi-dataset, multi-method comparison. Synthetic fixture values (percent).'
wide=r'\begin{table*}[t]\centering\begin{threeparttable}\caption{'+caption+r'}\label{tab:multi-benchmark}\small\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.12}\input{wide-body}'+notes+r'\end{threeparttable}\end{table*}'
(R/'wide.tex').write_text(wide)
for m,name in enumerate(metrics):
 key='metric-'+str(m+1);ls=[r'\begin{tabular}{@{}l*{4}{S[table-format=2.1]}@{}}',r'\toprule','Method & '+' & '.join('{'+d+'}' for d in datasets)+r' \\',r'\midrule']
 for i,method in enumerate(methods):ls.append(method+' & '+' & '.join(value(i,d,m) for d in range(4))+r' \\')
 ls +=[r'\bottomrule',r'\end{tabular}'];(R/(key+'-body.tex')).write_text('\n'.join(ls))
 (R/(key+'.tex')).write_text(r'\begin{table}[t]\centering\begin{threeparttable}\caption{'+name+' across four datasets. Synthetic fixture.'+r'}\label{tab:'+key+r'}\small\setlength{\tabcolsep}{3pt}\input{'+key+'-body}'+notes+r'\end{threeparttable}\end{table}')
# Dataset-block longtable: all 108 values, with actual continuation headers.
lt=[r'\begingroup\small\begin{longtable}{@{}ll*{3}{S[table-format=2.1]}@{}}',r'\caption{Dataset-block comparison. All values are invented fixtures.}\label{tab:multi-long}\\',r'\toprule',r'Dataset & Method & {Accuracy $\uparrow$} & {Macro-F1 $\uparrow$} & {ECE $\downarrow$}\\',r'\midrule\endfirsthead',r'\multicolumn{5}{l}{Table \thetable\ (continued)}\\\toprule',r'Dataset & Method & {Accuracy $\uparrow$} & {Macro-F1 $\uparrow$} & {ECE $\downarrow$}\\',r'\midrule\endhead',r'\midrule\multicolumn{5}{r}{Continued on next page}\\\endfoot',r'\bottomrule\endlastfoot']
for d,name in enumerate(datasets):
 if d:lt.append(r'\addlinespace')
 for i,method in enumerate(methods):lt.append(name+' & '+method+' & '+' & '.join(value(i,d,m) for m in range(3))+r' \\')
lt +=[r'\end{longtable}',r'\noindent\footnotesize Bold = best; underline = second distinct value. Ties share rank. Not significance.',r'\endgroup'];(R/'dataset-blocks.tex').write_text('\n'.join(lt))
records=[]
def compile(name,doc):
 (R/(name+'.tex')).write_text(doc)
 for k in range(2):
  cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'];p=subprocess.run(cmd,cwd=R,capture_output=True,text=True);records.append({'name':name,'pass':k+1,'command':cmd,'exit_status':p.returncode,'stdout':p.stdout});(R/'verification.json').write_text(json.dumps(records,indent=2))
  if p.returncode:raise RuntimeError(p.stdout[-1800:])
 log=(R/(name+'.log')).read_text(errors='replace');assert 'Overfull' not in log,(name,'overfull')
 subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1800','-png',name+'.pdf',name],cwd=R,check=True,capture_output=True)
for key in ['wide','metric-1','metric-2','metric-3']:
 s=(R/(key+'.tex')).read_text();s=re.sub(r'\\begin\{table\*?\}\[t\]','',s);s=re.sub(r'\\end\{table\*?\}','',s)
 compile(key+'-preview',r'\documentclass[varwidth=183mm,border=3mm]{standalone}\input{packages}\usepackage{caption}\begin{document}\captionsetup{type=table}'+s+r'\end{document}')
compile('longtable-preview',r'\documentclass[10pt]{article}\usepackage[paperwidth=210mm,paperheight=160mm,margin=15mm]{geometry}\input{packages}\begin{document}\input{dataset-blocks}\end{document}')
# Width tests do not shrink fonts or scale the table box.
compile('integration',r'''\documentclass[10pt,twocolumn]{article}\usepackage[a4paper,margin=18mm]{geometry}\input{packages}
\newsavebox{\checktable}\begin{document}
\sbox{\checktable}{\small\setlength{\tabcolsep}{2.5pt}\input{wide-body}}\ifdim\wd\checktable>\textwidth\errmessage{Wide table exceeds textwidth}\fi
\input{wide}\clearpage
\input{metric-1}\clearpage\input{metric-2}\clearpage\input{metric-3}\clearpage
\end{document}''')
assert v.shape==(9,4,3)
assert all((i,0,0,'best') in marked for i in [0,1]);assert (2,0,0,'second') in marked
for d in range(4):assert (int(v[:,d,2].argmin()),d,2,'best') in marked
(R/'review.json').write_text(json.dumps({'cells_per_layout':108,'methods':9,'baselines':8,'datasets':4,'metrics':3,'seed_count':1,'rank_ties_checked':True,'lower_is_better_checked':True,'all_compiles_overfull':0,'official_venue_class_tested':False},indent=2))
print('PASS: 108 cells; ties and ECE direction verified; 6 LaTeX documents compiled twice without overfull warnings.')
