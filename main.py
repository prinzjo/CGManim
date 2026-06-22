from manim import *
from manim_slides import ThreeDSlide

config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_width  = 16.0
config.frame_height = 9.0


# ═════════════════════════════════════
# 1. TITEL
# ═════════════════════════════════════
class TitleSlide(ThreeDSlide):
    def construct(self):
        titel = Tex("Computergrafik", font_size=84)
        untertitel = Tex("Transformationen, Kamera und Projektion", font_size=48)

        group = VGroup(titel, untertitel).arrange(DOWN, buff=0.5)

        self.play(Write(titel), FadeIn(untertitel))
        self.next_slide()
        self.play(FadeOut(group))


# ═════════════════════════════════════
# 2. AGENDA
# ═════════════════════════════════════
class AgendaSlide(ThreeDSlide):
    def construct(self):
        titel = Tex("Gliederung", font_size=54)

        agenda = BulletedList(
            "Grundlagen: Punkte vs. Vektoren",
            "Lineare 3D-Transformationen (Skalierung \\& Rotation)",
            "Homogene Koordinaten \\& das Translations-Problem",
            "Die View-Matrix (Kamera-Transformation)",
            "Projektionsmatrix \\& Aspect Ratio",
            "Perspective Divide \\& Z-Buffer Herleitung",
            font_size=40,
        )

        group = VGroup(titel, agenda).arrange(DOWN, buff=0.8)

        self.play(Write(titel), FadeIn(agenda))
        self.next_slide()
        self.play(FadeOut(group))


# ═════════════════════════════════════
# 2.5 ERKLÄRUNG: VEKTOR VS. PUNKT
# ═════════════════════════════════════
class VectorVsPointSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        title = Tex("Punkte vs. Vektoren", font_size=44).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6,
        )
        self.play(FadeIn(axes))
        self.next_slide()

        p = np.array([2.0, 1.5, 1.5])

        vector = Arrow3D(
            start=axes.c2p(0, 0, 0), end=axes.c2p(*p),
            color=YELLOW, thickness=0.02,
        )
        point = Sphere(radius=0.12, color=BLUE).move_to(axes.c2p(*p))

        label_vec = MathTex(r"\vec{p} = (2,\;1.5,\;1.5)", font_size=36, color=YELLOW)
        label_vec.to_corner(UR)
        label_pt = MathTex(r"P = (2,\;1.5,\;1.5)", font_size=36, color=BLUE)
        label_pt.next_to(label_vec, DOWN, buff=0.5)

        self.add_fixed_in_frame_mobjects(label_vec, label_pt)
        self.play(Create(vector), FadeIn(point), FadeIn(label_vec), FadeIn(label_pt))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 3.0 VISUELLE SKALIERUNG (3D)
# ═════════════════════════════════════
class Scale3DSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()
        cube = Cube(side_length=1.5, fill_opacity=0.4, color=BLUE)

        title = Tex("Skalierung im 3D-Raum", font_size=48).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        self.play(Create(axes), Create(cube))
        self.next_slide()

        scale_matrix = MathTex(
            r"S = \begin{pmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & s_z \end{pmatrix}",
            font_size=50,
        ).to_corner(UR)

        self.add_fixed_in_frame_mobjects(scale_matrix)
        self.play(FadeIn(scale_matrix))
        self.play(cube.animate.scale(1.5))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 3.1 SKALIERUNG AUF ZAHLENEBENE (MATHE)
# ═════════════════════════════════════
class ScaleMathSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        title = Tex("3D-Skalierung auf Zahlenebene", font_size=44).to_edge(UP)
        self.play(Write(title))

        scale_mat = MathTex(
            r"\begin{pmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & s_z \end{pmatrix}",
            r"\cdot",
            r"\begin{pmatrix} x \\ y \\ z \end{pmatrix}",
            font_size=44
        ).move_to(UP * 1)

        self.play(Write(scale_mat))
        self.next_slide()

        result_detailed = MathTex(
            r"= \begin{pmatrix} s_x \cdot x + 0 \cdot y + 0 \cdot z \\ 0 \cdot x + s_y \cdot y + 0 \cdot z \\ 0 \cdot x + 0 \cdot y + s_z \cdot z \end{pmatrix}",
            font_size=44
        ).next_to(scale_mat, DOWN, buff=0.6)

        self.play(Write(result_detailed))
        self.next_slide()

        result_final = MathTex(
            r"= \begin{pmatrix} s_x \cdot x \\ s_y \cdot y \\ s_z \cdot z \end{pmatrix}",
            font_size=44
        ).move_to(result_detailed.get_center())

        self.play(Transform(result_detailed, result_final))
        self.next_slide()

        explanation = Tex(
            r"Jede Achse wird strikt isoliert voneinander skaliert.\\",
            r"Der Ursprung $(0,0,0)$ bleibt dabei unverändert.",
            font_size=34, color=LIGHT_GREY
        ).next_to(result_detailed, DOWN, buff=0.6)

        self.play(FadeIn(explanation))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 3.2 VISUELLE ROTATION (3D)
