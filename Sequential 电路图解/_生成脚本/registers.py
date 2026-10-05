# -*- coding: utf-8 -*-
"""09 寄存器  10 移位寄存器  11 加载寄存器 —— 电路画法按课件 flipflops_slides.pdf。"""
import os
from lib import *
from latches import notes_page, steps_box, OUT, QB, QT, QN
from flipflops import B, panels, edge_list, shades, UP

QS = ['$Q_%d$' % i for i in range(4)]; DS = ['$D_%d$' % i for i in range(4)]


def draw_reg(kind):
    def f(cv, v, chg=()):
        cy = 116 if kind == 'load' else 100
        for i in range(4):
            x = 95 * i
            cv.block(x, 0, 50, 70, pins=[('D', 10, 16), ('Q', 40, 16), (QB, 40, 56)] + ([('EN', 15, 34)] if kind == 'load' else []), clk=52, fs=7.6)
            cv.wire([(x - 10, cy), (x - 10, 52), (x, 52)], v['C'])
            if kind == 'shift':
                cv.wire([(x - 45 if i else -35, 16), (x, 16)], v['SI'] if i == 0 else v['Q%d' % (i - 1)])
                B(cv, x + 73, 2, QS[i], v, 'Q%d' % i, chg)
                if i == 3:
                    cv.wire([(x + 50, 16), (x + 90, 16)], v['Q3'])
            else:
                cv.wire([(x - 20, -34), (x - 20, 16), (x, 16)], v['D%d' % i]); B(cv, x - 20, -43, DS[i], v, 'D%d' % i, chg)
                cv.wire([(x + 50, 16), (x + 64, 16)], v['Q%d' % i]); B(cv, x + 30, -11, QS[i], v, 'Q%d' % i, chg)
                if kind == 'load':
                    cv.wire([(x - 30, 100), (x - 30, 34), (x, 34)], v['W'])
        cv.wire([(-50, cy), (275, cy)], v['C']); cv.label(-66, cy, 'Clk', fs=9); B(cv, 120, cy + 13, 'Clk', v, 'C', chg)
        if kind == 'load':
            cv.wire([(-50, 100), (255, 100)], v['W']); cv.label(-72, 100, 'Write', fs=9); B(cv, 120, 88, 'Write', v, 'W', chg)
        if kind == 'shift':
            cv.label(-46, 16, 'SI', fs=9); B(cv, -16, 2, 'SI', v, 'SI', chg)
    return f


def sim_reg(kind, steps, q=None):
    """steps: (C, 数据, Write)。数据：shift 是 SI；其余是 4 位串（D0D1D2D3，左边是 D0，和图一致）。"""
    q = list(q) if q else [None] * 4; out, prev = [], None
    for C, dat, Wr in steps:
        if prev and prev[0] == 0 and C == 1:
            if kind == 'shift':
                q = [prev[1]] + q[:-1]
            elif kind == 'plain' or prev[2] == 1:
                q = [int(c) for c in prev[1]]
        v = dict(C=C, W=Wr)
        if kind == 'shift':
            v['SI'] = dat
        else:
            v.update({'D%d' % i: int(dat[i]) for i in range(4)})
        v.update({'Q%d' % i: q[i] for i in range(4)})
        out.append(v); prev = (C, dat, Wr)
    return out


def qs(v):
    return ''.join(sv(v['Q%d' % i]) for i in range(4))


def reg_panels(doc, kind, title, sub, items, seq):
    panels(doc, title, sub, items, seq, draw_reg(kind), 3, 0.8, (88 if kind == 'load' else 78, 185))


