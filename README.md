# Manim-Circuit Plugin
## Description
A manim-plugin that adds customized `Mobject` and `VMobject`(s) to create some electrical components. Some electrical components include: Resistors, Inductors, and Capacitors.

## Ok... But WHY?
Manim is an animation library for mathematics. So... what am I doing over here, making some basic circuit elements in the form of customized `Mobjects`? Well, as it turns out, much of circuit analysis has some pretty cool mathematics behind it, and so I wished that there was a library that could give me those customized `Mobjects`. I am making this library alongside the production of my [Practical Engineering series on YouTube](https://www.youtube.com/playlist?list=PLxAacf1hM524ZExrv4PxZPQFUXTQ9Wn1Y).

*"airight man, but you do know that other libraries exist, you know... `CircuiTikz` via LaTex, `circuitanimlib` for ManimGL just to name a few... Stop insisting on re-inventing the wheel".*

Alright, let's talk about `CircuiTikz`. I am fully aware that this wonderful LaTex package exists. Unfortunately, because it is created via LaTex compilation, it is a tad bit slower as it needs to compile the LaTex into `.dvi` and then to `.svg` as opposed to making the circuit elements (such as Resistors, Inductors, etc.) out of basic `Mobjects` using shapes, `Lines`, `ParametricFunctions` etc. Secondly, because it is written by making custom `Mobject` classes, you will have an easier time referencing them, as opposed to `TexMobjects` which have a bit stranger behavior. Also, I saw a ton of bugs on forums, other GitHub repositories, and complaints about `CircuitTikz`. Wonderful software for PDFs, making circuit diagrams in writeups, but it just simply does not fit my use case.

And for `circuitanimlib`, this was the most promising library, especially since I started using ManimGL. However, sadly it seems like the repository is unmaintained, and it also seems like the library (at the time of writing) has a few errors. It looks like the developer of the library tried to merge the repository and failed, leaving a bunch of files with git messages. Unfortunately, that does mean I have to debug the library's messy source code... No thanks. Additionally, installing ManimGL was a bit sketchy, the instructions didn't even work, so I had to make a few workarounds. Therefore, I cannot guarantee that I installed it correctly. With that, although there is a nice speed boost with ManimGL, I still value the developer experience more than rendering speed.

One more thing: This library is written for ManimCE, not ManimGL. I found that there is more up-to-date documentation on ManimCE anyways, as opposed to ManimGL, so that's why I wanted to make this. And for bonus points, ManimCE even has a nice plugin repository and supporting community plugins, and I'd like to add on to it!

## Insipiration
This whole project, repository, and practical engineering series would not have been created if it were not for Professor Harban S. Dhadwal from SBU. Circuit Analysis class was an UNREASONABLY DIFFICULT class, and I wanted to make any future students that will be studying the class feel LESS INTIMIDATED and maybe even EXCITED to study electrical engineering.

### A short anecdote:
I ended up getting a really bad grade in the course: (C), and thus the class dealt a massive blow to my GPA. Regardless, during the summer, right after the end of the semester, I decided to sit down and re-learn everything that I should have learned in that class that I had unfortunately missed or failed to understand. I must also say, that I most definitely unfairly criticized my professor because I found him unfair and maybe even a little bit mean, due to the way he taught. However, after making my practical engineering series and even starting to develop this library, I have a newfound respect for him, as I recognize that understanding, and even TEACHING such a daunting subject as Electrical Engineering is no easy feat. Are there things that I would have changed in the class to help effectively teach more students? Absolutely. Am I saying that I could have done better? Absolutely not. He did his best, even if it wasn't great. This practical engineering series, is merely a potentially botched attempt at teaching such a difficult topic. Will I succeed in teaching students with my videos, library, or other creations? Or will all of this fail, crash, and burn? Only time will tell.

## Roadmap
- [ ] Make this my first open-source package that I, FuzzyPenguin (online alias: Pete Aptenodyte Forsteri) will maintain.
- [ ] Release this to Pypi
- [ ] Make this a manim-plugin named manim-circuit
- [ ] Add all of the circuit elements that were used in our class
- [ ] Use this library for AT LEAST one of my future videos, whatever/whenever it may be\*
- [ ] Clean up the Code
- [ ] Maybe make a Circuit `Mobject` in order to help with circuit analysis
- [ ] If I have time, make logic gates too


\*Most likely Circuit Analysis using Laplace Transform for a pure Manim-based Animation Video
## Documentation

Please note, this is a WIP: More things will be added as development continues.
`Resistor()`, `Inductor()`, `Capacitor()`, support labels. For example:
`Inductor(label="0.3", direction=UP)` will make a 0.3 H inductor with a label on the top.

All customized Mobjects will have a `.get_terminals()` method to return all terminal points in a `dict`. Rotating and moving the customized `Mobject` will still give you the updated new coordinates of the terminals. This includes `Ground()` and `Opamp()`
## License

[MIT](https://choosealicense.com/licenses/mit/)