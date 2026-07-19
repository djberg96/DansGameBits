#!/usr/bin/env python3
"""Generate clean 100x100 SVG rulebook counter examples.

The geometry follows the existing NATO/Panzergruppe_Guderian SVG family in
this repository.  These are explanatory artwork, not a replacement counter mix.
"""

from pathlib import Path
import subprocess


OUT = Path(__file__).resolve().parents[1] / "figures"


def nato_symbol(kind: str, ink: str = "#17201b") -> str:
    # The lower label was removed after the original counter sheet became
    # available, allowing the NATO symbol and strength to use the full face.
    base = f'<rect x="19" y="32" width="62" height="35" rx="1" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    if kind == "infantry":
        return base + f'<path d="M19 32L81 67M19 67L81 32" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    if kind == "mechanized":
        return (base
                + f'<path d="M19 32L81 67M19 67L81 32" fill="none" stroke="{ink}" stroke-width="2.5"/>'
                + f'<ellipse cx="50" cy="49.5" rx="20" ry="8" fill="none" stroke="{ink}" stroke-width="2.5"/>')
    if kind == "mountain":
        return (base
                + f'<path d="M19 32L81 67M19 67L81 32" fill="none" stroke="{ink}" stroke-width="2.5"/>'
                + f'<path d="M41 63L50 54L59 63Z" fill="none" stroke="{ink}" stroke-width="2.2"/>')
    if kind == "armor":
        return base + f'<rect x="27" y="39" width="46" height="21" rx="10.5" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    if kind == "cavalry":
        return base + f'<path d="M19 67L81 32" fill="none" stroke="{ink}" stroke-width="2.5"/>'
    if kind == "airborne":
        return base + f'<path d="M22 35Q50 63 78 35M50 36V64" fill="none" stroke="{ink}" stroke-width="2.2"/>'
    raise ValueError(kind)


def counter(name: str, *, color: str, designation: str, strength: str,
            size: str = "", kind: str = "infantry",
            ink: str = "#17201b") -> None:
    symbol = nato_symbol(kind, ink)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect x="1" y="1" width="98" height="98" rx="4" fill="{color}" stroke="#17201b" stroke-width="2"/>
  <text x="50" y="17" font-family="Arial,Helvetica,sans-serif" font-size="13" font-weight="700" text-anchor="middle" fill="{ink}">{designation}</text>
  <text x="50" y="29" font-family="Arial,Helvetica,sans-serif" font-size="11" font-weight="700" text-anchor="middle" fill="{ink}">{size}</text>
  {symbol}
  <text x="50" y="91" font-family="Arial,Helvetica,sans-serif" font-size="27" font-weight="700" text-anchor="middle" fill="{ink}">{strength}</text>
</svg>'''
    path = OUT / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(OUT / f"{name}.pdf"), str(path)], check=True)


def marker(name: str, top: str, bottom: str, color: str) -> None:
    top_size = 15 if len(top) >= 7 else 19
    bottom_size = 13 if len(bottom) >= 8 else 18
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect x="1" y="1" width="98" height="98" rx="4" fill="{color}" stroke="#17201b" stroke-width="2"/>
  <text x="50" y="42" font-family="Arial,Helvetica,sans-serif" font-size="{top_size}" font-weight="700" text-anchor="middle" fill="#17201b">{top}</text>
  <text x="50" y="68" font-family="Arial,Helvetica,sans-serif" font-size="{bottom_size}" font-weight="700" text-anchor="middle" fill="#17201b">{bottom}</text>
</svg>'''
    path = OUT / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(OUT / f"{name}.pdf"), str(path)], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Flat approximations of the aged, screened colors in the supplied scan.
    # They deliberately capture hue/value rather than the paper and halftone noise.
    german = "#b9c3c1"     # cool blue-grey
    serbian = "#e88952"    # orange
    italian = "#d8c69f"    # tan
    croat = "#ebc95a"      # yellow
    bulgarian = "#aaa369"  # olive
    soviet = "#d997aa"     # pink
    partisan = "#e34f5f"   # red
    chetnik = "#f4f1e7"    # warm white
    chetnik_ink = "#c9252d" # red printing on the original counters
    marker_color = chetnik
    counter("german-infantry-front", color=german, designation="704", size="XX", strength="12")
    counter("german-infantry-back", color=german, designation="104L", size="XX", strength="15")
    counter("german-panzer", color=german, designation="1 Pz", size="XX", strength="30", kind="armor")
    counter("german-cavalry", color=german, designation="1 Cos", size="XX", strength="9", kind="cavalry")
    counter("german-parachute", color=german, designation="501 SS", size="II", strength="1", kind="airborne")
    counter("partisan-group", color=partisan, designation="30 GROUP", strength="1")
    counter("partisan-brigade", color=partisan, designation="30", size="X", strength="4")
    counter("partisan-infantry", color=partisan, designation="48", size="XX", strength="12")
    counter("german-mechanized-infantry", color=german, designation="4 SS", size="XX", strength="20", kind="mechanized")
    counter("german-mountain-infantry", color=german, designation="1", size="XX", strength="20", kind="mountain")
    counter("serbian-infantry", color=serbian, designation="1", size="X", strength="1")
    counter("italian-infantry", color=italian, designation="PARMA", size="XX", strength="6")
    counter("croat-infantry", color=croat, designation="1 UST", size="X", strength="2")
    counter("bulgarian-infantry", color=bulgarian, designation="14", size="XX", strength="12")
    counter("soviet-infantry", color=soviet, designation="4 GD", size="XXX", strength="42")
    counter("chetnik-group", color=chetnik, designation="1 GROUP", strength="1", ink=chetnik_ink)
    marker("tito-unidentified", "TITO", "NOT IDENT.", partisan)
    marker("tito-identified", "TITO", "IDENTIFIED", partisan)
    marker("victory-points", "VP (+)", "×1", marker_color)
    marker("victory-points-negative", "VP (-)", "×1", marker_color)
    marker("allied-progress", "ALLIED", "PROGRESS", marker_color)
    marker("game-turn", "GAME", "TURN", marker_color)
    marker("drought-turn", "DROUGHT", "TURN", marker_color)
    marker("anti-guerrilla-operations", "8", "AGO", soviet)


if __name__ == "__main__":
    main()
