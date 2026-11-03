"""Notebook kit: build student.ipynb and solution.ipynb from one cell list.

A session file defines SESSION (dict) with:
  folder   session folder name under sessions/
  title    notebook title
  cells    list made with md(), code(), exercise(), zoo()
  expect   strings that must appear in the executed solution output

Run:  _tools/venv/bin/python _tools/notebooks/build.py [s01 s02 ...]
"""
import nbformat as nbf

ROOT_MARK = "Python for Supply Chain"
DRIVE_DATA = "/content/drive/MyDrive/Python for Supply Chain/data/online_retail_ii_lesson.csv"
DRIVE_WORK = "/content/drive/MyDrive/Python for Supply Chain/work/"


def md(text):
    return {"kind": "md", "text": text.strip()}


def code(text, tag=None):
    """A cell that is the same for her and for the teacher."""
    return {"kind": "code", "student": text.strip(), "solution": text.strip(), "tag": tag}


def exercise(task, expected, student, solution, tag=None):
    """A text cell with the task and the expected result, then a TODO code cell."""
    text = f"**Your turn.** {task}\n\n*Expected:* {expected}"
    return [md(text), {"kind": "code", "student": student.strip(), "solution": solution.strip(), "tag": tag}]


def zoo(student, solution):
    """A cell that fails on purpose for her; the teacher notebook has it fixed."""
    return {"kind": "code", "student": student.strip(), "solution": solution.strip(), "tag": "error-on-purpose"}


def flatten(cells):
    out = []
    for c in cells:
        if isinstance(c, list):
            out.extend(c)
        else:
            out.append(c)
    return out


def make(cells, which):
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["colab"] = {"provenance": []}
    out = []
    for c in flatten(cells):
        if c["kind"] == "md":
            out.append(nbf.v4.new_markdown_cell(c["text"]))
        else:
            cell = nbf.v4.new_code_cell(c[which])
            if c.get("tag"):
                cell.metadata["tags"] = [c["tag"]]
            out.append(cell)
    nb.cells = out
    return nb


def blank(student, solution):
    """A code cell with no expected-answer text above it (used for the cold test)."""
    return {"kind": "code", "student": student.strip(), "solution": solution.strip(), "tag": None}