# ================= 09 寄存器 =================
def pdf_reg():
    doc = Doc(os.path.join(OUT, '09_寄存器.pdf'), '寄存器 · Registers')
    seq = sim_reg('plain', [(0, '1011', 0), (1, '1011', 0), (1, '0110', 0), (0, '0110', 0), (1, '0110', 0), (0, '1111', 0)])
    items = [
        ('1. 上电：Q 未知，D=1011 等在门口', '4 个 D 触发器共用一根 Clk。还没来过上升沿 → 每一位都未知。输入 %s%s%s%s=1011 只是停在 D 端。' % tuple(DS)),
        ('2. 上升沿：4 位同时装入', '同一个上升沿，每个触发器各自采样自己的 D → Q=1011。所有位在同一时刻一起变。'),
        ('3. Clk=1 期间 D 变成 0110', '触发器只在边沿采样 → Q 仍是 1011。寄存器“记住”了上一个边沿时的输入。'),
        ('4. 下降沿：什么都不发生', '正边沿触发 → 下降沿无效，Q 仍是 1011。'),
        ('5. 上升沿：装入 0110', '采到边沿前的 D=0110 → Q=0110。旧值被整个覆盖。'),
        ('6. D 又变成 1111（Clk=0）', 'Q 不变，要等下一个上升沿。注意：没有使能端的寄存器“每个上升沿都会装入”，想保持就得让 D 不变——这就是 load register 要加 EN 的原因。'),
    ]
    reg_panels(doc, 'plain', '1. 寄存器：n 个 D 触发器共用一个时钟（这里 4 位）',
               '寄存器 = 一排 D 触发器，一个触发器存 1 位，Clk 接在一起。下面是最基本的并行装入形式（课件 load register 的第一张图，无使能）。图中从左到右是第 0、1、2、3 位。',
               items, seq)
    ax = doc.page('1. 寄存器时序图 + 同步 / 异步复位', '浅橙 = Clk=1；黄色虚线 = 上升沿。总线写法：一格里的 4 个数字依次是第 0、1、2、3 位（和上一页图的左右顺序一致）。')
    n = 24; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]
    D = ['1011'] * 8 + ['0110'] * 8 + ['1111'] * 8; Q, q = [], '????'
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            q = D[i - 1]
        Q.append(q)
    yb = timing(ax, 170, 150, 950, [('Clk', C), ('%s%s%s%s' % tuple(DS), D), ('%s%s%s%s' % tuple(QS), Q)], n, rowh=52, shade=shades(C), edges=edge_list(C), vals=False)
    para(ax, 170, yb + 12, 'Q 总是比 D “晚到下一个上升沿”：D 在两个边沿之间变化，Q 在紧接着的那个上升沿才变成它。第一个上升沿之前 Q 未知。', 950, 9.2)
    ax.text(170, yb + 62, '复位（课件 Resetting inputs）：同一组波形，两种复位方式', fontsize=11, weight='bold', color=GREEN)
    R = [0] * 11 + [1] * 5 + [0] * 8; D1 = [1] * n; Qs, Qa, s, a = [], [], None, None
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            s = 0 if R[i - 1] else D1[i - 1]; a = D1[i - 1]
        if R[i]:
            a = 0
        Qs.append(s); Qa.append(a)
    yb2 = timing(ax, 170, yb + 100, 950, [('Clk', C), ('Reset', R), ('D（某一位）', D1), ('Q（同步复位）', Qs), ('Q（异步复位）', Qa)], n, rowh=46,
                 shade=shades(C), edges=edge_list(C), vals=False)
    para(ax, 170, yb2 + 12, '同步复位：Reset 变 1 之后要等到下一个上升沿 Q 才清 0。异步复位：Reset 一变 1，Q 立刻清 0，不看时钟；Reset 放开后要等下一个上升沿才重新装入 D。', 950, 9.2)
    ax = doc.page('2. 解析 Truth table：寄存器什么时候变、变成什么', '对每一位都成立（i = 0…n−1）。再加三种寄存器的对比和最高时钟频率。', legend=False)
    cv = CV(ax, 100, 190, 0.85); cv.mono = True
    draw_reg('plain')(cv, dict(C=0, W=0, **{'D%d' % i: 0 for i in range(4)}, **{'Q%d' % i: 0 for i in range(4)}))
    para(ax, 46, 330, '每一位：$Q_{i,T+1}$ = $D_i$（在上升沿）\n整体：Q ← D，n 位同时。\n\nn 位寄存器需要 n 个触发器，能存 $2^n$ 种不同的值。\n读：直接看 Q 线，随时可读。\n写：把值放到 D 上，等一个上升沿。', 360, 9.5, 1.7)
    table(ax, 440, 118, [90, 70, 90, 433], 32,
          [['Reset', 'Clk', '$Q_{T+1}$', '为什么'],
           ['0', UP, 'D', '每个触发器在上升沿采样自己的 D → 整个寄存器装入 D（边沿前的值）。'],
           ['0', '不是 ↑', QT, '触发器只在有效边沿更新 → 其余时间保持。D 怎么变都不影响 Q。'],
           ['1（同步）', UP, '0…0', '同步复位：在上升沿把所有位清 0，此时 D 被忽略。'],
           ['1（同步）', '不是 ↑', QT, '同步复位也要等边沿，没有边沿就不清。'],
           ['1（异步）', 'X', '0…0', '异步复位：立刻清 0，与时钟无关。']], left={3}, fs=8.8, hl={1})
    ax.text(440, 340, '三种寄存器对比（课件 Example #1: Registers）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 356, [120, 185, 185, 193], [28, 44, 44, 44, 44],
          [['', '基本寄存器', '移位寄存器 shift', '加载寄存器 load'],
           ['每一位的 D 接什么', '外部的 $D_i$', '前一位的 Q（第 0 位接 SI）', '外部的 $D_i$，但经过 EN 选择'],
           ['每个上升沿', '装入全部 n 位', '整体移动一位，SI 进来一位', 'Write=1 才装入，否则保持'],
           ['装满 n 位要多久', '1 个时钟', 'n 个时钟（串行）', '1 个时钟（并行）'],
           ['怎样保持旧值', '只能让 D 不变', '停时钟（课件未提供保持）', 'Write=0']], fs=8.6)
    ax.text(440, 580, '最高时钟频率（课件 Maximum clock frequency）', fontsize=11, weight='bold', color=GREEN)
    para(ax, 440, 602, '时钟周期 ≥ 任意两个触发器之间最长的传播延迟 + 触发器的 setup time。\n原因：上升沿后，前一级的新 Q 要穿过中间的组合逻辑，并且在下一个上升沿之前 setup 这么久就到达后一级的 D。\n'
         '例：触发器输出延迟 2 ns + 组合逻辑 6 ns + setup 2 ns = 10 ns → 最高频率 = 1 / 10 ns = 100 MHz。', 680, 9.3, 1.7)
    notes = [
        '寄存器 = 多个 D 触发器共用同一个时钟，一个触发器存 1 位。16 位整数就要 16 个触发器。',
        '所有位在同一个有效边沿同时更新。画波形时各位的跳变要对齐在同一条虚线上。',
        '寄存器里用的是触发器，不是锁存器。用锁存器的话 Clk=1 期间输入会一直“漏”进去（透明）。',
        'Q 的值 = 最近一个上升沿之前一瞬间的 D。两个边沿之间 D 的变化全部忽略。',
        '第一个上升沿（或复位）之前，寄存器内容未知。课件：触发器上电状态未知，所以需要 reset。',
        '同步复位：只在有效边沿清 0。异步复位：立刻清 0，不管时钟。题目没说就问清/写明假设；这个 Reset 和 SR 锁存器的 R 无关。',
        '基本寄存器没有“保持”功能：每个上升沿都会重新装入当时的 D。要“想写才写”→ 用带使能端的 D 触发器（load register）。',
        'Setup / hold：D 不能在有效边沿附近变化；边沿前要稳定 setup time，边沿后要稳定 hold time。',
        '最高时钟频率由“最长传播延迟 + setup time”决定，周期不能比它短。找最长的那条路径（关键路径）。',
        '位序：图里从左到右是 $D_0$…$D_3$。把它读成一个二进制数时，先确认题目规定哪一位是最高位。',
        '移位寄存器和加载寄存器是寄存器的两种接法：前者串行进（一次一位），后者并行进（一次全部）。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clk、D 画寄存器内容）', [
            '画出所有上升沿的竖虚线。',
            '有 Reset 先看 Reset：异步 → Reset=1 的整段 Q=0；同步 → 只在虚线处判断。',
            '每条虚线上读边沿前的 D（每一位），写到 Q。',
            '虚线之间 Q 不变。第一条虚线之前写 ?。',
            '多位时用总线画法：一个六边形格子里写当前的值。'])
        ax.text(x, y + 6, '同步 vs 异步复位', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [100, 137, 137], [26, 40, 40, 40],
              [['', '同步复位', '异步复位'], ['什么时候清 0', '下一个有效边沿', 'Reset 一有效就清'], ['需要时钟吗', '需要', '不需要'], ['Reset 很短（没碰到边沿）', '没效果', '照样清 0']], fs=8.6)
    notes_page(doc, '3. 满分注意事项：寄存器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 10 移位寄存器 =================
def pdf_shift():
    doc = Doc(os.path.join(OUT, '10_移位寄存器.pdf'), '移位寄存器 · Shift registers')
    seq = sim_reg('shift', [(0, 1, 0), (1, 1, 0), (0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)], q=[0, 0, 0, 0])
    items = [
        ('1. 初始 0000，SI=1（边沿前）', '每个触发器的 D 接前一个的 Q，第 0 个的 D 接 SI。此刻各个 D 端看到的是：SI=1、%s=0、%s=0、%s=0。（假设已复位为 0000）' % (QS[0], QS[1], QS[2])),
        ('2. 上升沿 1：1 进来 → 1000', '所有触发器同时采样“边沿前”的 D：%s←SI=1，%s←旧%s=0，%s←旧%s=0，%s←旧%s=0。' % (QS[0], QS[1], QS[0], QS[2], QS[1], QS[3], QS[2])),
        ('3. 时钟变低，SI 换成 0', '下降沿无效，Q 仍是 1000。下一位数据 0 放到 SI 上等着。'),
        ('4. 上升沿 2：→ 0100', '%s←SI=0，%s←旧%s=1，其余←0。刚才那个 1 向右挪了一格。每个上升沿只挪一格。' % (QS[0], QS[1], QS[0])),
        ('5. 时钟变低，SI 换成 1', 'Q 仍是 0100。'),
        ('6. 上升沿 3：→ 1010', '%s←1，%s←0，%s←1，%s←0。最先进来的那一位现在在 %s，最后进来的在 %s。' % (QS[0], QS[1], QS[2], QS[3], QS[2], QS[0])),
    ]
    reg_panels(doc, 'shift', '1. 移位寄存器：逐个上升沿看数据怎么挪（4 位示例）',
               '课件电路：一串 D 触发器首尾相连（课件是 16 位：$D_0$…$D_{15}$），共用 Clk。SI = serial in。每个上升沿：每一位同时把“自己左边那位的旧值”抄过来 → 整体右移一格。',
               items, seq)
    ax = doc.page('1. 移位寄存器时序图', '浅橙 = Clk=1；黄色虚线 = 上升沿。每条 Q 线都是它上面那条线“晚一个时钟”的拷贝。（初值 0000）')
    sib = [1, 0, 1, 1, 0, 0, 1, 0, 0]; n = 38; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]
    SI = [sib[min((i + 1) // 4, 8)] for i in range(n)]
    q = [0, 0, 0, 0]; QQ = [[], [], [], []]; rows_e = [['上升沿', 'SI（边沿前）', '%s%s%s%s（边沿后）' % tuple(QS), '说明']]; k = 0
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            k += 1; q = [SI[i - 1]] + q[:-1]
            rows_e.append(['第 %d 个 ↑' % k, SI[i - 1], ''.join(map(str, q)), '%d 进入 %s，其余各位右移一格' % (SI[i - 1], QS[0])])
        for j in range(4):
            QQ[j].append(q[j])
    yb = timing(ax, 120, 140, 560, [('Clk', C), ('SI', SI)] + [(QS[j], QQ[j]) for j in range(4)], n, rowh=58, shade=shades(C), edges=edge_list(C), vals=False)
    ax.text(730, 128, '每个上升沿之后的内容', fontsize=10.5, weight='bold', color=GREEN)
    table(ax, 730, 142, [70, 60, 130, 133], 28, [['上升沿', 'SI', '%s%s%s%s' % tuple(QS), '说明']] + [r[:3] + [r[3].replace('，其余各位右移一格', '')] for r in rows_e[1:]], fs=8.8)
    para(ax, 120, yb + 20, '读图方法：%s 是 SI “延迟一个时钟”，%s 是 %s 延迟一个时钟…… 所以一位数据从 SI 走到 %s 需要 4 个上升沿。表里每一行都是上一行整体右移、左边补上新的 SI。'
         % (QS[0], QS[1], QS[0], QS[3]), 1000, 9.2)
    ax = doc.page('2. 解析 Truth table：每一位的下一个值从哪来', '下一状态表 + 课件的 16 位例子 + 为什么不能用锁存器。', legend=False)
    cv = CV(ax, 96, 170, 0.85); cv.mono = True
    draw_reg('shift')(cv, dict(C=0, W=0, SI=0, **{'Q%d' % i: 0 for i in range(4)}))
    para(ax, 46, 290, '$Q_{0,T+1}$ = SI\n$Q_{i,T+1}$ = $Q_{i-1,T}$（i ≥ 1）\n\n右边全是“旧值”（边沿之前的值）。\n所有触发器同时采样，所以每个边沿数据只走一格，不会一口气冲到头。', 360, 9.5, 1.7)
    table(ax, 440, 118, [70] + [80] * 4 + [293], [26, 40, 30],
          [['Clk', '%s 新' % QS[0], '%s 新' % QS[1], '%s 新' % QS[2], '%s 新' % QS[3], '为什么'],
           [UP, 'SI', '旧 ' + QS[0], '旧 ' + QS[1], '旧 ' + QS[2], '每个 D 接的是左边那位的 Q；边沿时采到的是它的旧值。'],
           ['不是 ↑', '旧 ' + QS[0], '旧 ' + QS[1], '旧 ' + QS[2], '旧 ' + QS[3], '触发器只在有效边沿更新 → 保持。']], left={5}, fs=8.8, hl={1})
    ax.text(440, 232, '例：依次移入 1、0、1、1（初值 0000）', fontsize=11, weight='bold', color=GREEN)
    q = [0, 0, 0, 0]; ex = [['上升沿', 'SI'] + QS + ['说明']]
    for k, b in enumerate([1, 0, 1, 1]):
        q = [b] + q[:-1]
        ex.append(['第 %d 个' % (k + 1), b] + q + [['第一个 1 进来', '它挪到第 1 位', '它挪到第 2 位', '它到达最右边；4 位全部装满'][k]])
    table(ax, 440, 248, [80, 50, 50, 50, 50, 50, 353], 28, ex, left={6}, fs=8.8)
    ax.text(440, 410, '课件例子：16 位，移入 0101010101010101', fontsize=11, weight='bold', color=GREEN)
    para(ax, 440, 432, '从左边第一个字符开始，一个时钟送一位。16 个时钟之后：$Q_0$=1、$Q_1$=0、$Q_2$=1、…、$Q_{15}$=0。\n最后送进去的那一位（最右边的 1）停在 $Q_0$；最先送进去的那一位（最左边的 0）被推到最远的 $Q_{15}$。\n'
         '结论：n 位移位寄存器要 n 个时钟才能装满；先进去的位离 SI 最远。', 680, 9.3, 1.7)
    ax.text(440, 540, '为什么必须用触发器（课件 Value- vs Edge-triggered）', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 556, [150, 150, 383], [28, 46, 46],
          [['用什么', '时钟来一次的结果', '说明'],
           ['D 锁存器串联', '0 1 0 1 0 → 0 0 0 0 0', 'Clk=1 时全部透明，最左边的 0 一口气冲过所有级（“flooded”）。'],
           ['D 触发器串联', '0 1 0 1 0 → 0 0 1 0 1', '边沿瞬间各自采旧值，每个时钟只移一位，而且是在时钟变化的那一刻移。']], left={2}, fs=8.8, hl={2})
    notes = [
        '接法：第 0 个触发器的 D 接 SI，其余每个触发器的 D 接前一个的 Q；所有触发器共用 Clk。',
        '每个有效边沿：整体移动一格。$Q_0$←SI，$Q_1$←旧$Q_0$，$Q_2$←旧$Q_1$……一定用“旧值”。',
        '最常见的错误：在同一个边沿里用了刚更新的值（比如先把 $Q_0$ 改了，再用新 $Q_0$ 去改 $Q_1$）。正确做法是先把这一行全部抄下来，再整体右移。',
        '所有触发器是同时采样的。因为 Q 的变化比边沿晚一点点（传播延迟），后一级在边沿那一刻看到的还是前一级的旧值。',
        'n 位要 n 个时钟才能串行装满（课件：16 位 → 16 个 clock cycles）。一位数据从 SI 到最后一级的输出也要 n 个时钟。',
        '顺序：先移入的位走得最远（在 $Q_{n-1}$），最后移入的位在 $Q_0$。题目问“移入 xxxx 之后各位是什么”时注意别写反。',
        '每条 Q 的波形 = 前一条延迟一个时钟周期。画图时可以直接把上一行向右平移一个周期。',
        'SI 也只在边沿被采样：两个边沿之间 SI 的变化无效；SI 应在边沿前后保持稳定（setup/hold）。',
        '初值未知时，未知值也会一格一格被“推”出去：k 个时钟后前 k 位已确定，后面的仍未知。',
        '不能用锁存器搭：透明期间数据会直通多级（课件的 flood 例子）。这是“为什么需要边沿触发”的标准答案。',
        '移位寄存器是“串行进”；一次装入全部位的是 load register（并行进）。最右边的 Q 可以当串行输出。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clk、SI 求各位 / 画波形）', [
            '写下初值一行（例如 0000 或 ????）。',
            '每来一个上升沿：读边沿前的 SI，写在最左边；原来的各位整体右移一格；最右边那位掉出去。',
            '画波形：$Q_0$ = SI 延迟一拍；$Q_1$ = $Q_0$ 延迟一拍……',
            '检查：任何一位都只在上升沿变化，且各位同时变。'])
        ax.text(x, y + 6, '速记表：移入 a、b、c、d（a 最先）', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [94, 70, 70, 70, 70], 26,
              [['上升沿'] + QS, ['初始', '?', '?', '?', '?'], ['1', 'a', '?', '?', '?'], ['2', 'b', 'a', '?', '?'], ['3', 'c', 'b', 'a', '?'], ['4', 'd', 'c', 'b', 'a']], fs=8.8)
        para(ax, x, y + 200, '4 个时钟后：最先进来的 a 在最右边的 $Q_3$，最后进来的 d 在 $Q_0$。', w, 8.8, 1.55, '#C92A2A')
    notes_page(doc, '3. 满分注意事项：移位寄存器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


# ================= 11 加载寄存器 =================
def pdf_load():
    doc = Doc(os.path.join(OUT, '11_加载寄存器.pdf'), '加载寄存器 · Load registers')
    seq = sim_reg('load', [(0, '1011', 0), (1, '1011', 0), (0, '1011', 1), (1, '1011', 1), (0, '0110', 0), (1, '0110', 0)], q=[0, 0, 0, 0])
    items = [
        ('1. Write=0，D=1011，Q=0000', '每一位都是“带使能端的 D 触发器”，所有 EN 接同一根 Write。Write=0 → 每个触发器内部选的是自己的旧 Q。（假设初值 0000）'),
        ('2. 上升沿，Write=0：保持', '虽然来了上升沿，但 EN=0 → 每一位把自己又写了一遍 → Q 仍是 0000。D=1011 被无视。'),
        ('3. Write 变 1（Clk=0）', 'EN=1 → 每个触发器内部改成选外部的 D。数据已经到门口，但还没到边沿，Q 不变。'),
        ('4. 上升沿，Write=1：装入 1011', '4 位同时装入：%s%s%s%s=1011。一次时钟装满全部位（并行装入）。' % tuple(QS)),
        ('5. Write 变 0，D 变成 0110', 'D 变了，但 Write=0 → 进不来。'),
        ('6. 上升沿，Write=0：保持 1011', 'Q 不变。寄存器里的值一直留着，直到下一次 Write=1 的上升沿才会被覆盖。'),
    ]
    reg_panels(doc, 'load', '1. 加载寄存器：Write 控制“写还是不写”（4 位示例）',
               '课件电路：4 个带使能端的 D 触发器，$D_0$…$D_3$ 各自从上面进来，EN 全接 Write，时钟全接 Clk。上升沿且 Write=1 → 一次装入全部 4 位；Write=0 → 保持。',
               items, seq)
    ax = doc.page('1. 加载寄存器时序图', '浅橙 = Clk=1；黄色虚线 = 上升沿。总线格子里的 4 个数字依次是第 0、1、2、3 位。只有“上升沿那一刻 Write=1”才装入。')
    n = 26; C = [(1 if (i % 4) >= 2 else 0) for i in range(n)]
    D = ['1011'] * 8 + ['0110'] * 12 + ['1100'] * 6
    Wr = [0] * 5 + [1] * 3 + [0] * 3 + [1] * 2 + [0] * 4 + [1] * 4 + [0] * 5
    Q, q, k = [], '0000', 0; rows_e = [['上升沿', 'Write（边沿前）', 'D（边沿前）', 'Q（边沿后）', '说明']]
    for i in range(n):
        if i and C[i] == 1 and C[i - 1] == 0:
            k += 1
            if Wr[i - 1]:
                q = D[i - 1]
            rows_e.append(['第 %d 个 ↑' % k, Wr[i - 1], D[i - 1], q, '装入 D' if Wr[i - 1] else '保持（Write=0）'])
        Q.append(q)
    rows_e[4][-1] = '保持：Write 的脉冲没盖住边沿'; rows_e[6][-1] = '保持：Write 在边沿前刚好回到 0，新的 D=1100 没进来'
    yb = timing(ax, 170, 150, 950, [('Clk', C), ('Write', Wr), ('%s%s%s%s' % tuple(DS), D), ('%s%s%s%s' % tuple(QS), Q)], n, rowh=56,
                shade=shades(C), edges=edge_list(C), vals=False)
    ax.text(170, yb + 28, '每个上升沿发生了什么', fontsize=10.5, weight='bold', color=GREEN)
    table(ax, 170, yb + 42, [100, 130, 120, 120, 480], 26, rows_e, fs=9, hl={i for i, r in enumerate(rows_e) if r[-1] == '装入 D'})
    ax = doc.page('2. 解析 Truth table：Write 和时钟怎样决定 Q', '对每一位都成立。内部就是“带使能端的 D 触发器”那张表重复 n 次。', legend=False)
    cv = CV(ax, 104, 200, 0.82); cv.mono = True
    draw_reg('load')(cv, dict(C=0, W=0, **{'D%d' % i: 0 for i in range(4)}, **{'Q%d' % i: 0 for i in range(4)}))
    para(ax, 46, 345, '每一位：$Q_{i,T+1}$ = Write·$D_i$ + %s·$Q_{i,T}$\n（只在上升沿生效）\n\nWrite=1：选外部的 $D_i$ → 装入。\nWrite=0：选自己的 $Q_i$ → 保持。\n时钟一直在走，没有被 Write 挡住。' % ov('Write'), 360, 9.5, 1.7)
    table(ax, 440, 118, [80, 80, 90, 433], 32,
          [['Clk', 'Write', '$Q_{T+1}$', '为什么'],
           [UP, '1', 'D', 'EN=1 → 每个触发器内部的 2 选 1 选中外部 D → 上升沿装入全部 n 位。'],
           [UP, '0', QT, 'EN=0 → 2 选 1 选中自己的 Q → 上升沿写回旧值 → 看起来没变。'],
           ['不是 ↑', 'X', QT, '没有有效边沿，触发器不更新。Write 是 0 是 1 都一样。']], left={3}, fs=8.8, hl={1})
    ax.text(440, 276, '输入怎么变 → 输出怎么变', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 292, [260, 120, 303], 30,
          [['发生了什么', 'Q 的反应', '说明'],
           ['上升沿时 Write=1', '变成 D（全部位）', '并行装入，一个时钟完成'],
           ['上升沿时 Write=0', '不变', 'D 是什么都无所谓'],
           ['两个上升沿之间 Write 0→1→0', '不变', 'Write 只在边沿被“看”一次'],
           ['Write=1 期间 D 在变', '不变，直到边沿', '装入的是边沿前一瞬间的 D'],
           ['Write 一直是 1', '每个上升沿都装入', '退化成没有使能端的基本寄存器']], left={2}, fs=8.8)
    ax.text(440, 500, '和另外两种寄存器对比', fontsize=11, weight='bold', color=GREEN)
    table(ax, 440, 516, [130, 180, 180, 193], [28, 40, 40, 40],
          [['', '加载寄存器 load', '移位寄存器 shift', '基本寄存器'],
           ['数据怎么进', '并行：n 位一起', '串行：一次一位（SI）', '并行：n 位一起'],
           ['装满 n 位', '1 个时钟', 'n 个时钟', '1 个时钟'],
           ['怎样保持', 'Write=0', '—', '只能让 D 不变']], fs=8.6)
    notes = [
        '结构：n 个“带使能端的 D 触发器”并排，$D_i$ 各接各的，所有 EN 接同一根 Write，所有时钟接 Clk。',
        '装入条件要同时满足两个：① 有效（上升）边沿；② 边沿那一刻 Write=1。缺一个都不装。',
        'Write=0 时寄存器一直保持原值，不管 D 怎么变、来多少个时钟（课件：maintain values until overwritten by setting EN high）。',
        'Write 和 D 一样只在边沿被采样。Write 在两个上升沿之间升起又落下 → 没写进去。这是最常见的陷阱。',
        'Write=1 不是“透明”。就算 Write 一直为 1，Q 也只在上升沿变化。',
        '所有位同时装入、同时变化（并行）。和移位寄存器不同，它不需要 n 个时钟。',
        '装入的是边沿前一瞬间的 D。Write=1 期间 D 中途变了，以边沿前最后的值为准。',
        '实现方式是每一位前面一个 2 选 1（EN=0 选旧 Q，EN=1 选 D），不是用 AND 门去挡时钟。',
        '初值未知且 Write 一直为 0 → 一直未知。第一次 Write=1 的上升沿之后才有确定值（或用 reset）。',
        'Write 也常叫 Load / EN / WE。CPU 里的寄存器基本都是这种：时钟一直在跑，靠 Write 信号决定哪个寄存器在这个周期更新。',
        '画总线波形时：Q 的格子边界只可能出现在“Write=1 的上升沿”处，其它地方不许有边界。',
    ]

    def right(ax, x, y, w):
        y = steps_box(ax, x, y, w, '做题步骤（给 Clk、Write、D 画 Q）', [
            '画出所有上升沿的竖虚线。',
            '每条虚线上先看边沿前的 Write。',
            'Write=0 → 这条虚线跳过，Q 照旧。',
            'Write=1 → 读边沿前的 D（每一位），Q 整体变成它。',
            '虚线之间 Q 不变；第一次装入之前按题目给的初值（没给就是未知）。'])
        ax.text(x, y + 6, '特性表（背）', fontsize=11, weight='bold', color=GREEN, va='top')
        table(ax, x, y + 30, [90, 90, 90, 104], 26,
              [['Clk', 'Write', '$Q_{T+1}$', '功能'], [UP, '1', 'D', '装入'], [UP, '0', QT, '保持'], ['不是 ↑', 'X', QT, '保持']], fs=8.8)
        para(ax, x, y + 150, '一句话：时钟决定“什么时候可以变”，Write 决定“这次要不要变”，D 决定“变成什么”。', w, 9, 1.6, '#C92A2A')
    notes_page(doc, '3. 满分注意事项：加载寄存器', '下面每一条都是会被扣分的点。', notes, right)
    doc.close()


if __name__ == '__main__':
    pdf_reg(); pdf_shift(); pdf_load()
    print('ok')
