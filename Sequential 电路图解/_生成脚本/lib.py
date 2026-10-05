# -*- coding: utf-8 -*-
"""画图公共库：页面、门电路、带值的导线、时序图、表格、自动换行文字。
坐标系：整页 1169 x 827，y 向下。"""
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Rectangle

W, H = 1169, 827
RED, BLUE, GREY, YEL, GREEN = '#D9480F', '#1C5FC0', '#8C8C8C', '#F6C21C', '#2B8A3E'
INK, SUB, PEACH, PURPLE = '#1a1a1a', '#666666', '#FFF1DC', '#8E44AD'
plt.rcParams.update({'font.family': ['PingFang SC', 'Hiragino Sans GB', 'Arial Unicode MS'],
                     'pdf.fonttype': 3, 'mathtext.fontset': 'dejavusans',
                     'axes.unicode_minus': False, 'hatch.linewidth': 0.6})


def col(v):
    return RED if v == 1 else BLUE if v == 0 else GREY


def ov(s):
    return r'$\overline{%s}$' % s


def sv(v):
    return '?' if v is None else str(v)


# ---------- 三值逻辑 ----------
def NOT(a): return None if a is None else 1 - a
def AND(a, b): return 0 if (a == 0 or b == 0) else (1 if a == 1 and b == 1 else None)
def OR(a, b): return 1 if (a == 1 or b == 1) else (0 if a == 0 and b == 0 else None)
def NAND(a, b): return NOT(AND(a, b))
def NOR(a, b): return NOT(OR(a, b))


def settle(f, ta, tb, q, qb):
    """交叉耦合锁存器：上门 Q=f(ta,Q̄)，下门 Q̄=f(Q,tb)。不收敛(振荡)→未知。"""
    for _ in range(8):
        nq, nqb = f(ta, qb), f(q, tb)
        if (nq, nqb) == (q, qb):
            return q, qb
        q, qb = nq, nqb
    return None, None


# ---------- 文字换行 ----------
TOK = re.compile(r'\$[^$]*\$|[\x21-\x7e]+|\n|\s|.', re.S)


def tw(tok, fs):
    if tok.startswith('$') and len(tok) > 1:
        inner = re.sub(r'\\[a-zA-Z]+|[{}_^$ ]', '', tok)
        return len(inner) * fs * 0.66 / 0.72
    n = 0
    for ch in tok:
        n += 0.33 if ch == ' ' else 0.6 if ord(ch) < 0x2000 else 1.0
    return n * fs / 0.72


def wrap(text, width, fs):
    lines, cur, cw = [], '', 0
    for tok in TOK.findall(text):
        if tok == '\n':
            lines.append(cur); cur, cw = '', 0; continue
        t = tw(tok, fs)
        if cw + t > width and cur.strip():
            lines.append(cur); cur, cw = '', 0
            if tok.isspace():
                continue
        if tok in '，。；：、）！？' and not cur and lines:
            lines[-1] += tok; continue
        cur += tok; cw += t
    if cur:
        lines.append(cur)
    return lines


def para(ax, x, y, text, width, fs=9, lh=1.6, color=INK, weight='normal', va='top'):
    step = fs / 0.72 * lh
    for ln in wrap(text, width, fs):
        ax.text(x, y, ln, fontsize=fs, color=color, weight=weight, va=va, ha='left')
        y += step
    return y


def bullets(ax, x, y, items, width, fs=9.5, lh=1.6, gap=7, mark=None):
    for i, it in enumerate(items):
        m = (mark or '%d.' % (i + 1))
        ax.text(x, y, m, fontsize=fs, color=GREEN, weight='bold', va='top')
        y = para(ax, x + 24, y, it, width - 24, fs, lh) + gap
    return y


# ---------- 文档 / 页面 ----------
class Doc:
    def __init__(self, path, section):
        self.pdf, self.section, self.n, self.fig = PdfPages(path), section, 0, None

    def page(self, title, sub=None, legend=True):
        self._flush()
        self.fig = plt.figure(figsize=(11.69, 8.27))
        ax = self.fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
        self.n += 1
        ax.text(46, 27, self.section, color=GREEN, fontsize=8.5, weight='bold', va='center')
        ax.text(46, 56, title, fontsize=19, weight='bold', va='center', color=INK)
        if sub:
            ax.text(46, 91, sub, fontsize=9.6, color=SUB, va='center')
        if legend:
            for x, c, t in [(46, RED, '红 = 1'), (246, BLUE, '蓝 = 0'), (446, GREY, '灰虚线 = ?（未知/不确定）'),
                            (646, YEL, '黄框 = 这一步刚变的线'), (846, GREEN, '绿 = 开着（透明）的锁存器')]:
                ax.add_patch(Rectangle((x, 802), 9, 9, fc=c, ec='none'))
                ax.text(x + 15, 807, t, fontsize=7.5, color=c if c != YEL else '#C99700', va='center')
        ax.text(1133, 812, str(self.n), fontsize=7.5, color=SUB, ha='right', va='center')
        self.ax = ax
        return ax

    def _flush(self):
        if self.fig is not None:
            self.pdf.savefig(self.fig); plt.close(self.fig); self.fig = None

    def close(self):
        self._flush(); self.pdf.close()


