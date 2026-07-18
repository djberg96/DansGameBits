# Tito restored rulebook

The rulebook is set at 11pt in a two-column, black-and-white layout. Color is
reserved for the 100×100 SVG counter examples in `figures/`.

Build from this directory with:

```sh
pdflatex tito-rulebook.tex
pdflatex tito-rulebook.tex
```

The SVGs are accompanied by PDF renderings because pdfLaTeX embeds those
directly without requiring shell escape. To regenerate the vector examples
after editing their palette or labels:

```sh
python3 tools/make_counters.py
```

The original scans remain in `../../Misc/Images/Tito`. The final scan is used
as the counter-manifest appendix; all rules prose is editable text in
`sections/`.
