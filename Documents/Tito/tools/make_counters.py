#!/usr/bin/env python3
"""Generate clean 100x100 SVG rulebook counter examples.

The geometry follows the existing NATO/Panzergruppe_Guderian SVG family in
this repository.  These are explanatory artwork, not a replacement counter mix.
"""

from pathlib import Path
import subprocess


OUT = Path(__file__).resolve().parents[1] / "figures"


def nato_symbol(kind: str) -> str:
    base = '<rect x="22" y="29" width="56" height="31" rx="1" fill="none" stroke="#17201b" stroke-width="2.5"/>'
    if kind == "infantry":
        return base + '<path d="M22 29L78 60M22 60L78 29" fill="none" stroke="#17201b" stroke-width="2.5"/>'
    if kind == "armor":
        return base + '<rect x="29" y="36" width="42" height="17" rx="8.5" fill="none" stroke="#17201b" stroke-width="2.5"/>'
    if kind == "cavalry":
        return base + '<path d="M22 60L78 29" fill="none" stroke="#17201b" stroke-width="2.5"/>'
    if kind == "airborne":
        return base + '<path d="M25 32Q50 58 75 32M50 33V57" fill="none" stroke="#17201b" stroke-width="2.2"/>'
    raise ValueError(kind)


def counter(name: str, *, color: str, designation: str, strength: str,
            size: str = "", kind: str = "infantry", subtitle: str = "") -> None:
    symbol = nato_symbol(kind)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect x="1" y="1" width="98" height="98" rx="4" fill="{color}" stroke="#17201b" stroke-width="2"/>
  <text x="50" y="16" font-family="Arial,Helvetica,sans-serif" font-size="13" font-weight="700" text-anchor="middle" fill="#17201b">{designation}</text>
  <text x="50" y="27" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" text-anchor="middle" fill="#17201b">{size}</text>
  {symbol}
  <text x="50" y="83" font-family="Arial,Helvetica,sans-serif" font-size="23" font-weight="700" text-anchor="middle" fill="#17201b">{strength}</text>
  <text x="50" y="94" font-family="Arial,Helvetica,sans-serif" font-size="7.5" text-anchor="middle" fill="#17201b">{subtitle}</text>
</svg>'''
    path = OUT / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(OUT / f"{name}.pdf"), str(path)], check=True)


def marker(name: str, top: str, bottom: str, color: str) -> None:
    top_size = 15 if len(top) > 7 else 19
    bottom_size = 13 if len(bottom) > 9 else 18
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
    german = "#b8b8b8"
    serbian = "#e6a14a"
    italian = "#d6c096"
    croat = "#efd65b"
    bulgarian = "#999957"
    soviet = "#e4a2b8"
    partisan = "#c95656"
    chetnik = "#fafaf7"
    marker_color = "#e7dfc8"
    counter("german-infantry-front", color=german, designation="704", size="XX", strength="12", subtitle="INFANTRY")
    counter("german-infantry-back", color=german, designation="104L", size="XX", strength="15", subtitle="INFANTRY")
    counter("german-panzer", color=german, designation="1 Pz", size="XX", strength="30", kind="armor", subtitle="PANZER")
    counter("german-cavalry", color=german, designation="1 Cos", size="XX", strength="9", kind="cavalry", subtitle="CAVALRY")
    counter("german-parachute", color=german, designation="501 SS", size="II", strength="1", kind="airborne", subtitle="PARACHUTE")
    counter("partisan-group", color=partisan, designation="30 GROUP", strength="1", subtitle="PARTISAN GROUP")
    counter("partisan-brigade", color=partisan, designation="30", size="X", strength="4", subtitle="PARTISAN BRIGADE")
    counter("serbian-infantry", color=serbian, designation="1", size="X", strength="1", subtitle="SERBIAN")
    counter("italian-infantry", color=italian, designation="PARMA", size="XX", strength="6", subtitle="ITALIAN")
    counter("croat-infantry", color=croat, designation="1 UST", size="X", strength="2", subtitle="CROAT")
    counter("bulgarian-infantry", color=bulgarian, designation="14", size="XX", strength="12", subtitle="BULGARIAN")
    counter("soviet-infantry", color=soviet, designation="4 GD", size="XXX", strength="42", subtitle="SOVIET")
    counter("chetnik-group", color=chetnik, designation="1 GROUP", strength="1", subtitle="CHETNIK GROUP")
    marker("tito-unidentified", "TITO", "NOT IDENT.", partisan)
    marker("tito-identified", "TITO", "IDENTIFIED", partisan)
    marker("victory-points", "VP (+)", "×1", marker_color)
    marker("allied-progress", "ALLIED", "PROGRESS", marker_color)
    marker("game-turn", "GAME", "TURN", marker_color)
    marker("drought-turn", "DROUGHT", "TURN", marker_color)


if __name__ == "__main__":
    main()
