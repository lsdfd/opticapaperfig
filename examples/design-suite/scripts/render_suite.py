"""Six reproducible, synthetic optics figure redesigns. No experimental claims."""
from pathlib import Path
import argparse, json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Ellipse, FancyArrowPatch
from matplotlib.colors import Normalize
from scipy.ndimage import gaussian_filter
from optica_style import style, export_figure
from audit_pdf import audit

BLUE='#24769B'; ORANGE='#C17B39'; GREY='#6C7681'; INK='#24313C'
DPI=360

def digest(*items):
    h=hashlib.sha256()
    for obj in items:
        a=np.ascontiguousarray(obj);h.update(str((a.shape,a.dtype)).encode());h.update(a.tobytes())
    return h.hexdigest()

class Evidence:
    def __init__(self):self.records={}
    def register(self,key,artist):
        ax=artist.axes
        if not hasattr(ax,'_evidence_ids'):ax._evidence_ids=[]
        ax._evidence_ids.append(key)
    def ranges(self,fig):
        for ax in fig.axes:
            if hasattr(ax,'_evidence_ids'):
                key='axes-range:'+','.join(sorted(ax._evidence_ids))
                self.records[key]=digest(np.asarray(ax.get_xlim()+ax.get_ylim(),float))
    def line(self,key,artist):
        self.register(key,artist)
        self.records[key]=digest(np.asarray(artist.get_xdata()),np.asarray(artist.get_ydata()))
    def image(self,key,artist):
        self.register(key,artist)
        a=np.ma.asarray(artist.get_array())
        self.records[key]=digest(a.filled(np.nan),np.ma.getmaskarray(a),np.asarray(artist.get_clim(),float),np.asarray(artist.get_extent(),float))
    def semantic(self,key,obj):self.records[key]=hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()


def dataset():
    rng=np.random.default_rng(4317);d={}
    w=np.linspace(100,260,121);l=np.linspace(120,300,101);W,L=np.meshgrid(w,l)
    d.update(width=w,length=l,phi_te=2.7*np.tanh((W-175)/40)+.20*np.sin(L/35),phi_tm=2.5*np.tanh((L-200)/50)+.25*np.cos(W/40))
    wave=np.linspace(500,750,251);eta_te=.55+.31*np.exp(-((wave-621)/72)**2);eta_tm=.48+.33*np.exp(-((wave-639)/78)**2)
    ids=np.arange(0,len(wave),16)
    d.update(wave=wave,eta_te=eta_te,eta_tm=eta_tm,sample_wave=wave[ids],sample_te=eta_te[ids]+rng.normal(0,.013,len(ids)),sample_tm=eta_tm[ids]+rng.normal(0,.013,len(ids)),cross_te=.025+.025*((wave-620)/130)**2,cross_tm=.035+.022*((wave-640)/130)**2,angle_te=np.degrees(np.arcsin(wave/1700)),angle_tm=-np.degrees(np.arcsin(wave/1900)))
    x=(np.arange(151)-75)*6/151;X,Y=np.meshgrid(x,x)
    for name,c in [('te',-.60),('tm',.60)]:
        ref=np.exp(-2*((X-c)**2+(Y*.95)**2)/.65**2)
        pred=.94*np.exp(-2*((X-c-.09)**2+((Y+.05)*.95)**2)/.67**2)
        d['field_'+name]=ref;d['model_'+name]=pred;d['residual_'+name]=pred-ref
    d['field_x']=x;d['residual_limit']=np.ceil(max(np.abs(d['residual_te']).max(),np.abs(d['residual_tm']).max())*100)/100
    n=240;coords=(np.arange(n)+.5)*40/n-20;X,Y=np.meshgrid(coords,coords)
    target=np.zeros((n,n))
    for low,high,period in [(-17,-7,3.2),(-5,5,2.),(7,17,1.2)]:
        target[(X>low)&(X<high)&(np.abs(Y)<6)&(((X-low)%period)<period/2)]=1
    target[((np.hypot(X+11,Y-12)>3)&(np.hypot(X+11,Y-12)<4))]=1
    target[(np.abs(X-9)<.6)&(Y>9)&(Y<16)]=1;target[(X>5)&(X<13)&(np.abs(Y-12.5)<.6)]=1
    im_a=np.clip(gaussian_filter(target,2.1)+rng.normal(0,.012,target.shape),0,1)
    im_b=np.clip(gaussian_filter(target,.85)+rng.normal(0,.012,target.shape),0,1)
    d.update(image_x=coords,image_reference=target,image_a=im_a,image_b=im_b)
    n=65;cx=(np.arange(n)+.5)*2/n-1;XX,YY=np.meshgrid(cx,cx);theta=.8*XX+.5*YY;delta=1.3+.6*XX
    nvec=np.stack([np.cos(2*theta),np.sin(2*theta),np.zeros_like(theta)],axis=-1)
    m=np.zeros((4,4,n,n));m[0,0]=1
    skew=np.zeros((n,n,3,3));skew[...,0,2]=nvec[...,1];skew[...,1,2]=-nvec[...,0];skew[...,2,0]=-nvec[...,1];skew[...,2,1]=nvec[...,0]
    rot=np.cos(delta)[...,None,None]*np.eye(3)+(1-np.cos(delta))[...,None,None]*nvec[..., :,None]*nvec[...,None,:]+np.sin(delta)[...,None,None]*skew
    assert np.max(np.abs(np.einsum('...ji,...jk->...ik',rot,rot)-np.eye(3)))<1e-12
    for i in range(3):
        for j in range(3):m[i+1,j+1]=rot[...,i,j]
    d['mueller']=m
    return d


