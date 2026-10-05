# -*- coding: utf-8 -*-
"""05 边沿触发 D 触发器  06 T 触发器  07 JK 触发器  08 带使能端的 D 触发器
电路画法全部按课件 flipflops_slides.pdf。线上的值由仿真算出。"""
import os
from lib import *
from latches import notes_page, steps_box, OUT, QB, SB, RB, DB, QT, QN

Q1, Q1B, CB, ENB, KB = '$Q_1$', r'$\overline{Q}_1$', ov('C'), ov('EN'), ov('K')
UP, DN = '↑', '↓'


def B(cv, x, y, name, v, key, chg, fs=None):
    cv.badge(x, y, '%s=%s' % (name, sv(v[key])), v[key], key in chg, fs or (7.0 if cv.sc < 0.9 else 8.6))


def panels(doc, title, sub, items, seq, draw, cols, sc, off, chs=None, per=None):
    ch = chs or changes(seq); per = per or len(items); pages = (len(items) + per - 1) // per
    for p in range(pages):
        ax = doc.page(title + ('（%d/%d）' % (p + 1, pages) if pages > 1 else ''), sub)
        sl = slice(p * per, (p + 1) * per)
        for (x, y, w, h), (t, d), v, c in zip(grid(per, cols), items[sl], seq[sl], ch[sl]):
            panel(ax, x, y, w, h, t, d, fs=8.6 if cols <= 2 else 7.6)
            draw(CV(ax, x + off[0], y + off[1], sc), v, c)
    return ax


def edge_list(C):
    return [(i, UP) for i in range(1, len(C)) if C[i] == 1 and C[i - 1] == 0]


def shades(C):
    out, i, n = [], 0, len(C)
    while i < n:
        if C[i] == 1:
            j = i
            while j < n and C[j] == 1:
                j += 1
            out.append((i, j)); i = j
        else:
            i += 1
    return out


def bits(s):
    return [int(c) for c in s.replace(' ', '')]


# ================= 05 边沿触发 D 触发器 =================
def draw_dff(pos):
    def f(cv, v, chg=()):
        mo, so = (None, None) if cv.mono else (v['Cm'] == 1, v['Cs'] == 1)
        fs = 7.6 if cv.sc < 0.9 else 10
        cv.block(70, 0, 70, 110, on=mo, title='主锁存器', state=None if cv.mono else ('开' if mo else '关'), fs=fs,
                 pins=[('D', 11, 20), ('C', 11, 55), ('Q', 59, 20), (QB, 59, 90)])
        cv.block(205, 0, 70, 110, on=so, title='从锁存器', state=None if cv.mono else ('开' if so else '关'), fs=fs,
                 pins=[('S', 11, 20), ('C', 11, 55), ('R', 11, 90), ('Q', 59, 20), (QB, 59, 90)])
        cv.wire([(0, 20), (70, 20)], v['D'])
        cv.wire([(140, 20), (205, 20)], v['Q1']); cv.wire([(140, 90), (205, 90)], v['Q1b'])
        cv.wire([(275, 20), (322, 20)], v['Q']); cv.wire([(275, 90), (322, 90)], v['Qb'])
        if not pos:
            cv.wire([(0, 55), (70, 55)], v['C']); cv.wire([(24, 55), (24, 140), (44, 140)], v['C']); cv.dot(24, 55, v['C'])
            inv = cv.gate('not', 44, 140, 18)
            cv.wire([inv['o'], (184, 140), (184, 55), (205, 55)], v['Cs'])
            B(cv, 30, 70, 'C', v, 'C', chg); B(cv, 120, 154, CB, v, 'Cs', chg)
        else:
            cv.wire([(0, 55), (12, 55)], v['C']); inv1 = cv.gate('not', 12, 55, 16)
            cv.wire([inv1['o'], (70, 55)], v['Cm']); cv.dot(46, 55, v['Cm'])
            cv.wire([(46, 55), (46, 140), (66, 140)], v['Cm']); inv2 = cv.gate('not', 66, 140, 18)
            cv.wire([inv2['o'], (184, 140), (184, 55), (205, 55)], v['Cs'])
            B(cv, 8, 72, 'C', v, 'C', chg); B(cv, 50, 40, CB, v, 'Cm', chg); B(cv, 135, 154, 'C', v, 'Cs', chg)
        cv.label(-10, 20, 'D', fs=fs + 1); cv.label(-10, 55, 'C', fs=fs + 1); cv.label(333, 20, 'Q', fs=fs + 1); cv.label(333, 90, QB, fs=fs + 1)
        B(cv, 34, 6, 'D', v, 'D', chg); B(cv, 172, 6, Q1, v, 'Q1', chg); B(cv, 162, 104, Q1B, v, 'Q1b', chg)
        B(cv, 300, 6, 'Q', v, 'Q', chg); B(cv, 300, 104, QB, v, 'Qb', chg)
    return f


def sim_ms(steps, pos):
    q1 = q = qb = None; out = []
    for C, D in steps:
        Cm = NOT(C) if pos else C; Cs = NOT(Cm)
        if Cm == 1:
            q1 = D
        if Cs == 1:
            q, qb = q1, NOT(q1)
        out.append(dict(C=C, D=D, Cm=Cm, Cs=Cs, Q1=q1, Q1b=NOT(q1), Q=q, Qb=qb))
    return out


def symbol(ax, x, y, kind, label):
    cv = CV(ax, x, y, 1.0)
    cv.block(0, 0, 56, 70, pins=[('D', 10, 16), ('Q', 46, 16), (QB, 46, 54)] + ([('C', 10, 52)] if kind == 'latch' else []),
             clk=None if kind == 'latch' else 52, fs=8.5)
    cv.wire([(-16, 16), (0, 16)], 0, c='#333', lw=1.6); cv.wire([(56, 16), (72, 16)], 0, c='#333', lw=1.6); cv.wire([(56, 54), (72, 54)], 0, c='#333', lw=1.6)
    if kind == 'neg':
        ax.add_patch(Circle(cv.P(-4, 52), 4, fc='white', ec='#222', lw=1.2, zorder=6)); cv.wire([(-16, 52), (-8, 52)], 0, c='#333', lw=1.6)
    else:
        cv.wire([(-16, 52), (0, 52)], 0, c='#333', lw=1.6)
    ax.text(x + 28, y + 86, label, fontsize=8.2, ha='center', va='top', color=INK, linespacing=1.4)


