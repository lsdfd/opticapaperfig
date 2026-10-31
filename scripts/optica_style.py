"""Optics manuscript drawing helpers; defaults are recommendations, not journal rules."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib import font_manager
from cycler import cycler

COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#666666']

def style(profile='optica-draft', font=None):
    if profile not in ('optica-draft', 'nature-production'):
        raise ValueError('Unknown profile')
    if font is None:
        for candidate in ('Arial', 'Helvetica', 'DejaVu Sans'):
            try:
                font_manager.findfont(candidate, fallback_to_default=False)
                font = candidate
                break
            except ValueError:
                continue
    else:
        font_manager.findfont(font, fallback_to_default=False)
    nature = profile == 'nature-production'
    return {
        'font.family': 'sans-serif', 'font.sans-serif': [font],
        'font.size': 7 if nature else 8,
        'axes.labelsize': 7 if nature else 8,
        'axes.titlesize': 7 if nature else 8,
        'xtick.labelsize': 6 if nature else 7,
        'ytick.labelsize': 6 if nature else 7,
        'legend.fontsize': 6 if nature else 7,
        'axes.linewidth': .7, 'lines.linewidth': 1.15,
        'lines.markersize': 3.5, 'xtick.major.width': .7,
        'ytick.major.width': .7, 'xtick.major.size': 3,
        'ytick.major.size': 3, 'xtick.direction': 'out',
        'ytick.direction': 'out', 'axes.grid': False,
        'legend.frameon': False, 'axes.prop_cycle': cycler(color=COLORS),
        'text.color': '#222222', 'axes.labelcolor': '#222222',
        'figure.facecolor': 'white', 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'mathtext.fontset': 'dejavusans', 'savefig.bbox': None,
    }

def figure_mm(width=85, height=65, **kwargs):
    if width <= 0 or height <= 0:
        raise ValueError('Physical dimensions must be positive')
    kwargs.setdefault('layout', 'constrained')
    return plt.subplots(figsize=(width / 25.4, height / 25.4), **kwargs)

def panel_label(ax, label, profile='optica-draft', x=-.18, y=1.04):
    return ax.text(x, y, label, transform=ax.transAxes, ha='left', va='bottom',
                   fontsize=8 if profile == 'nature-production' else 9,
                   fontweight='bold', color='#222222', clip_on=False)

def field_scale(kind, *, vmin=None, vmax=None, period=2*np.pi, start=-np.pi):
    """Explicit scale semantics. Never estimates normalization from individual panels."""
    if kind == 'phase':
        if not np.isfinite(period) or period <= 0 or not np.isfinite(start):
            raise ValueError('Phase period must be positive and finite')
        if vmin is not None or vmax is not None:
            raise ValueError('Use start and period for phase')
        return 'twilight', Normalize(start, start + period)
    if kind not in ('intensity', 'signed'):
        raise ValueError('kind must be intensity, signed or phase')
    if vmin is None or vmax is None or not np.isfinite([vmin,vmax]).all() or vmin >= vmax:
        raise ValueError('Provide a finite explicit increasing comparison range')
    if kind == 'intensity':
        if vmin < 0:
            raise ValueError('Intensity scale cannot start below zero')
        return 'magma', Normalize(vmin, vmax)
    if not vmin < 0 < vmax:
        raise ValueError('Signed scale must straddle zero')
    return 'RdBu_r', TwoSlopeNorm(0, vmin, vmax)

def geometry_report(fig, groups, tolerance_pt=1.5):
    """Check equal rendered axes widths/heights in explicitly comparable groups only."""
    if tolerance_pt <= 0:
        raise ValueError('tolerance_pt must be positive')
    fig.canvas.draw()
    out = {'scope': 'width/height only; no collision or shared-edge check', 'groups': []}
    for name, axes in groups.items():
        if len(axes) < 2:
            raise ValueError('Each comparison group needs at least two axes')
        boxes = [a.get_window_extent().transformed(fig.dpi_scale_trans.inverted()) for a in axes]
        rects = [[b.x0*72,b.y0*72,b.width*72,b.height*72] for b in boxes]
        dw = float(np.ptp([b.width*72 for b in boxes]))
        dh = float(np.ptp([b.height*72 for b in boxes]))
        out['groups'].append({'name':name,'rectangles_pt':rects,
                              'width_spread_pt':dw,'height_spread_pt':dh,
                              'pass':max(dw,dh)<=tolerance_pt})
    out['pass'] = all(x['pass'] for x in out['groups'])
    return out

def export_figure(fig, stem, formats=('pdf','svg','png'), dpi=450):
    if dpi <= 0:
        raise ValueError('dpi must be positive')
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths=[]
    fig.canvas.draw()
    # Avoid tight crop: it changes promised physical dimensions.
    with mpl.rc_context({'savefig.bbox':None,'pdf.fonttype':42,'svg.fonttype':'none'}):
        for fmt in formats:
            if fmt not in ('pdf','svg','png','tiff'):
                raise ValueError('Unsupported export format')
            path = Path(str(stem)+'.'+fmt)
            fig.savefig(path, dpi=dpi, bbox_inches=None)
            paths.append(str(path))
    return paths
