#!/usr/bin/env python3
"""Generate annotated map excerpts for the Tito five-turn playbook.

The excerpts deliberately use numbered callouts rather than trying to reproduce
every stack on the map.  The corresponding playbook text supplies the exact
unit counts and die rolls.
"""

from pathlib import Path
import base64
from io import BytesIO
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1] / "figures"
MAP_PATH = ROOT / "Misc/Images/Tito/tito_map.jpg"


def map_data_uri(viewbox: tuple[int, int, int, int]) -> str:
    """Return only the requested map crop as an embedded JPEG."""
    x, y, width, height = viewbox
    with Image.open(MAP_PATH) as source:
        crop = source.crop((x, y, x + width, y + height)).convert("RGB")
        buffer = BytesIO()
        crop.save(buffer, format="JPEG", quality=91, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
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
    map_href = map_data_uri(viewbox)
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
  <image x="{x}" y="{y}" width="{width}" height="{height}"
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
        "GT1: Pančevo",
        (1030, 170, 670, 520),
        [
            badge(1, 1405, 455, "Start"),
            arrow(1405, 455, 1355, 245),
            badge(2, 1355, 245, "Pančevo"),
            arrow(1535, 380, 1365, 255, dashed=True),
            badge(4, 1510, 380, "Axis reply"),
        ],
    )

    write_map(
        "playbook-turn-1-south-map",
        "GT1: Cetinje",
        (960, 650, 470, 330),
        [
            arrow(1120, 760, 1195, 920),
            badge(3, 1195, 920, "Cetinje"),
        ],
    )

    write_map(
        "playbook-turn-2-map",
        "GT2: Serbia",
        (1080, 280, 520, 430),
        [
            badge(1, 1390, 535, "10 groups + Tito"),
            arrow(1380, 520, 1210, 495),
            badge(2, 1210, 495, "Užice"),
            arrow(1390, 540, 1310, 590),
            badge(3, 1310, 590, "Novi Pazar"),
        ],
    )

    write_map(
        "playbook-turn-2-slovenia-map",
        "GT2: Slovenia",
        (100, 120, 520, 360),
        [
            badge(4, 280, 295, "4 groups"),
        ],
    )

    write_map(
        "playbook-turn-2-south-map",
        "GT2: Montenegro",
        (980, 650, 440, 330),
        [
            badge(5, 1165, 885, "3 groups"),
        ],
    )

    write_map(
        "playbook-turn-3-map",
        "GT3: Serbia AGO",
        (980, 260, 560, 460),
        [
            badge(1, 1390, 535, "AGO: Serbia"),
            arrow(1370, 515, 1010, 390),
            badge(2, 1035, 385, "Reaction west"),
        ],
    )

    write_map(
        "playbook-turn-3-west-map",
        "GT3: Bosnia and Croatia",
        (420, 170, 600, 430),
        [
            arrow(1005, 385, 760, 360),
            badge(2, 760, 350, "Tito arrives"),
            badge(3, 580, 430, "Croatia uprising"),
            badge(4, 780, 290, "Bosnia uprising"),
        ],
    )

    write_map(
        "playbook-turn-4-map",
        "GT4: Escalation west",
        (400, 130, 700, 560),
        [
            badge(1, 760, 295, "Tito identified"),
            arrow(1080, 440, 660, 610),
            badge(2, 660, 610, "342 enters Croatia"),
        ],
    )

    write_map(
        "playbook-turn-4-east-map",
        "GT4: Serbia",
        (1080, 280, 440, 380),
        [
            badge(3, 1310, 590, "25th + 27th"),
            badge(4, 1415, 405, "342 starts"),
            arrow(1390, 420, 1090, 450),
        ],
    )

    write_map(
        "playbook-turn-5-map",
        "GT5: The hunt in Croatia",
        (420, 220, 650, 440),
        [
            badge(1, 535, 455, "Tito located"),
            badge(2, 865, 390, "AGO"),
            arrow(600, 455, 760, 350, dashed=True),
            badge(3, 760, 350, "Retreat"),
        ],
    )

    write_map(
        "playbook-turn-5-east-map",
        "GT5: Recruitment",
        (1100, 190, 500, 520),
        [
            arrow(1190, 325, 1360, 250),
            badge(4, 1190, 325, "Pančevo: none"),
            badge(5, 1310, 590, "Novi Pazar: +1"),
        ],
    )


if __name__ == "__main__":
    main()