def pdf_dff():
    doc = Doc(os.path.join(OUT, '05_边沿触发D触发器.pdf'), '边沿触发 D 触发器 · Edge-triggered D flip-flop')
    # --- 正边沿 ---
    seq = sim_ms([(0, 1), (1, 1), (1, 0), (0, 0), (0, 1), (0, 0), (1, 0), (1, 1)], True)
    items = [
        ('1. C=0, D=1：主开从关', '%s=1 → 主锁存器透明，%s=D=1。从锁存器的 C=0 → 关着，Q 从没被写过 → 未知。' % (CB, Q1)),
        ('2. 上升沿 C 0→1：Q 更新', '主锁存器关上，把 %s 冻结在边沿前的 D=1；同一时刻从锁存器打开：S=%s=1、R=%s=0 → Q=1。' % (Q1, Q1, Q1B)),
        ('3. C=1 期间 D 变 0', '主锁存器关着，D 的变化进不去 → %s 仍是 1。从锁存器开着但它的输入没变 → Q 仍是 1。' % Q1),
        ('4. 下降沿 C 1→0：Q 不变', '主锁存器重新打开 → %s=D=0。从锁存器关上 → Q 保持 1。下降沿对这个电路没有意义。' % Q1),
        ('5. C=0 期间 D 变 1', '主锁存器透明 → %s 跟着变 1。但从锁存器关着，Q 仍是 1。新值只“等”在两个锁存器之间。' % Q1),
        ('6. C=0 期间 D 又变 0', '%s 又跟着变 0，Q 还是不动。C=0 期间 D 怎么抖都没关系，只有边沿那一刻的值算数。' % Q1),
        ('7. 上升沿：Q 更新为 0', '主锁存器冻结 %s=0（边沿前一刻的 D）；从锁存器打开：S=0、R=1 → Q=0。' % Q1),
        ('8. C=1 期间 D 变 1：无效', '主锁存器关着 → %s=0 不变 → Q=0 不变。要等下一个上升沿。' % Q1),
    ]
    panels(doc, '1. 正边沿 D 触发器（课程选用）：8 步逐线图解',
           '课件 “positive-edge triggered”：C 先过一个非门进主锁存器（看 %s），再过一个非门进从锁存器（看 C）。主从永远一开一关，Q 只在 C 由 0→1 那一刻改变。' % CB,
           items, seq, draw_dff(True), 2, 1.12, (88, 128), per=4)
    ax = doc.page('1. 正边沿 D 触发器时序图', '浅橙背景 = C=1。黄色虚线 = 上升沿，Q 只在这里改变。格子编号 = 上一页的 8 步。')
    keys = ['D', 'C', 'Cm', 'Q1', 'Q1b', 'Q', 'Qb']; labs = ['D', 'C', CB, Q1, Q1B, 'Q', QB]
    yb = timing(ax, 105, 150, 1018, [(l, [s[k] for s in seq]) for k, l in zip(keys, labs)], 8, rowh=46,
                heads=[str(i + 1) for i in range(8)], shade=[(1, 3), (6, 8)], edges=[(1, UP), (6, UP)])
    ax.text(105, yb + 30, '数值表（黄底 = 和上一格相比发生了变化）', fontsize=9, color=SUB)
    yb = val_table(ax, 105, yb + 44, 1018, keys, labs, seq)
    para(ax, 105, yb + 26, '读图要点：① %s（主锁存器输出）在 C=0 的白色区域里照抄 D，在橙色区域里是水平线。② Q 在每条黄色虚线处变成“那一刻的 %s”，也就是边沿前一瞬间的 D。'
         '③ 第 3、8 格：C=1 期间 D 变了，Q 不理。第 5、6 格：C=0 期间 D 抖了两下，只有最后的值（0）在第 7 格被采样。' % (Q1, Q1), 1010, 9.2)
    # --- 负边沿（课件逐步图）---
    seqn = sim_ms([(1, 0), (0, 0), (0, 1), (1, 1), (0, 1), (0, 0), (1, 0), (0, 0)], False)
    itemsn = [
        ('1. C=1, D=0（课件图 1）', '时钟为高 → 主锁存器把 D 送到 %s=0。从锁存器的 C=%s=0，什么也不做 → Q 未知（课件写成 Z）。' % (Q1, CB)),
        ('2. 下降沿 C 1→0（课件图 2）', '主锁存器停止传输（冻结 %s=0），从锁存器开始工作：S=0、R=1 → Q=0、%s=1。' % (Q1, QB)),
        ('3. C=0 时 D 变 1（课件图 3）', '主锁存器关着 → 变化传不到从锁存器，要等时钟再变高。Q 仍是 0。'),
        ('4. 上升沿 C 0→1（课件图 4）', '主锁存器开始传输（%s=1）的同时，从锁存器停止（Q 保持 0）。新值卡在中间。' % Q1),
        ('5. 下降沿：Q 更新为 1', '主锁存器冻结 %s=1，从锁存器打开：S=1、R=0 → Q=1。输出只在下降沿改变。' % Q1),
        ('6. C=0 时 D 变 0', '被挡在主锁存器门外，%s、Q 都不变。' % Q1),
        ('7. 上升沿', '主锁存器打开：%s=D=0。从锁存器关上：Q 保持 1。' % Q1),
        ('8. 下降沿：Q 更新为 0', '从锁存器复制 %s=0 → Q=0、%s=1。' % (Q1, QB)),
    ]
    panels(doc, '1. 负边沿 D 触发器（课件 Flip-flop behaviour 逐步图）',
           '课件先讲的版本：D latch 接 SR latch，C 直接进主锁存器、%s 进从锁存器 → “negative-edge triggered”。Q 只在 C 由 1→0 那一刻改变。' % CB,
           itemsn, seqn, draw_dff(False), 2, 1.12, (88, 128), per=4)
    # --- 必考对比 ---
    ax = doc.page('1. 必考：同一组 C 和 D，三种器件的 Q 分别是什么？', '给你 C、D 波形，让你画 D 锁存器 / 负边沿 D 触发器 / 正边沿 D 触发器 的 Q。（一开始未知 → 斜线）')
    D = bits('0011101111 0000100011 1110001111 1110000110'); n = 40
    C = [(1 if (i % 8) >= 4 else 0) for i in range(n)]
    ql, qn, qp, a, b, c = [], [], [], None, None, None
    for i in range(n):
        if C[i] == 1:
            a = D[i]
        if i and C[i] == 1 and C[i - 1] == 0:
            c = D[i - 1]
        if i and C[i] == 0 and C[i - 1] == 1:
            b = D[i - 1]
        ql.append(a); qn.append(b); qp.append(c)
    ed = [(i, UP if C[i] else DN) for i in range(1, n) if C[i] != C[i - 1]]
    timing(ax, 150, 160, 980, [('C', C), ('D', D), ('Q（D 锁存器）', ql), ('Q（负边沿 FF）', qn), ('Q（正边沿 FF）', qp)], n,
           rowh=78, shade=shades(C), edges=ed, vals=False)
    bullets(ax, 70, 590, [
        'D 锁存器：橙色区域（C=1）内照抄 D，包括所有抖动；白色区域保持 C 下降那一刻的值。',
        '负边沿 FF：只看每条 “↓” 虚线左边一点点的 D，然后一直保持到下一个 ↓。C=1 期间 D 怎么抖都不管。',
        '正边沿 FF：只看每条 “↑” 虚线左边一点点的 D，然后一直保持到下一个 ↑。',
        '口诀：锁存器看“区间”，触发器看“点”。先把所有有效边沿的竖线画出来，再在每条线上读 D，最后连成阶梯。'], 1000, fs=9.3, mark='•')
    # --- 真值表 ---
    ax = doc.page('2. 解析 Truth table：D 触发器什么时候变、变成什么', '特性表 + 四个阶段里主/从锁存器各在干什么（以课程选用的正边沿型为例）。', legend=False)
    cv = CV(ax, 70, 150, 0.95); cv.mono = True
    draw_dff(True)(cv, dict(C=0, D=0, Cm=0, Cs=0, Q1=0, Q1b=0, Q=0, Qb=0))
    para(ax, 46, 330, '特征方程：$Q_{T+1}$ = D（只在有效边沿生效）\n\n主锁存器 = D latch，看 %s：%s=1（即 C=0）时 %s 跟随 D。\n从锁存器 = SR latch，看 C：C=1 时 S=%s、R=%s，把 %s 复制到 Q。\n'
         '因为 S、R 永远相反，从锁存器不会进入禁止态。\n\n负边沿型：去掉 C 前面那个非门即可（主看 C、从看 %s），下面两张表里“↑”和“↓”、“C=0”和“C=1”全部对调。'
         % (CB, CB, Q1, Q1, Q1B, Q1, CB), 360, 9.3, 1.7)
    table(ax, 440, 118, [80, 60, 80, 463], 30,
          [['Clk', 'D', QN, '为什么'],
           [UP, '0', '0', '上升沿瞬间：主锁存器关上（冻结 %s=0），从锁存器打开，把 0 复制到 Q。' % Q1],
           [UP, '1', '1', '同上，复制的是 1。$Q_{T+1}$ 只取决于边沿前一刻的 D，与旧的 Q 无关。'],
           ['0', 'X', QT, '从锁存器关着 → Q 保持。D 的变化只走到 %s。' % Q1],
           ['1', 'X', QT, '主锁存器关着 → %s 不变 → 从锁存器虽然开着，但写进去的还是同一个值。' % Q1],
           [DN, 'X', QT, '主锁存器打开、从锁存器关上 → Q 保持。下降沿不是有效边沿。']], left={3}, fs=8.8, hl={1, 2})
    ax.text(440, 330, '时钟的四个阶段（黄色那一行是唯一会改变 Q 的时刻）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 346, [120, 140, 110, 170, 143], 34,
          [['阶段', '主锁存器（看 %s）' % CB, '从锁存器（看 C）', Q1, 'Q'],
           ['C = 0（低）', '开（透明）', '关', '跟随 D', '不变'],
           ['上升沿 0→1', '关上，冻结', '打开', '冻结在边沿前的 D', '← 变成 %s' % Q1],
           ['C = 1（高）', '关', '开', '不变', '= %s，不变' % Q1],
           ['下降沿 1→0', '打开', '关上', '开始跟随 D', '冻结']], fs=9, hl={2})
    ax.text(440, 548, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 564, [240, 130, 313], 36,
          [['发生了什么', 'Q 的反应', '说明'],
           ['两个上升沿之间 D 变了很多次', '不变', '只有下一个上升沿前一瞬间的值会被采样'],
           ['上升沿到来，D ≠ Q', '变成 D', '比边沿稍晚一点点（clk-to-Q 延迟）'],
           ['上升沿到来，D = Q', '不变', '其实是把同一个值又写了一遍'],
           ['D 恰好在上升沿同时变化', '取变化前的旧值', '理想题按“边沿之前的值”算；真实电路这是 setup/hold 违规'],
           ['第一个上升沿之前', '?', '上电状态未知（课件图里写 Z），需要 reset']], left={2}, fs=8.8)
    notes = [
        '触发器（flip-flop）= 输出只在时钟的上升沿或下降沿改变的存储电路。D 触发器 = D latch（主）+ SR latch（从）+ 非门，主从永远一开一关。',
        '课件先画负边沿型（C 直接进主、%s 进从），再在 C 前面加一个非门得到正边沿型，并说“our choice for the course”。没有特别说明时按上升沿做。' % CB,
        '只在有效边沿采样：边沿以外的任何时刻，D 怎么变 Q 都不动。不要像锁存器那样在 C=1 期间跟着 D 画。',
        '采样的是“边沿之前一瞬间”的 D。如果 D 画成和边沿同时跳变，取跳变前的值。',
        'Q 的跳变画在边沿处（或稍微靠右一点表示延迟），然后水平保持到下一个有效边沿。',
        '第一个有效边沿之前 Q 未知（画斜线 / 写 ? 或 Z），除非题目给了初值或有 reset。',
        'Setup time：有效边沿之前 D 必须已经稳定一段时间。Hold time：有效边沿之后 D 还要继续稳定一段时间。输入不能在边沿附近变化。',
        '最高时钟频率：时钟周期 ≥ 任意两个触发器之间最长的传播延迟 + 触发器的 setup time。例：最长延迟 8 ns、setup 2 ns → 周期 ≥ 10 ns → 最高 100 MHz。',
        'Reset：同步复位只在有效边沿把 Q 清 0；异步复位一有效 Q 立刻清 0，不看时钟。它和 SR 锁存器的 R 输入不是一回事。',
        '符号：时钟端有三角形 = 边沿触发；三角形外再加小圆圈 = 负边沿；没有三角形、写着 C = 锁存器。%s 端的小圆圈只是“反相输出”。' % QB,
        '主从 SR 触发器（课件 SR master-slave）结构相同，只是主锁存器是 SR latch，所以 S=R=1 的问题仍然存在；D 触发器解决了它。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clk、D 波形画 Q）', [
            '看符号/题目：上升沿还是下降沿触发？',
            '把所有有效边沿画成竖虚线。',
            '在每条虚线左边一点点读 D 的值。',
            'Q 在这条虚线处变成该值，然后水平画到下一条虚线。',
            '第一条虚线之前画斜线（未知）。',
            '有中间线（如 %s）的题：先画中间线，再画 Q。' % Q1])
        ax.text(x, y + 6, '三种符号', fontsize=11, weight='bold', color=GREEN, va='top')
        symbol(ax, x + 30, y + 40, 'latch', 'D 锁存器\n电平触发'); symbol(ax, x + 160, y + 40, 'pos', '正边沿 FF\n只有三角形'); symbol(ax, x + 290, y + 40, 'neg', '负边沿 FF\n圆圈 + 三角形')
        y2 = y + 180
        ax.text(x, y2, 'Setup / Hold', fontsize=11, weight='bold', color=GREEN, va='top')
        x0, ww, yy = x + 34, w - 40, y2 + 34
        ax.add_patch(Rectangle((x0 + ww * 9 / 24, yy - 4), ww * 3 / 24, 80, fc='#D0E4FF', ec='none', zorder=1.5))
        ax.add_patch(Rectangle((x0 + ww * 12 / 24, yy - 4), ww * 2 / 24, 80, fc='#FFD9D9', ec='none', zorder=1.5))
        timing(ax, x0, yy, ww, [('Clk', [0] * 12 + [1] * 12), ('D', [0] * 5 + [1] * 14 + [0] * 5)], 24, rowh=38, vals=False, fs=9, lw=2, edges=[(12, UP)])
        ax.text(x0 + ww * 10.5 / 24, yy + 90, 'setup', fontsize=8.5, color=BLUE, ha='center'); ax.text(x0 + ww * 13.4 / 24, yy + 90, 'hold', fontsize=8.5, color='#C92A2A', ha='center')
        para(ax, x, yy + 104, '蓝色 + 红色窗口内 D 不许变。', w, 8.6, 1.5, '#333')
    notes_page(doc, '3. 满分注意事项：边沿触发 D 触发器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 06 T 触发器 =================
def draw_t(cv, v, chg=()):
    a1, a2 = cv.gate('and', 50, 20, 30), cv.gate('and', 50, 90, 30)
    cv.block(118, 0, 75, 110, title='SR 触发器', pins=[('S', 12, 20), ('R', 12, 90), ('Q', 63, 20), (QB, 63, 90)], clk=55, fs=8)
    cv.wire([a1['o'], (118, 20)], v['S']); cv.wire([a2['o'], (118, 90)], v['R'])
    cv.wire([(0, 30), (30, 30)], v['T']); cv.wire([(50, 27.5), (30, 27.5), (30, 82.5), (50, 82.5)], v['T']); cv.dot(30, 30, v['T'])
    cv.wire([(0, 55), (118, 55)], v['C'])
    cv.wire([(193, 20), (275, 20)], v['Q']); cv.wire([(193, 90), (275, 90)], v['Qb'])
    cv.wire([(225, 90), (225, -24), (38, -24), (38, 12.5), (50, 12.5)], v['Qb']); cv.dot(225, 90, v['Qb'])
    cv.wire([(210, 20), (210, 134), (38, 134), (38, 97.5), (50, 97.5)], v['Q']); cv.dot(210, 20, v['Q'])
    cv.label(-9, 30, 'T', fs=9); cv.label(-9, 55, 'C', fs=9); cv.label(286, 20, 'Q'); cv.label(286, 90, QB)
    B(cv, 12, 16, 'T', v, 'T', chg); B(cv, 14, 69, 'C', v, 'C', chg)
    B(cv, 99, 7, 'S', v, 'S', chg); B(cv, 99, 103, 'R', v, 'R', chg)
    B(cv, 252, 7, 'Q', v, 'Q', chg); B(cv, 252, 103, QB, v, 'Qb', chg)


def sim_t(steps, q=0):
    out, pc, S, R = [], None, None, None
    for C, T in steps:
        if pc == 0 and C == 1:
            q = 1 if S == 1 else 0 if R == 1 else q
        S, R = AND(T, NOT(q)), AND(T, q)
        out.append(dict(C=C, T=T, S=S, R=R, Q=q, Qb=NOT(q))); pc = C
    return out


def pdf_t():
    doc = Doc(os.path.join(OUT, '06_T触发器.pdf'), 'T 触发器 · T flip-flop (Toggle)')
    seq = sim_t([(0, 0), (0, 1), (1, 1), (0, 1), (1, 1), (0, 0), (1, 0), (1, 1)])
    items = [
        ('1. T=0, Q=0：两个 AND 都出 0', 'S=T·%s=0、R=T·Q=0 → SR 触发器处于“保持”。此时就算来上升沿，Q 也不变。（假设初值 Q=0）' % QB),
        ('2. T 变 1（时钟还是低）', 'S=T·%s=1·1=1，R=T·Q=1·0=0 → 已经“准备好置位”，但没到边沿，Q 不动。' % QB),
        ('3. 上升沿：Q 翻成 1', '边沿采到 S=1,R=0 → Q=1。随后反馈使 S=0、R=1（为下一次翻回去做准备），但这个边沿已经过去，不会再翻。'),
        ('4. 下降沿：什么都不发生', '触发器只认上升沿。Q、S、R 都不变。'),
        ('5. 上升沿：Q 翻回 0', '边沿采到 S=0,R=1 → Q=0。反馈又把 S、R 换回 1、0。T=1 时每个上升沿翻一次。'),
        ('6. 时钟变低，T 变 0', 'T=0 把两个 AND 都关掉：S=R=0。'),
        ('7. 上升沿：保持', '采到 S=R=0 → 保持，Q 仍是 0。T=0 时再多的时钟也不翻。'),
        ('8. C=1 期间 T 变 1：无效', 'S 变成 1，但上升沿已经过了 → Q 不变。T 只在边沿那一刻被“看”一次。'),
    ]
    panels(doc, '1. T 触发器：8 步逐线图解',
           '课件电路：两个 AND 门 + 一个边沿触发的 SR 触发器。上面的 AND：S = T·%s；下面的 AND：R = T·Q。T=1 → 每个上升沿翻转；T=0 → 保持。' % QB,
           items, seq, draw_t, 4, 0.78, (26, 158))
    # 时序：复刻课件波形
    ax = doc.page('1. T 触发器时序图（和课件同一组波形）', '浅橙 = Clock=1；黄色虚线 = 上升沿。Q 只在虚线处、且当时 T=1 才翻转。')
    n = 34; C = [(1 if (i % 8) >= 4 else 0) for i in range(n)]
    T = [0] * 2 + [1] * 5 + [0] * 7 + [1] * 9 + [0] * 3 + [1] * 8
    Q, S, R, q = [], [], [], 0
    rows_e = [['上升沿', 'T（边沿前）', 'Q（边沿前）', 'S=T·%s' % QB, 'R=T·Q', 'Q（边沿后）', '动作']]
    k = 0
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            k += 1; t, old = T[i - 1], q
            q = q ^ t
            rows_e.append(['第 %d 个 ↑' % k, t, old, t & (1 - old), t & old, q, '翻转' if t else '保持'])
        Q.append(q); S.append(T[i] & (1 - q)); R.append(T[i] & q)
    yb = timing(ax, 150, 150, 970, [('Clock', C), ('T', T), ('S=T·%s' % QB, S), ('R=T·Q', R), ('Q', Q), (QB, [1 - x for x in Q])], n,
                rowh=52, shade=shades(C), edges=edge_list(C), vals=False)
    ax.text(150, yb + 28, '每个上升沿发生了什么', fontsize=10.5, weight='bold', color=GREEN)
    table(ax, 150, yb + 42, [120, 130, 130, 130, 130, 130, 200], 26, rows_e, fs=9, hl={i for i, r in enumerate(rows_e) if r[-1] == '翻转'})
    para(ax, 150, yb + 42 + 26 * 5 + 16, '注意第 1 个 T 脉冲：它正好“盖住”第 1 个上升沿，所以有效。第 2 个上升沿时 T 已经回到 0 → 保持。T 在两个边沿之间升起又落下（没盖住任何边沿）则完全无效。', 960, 9.2)
    # 真值表
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '特性表（T、Q → 下一个 Q）+ 中间线 S、R 的推导。只在有效（上升）边沿生效。', legend=False)
    cv = CV(ax, 70, 175, 1.1); cv.mono = True
    draw_t(cv, dict(T=0, C=0, S=0, R=0, Q=0, Qb=0))
    para(ax, 46, 370, 'S = T·%s     R = T·Q\n特征方程：$Q_{T+1}$ = T ⊕ $Q_T$ = T·%s + %s·Q\n\nT=0：S=R=0 → SR 保持。\nT=1：Q=0 时 S=1（置位成 1）；Q=1 时 R=1（复位成 0）→ 总是变成相反值。\nQ 与 %s 互补 → S、R 不可能同时为 1 → 没有禁止态。'
         % (QB, QB, ov('T'), QB), 360, 9.5, 1.7)
    table(ax, 440, 118, [40, 46, 60, 60, 60, 70, 347], [26] + [42] * 4,
          [['T', QT, 'S=T·%s' % QB, 'R=T·Q', QN, '动作', '为什么'],
           ['0', '0', '0', '0', '0', '保持', 'T=0 → 两个 AND 都被关掉 → S=R=0 → SR 触发器保持原值 0。'],
           ['0', '1', '0', '0', '1', '保持', '同上，保持原值 1。T=0 时来多少个边沿都不变。'],
           ['1', '0', '1', '0', '1', '翻转', 'Q=0 → %s=1 → S=1·1=1，R=1·0=0 → 置位 → Q 变 1。' % QB],
           ['1', '1', '0', '1', '0', '翻转', 'Q=1 → R=1·1=1，S=1·0=0 → 复位 → Q 变 0。']], left={6}, fs=8.8, hl={(3, 4), (4, 4)})
    ax.text(440, 344, '简化成两行（背这个）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 360, [80, 120, 200], 26, [['T', QN, '说明'], ['0', QT, '保持'], ['1', r'$\overline{Q}_T$', '翻转 (toggle)']], fs=9)
    ax.text(880, 344, '激励表（设计电路时用）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 880, 360, [120, 100], 26, [['%s → %s' % (QT, QN), 'T'], ['0 → 0', '0'], ['0 → 1', '1'], ['1 → 0', '1'], ['1 → 1', '0']], fs=9)
    ax.text(440, 520, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 536, [220, 180, 283], 30,
          [['发生了什么', 'Q 的反应', '说明'],
           ['上升沿到来，T=1', '翻转', '0→1 或 1→0；%s 同时翻转' % QB],
           ['上升沿到来，T=0', '不变', '保持'],
           ['两个上升沿之间 T 0→1→0', '不变', '没盖住任何边沿的 T 脉冲无效'],
           ['T 一直是 1', '每个时钟周期翻一次', 'Q 的周期 = 时钟的 2 倍 → 二分频'],
           ['连续 n 个上升沿 T 都是 1', 'n 为奇数取反，偶数不变', '数翻转次数就行'],
           ['Q 初值未知', '一直未知', '翻转一个未知值还是未知 → 必须先 reset']], left={2}, fs=8.8)
    notes = [
        '一句话：T=1 时每个有效边沿翻转一次，T=0 时保持。特征方程 $Q_{T+1}$ = T ⊕ $Q_T$。',
        '课件电路是“两个 AND + SR 触发器”：S=T·%s、R=T·Q。也可以看成 D 触发器 + 异或门（D=T⊕Q），或者 JK 触发器把 J、K 接在一起（J=K=T）。三种画法功能相同。' % QB,
        'T 只在有效边沿被采样。画图时先画所有上升沿的竖线，在每条线上看 T（边沿前的值）：是 1 就翻，是 0 就平。',
        '两个边沿之间的 T 变化全部忽略。课件波形里第一个 T 脉冲之所以有效，是因为它跨过了第 1 个上升沿。',
        '为什么 T=1 时不会在一个时钟里疯狂翻转？因为是边沿触发，每个边沿只采样一次。Q 变化后 S、R 立刻互换，但要等下一个边沿才起作用。如果用锁存器，C=1 期间就会振荡。',
        'S 和 R 永远不会同时为 1（Q、%s 互补，两个 AND 最多一个出 1）→ 这里的 SR 触发器不会进入禁止态。' % QB,
        'T 触发器没有“直接写入某个值”的输入：上电未知时，翻转或保持都还是未知。所以题目一定会给初值（通常 Q=0）或 reset；没给就先写明你的假设。',
        'T 恒为 1 → Q 每个周期翻一次 → Q 的频率是时钟的一半（二分频）。把多个这样的触发器串起来就是计数器。',
        '%s 和 Q 同时翻转，始终互补。别忘了画。' % QB,
        '课件符号里时钟端是三角形 → 上升沿触发。如果题目的符号有小圆圈，则改成在下降沿翻转，其余完全一样。',
        '快速验算：数一数“T=1 的有效边沿”有几个。奇数个 → 最后的 Q 和初值相反；偶数个 → 相同。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clock、T 波形画 Q）', [
            '确认触发边沿（课件：上升沿）和 Q 的初值。',
            '把所有上升沿画成竖虚线。',
            '逐条虚线看“边沿前”的 T：T=1 → Q 翻转；T=0 → Q 不变。',
            '两条虚线之间 Q 一律水平。',
            '%s = Q 取反。' % QB,
            '若要画 S、R：S=T·%s，R=T·Q，它们随 T 和 Q 即时变化。' % QB])
        ax.text(x, y + 6, 'T=1 恒定：二分频', fontsize=11, weight='bold', color=GREEN, va='top')
        n = 32; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]; Q = []; q = 0
        for i in range(n):
            if i and C[i] == 1 and C[i - 1] == 0:
                q ^= 1
            Q.append(q)
        timing(ax, x + 44, y + 40, w - 50, [('Clock', C), ('Q', Q)], n, rowh=38, vals=False, fs=9, lw=2, edges=edge_list(C))
        para(ax, x, y + 130, 'Q 的一个周期 = 2 个时钟周期。\n再接一级（用上一级的输出当时钟）就是四分频…… 这就是计数器的来源。', w, 8.8, 1.55, '#333')
        ax.text(x, y + 196, '三种等价实现', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 220, [150, 224], 26, [['用什么搭', '接法'], ['SR 触发器（课件）', 'S = T·%s，R = T·Q' % QB], ['D 触发器', 'D = T ⊕ Q'], ['JK 触发器', 'J = K = T']], fs=8.8)
    notes_page(doc, '3. 满分注意事项：T 触发器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 07 JK 触发器 =================
def ff_front(cv, v, chg, top_in, bot_in):
    """JK 和 带使能 D 触发器共用的前半截：两个 AND → OR → D 触发器。"""
    big = cv.sc > 0.9
    a1, a2, o = cv.gate('and', 75, -10, 30), cv.gate('and', 75, 50, 30), cv.gate('or', 142, 20, 30)
    cv.block(212, 0, 70, 110, title='D 触发器', pins=[('D', 12, 20), ('Q', 58, 20), (QB, 58, 90)], clk=75, fs=10 if big else 7.6)
    cv.wire([a1['o'], (122, -10), (122, 12.5), o['a']], v['a']); cv.wire([a2['o'], (122, 50), (122, 27.5), o['b']], v['b'])
    cv.wire([o['o'], (212, 20)], v[top_in])
    cv.wire([(282, 20), (352, 20)], v['Q']); cv.wire([(282, 90), (352, 90)], v['Qb'])
    cv.label(362, 20, 'Q', fs=11 if big else 9); cv.label(362, 90, QB, fs=11 if big else 9)
    B(cv, 116, -25, 'a', v, 'a', chg); B(cv, 116, 65, 'b', v, 'b', chg)
    B(cv, 300, 7, 'Q', v, 'Q', chg); B(cv, 300, 103, QB, v, 'Qb', chg)


def draw_jk(cv, v, chg=()):
    ff_front(cv, v, chg, 'D', None); fl = 11 if cv.sc > 0.9 else 9
    inv = cv.gate('not', 22, 42.5, 15)
    cv.wire([(0, -2.5), (75, -2.5)], v['J']); cv.wire([(0, 42.5), (22, 42.5)], v['K']); cv.wire([inv['o'], (75, 42.5)], v['Kb'])
    cv.wire([(0, 114), (192, 114), (192, 75), (212, 75)], v['C'])
    cv.wire([(336, 90), (336, -42), (64, -42), (64, -17.5), (75, -17.5)], v['Qb']); cv.dot(336, 90, v['Qb'])
    cv.wire([(320, 20), (320, 134), (64, 134), (64, 57.5), (75, 57.5)], v['Q']); cv.dot(320, 20, v['Q'])
    cv.label(-10, -2.5, 'J', fs=fl); cv.label(-10, 42.5, 'K', fs=fl); cv.label(-10, 114, 'C', fs=fl)
    B(cv, 30, -15, 'J', v, 'J', chg); B(cv, 8, 56, 'K', v, 'K', chg); B(cv, 54, 30, KB, v, 'Kb', chg)
    B(cv, 192, 6, 'D', v, 'D', chg); B(cv, 120, 102, 'C', v, 'C', chg)


def jk_state(J, K, q, C=0):
    Kb = NOT(K); a, b = AND(J, NOT(q)), AND(Kb, q)
    return dict(J=J, K=K, Kb=Kb, a=a, b=b, D=OR(a, b), C=C, Q=q, Qb=NOT(q))


def pdf_jk():
    doc = Doc(os.path.join(OUT, '07_JK触发器.pdf'), 'JK 触发器 · JK Flip-Flop')
    combos = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    seq = [jk_state(*c) for c in combos]
    act = {(0, 0): '保持', (0, 1): '复位', (1, 0): '置位', (1, 1): '翻转'}
    why = [
        'a=J·%s=0，b=%s·Q=1·0=0 → D=0=旧 Q。上升沿把 0 再写一遍 → 保持。' % (QB, KB),
        'b=%s·Q=1·1=1 → D=1=旧 Q。上升沿把 1 再写一遍 → 保持。' % KB,
        'J=0 → a=0；Q=0 → b=0 → D=0。本来就是 0，复位后还是 0。',
        'K=1 → %s=0 → b=0；J=0 → a=0 → D=0。上升沿后 Q 从 1 变 0。' % KB,
        'a=J·%s=1·1=1 → D=1。上升沿后 Q 从 0 变 1。' % QB,
        'a=J·%s=1·0=0，b=%s·Q=1·1=1 → D=1。本来就是 1，置位后还是 1。' % (QB, KB),
        'a=J·%s=1 → D=1 = 旧 Q 的相反值。上升沿后 Q 从 0 翻成 1。' % QB,
        'a=1·0=0，b=%s·Q=0·1=0 → D=0 = 旧 Q 的相反值。上升沿后 Q 从 1 翻成 0。' % KB,
    ]
    items = [('%d. JK=%d%d, Q=%d → %s后 Q=%s（%s）' % (i + 1, J, K, q, UP, sv(seq[i]['D']), act[(J, K)]), why[i]) for i, (J, K, q) in enumerate(combos)]
    panels(doc, '1. JK 触发器：8 种情况（4 种功能 × Q 的两种旧值）',
           '课件电路：D = J·%s + %s·Q 接到正边沿 D 触发器。每格画的是“上升沿到来之前”的瞬间；黄框的 D 就是上升沿之后 Q 的新值。a = J·%s，b = %s·Q。' % (QB, KB, QB, KB),
           items, seq, draw_jk, 2, 1.12, (70, 152), chs=[{'D'}] * 8, per=4)
    # 时序图
    ax = doc.page('1. JK 触发器时序图', '浅橙 = CLK=1；黄色虚线 = 上升沿。每条虚线下面标出了边沿前的 JK 和对应的动作。')
    jk = [(0, 0), (1, 0), (0, 0), (0, 1), (1, 1), (1, 1), (0, 0), (1, 0), (1, 1), (0, 1)]
    n = 42; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]
    J = [jk[min((i + 1) // 4, 9)][0] for i in range(n)]
    K = [jk[min((i + 1) // 4, 9)][1] for i in range(n)]
    Q, Dd, q = [], [], 0
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            q = Dd[i - 1]
        Q.append(q); Dd.append((J[i] & (1 - q)) | ((1 - K[i]) & q))
    x0, w = 150, 970
    yb = timing(ax, x0, 150, w, [('CLK', C), ('J', J), ('K', K), ('D=J·%s+%s·Q' % (QB, KB), Dd), ('Q', Q), (QB, [1 - x for x in Q])], n,
                rowh=56, shade=shades(C), edges=edge_list(C), vals=False, fs=9.5)
    for i, e in edge_list(C):
        j, k = J[i - 1], K[i - 1]
        ax.text(x0 + i * w / n, yb + 16, 'JK=%d%d\n%s' % (j, k, act[(j, k)]), fontsize=7.8, color='#B07900', ha='center', va='center', linespacing=1.3)
    bullets(ax, 70, yb + 60, [
        '每条虚线上读边沿前的 J、K：00 → Q 画平；01 → Q 变 0；10 → Q 变 1；11 → Q 取反。',
        'D 这条中间线随 J、K、Q 即时变化（Q 一变，D 立刻跟着变），但只有“下一个上升沿前一瞬间”的 D 会被写进 Q。',
        '连续两个 11（第 5、6 条虚线）→ 翻转两次，回到原值。假设初值 Q=0。'], 1000, fs=9.3, mark='•')
    # 真值表
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '完整 8 行（J、K、$Q_T$ → 中间线 → $Q_{T+1}$）。只在上升沿生效。', legend=False)
    cv = CV(ax, 60, 175, 0.88); cv.mono = True
    draw_jk(cv, jk_state(0, 0, 0))
    para(ax, 46, 345, 'a = J·%s     b = %s·Q     D = a + b\n特征方程：$Q_{T+1}$ = J·%s + %s·$Q_T$\n\n理解：Q=0 时 b 一定是 0 → 只看 J（J=1 就变 1）。\nQ=1 时 a 一定是 0 → 只看 K（K=1 就变 0）。\n所以 J=K=1：0→1、1→0，就是翻转。'
         % (QB, KB, QB, KB), 360, 9.5, 1.7)
    rows = [['J', 'K', QT, KB, 'a=J·%s' % QB, 'b=%s·Q' % KB, 'D', QN, '功能', '为什么']]
    short = ['J=0 不置位、K=0 不复位：D 等于旧 Q', '同上：b=1 把旧的 1 送回 D', '已经是 0，K=1 只是确认', 'K=1 → %s=0 → b=0，没有东西让 D 为 1' % KB,
             'J=1 且 %s=1 → a=1 → D=1' % QB, '已经是 1，靠 b=%s·Q=1 维持' % KB, 'Q=0 时只看 J：J=1 → 变 1', 'Q=1 时只看 K：K=1 → 变 0']
    for (J_, K_, q_), s, sh in zip(combos, seq, short):
        rows.append([J_, K_, q_, s['Kb'], s['a'], s['b'], s['D'], s['D'], act[(J_, K_)], sh])
    table(ax, 440, 118, [30, 30, 40, 30, 62, 62, 34, 46, 50, 299], 30, rows, left={9}, fs=8.8, hl={(i, 7) for i in range(1, 9)})
    ax.text(440, 420, '简化成四行（背这个）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 436, [40, 40, 70, 150], 26, [['J', 'K', QN, '功能'], ['0', '0', QT, '保持 maintain'], ['0', '1', '0', '复位 reset'],
                                                ['1', '0', '1', '置位 set'], ['1', '1', r'$\overline{Q}_T$', '翻转 toggle']], fs=9)
    ax.text(790, 420, '激励表（设计电路时用，X = 无所谓）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 790, 436, [120, 60, 60], 26, [['%s → %s' % (QT, QN), 'J', 'K'], ['0 → 0', '0', 'X'], ['0 → 1', '1', 'X'], ['1 → 0', 'X', '1'], ['1 → 1', 'X', '0']], fs=9)
    para(ax, 440, 590, '激励表怎么来的：Q=0 时只看 J（K 无所谓）；Q=1 时只看 K（J 无所谓）。\n例如 0→1：必须 J=1，K 是 0（置位）或 1（翻转）都行 → K=X。', 680, 9.2, 1.7)
    notes = [
        '四种功能背熟：JK=00 保持、01 复位(Q=0)、10 置位(Q=1)、11 翻转。J 像 S（置位），K 像 R（复位）。',
        '和 SR 的唯一区别：11 不再是禁止态，而是翻转。所以 JK“用上了两个输入的全部四种组合”（课件原话）。',
        '特征方程 $Q_{T+1}$ = J·%s + %s·$Q_T$。课件的电路就是把这个式子用 2 个 AND + 1 个 OR + 1 个非门接到 D 触发器的 D 上。' % (QB, KB),
        '注意 K 要先取反：下面那个 AND 的输入是 %s 和 Q，不是 K 和 Q。画中间线时最容易漏掉这个非门。' % KB,
        '反馈接法：上面的 AND 接 %s（和 J 配），下面的 AND 接 Q（和 %s 配）。口诀：J 配 %s，K 配 Q。' % (QB, KB, QB),
        '只在有效边沿（课件：上升沿，时钟端三角形）更新。J、K 取边沿前的值；边沿之间它们怎么变都不影响 Q。',
        'Q 一变，D 会立刻跟着变（因为反馈），但 D 的新值要到下一个上升沿才被采样——所以 11 时每个边沿只翻一次。',
        'JK 可以变成别的触发器：J=K=T → T 触发器；J=D、K=%s → D 触发器。反过来考“用 JK 实现 xxx”就这样接。' % DB,
        '初值未知时：01、10 能把 Q 变成确定值；00（保持）和 11（翻转）仍然未知。',
        '激励表里有 X（don\'t care），设计时序电路时可以用来化简。0→1 是 J=1,K=X；1→0 是 J=X,K=1。',
        '快速理解：Q=0 时只有 J 说了算；Q=1 时只有 K 说了算。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 CLK、J、K 波形画 Q）', [
            '确认触发边沿和 Q 的初值。',
            '把所有上升沿画成竖虚线。',
            '每条虚线上读边沿前的 J、K，在线下写 00/01/10/11。',
            '00 → 平；01 → 0；10 → 1；11 → 取反。',
            '虚线之间 Q 水平。%s = Q 取反。' % QB,
            '如果要画 D：D = J·%s + %s·Q，逐段算。' % (QB, KB)])
        ax.text(x, y + 6, 'SR / JK / D / T 对照', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [70, 152, 152], 26,
              [['触发器', '特征方程', '特点'], ['SR', 'S + %s·Q' % RB, '11 禁止'], ['JK', 'J·%s + %s·Q' % (QB, KB), '11 翻转'],
               ['D', 'D', '直接写入'], ['T', 'T ⊕ Q', '1 翻转 / 0 保持']], fs=8.8)
        ax.text(x, y + 190, 'JK 变身', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 214, [120, 254], 26, [['想要', 'J、K 怎么接'], ['T 触发器', 'J = K = T'], ['D 触发器', 'J = D，K = %s' % DB],
                                               ['SR 触发器', 'J = S，K = R（别给 11）']], fs=8.8)
    notes_page(doc, '3. 满分注意事项：JK 触发器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 08 带使能端的 D 触发器 =================
def draw_en(cv, v, chg=()):
    ff_front(cv, v, chg, 'Din', None); fl = 11 if cv.sc > 0.9 else 9
    inv = cv.gate('not', 32, -2.5, 15)
    cv.wire([(0, -2.5), (32, -2.5)], v['EN']); cv.dot(16, -2.5, v['EN']); cv.wire([(16, -2.5), (16, 42.5), (75, 42.5)], v['EN'])
    cv.wire([inv['o'], (75, -2.5)], v['ENb']); cv.wire([(0, 57.5), (75, 57.5)], v['D'])
    cv.wire([(168, 75), (212, 75)], v['C'])
    cv.wire([(326, 20), (326, -42), (64, -42), (64, -17.5), (75, -17.5)], v['Q']); cv.dot(326, 20, v['Q'])
    cv.label(-14, -2.5, 'EN', fs=fl); cv.label(-10, 57.5, 'D', fs=fl); cv.label(152, 75, 'Clk', fs=fl - 1)
    B(cv, 8, -19, 'EN', v, 'EN', chg); B(cv, 56, 16, ENB, v, 'ENb', chg); B(cv, 36, 71, 'D', v, 'D', chg)
    B(cv, 188, 5, 'Din', v, 'Din', chg); B(cv, 188, 90, 'Clk', v, 'C', chg)


def sim_en(steps, q=0):
    out, pc, din = [], None, None
    for C, EN, D in steps:
        if pc == 0 and C == 1:
            q = din
        ENb = NOT(EN); a, b = AND(ENb, q), AND(EN, D); din = OR(a, b)
        out.append(dict(C=C, EN=EN, ENb=ENb, D=D, a=a, b=b, Din=din, Q=q, Qb=NOT(q))); pc = C
    return out


def pdf_en():
    doc = Doc(os.path.join(OUT, '08_带使能端的D触发器.pdf'), '带使能端的 D 触发器 · D flip-flop with enable')
    seq = sim_en([(0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)])
    items = [
        ('1. EN=0, D=1, Q=0（边沿前）', '%s=1 → 上面的 AND 选通 Q：a=1·Q=0。下面的 AND 被 EN=0 关掉：b=0。Din=a+b=0 —— 就是旧的 Q。' % ENB),
        ('2. 上升沿：Q 保持 0', '触发器照常在边沿采样，但采到的 Din 是自己的旧值 → Q 不变。外面的 D=1 被无视。'),
        ('3. EN 变 1：选通 D', '%s=0 → a=0；EN=1 → b=1·D=1 → Din=1。新数据已经到了触发器门口，等边沿。' % ENB),
        ('4. 上升沿：装入 D，Q=1', '采到 Din=1 → Q=1。EN=1 时它就是一个普通的 D 触发器。'),
        ('5. EN 变 0，D 变 0', 'a=%s·Q=1·1=1，b=0 → Din=1（旧 Q）。D 变成什么都进不来。' % ENB),
        ('6. 上升沿：Q 保持 1', '采到的还是自己 → Q=1。EN=0 时来多少个边沿都保持。'),
        ('7. EN 变 1（D=0）', 'a=0，b=1·0=0 → Din=0。'),
        ('8. 上升沿：装入 0，Q=0', '采到 Din=0 → Q=0。'),
    ]
    panels(doc, '1. 带使能端的 D 触发器：8 步逐线图解',
           '课件电路：一个 2 选 1 —— a = %s·Q（把旧值绕回来），b = EN·D（放新值进来），Din = a + b 接正边沿 D 触发器。EN=1 装入 D；EN=0 保持。（假设初值 Q=0）' % ENB,
           items, seq, draw_en, 2, 1.12, (74, 152), per=4)
    ax = doc.page('1. 带使能端的 D 触发器时序图', '浅橙 = Clk=1；黄色虚线 = 上升沿。只有“上升沿那一刻 EN=1”才会把 D 装进 Q。')
    n = 26; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]
    D = [1] * 8 + [0] * 12 + [1] * 6
    EN = [0] * 5 + [1] * 3 + [0] * 3 + [1] * 2 + [0] * 4 + [1] * 4 + [0] * 5
    Q, Din, q = [], [], 0
    rows_e = [['上升沿', 'EN（边沿前）', 'D（边沿前）', 'Din', 'Q（边沿后）', '说明']]
    k = 0
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            k += 1; old = q; q = Din[i - 1]
            rows_e.append(['第 %d 个 ↑' % k, EN[i - 1], D[i - 1], Din[i - 1], q, ('装入 D' if EN[i - 1] else '保持（EN=0）')])
        Q.append(q); Din.append(D[i] if EN[i] else q)
    rows_e[4][-1] = '保持：EN 的脉冲没盖住边沿'; rows_e[6][-1] = '保持：EN 在边沿前刚好回到 0'
    yb = timing(ax, 150, 150, 970, [('Clk', C), ('EN', EN), ('D', D), ('Din', Din), ('Q', Q)], n, rowh=54, shade=shades(C), edges=edge_list(C), vals=False)
    ax.text(150, yb + 28, '每个上升沿发生了什么', fontsize=10.5, weight='bold', color=GREEN)
    table(ax, 150, yb + 42, [110, 130, 130, 110, 130, 360], 26, rows_e, fs=9, hl={i for i, r in enumerate(rows_e) if '装入' in str(r[-1])})
    para(ax, 150, yb + 42 + 26 * 7 + 14, 'Din 这条线：EN=1 的时候等于 D，EN=0 的时候等于 Q。Q 永远在上升沿变成“边沿前的 Din”。', 960, 9.2)
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', 'EN、D、$Q_T$ → 中间线 → $Q_{T+1}$。只在上升沿生效。', legend=False)
    cv = CV(ax, 64, 175, 0.88); cv.mono = True
    draw_en(cv, dict(EN=0, ENb=0, D=0, a=0, b=0, Din=0, C=0, Q=0, Qb=0))
    para(ax, 46, 345, 'a = %s·Q     b = EN·D     Din = a + b\n特征方程：$Q_{T+1}$ = EN·D + %s·$Q_T$\n\n这就是一个 2 选 1 多路选择器（MUX）：\nEN=0 选 Q（自己绕回来）→ 保持；\nEN=1 选 D → 装入新值。\n时钟线没有被改动，触发器每个上升沿都在“写”，只是 EN=0 时写的是自己。'
         % (ENB, ENB), 360, 9.5, 1.7)
    rows = [['EN', 'D', QT, ENB, 'a=%s·Q' % ENB, 'b=EN·D', 'Din', QN, '功能', '为什么']]
    for EN_, D_, q_ in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
        a_, b_ = (1 - EN_) & q_, EN_ & D_
        rows.append([EN_, D_, q_, 1 - EN_, a_, b_, a_ | b_, a_ | b_, '装入' if EN_ else '保持',
                     ('b=D，a=0 → Din=D，旧 Q 被丢掉' if EN_ else 'b=0（D 被挡），a=Q → Din=旧 Q')])
    table(ax, 440, 118, [34, 30, 40, 34, 70, 66, 40, 46, 50, 273], 30, rows, left={9}, fs=8.8, hl={(i, 7) for i in range(1, 9)})
    ax.text(440, 420, '简化（背这个）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 436, [60, 60, 60, 80, 200], 26, [['Clk', 'EN', 'D', QN, '功能'], [UP, '0', 'X', QT, '保持'], [UP, '1', '0', '0', '装入 D'],
                                                   [UP, '1', '1', '1', '装入 D'], ['不是 ↑', 'X', 'X', QT, '保持']], fs=9)
    ax.text(440, 590, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 606, [260, 120, 303], 28,
          [['发生了什么', 'Q 的反应', '说明'],
           ['上升沿时 EN=1', '变成 D', '和普通 D 触发器一样'],
           ['上升沿时 EN=0', '不变', 'D 是什么都无所谓'],
           ['两个上升沿之间 EN 0→1→0', '不变', 'EN 也只在边沿被“看”一次'],
           ['EN=1 但没有上升沿', '不变', 'EN 不是锁存器的 C，不会让 Q “透明”']], left={2}, fs=8.8)
    notes = [
        '功能：上升沿到来时，EN=1 → Q 变成 D；EN=0 → Q 不变。其它时刻 Q 永远不变。',
        '特征方程 $Q_{T+1}$ = EN·D + %s·$Q_T$。看到这个式子就要认出它是“2 选 1 MUX + D 触发器”。' % ENB,
        '课件电路：上面的 AND 接 %s 和 Q（反馈），下面的 AND 接 EN 和 D，OR 的输出进 D 触发器。EN 先分叉：一路过非门去上面，一路直接去下面。' % ENB,
        'EN 和 D 一样，只在有效边沿被采样。EN 在两个边沿之间拉高又放下 → 什么都没装进去（最常见的陷阱）。',
        'EN=1 不等于“透明”。它不是 D 锁存器的 C：就算 EN 一直是 1，Q 也只在上升沿更新。',
        '保持不是因为“时钟被挡住”，而是因为把 Q 自己又写回去了。不要画成用 AND 门把 EN 和 Clk 与起来（门控时钟会产生毛刺和时钟偏移，课件不是这种做法）。',
        '画中间线 Din：EN=1 的区间抄 D，EN=0 的区间抄 Q。然后 Q 在每个上升沿取 Din 的边沿前值。',
        '初值未知且 EN=0 → 一直未知；必须有一次 EN=1 的上升沿（或 reset）才确定。',
        '符号：方框里 D、EN 两个输入 + 时钟三角形。有的书把 EN 写成 CE / LD / WE / Load / Write。',
        '用途：load register 的每一位都是它；所有位的 EN 接同一根 Write 线，就能“想写才写，不写就一直存着”。',
        '没有使能端的 D 触发器每个上升沿都会装入 D，所以不能“记住旧值超过一个周期”——这就是为什么需要 EN。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clk、EN、D 波形画 Q）', [
            '把所有上升沿画成竖虚线。',
            '每条虚线上先看边沿前的 EN。',
            'EN=0 → Q 不变，直接画平，跳到下一条。',
            'EN=1 → 再看边沿前的 D，Q 变成这个值。',
            '虚线之间 Q 水平。第一次装入之前按题目给的初值（没给就是未知）。'])
        ax.text(x, y + 6, '三个“看起来像”的东西', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [110, 132, 132], [26, 40, 40, 40],
              [['器件', '什么时候 Q 能变', '变成什么'], ['D 锁存器', 'C=1 的整段时间', '一直跟随 D'], ['D 触发器', '每个上升沿', '边沿前的 D'],
               ['带 EN 的 D 触发器', 'EN=1 的上升沿', '边沿前的 D']], fs=8.8)
        ax.text(x, y + 200, '等价的 MUX 画法', fontsize=11, weight='bold', color=GREEN, va='top')
        cv = CV(ax, x + 90, y + 262, 1.0)
        ax.add_patch(Polygon([cv.P(0, 0), cv.P(34, 14), cv.P(34, 66), cv.P(0, 80)], closed=True, fc='white', ec='#222', lw=1.5, zorder=5))
        cv.label(11, 22, '0', fs=8, weight='normal'); cv.label(11, 58, '1', fs=8, weight='normal')
        cv.block(90, 5, 60, 80, pins=[('D', 10, 18), ('Q', 50, 18)], clk=60, fs=8.5)
        for pts in ([(-40, 58), (0, 58)], [(34, 40), (62, 40), (62, 23), (90, 23)], [(150, 23), (200, 23)], [(175, 23), (175, -22), (-22, -22), (-22, 22), (0, 22)],
                    [(17, 100), (17, 73)], [(60, 65), (90, 65)]):
            cv.wire(pts, 0, c='#333', lw=1.6)
        cv.dot(175, 23, 0, c='#333'); cv.label(-50, 58, 'D', fs=9); cv.label(17, 110, 'EN', fs=9); cv.label(72, 78, 'Clk', fs=8.5); cv.label(210, 23, 'Q', fs=9)
    notes_page(doc, '3. 满分注意事项：带使能端的 D 触发器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


if __name__ == '__main__':
    pdf_dff(); pdf_t(); pdf_jk(); pdf_en()
    print('ok')
