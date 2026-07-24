#!/usr/bin/env python3
"""Generate annotated map excerpts for the Tito five-turn playbook.

The excerpts deliberately use numbered callouts rather than trying to reproduce
every stack on the map.  The corresponding playbook text supplies the exact
unit counts and die rolls.
"""

from pathlib import Path
import base64
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1] / "figures"
MAP_PATH = ROOT / "Misc/Images/Tito/tito_map.jpg"


def map_data_uri() -> str:
    encoded = base64.b64encode(MAP_PATH.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def badge(number: int, x: int, y: int, label: str = "") -> str:
    label_svg = ""
    if label:
        label_svg = (
            f'<rect x="{x + 22}" y="{y - 17}" width="{max(95, len(label) * 7)}" '
            f'height="30" rx="5" fill="#f7f5ee" fill-opacity=".94" '
            f'stroke="#17201b" stroke-width="2"/>'
            f'<text x="{x + 31}" y="{y + 4}" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="17" font-weight="700" fill="#17201b">{label}</text>'
        )
    return (
        f'<circle cx="{x}" cy="{y}" r="20" fill="#b72831" '
        f'stroke="#f7f5ee" stroke-width="5"/>'
        f'<text x="{x}" y="{y + 7}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="22" font-weight="700" text-anchor="middle" '
        f'fill="#ffffff">{number}</text>{label_svg}'
    )


def arrow(x1: int, y1: int, x2: int, y2: int, *, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="14 10"' if dashed else ""
    return (
        f'<path d="M{x1} {y1} C{(x1 + x2) // 2} {y1}, '
        f'{(x1 + x2) // 2} {y2}, {x2} {y2}" fill="none" '
        f'stroke="#b72831" stroke-width="8" stroke-linecap="round" '
        f'marker-end="url(#arrow)"{dash}/>'
    )


def write_map(name: str, title: str, viewbox: tuple[int, int, int, int],
              overlays: list[str]) -> None:
    x, y, width, height = viewbox
    map_href = map_data_uri()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    width="{width}" height="{height}" viewBox="{x} {y} {width} {height}">
  <defs>
    <marker id="arrow" markerWidth="24" markerHeight="24" refX="20" refY="10"
      orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L21,10 L0,20 z" fill="#b72831"/>
    </marker>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity=".45"/>
    </filter>
  </defs>
  <image x="0" y="0" width="1900" height="1267"
    xlink:href="{map_href}" opacity=".93"/>
  <rect x="{x + 14}" y="{y + 14}" width="{min(width - 28, 560)}" height="48"
    rx="7" fill="#f7f5ee" fill-opacity=".94" stroke="#17201b" stroke-width="2"/>
  <text x="{x + 34}" y="{y + 47}" font-family="Arial,Helvetica,sans-serif"
    font-size="25" font-weight="700" fill="#17201b">{title}</text>
  <g filter="url(#shadow)">
    {''.join(overlays)}
  </g>
</svg>'''
    svg_path = OUT / f"{name}.svg"
    pdf_path = OUT / f"{name}.pdf"
    svg_path.write_text(svg, encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-f", "pdf", "-o", str(pdf_path), str(svg_path)],
        check=True,
        cwd=OUT,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    write_map(
        "playbook-turn-1-map",
        "Game-Turn 1: Chetnik probes",
        (950, 170, 850, 790),
        [
            badge(1, 1405, 455, "Start"),
            arrow(1405, 455, 1355, 245),
            badge(2, 1355, 245, "Pančevo"),
            badge(3, 1195, 920, "Cetinje"),
            arrow(1535, 380, 1365, 255, dashed=True),
            badge(4, 1540, 380, "Axis reply"),
        ],
    )

    write_map(
        "playbook-turn-2-map",
        "Game-Turn 2: Tito and the Partisans",
        (120, 80, 1600, 880),
        [
            badge(1, 1390, 535, "10 groups + Tito"),
            arrow(1380, 520, 1210, 495),
            badge(2, 1210, 495, "Užice"),
            arrow(1390, 540, 1310, 590),
            badge(3, 1310, 590, "Novi Pazar"),
            badge(4, 280, 295, "4 groups"),
            badge(5, 1165, 885, "3 groups"),
        ],
    )

    write_map(
        "playbook-turn-3-map",
        "Game-Turn 3: The war spreads",
        (330, 100, 1230, 820),
        [
            badge(1, 1390, 535, "AGO: Serbia"),
            arrow(1370, 515, 760, 360),
            badge(2, 760, 350, "Tito escapes"),
            badge(3, 580, 430, "Croatia uprising"),
            badge(4, 780, 290, "Bosnia uprising"),
        ],
    )

    write_map(
        "playbook-turn-4-map",
        "Game-Turn 4: Winter and escalation",
        (330, 100, 1230, 830),
        [
            badge(1, 760, 295, "Tito identified"),
            badge(2, 1310, 590, "25th + 27th"),
            arrow(1390, 360, 660, 610),
            badge(3, 660, 610, "342 enters Croatia"),
            badge(4, 470, 245, "Winter"),
        ],
    )

    write_map(
        "playbook-turn-5-map",
        "Game-Turn 5: The hunt for Tito",
        (330, 100, 1230, 830),
        [
            badge(1, 535, 455, "Tito located"),
            arrow(1370, 370, 600, 430),
            badge(2, 865, 390, "AGO"),
            arrow(600, 455, 760, 350, dashed=True),
            badge(3, 760, 350, "Retreat"),
            badge(4, 495, 185, "Recruitment halved"),
        ],
    )


if __name__ == "__main__":
    main()
