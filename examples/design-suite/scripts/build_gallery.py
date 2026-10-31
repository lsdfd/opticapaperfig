from pathlib import Path
import json,html
from PIL import Image,ImageDraw,ImageFont
import fitz
from matplotlib import font_manager
from paper_captions import CAPTIONS, make_previews
ROOT=Path(__file__).resolve().parents[1]
CASES=[
('01-concept','核心机制图','输入、器件、输出：把同一组要素变成一个物理场景。',
 '从方框连接改为共享孔径的斜视结构；输入与两个输出沿清楚的方向展开。蓝/橙仅表示TE/TM通道，器件本身退为低饱和材料色。',
 '保留输入、30个各向异性单元、两个输出及全部连接关系。图形位置与视角改变；这是示意图，不是电磁仿真。'),
('02-phase-library','参数设计与相位','两张同尺度响应图，接一条共同条件下的横截面。',
 '把并排挤压的三个面板改成上方双图、下方宽剖面；相位采用完整周期的循环色图，共用色条，剖面线在主图中可定位。',
 '相位来自解析函数；图上截面为Length = 201 nm。所有取样值、坐标范围、色阶范围与剖面数组均保持不变。'),
('03-spectra','光谱与通道分离','主性能占大面积，泄漏和偏转角在侧面补充。',
 '用不等宽布局明确主次；蓝/橙贯穿三个面板，实线/虚线和圆点/方点提供冗余编码。去掉重网格与图例边框，给主曲线留出面积。',
 '曲线为解析模型，散点为固定随机种子的合成采样；不是实测。效率、泄漏与角度显示范围前后一致。'),
('04-field-comparison','光场公平对照','行固定通道，列固定目标、模型与差值。',
 '六个图块保留相同物理尺寸；非负强度用顺序色，正负差值用零中心发散色。两根共享色条明确比较基准，重复标注减到必要程度。',
 '二维高斯目标与轻微偏移模型均为合成数组；无逐图归一化。残差范围覆盖全部值，坐标方向与像素范围不变。'),
('05-imaging','成像、局部细节与剖面','整图→相同ROI→同一取样行，让图像观察落到曲线。',
 '将七个散排面板组织成三列对应链，底部剖面横贯整行。图像保留灰度，蓝色框只定位ROI；图例移出曲线区域。',
 '分辨率靶为程序生成，Blur A/B是已生成的两种模糊图。优化阶段不重做滤波或去噪；ROI和显示范围相同，剖面位于y = 0.083 μm。'),
('06-mueller','偏振矩阵','数学索引就是排版：4×4关系一眼可读。',
 '去掉16根重复色条，保留一个固定范围的零中心色条；行列标示输入/输出Stokes分量，只在外边显示坐标。重复结构服务比较，不为变化强行换版式。',
 '使用解析的归一化无损延迟器Mueller矩阵：M00 = 1，3×3子块为Stokes空间旋转，已验证正交性。不是偏振测量数据。')]

