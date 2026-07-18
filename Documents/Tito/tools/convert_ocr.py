#!/usr/bin/env python3
"""Turn the page-oriented Tito OCR into section-oriented LaTeX sources.

This is intentionally conservative: it preserves the wording of the 1980 rules,
while repairing scan line breaks and a short list of unmistakable OCR errors.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SECTION_NAMES = {
    1: "introduction",
    2: "game-equipment",
    3: "glossary",
    4: "sequence-of-play",
    5: "game-map",
    6: "movement",
    7: "guerrilla-units",
    8: "combat",
    9: "tito",
    10: "italian-units-and-allied-progress",
    11: "weather",
    12: "mountain-units",
    13: "reinforcements-replacements-and-upgrading",
    14: "yugoslav-victory-points",
    15: "how-to-start-and-win",
}


def page_text(ocr_dir: Path, number: int) -> str:
    return (ocr_dir / f"Tito{number}.txt").read_text(encoding="utf-8")


def repair_text(text: str) -> str:
    text = re.sub(r"^TITO RULES, PAGE\s*\d*\s*$", "", text, flags=re.M)
    text = text.replace("[6.4 YUGOSLAV", "[6.4] YUGOSLAV")
    replacements = {
        "THEGAME-TURN": "THE GAME-TURN",
        "MOVEA UNIT": "MOVE A UNIT",
        "atest": "a test",
        "acolor": "a color",
        "anew": "a new",
        "ina ": "in a ",
        "Ifthe": "If the",
        "Jslands": "Islands",
        "Execption": "Exception",
        "droughtand": "drought and",
        "dictates normal": "indicates normal",
        "/Jeft": "left",
        "/ocate": "locate",
        "al//": "all",
        "S5O1st": "501st",
        "5O1st": "501st",
        "5O\\st": "501st",
        "50\\st": "501st",
        "Italiar «init": "Italian unit",
        "Chetnik occupied": "Chetnik-occupied",
        "Yugoslav/ Partisan": "Yugoslav/Partisan",
        "pro- Yugoslav": "pro-Yugoslav",
        "pro- Yugoslav": "pro-Yugoslav",
        "balanceas": "balance as",
        "sustinence": "sustenance",
        "Game+Turn": "Game-Turn",
        "anti-guerrilla war": "anti-guerrilla war",
        "4% divisions": "4½ divisions",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"(?<!\w)\|(?!\w)", "1", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def join_wrapped_lines(block: str) -> str:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    out = ""
    for line in lines:
        if not out:
            out = line
        elif out.endswith("-") and line[:1].islower():
            out = out[:-1] + line
        else:
            out += " " + line
    for word in ("Hideaway", "GameTurn", "PlayerTurn", "Gamebox", "countermix"):
        fixes = {
            "Hideaway": "Hide-away",
            "GameTurn": "Game-Turn",
            "PlayerTurn": "Player-Turn",
            "Gamebox": "Game-box",
            "countermix": "counter mix",
        }
        out = out.replace(word, fixes[word])
    return out


def tex_escape(text: str) -> str:
    text = text.replace("&", r"\&").replace("%", r"\%")
    text = text.replace("#", r"\#").replace("_", r"\_")
    text = re.sub(r"(?<!\\)\$", r"\\$", text)
    text = text.replace("22”", r"22\textquotedblright")
    text = text.replace("34”", r"34\textquotedblright")
    return text


def heading_case(block: str) -> tuple[str, str] | None:
    match = re.match(r"^\[(\d+\.\d+[A-Z]?)\]\s*(.*)$", block, re.S)
    if not match:
        return None
    return match.group(1), match.group(2).strip()


def latexify(segment: str) -> str:
    blocks = [join_wrapped_lines(b) for b in re.split(r"\n\s*\n", segment) if b.strip()]
    output: list[str] = []
    general_rule_pending = False
    procedure_pending = False

    for block in blocks:
        block = block.strip(" >")
        if not block or block in {"ee eee)", "_"}:
            continue
        if block == "GENERAL RULE:":
            output.append(r"\ruleslabel{General Rule}")
            general_rule_pending = True
            continue
        if block == "PROCEDURE:":
            output.append(r"\ruleslabel{Procedure}")
            procedure_pending = True
            continue
        if block == "CASES:":
            output.append(r"\ruleslabel{Cases}")
            continue

        parsed = heading_case(block)
        if parsed:
            number, remainder = parsed
            title_like = remainder and remainder == remainder.upper() and len(remainder) < 100
            if number.endswith(".0"):
                output.append(rf"\section{{{tex_escape(remainder.title())}}}\label{{sec:{number}}}")
            elif re.fullmatch(r"\d+\.\d", number) and title_like:
                output.append(rf"\subsection{{{tex_escape(remainder.title())}}}\label{{sec:{number}}}")
            else:
                output.append(rf"\case{{{number}}} {tex_escape(remainder)}")
            continue

        escaped = tex_escape(block)
        if general_rule_pending:
            output.append(r"\begin{generalrule}" + "\n" + escaped + "\n" + r"\end{generalrule}")
            general_rule_pending = False
        elif procedure_pending:
            output.append(r"\begin{procedure}" + "\n" + escaped + "\n" + r"\end{procedure}")
            procedure_pending = False
        else:
            # Preserve readable hierarchy without over-interpreting OCR list structure.
            escaped = re.sub(r"^([A-Z]|\d+)\.\s+", r"\\textbf{\1.} ", escaped)
            output.append(escaped)

    return "\n\n".join(output).strip() + "\n"


def write_frontmatter(output_dir: Path, page1: str) -> None:
    read_first = page1.split("Read this First:", 1)[1].split("How the Section and Case Numbers", 1)[0]
    learn = page1.split("How to Learn to Play the Game:", 1)[1].split("[1.0] INTRODUCTION", 1)[0]
    # The obsolete postal-support paragraph is retained as a historical note, not as live support advice.
    learn = learn.split("We hope you enjoy", 1)[0]
    content = """\\section*{Read This First}