def create(height,after,title):
    fig=plt.figure(figsize=(178/25.4,height/25.4));fig._h=height
    if not after:
        fig.suptitle(title,fontsize=10,y=.965)
        fig.text(.065,.014,'SYNTHETIC DESIGN STUDY · no experimental data',fontsize=6.5)
    return fig

def axes(fig,x,y,w,h):return fig.add_axes([x/178,y/fig._h,w/178,h/fig._h])
def label(ax,s,after,x=-.15,y=1.06):
    ax.text(x,y,s,transform=ax.transAxes,ha='left',va='bottom',fontsize=7.5,fontweight='normal' if after else 'normal',color='#111111')
def clean(ax,after):
    if after:ax.spines[['top','right']].set_visible(False);ax.tick_params(pad=2)
    else:ax.grid(True,alpha=.65)
def line(ax,e,key,x,y,after,channel=0,label_=None,**kw):
    col=[BLUE,ORANGE][channel] if after else ['#1f77b4','#ff7f0e'][channel]
    obj,=ax.plot(x,y,color=col,label=label_,**kw);e.line(key,obj);return obj

def heat(ax,e,key,z,extent,vmin,vmax,after,kind='intensity'):
    cm=('magma' if kind=='intensity' else 'twilight' if kind=='phase' else 'RdBu_r' if kind=='signed' else 'gray') if after else ('gray' if kind=='gray' else 'jet')
    im=ax.imshow(z,origin='lower',extent=extent,vmin=vmin,vmax=vmax,cmap=cm,interpolation='nearest',aspect='equal');e.image(key,im);return im

def cb(fig,im,rect,caption,ticks=None):
    ax=axes(fig,*rect);c=fig.colorbar(im,cax=ax);c.ax.tick_params(labelsize=6.5,pad=2,length=2)
    if ticks is not None:c.set_ticks(ticks)
    c.set_label(caption,fontsize=7,labelpad=4);return c


