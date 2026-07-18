#!/usr/bin/env python3
"""Generate complete vector reconstructions of Tito's 200-counter sheet."""

from dataclasses import dataclass
from html import escape
from pathlib import Path
import subprocess


OUT = Path(__file__).resolve().parents[1] / "figures"
INK = "#17201b"
COLORS = {
    "german": "#b9c3c1",
    "serbian": "#e88952",
    "italian": "#d8c69f",
    "croat": "#ebc95a",
    "bulgarian": "#aaa369",
    "soviet": "#d997aa",
    "partisan": "#e34f5f",
    "chetnik": "#f4f1e7",
    "marker": "#f4f1e7",
}


@dataclass(frozen=True)
class Face:
    faction: str
    designation: str = ""
    size: str = ""
    strength: str = ""
    kind: str = "infantry"
    marker: str = ""
    ink: str = INK


def blank(faction: str) -> Face:
    return Face(faction=faction, kind="blank")


def unit(faction: str, designation: object, size: str, strength: object,
         kind: str = "infantry", ink: str = INK) -> Face:
    return Face(faction, str(designation), size, str(strength), kind, ink=ink)


def group(faction: str, number: int, strength: int = 1) -> Face:
    ink = "#c9252d" if faction == "chetnik" else INK
    return unit(faction, f"{number} GROUP", "", strength, ink=ink)


def marker(kind: str, designation: str = "", strength: str = "",
           faction: str = "marker") -> Face:
    return Face(faction, designation, strength=strength, kind="marker", marker=kind)


def new_sheet(backgrounds: list[tuple[range, range, str]]) -> list[list[Face]]:
    sheet = [[blank("marker") for _ in range(20)] for _ in range(10)]
    for rows, columns, faction in backgrounds:
        for row in rows:
            for column in columns:
                sheet[row - 1][column - 1] = blank(faction)
    return sheet


def put(sheet: list[list[Face]], row: int, column: int,
        faces: list[Face]) -> None:
    for offset, face in enumerate(faces):
        sheet[row - 1][column - 1 + offset] = face


