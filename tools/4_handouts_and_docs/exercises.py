"""Exercise lists for the handouts and the answer key, read from the session notebooks.

The notebook is the single source: every task cell ("**Fill in.** ... Expected: `x`") becomes
one row, so the handout and ANSWER_KEY.md always match what she sees in Colab.
"""
import re
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "2_notebooks"
sys.path.insert(0, str(NB))
import importlib  # noqa: E402

import nbkit  # noqa: E402

TASK = re.compile(r"^\*\*(Predict|Fill in|Fix it|Write it|Case|Extra)\.\*\*\s*(.*)$", re.S)
KEEP_OWN = {7, 8, 9}   # project items that are not notebook tasks stay as they were


def plain(text):
    return text.replace("`", "").replace("**", "").replace("\n", " ").strip()


def from_notebook(S):
    mod = importlib.import_module(f"sessions_s{S['no']:02d}")
    rows = []
    for c in nbkit.flatten(mod.SESSION["cells"]):
        if c["kind"] != "md":
            continue
        m = TASK.match(c["text"])
        if not m:
            continue
        kind, rest = m.groups()
        task, _, expected = rest.partition("Expected:")
        task = plain(task)
        if expected.strip():
            expected = plain(expected)
        elif kind == "Predict":
            expected = "Guess first, then run it to check"
        elif kind == "Fix it":
            expected = "The cell runs without an error"
        else:
            expected = "Your own sentence" if kind == "Case" else "Your own"
        rows.append((f"{kind}: {task}", expected))
    return rows


def apply(all_sessions):
    for S in all_sessions:
        if "own_exercises" in S:   # already applied (the module is imported by two builders)
            continue
        S["own_exercises"] = list(S["exercises"])
        rows = from_notebook(S)
        if rows:
            S["exercises"] = rows + (S["own_exercises"] if S["no"] in KEEP_OWN else [])
    return all_sessions
