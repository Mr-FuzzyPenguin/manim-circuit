from manim import *
from manim_circuit import *


class SampleCircuit(Scene):
    def construct(self):
        # It is helpful to use a Numberplane() to help move the parts and place them appropriately.
        n = NumberPlane().set_opacity(0.5)
        self.add(n)

        # Place the components down first. Then, connect with wires later.
        r1 = Resistor(270).shift(LEFT * 3.25 + UP)
        r2 = (
            Resistor("10k", direction=RIGHT)
            .rotate(90 * DEGREES)
            .shift(LEFT * 1.75 + DOWN * 0.5)
        )
        r3 = Resistor("1.1k", direction=DOWN).shift(DOWN * 2 + LEFT * 0.25)
        r4 = (
            Resistor(620, direction=RIGHT)
            .rotate(90 * DEGREES)
            .shift(RIGHT * 1.25 + DOWN * 0.5)
        )
        r5 = Resistor(430).shift(RIGHT * 2.75 + UP)
        r6 = (
            Resistor(360, direction=LEFT)
            .shift(RIGHT * 6 + DOWN * 0.5)
            .rotate(90 * DEGREES)
        )
        r7 = Resistor("5.6k").shift(UP * 3)
        v1 = VoltageSource(20).shift(LEFT * 5 + DOWN * 0.5)

        # You can rotate the voltage sources and move them.
        v2 = VoltageSource(10, direction=UP).rotate(-90 * DEGREES).shift(UP)
        v3 = VoltageSource(16, direction=LEFT).shift(RIGHT * 4 + DOWN * 0.5)
        gnd = Ground(ground_type="ground").shift(LEFT * 5 + DOWN * 3)

        # Add Circuit components.
        circuit = Circuit()
        self.add(circuit)
        circuit.add_components(v1, v2, v3, r1, r2, r3, r4, r5, r6, r7, gnd)

        # Add wires (it can get a bit tedious sometimes!)
        circuit.add_wire(gnd.get_terminals(), v1.get_terminals("negative"))
        circuit.add_wire(
            r3.get_terminals("left"),
            [gnd.get_terminals()[0], r3.get_terminals("left")[1], 0],
        )
        circuit.add_wire(
            r2.get_terminals("left"),
            [r2.get_terminals("left")[0], r3.get_terminals("left")[1], 0],
        )

        circuit.add_wire(
            v1.get_terminals("positive"),
            [v1.get_terminals("positive")[0], r7.get_terminals("left")[1], 0],
        )
        circuit.add_wire(
            r7.get_terminals("left"),
            [v1.get_terminals("positive")[0], r7.get_terminals("left")[1], 0],
            junctions=False,
        )
        circuit.add_wire(
            r1.get_terminals("left"),
            [v1.get_terminals("positive")[0], r1.get_terminals("left")[1], 0],
        )
        circuit.add_wire(r1.get_terminals("right"), v2.get_terminals("negative"))
        circuit.add_wire(
            r2.get_terminals("right"),
            [r2.get_terminals("right")[0], v2.get_terminals("negative")[1], 0],
        )
        circuit.add_wire(r5.get_terminals("left"), v2.get_terminals("positive"))
        circuit.add_wire(
            r4.get_terminals("right"),
            [r4.get_terminals("right")[0], v2.get_terminals("positive")[1], 0],
        )
        circuit.add_wire(
            r4.get_terminals("left"),
            [r4.get_terminals("left")[0], r3.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            v3.get_terminals("negative"),
            [v3.get_terminals("negative")[0], r3.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            r3.get_terminals("right"),
            [r4.get_terminals("left")[0], r3.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            [r4.get_terminals("left")[0], r3.get_terminals("right")[1], 0],
            [v3.get_terminals("negative")[0], r3.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            [v3.get_terminals("negative")[0], r3.get_terminals("right")[1], 0],
            [r6.get_terminals("left")[0], r3.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            r6.get_terminals("left"),
            [r6.get_terminals("left")[0], r3.get_terminals("right")[1], 0],
            junctions=False,
        )
        circuit.add_wire(
            r7.get_terminals("right"),
            [r6.get_terminals("right")[0], r7.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            r6.get_terminals("right"),
            [r6.get_terminals("right")[0], r7.get_terminals("right")[1], 0],
            junctions=False,
        )
        circuit.add_wire(
            r5.get_terminals("right"),
            [r6.get_terminals("right")[0], r5.get_terminals("right")[1], 0],
        )
        circuit.add_wire(
            v3.get_terminals("positive"),
            [v3.get_terminals("positive")[0], r5.get_terminals("right")[1], 0],
        )

        self.wait()
        for node, color in zip(
            circuit.node_list, [BLUE, RED, ORANGE, YELLOW, GREEN, PURPLE]
        ):
            self.play(node.animate.set_color(color))
        self.wait()
