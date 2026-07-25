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


def badge(number: int, x: int, y: int) -> str:
    return (
        f'<circle cx="{x}" cy="{y}" r="17" fill="#b72831" '
        f'stroke="#17201b" stroke-width="2"/>'
        f'<text x="{x}" y="{y + 6}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="19" font-weight="700" text-anchor="middle" '
        f'fill="#ffffff">{number}</text>'
    )


def arrow(x1: int, y1: int, x2: int, y2: int, *, dashed: bool = False,
          via: tuple[tuple[int, int], ...] = ()) -> str:
    dash = ' stroke-dasharray="12 8"' if dashed else ""
    points = [(x1, y1), *via, (x2, y2)]
    path = " ".join(
        ("M" if index == 0 else "L") + f"{x} {y}"
        for index, (x, y) in enumerate(points)
    )
    return (
        f'<path d="{path}" fill="none" '
        f'stroke="#b72831" stroke-width="6" stroke-linecap="round" '
        f'stroke-linejoin="round" '
        f'marker-end="url(#arrow)"{dash}/>'
    )


def leader(x1: int, y1: int, x2: int, y2: int) -> str:
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" '
        f'stroke="#b72831" stroke-width="3" stroke-linecap="round"/>'
    )


def write_map(name: str, title: str, viewbox: tuple[int, int, int, int],
              overlays: list[str]) -> None:
    x, y, width, height = viewbox
    map_href = map_data_uri(viewbox)
    title_width = min(width - 28, max(170, len(title) * 14 + 38))
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
  <rect x="{x + 14}" y="{y + 14}" width="{title_width}" height="48"
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
            leader(1450, 455, 1428, 455),
            badge(1, 1468, 455),
            arrow(1435, 430, 1360, 270, via=((1460, 340),)),
            leader(1400, 245, 1378, 245),
            badge(2, 1418, 245),
            arrow(1515, 365, 1375, 265, dashed=True, via=((1460, 320),)),
            leader(1570, 390, 1525, 375),
            badge(4, 1588, 396),
        ],
    )

    write_map(
        "playbook-turn-1-south-map",
        "GT1: Cetinje",
        (960, 650, 470, 330),
        [
            arrow(1210, 815, 1200, 905, via=((1260, 835), (1260, 890))),
            leader(1245, 915, 1210, 915),
            badge(3, 1263, 915),
        ],
    )

    write_map(
        "playbook-turn-2-map",
        "GT2: Serbia",
        (1080, 280, 520, 430),
        [
            badge(1, 1450, 525),
            arrow(1380, 520, 1210, 495),
            badge(2, 1178, 480),
            arrow(1390, 540, 1310, 590),
            leader(1362, 612, 1342, 600),
            badge(3, 1380, 622),
        ],
    )

    write_map(
        "playbook-turn-2-slovenia-map",
        "GT2: Slovenia",
        (100, 120, 520, 360),
        [
            badge(4, 350, 315),
        ],
    )

    write_map(
        "playbook-turn-2-south-map",
        "GT2: Montenegro",
        (980, 650, 440, 330),
        [
            leader(1222, 930, 1202, 920),
            badge(5, 1240, 935),
        ],
    )

    write_map(
        "playbook-turn-3-map",
        "GT3: Serbia AGO",
        (980, 260, 560, 460),
        [
            badge(1, 1450, 540),
            arrow(1340, 485, 1010, 390, via=((1250, 505), (1120, 480))),
            badge(2, 1035, 360),
        ],
    )

    write_map(
        "playbook-turn-3-west-map",
        "GT3: Bosnia and Croatia",
        (420, 170, 600, 430),
        [
            arrow(1005, 385, 885, 265, via=((980, 315),)),
            leader(920, 250, 895, 250),
            badge(2, 938, 250),
            leader(657, 500, 638, 485),
            badge(3, 675, 510),
            leader(837, 290, 817, 285),
            badge(4, 855, 295),
        ],
    )

    write_map(
        "playbook-turn-4-map",
        "GT4: Escalation west",
        (400, 130, 700, 560),
        [
            leader(902, 260, 887, 260),
            badge(1, 920, 260),
            arrow(1080, 440, 660, 610),
            leader(690, 647, 670, 615),
            badge(2, 700, 665),
        ],
    )

    write_map(
        "playbook-turn-4-east-map",
        "GT4: Serbia",
        (1080, 280, 440, 380),
        [
            leader(1382, 610, 1358, 600),
            badge(3, 1400, 620),
            leader(1372, 390, 1352, 405),
            badge(4, 1390, 380),
            arrow(1340, 410, 1090, 420, via=((1250, 390),)),
        ],
    )

    write_map(
        "playbook-turn-5-map",
        "GT5: The hunt in Croatia",
        (420, 220, 650, 440),
        [
            leader(662, 495, 645, 480),
            badge(1, 680, 495),
            leader(518, 405, 540, 420),
            badge(2, 500, 395),
            arrow(630, 465, 875, 275, dashed=True,
                  via=((720, 420), (825, 335))),
            leader(917, 275, 897, 275),
            badge(3, 935, 275),
        ],
    )

    write_map(
        "playbook-turn-5-east-map",
        "GT5: Recruitment",
        (1100, 190, 500, 520),
        [
            leader(1382, 270, 1352, 252),
            badge(4, 1400, 280),
            leader(1372, 640, 1350, 610),
            badge(5, 1390, 650),
        ],
    )


if __name__ == "__main__":
    main()
