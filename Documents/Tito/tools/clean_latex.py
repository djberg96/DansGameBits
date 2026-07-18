#!/usr/bin/env python3
"""Apply repeatable, mechanical OCR cleanups to generated section files."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "sections"

REPLACEMENTS = {
    "Game- Turn": "Game-Turn",
    "Game- Turns": "Game-Turns",
    "Player- Turn": "Player-Turn",
    "Player- Turns": "Player-Turns",
    "pro- Yugoslav": "pro-Yugoslav",
    "pro- Axis": "pro-Axis",
    "Anti- Guerrilla": "Anti-Guerrilla",
    "non- Italian": "non-Italian",
    "pre- determined": "predetermined",
    "througha": "through a",
    "rollis": "roll is",
    "Ifthé": "If the",
    "fu/l": "full",
    "fu//": "full",
    "50lst": "501st",
    "through 5S": "through 5",
    "through §5": "through 5",
    "brigadesize": "brigade size",
    "divisionstrength": "division strength",
    "Victory Roint": "Victory Point",
    "On.Game-Turn": "On Game-Turn",
    "inindicates": "indicates",
    "Phase,.a": "Phase, a",
    "upperhalf": "upper half",
    "Marker\\_is": "marker is",
    "an Jtalian": "an Italian",
    "q prohibited": "a prohibited",
    "Asa result": "As a result",
    "Bonus. Movement": "Bonus Movement",
    "market.towns": "market towns",
    "which.a": "which a",
    "«die": "die",
    "J or more": "1 or more",
    "A// numbered": "All numbered",
    "Itis ": "It is ",
    "that.are": "that are",
    "anormal": "a normal",
    "**D”’": "``D''",
    "two. types": "two types",
    "Chetniks stack": "Chetnik stack",
    "+1:If": "+1: If",
    "Inall": "In all",
    "Pro- Yugoslav": "Pro-Yugoslav",
    "by. recruitment": "by recruitment",
    "1 through 5. indicates": "1 through 5 indicates",
    "Exam- ‘ple": "Example",
    "Cases 6.64, .41, and 13.91D": "Cases 6.64, 9.41, and 13.91D",
    "the. game": "the game",
    "Re- . placements": "Replacements",
    "rein- . forcements": "reinforcements",
    "\n-Stage)": "\nStage)",
    "\n-created.": "\ncreated.",
    "2\\%": r"2\textonequarter",
    "Recruitment Values of \\%": r"Recruitment Values of \textonehalf",
    " \\_": "",
    "\\_": "",
    "7TITO RULES, PAGE 7": "",
}


for path in ROOT.glob("*.tex"):
    text = path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    text = re.sub(r"\bina\b", "in a", text)
    text = re.sub(r"^.*TITO RULES, PAGE.*$", "", text, flags=re.M)
    text = text.replace("‘*sphere of influence’’", "``sphere of influence''")
    text = text.replace("‘Bulgarian Occupation”’", "``Bulgarian Occupation''")
    text = text.replace("‘‘Bulgarian Occupation.”’", "``Bulgarian Occupation.''")
    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8")