# ═════════════════════════════════════
class Rotation3DSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()
        cube = Cube(side_length=1.5, fill_opacity=0.4, color=BLUE)

        title = Tex("Rotation im 3D-Raum", font_size=48).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        self.play(Create(axes), Create(cube))
        self.next_slide()

        rot_matrix = MathTex(
            r"R_z(\alpha) = \begin{pmatrix} \cos\alpha & -\sin\alpha & 0 \\ \sin\alpha & \cos\alpha & 0 \\ 0 & 0 & 1 \end{pmatrix}",
            font_size=50,
        ).to_corner(UR)

        self.add_fixed_in_frame_mobjects(rot_matrix)
        self.play(FadeIn(rot_matrix))
        self.play(Rotate(cube, angle=90 * DEGREES, axis=OUT))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 3.3 ROTATION: BASISVEKTOREN AM EINHEITSKREIS (MATHE)
# ═════════════════════════════════════
class RotationMathSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        title = Tex("Wie funktioniert eine Rotationsmatrix?", font_size=44).to_edge(UP)
        self.play(Write(title))

        core_idea = Tex(
            r"Der Trick der linearen Algebra:\\",
            r"\textbf{Eine Matrix speichert nur, wo die Basisvektoren landen!}",
            font_size=36, color=YELLOW
        ).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(core_idea))
        self.next_slide()

        ax = Axes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=5, y_length=5, tips=False
        ).move_to(LEFT * 3 + DOWN * 0.5)

        circle = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=LIGHT_GREY).move_to(ax.c2p(0, 0))

        self.play(Create(ax), Create(circle), FadeOut(core_idea))
        self.next_slide()

        i_vec = Arrow(start=ax.c2p(0, 0), end=ax.c2p(1, 0), buff=0, color=RED, stroke_width=4,
                      max_tip_length_to_length_ratio=0.15)
        j_vec = Arrow(start=ax.c2p(0, 0), end=ax.c2p(0, 1), buff=0, color=GREEN, stroke_width=4,
                      max_tip_length_to_length_ratio=0.15)

        i_label = MathTex(r"\hat{i} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}", color=RED, font_size=32).next_to(i_vec, DOWN)
        j_label = MathTex(r"\hat{j} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}", color=GREEN, font_size=32).next_to(j_vec, LEFT)

        self.play(Create(i_vec), Create(j_vec))
        self.play(FadeIn(i_label), FadeIn(j_label))
        self.next_slide()

        alpha = 35 * DEGREES

        rotating_text = Tex(r"Wir rotieren um den Winkel $\alpha$...", font_size=36).move_to(RIGHT * 3 + UP * 1.5)
        self.play(Write(rotating_text))
        self.play(FadeOut(i_label), FadeOut(j_label))

        self.play(
            Rotate(i_vec, angle=alpha, about_point=ax.c2p(0, 0)),
            Rotate(j_vec, angle=alpha, about_point=ax.c2p(0, 0)),
            run_time=2
        )
        self.next_slide()

        self.play(FadeOut(rotating_text))

        i_end = i_vec.get_end()
        i_x_line = DashedLine(ax.c2p(0, 0), [i_end[0], ax.c2p(0, 0)[1], 0], color=RED_B)
        i_y_line = DashedLine([i_end[0], ax.c2p(0, 0)[1], 0], i_end, color=RED_B)

        angle_arc = Arc(radius=0.7, start_angle=0, angle=alpha, arc_center=ax.c2p(0, 0), color=YELLOW)
        angle_label = MathTex(r"\alpha", font_size=28, color=YELLOW).next_to(angle_arc, RIGHT, buff=0.1).shift(UP * 0.1)

        self.play(Create(angle_arc), FadeIn(angle_label))
        self.play(Create(i_x_line), Create(i_y_line))

        i_math = MathTex(
            r"\hat{i}' = \begin{pmatrix} \cos(\alpha) \\ \sin(\alpha) \end{pmatrix}",
            color=RED, font_size=40
        ).move_to(RIGHT * 3 + UP * 1)

        self.play(Write(i_math))
        self.next_slide()

        j_end = j_vec.get_end()
        j_x_line = DashedLine(ax.c2p(0, 0), [j_end[0], ax.c2p(0, 0)[1], 0], color=GREEN_B)
        j_y_line = DashedLine([j_end[0], ax.c2p(0, 0)[1], 0], j_end, color=GREEN_B)

        self.play(Create(j_x_line), Create(j_y_line))

        j_math = MathTex(
            r"\hat{j}' = \begin{pmatrix} -\sin(\alpha) \\ \cos(\alpha) \end{pmatrix}",
            color=GREEN, font_size=40
        ).next_to(i_math, DOWN, buff=0.8)

        j_note = Tex(r"(x geht nach links $\to$ negativ!)", font_size=28, color=LIGHT_GREY).next_to(j_math, DOWN, buff=0.2)

        self.play(Write(j_math), FadeIn(j_note))
        self.next_slide()

        self.play(FadeOut(j_note))

        final_text = Tex("Die Spalten bilden die fertige Matrix:", font_size=36, color=YELLOW).move_to(RIGHT * 3 + UP * 2.5)

        self.play(
            Write(final_text),
            VGroup(i_math, j_math).animate.next_to(final_text, DOWN, buff=0.5)
        )

        base_matrix = MathTex(
            r"R = \begin{pmatrix}",
            r"i_x", r"&", r"j_x", r"\\",
            r"i_y", r"&", r"j_y",
            r"\end{pmatrix}",
            font_size=44
        ).next_to(j_math, DOWN, buff=0.8)

        base_matrix[1].set_color(RED)
        base_matrix[5].set_color(RED)
        base_matrix[3].set_color(GREEN)
        base_matrix[7].set_color(GREEN)

        self.play(Write(base_matrix))
        self.next_slide()

        final_matrix = MathTex(
            r"R(\alpha) = \begin{pmatrix}",
            r"\cos(\alpha)", r"&", r"-\sin(\alpha)", r"\\",
            r"\sin(\alpha)", r"&", r"\cos(\alpha)",
            r"\end{pmatrix}",
            font_size=44
        ).move_to(base_matrix.get_center())

        final_matrix[1].set_color(RED)
        final_matrix[5].set_color(RED)
        final_matrix[3].set_color(GREEN)
        final_matrix[7].set_color(GREEN)

        self.play(Transform(base_matrix, final_matrix))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 4. TRANSLATIONSPROBLEM
