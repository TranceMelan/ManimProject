# Mọi người xem nhanh trước khi sửa nha:
#
#  - Video có 8 cảnh, mỗi cảnh là 1 class, theo thứ tự:
#      S0_Intro            mở đầu: logo, tên đề tài, mục lục
#      S1_Definitions      định nghĩa liên tục, eps - delta
#      S2_EVT              định lý giá trị cực trị + chứng minh
#      S3_IVT              định lý giá trị trung gian + chứng minh
#      S4_Example          ví dụ học thuật: x^3 - 3x + 1
#      S5_Counterexamples  phản ví dụ
#      S6_WaterTank        ứng dụng: thiết kế bể nước hở
#      S7_Summary          tổng kết
#
#  - Chạy 1 cảnh:   manim -qh --fps 30 continuity.py S0_Intro
#    chạy đủ 8 cảnh rồi ghép lại bằng ffmpeg (lệnh ở cuối file)
#
#  - Dòng "# câu N" là chỗ bắt đầu câu thoại số N.
#    Mấy cái self.wait(...) ngay trước nó là thời gian chờ cho khớp giọng đọc,
#    đừng sửa mấy số đó kẻo lệch tiếng.
#
#  - Ảnh để trong thư mục assets/: logo trường + ảnh 3 nhà toán học (lấy từ Wikipedia)
#
#  - Nhóm có dùng AI hỗ trợ viết code, chỗ nào dùng thì có ghi chú ngay chỗ đó.
#
# File chia làm 4 phần:
#   1. Cài đặt chung (màu, trục)
#   2. Hàm phụ (viết chữ, đóng khung, thẻ ảnh)
#   3. Các hàm toán dùng trong video
#   4. Các cảnh của video

from manim import *
import numpy as np
import os


# ------------------------------------------------------------
# 1. CÀI ĐẶT CHUNG
# muốn đổi màu cả video thì sửa ở đây là được
# ------------------------------------------------------------
BG = "#000000"           # nền đen
C_F = "#9FE29F"          # đường đồ thị chính (xanh lá nhạt)
C_N = "#FFD166"          # vàng, để làm nổi
C_G = "#FF9F43"          # cam, chỗ đúng / giá trị lớn nhất
C_R = "#FF6B6B"          # đỏ, chỗ sai / mâu thuẫn
C_P = "#E879F9"          # hồng
GREY_T = "#BBBBBB"       # xám, cho chữ phụ
PANEL = "#000000"        # nền khung ảnh
GRAD = ("#2EE6D6", "#F472D0")   # 2 màu chuyển cho chữ tiêu đề ở đầu video

config.background_color = BG

# kiểu trục dùng chung cho mấy cái đồ thị
AX_CFG = {"stroke_color": WHITE, "stroke_width": 2, "include_ticks": False}


# ------------------------------------------------------------
# 2. HÀM PHỤ
# ------------------------------------------------------------

# viết chữ thường. Dùng latex hết cho cùng 1 font
# tôi có sài AI ở khúc này để đổi mấy ký hiệu ε, δ, → sang latex
def T(s, size=30, color=WHITE, weight=NORMAL):
    for a, b in [("<", "$<$"), (">", "$>$"), ("&", r"\&"), ("ε", r"$\varepsilon$"), ("δ", r"$\delta$"),
                 ("→", r"$\to$"), ("≠", r"$\neq$"), ("⇒", r"$\Rightarrow$"), ("•", r"$\bullet$"), ("·", r"$\cdot$")]:
        s = s.replace(a, b)
    if weight == BOLD:
        s = r"\textbf{" + s + "}"
    return Tex(r"\mbox{" + s + "}", font_size=size * 1.3, color=color)

# viết 1 đoạn chữ dài có công thức, canh trái
def TX(s, size=34, color=WHITE):
    return Tex(s, font_size=size, color=color, tex_environment="flushleft")

# viết công thức toán
def M(s, size=38, color=WHITE):
    return MathTex(s, font_size=size, color=color)

# dòng tiêu đề ở góc trên bên trái mỗi cảnh
def header(tag, title):
    g = VGroup(T(tag, 22, GREY_T, weight=BOLD), T(title, 34, weight=BOLD))
    return g.arrange(RIGHT, buff=0.3, aligned_edge=DOWN).to_corner(UL, buff=0.42)

# đóng khung quanh 1 thứ gì đó
def boxed(mob, color=C_N):
    rect = SurroundingRectangle(mob, buff=0.28, stroke_color=color, stroke_width=1.5)
    return VGroup(rect, mob)

# khung cho định nghĩa / định lý
def theorem_box(title, body, color=C_N):
    content = VGroup(T(title, 24, weight=BOLD), body)
    content.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return boxed(content, color)

# thẻ ảnh nhà toán học (ảnh lấy từ Wikipedia, để trong assets/)
# không có ảnh thì nó tự vẽ hình bóng thay vào
def portrait(file, name, years, role, h=3.0):
    w = h * 0.8
    frame = Rectangle(width=w, height=h, stroke_color=GREY_T,
                             stroke_width=2, fill_color=PANEL, fill_opacity=1)
    path = os.path.join("assets", file)
    if os.path.exists(path):
        pic = ImageMobject(path).scale_to_fit_height(h - 0.12)
        if pic.width > w - 0.12:
            pic.scale_to_fit_width(w - 0.12)
        pic.move_to(frame)
    else:
        k = h / 3.0
        head = Circle(radius=0.42 * k).set_fill(GREY_D, 1).set_stroke(width=0)
        head.move_to(frame.get_center() + UP * 0.35 * k)
        body = Ellipse(width=1.9 * k, height=1.5 * k).move_to(frame.get_bottom() + UP * 0.45 * k)
        body = Intersection(body, frame.copy()).set_fill(GREY_D, 1).set_stroke(width=0)
        hint = T("assets/" + file, 13, GREY_T).move_to(frame.get_top() + DOWN * 0.25)
        pic = VGroup(head, body, hint)
    cap = VGroup(T(name, 24, weight=BOLD), T(years, 18, GREY_T), T(role, 18, C_N),
                 T("Image source: Wikipedia", 14, GREY_T))
    cap.arrange(DOWN, buff=0.08).next_to(frame, DOWN, buff=0.18)
    return Group(frame, pic, cap)

# dấu tick
def check():
    return M(r"\checkmark", 40, C_G)

# dấu x đỏ
def xmark():
    return M(r"\times", 40, C_R)

# tìm nghiệm bằng phương pháp chia đôi
def chia_doi(f, lo, hi, it=60):
    for _ in range(it):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


# ------------------------------------------------------------
# 3. CÁC HÀM TOÁN DÙNG TRONG VIDEO
# ------------------------------------------------------------

# hàm mẫu ở phần định nghĩa
def f_def(x):
    return 0.9 + 0.32 * x + 0.55 * np.sin(0.9 * x)


# hàm mẫu ở phần EVT
def f_evt(x):
    return 2.1 + 1.0 * np.sin(x - 0.4) + 0.35 * np.sin(2.6 * x)


# hàm mẫu ở phần IVT: N = 2.2, g(x) = f(x) - N
NV = 2.2


def g_ivt(x):
    return 0.45 * (x - 3) - 1.0 * np.sin(1.5 * (x - 3))


def f_ivt(x):
    return NV + g_ivt(x)


# ví dụ học thuật: f(x) = x^3 - 3x + 1
def f_ex(x):
    return x ** 3 - 3 * x + 1


# bể nước: tấm thép 30x30 cm, cắt 4 góc cạnh x -> thể tích V(x) = x(30 - 2x)^2
SHEET = 30.0


def V(x):
    return x * (SHEET - 2 * x) ** 2


# ------------------------------------------------------------
# 4. CÁC CẢNH CỦA VIDEO
# ------------------------------------------------------------