def concept(d,after):
    fig=create(93,after,'Polarization routing');e=Evidence();ax=axes(fig,7,13,164,65);ax.set(xlim=(0,16),ylim=(0,6.5));ax.axis('off')
    semantics={'input':['TE','TM'],'device':'anisotropic meta-atom array','array_shape':[6,5],'outputs':['TE channel','TM channel'],'edges':[['input','device'],['device','TE channel'],['device','TM channel']],'colors':'channel identity, not wavelength','not_to_scale':True};e.semantic('concept',semantics)
    if after:
        # Flat vector surfaces share one oblique basis; no generated raster artwork.
        O=np.array([6.8,1.35]);u=np.array([1.8,.55]);v=np.array([-.6,3.3]);offset=np.array([.08,-.20])
        corners=[O,O+u,O+u+v,O+v];ax.add_patch(Polygon(np.array(corners)+offset,fc='#A6B3B7',ec='none'))
        ax.add_patch(Polygon(corners,fc='#E2E9E9',ec='#9EAEB2',lw=.7))
        for i in range(6):
            for j in range(5):
                c=O+(i+.5)/6*u+(j+.5)/5*v;aa=.105*u;bb=.09*v
                p=np.array([c-aa/2-bb/2,c+aa/2-bb/2,c+aa/2+bb/2,c-aa/2+bb/2]);lift=np.array([0,.16])
                ax.add_patch(Polygon(p,fc='#5F7B82',ec='none'));ax.add_patch(Polygon(p+lift,fc='#B1C3C6',ec='#526F78',lw=.35))
        center=np.array([7.35,3.30]);start=np.array([1.6,3.3])
        for delta,col in [(.10,BLUE),(-.10,ORANGE)]:
            ax.plot([start[0],center[0]],[start[1]+delta,center[1]+delta],color=col,lw=1.4,zorder=0)
        for point,col,name in [(np.array([13.7,4.7]),BLUE,'TE'),(np.array([13.7,1.8]),ORANGE,'TM')]:
            ax.add_patch(Polygon([center+[-.12,.18],center+[.12,-.18],point+[.0,-.35],point+[.0,.35]],fc=col,alpha=.12,ec='none',zorder=0))
            ax.add_patch(FancyArrowPatch(center,point,arrowstyle='-|>',mutation_scale=9,color=col,lw=1.2,zorder=0))
            ax.add_patch(Ellipse(point,(.45),1.3,fc='#F3F6F6',ec='#C7D1D5',lw=.6))
            ax.add_patch(Ellipse(point,.18,.55,fc=col,ec='none',alpha=.85));ax.text(14.2,point[1],name,color=col,va='center',fontsize=7.5,fontweight='normal')
        ax.text(1,4.05,'TE + TM',fontsize=8,color=INK);ax.text(1,2.65,'Input',fontsize=7,color=GREY)
        ax.text(7.2,.60,'Anisotropic meta-atoms',fontsize=7.5,ha='center');ax.text(13.9,.60,'Separated channels',fontsize=7.5,ha='center')
    else:
        rects=[(1,2.8,2.7,1,'TE + TM\ninput'),(6,2.3,3,2,'Anisotropic\nmeta-atom array'),(12,4.3,2.8,1,'TE channel'),(12,.9,2.8,1,'TM channel')]
        for i,(x,y,w,h,t) in enumerate(rects):ax.add_patch(Rectangle((x,y),w,h,fc=['#e1eff7','#dddddd','#e1eff7','#ffead0'][i],ec='black',lw=1));ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=8)
        for a,b in [((3.7,3.3),(6,3.3)),((9,3.3),(12,4.8)),((9,3.3),(12,1.4))]:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':1.3})
        for i in range(6):
            for j in range(5):ax.add_patch(Rectangle((6.25+i*.42,4.7+j*.16),.19,.09,fc=GREY))
    if not after:fig.text(.5,9/93,'Schematic, not to scale. Blue/orange identify polarization channels.',ha='center',fontsize=6.5,color=GREY)
    return fig,e,[]


