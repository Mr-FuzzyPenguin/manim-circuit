from manim import *
import math


class Source(VMobject):
    def __init__(
        self,
        mobject_group,
        letter,
        value,
        direction=LEFT,
        label=True,
        dependent=True,
        **kwargs,
    ):
        # initialize the vmobject
        super().__init__(**kwargs)
        self._direction = direction

        # If value is a number or override dependent is False
        if dependent is False or type(value) is int or type(value) is float:
            self.main_body = Circle().set_stroke(WHITE)
        else:
            self.main_body = (
                Square().set_stroke(WHITE).rotate(45 * DEGREES).scale(1 / np.sqrt(2))
            )

        # Add the scaled symbols first
        self.add(mobject_group.scale(0.5, about_point=self.main_body.get_center()))

        # Scale it down first and then add it onto the VMobject
        self.add(self.main_body.scale(0.5))

        if label:
            self.label = (
                MathTex(str(value) + r"\text{ " + letter + "}")
                .scale(0.5)
                .next_to(self.main_body, self._direction, buff=0.1)
            )
            self.add(self.label)
        else:
            self.label = None

    def get_terminals(self, val):
        if type(self.main_body) is Circle:
            proportion_offset = 0
        else:
            proportion_offset = -0.25

        if val == "positive":
            return self.main_body[0].point_from_proportion(0.25 + proportion_offset)
        elif val == "negative":
            return self.main_body[0].point_from_proportion(0.75 + proportion_offset)

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


def distance(a, b):
    return np.sqrt(np.sum([i * i for i in np.array(a) - np.array(b)]))


def validate_line_intersection(l1, l2):
    tolerance = 1e-5
    if math.isclose(
        distance(l2[0], l1[0]) + distance(l2[0], l1[1]),
        distance(*l1),
        rel_tol=tolerance,
    ) or math.isclose(
        distance(l2[1], l1[0]) + distance(l2[1], l1[1]),
        distance(*l1),
        rel_tol=tolerance,
    ):
        try:
            return line_intersection(l1, l2)
        except:
            return False
    else:
        return False


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
                    intersect = validate_line_intersection(
                        wire.get_anchors(),
                        [end1, end2],
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
