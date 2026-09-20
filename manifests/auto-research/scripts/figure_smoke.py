# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.8,<4", "numpy>=1.26,<3", "Pillow>=10,<13", "PyYAML>=6,<7"]
# ///
"""17 synthetic rendering fixtures, not a production scientific plotting backend."""
import argparse, hashlib, json, os, tempfile
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, Polygon
import numpy as np
import yaml
from PIL import Image, ImageDraw


def atomic_json(path,value):
    fd,name=tempfile.mkstemp(dir=path.parent,suffix='.tmp')
    with os.fdopen(fd,'w') as f:json.dump(value,f,indent=2)
    os.replace(name,path)


def label_color(rgba):
    rgb=np.array(rgba[:3])
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    lum=float(linear @ np.array([.2126,.7152,.0722]))
    return '#000000' if (lum+.05)/.05 >= 1.05/(lum+.05) else '#FFFFFF'


def render(kind,d,c,cm):
    fig,ax=plt.subplots(figsize=(5.5,3.9))
    fig.subplots_adjust(left=.17,right=.92,bottom=.23,top=.90)
    ax.spines[['top','right']].set_visible(False)
    ax.set_axisbelow(True);ax.grid(axis='y',color='#E6EBEF',linewidth=.6)
    def box(x,y,label,color=0,w=1.5,h=.65):
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.08',facecolor=c[color],alpha=.16,edgecolor=c[color]))
        ax.text(x,y,label,ha='center',va='center',fontsize=10)
    def arrow(a,b,label=''):
        ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#52616B','lw':1.2})
        if label:ax.text((a[0]+b[0])/2+.1,(a[1]+b[1])/2,label,fontsize=8)
    def canvas():ax.clear();ax.axis('off');ax.set_xlim(-1,7);ax.set_ylim(-.8,4)
    x=np.array(d['x']);vals=np.array(d['values']);matrix=np.array(d['matrix'])
    if kind=='architecture':
        canvas()
        for xx,yy,label,k in [(0,1.5,'Input',0),(2.5,2.7,'Encoder A',1),(2.5,.3,'Encoder B',2),(5,1.5,'Fusion',0),(5,3.2,'Output',3)]:box(xx,yy,label,k)
        for a,b in [((.8,1.5),(1.7,2.7)),((.8,1.5),(1.7,.3)),((3.3,2.7),(4.2,1.5)),((3.3,.3),(4.2,1.5)),((5,1.9),(5,2.8))]:arrow(a,b)
    elif kind=='flowchart':
        canvas();box(0,3,'Start');box(2.5,3,'Evaluate',1);box(5,3,'Accept',2);box(2.5,.5,'Revise',3)
        ax.add_patch(Polygon([(2.5,2.3),(3.3,1.7),(2.5,1.1),(1.7,1.7)],facecolor=c[1],alpha=.2))
        ax.text(2.5,1.7,'Pass?',ha='center');arrow((.8,3),(1.7,3));arrow((2.5,2.6),(2.5,2.3));arrow((3.3,1.7),(5,2.6),'yes');arrow((2.5,1.1),(2.5,.9),'no')
        ax.annotate('',xy=(1.7,3),xytext=(1.7,.5),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=-.45','color':'#52616B'})
    elif kind=='pipeline':
        canvas()
        for i,l in enumerate(['Collect','Train','Evaluate']):
            box(i*2.5,2.5,l,i);box(i*2.5,.5,['Dataset','Weights','Metrics'][i],i);arrow((i*2.5,2.1),(i*2.5,.9))
            if i<2:arrow((i*2.5+.8,2.5),(i*2.5+1.7,2.5))
    elif kind=='algorithm':
        canvas()
        for i,l in enumerate(['1  Initialize state','2  Compute gradient','3  Update state','4  Check convergence']):
            y=3-i;box(2,y,l,i%4,w=3.8,h=.52)
            if i<3:arrow((2,y-.35),(2,y-.65))
        ax.text(5,1.6,'Repeat 2–4\nuntil tolerance',ha='center',fontsize=9)
        ax.annotate('',xy=(4,2),xytext=(4,0),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=.2','color':'#52616B'})
    elif kind=='comparison':
        means=vals.mean(axis=1);sd=vals.std(axis=1,ddof=1)
        for i in range(3):ax.errorbar(means[i],i,xerr=sd[i],fmt=['o','s','D'][i],color=c[i],capsize=4)
        ax.set_yticks(range(3),['Baseline A','Baseline B','Ours']);ax.set_xlabel('Score');ax.set_xlim(.55,.95)
    elif kind=='ablation':
        delta=vals-vals[-1];ax.axvline(0,color='#6D7885',lw=1)
        for i in range(3):ax.errorbar(delta[i].mean(),i,xerr=delta[i].std(ddof=1),fmt='o',color=c[i],capsize=4)
        ax.set_yticks(range(3),['Without A','Without B','Full']);ax.set_xlabel('Difference from full model')
    elif kind=='training_curve':
        for i in range(3):ax.plot(x,np.array(d['curves'])[i],label=['Train','Validation','Reference'][i],color=c[i],ls=['--','-',':'][i])
        ax.set(xlabel='Step',ylabel='Synthetic loss');ax.legend(frameon=False)
    elif kind=='scaling':
        ax.plot(d['cost'],d['score'],'o-',color=c[0]);ax.set_xscale('log');ax.set(xlabel='Compute (log scale)',ylabel='Score')
    elif kind=='distribution':
        samples=np.array(d['samples']);ax.boxplot(samples.T,showfliers=True,medianprops={"color":c[0],"linewidth":1.3})
        for i,v in enumerate(samples):ax.scatter(np.full(len(v),i+1)+np.linspace(-.12,.12,len(v)),v,s=10,alpha=.6,color=c[i])
        ax.set_xticks([1,2,3],['Group A','Group B','Group C']);ax.set_ylabel('Sample value')
    elif kind=='scatter':
        ax.scatter(x,d['scatter'],c=c[0],s=24,alpha=.75);ax.set(xlabel='Input value',ylabel='Observed value');ax.grid(True,color='#E6EBEF')
    elif kind=='heatmap':
        ax.grid(False);im=ax.imshow(matrix,cmap=cm,vmin=0,vmax=1);fig.colorbar(im,ax=ax,label='Score');ax.set(xlabel='Parameter B',ylabel='Parameter A');ax.set_xticks(range(4),['B1','B2','B3','B4']);ax.set_yticks(range(3),['A1','A2','A3'])
        for (i,j),v in np.ndenumerate(matrix):ax.text(j,i,f'{v:.2f}',ha='center',va='center',color=label_color(cm(v)),fontsize=9)
    elif kind=='confusion_matrix':
        ax.grid(False);m=np.array(d['confusion']);im=ax.imshow(m,cmap=cm,vmin=0,vmax=m.max());fig.colorbar(im,ax=ax,label='Count')
        ax.set(xlabel='Predicted class',ylabel='True class');ax.set_xticks(range(3),['A','B','C']);ax.set_yticks(range(3),['A','B','C'])
        for (i,j),v in np.ndenumerate(m):ax.text(j,i,str(v),ha='center',va='center',color=label_color(cm(v/m.max())))
    elif kind=='qualitative_grid':
        ax.remove()
        for i in range(6):
            a=fig.add_subplot(2,3,i+1);a.imshow(np.array(d['images'])[i],cmap=cm,vmin=0,vmax=1);a.axis('off');a.set_title(['Input','Baseline','Method'][i%3],fontsize=10)
        fig.subplots_adjust(wspace=.08,hspace=.22)
    elif kind=='attention':
        ax.remove()
        for i,title in enumerate(['Input','Synthetic attribution']):
            a=fig.add_subplot(1,2,i+1);a.imshow(d['images'][0],cmap='gray',vmin=0,vmax=1)
            if i:
                a.imshow(d['images'][1],cmap=cm,alpha=.6,vmin=0,vmax=1)
                fig.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(0,1),cmap=cm),ax=a,fraction=.05,label='Attribution')
            a.axis('off');a.set_title(title,fontsize=10)
    elif kind=='timeline':
        t=np.array([0,3,10,17]);ax.hlines(0,0,17,color=c[0]);ax.scatter(t,[0]*4,color=c[0],s=40)
        for i,(xx,l) in enumerate(zip(t,['Start','Pilot','Analysis','Draft'])):ax.annotate(l,(xx,0),xytext=(0,25 if i%2==0 else -30),textcoords='offset points',ha='center')
        ax.set(xlabel='Elapsed days',ylim=(-1,1));ax.set_yticks([]);ax.grid(False)
    elif kind=='map':
        # Artificial Cartesian regions, deliberately not geographic evidence.
        ax.grid(False)
        for i in range(4):
            for j in range(3):ax.add_patch(Polygon([(i,j),(i+1,j),(i+1,j+1),(i,j+1)],facecolor=cm(matrix[j,i]),edgecolor='white',lw=1))
        ax.set(xlim=(0,4),ylim=(0,3),xlabel='Synthetic local x (km)',ylabel='Synthetic local y (km)');ax.set_aspect('equal')
        fig.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(0,1),cmap=cm),ax=ax,label='Synthetic value')
    elif kind=='concept_illustration':
        canvas()
        for xx,l,k in [(0,'Observe',0),(2.5,'Explain',1),(5,'Predict',2)]:box(xx,1.7,l,k)
        arrow((.8,1.7),(1.7,1.7));arrow((3.3,1.7),(4.2,1.7));ax.text(2.5,.2,'Mechanism storyboard — not measured evidence',ha='center',fontsize=9)
    else:raise ValueError(kind)
    fig.text(.17,.95,kind.replace('_',' ').upper(),fontsize=10,fontweight='bold',color='#243240')
    fig.text(.17,.055,'Synthetic fixture · not research evidence',fontsize=8,color='#52616B')
    if kind in {'comparison','ablation'}:fig.text(.17,.105,'3 paired seeds · mean ± sample SD',fontsize=8,color='#52616B')
    return fig


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--palette',default='editorial',choices=['editorial','contrast','earth','monochrome']);args=parser.parse_args()
    root=Path(__file__).resolve().parents[1];lib=yaml.safe_load((root/'writing/figure-types.yaml').read_text());pack=yaml.safe_load((root/'writing/figure-palettes.yaml').read_text());p=pack['palettes'][args.palette]
    args.output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'Liberation Sans','font.size':10.5,'axes.labelsize':11,'xtick.labelsize':9.5,'ytick.labelsize':9.5,'legend.fontsize':9,'axes.linewidth':.7,'lines.linewidth':1.5,'svg.fonttype':'none','svg.hashsalt':'figure-smoke','pdf.fonttype':42,'axes.labelcolor':'#243240','text.color':'#243240'})
    rng=np.random.default_rng(42);x=np.arange(20);yy,xx=np.mgrid[-1:1:24j,-1:1:24j]
    data={'synthetic':True,'seed':42,'x':x.tolist(),'values':[[.65,.67,.66],[.75,.76,.74],[.84,.85,.83]],'curves':[(np.exp(-x/(5+i))+.1*i).tolist() for i in range(3)],'cost':[1,3,10,30],'score':[.6,.72,.81,.85],'samples':rng.normal([0,1,2],.5,(24,3)).T.tolist(),'scatter':(x*.4+rng.normal(0,1,20)).tolist(),'matrix':rng.uniform(0,1,(3,4)).tolist(),'confusion':[[24,3,1],[2,21,5],[1,4,23]],'images':[np.exp(-((xx-i*.08)**2+(yy+i*.05)**2)*4).tolist() for i in range(6)]}
    atomic_json(args.output/'inputs.json',data);records=[]
    pending=[]
    for kind,spec in lib['types'].items():
        if spec['renderer']=='gpt-image':
            pending.append({'type':kind,'status':'blocked_backend_unavailable','renderer':'gpt-image','editable_renderer':'gpt-pptx','reason':'local smoke runner does not dispatch external models'})
            continue
        mode=spec['implementation']['color_mode'];mode='sequential' if kind=='qualitative_grid' else mode;cm=LinearSegmentedColormap.from_list('preset',p[mode]);fig=render(kind,data,p['categorical'],cm)
        for ext in ['svg','pdf','png']:
            dest=args.output/(kind+'.'+ext);fd,tmp=tempfile.mkstemp(dir=args.output,suffix='.'+ext);os.close(fd)
            fig.savefig(tmp,format=ext,dpi=160,metadata={'Creator':'synthetic-figure-smoke'} if ext=='pdf' else None);os.replace(tmp,dest)
        plt.close(fig)
        records.append({'type':kind,'synthetic':True,'palette':args.palette,'visual_review':'pending','outputs':{e:hashlib.sha256((args.output/(kind+'.'+e)).read_bytes()).hexdigest() for e in ['svg','pdf','png']}})
    # Contact sheet is a layout operation on generated scientific fixtures.
    sheet=Image.new('RGB',(1200,300*4),'#F4F5F7')
    for i,rec in enumerate(records):
        with Image.open(args.output/(rec['type']+'.png')) as im:
            im.thumbnail((400,290));sheet.paste(im,((i%3)*400,(i//3)*300))
    sheet.save(args.output/'contact-sheet.png');atomic_json(args.output/'manifest.json',records);atomic_json(args.output/'generation-requests.json',pending)
    print(json.dumps({'types':len(records),'palette':args.palette,'output':str(args.output)}))
if __name__=='__main__':main()
