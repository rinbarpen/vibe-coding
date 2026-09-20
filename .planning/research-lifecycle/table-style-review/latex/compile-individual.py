from pathlib import Path
import subprocess,json,re,shutil
R=Path(__file__).parent;out=R/'individual';out.mkdir(exist_ok=True);records=[]
for p in sorted((R/'tables').glob('*.tex')):
 key=p.stem
 if 'longtable' in key:
  doc=r'\documentclass[10pt]{article}\usepackage[paperwidth=210mm,paperheight=160mm,margin=18mm]{geometry}\input{table-packages}\begin{document}\input{tables/'+key+r'}\end{document}'
 else:
  content=p.read_text();content=re.sub(r'\\begin\{table\*?\}\[t\]','',content);content=re.sub(r'\\end\{table\*?\}','',content)
  doc=r'\documentclass[varwidth=183mm,border=3mm]{standalone}\input{table-packages}\usepackage{caption}\begin{document}\captionsetup{type=table}'+content+r'\end{document}'
 wrapper=R/(key+'-standalone.tex');wrapper.write_text(doc)
 for step in range(2):
  cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory=individual',wrapper.name];v=subprocess.run(cmd,cwd=R,text=True,capture_output=True);records.append({'table':key,'pass':step+1,'command':cmd,'exit_status':v.returncode,'stdout':v.stdout})
  (R/'individual-verification.json').write_text(json.dumps(records,indent=2))
  if v.returncode:print(v.stdout[-2000:]);raise SystemExit(v.returncode)
 pdf=out/(key+'-standalone.pdf');shutil.copy2(pdf,out/(key+'.pdf'));log=(out/(key+'-standalone.log')).read_text(errors='replace');assert 'Overfull' not in log,(key,'overfull')
 cmd=['pdftoppm','-f','1','-singlefile','-scale-to','1400','-png',str(out/(key+'.pdf')),str(out/key)];subprocess.run(cmd,check=True,capture_output=True)
 result=subprocess.run(['pdftotext',str(out/(key+'.pdf')),'-'],capture_output=True,text=True,check=True);(out/(key+'.txt')).write_text(result.stdout)
 if 'longtable' in key:assert 'continued' in result.stdout and 'config-032' in result.stdout
 print(key,'PASS')
print('ALL',len(list((R/'tables').glob('*.tex'))),'TABLES COMPILED TWICE; zero overfull warnings.')