def build():
    make_previews(ROOT)
    spec=json.loads((ROOT/'verification.json').read_text())
    assert all(c['identical_evidence'] and c['pdf_check'] in ('STATIC_CHECKS_PASS','REVIEWED_SUBSCRIPT_EXCEPTION') for c in spec['cases'])
    # Overview of original generated plots; thumbnails only, no data-image editing.
    canvas=Image.new('RGB',(1640,1670),'#edf1f4');draw=ImageDraw.Draw(canvas)
    font=font_manager.findfont('DejaVu Sans')
    titlefont=ImageFont.truetype(font,35);smallfont=ImageFont.truetype(font,19)
    draw.text((50,30),'Optics figure studies',fill='#24313c',font=titlefont)
    draw.text((50,82),'Synthetic data · revised typography',fill='#65727c',font=smallfont)
    for i,(name,title,_,__,___) in enumerate(CASES):
        x=40+(i%2)*790;y=130+(i//2)*505;draw.rounded_rectangle((x,y,x+770,y+485),radius=3,fill='white')
        im=Image.open(ROOT/'figures'/(name+'-after.png')).convert('RGB');im.thumbnail((742,450));canvas.paste(im,(x+(770-im.width)//2,y+(485-im.height)//2))
    canvas.save(ROOT/'overview.png')
    # Six-page comparison PDF; right hand figures retain their vector content.
    doc=fitz.open();mm=72/25.4
    for name,title,purpose,changes,bound in CASES:
        p=doc.new_page(width=400*mm,height=214*mm)
        p.insert_text((10*mm,11*mm),name.replace('-',' ').upper(),fontsize=15,color=(.14,.19,.24))
        p.insert_text((10*mm,23*mm),'BEFORE / baseline plotting',fontsize=10,color=(.40,.44,.48))
        p.insert_text((210*mm,23*mm),'AFTER / opticapaperfig',fontsize=10,color=(.14,.46,.61))
        p.insert_image(fitz.Rect(10*mm,30*mm,190*mm,199*mm),filename=str(ROOT/'figures'/(name+'-before.png')),keep_proportion=True)
        src=fitz.open(ROOT/'figures'/(name+'-after.pdf'));p.show_pdf_page(fitz.Rect(210*mm,30*mm,390*mm,199*mm),src,0);src.close()
        p.insert_text((10*mm,207*mm),'SYNTHETIC EXAMPLES. Numeric arrays, masks, scales and coordinate limits are unchanged. Diagram connectivity is unchanged.',fontsize=8,color=(.4,.44,.48))
    doc.save(ROOT/'comparisons.pdf',garbage=4,deflate=True);doc.close()
    cards=[];md=[]
    for i,(name,title,purpose,changes,bound) in enumerate(CASES,1):
        e=html.escape
        cards.append(f'''<section id="{name}"><div class="case-heading"><div><p class="number">EXAMPLE {i:02}</p><h2>{e(title)}</h2></div><span class="verified">数据与含义保持一致</span></div><p class="purpose">{e(purpose)}</p><div class="controls" role="group" aria-label="{e(title)}前后比较"><button data-mode="before" aria-pressed="false">优化前</button><button class="active" data-mode="after" aria-pressed="true">优化后</button><button data-mode="both" aria-pressed="false">并排比较</button></div><div class="views mode-after"><figure class="before"><figcaption>基础绘图</figcaption><a href="figures/{name}-before.png" target="_blank"><img loading="lazy" src="figures/{name}-before.png" alt="{e(title)}优化前"></a></figure><figure class="after"><figcaption>opticapaperfig 优化</figcaption><a href="figures/{name}-after.png" target="_blank"><img loading="lazy" src="figures/{name}-after.png" alt="{e(title)}优化后"></a></figure></div><p class="paper-caption">{e(CAPTIONS[name])}</p><p><b>改了什么：</b>{e(changes)}</p><details><summary>数据与比较说明</summary><p>{e(bound)}</p></details><p class="downloads"><a href="paper-previews/{name}.pdf">图＋图注预览</a><a href="figures/{name}-after.pdf">矢量 PDF</a><a href="figures/{name}-after.svg">可编辑 SVG</a><a href="figures/{name}-after.png">高清 PNG</a></p></section>''')
        md.append(f'## {i:02} · {title}\n\n{purpose}\n\n| 基础绘图 | opticapaperfig优化 |\n|---|---|\n| ![优化前](figures/{name}-before.png) | ![优化后](figures/{name}-after.png) |\n\n{changes}\n\n{CAPTIONS[name]}\n\n{bound}\n\n[PDF](figures/{name}-after.pdf) · [SVG](figures/{name}-after.svg) · [PNG](figures/{name}-after.png)\n')
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#eef2f4;color:#24313c;font:16px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1280px;margin:auto;padding:40px 32px}header{padding:20px 0 34px}h1{font-size:40px;line-height:1.3;letter-spacing:-1px;margin:10px 0 20px}h2{font-size:25px;margin:0}.eyebrow,.number{font-size:12px;font-weight:600;letter-spacing:1.5px;color:#24769b}.number{margin:0}.intro{max-width:840px;font-size:18px}.meta{font-size:14px;color:#6c7681}.links,.downloads{display:flex;gap:22px;flex-wrap:wrap}a{color:#24769b;text-underline-offset:4px}nav{display:flex;gap:10px 25px;flex-wrap:wrap;border-top:1px solid #cbd5dc;border-bottom:1px solid #cbd5dc;padding:16px 0}nav a{text-decoration:none;font-size:14px}section{background:white;margin:28px 0;padding:28px 34px;border:1px solid #dfe5e8}.case-heading{display:flex;align-items:center;justify-content:space-between;gap:20px}.verified{font-size:12px;color:#64747b}.paper-caption{font-family:"Times New Roman",Times,serif;font-size:17px;line-height:1.5;color:#111}.purpose{font-size:17px;color:#4c5c66}.controls{display:flex;gap:4px;margin:20px 0;padding:4px;border:1px solid #d7dfe4;width:max-content;border-radius:6px}button{border:0;background:transparent;padding:8px 18px;color:#536570;cursor:pointer;font:inherit;font-size:14px;border-radius:3px}button.active{background:#24313c;color:white}.views{min-height:240px}figure{margin:0}figcaption{color:#76828a;font-size:12px;padding:3px 0;text-align:center}.views img{display:block;width:100%;height:auto}.mode-after .before,.mode-before .after{display:none}.mode-both{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}details{color:#5c6a74;font-size:14px}summary{cursor:pointer}.downloads{font-size:14px;margin-bottom:0}.overview{width:100%;height:auto}footer{color:#687681;font-size:14px;padding:24px 0}code{font-family:ui-monospace,monospace;font-size:13px;background:#e6ebee;padding:3px 5px}@media(max-width:700px){main{padding:15px}h1{font-size:29px}section{padding:20px 14px}.case-heading{display:block}.verified{display:block;margin-top:10px}.mode-both{grid-template-columns:1fr}.controls button{padding:7px 14px}}'''
    nav=''.join(f'<a href="#{name}">{i:02} {title}</a>' for i,(name,title,*_) in enumerate(CASES,1))
    js="""document.querySelectorAll('.controls').forEach(group=>{group.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{const section=group.closest('section');section.querySelector('.views').className='views mode-'+button.dataset.mode;group.querySelectorAll('button').forEach(b=>{const on=b===button;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});}));});"""
    intro='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Optica Paper Figure · 六组前后对照</title><style>'''+css+'''</style><main><header><p class="eyebrow">OPTICAPAPERFIG / DESIGN STUDIES</p><h1>同一份内容，六种更清楚的表达。</h1><p class="intro">字体、色彩角色和线条保持统一；核心概念、设计、性能、光场、成像与偏振矩阵各自采用适合论点的版式。点击按钮切换前后，或并排比较；点击图片可看大图。</p><p class="meta">全部为明确标注的合成练习，优化前是同一脚本的基础绘图版本。不是实验结果，也不是某个真实器件的整套物理验证。前后不改变数值、掩膜、坐标范围或归一化；核心示意图保留相同对象与连接关系。</p><p class="links"><a href="comparisons.pdf">下载六页对照 PDF</a><a href="overview.png">查看全套缩略图</a><a href="scripts/render_suite.py">绘图源码</a><a href="verification.json">一致性检查</a><a href="https://github.com/lsdfd/opticapaperfig">公开 GitHub 仓库</a></p></header><nav>'''+nav+'</nav>'
    foot='''<footer><p>前后共6组；5组数值图逐项核对实际绘图数组、掩膜、色阶、像素范围及坐标轴范围；1组示意图核对对象与连接关系。PDF字体与尺寸已检查；Stokes下标的5.6 pt字号已单独目检，可比图块尺寸检查通过，另已实际查看画面。自动检查不等于科学有效性认证。</p><p>复现：<code>python scripts/render_suite.py</code>，再运行 <code>python scripts/build_gallery.py</code>。这些版式是示例，不要求未来所有论文照搬。</p></footer></main><script>'''+js+'</script></html>'
    (ROOT/'index.html').write_text(intro+''.join(cards)+foot)
    (ROOT/'README.md').write_text('# 六组同数据前后对照\n\n统一视觉语言，按不同论点改变版式。全部是合成练习；基础版和优化版使用相同数据、面板与科学含义。它们不构成真实器件的完整验证。图内排版已修订：取消展示页标题和页脚，数学变量与单位分开处理，完整图注置于图外。\n\n![六组优化结果](overview.png)\n\n[下载六页对照PDF](comparisons.pdf) · [交互式示例册HTML](index.html)（下载后本地打开） · [一致性检查](verification.json)\n\n'+ '\n'.join(md)+'\n## 复现\n\nPython 3；依赖见[requirements.txt](requirements.txt)。\n\n```bash\npython scripts/render_suite.py\npython scripts/build_gallery.py\n```\n\n修改已有工作时直接复用数据与绘图入口，不需要套用这些合成模型。\n')
    print('Gallery, overview, and six-page comparison PDF created.')
if __name__=='__main__':build()