# ------------------------------------------------------------
# CẢNH 0 - MỞ ĐẦU
# logo trường -> "Calculus 1" -> tên đề tài -> 2 đồ thị liền / đứt -> mục lục
# ------------------------------------------------------------
class S0_Intro(Scene):
    def construct(self):
        # logo trường + tên trường trên nền trắng
        logo = ImageMobject("assets/logo.png").scale_to_fit_height(1.3)
        ten = VGroup(Text("VIETNAM NATIONAL UNIVERSITY HO CHI MINH CITY", font="Arial", weight=BOLD,
                          color="#1589DB", font_size=22),
                     Text("HO CHI MINH CITY UNIVERSITY OF TECHNOLOGY", font="Arial", weight=BOLD,
                          color="#042C92", font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        noi_dung = Group(logo, ten).arrange(RIGHT, buff=0.35)
        nen = RoundedRectangle(width=noi_dung.width + 0.6, height=noi_dung.height + 0.4, corner_radius=0.3,
                               fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(noi_dung)
        banner = Group(nen, noi_dung)
        self.play(FadeIn(banner), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(banner))

        # chữ "Calculus 1" rồi tới tên đề tài + tên nhóm
        c1 = T("Calculus 1", 60, weight=BOLD).set_color_by_gradient(*GRAD)
        self.play(Write(c1), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(c1))
        tt = VGroup(T("Continuity, the Extreme Value Theorem", 50, weight=BOLD),
                    T("and the Intermediate Value Theorem", 50, weight=BOLD),
                    T("Group CA04", 36, weight=BOLD)).arrange(DOWN, buff=0.3)
        tt.set_color_by_gradient(*GRAD)
        self.play(Write(tt), run_time=2)
        self.wait(2)
        self.play(FadeOut(tt))

        # 2 đồ thị: bên trái vẽ 1 nét, bên phải bị đứt
        def make_axes():
            return Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=5.6, y_length=3.4,
                        tips=False, axis_config=AX_CFG)
        axL = make_axes().move_to(LEFT * 3.5 + DOWN * 0.4)
        axR = make_axes().move_to(RIGHT * 3.5 + DOWN * 0.4)
        fL = axL.plot(lambda x: 1.9 + 0.9 * np.sin(1.1 * x) + 0.15 * x, x_range=[0.3, 5.7],
                      color=C_F, stroke_width=6)
        r1 = axR.plot(lambda x: 1.2 + 0.5 * np.sin(1.3 * x) + 0.1 * x, x_range=[0.3, 3],
                      color=C_R, stroke_width=6)
        r2 = axR.plot(lambda x: 3.0 + 0.4 * np.sin(1.3 * x), x_range=[3, 5.7],
                      color=C_R, stroke_width=6)

        # câu 1
        self.play(Create(axL), Create(axR), run_time=1)
        # chấm vàng chạy theo đường như cây bút
        pen = Dot(color=C_N, radius=0.09).move_to(fL.get_start())
        self.add(pen)
        self.play(Create(fL), MoveAlongPath(pen, fL), run_time=3.2, rate_func=linear)
        labL = T("continuous: one stroke", 24, C_G).next_to(axL, DOWN, buff=0.3)
        self.play(FadeIn(labL, shift=UP * 0.15))

        self.wait(3.0)
        # câu 2
        pen2 = Dot(color=C_N, radius=0.09).move_to(r1.get_start())
        self.add(pen2)
        self.play(Create(r1), MoveAlongPath(pen2, r1), run_time=1.8, rate_func=linear)
        self.play(pen2.animate(path_arc=-PI / 1.5).move_to(r2.get_start()), run_time=0.9)
        self.play(Create(r2), MoveAlongPath(pen2, r2), run_time=1.6, rate_func=linear)
        # đánh dấu chỗ bị nhảy
        jump = DashedLine(r1.get_end(), r2.get_start(), color=C_N, dash_length=0.08)
        labR = T("discontinuous: the pen must lift", 24, C_R).next_to(axR, DOWN, buff=0.3)
        self.play(Create(jump), FadeIn(labR, shift=UP * 0.15))

        self.wait(0.3)
        # câu 3
        self.play(*[FadeOut(m) for m in [axL, axR, fL, r1, r2, pen, pen2, jump, labL, labR]])
        # mục lục video
        items = [
            ("Part A", "Definitions of continuity"),
            ("Part A", "Theorem 1 - Extreme Value Theorem  + proof"),
            ("Part A", "Theorem 2 - Intermediate Value Theorem  + proof"),
            ("Part A", "Academic example"),
            ("Part A", "Counterexamples"),
            ("Part B", "Practical application: designing a water tank"),
        ]
        rows = VGroup()
        for i, (p, s) in enumerate(items):
            num = T(f"{i + 1}", 26, BG, weight=BOLD)
            circ = Circle(radius=0.24, fill_color=C_N if p == "Part A" else C_F,
                          fill_opacity=1, stroke_width=0)
            num.move_to(circ)
            rows.add(VGroup(VGroup(circ, num), T(s, 28)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.55)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.35),
                  run_time=3.5)
        self.wait(4.0)


# ------------------------------------------------------------
# CẢNH 1 - ĐỊNH NGHĨA
# liên tục tại 1 điểm, eps - delta, liên tục trên đoạn [a,b], ảnh 3 nhà toán học
# ------------------------------------------------------------
class S1_Definitions(Scene):
    def construct(self):
        hd = header("PART A · 1", "Basic Definitions")
        self.play(FadeIn(hd, shift=DOWN * 0.2))

        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 4.2, 1], x_length=6.6, y_length=4.6,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 3.2 + DOWN * 0.55)
        curve = ax.plot(f_def, x_range=[0.3, 6.2], color=C_F, stroke_width=5)
        a = 3.2
        fa = f_def(a)
        P = ax.c2p(a, fa)
        a_lab = M("a", 36).next_to(ax.c2p(a, 0), DOWN, buff=0.15)
        fa_lab = M("f(a)", 32).next_to(ax.c2p(0, fa), LEFT, buff=0.12)
        vline = DashedLine(ax.c2p(a, 0), P, color=GREY_T, dash_length=0.07)
        hline = DashedLine(ax.c2p(0, fa), P, color=GREY_T, dash_length=0.07)
        dotP = Dot(P, color=C_N, radius=0.09)

        # câu 4
        self.play(Create(ax), run_time=1)
        self.play(Create(curve), run_time=1.6)
        self.play(Create(vline), Create(hline), FadeIn(a_lab), FadeIn(fa_lab), GrowFromCenter(dotP))

        self.wait(0.3)
        # câu 5
        # 2 chấm chạy từ trái và phải về điểm a (minh họa giới hạn)
        t = ValueTracker(0)
        xl = lambda: a - (a - 0.6) * (1 - t.get_value())
        xr = lambda: a + (6.0 - a) * (1 - t.get_value())
        dl = always_redraw(lambda: Dot(ax.c2p(xl(), f_def(xl())), color=C_G, radius=0.08))
        dr = always_redraw(lambda: Dot(ax.c2p(xr(), f_def(xr())), color=C_P, radius=0.08))
        tl = always_redraw(lambda: Triangle(color=C_G, fill_opacity=1).scale(0.09)
                           .move_to(ax.c2p(xl(), 0) + DOWN * 0.02))
        tr = always_redraw(lambda: Triangle(color=C_P, fill_opacity=1).scale(0.09)
                           .move_to(ax.c2p(xr(), 0) + DOWN * 0.02))
        self.add(dl, dr, tl, tr)
        lim_lr = M(r"\lim_{x\to a^-} f(x)", 36, C_G)
        lim_rr = M(r"\lim_{x\to a^+} f(x)", 36, C_P)
        eqs = VGroup(lim_lr, M("=", 36), lim_rr).arrange(RIGHT, buff=0.2)
        eqs.move_to(RIGHT * 3.6 + UP * 1.7)
        self.play(t.animate.set_value(0.985), run_time=3.5, rate_func=smooth)
        self.play(Write(eqs))

        self.wait(0.3)
        # câu 6
        # định nghĩa 1: liên tục tại 1 điểm
        dfn = VGroup(TX(r"$f$ is \textbf{continuous at} $a$ if", 34),
                     M(r"\lim_{x\to a} f(x) = f(a)", 46)).arrange(DOWN, buff=0.3)
        dbox = theorem_box("DEFINITION 1", dfn).move_to(RIGHT * 3.6 + DOWN * 0.6)
        self.play(FadeIn(dbox, shift=UP * 0.2))
        self.play(Indicate(dotP, color=C_N, scale_factor=1.8))

        self.wait(3.4)
        # câu 7
        self.remove(dl, dr, tl, tr)
        self.play(*[FadeOut(m) for m in [ax, curve, vline, hline, a_lab, fa_lab, dotP, eqs]],
                  dbox.animate.scale(0.85).move_to(LEFT * 3.7 + UP * 1.35))
        conds = VGroup(
            TX(r"1.\ \ $f(a)$ is defined", 32),
            TX(r"2.\ \ $\displaystyle\lim_{x\to a} f(x)$ exists", 32),
            TX(r"3.\ \ $\displaystyle\lim_{x\to a} f(x) = f(a)$", 32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 3.4 + UP * 1.35)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in conds], lag_ratio=0.5),
                  run_time=2.2)

        # 3 đồ thị nhỏ: liền / bị lỗ / bị nhảy
        def mini(kind):
            mx = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=3.4, y_length=2.3,
                      tips=False, axis_config=AX_CFG)
            g = VGroup(mx)
            if kind == "ok":
                g.add(mx.plot(lambda x: 0.8 + 0.5 * x - 0.06 * x * x, x_range=[0.2, 3.8],
                              color=C_G, stroke_width=4))
                g.add(Dot(mx.c2p(2, 0.8 + 1 - 0.24), color=C_N, radius=0.07))
                lab, mk = "continuous", check()
            elif kind == "hole":
                g.add(mx.plot(lambda x: 0.6 + 0.5 * x, x_range=[0.2, 3.8], color=C_R,
                              stroke_width=4))
                g.add(Circle(radius=0.08, color=C_R, stroke_width=3)
                      .set_fill(BG, 1).move_to(mx.c2p(2, 1.6)))
                g.add(Dot(mx.c2p(2, 2.6), color=C_R, radius=0.07))
                lab, mk = "hole:  lim ≠ f(a)", xmark()
            else:
                g.add(mx.plot(lambda x: 0.6 + 0.2 * x, x_range=[0.2, 2], color=C_R,
                              stroke_width=4))
                g.add(mx.plot(lambda x: 1.9 + 0.2 * x, x_range=[2, 3.8], color=C_R,
                              stroke_width=4))
                g.add(Circle(radius=0.08, color=C_R, stroke_width=3)
                      .set_fill(BG, 1).move_to(mx.c2p(2, 1.0)))
                g.add(Dot(mx.c2p(2, 2.3), color=C_R, radius=0.07))
                lab, mk = "jump:  no limit", xmark()
            g.add(M("a", 28).next_to(mx.c2p(2, 0), DOWN, buff=0.1))
            cap = VGroup(mk.scale(0.8), T(lab, 22)).arrange(RIGHT, buff=0.15)
            cap.next_to(mx, DOWN, buff=0.35)
            return VGroup(g, cap)

        minis = VGroup(mini("ok"), mini("hole"), mini("jump")).arrange(RIGHT, buff=0.9)
        minis.move_to(DOWN * 1.9)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in minis], lag_ratio=0.4),
                  run_time=2.4)

        self.wait(2.0)
        # câu 8
        self.play(*[FadeOut(m) for m in [dbox, conds, minis]])
        # ảnh 3 nhà toán học
        cards = Group(
            portrait("bolzano.png", "Bernard Bolzano", "1781 - 1848", "1817: continuity, IVT"),
            portrait("cauchy.png", "Augustin-Louis Cauchy", "1789 - 1857", "1821: Cours d'analyse"),
            portrait("weierstrass.png", "Karl Weierstrass", "1815 - 1897", "epsilon-delta, EVT"),
        ).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.45),
                  run_time=2.6)

        self.wait(2.6)
        # câu 9
        self.play(FadeOut(cards))
        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 4.2, 1], x_length=6.6, y_length=4.6,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 3.2 + DOWN * 0.55)
        curve = ax.plot(f_def, x_range=[0.3, 6.2], color=C_F, stroke_width=5)
        P = ax.c2p(a, fa)
        a_lab = M("a", 36).next_to(ax.c2p(a, 0), DOWN, buff=0.15)
        fa_lab = M("f(a)", 32).next_to(ax.c2p(0, fa), LEFT, buff=0.12)
        dotP = Dot(P, color=WHITE, radius=0.08)
        xs = np.linspace(0.3, 6.2, 3000)
        ys = f_def(xs)

        # tìm delta theo eps
        # tôi có sài AI ở khúc này để tính delta bằng số cho chính xác
        def delta_for(eps):
            bad = np.abs(xs - a)[np.abs(ys - fa) >= eps]
            d = bad.min() if bad.size else 3
            return 0.85 * d

        # dải eps (vàng) và cửa sổ delta (xanh), tự vẽ lại mỗi khi eps đổi
        eps = ValueTracker(1.0)

        def eps_band():
            e = eps.get_value()
            r = Rectangle(width=ax.x_length, height=ax.c2p(0, fa + e)[1] - ax.c2p(0, fa - e)[1],
                          stroke_width=0, fill_color=C_N, fill_opacity=0.16)
            r.move_to([ax.c2p(3.25, 0)[0], ax.c2p(0, fa)[1], 0])
            lines = VGroup(*[DashedLine(ax.c2p(0, fa + s * e), ax.c2p(6.5, fa + s * e),
                                        color=C_N, stroke_width=2, dash_length=0.08)
                             for s in (1, -1)])
            return VGroup(r, lines)

        def delta_band():
            d = delta_for(eps.get_value())
            r = Rectangle(width=ax.c2p(a + d, 0)[0] - ax.c2p(a - d, 0)[0], height=ax.y_length,
                          stroke_width=0, fill_color=C_G, fill_opacity=0.16)
            r.move_to([ax.c2p(a, 0)[0], ax.c2p(0, 2.1)[1], 0])
            lines = VGroup(*[DashedLine(ax.c2p(a + s * d, 0), ax.c2p(a + s * d, 4.2),
                                        color=C_G, stroke_width=2, dash_length=0.08)
                             for s in (1, -1)])
            piece = ax.plot(f_def, x_range=[a - d, a + d], color=C_G, stroke_width=8)
            return VGroup(r, lines, piece)

        def eps_brace():
            e = eps.get_value()
            b = BraceBetweenPoints(ax.c2p(6.45, fa), ax.c2p(6.45, fa + e), RIGHT, buff=0.05)
            b.set_color(C_N)
            return VGroup(b, M(r"\varepsilon", 34, C_N).next_to(b, RIGHT, buff=0.08))

        def delta_brace():
            d = delta_for(eps.get_value())
            b = BraceBetweenPoints(ax.c2p(a + d, 0), ax.c2p(a, 0), DOWN, buff=0.45)
            b.set_color(C_G)
            return VGroup(b, M(r"\delta", 34, C_G).next_to(b, DOWN, buff=0.06))

        # định nghĩa 2: eps - delta
        formula = VGroup(
            M(r"\forall\,\varepsilon>0,\ \ \exists\,\delta>0 :", 40),
            M(r"|x-a|<\delta \ \Longrightarrow\ |f(x)-f(a)|<\varepsilon", 40),
        ).arrange(DOWN, buff=0.3)
        formula[0][0][1].set_color(C_N); formula[0][0][6].set_color(C_G)
        fbox = theorem_box("DEFINITION 2  (epsilon - delta)", formula).scale(0.9)
        fbox.move_to(RIGHT * 3.65 + UP * 1.45)
        self.play(Create(ax), Create(curve), FadeIn(a_lab), FadeIn(fa_lab), FadeIn(dotP),
                  run_time=1.5)
        self.play(FadeIn(fbox, shift=UP * 0.2))

        self.wait(9.0)
        # câu 10
        eb = always_redraw(eps_band)
        ebr = always_redraw(eps_brace)
        step1 = VGroup(T("Challenge:", 22, C_N, weight=BOLD), T("a band of half-height ε", 22))
        step2 = VGroup(T("Response:", 22, C_G, weight=BOLD), T("a window of half-width δ", 22))
        for s in (step1, step2):
            s.arrange(RIGHT, buff=0.2)
        steps = VGroup(step1, step2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.move_to(RIGHT * 3.95 + DOWN * 0.75)
        self.play(FadeIn(eb), FadeIn(ebr), FadeIn(step1, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(0.8)
        db = always_redraw(delta_band)
        dbr = always_redraw(delta_brace)
        self.play(FadeIn(db), FadeIn(dbr), FadeIn(step2, shift=RIGHT * 0.2), run_time=1.2)
        self.bring_to_front(dotP)

        self.wait(5.5)
        # câu 11
        note = T("ε → small   ⇒   δ shrinks, but always exists", 19, C_F)
        note.next_to(steps, DOWN, buff=0.5).align_to(steps, LEFT)
        # cho eps nhỏ dần, delta cũng nhỏ theo
        self.play(eps.animate.set_value(0.28), run_time=3.5, rate_func=smooth)
        self.play(FadeIn(note))
        self.play(eps.animate.set_value(0.6), run_time=1.5)

        self.wait(0.3)
        # câu 12
        eb.clear_updaters(); db.clear_updaters(); ebr.clear_updaters(); dbr.clear_updaters()
        self.play(*[FadeOut(m) for m in [eb, db, ebr, dbr, steps, note, fbox, curve, dotP,
                                         a_lab, fa_lab]])
        # định nghĩa 3: liên tục trên đoạn [a,b]
        A, B = 1.2, 5.4
        seg = ax.plot(f_def, x_range=[A, B], color=C_F, stroke_width=6)
        dA = Dot(ax.c2p(A, f_def(A)), color=C_N, radius=0.09)
        dB = Dot(ax.c2p(B, f_def(B)), color=C_N, radius=0.09)
        la = M("a", 36).next_to(ax.c2p(A, 0), DOWN, buff=0.15)
        lb = M("b", 36).next_to(ax.c2p(B, 0), DOWN, buff=0.15)
        brk = M("[", 60, C_N).move_to(ax.c2p(A, 0))
        brk2 = M("]", 60, C_N).move_to(ax.c2p(B, 0))
        arrA = Arrow(ax.c2p(A + 0.9, f_def(A + 0.9)) + UP * 0.45, ax.c2p(A, f_def(A)) + UP * 0.2,
                     color=C_G, buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        arrB = Arrow(ax.c2p(B - 0.9, f_def(B - 0.9)) + UP * 0.5, ax.c2p(B, f_def(B)) + UP * 0.2,
                     color=C_P, buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        conds = VGroup(
            TX(r"$f$ is \textbf{continuous on} $[a,b]$ if:", 32),
            TX(r"$\bullet$\ continuous at every $x\in(a,b)$", 30),
            TX(r"$\bullet$\ from the right at $a$:\ $\displaystyle\lim_{x\to a^+}f(x)=f(a)$", 30),
            TX(r"$\bullet$\ from the left at $b$:\ \ $\displaystyle\lim_{x\to b^-}f(x)=f(b)$", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conds[2].set_color(C_G)
        conds[3].set_color(C_P)
        cbox = theorem_box("DEFINITION 3", conds).scale(0.92).move_to(RIGHT * 3.55 + DOWN * 0.3)
        self.play(Create(seg), FadeIn(brk), FadeIn(brk2), FadeIn(la), FadeIn(lb), run_time=1.5)
        self.play(FadeIn(dA), FadeIn(dB), FadeIn(cbox, shift=UP * 0.2))
        self.play(GrowArrow(arrA), GrowArrow(arrB))
        self.wait(4.2)


# ------------------------------------------------------------
# CẢNH 2 - ĐỊNH LÝ EVT (giá trị cực trị)
# phát biểu, hình minh họa, chứng minh 2 bước
# ------------------------------------------------------------
class S2_EVT(Scene):
    def construct(self):
        hd = header("PART A · 2", "Theorem 1 - Extreme Value Theorem (EVT)")
        # câu 13
        self.play(FadeIn(hd, shift=DOWN * 0.2))

        self.wait(2.4)
        # câu 14
        # phát biểu định lý
        # tôi có edit phần này (xuống dòng lại cho dễ đọc)
        stmt = TX(r"If $f$ is continuous on a \textbf{closed} interval $[a,b]$, then $f$ attains\\ "
                  r"an absolute maximum value $f(d)$ and an absolute minimum value $f(c)$\\ "
                  r"for some numbers $c,d\in[a,b]$.", 32)
        sbox = theorem_box("THEOREM 1  (EVT)", stmt).move_to(UP * 1.75)
        self.play(FadeIn(sbox, shift=UP * 0.2), run_time=1.2)

        self.wait(6.5)
        # câu 15
        # ảnh Weierstrass
        card = portrait("weierstrass.png", "Karl Weierstrass", "1815 - 1897",
                        "proved the EVT (1860s)", h=2.8)
        card.move_to(RIGHT * 4.6 + DOWN * 1.55)
        self.play(FadeIn(card, shift=LEFT * 0.3))

        ax = Axes(x_range=[0, 6.3, 1], y_range=[0, 4, 1], x_length=7.4, y_length=4.0,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 2.2 + DOWN * 1.55)
        A, B = 0.6, 5.7
        xs = np.linspace(A, B, 4000)
        ys = f_evt(xs)
        d_, c_ = xs[ys.argmax()], xs[ys.argmin()]
        Mv, mv = ys.max(), ys.min()
        curve = ax.plot(f_evt, x_range=[A, B], color=C_F, stroke_width=5)
        ends = VGroup(Dot(ax.c2p(A, f_evt(A)), color=C_F), Dot(ax.c2p(B, f_evt(B)), color=C_F))
        la = M("a", 32).next_to(ax.c2p(A, 0), DOWN, buff=0.12)
        lb = M("b", 32).next_to(ax.c2p(B, 0), DOWN, buff=0.12)

        self.wait(4.5)
        # câu 16
        self.play(Create(ax), FadeIn(la), FadeIn(lb), run_time=1)
        self.play(Create(curve), FadeIn(ends), run_time=1.5)
        # đường ngang quét từ trên xuống, chạm đồ thị chỗ nào thì đó là max
        yT = ValueTracker(4.0)
        sweep = always_redraw(lambda: Line(ax.c2p(A - 0.3, yT.get_value()),
                                           ax.c2p(B + 0.3, yT.get_value()),
                                           color=C_G, stroke_width=3))
        self.add(sweep)
        self.play(yT.animate.set_value(Mv), run_time=2.0, rate_func=smooth)
        dmax = Dot(ax.c2p(d_, Mv), color=C_G, radius=0.1)
        lmax = M(r"\text{max } f(d)", 30, C_G).next_to(dmax, UP, buff=0.12)
        self.play(GrowFromCenter(dmax), FadeIn(lmax))
        sweep.clear_updaters()
        self.play(FadeOut(sweep), run_time=0.3)
        # quét từ dưới lên thì ra min
        yB = ValueTracker(0.0)
        sweep2 = always_redraw(lambda: Line(ax.c2p(A - 0.3, yB.get_value()),
                                            ax.c2p(B + 0.3, yB.get_value()),
                                            color=C_R, stroke_width=3))
        self.add(sweep2)
        self.play(yB.animate.set_value(mv), run_time=1.8, rate_func=smooth)
        dmin = Dot(ax.c2p(c_, mv), color=C_R, radius=0.1)
        lmin = M(r"\text{min } f(c)", 30, C_R).next_to(dmin, DOWN, buff=0.12)
        self.play(GrowFromCenter(dmin), FadeIn(lmin))
        sweep2.clear_updaters()
        self.play(FadeOut(sweep2), run_time=0.3)

        self.wait(0.3)
        # câu 17
        self.play(*[FadeOut(m) for m in [sbox, card, ax, curve, ends, la, lb, dmax, lmax, dmin, lmin]])
        # chứng minh bước 1: f bị chặn
        st = T("Proof · Step 1:  f is bounded", 28, C_N, weight=BOLD).next_to(hd, DOWN, buff=0.3)
        st.to_edge(LEFT, buff=0.5)
        self.play(FadeIn(st))
        nl = NumberLine(x_range=[0, 6, 1], length=6.4, include_ticks=False,
                        color=GREY_T, stroke_width=3).move_to(LEFT * 3.3 + DOWN * 2.3)
        nl_a = VGroup(M("[", 54, C_N).move_to(nl.n2p(0)), M("a", 32).next_to(nl.n2p(0), DOWN, buff=0.25))
        nl_b = VGroup(M("]", 54, C_N).move_to(nl.n2p(6)), M("b", 32).next_to(nl.n2p(6), DOWN, buff=0.25))
        # dãy x_n dồn về x*, cột f(x_n) cao dần -> vô lý
        # tôi có sài AI ở khúc này để vẽ mấy cái cột
        xstar = 3.7
        pts = [xstar + ((-1) ** k) * 2.6 / (k ** 1.1) for k in range(1, 9)]
        bars = VGroup()
        dots = VGroup()
        for k, p in enumerate(pts, start=1):
            h = 0.38 * k
            dots.add(Dot(nl.n2p(p), color=C_R, radius=0.07))
            bars.add(Rectangle(width=0.12, height=h, stroke_width=0, fill_color=C_R,
                               fill_opacity=0.75).next_to(nl.n2p(p), UP, buff=0.0))
        hint = M(r"f(x_n) > n", 34, C_R).move_to(nl.n2p(0.9) + UP * 2.6)
        lines = VGroup(
            TX(r"Suppose $f$ is not bounded above:\\ pick $x_n\in[a,b]$ with $f(x_n)>n$.", 30),
            TX(r"Bolzano--Weierstrass: a subsequence\\ $x_{n_k}\to x^*\in[a,b]$ \ (closed!)", 30),
            TX(r"Continuity: $f(x_{n_k})\to f(x^*)$, a finite number.", 30),
            TX(r"But $f(x_{n_k})>n_k\to\infty$. \ Contradiction!", 30),
            TX(r"$\Rightarrow$ $f$ is bounded (below: same argument).", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.65 + DOWN * 0.35)
        lines[3].set_color(C_R)
        lines[4].set_color(C_G)
        self.play(Create(nl), FadeIn(nl_a), FadeIn(nl_b), FadeIn(lines[0], shift=RIGHT * 0.2))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i]), GrowFromEdge(bars[i], DOWN))
                                for i in range(len(pts))], lag_ratio=0.35), FadeIn(hint),
                  run_time=3.0)

        self.wait(0.5)
        # câu 18
        xs_dot = Dot(nl.n2p(xstar), color=C_N, radius=0.1)
        xs_lab = M("x^*", 34, C_N).next_to(xs_dot, DOWN, buff=0.25)
        brace_arrows = VGroup(*[Arrow(nl.n2p(p) + DOWN * 0.95, nl.n2p(xstar) + DOWN * 0.95,
                                      buff=0.05, color=C_N, stroke_width=2,
                                      max_tip_length_to_length_ratio=0.15)
                                for p in pts[:3]])
        self.play(FadeIn(lines[1], shift=RIGHT * 0.2))
        self.play(GrowFromCenter(xs_dot), FadeIn(xs_lab),
                  LaggedStart(*[GrowArrow(b) for b in brace_arrows], lag_ratio=0.2), run_time=1.6)

        self.wait(5.3)
        # câu 19
        self.play(FadeIn(lines[2], shift=RIGHT * 0.2))
        self.play(FadeIn(lines[3], shift=RIGHT * 0.2), Indicate(bars, color=C_R))
        self.play(FadeIn(lines[4], shift=RIGHT * 0.2))

        self.wait(6.2)
        # câu 20
        self.play(*[FadeOut(m) for m in [nl, nl_a, nl_b, dots, bars, hint, xs_dot, xs_lab,
                                         brace_arrows, lines]])
        # chứng minh bước 2: f đạt được max
        st2 = T("Proof · Step 2:  f reaches its maximum", 28, C_N, weight=BOLD).move_to(st, aligned_edge=LEFT)
        self.play(ReplacementTransform(st, st2))
        ax = Axes(x_range=[0, 6.3, 1], y_range=[0, 4, 1], x_length=6.6, y_length=4.4,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 3.3 + DOWN * 0.75)
        curve = ax.plot(f_evt, x_range=[A, B], color=C_F, stroke_width=5)
        Mline = DashedLine(ax.c2p(0, Mv), ax.c2p(6.2, Mv), color=C_N, dash_length=0.1)
        Mlab = M(r"M=\sup f", 30, C_N).next_to(ax.c2p(0.3, Mv), UP, buff=0.12).shift(RIGHT * 0.6)
        lines2 = VGroup(
            TX(r"$f$ bounded $\Rightarrow$ $M=\sup_{[a,b]} f$ exists.", 30),
            TX(r"Pick $x_n$ with $f(x_n)\to M$.", 30),
            TX(r"A subsequence $x_{n_k}\to d\in[a,b]$.", 30),
            TX(r"Continuity: $f(d)=\lim f(x_{n_k}) = M$.", 30),
            TX(r"$\Rightarrow$ the maximum is attained. \ Same for $\inf f$. \ $\blacksquare$", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.5 + DOWN * 0.5)
        lines2[4].set_color(C_G)
        self.play(Create(ax), Create(curve), run_time=1.4)
        self.play(Create(Mline), FadeIn(Mlab), FadeIn(lines2[0], shift=RIGHT * 0.2))
        # mấy điểm tiến dần tới M
        offs = [1.4, -1.1, 0.75, -0.5, 0.3, -0.16, 0.08]
        seq = VGroup(*[Dot(ax.c2p(d_ + o, f_evt(d_ + o)), color=C_N, radius=0.07) for o in offs])
        self.play(FadeIn(lines2[1], shift=RIGHT * 0.2),
                  LaggedStart(*[FadeIn(s, scale=0.5) for s in seq], lag_ratio=0.3), run_time=2.2)

        self.wait(0.3)
        # câu 21
        dD = Dot(ax.c2p(d_, Mv), color=C_G, radius=0.11)
        dlab = M("d", 32, C_G).next_to(ax.c2p(d_, 0), DOWN, buff=0.12)
        dv = DashedLine(ax.c2p(d_, 0), ax.c2p(d_, Mv), color=C_G, dash_length=0.07)
        self.play(FadeIn(lines2[2], shift=RIGHT * 0.2), seq.animate.set_opacity(0.35))
        self.play(GrowFromCenter(dD), Create(dv), FadeIn(dlab), FadeIn(lines2[3], shift=RIGHT * 0.2))
        self.play(FadeIn(lines2[4], shift=RIGHT * 0.2), Flash(dD, color=C_G))
        self.wait(6.5)


# ------------------------------------------------------------
# CẢNH 3 - ĐỊNH LÝ IVT (giá trị trung gian)
# phát biểu, kéo N lên xuống, chứng minh 5 bước, hệ quả Bolzano
# ------------------------------------------------------------
class S3_IVT(Scene):
    def construct(self):
        hd = header("PART A · 3", "Theorem 2 - Intermediate Value Theorem (IVT)")
        # câu 22
        self.play(FadeIn(hd, shift=DOWN * 0.2))
        # ảnh Bolzano
        card = portrait("bolzano.png", "Bernard Bolzano", "1781 - 1848", "proved the IVT (1817)", h=2.8)
        card.move_to(RIGHT * 4.6 + DOWN * 1.5)

        self.wait(5.1)
        # câu 23
        # phát biểu định lý
        stmt = TX(r"If $f$ is continuous on $[a,b]$ and $N$ is any number strictly between "
                  r"$f(a)$ and $f(b)$,\\ then there is at least one $c\in(a,b)$ with $f(c)=N$.", 32)
        sbox = theorem_box("THEOREM 2  (IVT)", stmt).move_to(UP * 2.05)
        self.play(FadeIn(sbox, shift=UP * 0.2), FadeIn(card, shift=LEFT * 0.3), run_time=1.3)

        A, B = 0.5, 5.5
        ax = Axes(x_range=[0, 6.2, 1], y_range=[0, 4.3, 1], x_length=7.4, y_length=4.0,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 2.2 + DOWN * 1.6)
        curve = ax.plot(f_ivt, x_range=[A, B], color=C_F, stroke_width=5)
        la = M("a", 30).next_to(ax.c2p(A, 0), DOWN, buff=0.12)
        lb = M("b", 30).next_to(ax.c2p(B, 0), DOWN, buff=0.12)
        dA = Dot(ax.c2p(A, f_ivt(A)), color=C_F)
        dB = Dot(ax.c2p(B, f_ivt(B)), color=C_F)
        lfa = M("f(a)", 28).next_to(dA, LEFT, buff=0.12)
        lfb = M("f(b)", 28).next_to(dB, RIGHT, buff=0.12)

        self.wait(7.1)
        # câu 24
        self.play(Create(ax), FadeIn(la), FadeIn(lb), run_time=1)
        self.play(Create(curve), FadeIn(dA), FadeIn(dB), FadeIn(lfa), FadeIn(lfb), run_time=1.6)
        Nt = ValueTracker(NV)
        xs = np.linspace(A, B, 4000)

        # tìm chỗ đồ thị cắt đường y = N
        def crossings(N):
            v = f_ivt(xs) - N
            idx = np.where(np.diff(np.sign(v)) != 0)[0]
            return [xs[i] for i in idx]

        Nline = always_redraw(lambda: DashedLine(ax.c2p(0, Nt.get_value()), ax.c2p(6.1, Nt.get_value()),
                                                 color=C_N, dash_length=0.1, stroke_width=3))
        Nlab = always_redraw(lambda: M("N", 32, C_N).next_to(ax.c2p(0, Nt.get_value()), LEFT, buff=0.12))
        cdots = always_redraw(lambda: VGroup(*[Dot(ax.c2p(c, Nt.get_value()), color=C_N, radius=0.09)
                                               for c in crossings(Nt.get_value())]))
        self.play(Create(Nline), FadeIn(Nlab))
        self.play(FadeIn(cdots))

        self.wait(1.5)
        # câu 25
        # kéo N lên xuống, lúc nào cũng có chỗ cắt
        self.play(Nt.animate.set_value(f_ivt(A) + 0.15), run_time=2.2)
        self.play(Nt.animate.set_value(f_ivt(B) - 0.15), run_time=3.0)
        self.play(Nt.animate.set_value(NV), run_time=1.6)

        self.wait(0.3)
        # câu 26
        Nline.clear_updaters(); Nlab.clear_updaters(); cdots.clear_updaters()
        self.play(*[FadeOut(m) for m in [sbox, card, ax, curve, la, lb, dA, dB, lfa, lfb,
                                         Nline, Nlab, cdots]])
        # chứng minh bước 1: dời đồ thị xuống N đơn vị
        ax = Axes(x_range=[0, 6.2, 1], y_range=[-2.2, 4.3, 1], x_length=6.4, y_length=5.4,
                  tips=True, axis_config=AX_CFG).move_to(LEFT * 3.45 + DOWN * 0.6)
        curve = ax.plot(f_ivt, x_range=[A, B], color=C_F, stroke_width=5)
        Nline = DashedLine(ax.c2p(0, NV), ax.c2p(6.1, NV), color=C_N, dash_length=0.1, stroke_width=3)
        Nlab = M("N", 32, C_N).next_to(ax.c2p(0, NV), LEFT, buff=0.12)
        la = M("a", 30).next_to(ax.c2p(A, 0), UP, buff=0.12)
        lb = M("b", 30).next_to(ax.c2p(B, 0), DOWN, buff=0.12)
        flab = M("f", 32, C_F).next_to(ax.c2p(B, f_ivt(B)), UR, buff=0.05)
        col = VGroup(
            T("Step 1 · Shift", 26, C_N, weight=BOLD),
            M(r"g(x) = f(x) - N", 38),
            TX(r"$g$ is continuous on $[a,b]$,", 30),
            M(r"g(a) < 0 < g(b)", 36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.3 + UP * 1.4)
        self.play(Create(ax), Create(curve), FadeIn(la), FadeIn(lb), FadeIn(flab), run_time=1.4)
        self.play(Create(Nline), FadeIn(Nlab), FadeIn(col[0]), FadeIn(col[1]))
        # dời f thành g
        shift_v = ax.c2p(0, 0) - ax.c2p(0, NV)
        glab = M("g", 32, C_P).next_to(ax.c2p(B, g_ivt(B)), UR, buff=0.05)
        self.play(curve.animate.shift(shift_v).set_color(C_P), Nline.animate.shift(shift_v).set_opacity(0),
                  FadeOut(Nlab), Transform(flab, glab), run_time=2.0)
        self.remove(Nline)

        self.wait(2.9)
        # câu 27
        gA = Dot(ax.c2p(A, g_ivt(A)), color=C_R)
        gB = Dot(ax.c2p(B, g_ivt(B)), color=C_G)
        self.play(FadeIn(col[2]), FadeIn(col[3]), FadeIn(gA), FadeIn(gB))
        goal = TX(r"Goal: find $c$ with $g(c)=0$.", 30, C_N).next_to(col, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(goal))

        self.wait(4.1)
        # câu 28
        # bước 2: tập S = {g < 0}, c = sup S
        xs = np.linspace(A, B, 6000)
        v = g_ivt(xs)
        roots = [xs[i] for i in np.where(np.diff(np.sign(v)) != 0)[0]]
        c_ = roots[-1]
        segS = VGroup(Line(ax.c2p(A, 0), ax.c2p(roots[0], 0)),
                      Line(ax.c2p(roots[1], 0), ax.c2p(roots[2], 0))).set_stroke(C_R, 9)
        col2 = VGroup(
            T("Step 2 · The set S", 26, C_N, weight=BOLD),
            M(r"S=\{x\in[a,b] : g(x)<0\}", 36),
            TX(r"$a\in S$, so $S\neq\varnothing$; \ $S$ bounded above by $b$.", 30),
            TX(r"Completeness axiom: $c=\sup S$ exists,\ \ $a\le c\le b$.", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.4)
        self.play(FadeOut(col), FadeOut(goal))
        self.play(FadeIn(col2[0]), FadeIn(col2[1]), Create(segS), run_time=1.6)
        Slab = M("S", 32, C_R).next_to(ax.c2p((roots[1] + roots[2]) / 2, 0), DOWN, buff=0.18)
        Slab2 = M("S", 32, C_R).next_to(ax.c2p((A + roots[0]) / 2, 0), UP, buff=0.18)
        self.play(FadeIn(Slab), FadeIn(Slab2), FadeIn(col2[2]))

        self.wait(3.5)
        # câu 29
        cmark = Line(ax.c2p(c_, -0.25), ax.c2p(c_, 0.25), color=C_N, stroke_width=5)
        clab = M(r"c=\sup S", 30, C_N).next_to(ax.c2p(c_, 0), UP, buff=0.5).shift(LEFT * 0.3)
        self.play(FadeIn(col2[3]), Create(cmark), FadeIn(clab))

        self.wait(5.0)
        # câu 30
        self.play(FadeOut(col2))
        # bước 3, 4: giả sử g(c) < 0 rồi g(c) > 0, cả 2 đều vô lý
        # tôi có sài AI ở khúc này để làm hiệu ứng gạch chéo
        col3 = VGroup(
            T("Step 3 · Suppose g(c) < 0", 26, C_R, weight=BOLD),
            TX(r"Continuity: $g<0$ on $(c-\varepsilon,\,c+\varepsilon)$.", 30),
            TX(r"Then some $x>c$ lies in $S$ \ --- but $c$\\ is an upper bound of $S$. \ Contradiction!", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.75)
        col4 = VGroup(
            T("Step 4 · Suppose g(c) > 0", 26, C_G, weight=BOLD),
            TX(r"Continuity: $g>0$ on $(c-\varepsilon,\,c+\varepsilon)$.", 30),
            TX(r"No point of $S$ there, so $c-\varepsilon$ is a\\ smaller upper bound. \ Contradiction!", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(col3, DOWN, aligned_edge=LEFT, buff=0.45)
        e = 0.35
        win = Rectangle(width=ax.c2p(c_ + e, 0)[0] - ax.c2p(c_ - e, 0)[0], height=1.3,
                        stroke_width=0, fill_color=C_R, fill_opacity=0.2).move_to(ax.c2p(c_, -0.3))
        hyp = Dot(ax.c2p(c_, -0.55), color=C_R, radius=0.09)
        hyp_seg = Line(ax.c2p(c_ - e, 0), ax.c2p(c_ + e, 0)).set_stroke(C_R, 9)
        q1 = M("?", 36, C_R).next_to(hyp, DOWN, buff=0.1)
        self.play(FadeIn(col3[0]), FadeIn(win), FadeIn(hyp), FadeIn(q1))
        self.play(FadeIn(col3[1]), Create(hyp_seg))
        cross1 = Cross(VGroup(win, q1), stroke_color=C_R, stroke_width=5)
        self.play(FadeIn(col3[2]), Create(cross1))

        self.wait(6.3)
        # câu 31
        self.play(FadeOut(VGroup(win, hyp, hyp_seg, q1, cross1)))
        win2 = win.copy().set_fill(C_G, 0.2).move_to(ax.c2p(c_, 0.3))
        hyp2 = Dot(ax.c2p(c_, 0.55), color=C_G, radius=0.09)
        q2 = M("?", 36, C_G).next_to(hyp2, UP, buff=0.1)
        newub = Line(ax.c2p(c_ - e, -0.25), ax.c2p(c_ - e, 0.25), color=C_G, stroke_width=5)
        self.play(FadeIn(col4[0]), FadeIn(win2), FadeIn(hyp2), FadeIn(q2), clab.animate.set_opacity(0.3))
        self.play(FadeIn(col4[1]), Create(newub))
        cross2 = Cross(VGroup(win2, q2), stroke_color=C_R, stroke_width=5)
        self.play(FadeIn(col4[2]), Create(cross2))

        self.wait(6.2)
        # câu 32
        self.play(FadeOut(VGroup(win2, hyp2, q2, newub, cross2, col3, col4)), clab.animate.set_opacity(1))
        # bước 5: kết luận g(c) = 0
        concl = VGroup(
            T("Step 5 · Conclusion", 26, C_N, weight=BOLD),
            M(r"g(c)=0 \ \Longrightarrow\ f(c)=N", 40),
            TX(r"$g(a)<0<g(b)$ $\Rightarrow$ $c\ne a,\ c\ne b$, \ so $c\in(a,b)$. \ $\blacksquare$", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.2 + UP * 1.4)
        root_dot = Dot(ax.c2p(c_, 0), color=C_N, radius=0.12)
        self.play(FadeIn(concl[0]), GrowFromCenter(root_dot))
        self.play(Write(concl[1]), Flash(root_dot, color=C_N))
        self.play(FadeIn(concl[2], shift=RIGHT * 0.2))

        self.wait(2.8)
        # câu 33
        # hệ quả: định lý Bolzano (trường hợp N = 0)
        bol = VGroup(TX(r"If $f$ is continuous on $[a,b]$ and $f(a)\,f(b)<0$,\\ then "
                        r"$f(c)=0$ for some $c\in(a,b)$.", 30))
        bbox = theorem_box("COROLLARY  (Bolzano's theorem)", bol, C_F)
        bbox.next_to(concl, DOWN, aligned_edge=LEFT, buff=0.55)
        self.play(FadeIn(bbox, shift=UP * 0.2))
        self.wait(4.7)


# ------------------------------------------------------------
# CẢNH 4 - VÍ DỤ HỌC THUẬT
# (a) IVT + chia đôi, (b) EVT tìm max min
# ------------------------------------------------------------
class S4_Example(Scene):
    def construct(self):
        hd = header("PART A · 4", "Academic Example")
        self.play(FadeIn(hd, shift=DOWN * 0.2))
        prob = M(r"f(x) = x^3 - 3x + 1, \qquad x\in[0,2]", 42).next_to(hd, DOWN, buff=0.35)
        ax = Axes(x_range=[-0.4, 2.4, 0.5], y_range=[-1.6, 3.6, 1], x_length=6.4, y_length=4.9,
                  tips=True, axis_config={**AX_CFG, "include_ticks": True, "tick_size": 0.06},
                  x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2], "font_size": 24},
                  y_axis_config={"numbers_to_include": [-1, 1, 2, 3], "font_size": 24},
                  ).move_to(LEFT * 3.5 + DOWN * 0.95)
        zero = MathTex("0", font_size=24, color=WHITE).next_to(ax.c2p(0, 0), DL, buff=0.08)
        curve = ax.plot(f_ex, x_range=[-0.3, 2.13], color=C_F, stroke_width=5)
        seg = ax.plot(f_ex, x_range=[0, 2], color=C_F, stroke_width=8)

        # câu 34
        self.play(Write(prob))
        self.play(Create(ax), FadeIn(zero), run_time=1.2)
        self.play(Create(curve), run_time=1.5)
        self.play(curve.animate.set_stroke(opacity=0.35), Create(seg))

        self.wait(2.3)
        # câu 35
        # câu (a): dùng IVT chứng minh có nghiệm trong (0, 1)
        pa = VGroup(
            T("(a)  IVT: a root in (0, 1)?", 26, C_N, weight=BOLD),
            TX(r"$f$ is a polynomial $\Rightarrow$ continuous on $[0,1]$.", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.55)
        self.play(FadeIn(pa[0]), FadeIn(pa[1], shift=RIGHT * 0.2))

        self.wait(4.6)
        # câu 36
        vals = VGroup(M(r"f(0) = 1 > 0", 36, C_G), M(r"f(1) = -1 < 0", 36, C_R)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        vals.next_to(pa, DOWN, aligned_edge=LEFT, buff=0.3)
        d0 = Dot(ax.c2p(0, 1), color=C_G, radius=0.1)
        d1 = Dot(ax.c2p(1, -1), color=C_R, radius=0.1)
        self.play(FadeIn(vals[0]), GrowFromCenter(d0))
        self.play(FadeIn(vals[1]), GrowFromCenter(d1))

        self.wait(2.7)
        # câu 37
        concl = TX(r"$f(1)<0<f(0)$ $\Rightarrow$ by the IVT,\\ $\exists\,c\in(0,1)$ with $f(c)=0$.", 30, C_N)
        concl.next_to(vals, DOWN, aligned_edge=LEFT, buff=0.3)
        c0 = chia_doi(f_ex, 0, 1)
        rdot = Dot(ax.c2p(c0, 0), color=C_N, radius=0.11)
        self.play(FadeIn(concl, shift=RIGHT * 0.2))
        self.play(GrowFromCenter(rdot), Flash(rdot, color=C_N))

        self.wait(3.1)
        # câu 38
        self.play(FadeOut(VGroup(pa, vals, concl)))
        # chia đôi 6 bước, có bảng số
        # tôi có sài AI ở khúc này để làm bảng chia đôi
        btitle = T("Bisection method", 26, C_N, weight=BOLD)
        hdr = VGroup(M("n", 30, GREY_T), M("[a_n,\\ b_n]", 30, GREY_T), M("m_n", 30, GREY_T),
                     M("f(m_n)", 30, GREY_T))
        lo, hi = 0.0, 1.0
        rows = []
        brackets = []
        for n in range(1, 7):
            m = (lo + hi) / 2
            fm = f_ex(m)
            rows.append((n, lo, hi, m, fm))
            brackets.append((lo, hi))
            if f_ex(lo) * fm < 0:
                hi = m
            else:
                lo = m
        cw = [0.6, 2.3, 1.2, 1.5]

        def row_mobs(cells, colr=WHITE):
            g = VGroup()
            x = 0
            for w, c in zip(cw, cells):
                c.set_color(colr) if colr != WHITE else None
                c.move_to(RIGHT * (x + w / 2))
                g.add(c)
                x += w
            return g

        table = VGroup(row_mobs(list(hdr)))
        for (n, l, h, m, fm) in rows:
            table.add(row_mobs([M(str(n), 30), M(f"[{l:.4f},\\ {h:.4f}]", 28), M(f"{m:.4f}", 28),
                                M(f"{fm:+.4f}", 28, C_G if fm > 0 else C_R)]))
        table.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rule = Line(LEFT, RIGHT).set_width(sum(cw)).set_stroke(GREY_T, 1.5).next_to(table[0], DOWN, buff=0.1).align_to(table[0], LEFT)
        tblock = VGroup(btitle, VGroup(table, rule)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        tblock.move_to(RIGHT * 3.4 + DOWN * 0.35)
        self.play(FadeIn(btitle), FadeIn(table[0]), Create(rule))

        def bracket_mob(l, h):
            return VGroup(
                Line(ax.c2p(l, 0), ax.c2p(h, 0)).set_stroke(C_N, 8, 0.8),
                Line(ax.c2p(l, -0.18), ax.c2p(l, 0.18), color=C_N, stroke_width=4),
                Line(ax.c2p(h, -0.18), ax.c2p(h, 0.18), color=C_N, stroke_width=4),
            )
        br = bracket_mob(*brackets[0])
        self.play(Create(br))
        mdot = None
        self.wait(2.4)
        # câu 39
        for i, (n, l, h, m, fm) in enumerate(rows):
            md = Dot(ax.c2p(m, f_ex(m)), color=C_G if fm > 0 else C_R, radius=0.07)
            anims = [FadeIn(table[i + 1], shift=UP * 0.1), FadeIn(md)]
            if i > 0:
                anims.append(Transform(br, bracket_mob(*brackets[i])))
            self.play(*anims, run_time=0.9)
            if mdot is not None:
                self.remove(mdot)
            mdot = md
        final = M(r"c \approx 0.347", 40, C_N).next_to(tblock, DOWN, buff=0.35).align_to(tblock, LEFT)
        self.play(Write(final), Indicate(rdot, color=C_N))

        self.wait(0.3)
        # câu 40
        self.play(FadeOut(VGroup(tblock, final, br, mdot)), FadeOut(rdot), FadeOut(d0), FadeOut(d1))
        # câu (b): dùng EVT tìm max, min
        pb = VGroup(
            T("(b)  EVT: absolute max & min on [0, 2]", 26, C_N, weight=BOLD),
            TX(r"Continuous on closed $[0,2]$ $\Rightarrow$ max \& min exist.", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.55)
        self.play(FadeIn(pb[0]), FadeIn(pb[1], shift=RIGHT * 0.2))

        self.wait(4.3)
        # câu 41
        der = VGroup(M(r"f'(x) = 3x^2 - 3 = 0", 36), M(r"\Rightarrow\ x=1 \ \ \text{or}\ \ x=-1", 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        der.next_to(pb, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(der[0]))
        self.play(Write(der[1]))
        strike = Line(der[1][0][-4:].get_left(), der[1][0][-4:].get_right(), color=C_R, stroke_width=4)
        note = T("not in [0, 2]", 20, C_R).next_to(der[1], RIGHT, buff=0.2)
        self.play(Create(strike), FadeIn(note))

        self.wait(5.1)
        # câu 42
        # bảng giá trị
        cells = [("x", "f(x)")] + [("0", "1"), ("1", "-1"), ("2", "3")]
        tb = VGroup()
        for i, (xv, yv) in enumerate(cells):
            cl = GREY_T if i == 0 else WHITE
            r = VGroup(M(xv, 32, cl), M(yv, 32, cl))
            r[0].move_to(LEFT * 0.7); r[1].move_to(RIGHT * 0.7)
            tb.add(r)
        tb.arrange(RIGHT, buff=0.6)
        tb_grid = VGroup(*[VGroup(r[0], r[1]).arrange(DOWN, buff=0.25) for r in tb]).arrange(RIGHT, buff=0.7)
        tb_box = SurroundingRectangle(tb_grid, buff=0.2, stroke_color=GREY_T, stroke_width=1.5)
        tbl = VGroup(tb_box, tb_grid).next_to(der, DOWN, aligned_edge=LEFT, buff=0.35)
        p0 = Dot(ax.c2p(0, 1), color=WHITE, radius=0.09)
        p1 = Dot(ax.c2p(1, -1), color=C_R, radius=0.11)
        p2 = Dot(ax.c2p(2, 3), color=C_G, radius=0.11)
        self.play(FadeIn(tbl), LaggedStart(FadeIn(p0), FadeIn(p1), FadeIn(p2), lag_ratio=0.4), run_time=1.6)

        self.wait(4.0)
        # câu 43
        tb_grid[2][1].set_color(C_R); tb_grid[3][1].set_color(C_G)
        res = VGroup(M(r"\min f = -1 \ \ (x=1)", 34, C_R), M(r"\max f = 3 \ \ (x=2)", 34, C_G)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        res.next_to(tbl, DOWN, aligned_edge=LEFT, buff=0.3)
        lmin = M(r"\min", 28, C_R).next_to(p1, DOWN, buff=0.12)
        lmax = M(r"\max", 28, C_G).next_to(p2, LEFT, buff=0.15)
        self.play(FadeIn(res[0]), FadeIn(lmin), Flash(p1, color=C_R))
        self.play(FadeIn(res[1]), FadeIn(lmax), Flash(p2, color=C_G))
        self.wait(5.6)


# ------------------------------------------------------------
# CẢNH 5 - PHẢN VÍ DỤ
# bỏ tính liên tục thì IVT sai, bỏ đoạn đóng thì EVT sai
# ------------------------------------------------------------
class S5_Counterexamples(Scene):
    def construct(self):
        hd = header("PART A · 5", "Counterexamples - why the hypotheses matter")
        # câu 44
        self.play(FadeIn(hd, shift=DOWN * 0.2))
        divider = DashedLine(UP * 2.6, DOWN * 3.7, color=GREY_T, dash_length=0.1, stroke_width=1.5)
        self.play(Create(divider))

        # bên trái: hàm bị nhảy -> IVT không còn đúng
        tl = T("No continuity  →  IVT fails", 26, C_R, weight=BOLD).move_to(LEFT * 3.55 + UP * 2.25)
        defl = M(r"f(x)=\begin{cases}-1, & x<0\\ \ \ 1, & x\ge 0\end{cases}\qquad x\in[-1,1]", 32)
        defl.next_to(tl, DOWN, buff=0.3)
        axL = Axes(x_range=[-1.3, 1.3, 1], y_range=[-1.6, 1.6, 1], x_length=5.4, y_length=3.4,
                   tips=True, axis_config={**AX_CFG, "include_ticks": True},
                   x_axis_config={"numbers_to_include": [-1, 1], "font_size": 22},
                   y_axis_config={"numbers_to_include": [-1, 1], "font_size": 22}).move_to(LEFT * 3.55 + DOWN * 1.6)
        p1 = Line(axL.c2p(-1, -1), axL.c2p(0, -1), color=C_F, stroke_width=6)
        p2 = Line(axL.c2p(0, 1), axL.c2p(1, 1), color=C_F, stroke_width=6)
        o1 = Circle(radius=0.08, color=C_F, stroke_width=3).set_fill(BG, 1).move_to(axL.c2p(0, -1))
        c1 = Dot(axL.c2p(0, 1), color=C_F, radius=0.08)
        e1 = Dot(axL.c2p(-1, -1), color=C_F, radius=0.08)
        e2 = Dot(axL.c2p(1, 1), color=C_F, radius=0.08)
        Nl = DashedLine(axL.c2p(-1.25, 0), axL.c2p(1.25, 0), color=C_N, stroke_width=4, dash_length=0.1)
        Nlab = M("N=0", 28, C_N).next_to(axL.c2p(-1.25, 0), UP, buff=0.12).shift(RIGHT * 0.35)

        self.wait(2.5)
        # câu 45
        self.play(FadeIn(tl), Write(defl))
        self.play(Create(axL), run_time=1)
        self.play(Create(p1), FadeIn(e1), FadeIn(o1))
        self.play(Create(p2), FadeIn(c1), FadeIn(e2))

        self.wait(1.0)
        # câu 46
        self.play(Create(Nl), FadeIn(Nlab))
        jump = DoubleArrow(axL.c2p(0.12, -0.92), axL.c2p(0.12, 0.92), color=C_R, buff=0, stroke_width=4,
                           tip_length=0.18)
        jl = T("jump", 22, C_R).next_to(jump, RIGHT, buff=0.1).shift(UP * 0.45)
        self.play(GrowFromCenter(jump), FadeIn(jl))
        noc = M(r"f(x)\neq 0 \ \ \text{for all } x", 30, C_R).next_to(axL, DOWN, buff=0.2)
        self.play(FadeIn(noc))

        # bên phải: 1/x trên (0,1] -> EVT không còn đúng
        tr = T("Not closed  →  EVT fails", 26, C_R, weight=BOLD).move_to(RIGHT * 3.55 + UP * 2.25)
        defr = M(r"f(x)=\frac{1}{x}, \qquad x\in(0,1]", 34).next_to(tr, DOWN, buff=0.3)
        defr.align_to(defl, UP)
        axR = Axes(x_range=[0, 1.2, 0.5], y_range=[0, 9, 2], x_length=5.0, y_length=3.4,
                   tips=True, axis_config={**AX_CFG, "include_ticks": True},
                   x_axis_config={"numbers_to_include": [0.5, 1], "font_size": 22},
                   y_axis_config={"numbers_to_include": [2, 4, 6, 8], "font_size": 22}).move_to(RIGHT * 3.55 + DOWN * 1.6)
        self.wait(3.4)
        # câu 47
        self.play(FadeIn(tr), Write(defr))
        self.play(Create(axR), run_time=1)
        hyp = axR.plot(lambda x: 1 / x, x_range=[1 / 8.6, 1], color=C_F, stroke_width=5)
        e_r = Dot(axR.c2p(1, 1), color=C_F, radius=0.08)
        open0 = M("(", 50, C_N).move_to(axR.c2p(0, 0)).shift(RIGHT * 0.05)
        self.play(Create(hyp), FadeIn(e_r), FadeIn(open0), run_time=1.5)

        self.wait(2.9)
        # câu 48
        xt = ValueTracker(0.7)
        tracer = always_redraw(lambda: Dot(axR.c2p(xt.get_value(), min(1 / xt.get_value(), 9)),
                                           color=C_N, radius=0.09))
        val = always_redraw(lambda: M(f"f(x) = {1 / xt.get_value():.1f}", 28, C_N)
                            .next_to(axR.c2p(0.62, 7.6), RIGHT, buff=0))
        self.add(tracer, val)
        self.play(xt.animate.set_value(0.118), run_time=3.0, rate_func=rate_functions.ease_in_quad)
        up = Arrow(axR.c2p(0.12, 7.0), axR.c2p(0.12, 9.6), color=C_R, buff=0, stroke_width=5)
        inf = M(r"\to\infty", 30, C_R).next_to(up, RIGHT, buff=0.1)
        self.play(GrowArrow(up), FadeIn(inf))
        nomax = T("no maximum value", 24, C_R).next_to(axR, DOWN, buff=0.2)
        self.play(FadeIn(nomax))

        self.wait(0.8)
        # câu 49
        tracer.clear_updaters(); val.clear_updaters()
        # tôi có edit phần này (dời khung lên trên cho khỏi đè đồ thị)
        msg = boxed(T("continuity  +  closed interval  are both needed", 26, C_N, weight=BOLD), C_N)
        msg[0].set_fill(PANEL, 1)
        msg.move_to(UP * 1.55)
        self.play(FadeOut(defl), FadeOut(defr), FadeIn(msg, shift=UP * 0.2))
        self.wait(3.1)


# ------------------------------------------------------------
# CẢNH 6 - ỨNG DỤNG: BỂ NƯỚC HỞ
# cắt 4 góc tấm thép, gấp thành hộp, tìm x cho thể tích lớn nhất
# ------------------------------------------------------------
class S6_WaterTank(Scene):
    def construct(self):
        hd = header("PART B", "Application - Designing an Open-Top Water Tank")
        # câu 50
        self.play(FadeIn(hd, shift=DOWN * 0.2))

        xT = ValueTracker(4.0)
        k = 3.6 / SHEET
        sheet_c = LEFT * 3.6 + DOWN * 0.7

        # vẽ tấm thép đã cắt 4 góc
        def sheet_mob():
            x = xT.get_value() * k
            s = SHEET * k
            o = sheet_c + LEFT * s / 2 + DOWN * s / 2
            pts = [o + RIGHT * x, o + RIGHT * (s - x), o + RIGHT * (s - x) + UP * x,
                   o + RIGHT * s + UP * x, o + RIGHT * s + UP * (s - x), o + RIGHT * (s - x) + UP * (s - x),
                   o + RIGHT * (s - x) + UP * s, o + RIGHT * x + UP * s, o + RIGHT * x + UP * (s - x),
                   o + UP * (s - x), o + UP * x, o + RIGHT * x + UP * x]
            cross = Polygon(*pts, stroke_color=WHITE, stroke_width=2, fill_color=C_F, fill_opacity=0.35)
            cuts = VGroup(*[Square(side_length=x, stroke_color=C_R, stroke_width=2, fill_color=C_R,
                                   fill_opacity=0.25).move_to(o + RIGHT * cx + UP * cy)
                            for cx in (x / 2, s - x / 2) for cy in (x / 2, s - x / 2)])
            folds = VGroup(
                DashedLine(o + RIGHT * x + UP * x, o + RIGHT * (s - x) + UP * x),
                DashedLine(o + RIGHT * x + UP * (s - x), o + RIGHT * (s - x) + UP * (s - x)),
                DashedLine(o + RIGHT * x + UP * x, o + RIGHT * x + UP * (s - x)),
                DashedLine(o + RIGHT * (s - x) + UP * x, o + RIGHT * (s - x) + UP * (s - x)),
            ).set_stroke(WHITE, 1.5, 0.6)
            return VGroup(cuts, cross, folds)

        sheet = always_redraw(sheet_mob)
        s_full = SHEET * k
        top_brace = BraceBetweenPoints(sheet_c + LEFT * s_full / 2 + UP * s_full / 2,
                                       sheet_c + RIGHT * s_full / 2 + UP * s_full / 2, UP)
        top_lab = T("30 cm", 24).next_to(top_brace, UP, buff=0.1)
        xlab = always_redraw(lambda: M("x", 30, C_R).next_to(
            sheet_c + LEFT * s_full / 2 + UP * (s_full / 2 - xT.get_value() * k / 2), LEFT, buff=0.15))

        self.wait(4.9)
        # câu 51
        self.play(FadeIn(sheet), GrowFromCenter(top_brace), FadeIn(top_lab))
        self.play(FadeIn(xlab))
        self.play(xT.animate.set_value(6.5), run_time=1.6)
        self.play(xT.animate.set_value(5.0), run_time=1.2)

        # vẽ cái hộp sau khi gấp (giả 3D)
        # tôi có sài AI ở khúc này để tính tọa độ mấy mặt của hộp
        kb = 0.13
        box_c = LEFT * 3.6 + DOWN * 1.2

        def box_mob():
            x = xT.get_value()
            s = (SHEET - 2 * x) * kb
            h = x * kb
            D = np.array([0.42, 0.3, 0]) * s * 0.9
            o = box_c + LEFT * (s + D[0]) / 2 + DOWN * (h + D[1]) / 2
            R, U = RIGHT * s, UP * h
            P = lambda *v: o + sum(v, np.zeros(3))
            face = lambda *pts, op=0.25: Polygon(*pts, stroke_color=WHITE, stroke_width=2,
                                                 fill_color=C_F, fill_opacity=op)
            back = face(P(D), P(D, R), P(D, R, U), P(D, U), op=0.18)
            left = face(P(), P(D), P(D, U), P(U), op=0.22)
            base = face(P(), P(R), P(R, D), P(D), op=0.3)
            right = face(P(R), P(R, D), P(R, D, U), P(R, U), op=0.3)
            front = face(P(), P(R), P(R, U), P(U), op=0.35)
            water = Polygon(P(), P(R), P(R, D), P(D), stroke_width=0, fill_color=C_F, fill_opacity=0)
            return VGroup(back, left, base, right, front, water)

        box = always_redraw(box_mob)

        def box_labels():
            x = xT.get_value()
            s = (SHEET - 2 * x) * kb
            h = x * kb
            D = np.array([0.42, 0.3, 0]) * s * 0.9
            o = box_c + LEFT * (s + D[0]) / 2 + DOWN * (h + D[1]) / 2
            bl = M(r"30-2x", 28, C_N).next_to(o + RIGHT * s / 2, DOWN, buff=0.15)
            hl = M("x", 30, C_R).next_to(o + RIGHT * s + UP * h / 2, RIGHT, buff=0.1)
            return VGroup(bl, hl)

        blabs = always_redraw(box_labels)

        self.wait(1.0)
        # câu 52
        self.play(FadeOut(top_brace), FadeOut(top_lab), FadeOut(xlab))
        sheet.clear_updaters()
        target = box_mob()
        self.play(ReplacementTransform(sheet, target), run_time=1.8)
        self.remove(target)
        self.add(box)
        self.play(FadeIn(blabs))

        formula = M(r"V(x) = x\,(30-2x)^2 \ \ \text{cm}^3,\qquad 0\le x\le 15", 40)
        formula.next_to(hd, DOWN, buff=0.35)
        self.wait(1.6)
        # câu 53
        self.play(Write(formula), run_time=1.6)

        # đồ thị V(x)
        ax = Axes(x_range=[0, 15.8, 5], y_range=[0, 2400, 500], x_length=6.2, y_length=4.3,
                  tips=True, axis_config={**AX_CFG, "include_ticks": True},
                  x_axis_config={"numbers_to_include": [5, 10, 15], "font_size": 24},
                  y_axis_config={"numbers_to_include": [500, 1000, 1500, 2000], "font_size": 22},
                  ).move_to(RIGHT * 3.5 + DOWN * 1.05)
        axl = VGroup(M("x\\ (\\text{cm})", 26, GREY_T).next_to(ax.x_axis.get_end(), UP, buff=0.15).shift(LEFT * 0.3),
                     M("V\\ (\\text{cm}^3)", 26, GREY_T).next_to(ax.y_axis.get_end(), RIGHT, buff=0.15))
        vcurve = ax.plot(V, x_range=[0, 15], color=C_F, stroke_width=5)
        self.play(Create(ax), FadeIn(axl), run_time=1.2)
        self.play(Create(vcurve), run_time=1.6)

        tracker = always_redraw(lambda: Dot(ax.c2p(xT.get_value(), V(xT.get_value())), color=C_N, radius=0.1))
        drop = always_redraw(lambda: DashedLine(ax.c2p(xT.get_value(), 0), ax.c2p(xT.get_value(), V(xT.get_value())),
                                                color=C_N, dash_length=0.07, stroke_width=2))
        readout = always_redraw(lambda: VGroup(
            M(f"x = {xT.get_value():.2f}\\ \\text{{cm}}", 38),
            M(f"V = {V(xT.get_value()):.0f}\\ \\text{{cm}}^3", 38, C_N),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 5.0 + UP * 1.55))

        self.wait(3.4)
        # câu 54
        self.play(FadeIn(tracker), FadeIn(drop), FadeIn(readout))
        # kéo x qua lại xem thể tích đổi ra sao
        self.play(xT.animate.set_value(0.8), run_time=2.0)
        self.play(xT.animate.set_value(12.5), run_time=3.5)
        self.play(xT.animate.set_value(5.0), run_time=2.2)

        self.wait(0.3)
        # câu 55
        # dùng EVT: chắc chắn có max
        for m in (box, blabs, readout):
            m.clear_updaters()
        self.play(FadeOut(box), FadeOut(blabs), FadeOut(readout))
        lines = VGroup(
            TX(r"$V$ is a polynomial $\Rightarrow$ continuous on $[0,15]$.", 30),
            TX(r"EVT $\Rightarrow$ an absolute maximum \textbf{exists}.", 30, C_G),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 3.5 + UP * 1.35)
        self.play(FadeIn(lines[0], shift=RIGHT * 0.2))
        self.play(FadeIn(lines[1], shift=RIGHT * 0.2))

        self.wait(4.0)
        # câu 56
        # đạo hàm = 0
        der = VGroup(M(r"V'(x) = (30-2x)(30-6x)", 36), M(r"V'(x)=0 \ \Rightarrow\ x=5 \ \text{or}\ x=15", 36))
        der.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(lines, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(der[0]))
        self.play(Write(der[1]))

        self.wait(3.6)
        # câu 57
        # so sánh giá trị ở 2 đầu mút và điểm tới hạn
        tvals = VGroup(M(r"V(0) = 0", 34), M(r"V(15) = 0", 34), M(r"V(5) = 2000", 34, C_G)).arrange(RIGHT, buff=0.55)
        tvals.next_to(der, DOWN, aligned_edge=LEFT, buff=0.35)
        pts = VGroup(Dot(ax.c2p(0, 0), color=WHITE), Dot(ax.c2p(15, 0), color=WHITE),
                     Dot(ax.c2p(5, 2000), color=C_G, radius=0.12))
        tracker.clear_updaters(); drop.clear_updaters()
        self.play(FadeOut(tracker), LaggedStart(*[FadeIn(t) for t in tvals], lag_ratio=0.5),
                  LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.5), run_time=2)
        mxl = M(r"\max", 30, C_G).next_to(pts[2], UP, buff=0.12)
        self.play(FadeIn(mxl), Flash(pts[2], color=C_G))

        self.wait(5.0)
        # câu 58
        self.play(FadeOut(VGroup(lines, der)), tvals.animate.move_to(LEFT * 3.5 + UP * 1.6))
        xT.set_value(5.0)
        box_c = LEFT * 3.6 + DOWN * 1.3
        # hộp tốt nhất khi x = 5
        best = box_mob()
        best_l = box_labels()
        best_l[0].become(M(r"20\ \text{cm}", 28, C_N).move_to(best_l[0]))
        best_l[1].become(M(r"5\ \text{cm}", 28, C_R).next_to(best, RIGHT, buff=0.1).shift(DOWN * 0.5))
        res = boxed(M(r"V_{\max} = 2000\ \text{cm}^3 = 2\ \text{L}", 36, C_G), C_G)
        res.next_to(tvals, DOWN, buff=0.4).align_to(tvals, LEFT)
        self.play(FadeIn(best, shift=UP * 0.2), FadeIn(best_l))
        self.play(FadeIn(res, shift=UP * 0.2))

        self.wait(4.4)
        # câu 59
        self.play(FadeOut(VGroup(best, best_l, res)))
        # thêm: dùng IVT tìm x để bể chứa đúng 1 lít
        line1000 = DashedLine(ax.c2p(0, 1000), ax.c2p(15.5, 1000), color=C_P, dash_length=0.1, stroke_width=3)
        l1000 = M("1000", 26, C_P).next_to(ax.c2p(15.5, 1000), UP, buff=0.08)
        ivt_txt = VGroup(
            TX(r"Need $V(x)=1000$ cm$^3$ (1 liter):", 30, C_P),
            M(r"V(0)=0 \ <\ 1000\ <\ 2000=V(5)", 34),
            TX(r"IVT $\Rightarrow$ $\exists\,x\in(0,5)$ with $V(x)=1000$.", 30),
            M(r"\text{bisection: } x \approx 1.34\ \text{cm}", 34, C_N),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tvals, DOWN, aligned_edge=LEFT, buff=0.45)
        x1 = 1.3397459621556136
        hit = Dot(ax.c2p(x1, 1000), color=C_P, radius=0.11)
        self.play(Create(line1000), FadeIn(ivt_txt[0]))
        self.play(FadeIn(ivt_txt[1]))
        self.play(FadeIn(ivt_txt[2]), GrowFromCenter(hit))
        self.play(FadeIn(ivt_txt[3]), Flash(hit, color=C_P))

        self.wait(8.6)
        # câu 60
        self.play(FadeOut(VGroup(tvals, ivt_txt)))
        # giới hạn của mô hình
        lim = VGroup(
            T("Model limitations", 26, C_R, weight=BOLD),
            T("•  sheet thickness is ignored", 24),
            T("•  material lost at folds and welds", 24),
            T("•  structural strength not modelled", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 3.6 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lim], lag_ratio=0.4), run_time=2.2)
        self.wait(4.5)


# ------------------------------------------------------------
# CẢNH 7 - TỔNG KẾT
# ------------------------------------------------------------
class S7_Summary(Scene):
    def construct(self):
        hd = header("SUMMARY", "What we learned")
        self.play(FadeIn(hd, shift=DOWN * 0.2))

        # 3 thẻ tóm tắt
        def card(title, body_tex, color):
            t = T(title, 28, color, weight=BOLD)
            b = TX(body_tex, 32)
            g = VGroup(t, b).arrange(DOWN, buff=0.3)
            r = Rectangle(width=4.0, height=3.0, stroke_color=color,
                                 stroke_width=2, fill_color=color, fill_opacity=0.07)
            g.move_to(r)
            return VGroup(r, g)

        c1 = card("Continuity", r"$\displaystyle\lim_{x\to a}f(x)=f(a)$\\ no holes, no jumps", C_F)
        c2 = card("EVT", r"continuous on $[a,b]$\\ $\Rightarrow$ absolute max\\ and min exist", C_G)
        c3 = card("IVT", r"continuous on $[a,b]$\\ $\Rightarrow$ every value\\ between is hit", C_N)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.4).move_to(UP * 0.9)

        # câu 61
        self.play(FadeIn(c1, shift=UP * 0.3))
        self.wait(4.4)
        # câu 62
        self.play(FadeIn(c2, shift=UP * 0.3))
        self.wait(2.5)
        self.play(FadeIn(c3, shift=UP * 0.3))

        self.wait(1.6)
        # câu 63
        # tài liệu tham khảo
        refs = VGroup(
            T("References", 22, GREY_T, weight=BOLD),
            T("Stewart, J. (2020). Calculus: Early transcendentals (9th ed.). Cengage.", 18, GREY_T),
            T("Bartle, R. G., & Sherbert, D. R. (2011). Introduction to real analysis (4th ed.). Wiley.", 18, GREY_T),
            T("Huy, N. D. (2021). Giao trinh giai tich 1. VNU-HCM.", 18, GREY_T),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(DOWN * 2.95)
        self.play(FadeIn(refs, shift=UP * 0.2))
        thanks = T("Thank you for watching!", 40, C_N, weight=BOLD).next_to(cards, DOWN, buff=0.4)
        self.play(Write(thanks))
        self.wait(4.3)


# ------------------------------------------------------------
# GHÉP VIDEO
# chạy xong 8 cảnh thì tạo file list.txt, mỗi dòng 1 cảnh theo thứ tự:
#   file 'media/videos/continuity/1080p30/S0_Intro.mp4'
#   file 'media/videos/continuity/1080p30/S1_Definitions.mp4'
#   ... tới S7_Summary
# rồi chạy:
#   ffmpeg -f concat -safe 0 -i list.txt -c copy video_CA04.mp4
# ------------------------------------------------------------