def panel(ax, x, y, w, h, title, desc, fs=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=9', fc='#F8F8F8', ec='#D9D9D9', lw=1))
    ax.text(x + 12, y + 16, title, fontsize=10.5, weight='bold', va='center', color=INK)
    para(ax, x + 12, y + 34, desc, w - 24, fs, 1.6, '#333')


def grid(n, cols, top=118, bot=796, left=46, right=1123, gap=4):
    rows = (n + cols - 1) // cols
    w = (right - left - gap * (cols - 1)) / cols
    h = min(336, (bot - top - gap * (rows - 1) * 3) / rows)
    return [(left + (i % cols) * (w + gap), top + (i // cols) * (h + 11), w, h) for i in range(n)]


def box(ax, x, y, w, h, fc='#F8F8F8', ec='#D9D9D9'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=9', fc=fc, ec=ec, lw=1))


# ---------- 电路画布 ----------
class CV:
    def __init__(self, ax, ox, oy, sc=1.0):
        self.ax, self.ox, self.oy, self.sc, self.mono = ax, ox, oy, sc, False

    def P(self, x, y):
        return (self.ox + self.sc * x, self.oy + self.sc * y)

    def wire(self, pts, v, lw=3.0, z=2, c=None):
        xs, ys = zip(*[self.P(*p) for p in pts])
        if self.mono:
            c, lw = '#3a3a3a', lw * 0.7
        self.ax.plot(xs, ys, color=c or col(v), lw=lw * max(self.sc, 0.6), zorder=z,
                     ls=(0, (2.2, 1.5)) if (v is None and c is None) else '-',
                     solid_capstyle='round', solid_joinstyle='round', dash_capstyle='butt')

    def dot(self, x, y, v, r=3.2, c=None):
        if self.mono:
            c = '#3a3a3a'
        self.ax.add_patch(Circle(self.P(x, y), r * self.sc, fc=c or col(v), ec='none', zorder=3))

    def badge(self, x, y, txt, v, chg=False, fs=7.2):
        if self.mono:
            return
        self.ax.text(*self.P(x, y), txt, fontsize=fs, color='white', weight='bold', ha='center', va='center', zorder=10,
                     bbox=dict(boxstyle='round,pad=0.22', fc=col(v), ec=YEL if chg else col(v), lw=2.0 if chg else 0.4))

    def label(self, x, y, txt, fs=10, ha='center', weight='bold', color=INK, va='center'):
        self.ax.text(*self.P(x, y), txt, fontsize=fs, ha=ha, va=va, weight=weight, color=color, zorder=11)

    def gate(self, kind, x, y, h=36):
        base = {'nand': 'and', 'nor': 'or'}.get(kind, kind)
        if base == 'and':
            th = np.linspace(-np.pi / 2, np.pi / 2, 24)
            pts = [(x, y - h / 2)] + [(x + h * .5 + h / 2 * np.cos(t), y + h / 2 * np.sin(t)) for t in th] + [(x, y + h / 2)]
            tip, xin = x + h, x
        elif base == 'or':
            t = np.linspace(0, 1, 16)[:, None]
            def q(p0, p1, p2): return ((1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) + t ** 2 * np.array(p2)).tolist()
            pts = q((x, y - h / 2), (x + .65 * h, y - h / 2), (x + 1.08 * h, y)) + \
                q((x + 1.08 * h, y), (x + .65 * h, y + h / 2), (x, y + h / 2)) + q((x, y + h / 2), (x + .3 * h, y), (x, y - h / 2))
            tip, xin = x + 1.08 * h, x + 0.11 * h
        else:  # not
            pts = [(x, y - h / 2), (x + .85 * h, y), (x, y + h / 2)]
            tip, xin = x + .85 * h, x
        self.ax.add_patch(Polygon([self.P(*p) for p in pts], closed=True, fc='white', ec='#222', lw=1.5, zorder=5, joinstyle='round'))
        xo = tip
        if kind in ('nand', 'nor', 'not'):
            r = max(2.6, 0.085 * h)
            self.ax.add_patch(Circle(self.P(tip + r, y), r * self.sc, fc='white', ec='#222', lw=1.3, zorder=5))
            xo = tip + 2 * r
        return dict(a=(xin, y - h / 4), b=(xin, y + h / 4), o=(xo, y), i=(x, y))

    def block(self, x, y, w, h, on=None, title=None, state=None, pins=(), fs=8.5, clk=None):
        fc, ec = {True: ('#E6F4EA', GREEN), False: ('#EEEEEE', '#8C8C8C'), None: ('#EAF0FF', '#3355BB')}[on]
        x0, y0 = self.P(x, y)
        self.ax.add_patch(FancyBboxPatch((x0, y0), w * self.sc, h * self.sc, boxstyle='round,pad=0,rounding_size=%g' % (5 * self.sc),
                                         fc=fc, ec=ec, lw=1.8, zorder=4))
        if title:
            self.label(x + w / 2, y - 9, title, fs=fs, weight='bold')
        if state:
            self.label(x + w / 2, y + h / 2 + (8 if clk is None else 0), state, fs=fs + 1.5, color=ec)
        for txt, px, py in pins:
            self.label(x + px, y + py, txt, fs=fs, weight='normal', ha='center')
        if clk is not None:
            self.ax.add_patch(Polygon([self.P(x, y + clk - 7), self.P(x + 11, y + clk), self.P(x, y + clk + 7)], closed=True,
                                      fc='white', ec='#222', lw=1.2, zorder=6))


def latch(cv, kind, gx, yt, tin, bin_, q, qb, dy=96, h=36, out=62):
    """交叉耦合的两个门（NOR 或 NAND）。返回 (上门, 下门, 输出线末端x)。"""
    g1, g2 = cv.gate(kind, gx, yt, h), cv.gate(kind, gx, yt + dy, h)
    xo = g1['o'][0]; xt, xe, xf = xo + 30, xo + out, gx - 22
    m1, m2 = yt + dy * .36, yt + dy * .64
    cv.wire([g1['o'], (xe, yt)], q); cv.wire([g2['o'], (xe, yt + dy)], qb)
    cv.wire([(xt, yt), (xt, m1), (xf, m2), (xf, g2['a'][1]), g2['a']], q)
    cv.wire([(xt, yt + dy), (xt, m2), (xf, m1), (xf, g1['b'][1]), g1['b']], qb)
    cv.dot(xt, yt, q); cv.dot(xt, yt + dy, qb)
    return g1, g2, xe


# ---------- 时序图 ----------
def timing(ax, x0, y0, w, rows, n, rowh=50, heads=None, shade=(), edges=(), vals=True, hl=None, fs=10, lw=2.4):
    """rows: [(标签, [每格的值])]；值为 0/1/None(未知)；值为字符串时画成总线。
    shade: [(a,b)] 第 a..b 格涂浅橙；edges: [(格边界下标, '↑'或'↓')]。"""
    cw = w / n; tot = rowh * len(rows)
    for a, b in shade:
        ax.add_patch(Rectangle((x0 + a * cw, y0 - 6), (b - a) * cw, tot + 6, fc=PEACH, ec='none', zorder=0))
    if heads:
        for i, t in enumerate(heads):
            ax.text(x0 + (i + .5) * cw, y0 - 18, t, fontsize=9, color='#444', ha='center', va='center')
            ax.plot([x0 + i * cw] * 2, [y0 - 4, y0 + tot], color='#E3E3E3', lw=0.7, zorder=0.5)
    if hl is not None:
        ax.add_patch(Rectangle((x0 + hl * cw, y0 - 8), cw, tot + 10, fc='none', ec=GREEN, lw=2.2, zorder=9))
    for k, e in edges:
        x = x0 + k * cw
        ax.plot([x, x], [y0 - 8, y0 + tot], color='#E6A700', lw=1.2, ls=(0, (1, 2)), zorder=6)
        ax.text(x, y0 - (34 if heads else 16), e, fontsize=10, color='#C98A00', ha='center', va='center')
    for r, row in enumerate(rows):
        lab, vs = row[0], row[1]
        yh = y0 + r * rowh + rowh * 0.2; yl = y0 + r * rowh + rowh * 0.8
        ax.text(x0 - 12, (yh + yl) / 2, lab, fontsize=fs, ha='right', va='center', color=INK)
        ax.plot([x0, x0 + w], [yl + 3, yl + 3], color='#E8E8E8', lw=0.7, zorder=0.5)
        i = 0
        while i < n:
            j = i
            while j < n and vs[j] == vs[i]:
                j += 1
            v, xa, xb = vs[i], x0 + i * cw, x0 + j * cw
            if isinstance(v, str):
                d = min(4, cw * .2)
                ax.add_patch(Polygon([(xa, (yh + yl) / 2), (xa + d, yh), (xb - d, yh), (xb, (yh + yl) / 2), (xb - d, yl), (xa + d, yl)],
                                     closed=True, fc='#F4F6FA' if '?' not in v else '#E0E0E0', ec='#444', lw=1.4, zorder=3,
                                     hatch='////' if '?' in v else None))
                ax.text((xa + xb) / 2, (yh + yl) / 2, v, fontsize=fs - 1, ha='center', va='center', weight='bold', color=INK, zorder=4,
                        family='Menlo')
            elif v is None:
                ax.add_patch(Rectangle((xa, yh + 2), xb - xa, yl - yh - 2, fc='#E0E0E0', ec='#999', hatch='////', lw=0.6, zorder=2))
            else:
                y = yh if v == 1 else yl
                ax.plot([xa, xb], [y, y], color=col(v), lw=lw, zorder=3, solid_capstyle='butt')
                if vals and (xb - xa) > 14:
                    ax.text((xa + xb) / 2, (yh + yl) / 2, str(v), fontsize=6.8, color=col(v), ha='center', va='center')
            if j < n and v in (0, 1) and vs[j] in (0, 1):
                ax.plot([xb, xb], [yh, yl], color='#222', lw=1.6, zorder=4)
            i = j
    return y0 + tot


def expand(vals, k):
    """把每格的值重复 k 次（用于把粗格变细格）。"""
    out = []
    for v in vals:
        out += [v] * k
    return out


# ---------- 表格 ----------
def table(ax, x, y, colw, rowh, data, hl=(), fs=9, head=True, left=(), headfc='#E9ECEF', lw=1.0, hlfc='#FFF3BF'):
    """data: 行的列表。hl: {(i,j)} 或 {i} 高亮。left: 需要左对齐并自动换行的列号。rowh 可为数或列表。"""
    rh = rowh if isinstance(rowh, (list, tuple)) else [rowh] * len(data)
    yy = y
    for i, row in enumerate(data):
        xx = x
        for j, cell in enumerate(row):
            fc = headfc if (head and i == 0) else (hlfc if ((i, j) in hl or i in hl) else 'white')
            ax.add_patch(Rectangle((xx, yy), colw[j], rh[i], fc=fc, ec='#111', lw=lw, zorder=1))
            s = sv(cell) if not isinstance(cell, str) else cell
            c = RED if s == '1' else BLUE if s == '0' else GREY if s == '?' else INK
            bold = (head and i == 0) or s in ('0', '1', '?')
            if j in left and not (head and i == 0):
                lines = wrap(s, colw[j] - 24, fs)
                step = fs / 0.72 * 1.45
                ty = yy + rh[i] / 2 - step * (len(lines) - 1) / 2
                for ln in lines:
                    ax.text(xx + 7, ty, ln, fontsize=fs, color=c, va='center', ha='left', zorder=2); ty += step
            else:
                ax.text(xx + colw[j] / 2, yy + rh[i] / 2, s, fontsize=fs + (0.5 if s in ('0', '1') else 0), color=c, va='center', ha='center',
                        weight='bold' if bold else 'normal', zorder=2)
            xx += colw[j]
        yy += rh[i]
    return yy


def changes(seq):
    """seq: 每步的 {名字:值}。返回每步相对上一步变化了的名字集合。"""
    out = [set()]
    for a, b in zip(seq, seq[1:]):
        out.append({k for k in b if b[k] != a.get(k)})
    return out


def val_table(ax, x, y, w, names, labels, seq, fs=9, rowh=20, labw=16, heads=None):
    """时序图下面的数值表：黄底 = 和上一步相比变了。"""
    n = len(seq); cw = w / n; ch = changes(seq)
    data = [[''] + (heads or [str(i + 1) for i in range(n)])]
    hl = set()
    for r, (k, lab) in enumerate(zip(names, labels)):
        data.append([lab] + [seq[i][k] for i in range(n)])
        hl |= {(r + 1, i + 1) for i in range(n) if k in ch[i]}
    for r, lab in enumerate(labels):
        ax.text(x - 8, y + rowh * (r + 1.5), lab, fontsize=fs, ha='right', va='center')
    return table(ax, x, y, [cw] * n, rowh, [row[1:] for row in data], hl={(i, j - 1) for i, j in hl}, fs=fs, headfc='#F0F0F0')
