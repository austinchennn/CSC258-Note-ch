# -*- coding: utf-8 -*-
"""01 SR 锁存器(NOR)  02 S̄R̄ 锁存器(NAND)  03 Clocked SR 锁存器  04 D 锁存器
电路画法全部按课件 flipflops_slides.pdf。所有线上的值由门级仿真算出，不是手填。"""
import os
from lib import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
QB = ov('Q'); SB = ov('S'); RB = ov('R'); DB = ov('D')
QT, QBT, QN, QBN = '$Q_T$', r'$\overline{Q}_T$', '$Q_{T+1}$', r'$\overline{Q}_{T+1}$'
DY = 96


# ================= 画电路 =================
def draw_sr(kind):
    top, bot, tl, bl = ('R', 'S', 'R', 'S') if kind == 'nor' else ('Sb', 'Rb', SB, RB)

    def f(cv, v, chg=()):
        g1, g2, xe = latch(cv, kind, 52, 0, v[top], v[bot], v['Q'], v['Qb'], DY)
        cv.wire([(0, -9), g1['a']], v[top]); cv.wire([(0, DY + 9), g2['b']], v[bot])
        cv.label(-10, -9, tl); cv.label(-10, DY + 9, bl); cv.label(xe + 11, 0, 'Q'); cv.label(xe + 11, DY, QB)
        cv.badge(22, -24, '%s=%s' % (tl, sv(v[top])), v[top], top in chg)
        cv.badge(22, DY + 24, '%s=%s' % (bl, sv(v[bot])), v[bot], bot in chg)
        cv.badge(xe - 18, -16, 'Q=%s' % sv(v['Q']), v['Q'], 'Q' in chg)
        cv.badge(xe - 18, DY + 16, '%s=%s' % (QB, sv(v['Qb'])), v['Qb'], 'Qb' in chg)
    return f


def draw_csr(cv, v, chg=()):
    n1, n2 = cv.gate('nand', 0, -9), cv.gate('nand', 0, DY + 9)
    g1, g2, xe = latch(cv, 'nand', 92, 0, v['a'], v['b'], v['Q'], v['Qb'], DY)
    cv.wire([(-45, -18), (0, -18)], v['S']); cv.wire([(-45, DY + 18), (0, DY + 18)], v['R'])
    cv.wire([(-45, DY / 2), (-18, DY / 2)], v['C']); cv.wire([(0, 0), (-18, 0), (-18, DY), (0, DY)], v['C']); cv.dot(-18, DY / 2, v['C'])
    cv.wire([n1['o'], g1['a']], v['a']); cv.wire([n2['o'], g2['b']], v['b'])
    for t, y in (('S', -18), ('C', DY / 2), ('R', DY + 18)):
        cv.label(-54, y, t)
    cv.label(xe + 11, 0, 'Q'); cv.label(xe + 11, DY, QB)
    cv.badge(-27, -32, 'S=%s' % sv(v['S']), v['S'], 'S' in chg); cv.badge(-27, DY + 32, 'R=%s' % sv(v['R']), v['R'], 'R' in chg)
    cv.badge(7, DY / 2, 'C=%s' % sv(v['C']), v['C'], 'C' in chg)
    cv.badge(66, -24, 'a=%s' % sv(v['a']), v['a'], 'a' in chg); cv.badge(66, DY + 24, 'b=%s' % sv(v['b']), v['b'], 'b' in chg)
    cv.badge(xe - 18, -16, 'Q=%s' % sv(v['Q']), v['Q'], 'Q' in chg)
    cv.badge(xe - 18, DY + 16, '%s=%s' % (QB, sv(v['Qb'])), v['Qb'], 'Qb' in chg)
    if cv.mono:
        cv.label(66, -22, 'a', fs=9, color=GREEN); cv.label(66, DY + 22, 'b', fs=9, color=GREEN)


def draw_dl(cv, v, chg=()):
    n1, n2 = cv.gate('nand', 0, -9), cv.gate('nand', 0, DY + 9)
    g1, g2, xe = latch(cv, 'nand', 92, 0, v['a'], v['b'], v['Q'], v['Qb'], DY)
    inv = cv.gate('not', -40, DY + 18, 16)
    cv.wire([(-64, -18), (0, -18)], v['D']); cv.wire([(-52, -18), (-52, DY + 18), (-40, DY + 18)], v['D']); cv.dot(-52, -18, v['D'])
    cv.wire([inv['o'], (0, DY + 18)], v['Db'])
    cv.wire([(-30, DY / 2), (-14, DY / 2)], v['C']); cv.wire([(0, 0), (-14, 0), (-14, DY), (0, DY)], v['C']); cv.dot(-14, DY / 2, v['C'])
    cv.wire([n1['o'], g1['a']], v['a']); cv.wire([n2['o'], g2['b']], v['b'])
    cv.label(-73, -18, 'D'); cv.label(-38, DY / 2, 'C'); cv.label(xe + 11, 0, 'Q'); cv.label(xe + 11, DY, QB)
    cv.badge(-30, -32, 'D=%s' % sv(v['D']), v['D'], 'D' in chg)
    cv.badge(-22, DY + 39, '%s=%s' % (DB, sv(v['Db'])), v['Db'], 'Db' in chg)
    cv.badge(10, DY / 2, 'C=%s' % sv(v['C']), v['C'], 'C' in chg)
    cv.badge(66, -24, 'a=%s' % sv(v['a']), v['a'], 'a' in chg); cv.badge(66, DY + 24, 'b=%s' % sv(v['b']), v['b'], 'b' in chg)
    cv.badge(xe - 18, -16, 'Q=%s' % sv(v['Q']), v['Q'], 'Q' in chg)
    cv.badge(xe - 18, DY + 16, '%s=%s' % (QB, sv(v['Qb'])), v['Qb'], 'Qb' in chg)
    if cv.mono:
        cv.label(66, -22, 'a', fs=9, color=GREEN); cv.label(66, DY + 22, 'b', fs=9, color=GREEN)


# ================= 仿真 =================
def sim_sr(kind, steps):
    q = qb = None; out = []
    for a, b in steps:
        if kind == 'nor':   # a=S, b=R；课件：R 在上(出 Q)，S 在下(出 Q̄)
            q, qb = settle(NOR, b, a, q, qb); out.append(dict(S=a, R=b, Q=q, Qb=qb))
        else:               # a=S̄ 在上(出 Q)，b=R̄ 在下
            q, qb = settle(NAND, a, b, q, qb); out.append(dict(Sb=a, Rb=b, Q=q, Qb=qb))
    return out