# ═════════════════════════════════════
class TranslationProblemSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        title = Tex("Das Problem der Translation", font_size=48).to_edge(UP)

        bullets = BulletedList(
            "Rotation \\& Skalierung = linear",
            "Translation verschiebt Ursprung",
            "3×3 Matrix reicht nicht",
            r"$\vec{p}' = M\vec{p} + \vec{t}$",
            font_size=38
        ).move_to(ORIGIN)

        self.play(Write(title))
        self.play(FadeIn(bullets))
        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 5. HOMOGENE KOORDINATEN (GEFIXT!)
# ═════════════════════════════════════
class HomogeneousSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        title = Tex("Homogene Koordinaten", font_size=48).to_edge(UP)

        step_mat = MathTex(
            r"\begin{pmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{pmatrix}",
            r"\cdot",
            r"\begin{pmatrix} x \\ y \\ z \\ 1 \end{pmatrix}",
            font_size=44
        ).move_to(UP * 1)

        result_step = MathTex(
            r"= \begin{pmatrix} 1 \cdot x + 0 \cdot y + 0 \cdot z + t_x \cdot 1 \\ 0 \cdot x + 1 \cdot y + 0 \cdot z + t_y \cdot 1 \\ 0 \cdot x + 0 \cdot y + 1 \cdot z + t_z \cdot 1 \\ 1 \end{pmatrix}",
            r"= \begin{pmatrix} x + t_x \\ y + t_y \\ z + t_z \\ 1 \end{pmatrix}",
            font_size=44
        ).next_to(step_mat, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(Write(step_mat))
        self.next_slide()
        self.play(Write(result_step[0]))
        self.next_slide()
        self.play(Transform(result_step[0], result_step[1]))
        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 5.5 SCHERUNG = TRANSLATION IN 4D
# ═════════════════════════════════════
class ShearSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-135 * DEGREES)

        title = Tex("Scherung in 3D", font_size=44).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
            x_length=6, y_length=4, z_length=4,
        )
        self.play(FadeIn(axes))

        h = 1.0
        b = [np.array(c) for c in [(-h, -h, -h), (h, -h, -h), (h, h, -h), (-h, h, -h)]]
        t = [np.array(c) for c in [(-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)]]

        face_bottom = Polygon(*b, fill_color=BLUE_D, fill_opacity=0.55, stroke_color=WHITE, stroke_width=1.5)
        face_top = Polygon(*t, fill_color=RED_C, fill_opacity=0.80, stroke_color=WHITE, stroke_width=2.0)
        face_front = Polygon(b[0], b[1], t[1], t[0], fill_color=TEAL_D, fill_opacity=0.45, stroke_color=WHITE,
                             stroke_width=1.5)
        face_right = Polygon(b[1], b[2], t[2], t[1], fill_color=GREEN_D, fill_opacity=0.45, stroke_color=WHITE,
                             stroke_width=1.5)
        face_back = Polygon(b[2], b[3], t[3], t[2], fill_color=TEAL_D, fill_opacity=0.45, stroke_color=WHITE,
                            stroke_width=1.5)
        face_left = Polygon(b[3], b[0], t[0], t[3], fill_color=GREEN_D, fill_opacity=0.45, stroke_color=WHITE,
                            stroke_width=1.5)

        cube = VGroup(face_bottom, face_top, face_front, face_right, face_back, face_left)
        self.play(FadeIn(cube))
        self.next_slide()

        arr_top = Arrow3D(start=np.array([0, 0, h]), end=np.array([1.4, 0, h]), color=YELLOW, thickness=0.02)
        arr_bot = Arrow3D(start=np.array([0, 0, -h]), end=np.array([-1.4, 0, -h]), color=YELLOW, thickness=0.02)
        self.play(FadeIn(arr_top, arr_bot))
        self.next_slide()

        s = 0.8

        def shear_func(point):
            x, y, z = point
            return np.array([x + s * z, y, z])

        self.play(
            ApplyPointwiseFunction(shear_func, cube),
            FadeOut(arr_top), FadeOut(arr_bot),
            run_time=2.5,
        )
        self.next_slide()

        top_ghost = Polygon(*t, fill_opacity=0, stroke_color=YELLOW, stroke_width=1.5)
        top_ghost.set_stroke(opacity=0.4)

        trans_arrow = Arrow3D(
            start=np.array([0, 0, h]), end=np.array([s * h, 0, h]),
            color=YELLOW, thickness=0.025,
        )

        self.play(
            FadeOut(face_bottom), FadeOut(face_front), FadeOut(face_right),
            FadeOut(face_back), FadeOut(face_left), FadeOut(axes),
            FadeIn(top_ghost),
        )
        self.play(Create(trans_arrow))
        self.next_slide()

        conclusion = Tex(
            r"Oberseite wurde nur verschoben $\to$ 2D-Translation",
            font_size=34,
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 6. KAMERA-TRANSFORMATION
# ═════════════════════════════════════
class CameraSlide(ThreeDSlide):
    def construct(self):
        title = Text("Kamera-Transformation", font_size=40).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)
        self.play(Write(title))

        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=0.8)

        world = VGroup()
        for x in range(-3, 4):
            world.add(Line3D([x, -3, 0], [x, 3, 0], color=GREY, stroke_width=0.8))
        for y in range(-3, 4):
            world.add(Line3D([-3, y, 0], [3, y, 0], color=GREY, stroke_width=0.8))

        target_cube = Cube(side_length=0.5, fill_color=GREEN, fill_opacity=0.8)
        target_cube.move_to([2, 2, 0.5])
        world.add(target_cube)

        shaft_length = 0.8
        tip_length = 0.3

        shaft = Cylinder(radius=0.06, height=shaft_length, fill_color=BLUE, fill_opacity=1, stroke_width=0, direction=OUT)
        tip = Cone(base_radius=0.15, height=tip_length, fill_color=RED, fill_opacity=1, direction=IN, stroke_width=0)
        tip.shift(IN * (shaft_length / 1.2))

        cam_arrow = VGroup(shaft, tip)
        cam_arrow.move_to([0, 0, 3])

        self.play(FadeIn(world), FadeIn(cam_arrow))
        self.next_slide()

        label_trans = Text("Kamera Bewegung", font_size=30, color=YELLOW).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(label_trans)
        self.remove(label_trans)
        self.play(Write(label_trans))

        self.play(cam_arrow.animate.shift(RIGHT * 2 + UP * 2), run_time=1.5)
        self.next_slide()

        self.play(cam_arrow.animate.shift(LEFT * 2 + DOWN * 2), run_time=0.1)
        self.next_slide()

        self.play(world.animate.shift(LEFT * 2 + DOWN * 2), run_time=2)
        self.next_slide()

        self.play(FadeOut(*self.mobjects))