def library(d,after):
    fig=create(139,after,'Meta-atom phase design');e=Evidence();w=d['width'];l=d['length'];extent=[w[0]-(w[1]-w[0])/2,w[-1]+(w[1]-w[0])/2,l[0]-(l[1]-l[0])/2,l[-1]+(l[1]-l[0])/2]
    if after:aa=[axes(fig,20,61,60,60),axes(fig,103,61,60,60),axes(fig,20,17,143,31)]
    else:aa=list(fig.subplots(1,3));fig.subplots_adjust(left=.10,right=.94,bottom=.20,top=.83,wspace=.65)
    ims=[]
    for i,(ax,z) in enumerate(zip(aa[:2],[d['phi_te'],d['phi_tm']])):
        im=heat(ax,e,'phase_'+str(i),z,extent,-np.pi,np.pi,after,'phase');ims.append(im)
        ax.set(xlabel='Width (nm)',ylabel='Length (nm)',title=['TE phase','TM phase'][i],xlim=(100,260),ylim=(120,300));label(ax,chr(97+i),after)
        if after:
            ax.axhline(l[45],color='white',lw=.7,ls='--');ax.set(xticks=[100,180,260],yticks=[120,210,300])
            if i==1:ax.set_ylabel('');ax.tick_params(labelleft=False)
        else:fig.colorbar(im,ax=ax,fraction=.05,pad=.05)
    if after:
        # Equal physical aspect compresses axes horizontally; colorbar has its own slot.
        cax=axes(fig,85,65,2,54);c=fig.colorbar(ims[0],cax=cax);c.set_ticks([-np.pi,0,np.pi],labels=['−π','0','π']);c.ax.tick_params(labelsize=7,pad=2);c.set_label('Phase (rad)',fontsize=7)
    ax=aa[2]
    for i,key in enumerate(['phi_te','phi_tm']):line(ax,e,'cut_'+key,w,d[key][45],after,i,['TE','TM'][i],lw=1.2,ls='-' if i==0 or not after else '--')
    ax.set(xlabel='Width (nm)',ylabel='Phase (rad)',xlim=(100,260),ylim=(-np.pi,np.pi),title=f'Cross-section at length = {l[45]:.0f} nm',yticks=[-np.pi,0,np.pi],yticklabels=['−π','0','π']);ax.legend(loc='lower right',ncol=2 if after else 1);clean(ax,after);label(ax,'c',after,x=-.065 if after else -.15)
    return fig,e,[aa[:2]]


def spectra(d,after):
    fig=create(104,after,'Spectral response and channel separation');e=Evidence();wave=d['wave']
    if after:aa=[axes(fig,17,21,90,64),axes(fig,128,61,40,24),axes(fig,128,21,40,24)]
    else:aa=list(fig.subplots(1,3));fig.subplots_adjust(left=.10,right=.95,bottom=.20,top=.82,wspace=.60)
    ax=aa[0]
    for i,ch in enumerate(['te','tm']):
        line(ax,e,'eta_'+ch,wave,d['eta_'+ch],after,i,ch.upper()+' model',lw=1.25,ls='-' if i==0 or not after else '--')
        line(ax,e,'sample_'+ch,d['sample_wave'],d['sample_'+ch],after,i,ch.upper()+' samples',ls='none',marker='o' if i==0 else 's',ms=3,mfc='white' if after else None,mew=.75)
    ax.set(xlabel='Wavelength (nm)',ylabel='Channel efficiency',xlim=(500,750),ylim=(0,1));ax.legend(loc='lower center',ncol=2,fontsize=6.5);clean(ax,after);label(ax,'a',after,x=-.12)
    ax=aa[1]
    for i,ch in enumerate(['te','tm']):line(ax,e,'cross_'+ch,wave,d['cross_'+ch],after,i,ch.upper(),ls='-' if i==0 or not after else '--',lw=1.15)
    ax.set(xlim=(500,750),ylim=(0,.1),ylabel='Leakage',title='Opposite channel',xticks=[500,625,750]);clean(ax,after);label(ax,'b',after,x=-.25)
    ax=aa[2]
    for i,ch in enumerate(['te','tm']):line(ax,e,'angle_'+ch,wave,d['angle_'+ch],after,i,ch.upper(),ls='-' if i==0 or not after else '--',lw=1.15)
    ax.set(xlabel='Wavelength (nm)',ylabel='Angle (°)',xlim=(500,750),ylim=(-30,30),xticks=[500,625,750]);ax.axhline(0,color='#b5bec4',lw=.6);clean(ax,after);label(ax,'c',after,x=-.25)
    return fig,e,[]


