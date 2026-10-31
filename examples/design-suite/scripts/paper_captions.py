"""External scientific captions for synthetic examples; not baked into figure artwork."""
from pathlib import Path
import fitz
from matplotlib import font_manager

CAPTIONS={
'01-concept':'Fig. 1. Schematic of polarization routing through an anisotropic meta-atom array. TE and TM inputs share an aperture and are directed to separate output channels. Blue and orange identify polarization channels, not wavelength. The diagram is illustrative and not to scale.',
'02-phase-library':'Fig. 2. Synthetic phase-response library. (a,b) Analytic TE and TM phase responses as functions of meta-atom width and length. Both maps use the same phase range. (c) Cross-sections at a length of 201 nm, indicated by dashed lines in (a,b). These are analytic examples, not electromagnetic simulation results.',
'03-spectra':'Fig. 3. Synthetic spectral response. (a) Channel efficiencies from an analytic model (lines) and synthetic samples (symbols). (b) Fraction of incident power routed to the opposite channel. (c) Deflection angles. Blue and orange denote TE and TM, respectively. All data are synthetic.',
'04-field-comparison':'Fig. 4. Comparison of synthetic target and model intensity distributions. Rows correspond to TE and TM; columns show the target, model and signed difference (model minus target). All intensity maps share one reference and range; they are not normalized separately. Both difference maps use the same symmetric scale.',
'05-imaging':'Fig. 5. Synthetic image-detail comparison. (a–c) A procedural resolution target and two precomputed blurred images. (d–f) The same 10 μm region of interest, marked in (a–c). (g) Intensity profiles at y = 0.083 μm. Crops, intensity ranges and sampling are identical across conditions; all images are synthetic.',
'06-mueller':'Fig. 6. Synthetic normalized Mueller matrix for a spatially varying ideal retarder. Rows and columns index output and input Stokes components, respectively. Every tile spans x, y = −1 to 1 in arbitrary spatial units and shares the same −1 to 1 colour scale. The 3 × 3 polarization block is an orthogonal Stokes-space rotation; these are analytic data, not measurements.'}

def make_previews(root):
    root=Path(root);out=root/'paper-previews';out.mkdir(exist_ok=True)
    for family in ['Times New Roman','Liberation Serif','DejaVu Serif']:
        try:font=font_manager.findfont(family,fallback_to_default=False);break
        except ValueError:continue
    for name,text in CAPTIONS.items():
        src=fitz.open(root/'figures'/(name+'-after.pdf'));w=src[0].rect.width;h=src[0].rect.height
        doc=fitz.open();page=doc.new_page(width=w,height=h+95)
        page.show_pdf_page(fitz.Rect(0,0,w,h),src,0)
        page.insert_font(fontname='CaptionBody',fontfile=str(font))
        result=page.insert_textbox(fitz.Rect(5,h+10,w-5,h+90),text,fontname='CaptionBody',fontsize=8.5,lineheight=1.2,color=(0,0,0))
        assert result>=0,(name,result)
        caption_bottom=max(s['bbox'][3] for b in page.get_text('dict')['blocks'] for line in b.get('lines',[]) for s in line['spans'] if s['bbox'][1]>h)
        page.set_cropbox(fitz.Rect(0,0,w,caption_bottom+9))
        doc.set_metadata({'title':name+' — synthetic figure and external caption','subject':'Synthetic educational example; not experimental data'})
        doc.save(out/(name+'.pdf'));page.get_pixmap(matrix=fitz.Matrix(2,2)).save(out/(name+'.png'));doc.close();src.close()
