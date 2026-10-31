---
name: opticapaperfig
description: >-
  Restyle optics and photonics paper figures from existing code, data or images;
  improve composition, typography, color and visual narrative without changing
  scientific content. Also design core concept figures and graphical abstracts.
  Use for 光学顶刊风格、超表面论文美化、组图优化、核心示意图、图文摘要.
---

# Optica Paper Figure

**同一份工作、同一份数据、同一批图，做得更清楚、更好看。**
让物理想法成为视觉主角，让证据有秩序。色调、布局、字体、线条与叙事一起设计；不能只换配色，也不能只讲逻辑。

## 五条审美原则

1. **有主角，其余安静。** 最重要的结构、变化或结果获得最多面积与视觉对比；不要所有面板一样抢眼。装饰不能比现象更亮。
2. **关系成为构图。** 因果沿路径展开，对照用同尺度并置，层级用远近和大小，分组用留白。先决定眼睛怎么走，再摆图。
3. **颜色承担角色。** 基底与辅助元素克制，关键光束/通道突出；同一物理对象全篇同色。照片保留本色，强度、正负场、相位分别选色图。
4. **全文统一，逐图有别。** 字体、色彩含义和制图风格贯穿全文；每张大图按自己的论点选择构图，前后连成叙事。同类比较整齐重复，不同任务不硬套同一网格。
5. **细节说同一种语言。** 一套字族、字号层级、线重、箭头、视角与材质。图内短标注、图外完整图注；变量斜体、单位正体，不套展示页大标题与页脚。缩到最终尺寸仍清晰。

## 实际怎么改

先看现有图与代码；多张图先按[全文图序](references/paper-narrative.md)明确各自论点与衔接。绘图前读[字体、单位与图注](references/typography.md)和[视觉参数](references/design-system.md)，再从[精选原图](references/gallery.md)看2–4张匹配参考，提取“构图关系＋色彩角色＋细节语言”，不要照抄内容。光学定义有疑问时查[语义检查](references/optics-semantics.md)。
列明准备改的色调、布局、字体、线条、叙事五项，随后直接修改获授权的绘图层。优先用现有面板重排、调整面积与视觉编码；不为套模板新增数据或结果面板。只有用户要求补充分析或新图时，才做可追溯的派生展示。
沿用已有Python/MATLAB/R/矢量流程，保留before，按最终尺寸渲染after。先看缩略图主次，再逐项看字、轴、色条、比例尺、对齐与遮挡；不能只检查代码不看画面。[接入与验收](references/implementation-qa.md)含导出工具。

## 整篇文章最核心的图

把贡献写成“通过___，让___变成___”，再画**输入→关键物理作用→新能力**；选一个中心对象、一条主路径、一个记得住的结果。先用黑白轮廓讲通，再给必要的颜色与空间感。
正式图文摘要要独立可读、适合缩略图；Fig. 1可再接局部机理和必要证据。两者不等于把所有结果拼在一起。具体画法与真实案例见[核心图与图文摘要](references/hero-figure.md)。

## 科学内容不动

不因美化改变数据、归一化、筛样、平滑、拟合、坐标约定、误差或指标。对照保留共同色阶与基准；不编SEM、光斑或实验结果。只有图片时不能假装恢复精确数据。科学处理确需改变，先讲依据，依据不足先问。

## 按需参考

- [精选原图与审美拆解](references/gallery.md)：本地图片、原文入口、值得学与不照搬的部分；[图片署名](references/THIRD_PARTY.md)。
- [全文图序、统一性与差异性](references/paper-narrative.md)；[字体、单位与图注](references/typography.md)；[视觉参数](references/design-system.md)；[组图配方](references/panel-recipes.md)；[核心图](references/hero-figure.md)。
- [光学语义](references/optics-semantics.md)；[期刊规格](references/journal-profiles.md)；[代码与验收](references/implementation-qa.md)。
- [逐篇观察](references/evidence-atlas.md)、[来源清单](references/corpus.json)：实际看过的证据。已发表做法不是官方要求，建议数值不是截图测量。

交付修改后的源码、可编辑母版、预览与简短的前后说明。以真实画面判断是否进步；这不是Optica官方模板，也不承诺发表结果。
