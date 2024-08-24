from manim import *
from manim_circuit import *


class AllPartsAndVariants(Scene):
    def construct(self):
        ground_variants = VGroup(
            Ground(ground_type="ground"),
            Ground(ground_type="ground", label="D"),
            Ground(ground_type="ground", label="A"),
            Ground(ground_type="earth"),
        ).arrange(DOWN, buff=0.75)

        capacitor_variants = VGroup(
            Capacitor(polarized=True, label="x"),
            Capacitor(polarized=True),
            Capacitor(polarized=False, label="x"),
            Capacitor(polarized=False),
        ).arrange(DOWN, buff=0.75)

        resistor_variants = VGroup(Resistor(label="y"), Resistor()).arrange(
            DOWN, buff=0.75
        )
        inductor_variants = VGroup(Inductor(label="z"), Inductor()).arrange(
            DOWN, buff=0.75
        )

        source_variants = VGroup(
            VoltageSource(value="V_1", label=True, direction=LEFT, dependent=False),
            VoltageSource(value="V_2", label=True, direction=LEFT, dependent=True),
            CurrentSource(value="I_1", label=True, direction=LEFT, dependent=False),
            CurrentSource(value="I_2", label=True, direction=LEFT, dependent=True),
        ).arrange(DOWN, buff=0.75)

        Opamp_variants = VGroup(
            Opamp(bias_supply="positive", label=False),
            Opamp(bias_supply="negative", label=False),
            Opamp(bias_supply="both", label=True),
        ).arrange(DOWN, buff=0.75)

        all_electric_parts = VGroup(
            ground_variants,
            capacitor_variants,
            resistor_variants,
            inductor_variants,
            source_variants,
            Opamp_variants,
        ).arrange()

        self.add(all_electric_parts)