# ═════════════════════════════════════
# 7. PROJEKTION (VEREINFACHT)
# ═════════════════════════════════════
class ProjectionSlide(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1
        )

        title = Tex("Projektionsidee", font_size=48).to_edge(UP)

        agenda = BulletedList(
            "Perspektive: Je weiter Objekte weg sind, desto kleiner erscheinen sie",
            "Field of View (FOV): Definiert die Sichtweite / den Sichtkegel",
            "NDC Format: Abbildung in den Einheitswürfel $[-1, 1] \\times [-1, 1] \\times [-1, 1]$ ",
            font_size=40,
        ).arrange(DOWN, buff=0.8)

        self.play(Write(title), FadeIn(agenda))
        self.next_slide()
        self.play(FadeOut(*self.mobjects))


class ProjectionDiagramSlide(ThreeDSlide):
    def construct(self):
        scale = 2.5

        origin = np.array([-5.0, 0.0, 0.0])

        y_axis = Line(origin + DOWN * 3.5, origin + UP * 3.5, color=WHITE)
        z_axis = Line(origin, origin + RIGHT * 11, color=WHITE)

        lbl_y_plus = Text("+Y", font_size=36).next_to(y_axis, UP)
        lbl_y_minus = Text("-Y", font_size=36).next_to(y_axis, DOWN)
        lbl_z_plus = Text("+Z", font_size=36).next_to(z_axis, RIGHT)
        lbl_origin = Text("(0,0,0)", font_size=32).next_to(origin, LEFT)

        axes_group = VGroup(y_axis, z_axis, lbl_y_plus, lbl_y_minus, lbl_z_plus, lbl_origin)

        z_proj_dist = 2.0
        proj_x = origin[0] + z_proj_dist

        proj_top = np.array([proj_x, 1 * scale, 0.0])
        proj_bottom = np.array([proj_x, -1 * scale, 0.0])

        proj_plane = Line(proj_bottom, proj_top, color=LIGHT_GREY)

        lbl_1 = Text("1", font_size=28, color=YELLOW).next_to(proj_top, UP, buff=0.1)
        lbl_minus_1 = Text("-1", font_size=28, color=YELLOW).next_to(proj_bottom, DOWN, buff=0.1)

        frustum_top = Line(origin, origin + np.array([10.0, 10.0 * (1 * scale / z_proj_dist), 0.0]), color=RED)
        frustum_bottom = Line(origin, origin + np.array([10.0, 10.0 * (-1 * scale / z_proj_dist), 0.0]), color=RED)

        bottom_angle = np.arctan2(-1 * scale / z_proj_dist, 1.0)
        fov_arc = Arc(
            radius=1.8,
            start_angle=bottom_angle,
            angle=abs(bottom_angle),
            arc_center=origin,
            color=YELLOW
        )
        fov_label = MathTex(r"\frac{FOV}{2}", font_size=32, color=YELLOW)
        fov_label.move_to(origin + np.array([1.0, -0.6, 0.0]))

        fov_group = VGroup(fov_arc, fov_label)

        d_y_offset = -2.0
        d_arrow = DoubleArrow(
            origin + np.array([0.0, d_y_offset, 0.0]),
            np.array([proj_x, origin[1] + d_y_offset, 0.0]),
            buff=0,
            color=WHITE,
            tip_length=0.2
        )
        d_tick_left = Line(origin + np.array([0.0, d_y_offset + 0.1, 0.0]),
                           origin + np.array([0.0, d_y_offset - 0.1, 0.0]), color=WHITE)
        d_tick_right = Line(np.array([proj_x, origin[1] + d_y_offset + 0.1, 0.0]),
                            np.array([proj_x, origin[1] + d_y_offset - 0.1, 0.0]), color=WHITE)

        d_label = MathTex("d", font_size=36).next_to(d_arrow, DOWN, buff=0.1)
        d_group = VGroup(d_arrow, d_tick_left, d_tick_right, d_label)

        eq1 = MathTex(r"\tan\left(\frac{FOV}{2}\right) = \frac{1}{d}", font_size=40)
        eq2 = MathTex(r"\implies d = \frac{1}{\tan\left(\frac{FOV}{2}\right)}", font_size=40)

        eq2.to_corner(RIGHT + (0, 7, 0), buff=0.8)
        eq1.next_to(eq2, LEFT, buff=0.5)

        eq3 = MathTex(r"\frac{y_p}{d} = \frac{y}{z}", font_size=40)
        eq4 = MathTex(r"\implies y_p = \frac{y \cdot d}{z}", font_size=40)
        eq5 = MathTex(r"= \frac{y}{z \cdot \tan\left(\frac{FOV}{2}\right)}", font_size=40)

        eq3.next_to(eq1, DOWN, buff=0.8, aligned_edge=LEFT)
        eq4.next_to(eq3, RIGHT, buff=0.5)
        eq5.next_to(eq4, RIGHT, buff=0.3)

        h_obj = 1.8 * scale
        w_obj = 0.4

        z_obj = 9.0
        pillar = Rectangle(width=w_obj, height=h_obj, fill_color=LIGHT_GREY, fill_opacity=0.3, color=WHITE)
        pillar.move_to(np.array([origin[0] + z_obj + w_obj / 2, h_obj / 2, 0.0]))

        p_top_left = np.array([origin[0] + z_obj, h_obj, 0.0])
        dash = DashedLine(p_top_left, origin, color=GREY, dashed_ratio=0.5)

        dot_pillar = Dot(p_top_left, color=RED)
        label_pillar = MathTex(r"(x, y, z)", font_size=32, color=RED).next_to(dot_pillar, DOWN + LEFT, buff=0.1)

        intersect_y = h_obj * (z_proj_dist / z_obj)
        p_intersect = np.array([proj_x, intersect_y, 0.0])

        dot_proj = Dot(p_intersect, color=RED)
        label_proj = MathTex(r"(\dots, y_p, d)", font_size=32, color=RED).next_to(dot_proj, DOWN + RIGHT, buff=0.1)

        self.play(Create(axes_group))
        self.play(Create(frustum_top), Create(frustum_bottom))

        self.next_slide()
        self.play(
            Create(proj_plane),
            Write(lbl_1),
            Write(lbl_minus_1)
        )

        self.next_slide()
        self.play(Create(fov_group), Create(d_group))

        self.next_slide()
        self.play(Write(eq1))

        self.next_slide()
        self.play(Write(eq2))

        self.next_slide()
        self.play(FadeIn(pillar))
        self.play(Create(dash))

        self.next_slide()
        self.play(FadeIn(dot_pillar), Write(label_pillar))

        self.next_slide()
        self.play(FadeIn(dot_proj), Write(label_proj))

        self.next_slide()
        self.play(Write(eq3))

        self.next_slide()
        self.play(Write(eq4))

        self.next_slide()
        self.play(Write(eq5))

        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 8. PROJEKTIONSMATRIX