def sim_csr(steps):
    q = qb = None; out = []
    for C, S, R in steps:
        a, b = NAND(S, C), NAND(R, C); q, qb = settle(NAND, a, b, q, qb)
        out.append(dict(C=C, S=S, R=R, a=a, b=b, Q=q, Qb=qb))
    return out


def sim_dl(steps):
    q = qb = None; out = []
    for C, D in steps:
        Db = NOT(D); a, b = NAND(D, C), NAND(Db, C); q, qb = settle(NAND, a, b, q, qb)
        out.append(dict(C=C, D=D, Db=Db, a=a, b=b, Q=q, Qb=qb))
    return out


# ================= 通用页面 =================
def panels(doc, title, sub, items, seq, draw, cols, sc, off):
    ax = doc.page(title, sub); ch = changes(seq)
    for (x, y, w, h), (t, d), v, c in zip(grid(len(items), cols), items, seq, ch):
        panel(ax, x, y, w, h, t, d)
        draw(CV(ax, x + off[0], y + off[1], sc), v, c)


def timing_page(doc, title, sub, keys, labels, seq, shade=(), note='', extra=None):
    ax = doc.page(title, sub); n = len(seq)
    rows = [(lab, [s[k] for s in seq]) for k, lab in zip(keys, labels)]
    rh = 62 if len(rows) <= 5 else 46
    yb = timing(ax, 105, 150, 1018, rows, n, rowh=rh, heads=[str(i + 1) for i in range(n)], shade=shade)
    ax.text(105, yb + 30, '数值表（黄底 = 和上一格相比发生了变化）', fontsize=9, color=SUB)
    yb = val_table(ax, 105, yb + 44, 1018, keys, labels, seq)
    para(ax, 105, yb + 28, note, 1010, 9.2)
    if extra:
        extra(ax)


def notes_page(doc, title, sub, notes, right):
    ax = doc.page(title, sub, legend=False)
    bullets(ax, 46, 118, notes, 625, fs=9.3, lh=1.55, gap=6)
    box(ax, 715, 112, 410, 680)
    right(ax, 733, 132, 374)
    return ax


def steps_box(ax, x, y, w, title, steps, fs=8.8):
    ax.text(x, y, title, fontsize=11, weight='bold', color=GREEN, va='top')
    return bullets(ax, x, y + 24, steps, w, fs=fs, lh=1.5, gap=4)


