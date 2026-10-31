"""Original synthetic optics example. No experimental evidence or third-party artwork."""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from optica_style import style, field_scale, panel_label, export_figure, geometry_report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out-dir',default='demo-output');a=p.parse_args()
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    # Sample centres match imshow pixel edges at -3 and +3 micrometres.
    x=(np.arange(181)-90)*6/181; X,Y=np.meshgrid(x,x)
    target=np.exp(-2*(X*X+Y*Y)); variant=.91*np.exp(-2*((X-.15)**2+(Y+.07)**2))
    residual=variant-target;wave=np.linspace(450,750,101)
    te=.6+.2*np.exp(-((wave-570)/65)**2);tm=.53+.22*np.exp(-((wave-615)/70)**2)
    phase=np.arctan2(Y,X);masked=np.ma.masked_where(X*X+Y*Y<.12**2,phase)
    limit=np.ceil(np.max(np.abs(residual))*100)/100
    def plotted_digest(fig):
        h=hashlib.sha256()
        for ax in fig.axes:
            for im in ax.images:
                arr=np.ma.asarray(im.get_array());h.update(arr.filled(np.nan).tobytes());h.update(np.ma.getmaskarray(arr).tobytes())
                h.update(np.asarray(im.get_clim()+tuple(im.get_extent()),dtype=float).tobytes())
            for line in ax.lines:
                if line.get_label() in ('Target','Perturbed','TE','TM'):
                    h.update(np.asarray(line.get_xdata()).tobytes());h.update(np.asarray(line.get_ydata()).tobytes())
        return h.hexdigest()
    digest=lambda:hashlib.sha256(b''.join(v.tobytes() for v in [x,target,variant,residual,wave,te,tm,phase])).hexdigest()
    before_hash=digest()
    with plt.rc_context({'font.size':8}):
        fig,axs=plt.subplots(2,3,figsize=(178/25.4,130/25.4))
        for ax,z,title,lo,hi in zip(axs[0],[target,variant,residual],['Target intensity','Perturbed intensity','Intensity difference'],[0,0,-limit],[1,1,limit]):
            im=ax.imshow(z,extent=[-3,3,-3,3],origin='lower',vmin=lo,vmax=hi,cmap='jet',interpolation='nearest')
            fig.colorbar(im,ax=ax);ax.set_title(title);ax.set(xlabel='x (μm)',ylabel='y (μm)')
        axs[1,0].plot(x,target[len(x)//2],label='Target');axs[1,0].plot(x,variant[len(x)//2],label='Perturbed')
        axs[1,0].legend();axs[1,0].grid();axs[1,0].set(xlabel='x (μm)',ylabel='Relative intensity',title='Profile at y = 0',xlim=(-3,3),ylim=(0,1.1))
        axs[1,1].plot(wave,te,label='TE');axs[1,1].plot(wave,tm,label='TM')
        axs[1,1].legend();axs[1,1].grid();axs[1,1].set(xlabel='Wavelength (nm)',ylabel='Efficiency',title='Spectral response',xlim=(450,750),ylim=(0,1))
        im=axs[1,2].imshow(masked,extent=[-3,3,-3,3],origin='lower',cmap='jet',vmin=-np.pi,vmax=np.pi,interpolation='nearest')
        cb=fig.colorbar(im,ax=axs[1,2]);cb.set_ticks([-np.pi,0,np.pi],labels=['−π','0','π']);axs[1,2].set(xlabel='x (μm)',ylabel='y (μm)',title='Phase (rad)')
        for i,ax in enumerate(axs.flat):ax.text(0,1.15,f'({chr(97+i)})',transform=ax.transAxes)
        fig.suptitle('SYNTHETIC OPTICS / STYLE DEMONSTRATION',fontsize=9)
        fig.text(.08,.015,'Independent phase example; centre masked. Shared intensity reference.',fontsize=6.5)
        fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(out/'before.png',dpi=450)
        before_plotted_hash=plotted_digest(fig);plt.close(fig)
    with plt.rc_context(style()):
        # Explicit millimetre rectangles keep comparable data areas identical.
        fig=plt.figure(figsize=(178/25.4,130/25.4))
        def axes_mm(left,bottom,width,height):
            return fig.add_axes([left/178,bottom/130,width/178,height/130])
        axes=[]
        maps=[(target,'Target intensity','intensity',0,1),
              (variant,'Perturbed intensity','intensity',0,1),
              (residual,'Intensity difference','signed',-limit,limit)]
        for i,(z,title,kind,lo,hi) in enumerate(maps):
            left=14+58*i
            ax=axes_mm(left,74,36,36);cax=axes_mm(left+37,74,1.8,36)
            cmap,norm=field_scale(kind,vmin=lo,vmax=hi)
            im=ax.imshow(z,origin='lower',extent=[-3,3,-3,3],cmap=cmap,norm=norm,interpolation='nearest')
            ax.set(xlabel='x (μm)',title=title,xticks=[-3,0,3],yticks=[-3,0,3])
            if i==0:ax.set_ylabel('y (μm)')
            if i<2:ax.axhline(0,color='white',lw=.6,ls='--')
            cb=fig.colorbar(im,cax=cax);cb.set_ticks([lo,(lo+hi)/2,hi])
            cb.ax.tick_params(length=2,pad=2,labelsize=6.5)
            axes.append(ax);panel_label(ax,f'({chr(97+i)})',x=-.22,y=1.08)
        ax=axes_mm(14,17,40,36)
        ax.plot(x,target[len(x)//2],label='Target');ax.plot(x,variant[len(x)//2],'--',label='Perturbed')
        ax.set(xlabel='x (μm)',ylabel='Relative intensity',title='Profile at y = 0',xlim=(-3,3),ylim=(0,1.1),xticks=[-3,0,3])
        ax.legend(loc='upper right',fontsize=6.5);panel_label(ax,'(d)',x=-.20,y=1.08)
        ax=axes_mm(72,17,40,36)
        ax.plot(wave,te,label='TE');ax.plot(wave,tm,'--',label='TM')
        ax.set(xlabel='Wavelength (nm)',ylabel='Efficiency',title='Spectral response',ylim=(0,1),xlim=(450,750),xticks=[450,600,750])
        ax.legend(fontsize=6.5,loc='lower right');panel_label(ax,'(e)',x=-.20,y=1.08)
        ax=axes_mm(130,17,36,36);cax=axes_mm(167,17,1.8,36)
        cmap,norm=field_scale('phase')
        im=ax.imshow(masked,extent=[-3,3,-3,3],origin='lower',cmap=cmap,norm=norm,interpolation='nearest')
        ax.set(xlabel='x (μm)',title='Phase (rad)',xticks=[-3,0,3],yticks=[-3,0,3])
        cb=fig.colorbar(im,cax=cax);cb.set_ticks([-np.pi,0,np.pi],labels=['−π','0','π'])
        cb.ax.tick_params(length=2,pad=2,labelsize=6.5);panel_label(ax,'(f)',x=-.22,y=1.08)
        fig.text(14/178,125/130,'SYNTHETIC OPTICS / STYLE DEMONSTRATION',fontsize=9,fontweight='bold')
        fig.text(14/178,120/130,'Analytic arrays only · shared intensity reference · no experimental claims',fontsize=7,color='#555555')
        fig.text(14/178,3/130,'(f): independent phase example; centre masked. Spatial axes: μm.',fontsize=6.5)
        geo=geometry_report(fig,{'intensity_and_residual':axes});(out/'geometry.json').write_text(json.dumps(geo,indent=2))
        export_figure(fig,out/'after');after_plotted_hash=plotted_digest(fig);plt.close(fig)
    assert before_plotted_hash==after_plotted_hash,'Plotted values, masks, ranges or extents changed'
    assert digest()==before_hash,'Plotting mutated data'
    np.savez(out/'synthetic_data.npz',x=x,target=target,variant=variant,residual=residual,wavelength=wave,te=te,tm=tm,phase=phase,phase_mask=np.ma.getmaskarray(masked))
    (out/'provenance.json').write_text(json.dumps({'data_kind':'synthetic analytic example; NOT research evidence','array_sha256_before':before_hash,'array_sha256_after':digest(),'geometry_pass':geo['pass'],'same_six_panels':True,'plotted_sha256_before':before_plotted_hash,'plotted_sha256_after':after_plotted_hash},indent=2))
    print(out.resolve())

if __name__=='__main__':main()