# ═════════════════════════════════════
class ProjectionMatrixSlide(ThreeDSlide):
    def construct(self):
        title = Text("Aufbau der Projektionsmatrix", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))

        target_label = Text("Ziel:", font_size=38, color=YELLOW)
        target_eqs = MathTex(
            r"\begin{aligned} "
            r"x_p &= \frac{x}{z \cdot \tan\left(\frac{FOV}{2}\right)} \\[1.5ex] "
            r"y_p &= \frac{y}{z \cdot \tan\left(\frac{FOV}{2}\right)} "
            r"\end{aligned}",
            font_size=38
        )

        target_group = VGroup(target_label, target_eqs).arrange(DOWN, aligned_edge=LEFT)
        target_group.to_edge(RIGHT, buff=0.8)

        self.play(FadeIn(target_group))

        mat_size = 44

        mat_id = MathTex(
            r"\begin{bmatrix} "
            r"1 & 0 & 0 & 0 \\ "
            r"0 & 1 & 0 & 0 \\ "
            r"0 & 0 & 1 & 0 \\ "
            r"0 & 0 & 0 & 1 "
            r"\end{bmatrix}",
            font_size=mat_size
        )
        vec_in = MathTex(
            r"\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}",
            font_size=mat_size
        )
        equals = MathTex("=", font_size=mat_size + 4)
        vec_out_id = MathTex(
            r"\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}",
            font_size=mat_size
        )

        group_step1 = VGroup(mat_id, vec_in, equals, vec_out_id).arrange(RIGHT, buff=0.2)
        group_step1.move_to(LEFT * 1.5)

        self.play(
            Write(mat_id),
            Write(vec_in),
            Write(equals),
            Write(vec_out_id)
        )

        self.next_slide()

        mat_scaled = MathTex(
            r"\begin{bmatrix} "
            r"\frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\ "
            r"0 & \frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\ "
            r"0 & 0 & 1 & 0 \\ "
            r"0 & 0 & 0 & 1 "
            r"\end{bmatrix}",
            font_size=mat_size
        )

        vec_out_scaled = MathTex(
            r"\begin{bmatrix} "
            r"\frac{x}{\tan\left(\frac{FOV}{2}\right)} \\[1.5ex] "
            r"\frac{y}{\tan\left(\frac{FOV}{2}\right)} \\[1ex] "
            r"z \\ "
            r"1 "
            r"\end{bmatrix}",
            font_size=mat_size
        )

        group_step2 = VGroup(mat_scaled, vec_in.copy(), equals.copy(), vec_out_scaled).arrange(RIGHT, buff=0.2)
        group_step2.move_to(LEFT * 1.5)

        self.play(
            Transform(mat_id, mat_scaled),
            Transform(vec_in, group_step2[1]),
            Transform(equals, group_step2[2]),
            Transform(vec_out_id, vec_out_scaled)
        )

        self.next_slide()

        info_text = Tex(
            r"Matrix kann nicht durch eine Variable wie $z$ dividieren\\",
            r"$\Rightarrow$ Die feste Grafikpipeline hat einen Schritt (Perspective Divide), wo $x, y, z$ am Ende automatisch durch $w$.",
            font_size=36, color=LIGHT_GREY
        )
        info_text.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(info_text))

        self.next_slide()

        mat_persp = MathTex(
            r"\begin{bmatrix} "
            r"\frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\ "
            r"0 & \frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\ "
            r"0 & 0 & 1 & 0 \\ "
            r"0 & 0 & 1 & 0 "
            r"\end{bmatrix}",
            font_size=mat_size
        )

        vec_out_persp = MathTex(
            r"\begin{bmatrix} "
            r"\frac{x}{\tan\left(\frac{FOV}{2}\right)} \\[1.5ex] "
            r"\frac{y}{\tan\left(\frac{FOV}{2}\right)} \\[1ex] "
            r"z \\ "
            r"z "
            r"\end{bmatrix}",
            font_size=mat_size
        )

        group_step3 = VGroup(mat_persp, vec_in.copy(), equals.copy(), vec_out_persp).arrange(RIGHT, buff=0.2)
        group_step3.move_to(LEFT * 1.5)

        self.play(
            Transform(mat_id, mat_persp),
            Transform(vec_in, group_step3[1]),
            Transform(equals, group_step3[2]),
            Transform(vec_out_id, vec_out_persp)
        )

        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 8.1 PROJEKTIONSMATRIX
