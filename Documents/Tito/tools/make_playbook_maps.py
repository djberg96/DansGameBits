#!/usr/bin/env python3
"""Generate annotated map excerpts for the Tito five-turn playbook."""

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


def counter_data_uri(filename: str, replacements: dict[str, str] | None = None) -> str:
    """Return a counter SVG as an embedded data URI, with optional text changes."""
    counter_svg = (OUT / filename).read_text(encoding="utf-8")
    for old, new in (replacements or {}).items():
        counter_svg = counter_svg.replace(f">{old}<", f">{new}<")
    encoded = base64.b64encode(counter_svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def counter_stack(
    filename: str,
    x: int,
    y: int,
    size: int,
    count: int = 1,
    replacements: dict[str, str] | None = None,
    count_side: str = "right",
) -> str:
    """Draw a compact stack of identical counters with an explicit unit count."""
    href = counter_data_uri(filename, replacements)
    visible_counters = min(count, 3)
    offset = 2
    images = "".join(
        f'<image x="{x + layer * offset}" y="{y - layer * offset}" '
        f'width="{size}" height="{size}" xlink:href="{href}"/>'
        for layer in reversed(range(visible_counters))
    )
    if count == 1:
        return images

    tab_width = 25
    tab_height = 16
    tab_x = x - 18 if count_side == "left" else x + size - 6
    tab_y = y + size - 11
    return (
        images
        + f'<rect x="{tab_x}" y="{tab_y}" width="{tab_width}" '
        f'height="{tab_height}" rx="5" '
        f'fill="#17201b" stroke="#f7f5ee" stroke-width="1.5"/>'
        f'<text x="{tab_x + tab_width / 2}" y="{tab_y + 12}" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="11" '
        f'font-weight="700" text-anchor="middle" fill="#ffffff">×{count}</text>'
    )


def write_map(
    name: str,
    title: str,
    viewbox: tuple[int, int, int, int],
    overlays: list[str],
    compact_title: bool = False,
) -> None:
    x, y, width, height = viewbox
    map_href = map_data_uri(viewbox)
    if compact_title:
        title_width = min(width - 28, max(150, len(title) * 11 + 32))
        title_height = 40
        title_font_size = 20
        title_baseline = y + 41
    else:
        title_width = min(width - 28, max(170, len(title) * 14 + 38))
        title_height = 48
        title_font_size = 25
        title_baseline = y + 47
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    width="{width}" height="{height}" viewBox="{x} {y} {width} {height}">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity=".45"/>
    </filter>
  </defs>
  <image x="{x}" y="{y}" width="{width}" height="{height}"
    xlink:href="{map_href}" opacity=".93"/>
  <rect x="{x + 14}" y="{y + 14}" width="{title_width}" height="{title_height}"
    rx="7" fill="#f7f5ee" fill-opacity=".94" stroke="#17201b" stroke-width="2"/>
  <text x="{x + 34}" y="{title_baseline}" font-family="Arial,Helvetica,sans-serif"
    font-size="{title_font_size}" font-weight="700" fill="#17201b">{title}</text>
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
            counter_stack(
                "chetnik-group.svg", 1310, 235, 32, 3, count_side="left"
            ),
            counter_stack(
                "german-infantry-front.svg",
                1355,
                235,
                32,
                replacements={"704": "714"},
            ),
            counter_stack("chetnik-group.svg", 1435, 395, 32, 2),
            badge(1, 1482, 380),
            badge(2, 1408, 220),
            badge(4, 1587, 337),
        ],
    )

    write_map(
        "playbook-turn-1-south-map",
        "GT1: Cetinje",
        (960, 650, 470, 330),
        [
            counter_stack("chetnik-group.svg", 1141, 903, 32, 2),
            badge(3, 1120, 950),
        ],
    )

    write_map(
        "playbook-turn-2-map",
        "GT2: Serbia",
        (1080, 280, 520, 430),
        [
            counter_stack(
                "partisan-group.svg", 1167, 510, 32, 3, count_side="left"
            ),
            counter_stack("german-infantry-front.svg", 1210, 510, 32),
            counter_stack(
                "partisan-group.svg", 1308, 602, 32, 3, count_side="left"
            ),
            counter_stack(
                "partisan-group.svg", 1338, 403, 30, 4, count_side="left"
            ),
            counter_stack("tito-unidentified.svg", 1346, 395, 30),
            counter_stack("chetnik-group.svg", 1427, 457, 30),
            counter_stack("chetnik-group.svg", 1461, 523, 30, 2),
            badge(1, 1310, 455),
            badge(2, 1160, 500),
            badge(3, 1410, 622),
        ],
    )

    write_map(
        "playbook-turn-2-slovenia-map",
        "GT2: Slovenia",
        (100, 120, 520, 360),
        [
            counter_stack("partisan-group.svg", 231, 214, 30, 4),
            badge(4, 350, 315),
        ],
    )

    write_map(
        "playbook-turn-2-south-map",
        "GT2: Montenegro",
        (980, 650, 440, 330),
        [
            counter_stack(
                "partisan-group.svg", 1141, 903, 32, 3, count_side="left"
            ),
            counter_stack(
                "italian-infantry.svg",
                1184,
                903,
                32,
                replacements={"PARMA": "MACERATA"},
            ),
            counter_stack("chetnik-group.svg", 1219, 662, 30, 4),
            badge(5, 1240, 935),
        ],
        compact_title=True,
    )

    write_map(
        "playbook-turn-3-map",
        "GT3: Serbia AGO",
        (980, 260, 560, 460),
        [
            counter_stack(
                "german-infantry-front.svg",
                1342,
                392,
                30,
                replacements={"704": "714"},
            ),
            counter_stack(
                "german-infantry-front.svg",
                1347,
                387,
                30,
                replacements={"704": "717"},
            ),
            counter_stack(
                "german-infantry-front.svg", 1342, 452, 30
            ),
            counter_stack(
                "german-infantry-front.svg",
                1347,
                447,
                30,
                replacements={"704": "342", "12": "18"},
            ),
            counter_stack(
                "chetnik-group.svg", 1387, 395, 30, 2, count_side="left"
            ),
            counter_stack(
                "partisan-group.svg", 1437, 395, 30, 4
            ),
            counter_stack("partisan-group.svg", 1437, 452, 30),
            counter_stack(
                "chetnik-group.svg", 1462, 527, 30
            ),
            counter_stack(
                "partisan-group.svg", 1308, 602, 30, 5, count_side="left"
            ),
            badge(1, 1510, 500),
            badge(2, 1035, 360),
        ],
    )

    write_map(
        "playbook-turn-3-west-map",
        "GT3: Bosnia and Croatia",
        (420, 170, 600, 430),
        [
            counter_stack(
                "partisan-group.svg", 795, 245, 30, 2, count_side="left"
            ),
            counter_stack("tito-unidentified.svg", 803, 237, 30),
            badge(2, 850, 235),
            badge(3, 790, 550),
            badge(4, 910, 420),
        ],
    )

    write_map(
        "playbook-turn-4-map",
        "GT4: Escalation west",
        (400, 130, 700, 560),
        [
            badge(1, 920, 260),
            badge(2, 700, 665),
        ],
    )

    write_map(
        "playbook-turn-4-east-map",
        "GT4: Serbia",
        (1080, 280, 440, 380),
        [
            badge(3, 1400, 620),
            badge(4, 1475, 370),
        ],
    )

    write_map(
        "playbook-turn-5-map",
        "GT5: The hunt in Croatia",
        (420, 220, 650, 440),
        [
            badge(1, 680, 495),
            badge(2, 500, 395),
            badge(3, 935, 275),
        ],
    )

    write_map(
        "playbook-turn-5-east-map",
        "GT5: Recruitment",
        (1100, 190, 500, 520),
        [
            badge(4, 1400, 280),
            badge(5, 1390, 650),
        ],
    )


if __name__ == "__main__":
    main()
