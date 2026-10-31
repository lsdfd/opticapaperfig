# 原图观察图谱

核查日期：2026-10-31。亲自查看16篇原始研究的51张编号图（每张含若干子面板），外加1篇News & Views的1张图，后者不计入研究样本。
期刊分布：Optica 5篇、Nature Photonics 5篇、Light: Science & Applications 4篇、Nature Communications 1篇、Nature 1篇。

这是有目的的设计样本，不是期刊风格的统计调查；主要围绕超表面及相关光学，未覆盖所有光学子领域。Optica包含较早经典研究，其他样本主要来自2024–2026。
已查看原图像素或本地渲染PDF，不是只读摘要。若页面只提供685像素图，足以观察布局与编码，但不用于断言精确字体或线宽；精确参数表是本skill建议。
完整逐图URL、PDF页号和查看方式见[corpus.json](corpus.json)。不把未能显示的截图或未下载成功的PDF算作已看图。
新增[精选图库](gallery.md)：附11张已核查CC BY 4.0许可的样本原图，另附新查看的3篇论文的正式摘要图，逐图署名。其余图保留来源入口；不同图片按各自许可使用，不能视为我们的研究结果。

新增摘要图的3篇论文单独记录在corpus.json的extra_graphical_abstracts，不并入上面的51张编号图；截至本版，共查看19篇研究论文的51张编号图和3张摘要图，外加1张评论图。

## 从样本归纳的规则及边界

| 归纳 | 证据锚点 | 不能过度推论 |
|---|---|---|
| 原理/结构与定量证据分工 | N01 F2；N04 F1；O09 F6 | 不要求每张图都有3D渲染 |
| 比较矩阵保持行列语义 | N12 F4；O02 F4/F5；O08 F5 | 不盲目把所有量用同一色条 |
| 颜色贯穿同一物理角色 | N09 F8；O08 F1；O10 F2 | 不是固定全刊蓝橙或强制去RGB |
| 示意图可以简洁矢量 | N09 F1/F2；O08 F1 | 重3D不是发表必要条件 |
| SEM与功能结果形成证据链 | N04 F1/F2；O09 F6 | SEM不能由AI生成替代 |
| 光斑搭配剖面/指标 | O08 F5；O09 F6；N10 F7 | 仅光斑好看不能证明效率 |
| 黑底用于特定光学图像 | N01 F1；N06 F1；O10 F1 | 不是整篇数据图要改深色主题 |
| 失败/低光条件也要展示 | O10 F11；N06 F5 | 不挑选最漂亮样本作为全部证据 |

原图也有彩虹色、红绿区分、过密框线和小字。新图优先改善这些问题，而不是因已发表就照搬。

## 逐篇观察
### N01 · Nature Photonics · 2024