# ================= 01 SR 锁存器 (NOR) =================
def pdf_sr_nor():
    doc = Doc(os.path.join(OUT, '01_SR锁存器_NOR版.pdf'), 'SR 锁存器（NOR 版）· SR latch')
    seq = sim_sr('nor', [(1, 0), (0, 0), (0, 1), (0, 0), (1, 1), (0, 0), (0, 1), (1, 1), (0, 1), (0, 0)])
    items = [
        ('1. 置位 Set：S=1, R=0', 'S=1 进下面的 NOR：有 1 出 0 → %s=0。%s=0 绕回上面，上面两个输入 R=0、%s=0 → Q=1。' % (QB, QB, QB)),
        ('2. 保持：S=0, R=0', 'S 撤掉了，但 Q=1 绕回下面的 NOR，仍把 %s 压在 0；%s=0 又让 Q 保持 1 → 记住了 1。' % (QB, QB)),
        ('3. 复位 Reset：R=1', 'R=1 进上面的 NOR → Q=0。Q=0 绕到下面：S=0、Q=0 → %s=1。' % QB),
        ('4. 保持：S=0, R=0', '输入和第 2 格一模一样，但这次记住的是 0 → 00 时输出只取决于历史。'),
        ('5. 禁止：S=1, R=1', '两个 NOR 都有一个输入是 1 → Q=0 且 %s=0。此刻不是未知，是“两个都为 0”（不互补）。' % QB),
        ('6. 同时回到 0,0', '两个门同时看到 0,0 → 同时想变 1 → 又同时变 0……竞争/振荡，最后落在哪边不可预测 → 写 ?。'),
        ('7. 未知时来个复位', '不管之前是什么，R=1 强制 Q=0，再得 %s=1。未知状态被一次 set/reset 清掉。' % QB),
        ('8. 再次进入 1,1', '又是 Q=%s=0（禁止态）。接下来换一种“撤法”。' % QB),
        ('9. 先撤 S（R 还是 1）', '不是同时撤 → 没有竞争。此刻就是 S=0,R=1 → 复位：Q=0、%s=1，结果确定。' % QB),
        ('10. 再撤 R → 保持', '从 0,1 回到 0,0 是普通的保持 → Q=0。结论：后撤的那个输入说了算。'),
    ]
    panels(doc, '1. SR 锁存器（NOR 版）：10 种常考变化', 'NOR 规则：有 1 出 0；全 0 才出 1。课件画法：R 在上面的门（出 Q），S 在下面的门（出 %s）——是交叉的。' % QB,
           items, seq, draw_sr('nor'), 5, 0.93, (26, 168))
    timing_page(doc, '1. SR 锁存器（NOR 版）时序图', '格子编号 = 上一页的 10 种情况。灰色斜线 = 不确定。',
                ['S', 'R', 'Q', 'Qb'], ['S', 'R', 'Q', QB], seq,
                note='读图要点：① S=1→Q=1；R=1→Q=0；S=R=0→保持（看上一格）。② 第 5、8 格 S=R=1 时 Q=%s=0（画成两条都在低位，不是斜线）。'
                     '③ 第 6 格 1,1 同时回 0,0 → 斜线（未知）；第 9→10 格先撤 S 再撤 R → 确定为 0。④ 第 7 格：未知状态下只要来一次 R=1（或 S=1）就重新确定。' % QB)
    # ---- 真值表解析 ----
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '课件原表 + 逐门推导。X = 无所谓（不管之前是什么）。红线划掉的那一行 = 禁止输入。', legend=False)
    cv = CV(ax, 78, 190, 1.35); cv.mono = True
    draw_sr('nor')(cv, dict(S=0, R=0, Q=0, Qb=0))
    para(ax, 46, 385, '上面的门：Q = NOR(R, %s)\n下面的门：%s = NOR(S, Q)\n特征方程：$Q_{T+1}$ = S + %s·$Q_T$（要求 S·R = 0）\n\n口诀：谁是 1，它所在的那个门输出就被压成 0。\nS 压 %s（所以 Q 变 1）；R 压 Q。' % (QB, QB, RB, QB),
         340, 10, 1.75)
    data = [['S', 'R', QT, QBT, QN, QBN, '结果', '为什么（逐门推）'],
            ['0', '0', '0', '1', '0', '1', '保持', '两个外部输入都是 0，NOR 的输出只由反馈决定：%s=1 把 Q 压成 0，Q=0 让 %s 继续为 1 → 原样锁住。' % (QB, QB)],
            ['0', '0', '1', '0', '1', '0', '保持', '同理：Q=1 把 %s 压成 0，%s=0 让 Q 继续为 1。同样的输入、不同的输出 → 这就是“记忆”。' % (QB, QB)],
            ['0', '1', 'X', 'X', '0', '1', '复位', 'R=1 → 上面的 NOR 必出 0 → Q=0。下面的 NOR 输入 S=0、Q=0 → %s=1。与之前的状态无关。' % QB],
            ['1', '0', 'X', 'X', '1', '0', '置位', 'S=1 → 下面的 NOR 必出 0 → %s=0。上面的 NOR 输入 R=0、%s=0 → Q=1。与之前的状态无关。' % (QB, QB)],
            ['1', '1', 'X', 'X', '0', '0', '禁止', '两个 NOR 都有 1 输入 → 两个输出都是 0，Q 与 %s 不再互补；之后若同时回 00 → 不稳定。' % QB]]
    cw = [34, 34, 40, 40, 46, 46, 52, 400]
    yb = table(ax, 432, 118, cw, [26] + [44] * 5, data, left={7}, fs=8.6)
    ax.plot([432, 432 + sum(cw[:-1])], [yb - 22, yb - 22], color='#E03131', lw=2.2, zorder=5)
    ax.text(432, yb + 30, '输入怎么变 → 输出怎么变（考“变化”就考这张）', fontsize=11, weight='bold', color=GREEN)
    data2 = [['S R 从', '变到', 'Q', QB, '说明'],
             ['1 0', '0 0', '1', '0', '记住刚才的置位（课件：remembers previous output when going from 10 or 01 to 00）'],
             ['0 1', '0 0', '0', '1', '记住刚才的复位'],
             ['任意', '1 0 / 0 1', '1 / 0', '0 / 1', '直接置位 / 复位，不看历史（哪怕之前是未知也行）'],
             ['任意', '1 1', '0', '0', '禁止态：两个输出都是 0'],
             ['1 1', '0 0（同时）', '?', '?', '不稳定：结果取决于哪个信号先变 → 写 ? / unknown'],
             ['1 1', '0 1（S 先撤）', '0', '1', 'R 还在 → 复位。之后再回 00 就保持 0'],
             ['1 1', '1 0（R 先撤）', '1', '0', 'S 还在 → 置位。之后再回 00 就保持 1']]
    table(ax, 432, yb + 46, [60, 110, 46, 46, 430], 36, data2, left={4}, fs=8.6, hl={5})

    # ---- 注意事项 ----
    notes = [
        '先认门：课件的 SR latch 是两个 NOR。R 接上面的门（它的输出是 Q），S 接下面的门（它的输出是 %s）。别想当然地认为“S 离 Q 近”。' % QB,
        'NOR 口诀：有 1 出 0，全 0 出 1。所以输入是“高电平有效”：S=1 置位、R=1 复位、00 保持、11 禁止。',
        '00 时的输出取决于“上一格”。填表/画波形遇到 S=R=0，一定回头看前一个状态，不能凭输入直接写。',
        '禁止态 S=R=1 当下的输出是确定的：Q=0、%s=0（两个都是 0）。很多人错写成“未知”。未知出现在 11 → 00 同时撤掉之后。' % QB,
        '11 → 00：课件原话“unstable behaviour … when inputs go from 11 to 00”，输出取决于哪个信号先变。答题写 ? / unknown / unstable。',
        '如果题目明说“S 先回 0”，那就等于先经过 S=0,R=1 → Q=0，然后保持 0；“R 先回 0”则 Q=1。后撤的输入决定结果。',
        '上电初始状态未知（Q=?）。只有给过一次 S=1 或 R=1 之后才有确定值；未知状态下 S=R=0 依旧未知。',
        '输出不是瞬间变（课件 SR latch timing diagram）：S↑ 后先是 %s 掉下去（1 级门延迟），再过 1 级 Q 才升上来；R↑ 则是 Q 先掉、%s 后升。所以 S→Q 要 2 级门延迟，中间有一小段 Q=%s=0。' % (QB, QB, QB),
        'Q 和 %s 两条线都要画/都要填。正常情况下它们互补；只有禁止态时相等。' % QB,
        '对比 NAND 版（%s%s latch）：那边是低电平有效，11 保持、00 禁止且输出都是 1。题目先看是 NOR 还是 NAND，再套表。' % (SB, RB),
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（画 Q 的波形 / 填表）', [
            '确认是 NOR 版，标出 S、R 各接哪个门。',
            '从左到右一格一格走。先看 S、R 有没有 1：S=1→Q=1；R=1→Q=0。',
            '都是 0 → 抄上一格。上一格是 ? 就还是 ?。',
            '都是 1 → Q=0 且 %s=0，并在旁边标“禁止”。' % QB,
            '离开 11 时看怎么离开：同时→?；一个先撤→按剩下的那个算。',
            '%s 一般是 Q 取反，但禁止态要单独写。' % QB])
        ax.text(x, y + 6, 'NOR 版 vs NAND 版', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [92, 141, 141], 24,
              [['', 'SR (NOR)', '%s%s (NAND)' % (SB, RB)], ['有效电平', '1 有效', '0 有效'], ['保持', 'S=R=0', '%s=%s=1' % (SB, RB)],
               ['置位 Q=1', 'S=1, R=0', '%s=0, %s=1' % (SB, RB)], ['复位 Q=0', 'S=0, R=1', '%s=1, %s=0' % (SB, RB)],
               ['禁止', '1,1 → Q=%s=0' % QB, '0,0 → Q=%s=1' % QB], ['不稳定', '11 → 00', '00 → 11'], ['出 Q 的门接', 'R', SB]], fs=8.4)
        y2 = y + 30 + 24 * 8 + 22
        ax.text(x, y2, '门延迟：S→%s→Q（各差 1 级门）' % QB, fontsize=10, weight='bold', color=GREEN, va='top')
        S = [0] * 3 + [1] * 9 + [0] * 12; R = [0] * 15 + [1] * 7 + [0] * 2
        Qb_ = [1] * 4 + [0] * 13 + [1] * 7; Q_ = [0] * 5 + [1] * 11 + [0] * 8
        timing(ax, x + 30, y2 + 28, w - 34, [('S', S), ('R', R), ('Q', Q_), (QB, Qb_)], 24, rowh=30, vals=False, fs=9, lw=2)
    notes_page(doc, '3. 满分注意事项：SR 锁存器（NOR 版）', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 02 S̄R̄ 锁存器 (NAND) =================
def pdf_sr_nand():
    doc = Doc(os.path.join(OUT, '02_非S非R锁存器_NAND版.pdf'), '%s%s 锁存器（NAND 版）· %s%s latch' % (SB, RB, SB, RB))
    seq = sim_sr('nand', [(1, 0), (1, 1), (0, 1), (1, 1), (0, 0), (1, 1), (0, 1), (0, 0), (1, 0), (1, 1)])
    items = [
        ('1. 复位：%s=1, %s=0' % (SB, RB), '课件的起点。%s=0 进下面的 NAND：有 0 出 1 → %s=1。上面两个输入 %s=1、%s=1 → Q=0。' % (RB, QB, SB, QB)),
        ('2. 保持：1, 1', '%s 回到 1。Q=0 绕回下面的 NAND，继续让 %s=1；%s=1 让 Q 保持 0 → 记住了 0。' % (RB, QB, QB)),
        ('3. 置位：%s=0' % SB, '%s=0 进上面的 NAND → Q=1。下面两个输入 Q=1、%s=1 → %s=0。' % (SB, RB, QB)),
        ('4. 保持：1, 1', '输入和第 2 格一样，这次记住的是 1。低电平有效：两个都是 1 才是“什么都不做”。'),
        ('5. 禁止：0, 0', '两个 NAND 都有 0 输入 → Q=1 且 %s=1（两个都是 1，和 NOR 版的“都是 0”相反）。' % QB),
        ('6. 同时回到 1,1', '两个门同时看到 1,1 → 同时变 0 → 又同时变 1……竞争，结果不可预测 → 写 ?。'),
        ('7. 未知时来个置位', '%s=0 强制 Q=1，再得 %s=0。未知被一次 set/reset 清掉。' % (SB, QB)),
        ('8. 再次进入 0,0', '又是 Q=%s=1（禁止态）。接下来换一种“放法”。' % QB),
        ('9. 先放开 %s' % SB, '%s 先回 1，%s 还是 0 → 此刻就是复位：Q=0、%s=1，结果确定。' % (SB, RB, QB)),
        ('10. 再放开 %s → 保持' % RB, '从 1,0 回到 1,1 是普通的保持 → Q=0。后放开的那个输入说了算。'),
    ]
    panels(doc, '1. %s%s 锁存器（NAND 版）：10 种常考变化' % (SB, RB),
           'NAND 规则：有 0 出 1；全 1 才出 0。输入低电平有效，所以写成 %s、%s。课件画法：%s 在上面的门（出 Q），%s 在下面的门（出 %s）。' % (SB, RB, SB, RB, QB),
           items, seq, draw_sr('nand'), 5, 0.93, (26, 168))
    timing_page(doc, '1. %s%s 锁存器（NAND 版）时序图' % (SB, RB), '格子编号 = 上一页的 10 种情况。注意输入“平时在高位”，拉低才是动作。',
                ['Sb', 'Rb', 'Q', 'Qb'], [SB, RB, 'Q', QB], seq,
                note='读图要点：① %s=0→Q=1；%s=0→Q=0；两个都是 1→保持（看上一格）。② 第 5、8 格两个输入都为 0 时 Q=%s=1（两条都画在高位）。'
                     '③ 第 6 格 0,0 同时回 1,1 → 斜线（未知）；第 9→10 格先放 %s 再放 %s → 确定为 0。' % (SB, RB, QB, SB, RB))
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '课件原表 + 逐门推导。X = 无所谓。红线划掉的那一行 = 禁止输入。', legend=False)
    cv = CV(ax, 78, 190, 1.35); cv.mono = True
    draw_sr('nand')(cv, dict(Sb=0, Rb=0, Q=0, Qb=0))
    para(ax, 46, 385, '上面的门：Q = NAND(%s, %s)\n下面的门：%s = NAND(%s, Q)\n特征方程：$Q_{T+1}$ = S + %s·$Q_T$（S 指 %s 取反后的值）\n\n口诀：谁是 0，它所在的那个门输出就被顶成 1。\n%s=0 顶 Q；%s=0 顶 %s。'
         % (SB, QB, QB, RB, RB, SB, SB, RB, QB), 350, 10, 1.75)
    data = [[SB, RB, QT, QBT, QN, QBN, '结果', '为什么（逐门推）'],
            ['0', '0', 'X', 'X', '1', '1', '禁止', '两个 NAND 都有 0 输入 → 两个输出都是 1，Q 与 %s 不互补；之后若同时回 11 → 不稳定。' % QB],
            ['0', '1', 'X', 'X', '1', '0', '置位', '%s=0 → 上面的 NAND 必出 1 → Q=1。下面的 NAND 输入 Q=1、%s=1 → %s=0。与之前无关。' % (SB, RB, QB)],
            ['1', '0', 'X', 'X', '0', '1', '复位', '%s=0 → 下面的 NAND 必出 1 → %s=1。上面的 NAND 输入 %s=1、%s=1 → Q=0。与之前无关。' % (RB, QB, SB, QB)],
            ['1', '1', '0', '1', '0', '1', '保持', '外部输入都是 1，NAND 变成“对反馈取反”：%s=1 → Q=0；Q=0 → %s=1。原样锁住。' % (QB, QB)],
            ['1', '1', '1', '0', '1', '0', '保持', '同理：%s=0 → Q=1；Q=1 且 %s=1 → %s=0。同样的输入、不同的输出 = 记忆。' % (QB, RB, QB)]]
    cw = [34, 34, 40, 40, 46, 46, 52, 400]
    yb = table(ax, 432, 118, cw, [26] + [44] * 5, data, left={7}, fs=8.6)
    ax.plot([432, 432 + sum(cw[:-1])], [118 + 26 + 22] * 2, color='#E03131', lw=2.2, zorder=5)
    ax.text(432, yb + 30, '输入怎么变 → 输出怎么变（考“变化”就考这张）', fontsize=11, weight='bold', color=GREEN)
    data2 = [['%s %s 从' % (SB, RB), '变到', 'Q', QB, '说明'],
             ['1 0', '1 1', '0', '1', '记住刚才的复位（课件：remembers its signal when going from 10 or 01 to 11）'],
             ['0 1', '1 1', '1', '0', '记住刚才的置位'],
             ['任意', '0 1 / 1 0', '1 / 0', '0 / 1', '直接置位 / 复位，不看历史'],
             ['任意', '0 0', '1', '1', '禁止态：两个输出都是 1'],
             ['0 0', '1 1（同时）', '?', '?', '不稳定：课件“Going from 00 to 11 produces unstable behaviour”'],
             ['0 0', '1 0（%s 先放开）' % SB, '0', '1', '%s 还是 0 → 复位。之后回 11 保持 0' % RB],
             ['0 0', '0 1（%s 先放开）' % RB, '1', '0', '%s 还是 0 → 置位。之后回 11 保持 1' % SB]]
    table(ax, 432, yb + 46, [60, 120, 46, 46, 420], 36, data2, left={4}, fs=8.6, hl={5})
    notes = [
        '名字上有横线 = 低电平有效。%s=0 才是“置位”，%s=0 才是“复位”。看到 0 才动手，看到 1 是“放开”。' % (SB, RB),
        'NAND 口诀：有 0 出 1，全 1 出 0。课件画法：%s 接上面的门（输出 Q），%s 接下面的门（输出 %s）——这里不交叉。' % (SB, RB, QB),
        '保持是 11，不是 00！这是和 NOR 版最容易混的地方（课件 Note：inputs of 11 maintain the previous output state）。',
        '禁止态是 00，此时 Q=%s=1（两个都是 1）。NOR 版禁止态是 11 且两个都是 0。别记反。' % QB,
        '00 → 11 同时放开 → 不稳定，“Output depends on which input changes first”。答题写 ? / unknown。',
        '题目若说明哪一个先回 1：后回 1 的那个（还在 0 的那个）决定结果。%s 后放 → Q=1；%s 后放 → Q=0。' % (SB, RB),
        '课件真值表里 00 那一行被红线划掉：表示“这种输入不允许出现”，但它的即时输出 (1,1) 仍要会写。',
        '上电初始 Q 未知；11（保持）不会让未知变确定，必须先拉低一次 %s 或 %s。' % (SB, RB),
        '门延迟：%s↓ 后 Q 先升（1 级），%s 再降（再 1 级）；中间短暂 Q=%s=1。' % (SB, QB, QB),
        '它就是后面 clocked SR latch / D latch 的“后半截”：那两个电路只是在它前面再加一层 NAND。把这张表背熟，后面全是套用。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（画 Q 的波形 / 填表）', [
            '确认是 NAND 版（输入名带横线 / 门是 NAND）。',
            '一格一格走。先找 0：%s=0→Q=1；%s=0→Q=0。' % (SB, RB),
            '都是 1 → 抄上一格（上一格是 ? 就还是 ?）。',
            '都是 0 → Q=1 且 %s=1，并标“禁止”。' % QB,
            '离开 00 时：同时→?；一个先放→按还为 0 的那个算。',
            '如果题目给的是不带横线的 S、R 再经过非门/NAND 进来，先把它们换算成 %s、%s 再套表。' % (SB, RB)])
        ax.text(x, y + 6, 'NAND 版 vs NOR 版', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [92, 141, 141], 24,
              [['', '%s%s (NAND)' % (SB, RB), 'SR (NOR)'], ['有效电平', '0 有效', '1 有效'], ['保持', '%s=%s=1' % (SB, RB), 'S=R=0'],
               ['置位 Q=1', '%s=0, %s=1' % (SB, RB), 'S=1, R=0'], ['复位 Q=0', '%s=1, %s=0' % (SB, RB), 'S=0, R=1'],
               ['禁止', '0,0 → Q=%s=1' % QB, '1,1 → Q=%s=0' % QB], ['不稳定', '00 → 11', '11 → 00'], ['出 Q 的门接', SB, 'R']], fs=8.4)
        y2 = y + 30 + 24 * 8 + 22
        ax.text(x, y2, '门延迟：%s→Q→%s（各差 1 级门）' % (SB, QB), fontsize=10, weight='bold', color=GREEN, va='top')
        S = [1] * 3 + [0] * 9 + [1] * 12; R = [1] * 15 + [0] * 7 + [1] * 2
        Q_ = [0] * 4 + [1] * 13 + [0] * 7; Qb_ = [1] * 5 + [0] * 11 + [1] * 8
        timing(ax, x + 30, y2 + 28, w - 34, [(SB, S), (RB, R), ('Q', Q_), (QB, Qb_)], 24, rowh=30, vals=False, fs=9, lw=2)
    notes_page(doc, '3. 满分注意事项：%s%s 锁存器（NAND 版）' % (SB, RB), '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 03 Clocked SR 锁存器 =================
def pdf_csr():
    doc = Doc(os.path.join(OUT, '03_Clocked_SR锁存器.pdf'), '门控 / 时钟 SR 锁存器 · Clocked (gated) SR latch')
    seq = sim_csr([(1, 0, 1), (1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1), (1, 0, 1)])
    items = [
        ('1. C=1, S=0, R=1：复位', '课件第一张图。时钟为高，第一层 NAND 把 S、R 取反：a=1、b=0。b=0 → 下门出 1 → %s=1；上门两个输入都是 1 → Q=0。' % QB),
        ('2. C=1, S=R=0：保持', '课件第二张图。R 回 0 → b=1。a=b=1 是内部 %s%s 锁存器的“保持” → Q 仍是 0。' % (SB, RB)),
        ('3. C 变 0：门关上', '课件“Now set the clock low”。C=0 → 两个第一层 NAND 都有 0 输入 → a=b=1 → 保持，Q=0。'),
        ('4. C=0 时 S 变 1：被挡住', 'S=1 但 C=0 → a 仍是 1（有 0 出 1），变化到不了第二层 → Q 不变。时钟必须为高，输入才有效。'),
        ('5. C 变 1：立刻置位', 'C 一变高，S=1 立刻生效：a=0 → Q=1，再得 %s=0。锁存器看的是“C=1 这一整段”，不是边沿。' % QB),
        ('6. C=1, S=R=1：禁止', 'a=b=0 → 两个第二层 NAND 都有 0 输入 → Q=1 且 %s=1（课件：both outputs will be high）。' % QB),
        ('7. C 回到 0（S=R 仍是 1）', 'a、b 同时从 0 回到 1 = 内部锁存器 00→11 → 输出取决于哪根中间线先变 → 不可预测，写 ?。'),
        ('8. C=1, S=0, R=1：重新确定', '未知状态下，只要在 C=1 时给一次合法的 set/reset，就重新得到确定值：b=0 → Q=0、%s=1。' % QB),
    ]
    panels(doc, '1. Clocked SR 锁存器：8 种常考变化',
           '课件电路：在 %s%s 锁存器前面再加一层 NAND。a = (S·C)′，b = (R·C)′，它们就是内部锁存器的 %s、%s（低有效）。C=0 时 a=b=1 → 只能保持。' % (SB, RB, SB, RB),
           items, seq, draw_csr, 4, 0.9, (62, 172))
    timing_page(doc, '1. Clocked SR 锁存器时序图', '浅橙背景 = C=1（门开着）。格子编号 = 上一页的 8 种情况。',
                ['C', 'S', 'R', 'a', 'b', 'Q', 'Qb'], ['C', 'S', 'R', 'a=(S·C)′', 'b=(R·C)′', 'Q', QB], seq,
                shade=[(0, 2), (4, 6), (7, 8)],
                note='做题方法：先画 a、b 两条中间线（C=0 的地方一律是 1；C=1 的地方 a=S 取反、b=R 取反），再把 a、b 当成 %s%s 锁存器的输入去画 Q。'
                     '白色区域（C=0）里 Q 一定是一条水平线；橙色区域里 S=1→Q=1、R=1→Q=0、都为 0→保持、都为 1→Q=%s=1。' % (SB, RB, QB))
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '课件原表（C, S, R → $Q_{T+1}$）+ 我加的中间线 a、b 和逐门推导。', legend=False)
    cv = CV(ax, 110, 185, 1.2); cv.mono = True
    draw_csr(cv, dict(S=0, R=0, C=0, a=0, b=0, Q=0, Qb=0))
    para(ax, 46, 375, 'a = (S·C)′     b = (R·C)′\nQ = NAND(a, %s)     %s = NAND(b, Q)\n\nC=1 时：$Q_{T+1}$ = S + %s·$Q_T$（要求 S·R=0）\nC=0 时：$Q_{T+1}$ = $Q_T$\n\n注意：这里 S 在上面、直接对应 Q（两次取反 = 不取反），和 NOR 版 SR 锁存器“R 在上”不一样。'
         % (QB, QB, RB), 350, 9.6, 1.7)
    data = [['C', 'S', 'R', 'a', 'b', QN, 'Result', '为什么（逐门推）'],
            ['0', 'X', 'X', '1', '1', QT, 'no change', 'C=0 → 第一层两个 NAND 都有 0 输入 → a=b=1 → 内部锁存器处于 11 保持。S、R 怎么变都没用。'],
            ['1', '0', '0', '1', '1', QT, 'no change', 'C=1 但 S=R=0 → a=b=1 → 同样是保持。'],
            ['1', '0', '1', '1', '0', '0', 'reset', 'b=(1·1)′=0 → 下面的门必出 1 → %s=1；上面的门输入 a=1、%s=1 → Q=0。' % (QB, QB)],
            ['1', '1', '0', '0', '1', '1', 'set', 'a=(1·1)′=0 → 上面的门必出 1 → Q=1；下面的门输入 b=1、Q=1 → %s=0。' % QB],
            ['1', '1', '1', '0', '0', '?', 'Undefined', 'a=b=0 → 当下 Q=%s=1；C 一掉 a、b 同时回 1 → 取决于哪根中间线先变 → 不确定。禁止输入。' % QB]]
    cw = [30, 30, 30, 30, 30, 50, 76, 414]
    yb = table(ax, 432, 118, cw, [26] + [44] * 5, data, left={7}, fs=8.6)
    ax.plot([432, 432 + sum(cw[:-1])], [yb - 22, yb - 22], color='#E03131', lw=2.2, zorder=5)
    ax.text(432, yb + 30, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    data2 = [['发生了什么', 'Q 的反应', '说明'],
             ['C=0 期间 S 或 R 变化', '不变', '被第一层 NAND 挡住（a、b 一直是 1）'],
             ['C 0→1，此时 S=1,R=0', '立刻变 1', '不用等什么边沿，C 一高就生效'],
             ['C=1 期间 S 0→1→0（毛刺）', '变 1 并一直保持', '电平敏感：C=1 期间任何一次 S=1 都会被“抓住”'],
             ['C=1 期间 R 0→1', '立刻变 0', '同上'],
             ['C 1→0', '锁住下降那一刻的状态', '之后直到下次 C=1 都是水平线'],
             ['S=R=1 且 C=1', 'Q=%s=1' % QB, '禁止态，当下两个输出都是 1'],
             ['S=R=1 时 C 1→0', '?', '课件 Forbidden state：depends on which middle wire changes first'],
             ['S=R=1,C=1 时先撤 R', 'Q=1', '剩 S=1 → 正常置位，结果确定（先撤 S 则 Q=0）']]
    table(ax, 432, yb + 46, [200, 150, 340], 34, data2, left={2}, fs=8.6, hl={7})
    notes = [
        '结构：两层 NAND。第二层是 %s%s 锁存器；第一层把 S、R 和 C 做 NAND。所以外部 S、R 是高电平有效（两次取反抵消）。' % (SB, RB),
        'C=0 → 永远保持。无论 S、R 是什么（包括 S=R=1），Q 都不变。真值表第一行的 X X 就是这个意思。',
        'C=1 → 和普通 SR 锁存器一样：10 置位、01 复位、00 保持、11 禁止。',
        '它是“电平触发”（level-sensitive），不是边沿触发：C=1 的整段时间里，S、R 一变 Q 立刻跟着变。画波形时橙色区域内要逐个变化点检查。',
        'C 下降的那一刻把当时的状态锁住。之后白色区域里 Q 必须是水平线。',
        '禁止态 S=R=1（且 C=1）：这个电路里当下 Q=1、%s=1（课件写“outputs will also be high”）。注意：如果是 AND+NOR 画法的门控锁存器，则两个都是 0——看清题目用的是哪种门。' % QB,
        '课件真值表在 1 1 1 那行写 “?  Undefined”。考试填 $Q_{T+1}$ 就写 ? / undefined，并说明原因：C 回 0 时两根中间线同时从 0 变 1，谁先变不确定。',
        '符号：方框里 S、C、R 三个输入，%s 输出端的小圆圈只是“反相输出”的记号，不是多了一个非门（课件 Note）。' % QB,
        'C 接的常常是时钟（周期性 0/1 脉冲），所以叫 clocked SR latch；也叫 gated SR latch。C 也可以叫 Enable。',
        '解决禁止态的办法（课件）：不让 S 和 R 同时为 1 → 用一根 D 同时产生 S=D、R=%s → 就得到 D latch。' % DB,
        '上电时 Q 未知，且 C=0 或 S=R=0 都不会改变未知；要 C=1 且 S≠R 才确定。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 C、S、R 波形画 Q）', [
            '把 C=1 的区间涂出来（其余区间 Q 一律水平）。',
            '可选但推荐：先画 a=(S·C)′、b=(R·C)′。C=0 处两条都是 1。',
            '在每个 C=1 区间内，从左到右找 S、R 的每个变化点，按 10→1、01→0、00→保持、11→禁止 更新 Q。',
            'C 下降处：记下此刻的 Q，一直保持到下一个 C 上升。',
            'C 上升处：马上按当前的 S、R 更新（不要等）。',
            '若在 S=R=1 时 C 下降 → 之后画斜线/写 ?，直到下一次合法的 set/reset。'])
        ax.text(x, y + 6, '特性表（背）', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [44, 44, 44, 90, 152], 24,
              [['C', 'S', 'R', QN, '结果'], ['0', 'X', 'X', QT, '保持'], ['1', '0', '0', QT, '保持'], ['1', '0', '1', '0', '复位'],
               ['1', '1', '0', '1', '置位'], ['1', '1', '1', '?', '禁止 / 未定义']], fs=8.6)
        ax.text(x, y + 30 + 24 * 6 + 20, '锁存器 = 看电平；触发器 = 看边沿。\n这是整章最重要的一句话。', fontsize=9.5, color='#C92A2A', va='top', linespacing=1.6)
    notes_page(doc, '3. 满分注意事项：Clocked SR 锁存器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 04 D 锁存器 =================
def pdf_dl():
    doc = Doc(os.path.join(OUT, '04_D锁存器.pdf'), 'D 锁存器 · D latch (gated D-latch)')
    seq = sim_dl([(0, 0), (1, 1), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0), (0, 0)])
    items = [
        ('1. 上电，C=0：Q 未知', 'C=0 → a=b=1 → 内部锁存器只能保持。但它从来没被写过，所以 Q、%s 都是 ?。D 是什么都没用。' % QB),
        ('2. C=1, D=1：透明，Q=1', 'D=1、C=1 → a=0 → Q=1。%s=0 → b=1；下门两个输入都是 1 → %s=0。Q 等于 D。' % (DB, QB)),
        ('3. C=1, D 变 0：Q 立刻变 0', 'D=0 → a=1；%s=1、C=1 → b=0 → %s=1 → Q=0。C=1 时 Q 像一根导线一样连着 D（“透明”）。' % (DB, QB)),
        ('4. C=1, D 又变 1：Q 又跟着变', 'D 抖几次，Q 就抖几次——这就是锁存器的问题（课件 Latches are transparent）。'),
        ('5. C 变 0：锁住', 'a=b=1 → 保持关门那一刻的值 Q=1。'),
        ('6. C=0, D 变 0：无效', 'D、%s 都变了，但 C=0 把两个第一层 NAND 都堵死：a=b=1 不变 → Q 仍是 1。' % DB),
        ('7. C 变 1：立刻跟随', '门一开，Q 立刻等于此刻的 D=0（b=0 → %s=1 → Q=0）。不用等任何边沿。' % QB),
        ('8. C 变 0：锁住 0', '保持 Q=0。因为 S=D、R=%s 永远相反，a、b 不可能同时为 0 → D 锁存器没有禁止态。' % DB),
    ]
    panels(doc, '1. D 锁存器：8 种常考变化',
           '课件电路：把 clocked SR 锁存器的 S 接 D、R 接 %s（一个非门）。a = (D·C)′，b = (%s·C)′。C=1：Q=D（透明）；C=0：保持。' % (DB, DB),
           items, seq, draw_dl, 4, 0.86, (78, 172))
    timing_page(doc, '1. D 锁存器时序图', '浅橙背景 = C=1。橙色区域内 Q 和 D 完全一样；白色区域内 Q 是一条水平线（保持 C 下降那一刻的值）。',
                ['C', 'D', 'Db', 'a', 'b', 'Q', 'Qb'], ['C', 'D', DB, 'a=(D·C)′', 'b=(%s·C)′' % DB, 'Q', QB], seq,
                shade=[(1, 4), (6, 7)],
                note='一句话：D 锁存器是“电平触发”——C=1 的整段时间都在跟随 D；C=0 时不理 D。'
                     '第 1 格是上电后还没开过门 → 未知。第 5 格锁住的是“C 下降那一瞬间”的 D（=1），不是之后的 D。')
    ax = doc.page('2. 解析 Truth table：每一行为什么是这个结果', '课件原表只有 $Q_T$、D → $Q_{T+1}$（默认 C=1）。这里补上 C=0 的两行和中间线。', legend=False)
    cv = CV(ax, 132, 185, 1.2); cv.mono = True
    draw_dl(cv, dict(D=0, Db=0, C=0, a=0, b=0, Q=0, Qb=0))
    para(ax, 46, 385, 'a = (D·C)′     b = (%s·C)′\n\nC=1 时：$Q_{T+1}$ = D（和 $Q_T$ 无关）\nC=0 时：$Q_{T+1}$ = $Q_T$\n合起来：$Q_{T+1}$ = C·D + %s·$Q_T$\n\n等价于 clocked SR 锁存器里 S=D、R=%s：\nD=1 → 置位；D=0 → 复位；永远不会 S=R=1。' % (DB, ov('C'), DB), 350, 9.6, 1.7)
    data = [['C', 'D', QT, DB, 'a', 'b', QN, '说明', '为什么（逐门推）'],
            ['1', '0', '0', '1', '1', '0', '0', '写入 0', 'D=0 → a=1；%s=1、C=1 → b=0 → %s=1 → Q=0。' % (DB, QB)],
            ['1', '1', '0', '0', '0', '1', '1', '写入 1', 'D=1、C=1 → a=0 → Q=1；b=1、Q=1 → %s=0。旧值 0 被覆盖。' % QB],
            ['1', '0', '1', '1', '1', '0', '0', '写入 0', '同第 1 行：旧值是 1 也没用，Q 被复位成 0。'],
            ['1', '1', '1', '0', '0', '1', '1', '写入 1', '同第 2 行。C=1 时 $Q_{T+1}$ 这一列和 D 这一列一模一样。'],
            ['0', 'X', '0', 'X', '1', '1', '0', '保持', 'C=0 → a=b=1 → 内部 %s%s 锁存器保持。D 无所谓。' % (SB, RB)],
            ['0', 'X', '1', 'X', '1', '1', '1', '保持', '同上，保持的是 1。']]
    cw = [30, 30, 40, 30, 30, 30, 50, 60, 390]
    yb = table(ax, 432, 118, cw, [26] + [38] * 6, data, left={8}, fs=8.6, hl={(i, 6) for i in range(1, 7)})
    ax.text(432, yb + 30, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    data2 = [['发生了什么', 'Q 的反应', '说明'],
             ['C=1 期间 D 变化', '立刻跟着变', '透明：Q 就是 D 的拷贝（只差一点门延迟）'],
             ['C 1→0', '锁住下降那一刻的 D', '之后是水平线，直到下次 C=1'],
             ['C=0 期间 D 变化', '不变', '被第一层 NAND 挡住'],
             ['C 0→1', '立刻变成当前的 D', '如果此时 D ≠ 旧 Q，Q 在 C 的上升处就跳变'],
             ['上电后 C 一直是 0', '?', '没写过就是未知；第一次 C=1 后才确定'],
             ['D 和 C 同时变（C 下降瞬间 D 也在变）', '不确定', '违反 setup/hold，实际电路可能锁到新值或旧值']]
    table(ax, 432, yb + 46, [230, 150, 310], 36, data2, left={2}, fs=8.6)
    notes = [
        '结构：clocked SR 锁存器 + 一个非门。D 直接进上面的 NAND（相当于 S），%s 进下面的 NAND（相当于 R）。' % DB,
        '功能就两句：C=1 → Q=D；C=0 → Q 不变。课件表格里 $Q_{T+1}$ 一列等于 D 一列，和 $Q_T$ 无关。',
        '没有禁止态：S=D、R=%s 永远一个 0 一个 1，所以内部 a、b 不可能同时为 0（课件：avoid the indeterminate state problem）。' % DB,
        '“透明”(transparent)：C=1 时输入的任何变化都直接出现在输出上。画波形时橙色区域要把 D 的每一个抖动都照抄到 Q。',
        '锁住的值 = C 下降那一瞬间的 D，不是 C=1 期间“最常见”的值，也不是 C 上升时的值。',
        'C 上升时如果 D 和旧 Q 不同，Q 立刻跳变（不等下降沿）。这是和触发器最大的区别。',
        '课件的“计算器”例子：按住 = 时（C=1）加法结果不停地绕回去再加 → 输出 86、151、223……而不是 1、2、3。锁存器做不了“按一下加一次”。',
        '课件规则：锁存器的输出不要直接或经过组合逻辑接回同一个时钟控制的锁存器输入。例：把 %s 接回 D，C=1 期间 Q 会 0→1→0→1 不停振荡，直到 C 变 0。' % QB,
        '课件“5 个 D 锁存器串联”例子：C=1 时所有锁存器同时透明，最左边的 0 一口气冲到最右边（全变 0），而不是每次只移一位 → 所以移位寄存器必须用触发器。',
        '%s 一直是 Q 的反相（D 锁存器里它们永远互补），但两条都要画。' % QB,
        '符号：方框 D、C 两个输入；没有三角形（三角形 = 边沿触发的触发器）。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 C、D 波形画 Q）', [
            '把 C=1 的区间涂出来。',
            '涂色区间内：把 D 原样描到 Q 上（包括所有毛刺）。',
            '每个涂色区间的右端（C 下降）：看此刻 D 的值，向右画水平线直到下一个 C 上升。',
            '第一个 C=1 之前：Q 画斜线/写 ?（除非题目给了初值）。',
            '%s = Q 取反。' % QB])
        ax.text(x, y + 6, '特性表（背）', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [60, 60, 100, 154], 24,
              [['C', 'D', QN, '结果'], ['0', 'X', QT, '保持'], ['1', '0', '0', '跟随 D'], ['1', '1', '1', '跟随 D']], fs=8.6)
        y2 = y + 30 + 24 * 4 + 24
        ax.text(x, y2, '经典陷阱：%s 接回 D（课件 transparency example）' % QB, fontsize=10, weight='bold', color=GREEN, va='top')
        C_ = [0] * 3 + [1] * 12 + [0] * 5; Q_ = [0] * 4 + [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0] + [0] * 5
        timing(ax, x + 30, y2 + 30, w - 34, [('C', C_), ('Q', Q_)], 20, rowh=34, vals=False, fs=9, lw=2, shade=[(3, 15)])
        para(ax, x, y2 + 110, 'C=1 期间 Q 不停翻转；C 掉下去时停在哪个值无法预测。想要“每个时钟只翻一次”→ 必须用边沿触发的触发器。', w, 8.6, 1.55, '#C92A2A')
    notes_page(doc, '3. 满分注意事项：D 锁存器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


if __name__ == '__main__':
    pdf_sr_nor(); pdf_sr_nand(); pdf_csr(); pdf_dl()
    print('ok')