def front_sheet() -> list[list[Face]]:
    sheet = new_sheet([
        (range(1, 3), range(1, 11), "german"),
        (range(1, 3), range(11, 21), "chetnik"),
        (range(3, 5), range(1, 7), "german"),
        (range(3, 5), range(7, 11), "italian"),
        (range(3, 5), range(11, 15), "chetnik"),
        (range(3, 5), range(15, 21), "marker"),
        (range(5, 7), range(1, 4), "serbian"),
        (range(5, 7), range(4, 11), "italian"),
        (range(5, 11), range(11, 21), "partisan"),
        (range(7, 9), range(1, 11), "croat"),
        (range(9, 11), range(1, 6), "bulgarian"),
        (range(9, 11), range(6, 11), "soviet"),
    ])

    put(sheet, 1, 1, [unit("german", d, "XX", s) for d, s in
        [(704, 12), (714, 12), (717, 12), (718, 12), (297, 12),
         ("11LW", 12), (113, 18), (181, 18), (342, 18), (264, 15)]])
    put(sheet, 2, 1, [
        unit("german", 371, "XX", 15), unit("german", "100L", "XX", 10),
        unit("german", 369, "XX", 10), unit("german", 373, "XX", 10),
        unit("german", 392, "XX", 10), unit("german", 98, "XX", 20),
        unit("german", 187, "XX", 9), unit("german", 173, "XX", 6),
        unit("german", 125, "III", 3),
        unit("german", "4SS", "XX", 20, "mechanized"),
    ])
    put(sheet, 3, 1, [
        unit("german", 22, "XX", 24, "mountain"),
        unit("german", 92, "II", 6, "mechanized"),
        unit("german", 1, "XX", 20),
        unit("german", "7SS", "XX", 16, "mountain"),
        unit("german", "13SS", "XX", 8, "mountain"),
        unit("german", "21SS", "XX", 8, "mountain"),
    ])
    put(sheet, 4, 1, [
        unit("german", "501SS", "II", 1, "airborne"),
        unit("german", "23SS", "XX", 4, "mountain"),
        unit("german", "1Pz", "XX", 30, "armor"),
        unit("german", "202Pz", "II", 10, "armor"),
        unit("german", "1Cos", "XX", 9, "cavalry"),
    ])

    put(sheet, 3, 7, [unit("italian", d, "XX", 6) for d in
        ["Emilia", "Marche", "Murze", "Messina"]])
    put(sheet, 4, 7, [unit("italian", d, "XX", 6) for d in
        ["Sassari", "Re", "Lombard", "Macerata"]])
    put(sheet, 5, 1, [unit("serbian", n, "X", 1) for n in range(1, 4)])
    put(sheet, 6, 1, [unit("serbian", n, "X", 1) for n in range(4, 6)])
    put(sheet, 5, 4, [unit("italian", d, "XX", 6) for d in
        ["Perugia", "Venezia", "Puglia", "Firenze", "Arezzo", "Parma", "Alpi Gr"]])
    put(sheet, 6, 4, [
        unit("italian", "CD Alpi", "XX", 6, "mountain"),
        unit("italian", "Savoia", "XX", 6, "mountain"),
        unit("italian", "Zara", "XX", 6, "mechanized"),
        unit("italian", "Isonzo", "XX", 6), unit("italian", "Ferrara", "XX", 6),
        unit("italian", "Taurinense", "XX", 6, "mountain"),
        unit("italian", "Bergamo", "XX", 6),
    ])

    put(sheet, 7, 1, [unit("croat", n, "X", 1) for n in range(2, 7)] +
        [unit("croat", f"{n}Mt", "X", 2, "mountain") for n in range(1, 6)])
    put(sheet, 8, 1, [unit("croat", "Gd", "III", 3)] +
        [unit("croat", f"{n}Ust", "X", 2) for n in range(1, 6)] +
        [unit("croat", 1, "X", 1)])
    put(sheet, 9, 1, [unit("bulgarian", d, "XX", s) for d, s in
        [(7, 15), (8, 15), (6, 18), (9, 18)]])
    put(sheet, 10, 1, [unit("bulgarian", d, "XX", 12) for d in [14, 22, 24, 25, 27]])
    put(sheet, 9, 6, [unit("soviet", d, "XXX", s) for d, s in
        [(68, 30), (64, 30), ("10Gd", 33), ("18Gd", 33), ("20Gd", 33)]])
    put(sheet, 10, 6, [
        unit("soviet", 75, "XXX", 30), unit("soviet", "31Gd", "XXX", 33),
        unit("soviet", 5, "X", 12, "mechanized"),
        unit("soviet", 7, "XXX", 38, "mechanized"),
        unit("soviet", "4Gd", "XXX", 42, "mechanized"),
    ])

    put(sheet, 1, 11, [group("chetnik", n) for n in range(1, 11)])
    put(sheet, 2, 11, [group("chetnik", n) for n in range(11, 21)])
    put(sheet, 3, 11, [group("chetnik", n) for n in range(21, 24)])
    put(sheet, 4, 11, [group("chetnik", n) for n in range(24, 26)])
    sheet[2][14] = marker("turn", "GAME")
    sheet[2][15] = marker("allied", "ALLIED")
    sheet[3][14] = marker("vp", "VP (+)", "×1")
    sheet[3][15] = marker("vp", "VP (+)", "×10")
    sheet[3][16] = marker("vp", "VP (+)", "×100")
    sheet[3][19] = marker("tito", "TITO", "NOT IDENT.", "partisan")

    put(sheet, 5, 11, [group("partisan", n) for n in range(1, 7)] +
        [unit("partisan", n, "X", 4) for n in range(31, 35)])
    put(sheet, 6, 11, [unit("partisan", n, "X", 4) for n in range(35, 45)])
    put(sheet, 7, 11, [unit("partisan", n, "X", 4) for n in range(45, 55)])
    put(sheet, 8, 11, [unit("partisan", n, "X", 4) for n in range(55, 61)] +
        [group("partisan", n) for n in range(7, 11)])
    put(sheet, 9, 11, [group("partisan", n) for n in range(11, 21)])
    put(sheet, 10, 11, [group("partisan", n) for n in range(21, 31)])
    return sheet