[360° structured light with learned metasurfaces](https://www.nature.com/articles/s41566-024-01450-x)

查看：Fig. 1, Fig. 2, Fig. 4。主题：3D结构光、学习型超表面。

**直接看到**：F1黑背景表现投射场景；F2横向优化流程带前后向箭头，下方单元、光谱、SEM、实景；F4照片/光路/定量曲线与多场景成像按行组装。

**可迁移判断**：黑底概念图与白底证据图可共存；图面要区分空间结构和优化流。

### N02 · Nature Photonics · 2024

[Metasurface-enabled single-shot and complete Mueller matrix imaging](https://www.nature.com/articles/s41566-024-01426-x)

查看：Fig. 1, Fig. 2, Fig. 5。主题：偏振、Mueller矩阵成像。

**直接看到**：F1用绿光、浅蓝器件、粉色检测区解释角色；F2以矩阵空间和算子排布组织密集内容；F5照片、测量拼图、Stokes条带和4×4矩阵分组。

**可迁移判断**：矩阵按数学索引排布；颜色服务概念角色。F5带符号矩阵并非都采用零中心发散色，这不作为推荐。

### N03 · Nature Photonics · 2025

[Expanding momentum bandgaps in photonic time crystals through resonances](https://www.nature.com/articles/s41566-024-01563-3)

查看：Fig. 1, Fig. 2, Fig. 5。主题：时间晶体、色散与带隙。

**直接看到**：F1的2×2曲线共享坐标，灰带与箭头标带隙；F2两列机制对比；F5左机制、右热图/局部/散点，嵌套分组。

**可迁移判断**：物理区域阴影有解释作用；双轴和红绿组合需检查歧义，不照搬。

### N04 · Nature Photonics · 2025

[Plasmonic biosensor enabled by resonant quantum tunnelling](https://www.nature.com/articles/s41566-025-01708-y)

查看：Fig. 1, Fig. 2, Fig. 4。主题：等离激元传感、多尺度表征。

**直接看到**：F1上方机制，下方照片到SEM/TEM逐级放大，框线串联；F2发光图与SEM同列对应；F4左右两类分析，ROI色与谱线对应，最后给误差和检出限。

**可迁移判断**：显微证据串联尺度；把定量校准接在代表图像之后，保留噪声。

### N05 · Nature Photonics · 2026

[Generation of continuous-wave 1–11 THz radiation with intersubband polaritonic metasurfaces](https://www.nature.com/articles/s41566-026-01889-0)

查看：Fig. 1, Fig. 2, Fig. 4。主题：太赫兹产生、器件与光谱。

**直接看到**：F1单幅光路渲染；F2器件、能带、响应横排；F4为2×3实验证据，包含SEM、光谱、功率关系、效率、光斑和吸收谱。

**可迁移判断**：不同角色可以同组但不强行共色条；多曲线用线型并记录倍率。

### N06 · Light: Science & Applications · 2024

[Ultra-robust informational metasurfaces based on spatial coherence structures engineering](https://www.nature.com/articles/s41377-024-01485-3)

查看：Fig. 1, Fig. 2, Fig. 5。主题：相干结构、鲁棒全息。

**直接看到**：F1黑底机制表达障碍前后光场；F2转换流程后接强度/相位图；F5按遮挡条件排图，图标标明遮挡范围。

**可迁移判断**：按条件构成证据矩阵；彩虹相位图可改循环色，不把发表样式当最优。

### N07 · Light: Science & Applications · 2024

[Broadband infrared imaging governed by guided-mode resonance in dielectric metasurfaces](https://www.nature.com/articles/s41377-024-01535-w)

查看：Fig. 1, Fig. 2, Fig. 8。主题：非线性红外成像、导模共振。

**直接看到**：F1结构及SEM在左、能带在右；F2宽谱上方，分解谱与对应场图下方；F8明场照片、逐层图像和层位曲线对应。

**可迁移判断**：色条必须区分不同场分量；密集谱线用线型；层深/尺度标签必须明确。

### N09 · Light: Science & Applications · 2024

[Shape optimization for high efficiency metasurfaces: theory and implementation](https://www.nature.com/articles/s41377-024-01629-5)

查看：Fig. 1, Fig. 2, Fig. 8。主题：形状优化、偏振效率。

**直接看到**：F1三列黑白结构对比；F2紧凑闭环优化流程；F8仿真、实验、提升三列，蓝橙表示TE/TM，实虚线区分方案/来源。

**可迁移判断**：一张图只用少量颜色也能承载多维语义；形状示意无需重3D。

### N10 · Light: Science & Applications · 2026

[Minimalist optical system for achromatic imaging within extended field of view based on monolithic integrated meta-axicon cluster](https://www.nature.com/articles/s41377-026-02272-y)

查看：Fig. 1, Fig. 2, Fig. 7。主题：消色差成像、轴锥与视场。

**直接看到**：F1 RGB射线与传播图、响应曲线；F2角度曲线紧邻通道光斑；F7同位置ROI和剖面形成对照，方法按上下排列。

**可迁移判断**：物理RGB应保留，并以通道标签辅助；ROI-剖面必须对应。

### N11 · Nature Communications · 2024

[Metasurface-enabled broadband multidimensional photodetectors](https://www.nature.com/articles/s41467-024-52632-8)

查看：Fig. 1, Fig. 2, Fig. 5。主题：多维探测、偏振与机器学习。

**直接看到**：F1按概念层、器件层、学习流程分三条带；F2器件、流线场、参数热图和拟合；F5响应曲线与网络、混淆矩阵、区间预测分组。

**可迁移判断**：模块结构与定量输出分工；密度较高，缩图时需警惕小字及图例。

### N12 · Nature · 2024

[Full-colour 3D holographic augmented-reality displays with metasurface waveguides](https://www.nature.com/articles/s41586-024-07386-0)

查看：Fig. 1, Fig. 2, Fig. 4。主题：全彩AR、超表面波导。

**直接看到**：F1传统/新结构并列并给实体照片；F2光路-场图-结构/SEM-效率；F4行=方法、列=场景，统一ROI框，另给不同焦距结果。

**可迁移判断**：等条件矩阵比随意拼照片更利于判断方法差异。

### O02 · Optica · 2025

[Structuring light waves in 3D volumes with high precision using communication mode optics](https://pure.tue.nl/ws/portalfiles/portal/367405705/optica-12-9-1502.pdf)

查看：Fig. 1, Fig. 3, Fig. 4, Fig. 5。主题：三维光场、通信模态。

**直接看到**：F1分格定义几何与算子；F3目标、系数、场、编码和光路按证据链排布；F4按Target/Simulated/Measured列对比；F5多层结果保持固定行列。

**可迁移判断**：原版包含较重分隔线，可学语义对齐而不照搬边框。图注明确模拟/实测空间比例不一致，应保留这一限制。

### O07 · Optica · 2018

[Computational complex optical field imaging using a designed metasurface diffuser](https://authors.library.caltech.edu/records/bhh5g-xxv45)

查看：Fig. 1, Fig. 2, Fig. 3, Fig. 6。主题：计算复场成像。

**直接看到**：F1光学到计算到幅度/相位；F2侧视/顶视/单元、映射、实物/SEM；F3按目标/无迭代/有迭代分组；F6计算与传统成像左右对照。

**可迁移判断**：幅度与相位有独立色条；旧式彩色虚线框可换为留白与简短组标题。

### O08 · Optica · 2017

[Controlling the sign of chromatic dispersion in diffractive optics with dielectric metasurfaces](https://authors.library.caltech.edu/records/nnf8v-92988)

查看：Fig. 1, Fig. 2, Fig. 5。主题：色散、消色差聚焦。

**直接看到**：F1五列色散机制、两行元件类型；F2机制与定量预测组合；F5仿真/实测曲线在上，传播图/焦斑/线剖面在下，以波长匹配行。

**可迁移判断**：二维对比矩阵能解释多种色散；小inset和密集标注不能当固定模板。

### O09 · Optica · 2020

[Multifunctional 2.5D metastructures enabled by adjoint optimization](https://authors.library.caltech.edu/records/jxqdh-gnr74)

查看：Fig. 1, Fig. 2, Fig. 6。主题：多层超表面、伴随优化。

**直接看到**：F1少量射线与局部层结构；F2单元、两张参数映射和两层版图；F6 SEM逐级放大、实验光路、正交焦场和剖面完整闭环。

**可迁移判断**：材料层、波长和测量/理想曲线分别编码；伪彩SEM需注明。

### O10 · Optica · 2020

[Ultralow-light-level color image reconstruction using high-efficiency plasmonic metasurface mosaic filters](https://eprints.gla.ac.uk/216252/)

查看：Fig. 1, Fig. 2, Fig. 11, Fig. 12。主题：低光成像、RGB滤波。

**直接看到**：F1黑底功能渲染与白底单元剖面结合；F2 RGB SEM与对应谱线按列；F11固定目标按曝光排序并给每像素光子数；F12多目标应用。

**可迁移判断**：把弱光退化和采集条件同时展示，比仅挑清晰效果图更有信息。

## 线索来源与排除项

搜索了“超表面学习之路”，找到大学网站转载的“超构表面学习之路”文章。只将其作为发现论文的线索，规则来自原论文和官方指南；不声称完整浏览该公众号。
N08为News & Views，仅补充示意图观察。部分Optica论文仅取得文本或遇到访问限制，均未计入51张图。
正式期刊要求与自己的推荐值见[journal-profiles.md](journal-profiles.md)，不要从此图谱推导未核查的投稿硬规则。