def fields(d,after):
    fig=create(123,after,'Spatial field agreement');e=Evidence()
    if after:aa=np.array([[axes(fig,16+55*j,68-50*i,34,34) for j in range(3)] for i in range(2)])
    else:aa=fig.subplots(2,3);fig.subplots_adjust(left=.10,right=.94,bottom=.15,top=.83,wspace=.65,hspace=.65)
    ims=[];lim=float(d['residual_limit'])
    for i,ch in enumerate(['te','tm']):
        for j,prefix in enumerate(['field','model','residual']):
            ax=aa[i,j];im=heat(ax,e,f'{prefix}_{ch}',d[f'{prefix}_{ch}'],[-3,3,-3,3],-lim if j==2 else 0,lim if j==2 else 1,after,'signed' if j==2 else 'intensity');ims.append(im)
            ax.set(xticks=[-3,0,3],yticks=[-3,0,3]);label(ax,chr(97+3*i+j),after,x=0 if after else -.20)
            if i==0:ax.set_title(['Target intensity','Model intensity','Model − target'][j],fontsize=7.5)
            if i==1 or not after:ax.set_xlabel(r'$x$ (μm)')
            if j==0 or not after:ax.set_ylabel(r'$y$ (μm)')
            if after and j>0:ax.tick_params(labelleft=False)
            if not after:fig.colorbar(im,ax=ax,fraction=.045,pad=.04)
        if after:fig.text(3/178,(85-50*i)/123,ch.upper(),color=[BLUE,ORANGE][i],fontsize=7.5,fontweight='normal',rotation=90,va='center')
    if after:
        cb(fig,ims[0],(108,18,2,84),'Shared intensity',[0,.5,1]);cb(fig,ims[2],(163,18,2,84),'Difference',[-lim,0,lim])
    return fig,e,[list(aa.flat)]