# ═════════════════════════════════════
class ProjectionZDerivationSlide(ThreeDSlide):
    def construct(self):
        title = Text("Herleitung für Z-Near und Z-Far", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))

        mat_size = 40

        mat = MathTex(
            r"\begin{bmatrix} "
            r"\frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\ "
            r"0 & \frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\ "
            r"a & b & c & d \\ "
            r"0 & 0 & 1 & 0 "
            r"\end{bmatrix}",
            font_size=mat_size
        )
        vec_in = MathTex(
            r"\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}",
            font_size=mat_size
        )
        equals = MathTex("=", font_size=mat_size + 4)

        vec_out = MathTex(
            r"\begin{bmatrix} \dots \\ \dots \\ ax + by + cz + d \cdot 1 \\ z \end{bmatrix}",
            font_size=mat_size
        )

        equation_group = VGroup(mat, vec_in, equals, vec_out).arrange(RIGHT, buff=0.2)
        equation_group.move_to(UP * 0.5)

        self.play(Write(equation_group))

        self.next_slide()

        explanation = Tex("Welche Reihe bestimmt die neue $z$-Komponente?", font_size=36, color=YELLOW)
        explanation.next_to(equation_group, DOWN, buff=0.4)
        self.play(Write(explanation))

        self.next_slide()
        self.play(FadeOut(explanation))

        formula = MathTex(r"ax", r"+", r"by", r"+", r"cz", r"+", r"d", font_size=48)
        formula.move_to(DOWN * 1.5)
        self.play(Write(formula))

        self.next_slide()

        info_text = Tex(
            r"Die Tiefe eines Punktes darf nicht von seiner horizontalen ($x$) oder\\",
            r"vertikalen ($y$) Position auf dem Bildschirm abhängen.\\",
            r"$\Rightarrow$ $ax$ und $by$ sind für die Tiefenabbildung nutzlos.",
            font_size=36, color=LIGHT_GREY
        )
        info_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(info_text))

        self.next_slide()

        cross_ax = Line(
            formula[0].get_corner(DL) + LEFT * 0.05 + DOWN * 0.05,
            formula[0].get_corner(UR) + RIGHT * 0.05 + UP * 0.05,
            color=RED, stroke_width=4
        )
        cross_by = Line(
            formula[2].get_corner(DL) + LEFT * 0.05 + DOWN * 0.05,
            formula[2].get_corner(UR) + RIGHT * 0.05 + UP * 0.05,
            color=RED, stroke_width=4
        )

        self.play(Create(cross_ax), Create(cross_by))

        self.next_slide()

        self.play(
            FadeOut(info_text),
            FadeOut(cross_ax),
            FadeOut(cross_by),
            FadeOut(formula[0]),  # ax
            FadeOut(formula[1]),  # +
            FadeOut(formula[2]),  # by
            FadeOut(formula[3]),  # +
        )

        remaining_formula = VGroup(formula[4], formula[5], formula[6])
        self.play(remaining_formula.animate.move_to(DOWN * 1.5))

        self.next_slide()

        div_text = Tex(
            r"Nun müssen wir die anschließende Division durch die $w$-Komponente beachten.\\",
            r"Da $w = z$ ist, wird der gesamte Ausdruck am Ende durch $z$ geteilt:",
            font_size=36, color=LIGHT_GREY
        )
        div_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(div_text))

        self.next_slide()

        formula_fraction = MathTex(
            r"z_p = \frac{cz + d}{z}",
            font_size=48
        ).move_to(DOWN * 1.5)

        self.play(Transform(remaining_formula, formula_fraction))

        self.next_slide()

        formula_final = MathTex(
            r"z_p = c + \frac{d}{z}",
            font_size=48
        ).move_to(DOWN * 1.5)

        self.play(
            FadeOut(div_text),
            Transform(remaining_formula, formula_final)
        )

        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))


