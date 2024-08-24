from manim import *


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

        self.main_body = (
            # TODO This parametric function, although stolen directly from Desmos is
            # unfortunately formatted badly. Considering using something else besides
            # ParametricFunction(s) to make Resistors.
            ParametricFunction(
                (
                    lambda t: (
                        t,
                        (
                            2
                            * np.arcsin(
                                np.sin(
                                    (25.7244 * PI * t + 11.64 * PI) / 21.88
                                    + (13.26 * PI) / 21.88
                                )
                            )
                            / PI
                        ),
                        0,
                    )
                ),
                t_range=(-4.15 / (2.21 * 1.94), 17.73 / 4.2874),
            )
            .scale(0.25)
            .center()
        )

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


class VoltageSource(VMobject):
    def __init__(self, value=1, label=True, direction=LEFT, dependent=False, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        if dependent is True or type(value) is int or type(value) is float:
            self.main_body = VGroup(
                Circle().set_stroke(WHITE),
            )
        else:
            self.main_body = VGroup(
                Square().set_stroke(WHITE).rotate(45 * DEGREES).scale(1 / np.sqrt(2))
            )

        # + and -
        self.main_body.add(Line(DOWN * 0.3, UP * 0.3).shift(UP * 0.5))
        self.main_body.add(Line(LEFT * 0.3, RIGHT * 0.3).shift(UP * 0.5))
        self.main_body.add(Line(LEFT * 0.3, RIGHT * 0.3).shift(DOWN * 0.5))

        self.main_body.scale(0.5)

        self.add(self.main_body)

        if label:
            self.label = (
                MathTex(str(value) + r"\text{ V}")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)
        else:
            self.label = None

    def get_terminals(self, val):
        if val == "positive":
            return self.main_body[0].point_from_proportion(0.25)
        elif val == "negative":
            return self.main_body[0].point_from_proportion(0.75)

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


class CurrentSource(VMobject):
    def __init__(self, value=1, label=True, direction=LEFT, dependent=False, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        if dependent is True or type(value) is int or type(value) is float:
            self.main_body = VGroup(
                Circle().set_stroke(WHITE),
            )
        else:
            self.main_body = VGroup(
                Square().set_stroke(WHITE).rotate(45 * DEGREES).scale(1 / np.sqrt(2))
            )

        self.main_body.add(Line(DOWN * 0.75, UP * 0.75).add_tip(tip_shape=StealthTip))

        self.main_body.scale(0.5)

        self.add(self.main_body)

        if label:
            self.label = (
                MathTex(str(value) + r"\text{ A}")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)

    def get_terminals(self, val):
        if val == "positive":
            return self.main_body[0].point_from_proportion(0.25)
        elif val == "negative":
            return self.main_body[0].point_from_proportion(0.75)

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


class Circuit(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Get a VGroup() of components
        self.component_list = VGroup()

        # Effectively, the node_list contains all Node types
        self.node_list = VGroup()

        self.add(self.component_list)

        # Add node_list VGroup() of nodes (with wires)
        self.add(self.node_list)
        # Add Dot() for junctions

    def add_components(self, *args):
        for component in args:
            self.component_list.add(component)

    # line_intersection annoyingly (but true to its name),
    # will get the intersection between two lines. NOT segments
    # which is unfortunate, considering that's what "wires" are.
    def validate_line_intersection(self, l1, l2):
        try:
            preliminary_result = line_intersection(l1, l2)
        except:
            return False

        x_range1 = [l1[0][0], l1[1][0]]
        x_range1.sort()
        y_range1 = [l1[0][1], l1[1][1]]
        y_range1.sort()

        x_range2 = [l2[0][0], l2[1][0]]
        x_range2.sort()
        y_range2 = [l2[0][1], l2[1][1]]
        y_range2.sort()

        # TODO In the future, ideally a different implementation that's
        # a bit more mathematical, (and less brute-force) will be used
        if (
            (
                (
                    x_range1[1] > preliminary_result[0]
                    or np.allclose([preliminary_result[0]], [x_range1[1]])
                )
                and (
                    preliminary_result[0] > x_range1[0]
                    or np.allclose([preliminary_result[0]], [x_range1[0]])
                )
            )
            and (
                (
                    x_range2[1] > preliminary_result[0]
                    or np.allclose([preliminary_result[0]], [x_range2[1]])
                )
                and (
                    preliminary_result[0] > x_range2[0]
                    or np.allclose([preliminary_result[0]], [x_range2[0]])
                )
            )
            and (
                (
                    y_range1[1] > preliminary_result[1]
                    or np.allclose([preliminary_result[1]], [y_range1[1]])
                )
                and (
                    preliminary_result[1] > y_range1[0]
                    or np.allclose([preliminary_result[1]], [y_range1[0]])
                )
            )
            and (
                (
                    y_range2[1] > preliminary_result[1]
                    or np.allclose([y_range2[1]], [preliminary_result[1]])
                )
                and (
                    preliminary_result[1] > y_range2[0]
                    or np.allclose([preliminary_result[1]], [y_range2[0]])
                )
            )
            # Check if the intersection lies on one of the ends
            and (
                np.allclose(l1[0], preliminary_result)
                or np.allclose(l1[1], preliminary_result)
                or np.allclose(l2[0], preliminary_result)
                or np.allclose(l2[1], preliminary_result)
            )
        ):
            return preliminary_result
        else:
            return False

    def add_wire(self, end1, end2, junctions=True):
        # First wire
        if len(self.node_list) == 0:
            newNode = Node()
            newWire = Wire(end1, end2)
            newNode.add_wire_to_node(newWire)
            self.node_list.add(newNode)
            return
        # Not first wire.
        # Loop through all nodes and wires through each node
        else:
            intersections = []
            wires = []
            node_attachments = []

            # NOTE type(node) == Node
            for node in self.node_list:
                # NOTE type(wire) == VMobject
                for wire in node.line_wires:
                    intersect = self.validate_line_intersection(
                        [end1, end2], wire.get_anchors()
                    )

                    # Found intersection.
                    if not intersect is False:
                        wires.append(wire)
                        intersections.append(intersect)
                        node_attachments.append(node)

            # No intersections means new node.
            if len(intersections) == 0:
                newNode = Node()
                newWire = Wire(end1, end2)

                # the add_wire method will automatically let the Wire object
                # know what its root is (which is just gonna be the Node itself)
                newNode.add_wire_to_node(newWire)

                self.node_list.add(newNode)

            # Seems to intersect at one wire
            # just add this new wire onto the Wire() root.
            elif len(intersections) == 1:
                newWire = Wire(end1, end2)
                node_attachments[0].add_wire_to_node(newWire)

                if junctions is True:
                    node_attachments[0].add_junction(intersections[0])

            elif len(intersections) == 2:
                # Merge downwards from 1 to 0
                # Collect everything from node 1, and put it into node 0
                for wire in node_attachments[1].line_wires:
                    node_attachments[0].line_wires.add(wire)
                for dot in node_attachments[1].dot_junctions:
                    node_attachments[0].dot_junctions.add(dot)

                # Add new wire onto node
                newWire = Wire(end1, end2)
                node_attachments[0].add_wire_to_node(newWire)
                if junctions is True:
                    node_attachments[0].add_junction(intersections[0])
                    node_attachments[0].add_junction(intersections[1])

                # Remove it from the self.node_list to avoid "ghost" nodes.
                for node, i in zip(self.node_list, range(len(self.node_list))):
                    if node == node_attachments[1]:
                        self.node_list.remove(node)
                        break

                # Finally, delete node 1
                del node_attachments[1]


class Wire(VMobject):
    def __init__(self, end1, end2, **kwargs):
        super().__init__(**kwargs)

        # Consider using a different approach than using Lines.
        self.wire = Line(end1, end2)
        self.add(self.wire)
        self.node_root = None

    def get_anchors(self):
        return self.wire.get_anchors()


class Node(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # add Wire().wire (or VMobject: Line())
        # into self.line_wires
        self.line_wires = VGroup()
        self.dot_junctions = VGroup()

        # NOTE In a future update, I want to try to
        # have designated calculated "voltages"
        # relative to ground using sympy or some python and spice
        # library. Something like pyspice or ngspice...
        # self.known_voltage = None

        self.add(self.line_wires)
        self.add(self.dot_junctions)

    def add_wire_to_node(self, wire):
        self.line_wires.add(wire.wire)
        wire.root = self

    def add_junction(self, coordinate):
        self.dot_junctions.add(Dot(coordinate))