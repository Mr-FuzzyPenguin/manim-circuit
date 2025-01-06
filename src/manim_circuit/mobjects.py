from manim import *
from .utils import *


class VoltageSource(Source):
    def __init__(self, value=1, label=True, direction=LEFT, dependent=True, **kwargs):
        # + and -
        markings = VGroup()
        markings.add(Line(DOWN * 0.3, UP * 0.3).shift(UP * 0.5))
        markings.add(Line(LEFT * 0.3, RIGHT * 0.3).shift(UP * 0.5))
        markings.add(Line(LEFT * 0.3, RIGHT * 0.3).shift(DOWN * 0.5))

        super().__init__(
            markings,
            letter="V",
            value=value,
            direction=direction,
            dependent=dependent,
            **kwargs,
        )


class CurrentSource(Source):
    def __init__(self, value=1, label=True, direction=LEFT, dependent=True, **kwargs):
        # Arrow
        markings = Line(DOWN * 0.75, UP * 0.75).add_tip(tip_shape=StealthTip)
        super().__init__(
            markings,
            letter="A",
            value=value,
            direction=direction,
            dependent=dependent,
            **kwargs,
        )


class Inductor(VMobject):
    def __init__(self, label=None, direction=DOWN, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        self.main_body = (
            ParametricFunction(
                (lambda t: ((np.cos(t) / 1.94) + (t / (2.21 * PI)), -np.sin(t), 0)),
                t_range=(-PI, 8 * PI),
            )
            .scale(0.25)
            .center()
        )

        self.add(self.main_body)

        # check if lebel is present.
        if not label is None:
            self.label = (
                Tex(str(label) + " H")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)
        else:
            self.label = None

    def get_anchors(self):
        return [self.main_body.get_start(), self.main_body.get_end()]

    def get_terminals(self, val):
        if val == "left":
            return self.main_body.get_start()
        elif val == "right":
            return self.main_body.get_end()

    def center(self):
        self.shift(
            DOWN * self.main_body.get_center()[1] + LEFT * self.main_body.get_center()
        )

        return self

    def rotate(self, angle, *args, **kwargs):
        super().rotate(angle, about_point=self.main_body.get_center(), *args, **kwargs)
        if not self.label == None:
            self.label.rotate(-angle).next_to(self.main_body, self._direction, buff=0.1)

        return self


class Resistor(VMobject):
    def __init__(self, label=None, direction=DOWN, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        # Less points, more cleaner!
        self.main_body = VMobject()
        points = [
            [-0.96795, 0, 0],
            [-0.54268, 1, 0],
            [0.30788, -1, 0],
            [1.15843, 1, 0],
            [2.00899, -1, 0],
            [2.85954, 1, 0],
            [3.7101, -1, 0],
            [4.13537, 0, 0],
        ]
        self.main_body.start_new_path(points[0])
        for i in points[1:]:
            self.main_body.add_line_to(np.array(i))
        self.main_body.scale(0.25).center()

        self.add(self.main_body)

        # check if lebel is present.
        if not label is None:
            self.label = (
                Tex(str(label) + r" $\Omega $")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)
        else:
            self.label = None

    def get_anchors(self):
        return [self.main_body.get_start(), self.main_body.get_end()]

    def get_terminals(self, val):
        if val == "left":
            return self.main_body.get_start()
        elif val == "right":
            return self.main_body.get_end()

    def center(self):
        self.shift(
            DOWN * self.main_body.get_center()[1] + LEFT * self.main_body.get_center()
        )

        return self

    def rotate(self, angle, *args, **kwargs):
        super().rotate(angle, about_point=self.main_body.get_center(), *args, **kwargs)
        if not self.label == None:
            self.label.rotate(-angle).next_to(self.main_body, self._direction, buff=0.1)

        return self


class Capacitor(VMobject):
    def __init__(self, label=None, direction=DOWN, polarized=False, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        self.main_body = VGroup(
            Line([(7 / 4.42) - 0.125, 1, 0], [(7 / 4.42) - 0.125, -1, 0]),
        )

        # not polarized:
        if not polarized:
            self.main_body.add(
                Line([(7 / 4.42) + 0.125, 1, 0], [(7 / 4.42) + 0.125, -1, 0])
            )
        else:
            self.main_body.add(
                ArcBetweenPoints(
                    start=[(7 / 4.42) + 0.325, 1, 0],
                    end=[(7 / 4.42) + 0.325, -1, 0],
                    angle=PI / 4,
                )
            )
            pass

        self.main_body.scale(0.25).center()

        self.add(self.main_body)

        # check if lebel is present.
        if not label is None:
            self.label = (
                Tex(str(label) + "F")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)

    def get_terminals(self, val):
        if val == "left":
            return self.main_body[0].get_midpoint()
        elif val == "right":
            return self.main_body[1].get_midpoint()

    def center(self):
        self.shift(
            DOWN * self.main_body.get_center()[1] + LEFT * self.main_body.get_center()
        )

        return self

    def rotate(self, angle, *args, **kwargs):
        super().rotate(angle, about_point=self.main_body.get_center(), *args, **kwargs)
        if not self.label == None:
            self.label.rotate(-angle).next_to(self.main_body, self._direction, buff=0.1)

        return self


class Ground(VMobject):
    def __init__(self, ground_type="ground", label=None, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        if ground_type == "ground":
            self.main_body = VGroup(Polygon([0, 0, 0], [2, 0, 0], [1, -1, 0]))
            if not label is None and label == "D" or label == "A":
                self.main_body.add(Text(label).move_to(self.main_body))
                # 'D' or 'A' for digital vs analog ground
                pass

        elif ground_type == "earth":
            self.main_body = VGroup(
                Line([0, 0, 0], [2, 0, 0]),
                Line([(1 / 3), -(1 / 3), 0], [(5 / 3), -(1 / 3), 0]),
                Line([(2 / 3), -(2 / 3), 0], [(4 / 3), -(2 / 3), 0]),
            )

        # tail for ground:
        self.add(self.main_body)

        # Scale down to match the scale of other electrical mobjects
        self.main_body.set_color(WHITE)
        self.main_body.stroke_opacity = 1

        self.main_body.center().scale(0.25).center()

    def get_terminals(self, *args):
        if len(self.main_body) != 3:
            return self.main_body[0].point_from_proportion(1 / (2 + 2 * np.sqrt(2)))
        else:
            return self.main_body[0].point_from_proportion(0.5)


class Opamp(VMobject):
    def __init__(self, bias_supply=None, label=False, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        self._plots = VGroup()
        self._terminals = {
            "positive_input": None,
            "negative_input": None,
            "positive_bias": None,
            "negative_bias": None,
            "output": None,
        }

        # main body structure
        self.main_body = VGroup(
            Triangle().rotate(-90 * DEGREES).set_color(WHITE),
        )

        # Indications for the input terminals
        self.main_body.add(
            VGroup(
                Line(DOWN * 0.15, UP * 0.15), Line(LEFT * 0.15, RIGHT * 0.15)
            ).next_to(
                self.main_body.get_left() + [0, self.main_body.height / 4, 0],
                RIGHT,
                buff=0.05,
            )
        )
        self.main_body.add(
            Line(LEFT * 0.15, RIGHT * 0.15).next_to(
                self.main_body.get_left() - [0, self.main_body.height / 4, 0],
                RIGHT,
                buff=0.05,
            ),
        )
        self.add(self.main_body)

        # Rails
        self._labels = VGroup()
        self._pos_rail = Line(
            (self.main_body.get_left() + [0, self.main_body.height / 4, 0]),
            (self.main_body.get_left() + [-0.25, self.main_body.height / 4, 0]),
        )

        self._plots.add(
            Dot(
                self.main_body.get_left() + [-0.25, self.main_body.height / 4, 0]
            ).set_opacity(0)
        )
        self._terminals["positive_input"] = self._plots[-1].get_center()

        self._neg_rail = Line(
            (self.main_body.get_left() - [0, self.main_body.height / 4, 0]),
            (self.main_body.get_left() - [0.25, self.main_body.height / 4, 0]),
        )
        self._plots.add(
            Dot(
                self.main_body.get_left() - [0.25, self.main_body.height / 4, 0]
            ).set_opacity(0)
        )
        self._terminals["negative_input"] = self._plots[-1].get_center()

        self._output_rail = Line(
            self.main_body.get_right(), (self.main_body.get_right() + [0.25, 0, 0])
        )
        self._plots.add(Dot(self.main_body.get_right() + [0.25, 0, 0]).set_opacity(0))
        self._terminals["output"] = self._plots[-1].get_center()

        self.rails = VGroup(self._pos_rail, self._neg_rail, self._output_rail)

        if "positive" == bias_supply or "both" == bias_supply:
            self._positive_bias = Line(
                (self.main_body.get_corner(UL) + self.main_body.get_right()) / 2,
                (self.main_body.get_corner(UL) + self.main_body.get_right()) / 2
                + [0, 0.25, 0],
            )
            self.rails.add(self._positive_bias)
            if label is True:
                self._labels.add(
                    MathTex(r"V_{CC}").scale(0.5).next_to(self._positive_bias, RIGHT)
                )

            self._plots.add(
                Dot(
                    (self.main_body.get_corner(UL) + self.main_body.get_right()) / 2
                    + [0, 0.25, 0]
                ).set_opacity(0)
            )
            self._terminals["positive_bias"] = self._plots[-1].get_center()

        if "negative" == bias_supply or "both" == bias_supply:
            self._negative_bias = Line(
                (self.main_body.get_corner(DL) + self.main_body.get_right()) / 2,
                (self.main_body.get_corner(DL) + self.main_body.get_right()) / 2
                + [0, -0.25, 0],
            )
            self.rails.add(self._negative_bias)
            if label is True:
                self._labels.add(
                    MathTex(r"-V_{CC}").scale(0.5).next_to(self._negative_bias, RIGHT)
                )

            self._plots.add(
                Dot(
                    (self.main_body.get_corner(DL) + self.main_body.get_right()) / 2
                    + [0, -0.25, 0]
                ).set_opacity(0)
            )

            self._terminals["negative_bias"] = self._plots[-1].get_center()
        self.add(self.rails, self._labels, self._plots)

    def get_terminals(self, val):
        return self._terminals[val]