def back_sheet() -> list[list[Face]]:
    sheet = new_sheet([
        (range(1, 3), range(1, 11), "chetnik"),
        (range(1, 3), range(11, 21), "german"),
        (range(3, 5), range(1, 11), "marker"),
        (range(3, 7), range(11, 21), "partisan"),
        (range(5, 11), range(1, 11), "partisan"),
        (range(7, 9), range(11, 21), "croat"),
        (range(9, 11), range(11, 16), "soviet"),
        (range(9, 11), range(16, 21), "bulgarian"),
    ])
    red = "#c9252d"
    put(sheet, 1, 1, [unit("chetnik", n, "X", 4, ink=red) for n in range(10, 0, -1)])
    put(sheet, 2, 1, [unit("chetnik", n, "X", 4, ink=red) for n in range(20, 10, -1)])
    put(sheet, 1, 17, [unit("german", d, "XX", 15) for d in
        ["118L", "117L", "114L", "104L"]])

    sheet[2][5] = marker("turn", "DROUGHT")
    put(sheet, 3, 8, [unit("chetnik", n, "X", 4, ink=red) for n in [23, 22, 21]])
    sheet[3][0] = marker("tito", "TITO", "IDENTIFIED", "partisan")
    sheet[3][3] = marker("vp", "VP (-)", "×100")
    sheet[3][4] = marker("vp", "VP (-)", "×10")
    sheet[3][5] = marker("vp", "VP (-)", "×1")
    put(sheet, 4, 9, [unit("chetnik", n, "X", 4, ink=red) for n in [25, 24]])

    put(sheet, 3, 11, [unit("partisan", n, "XX", 12) for n in [34, 33, 32, 31]])
    put(sheet, 4, 11, [unit("partisan", n, "XX", 12) for n in [39, 38, 37, 36]])
    put(sheet, 5, 1, [unit("partisan", n, "XX", 12) for n in [4, 3, 2, 1]] +
        [unit("partisan", n, "X", 4) for n in [6, 5, 4, 3, 2, 1]])
    put(sheet, 5, 11, [unit("partisan", n, "XX", 12) for n in [49, 48, 47, 46, 45, 44, 43]])
    put(sheet, 6, 1, [unit("partisan", n, "XX", 12) for n in range(14, 4, -1)])
    put(sheet, 6, 11, [unit("partisan", n, "XX", 12) for n in [35, 42, 41, 40, 52, 51, 50]])
    put(sheet, 7, 1, [unit("partisan", n, "XX", 12) for n in range(24, 14, -1)])
    put(sheet, 8, 1, [unit("partisan", n, "X", 4) for n in [10, 9, 8, 7]] +
        [unit("partisan", n, "XX", 12) for n in [30, 29, 28, 27, 26, 25]])
    put(sheet, 9, 1, [unit("partisan", n, "X", 4) for n in range(20, 10, -1)])
    put(sheet, 10, 1, [unit("partisan", n, "X", 4) for n in range(30, 20, -1)])

    put(sheet, 7, 11, [unit("croat", n, "X", 4) for n in range(15, 5, -1)])
    put(sheet, 8, 14, [unit("croat", n, "X", 4) for n in [5, 4, 3, 2, 1]] +
        [unit("croat", "Sturm", "X", 5), unit("croat", "Gd", "X", 5)])
    put(sheet, 9, 11, [marker("ago", str(n), faction="soviet") for n in [8, 8, 8, 7, 6]])
    put(sheet, 10, 11, [marker("ago", str(n), faction="soviet") for n in [11, 10, 9, 8, 5]])
    put(sheet, 10, 16, [unit("bulgarian", n, "XX", 15) for n in [5, 4, 3, 2, 1]])
    return sheet