\\addcontentsline{toc}{section}{Read This First}

% Editorial note: wording retained from the original rules booklet.
""" + latexify(read_first).replace("\\section", "% \\section") + """

\\subsection*{How to Learn to Play the Game}
""" + latexify(learn)
    (output_dir / "00-frontmatter.tex").write_text(content, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: convert_ocr.py OCR_DIR OUTPUT_SECTIONS_DIR")
    ocr_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = {n: repair_text(page_text(ocr_dir, n)) for n in range(1, 12)}
    write_frontmatter(output_dir, pages[1])

    rules = pages[1][pages[1].index("[1.0] INTRODUCTION"):] + "\n\n"
    rules += "\n\n".join(pages[n] for n in range(2, 12))
    rules = rules.split("TITO DESIGN CREDITS", 1)[0]

    matches = list(re.finditer(r"^\[(\d+)\.0\]\s+", rules, flags=re.M))
    for i, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(rules)
        segment = rules[match.start():end]
        filename = f"{number:02d}-{SECTION_NAMES[number]}.tex"
        (output_dir / filename).write_text(latexify(segment), encoding="utf-8")

    tail = pages[11]
    credits = tail.split("TITO DESIGN CREDITS", 1)[1].split("ADDENDA", 1)[0]
    addenda = tail.split("ADDENDA", 1)[1].split("DESIGNER’S NOTES", 1)[0]
    notes = tail.split("DESIGNER’S NOTES", 1)[1]
    (output_dir / "16-credits.tex").write_text("\\section*{Design Credits}\n" + latexify(credits), encoding="utf-8")
    (output_dir / "17-addenda.tex").write_text("\\section{Addenda}\n" + latexify(addenda), encoding="utf-8")
    (output_dir / "18-designers-notes.tex").write_text("\\section{Designer’s Notes}\n" + latexify(notes), encoding="utf-8")


if __name__ == "__main__":
    main()
