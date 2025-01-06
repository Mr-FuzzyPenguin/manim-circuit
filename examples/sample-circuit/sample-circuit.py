from manim import *
from manim_circuit import *


class SampleCircuit(Scene):
    def construct(self):
        # It is helpful to use a Numberplane() to help move the parts and place them appropriately.
        n = NumberPlane().set_opacity(0.5)
        self.add(n)

        # Place the components down first. Then, connect with wires later.
        r270 = Resistor(270).shift(LEFT * 3.25 + UP)
        r10000 = (
            Resistor("10k", direction=RIGHT)
            .rotate(90 * DEGREES)
            .shift(LEFT * 1.75 + DOWN * 0.5)
        )
        r1100 = Resistor("1.1k", direction=DOWN).shift(DOWN * 2 + LEFT * 0.25)
        r620 = (
            Resistor(620, direction=RIGHT)
            .rotate(90 * DEGREES)
            .shift(RIGHT * 1.25 + DOWN * 0.5)
        )
        r430 = Resistor(430).shift(RIGHT * 2.75 + UP)
        r360 = (
            Resistor(360, direction=LEFT)
            .shift(RIGHT * 6 + DOWN * 0.5)
            .rotate(90 * DEGREES)
        )
        r5600 = Resistor("5.6k").shift(UP * 3)
        v20 = VoltageSource(20).shift(LEFT * 5 + DOWN * 0.5)

        # You can rotate the voltage sources and move them.
        v10 = VoltageSource(10, direction=UP).rotate(-90 * DEGREES).shift(UP)
        v16 = VoltageSource(16, direction=LEFT).shift(RIGHT * 4 + DOWN * 0.5)
        gnd = Ground(ground_type="ground").shift(LEFT * 5 + DOWN * 3)

        # Add Circuit components.
        circuit = Circuit()
        circuit.add_components(v20, v16, v10, r270, r10000, r1100, r620, r430, r360, r5600, gnd)

        # A much streamline and easier way to edit.
        circuit.add_wire(gnd.get_terminals(), v20.get_terminals("negative"))
        circuit.add_wire(v20.get_terminals("negative"), r1100.get_terminals("left"))
        circuit.add_wire(r10000.get_terminals("left"), r1100.get_terminals("left"))
        circuit.add_wire(v20.get_terminals("positive"), r5600.get_terminals("left"))
        circuit.add_wire(v20.get_terminals("positive"), r270.get_terminals("left"))
        circuit.add_wire(r10000.get_terminals("right"), r270.get_terminals("right"))
        circuit.add_wire(r10000.get_terminals("right"), v10.get_terminals("negative"))
        circuit.add_wire(r620.get_terminals("right"), v10.get_terminals("positive"))

        # you can invert the direction of the wire. Vertical first, or horizontal first.
        circuit.add_wire(r430.get_terminals("left"), r620.get_terminals("right"), invert=True)
        circuit.add_wire(r1100.get_terminals("right"),r360.get_terminals("left"), invert=True)
        circuit.add_wire(v16.get_terminals("negative"),r1100.get_terminals("right"))

        # You can also custom define wires to have better control with how the junctions are generated
        circuit.add_wire(r620.get_terminals("left"), r620.get_terminals("left") + DOWN*(r620.get_terminals("left")[1] - r1100.get_terminals("right")), invert=True)

        # The order in which the wires are added matters.
        circuit.add_wire(r5600.get_terminals("right"), r360.get_terminals("right"), invert=True)
        circuit.add_wire(r430.get_terminals("right"), r360.get_terminals("right"), invert=True)
        circuit.add_wire(v16.get_terminals("positive"), r430.get_terminals("right"))

        self.add(circuit)
        self.wait()

        # Automatic node detection
        for node, color in zip(
            circuit.node_list, [BLUE, RED, ORANGE, YELLOW, GREEN, PURPLE]
        ):
            self.play(node.animate.set_color(color))
        self.wait()
