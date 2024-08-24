# Manim-Circuit Plugin
## Description
A manim-plugin that adds customized `Mobject` and `VMobject`(s) to create some electrical components. Some electrical components include: Resistors, Inductors, and Capacitors.

## Ok... But WHY?
Manim is an animation library for mathematics. So... what am I doing over here, making some basic circuit elements in the form of customized `Mobjects`? Well, as it turns out, much of circuit analysis has some pretty cool mathematics behind it, and so I wished that there was a library that could give me those customized `Mobjects`. I am making this library alongside the production of my [Practical Engineering series on YouTube](https://www.youtube.com/playlist?list=PLxAacf1hM524ZExrv4PxZPQFUXTQ9Wn1Y).

*"airight man, but you do know that other libraries exist, you know... `CircuiTikz` via LaTex, `circuitanimlib` for ManimGL just to name a few... Stop insisting on re-inventing the wheel".*

Alright, let's talk about `CircuiTikz`. I am fully aware that this wonderful LaTex package exists. You can choose to use CircuitTikz to render the circuit, but you cannot select components of that `Tex` Mobject like you would when using this manim-plugin. Also, I saw a few bugs on forums relating manim and `CircuitTikz` together, on other GitHub repositories.`CircuitTikz` is great at making PDFs, drawing circuit diagrams in papers, but it just simply does not fit nicely with Manim.

And for `circuitanimlib`, the library seemed promising, until I realized its latest commit renders it broken, and its unmaintained. Also, it uses ManimGL which, although faster, has limited documentation on it.

This library is written for ManimCE, not ManimGL. Additionally, there are more resrouces for ManimCE as opposed to ManimGL. Additionally still, ManimCE even has a nice plugin repository and active community plugins. I'd like to make a contribution onto it!

### Inspiration
[Why I made this library](STORY.md)
## Roadmap
- [X] Make this my first open-source package that I, FuzzyPenguin (online alias: Pete Aptenodyte Forsteri) will maintain.
- [ ] Release this to Pypi
- [X] Make this a manim-plugin named manim-circuit
- [ ] Add all of the circuit elements that were used in our class
- [ ] Use this library for AT LEAST one of my future videos whatever it may be\*
- [ ] Clean up the Code
- [X] Maybe make a Circuit `Mobject` in order to help with circuit analysis
- [ ] If I have time, make logic gates too


\*Most likely Circuit Analysis using Laplace Transform for a pure Manim-based animation video
## Documentation

Please note, this is a WIP: More things will be added as Development continues.
`Resistor()`, `Inductor()`, `Capacitor()`, supports labels. For example:
`Inductor(label="0.3", direction=UP)` will make a 0.3 H inductor with a label on the top.

All customized Mobjects will have a `.get_terminals(self, val)` method where passing something in `val` will return the coordinate of a pin of any circuit Element.

Examples in [examples/](examples/)
## License

[MIT](https://choosealicense.com/licenses/mit/)

