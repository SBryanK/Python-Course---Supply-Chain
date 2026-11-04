"""Build, run and check the course notebooks.

For every session it writes
  sessions/<folder>/student.ipynb            (what she gets, no outputs)
  teacher_only/sessions/<folder>/solution.ipynb  (answers, with outputs)
then runs both in a fresh kernel. Drive cells are swapped for local paths during the
test run only; the saved files keep the Drive cells.

Run:  python tools/2_notebooks/build.py [s01 s02 ...]
"""
import copy
import importlib
import os
import re
import sys
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import nbkit  # noqa: E402

WORK = Path(os.environ.get("TEST_WORK", "/private/tmp/pysc_work"))
LOCAL_DATA = str(ROOT / "data" / "online_retail_ii_lesson.csv")
BANNED = ["delve", "leverage", "seamless", "journey"]
SESSIONS = ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10"]


def local_copy(nb):
    nb = copy.deepcopy(nb)
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        s = c.source
        s = s.replace(nbkit.DRIVE_DATA, LOCAL_DATA).replace(nbkit.DRIVE_WORK, str(WORK) + "/")
        s = re.sub(r"^from google\.colab import drive\s*$", "", s, flags=re.M)
        s = re.sub(r"^drive\.mount\(.*\)\s*$", "", s, flags=re.M)
        c.source = s
    return nb


def run(nb, name):
    WORK.mkdir(parents=True, exist_ok=True)
    test = local_copy(nb)
    client = NotebookClient(test, timeout=300, kernel_name="python3", allow_errors=True,
                            resources={"metadata": {"path": str(WORK)}})
    client.execute()
    return test


def errors(nb):
    found = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        for o in c.get("outputs", []):
            if o.output_type == "error":
                tags = c.metadata.get("tags", [])
                found.append((i, "error-on-purpose" in tags or "exercise" in tags, o.ename))
    return found


def text_of(nb):
    out = []
    for c in nb.cells:
        if c.cell_type == "code":
            for o in c.get("outputs", []):
                if o.output_type == "stream":
                    out.append(o.text)
                elif o.output_type in ("execute_result", "display_data"):
                    out.append(o.get("data", {}).get("text/plain", ""))
    return "\n".join(out)


def style_problems(nb):
    problems = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "markdown":
            continue
        t = c.source
        if "—" in t:
            problems.append(f"cell {i}: em dash")
        if re.search(r"[A-Za-z0-9)]!(\s|$)", t):
            problems.append(f"cell {i}: exclamation mark")
        for w in BANNED:
            if w in t.lower():
                problems.append(f"cell {i}: banned word {w}")
        if re.search(r"michella|natalia|bryan", t, re.I):
            problems.append(f"cell {i}: a name")
    return problems


def build_one(key):
    mod = importlib.import_module(f"sessions_{key}")
    S = mod.SESSION
    cells = nbkit.flatten(S["cells"])
    n = len(cells)
    student = nbkit.make(S["cells"], "student")
    solution = nbkit.make(S["cells"], "solution")
    sdir = ROOT / "sessions" / S["folder"]
    tdir = ROOT / "teacher_only" / "sessions" / S["folder"]
    sdir.mkdir(parents=True, exist_ok=True)
    tdir.mkdir(parents=True, exist_ok=True)

    ran_stu = run(student, key)   # student first, so the solution run leaves the correct files in WORK
    ran_sol = run(solution, key)

    report = [f"{key}: {n} cells"]
    if n > 50:
        report.append(f"  FAIL more than 50 cells ({n})")
    for i, intended, ename in errors(ran_sol):
        if not intended or ran_sol.cells[i].metadata.get("tags") == ["exercise"]:
            report.append(f"  FAIL solution error in cell {i}: {ename}")
    for i, intended, ename in errors(ran_stu):
        if not intended:
            report.append(f"  FAIL student error in cell {i}: {ename}")
    out = text_of(ran_sol)
    if "Not yet" in out:
        report.append(f"  FAIL a check() fails in the solution ({out.count('Not yet')}x)")
    for want in S.get("expect", []):
        if want not in out:
            report.append(f"  FAIL expected output missing: {want!r}")
    for p in style_problems(student):
        report.append("  FAIL " + p)

    # Save: student without outputs, solution with the outputs from the test run.
    for c in student.cells:
        if c.cell_type == "code":
            c["outputs"], c["execution_count"] = [], None
    for c, r in zip(solution.cells, ran_sol.cells):
        if c.cell_type == "code":
            c["outputs"] = r.get("outputs", [])
            c["execution_count"] = r.get("execution_count")
    nbf.write(student, sdir / "student.ipynb")
    nbf.write(solution, tdir / "solution.ipynb")
    ok = len(report) == 1
    report.append("  ok" if ok else "")
    print("\n".join(r for r in report if r))
    return ok


if __name__ == "__main__":
    keys = sys.argv[1:] or SESSIONS
    sys.dont_write_bytecode = True
    results = [build_one(k) for k in keys]
    sys.exit(0 if all(results) else 1)
