# 接入代码与验收

用rg找绘图入口、保存调用、配置和数据：`savefig|imshow|pcolormesh|plot\(|exportgraphics|ggsave`。读适用AGENTS.md；沿用Python、MATLAB、R或现有矢量流程，不强制迁移。
把参数收拢到局部style/theme；用context避免污染。保留原始数据hash，必要时比较实际绘图输入数组；仅数据文件hash相同不能证明中间处理没变。
普通美化只需验证真实入口能运行、关键数值/单位/归一化不变、输出清晰，不必重跑重型仿真或编写镜像实现的测试。缺数据或依赖如实报告。

## 后端

- Python：rc_context、mm/25.4尺寸、GridSpec独立色条；PDF fonttype=42、SVG fonttype=none。
- MATLAB：centimeters设图尺寸，统一FontName/FontSize/LineWidth；tiledlayout；exportgraphics矢量PDF。实际检查图像和曲面是否栅格。
- R：复用现有ggplot/patchwork/base流程；theme和cairo_pdf；linewidth与Python pt不等同，按输出测量。不改统计变换。
- SVG/Illustrator/Inkscape：文字、比例尺独立层，保留viewBox和物理尺寸；链接照片随文件交付或嵌入。SEM无需矢量化。

## Python调用

依赖：Python 3、NumPy、Matplotlib；PDF检查另需PyMuPDF（`import fitz`）。先用项目环境；缺少时在项目虚拟环境安装，不覆盖已有全局依赖。脚本无需下载论文图。

将scripts加入导入路径，或复制所需小模块到获授权项目目录并注明来源。

```python
import matplotlib.pyplot as plt
from optica_style import style, figure_mm, export_figure, panel_label
with plt.rc_context(style('optica-draft')):
    fig, ax = figure_mm(85, 65)
    ax.plot(x, y, label='Measurement')  # x,y来自真实数据
    ax.set(xlabel='Wavelength (nm)', ylabel='Transmission')
    ax.legend()
    panel_label(ax, '(a)')
    export_figure(fig, 'outputs/figure1')
```

固定画布尺寸，不默认bbox_inches=tight改变最终宽高；先留边界。复杂布局可绕过helper。

## 三层验收

**科学层**：量/单位/光学约定、实测身份、显示变换、色条基准、比例尺校准、误差定义、反例；图注解释所有编码。
**几何层**：渲染后检查实际绘图区；同组宽高误差以1.5pt作本地起点。不同角色、跨行图、不同纵横比不盲目同组。目检文字/箭头/图例/色条碰撞、遮线、编号、页边。
**文件层**：PDF物理尺寸、字/字体、栅格有效dpi、页数，SVG可编辑，PNG清晰；不可只改dpi属性。自动检查不能证明科学正确或零遮挡。

```bash
python scripts/audit_pdf.py figure.pdf --min-font-pt 6 --min-image-dpi 300 --width-mm 178 --json-out figure.audit.json
```

返回0仅表示有限静态检查通过，1需处理，2无法审计。公式上下标有合理例外时人工记录，不全局降阈值掩盖小字。
`geometry_report(fig, groups)`仅检查显式组的渲染后宽高并返回数值；不自动验证共边、间距和碰撞，继续目检。
交付可编辑母版、PNG、投稿所需格式和运行命令，清楚说明实际检查；不把退出0写成“全部投稿规范通过”。
