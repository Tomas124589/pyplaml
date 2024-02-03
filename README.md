# PyPLAML

An extension for Manim (https://www.manim.community/) supporting class diagrams. Allows creating various types
of classes (interfaces,
enums, ...) and relations between them, which can be later animated using Manim interface.

There is also a parser for PlantUML (https://plantuml.com/class-diagram), which can automatically create a diagram from
provided .puml file.

## Requirements

- ffmpeg, https://ffmpeg.org/download.html
- graphviz, https://graphviz.org/download
- (Windows only) Microsoft Visual C++ 14.0 or newer

## Installation

Before installation, make sure ffmpeg and graphviz are included in PATH.

Run in package root (where pyproject.toml is):

```
pip install .
```

### Fix for Windows Graphviz "Failed building wheel" error

```
python -m pip install --use-pep517 `
              --config-settings="--global-option=build_ext" `
              --config-settings="--global-option=-IC:\Program Files\Graphviz\include" `
              --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" `
              pygraphviz
```

## Usage

Usage is same as running any other manim scene. To run a scene from examples run:

```commandline
manim examples/scenes/animals.py -pql
```