def symbol(kind: str, x: int, y: int, ink: str) -> str:
    left, top, width, height = x + 19, y + 33, 62, 34
    base = (f'<rect x="{left}" y="{top}" width="{width}" height="{height}" '
            f'fill="none" stroke="{ink}" stroke-width="2.4"/>')
    if kind in {"infantry", "mechanized", "mountain"}:
        base += (f'<path d="M{left} {top}L{left + width} {top + height}'
                 f'M{left} {top + height}L{left + width} {top}" '
                 f'fill="none" stroke="{ink}" stroke-width="2.4"/>')
    if kind == "mechanized":
        base += (f'<ellipse cx="{x + 50}" cy="{y + 50}" rx="19" ry="7.5" '
                 f'fill="none" stroke="{ink}" stroke-width="2.3"/>')
    elif kind == "mountain":
        base += (f'<path d="M{x + 41} {y + 64}L{x + 50} {y + 55}'
                 f'L{x + 59} {y + 64}Z" fill="none" stroke="{ink}" stroke-width="2"/>')
    elif kind == "armor":
        base += (f'<rect x="{x + 28}" y="{y + 40}" width="44" height="20" rx="10" '
                 f'fill="none" stroke="{ink}" stroke-width="2.4"/>')
    elif kind == "cavalry":
        base += (f'<path d="M{left} {top + height}L{left + width} {top}" '
                 f'fill="none" stroke="{ink}" stroke-width="2.4"/>')
    elif kind == "airborne":
        base += (f'<path d="M{x + 22} {y + 36}Q{x + 50} {y + 63} {x + 78} {y + 36}'
                 f'M{x + 50} {y + 37}V{y + 64}" fill="none" stroke="{ink}" stroke-width="2.1"/>')
    return base


def text(x: int, y: int, value: str, size: float, ink: str = INK,
         weight: int = 700) -> str:
    return (f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="middle" '
            f'fill="{ink}">{escape(value)}</text>')


def draw_face(face: Face, column: int, row: int) -> str:
    x, y = column * 100, row * 100
    color = COLORS[face.faction]
    items = [f'<rect x="{x + 1}" y="{y + 1}" width="98" height="98" '
             f'fill="{color}" stroke="#59605c" stroke-width="1.2"/>']
    if face.kind == "blank":
        return "".join(items)
    if face.kind == "marker":
        if face.marker == "tito":
            items += [text(x + 50, y + 41, face.designation, 15),
                      text(x + 50, y + 65, face.strength, 10)]
        elif face.marker == "turn":
            items += [text(x + 50, y + 41, face.designation, 12),
                      text(x + 50, y + 63, "TURN", 13)]
        elif face.marker == "allied":
            items += [text(x + 50, y + 40, "ALLIED", 12),
                      text(x + 50, y + 63, "PROGRESS", 9)]
        elif face.marker == "vp":
            items += [text(x + 50, y + 35, face.designation, 12),
                      text(x + 50, y + 66, face.strength, 15)]
        elif face.marker == "ago":
            items += [text(x + 50, y + 25, face.designation, 11),
                      text(x + 50, y + 63, "AGO", 19)]
        return "".join(items)

    designation_size = 9 if len(face.designation) > 6 else 11
    items += [text(x + 50, y + 16, face.designation, designation_size, face.ink),
              text(x + 50, y + 29, face.size, 9, face.ink),
              symbol(face.kind, x, y, face.ink),
              text(x + 50, y + 91, face.strength, 23, face.ink)]
    return "".join(items)


def write_sheet(name: str, sheet: list[list[Face]]) -> None:
    if len(sheet) != 10 or any(len(row) != 20 for row in sheet):
        raise ValueError(f"{name} must contain exactly 200 positions")
    body = "".join(draw_face(face, column, row)
                   for row, faces in enumerate(sheet)
                   for column, face in enumerate(faces))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1000" '
           f'viewBox="0 0 2000 1000">{body}'
           '<rect x="1" y="1" width="1998" height="998" fill="none" '
           'stroke="#17201b" stroke-width="2"/></svg>')
    svg_path = OUT / f"{name}.svg"
    pdf_path = OUT / f"{name}.pdf"
    svg_path.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf_path), str(svg_path)], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_sheet("counter-sheet-front", front_sheet())
    write_sheet("counter-sheet-back", back_sheet())


if __name__ == "__main__":
    main()