# ═════════════════════════════════════
# 8.2 PROJEKTIONSMATRIX
# ═════════════════════════════════════
class ProjectionSolveSystemSlide(ThreeDSlide):
    def construct(self):
        title = Text("Berechnung von c und d", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        system_title = Tex("Abbildung in die Normalized Device Coordinates (NDC)", font_size=32, color=YELLOW)
        system_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(system_title))

        eq1 = MathTex(r"(I) \quad c + \frac{d}{z_{near}} = -1", font_size=36)
        eq2 = MathTex(r"(II) \quad c + \frac{d}{z_{far}} = 1", font_size=36)

        eq_group = VGroup(eq1, eq2).arrange(DOWN, buff=0.3).next_to(system_title, DOWN, buff=0.4)
        self.play(Write(eq_group))
        self.next_slide()

        note = Tex("Zur Übersichtlichkeit: $z_{near} = n$, $z_{far} = f$", font_size=28, color=LIGHT_GREY)
        note.next_to(eq_group, DOWN, buff=0.4)
        self.play(FadeIn(note))

        eq1_short = MathTex(r"(I) \quad c + \frac{d}{n} = -1", font_size=36)
        eq2_short = MathTex(r"(II) \quad c + \frac{d}{f} = 1", font_size=36)
        eq_group_short = VGroup(eq1_short, eq2_short).arrange(DOWN, buff=0.3).move_to(eq_group)

        self.play(
            Transform(eq1, eq1_short),
            Transform(eq2, eq2_short)
        )
        self.next_slide()

        self.play(FadeOut(note))

        step1_text = Tex("1. Gleichung (II) nach $c$ auflösen:", font_size=32, color=YELLOW)
        step1_text.next_to(eq_group_short, DOWN, buff=0.4).align_to(eq_group_short, LEFT)

        eq_c_temp = MathTex(r"c = 1 - \frac{d}{f}", font_size=36).next_to(step1_text, DOWN, buff=0.2)
        self.play(Write(step1_text), Write(eq_c_temp))
        self.next_slide()

        step2_text = Tex("2. $c$ in Gleichung (I) einsetzen:", font_size=32, color=YELLOW)
        step2_text.next_to(eq_c_temp, DOWN, buff=0.4).align_to(eq_group_short, LEFT)

        eq_sub = MathTex(r"1 - \frac{d}{f} + \frac{d}{n} = -1", font_size=36).next_to(step2_text, DOWN, buff=0.2)
        self.play(Write(step2_text), Write(eq_sub))
        self.next_slide()

        self.play(
            FadeOut(system_title), FadeOut(eq_group), FadeOut(eq1), FadeOut(eq2),
            FadeOut(step1_text), FadeOut(eq_c_temp), FadeOut(step2_text),
            eq_sub.animate.next_to(title, DOWN, buff=0.5)
        )
        self.next_slide()

        step3_text = Tex("3. Nach $d$ auflösen:", font_size=32, color=YELLOW).next_to(eq_sub, DOWN, buff=0.3)
        self.play(Write(step3_text))

        d_eq1 = MathTex(r"\frac{d}{n} - \frac{d}{f} = -2", font_size=36)
        d_eq2 = MathTex(r"d \cdot \left(\frac{1}{n} - \frac{1}{f}\right) = -2", font_size=36)
        d_eq3 = MathTex(r"d \cdot \left(\frac{f - n}{n \cdot f}\right) = -2", font_size=36)
        d_eq4 = MathTex(r"d = \frac{-2 n f}{f - n}", font_size=40, color=GREEN)

        d_group = VGroup(d_eq1, d_eq2, d_eq3, d_eq4).arrange(DOWN, buff=0.3).next_to(step3_text, DOWN, buff=0.3)

        self.play(Write(d_eq1))
        self.next_slide()
        self.play(Write(d_eq2))
        self.next_slide()
        self.play(Write(d_eq3))
        self.next_slide()
        self.play(Write(d_eq4))
        self.next_slide()

        self.play(
            FadeOut(eq_sub), FadeOut(step3_text),
            FadeOut(d_eq1), FadeOut(d_eq2), FadeOut(d_eq3),
            d_eq4.animate.next_to(title, DOWN, buff=0.5)
        )
        self.next_slide()

        step4_text = Tex(r"4. $d$ in $c = 1 - \frac{d}{f}$ einsetzen:", font_size=32, color=YELLOW)
        step4_text.next_to(d_eq4, DOWN, buff=0.4)
        self.play(Write(step4_text))

        c_eq1 = MathTex(r"c = 1 - \frac{1}{f} \cdot \left(\frac{-2 n f}{f - n}\right)", font_size=36)
        c_eq2 = MathTex(r"c = 1 + \frac{2 n}{f - n}", font_size=36)
        c_eq3 = MathTex(r"c = \frac{f - n}{f - n} + \frac{2 n}{f - n}", font_size=36)
        c_eq4 = MathTex(r"c = \frac{f + n}{f - n}", font_size=40, color=GREEN)

        c_group = VGroup(c_eq1, c_eq2, c_eq3, c_eq4).arrange(DOWN, buff=0.3).next_to(step4_text, DOWN, buff=0.3)

        self.play(Write(c_eq1))
        self.next_slide()
        self.play(Write(c_eq2))
        self.next_slide()
        self.play(Write(c_eq3))
        self.next_slide()
        self.play(Write(c_eq4))
        self.next_slide()

        self.play(
            FadeOut(step4_text), FadeOut(c_eq1), FadeOut(c_eq2), FadeOut(c_eq3)
        )

        results_group = VGroup(c_eq4, d_eq4).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        self.play(
            c_eq4.animate.move_to(results_group[0].get_center()),
            d_eq4.animate.move_to(results_group[1].get_center())
        )

        final_text = Tex("Die Matrix-Einträge sind berechnet!", font_size=36, color=YELLOW)
        final_text.next_to(results_group, UP, buff=1)
        self.play(Write(final_text))
        self.next_slide()

        self.play(
            FadeOut(final_text),
            FadeOut(c_eq4),
            FadeOut(d_eq4),
            Transform(title, Text("Die fertige Projektionsmatrix", font_size=40).to_edge(UP))
        )

        mat_size = 38
        final_matrix = MathTex(
            r"\begin{bmatrix} "
            r"\frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\ "
            r"0 & \frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\ "
            r"0 & 0 & \frac{f + n}{f - n} & \frac{-2nf}{f - n} \\ "
            r"0 & 0 & 1 & 0 "
            r"\end{bmatrix}",
            font_size=mat_size
        )

        final_matrix.move_to(ORIGIN)

        matrix_explanation = Tex(
            r"Mit $a=0$ und $b=0$ (da $x$ und $y$ keinen Einfluss auf die Tiefe haben)\\",
            r"sowie den eben berechneten Werten für $c$ und $d$.",
            font_size=32, color=LIGHT_GREY
        ).next_to(final_matrix, DOWN, buff=0.8)

        self.play(Write(final_matrix))
        self.next_slide()
        self.play(FadeIn(matrix_explanation))

        self.next_slide()
        self.play(FadeOut(Group(*self.mobjects)))

# ═════════════════════════════════════
# MAIN
# ═════════════════════════════════════
class ComputergrafikPraesentation(ThreeDSlide):
    def construct(self):
        TitleSlide.construct(self)
        AgendaSlide.construct(self)
        VectorVsPointSlide.construct(self)
        Scale3DSlide.construct(self)
        ScaleMathSlide.construct(self)
        Rotation3DSlide.construct(self)
        RotationMathSlide.construct(self)
        TranslationProblemSlide.construct(self)
        HomogeneousSlide.construct(self)
        ShearSlide.construct(self)
        CameraSlide.construct(self)
        ProjectionSlide.construct(self)
        ProjectionDiagramSlide.construct(self)
        ProjectionMatrixSlide.construct(self)
        ProjectionZDerivationSlide.construct(self)
        ProjectionSolveSystemSlide.construct(self)
