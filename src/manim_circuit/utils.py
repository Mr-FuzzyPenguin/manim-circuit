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


class Circuit(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Get a VGroup() of components
        self.component_list = VGroup()

        # Effectively, the node_list contains all Node types
        self.node_list = VGroup()

        self.add(self.component_list)

        # Add node_list VGroup() of nodes (with wires)
        # Add Dot() for junctions
        self.add(self.node_list)

    # This function returns the endpoints of the wire.
    def __create_wire(self, end1, end2, diagonal=False, invert=False):
        # Check if a turn is necessary. Only satisfiable if:
        # 1. diagonal flag is not set/overriden to True
        # 2. end1.x != end2.x and end1.y != end2.y
        if (
            not math.isclose(end1[0], end2[0]) and not math.isclose(end1[1], end2[1])
        ) and diagonal is not True:
            # Define the turn
            if invert is True:
                turn = [end2[0], end1[1], 0]
            else:
                turn = [end1[0], end2[1], 0]
            return [end1, turn, end2]

        # This is diagonal, OR it is a straight line
        else:
            return [end1, end2]

    def add_components(self, *args):
        for component in args:
            self.component_list.add(component)

    def add_wire(
        self,
        end1,
        end2,
        diagonal=False,
        invert=False,
    ):
        wire = self.__create_wire(end1, end2, diagonal, invert)

        # First wire
        if len(self.node_list) == 0:
            # Create the first node
            node = Node()
            node.add_wire(wire)

            # Adding the newly editted node
            self.node_list.add(node)

            return wire
        # Not first wire.
        # Loop through all nodes and wires through each node
        else:
            intersections = []
            # Iterate through all nodes.
            for node in self.node_list:
                # search if a coordinate of the wire belong in the node.
                # If so, add to node intersections
                # search is a list that returns either True or coordinate or False
                # It is important because we can then add Dots() from this list.
                search = list(map(node.check_coord, wire))
                if not all([type(s) == bool and s == False for s in search]):
                    intersections.append(node)

                    # Go through the search
                    # If there is a coordinate, tell the node to add a junction there.
                    for dot in search:
                        if not type(dot) == bool:
                            node.add_dot(dot)


            # This means that the wire is not attached to any node,
            # Make a new node.
            if len(intersections) == 0:
                node = Node()
                node.add_wire(wire)
                node.set_color(WHITE)
                self.node_list.add(node)

            elif len(intersections) == 1:
                intersections[0].add_wire(wire)

            elif len(intersections) == 2:
                intersections[0].merge(intersections[1], wire)
                self.node_list.remove(intersections[1])

            elif len(intersections) == 3:
                intersections[0].merge(intersections[1], wire)
                intersections[0].merge(intersections[2])
                self.node_list.remove(intersections[1])
                self.node_list.remove(intersections[2])


class Node(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # NOTE In a future update, I want to try to
        # have designated calculated "voltages"
        # relative to ground using sympy or some python and spice
        # library. Something like pyspice or ngspice...
        # self.known_voltage = None
        # Voltage functionality has not been added in v2 yet.
        self.voltage = None

        self.coords = []
        self.junction_dots = VGroup()

        self.add(self.junction_dots)

        self.set_color(WHITE)

    def __update(self):
        self.clear_points()
        for path in self.coords:
            self.start_new_path(path[0])
            for coord in path[1:]:
                self.add_line_to(np.array(coord))

    def check_coord(self, coord):
        # coord is to be checked.
        # return a non-False value if:
        # 1. It paired coordinates in self.coords (and not endpoint)
        #       return True
        # 2. It is validated by line_intersection "proof"
        #       return the coordinate
        for wire in self.coords:
            # new wire is connected to an end of a wire.
            if np.allclose(coord, wire[0]) or np.allclose(coord, wire[-1]):
                return True

            # reading the endpoints of wire
            for i in range(len(wire) - 1):
                coord_is_in_between_a_line = validate_forms_approx_line(
                    coord, [wire[i], wire[i + 1]]
                )
                # Coord matches a coordinate that is in the middle.
                if (
                    np.allclose(coord, wire[i]) and i != 0
                ) or coord_is_in_between_a_line:
                    return coord

        return False

    def add_dot(self, dot_coord):
        self.junction_dots.add(Dot(dot_coord))

    # wire is just a matrix with dimensions 2n x 3 or 3 x 3
    # depending entirely on if it is a diagonal wire or not
    def add_wire(self, wire_param):
        if len(self.coords) == 0:
            self.coords.append(wire_param)
            self.__update()
            return

        # Check if continuity in any wire (assume False)
        cont = False
        # wire is a single path of arbitrary length. It's a dot chain.
        for wire, i in zip(self.coords, range(len(self.coords))):
            if np.allclose(wire[0], wire_param[0]):
                self.coords[i] = wire_param[1:][::-1] + wire
                cont = True
                break

            elif np.allclose(wire[0], wire_param[-1]):
                self.coords[i] = wire_param[:-1] + wire
                cont = True
                break

            elif np.allclose(wire[-1], wire_param[0]):
                self.coords[i] = wire + wire_param[1:]
                cont = True
                break

            elif np.allclose(wire[-1], wire_param[-1]):
                self.coords[i] = wire + wire_param[:-1][::-1]
                cont = True
                break

        # Aggregated data
        if cont is not True:
            self.coords.append(wire_param)

        self.__update()

    def merge(self, node, wire=False):
        if wire is not False:
            self.add_wire(wire)

        # Get all the junction dots.
        for dot in node.junction_dots:
            self.junction_dots.add(dot)

        self.coords = self.coords + node.coords
        node.clear_points()
        self.__update()


def distance(a, b):
    return np.sqrt(np.sum([i * i for i in np.array(a) - np.array(b)]))


def validate_forms_approx_line(coord, line, tolerance=1e-5):
    # Check if the sum of the distance(s) between a coordinate to the end(s) of a line
    # equates to the distance of the line
    return math.isclose(
        distance(coord, line[0]) + distance(coord, line[1]),
        distance(*line),
        rel_tol=tolerance,
    )
