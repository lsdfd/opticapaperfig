"""Read-only finite checks of figure PDFs; never claims scientific or collision validation."""
import argparse, json, sys
from pathlib import Path

def audit(path, min_font=6, min_dpi=300, width_mm=None):
    import fitz
    issues=[]; pages=[]
    with fitz.open(path) as doc:
        for idx,p in enumerate(doc):
            fonts=set(); sizes=[]; chars=0
            for b in p.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    for s in line['spans']:
                        if not s['text'].strip():continue
                        chars+=len(s['text']); fonts.add(s['font']);sizes.append(s['size'])
                        if s['size'] < min_font-.05:
                            issues.append({'page':idx+1,'kind':'small_text','size_pt':round(s['size'],2),'text':s['text'][:60]})
                        r=fitz.Rect(s['bbox'])
                        if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:
                            issues.append({'page':idx+1,'kind':'text_outside_page','text':s['text'][:60]})
            if chars==0:issues.append({'page':idx+1,'kind':'no_extractable_text','note':'Could be intentional image-only or outlined text; review source'})
            image_dpi=[]
            for im in p.get_image_info():
                # Transform vectors capture displayed axis lengths, including rotated images.
                a,b,c,d,e,f=im['transform'];w=(a*a+b*b)**.5;h=(c*c+d*d)**.5
                if not w or not h:continue
                dpi=min(im['width']*72/w,im['height']*72/h)
                image_dpi.append(round(dpi,1))
                # Tiny colormap strips and masks are still reported, not silently exempted.
                if dpi+1<min_dpi:issues.append({'page':idx+1,'kind':'low_image_dpi','effective_dpi':round(dpi,1),'pixels':[im['width'],im['height']]})
            wmm=p.rect.width*25.4/72
            if width_mm and abs(wmm-width_mm)>.3:issues.append({'page':idx+1,'kind':'wrong_width','actual_mm':wmm,'expected_mm':width_mm})
            pages.append({'page':idx+1,'width_mm':round(wmm,3),'height_mm':round(p.rect.height*25.4/72,3),
                          'fonts':sorted(fonts),'min_font_pt':round(min(sizes),2) if sizes else None,'image_dpi':image_dpi})
    return {'status':'REVIEW_REQUIRED' if issues else 'STATIC_CHECKS_PASS',
            'limitations':'Scientific meaning, hidden/clipped content, font editability in every editor, contrast and overlap are NOT automatically verified.',
            'pages':pages,'issues':issues}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf');p.add_argument('--min-font-pt',type=float,default=6)
    p.add_argument('--min-image-dpi',type=float,default=300);p.add_argument('--width-mm',type=float);p.add_argument('--json-out')
    a=p.parse_args()
    try:r=audit(a.pdf,a.min_font_pt,a.min_image_dpi,a.width_mm)
    except Exception as e:r={'status':'NOT_AUDITABLE','error':str(e)}
    output=json.dumps(r,ensure_ascii=False,indent=2)
    if a.json_out:Path(a.json_out).write_text(output)
    print(output)
    return {'STATIC_CHECKS_PASS':0,'REVIEW_REQUIRED':1,'NOT_AUDITABLE':2}[r['status']]

if __name__=='__main__':sys.exit(main())