def imaging(d,after):
    fig=create(168,after,'Image detail and spatial contrast');e=Evidence();names=['reference','a','b'];titles=['Reference','Blur A','Blur B'];x=d['image_x'];roi=np.where((x>=-5)&(x<=5))[0];xx=x[roi];dx=x[1]-x[0]
    if after:
        full=[axes(fig,17+53*i,103,40,40) for i in range(3)];crops=[axes(fig,23+53*i,61,28,28) for i in range(3)];prof=axes(fig,17,17,146,27)
    else:
        arr=fig.subplots(2,4).flatten();full=list(arr[:3]);crops=list(arr[3:6]);prof=arr[6];arr[7].axis('off');fig.subplots_adjust(left=.09,right=.96,bottom=.17,top=.84,wspace=.65,hspace=.7)
    for i,(name,ax) in enumerate(zip(names,full)):
        z=d['image_'+name];im=heat(ax,e,'full_'+name,z,[-20,20,-20,20],0,1,after,'gray');ax.set(title=titles[i],xticks=[-20,0,20],yticks=[-20,0,20]);ax.add_patch(Rectangle((-5,-5),10,10,fc='none',ec=BLUE if after else 'red',lw=.8))
        if i==0 or not after:ax.set_ylabel(r'$y$ (μm)')
        if after and i>0:ax.tick_params(labelleft=False)
        if not after:ax.set_xlabel(r'$x$ (μm)')
        label(ax,chr(97+i),after,x=-.18)
        crop=z[np.ix_(roi,roi)];ax=crops[i];heat(ax,e,'roi_'+name,crop,[xx[0]-dx/2,xx[-1]+dx/2,xx[0]-dx/2,xx[-1]+dx/2],0,1,after,'gray')
        ax.set(xticks=[-5,0,5],yticks=[-5,0,5]);ax.set_xlabel(r'$x$ (μm)')
        if after:
            ax.axhline(x[len(x)//2],color=BLUE,lw=.65,ls='--');ax.set_title('Same 10 μm ROI',fontsize=6.5)
            if i>0:ax.tick_params(labelleft=False)
        else:ax.set(title='ROI '+titles[i],ylabel=r'$y$ (μm)')
        label(ax,chr(100+i),after,x=-.24)
    ax=prof
    for i,name in enumerate(names):
        artist,=ax.plot(x,d['image_'+name][len(x)//2],color=[INK,ORANGE,BLUE][i] if after else ['k','r','b'][i],ls=['-',':','--'][i] if after else '-',lw=.9 if i==0 else 1.1,label=titles[i]);e.line('profile_'+name,artist)
    ax.set(xlabel=r'$x$ (μm)',ylabel='Intensity',xlim=(-20,20),ylim=(-.05,1.12));ax.legend(loc='lower right' if after else 'upper center',bbox_to_anchor=(1,1.02) if after else None,ncol=3,fontsize=6.5,borderaxespad=0);clean(ax,after)
    if after:ax.set_title(f'Profile at y = {x[len(x)//2]:.3f} μm',loc='left',fontsize=7,pad=6)
    label(ax,'g',after,x=-.06)
    return fig,e,[full,crops]


def mueller(d,after):
    fig=create(163,after,'Spatially varying polarization transfer');e=Evidence()
    if after:aa=np.array([[axes(fig,29+32*j,116-32*i,27,27) for j in range(4)] for i in range(4)])
    else:aa=fig.subplots(4,4);fig.subplots_adjust(left=.10,right=.95,bottom=.12,top=.87,wspace=.75,hspace=.75)
    for i in range(4):
        for j in range(4):
            ax=aa[i,j];im=heat(ax,e,f'M{i}{j}',d['mueller'][i,j],[-1,1,-1,1],-1,1,after,'signed');ax.set(xticks=[-1,1],yticks=[-1,1]);ax.tick_params(labelsize=6.5)
            if after:
                for sp in ax.spines.values():sp.set_color('#c7cfd4');sp.set_linewidth(.5)
                ax.tick_params(labelleft=j==0,labelbottom=i==3,length=2)
                if i==3:ax.set_xlabel(r'$x$ (a.u.)',fontsize=6.5,labelpad=1)
                if j==0:fig.text(16/178,(129.5-32*i)/163,'$S_'+str(i)+'$',fontsize=8,ha='center',va='center')
                if i==0:fig.text((42.5+32*j)/178,147/163,'$S_'+str(j)+'$',fontsize=8,ha='center')
            else:ax.set(title=f'M{i}{j}',xlabel=r'$x$ (a.u.)',ylabel=r'$y$ (a.u.)');fig.colorbar(im,ax=ax,fraction=.06,pad=.03)
    if after:
        c=cb(fig,im,(162,20,2,123),'Normalized Mueller element',[-1,0,1]);fig.text(2/178,82/163,'Output Stokes component',fontsize=7,rotation=90,va='center');fig.text(92/178,154/163,'Input Stokes component',fontsize=7,ha='center',color=GREY)
    return fig,e,[list(aa.flat)]


# Typography-only finishing. Keep numeric data, axis limits and physical plot sizes.
TRIMS={'01-concept':(12,72),'02-phase-library':(6,129),'03-spectra':(11,93),'04-field-comparison':(7,110),'05-imaging':(6,151),'06-mueller':(9,159)}
def paper_typography(fig,name):
    for ax in fig.axes:
        ax.xaxis.label.set_fontsize(7.5);ax.yaxis.label.set_fontsize(7.5)
        ax.xaxis.label.set_color('#111111');ax.yaxis.label.set_color('#111111')
        for title in [ax.title,ax._left_title,ax._right_title]:
            title.set_fontsize(7.5);title.set_fontweight('normal');title.set_color('#111111')
        ax.tick_params(labelsize=7)
        legend=ax.get_legend()
        if legend:
            for t in legend.get_texts():t.set_fontsize(7);t.set_color('#111111')
        for t in ax.texts:
            if t.get_text() in list('abcdefg'):
                t.set_fontsize(8);t.set_fontweight('bold');t.set_color('#111111')
            else:t.set_fontweight('normal');t.set_fontsize(7.5)
    if name=='03-spectra':
        fig.axes[1].set_yticks([0,.05,.10],labels=['0','0.05','0.10'])
    if name=='02-phase-library':
        # Explain the cut in the external caption; retain the necessary condition.
        fig.axes[2].set_title(r'$l = 201$ nm')
    if name=='05-imaging':
        for ax in fig.axes[3:6]:ax.set_title('ROI')
        fig.axes[-1].set_title(r'$y = 0.083$ μm',loc='left')
    old_h=fig._h;bottom,top=TRIMS[name];new_h=top-bottom
    for ax in fig.axes:
        pos=ax.get_position(original=True)
        ax.set_position([pos.x0,(pos.y0*old_h-bottom)/new_h,pos.width,pos.height*old_h/new_h])
    for t in fig.texts:
        x,y=t.get_position();t.set_position((x,(y*old_h-bottom)/new_h));t.set_fontweight('normal')
    fig.set_size_inches(178/25.4,new_h/25.4);fig._h=new_h


CASES=[('01-concept',concept),('02-phase-library',library),('03-spectra',spectra),('04-field-comparison',fields),('05-imaging',imaging),('06-mueller',mueller)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default=str(Path(__file__).resolve().parents[1]));args=p.parse_args();out=Path(args.out);(out/'figures').mkdir(parents=True,exist_ok=True)
    d=dataset();np.savez_compressed(out/'synthetic-data.npz',**d);original=digest(*(d[k] for k in sorted(d)))
    results=[]
    for name,render in CASES:
        signatures=[];geometry=None
        for after in [False,True]:
            rc=style() if after else {'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':7,'axes.titlesize':8,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'legend.fontsize':7,'axes.linewidth':.8,'lines.linewidth':1.2,'pdf.fonttype':42,'svg.fonttype':'none','savefig.bbox':None}
            with plt.rc_context(rc):
                fig,e,groups=render(d,after)
                if after:paper_typography(fig,name)
                fig.canvas.draw();e.ranges(fig);signatures.append(e.records)
                if after:
                    geometry=[]
                    for group in groups:
                        rects=np.array([[a.get_window_extent().width*72/fig.dpi,a.get_window_extent().height*72/fig.dpi] for a in group]);spreads=np.ptp(rects,axis=0);geometry.append({'width_spread_pt':float(spreads[0]),'height_spread_pt':float(spreads[1]),'pass':bool(np.max(spreads)<=1.5)})
                    assert all(g['pass'] for g in geometry),(name,geometry)
                stem=out/'figures'/(name+('-after' if after else '-before'))
                export_figure(fig,stem,formats=('png','pdf','svg') if after else ('png',),dpi=DPI);plt.close(fig)
        assert signatures[0]==signatures[1],('Evidence changed',name,signatures)
        checks=audit(out/'figures'/(name+'-after.pdf'),min_font=6,min_dpi=300,width_mm=178)
        status=checks['status']
        if name=='06-mueller' and len(checks['issues'])==8 and all(i['kind']=='small_text' and i['text'] in '0123' and abs(i['size_pt']-5.6)<.05 for i in checks['issues']):
            status='REVIEWED_SUBSCRIPT_EXCEPTION'
            checks['typographic_exception']='Eight 5.6 pt Stokes indices attached to 8 pt S labels. Visually reviewed at the final size; other small text is not exempt.'
        (out/'figures'/(name+'-audit.json')).write_text(json.dumps(checks,indent=2))
        results.append({'case':name,'identical_evidence':True,'checked_invariants':len(signatures[0]),'evidence_hashes':signatures[0],'geometry':geometry,'pdf_check':status})
        print(name,len(signatures[0]),checks['status'],flush=True)
    assert digest(*(d[k] for k in sorted(d)))==original
    (out/'verification.json').write_text(json.dumps({'provenance':'All numeric data are procedural synthetic examples, not an experiment or a full-wave simulation. These six exercises are not evidence for one physically validated device.','data_sha256':original,'data_mutated':False,'cases':results,'limitations':'PDF checks are finite; semantic diagram equality checks nodes and connections, not optical simulation. Visual review is still required.'},indent=2))
if __name__=='__main__':main()
