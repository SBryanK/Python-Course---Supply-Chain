"""Run the saved notebooks (student and solution) in the current Python environment.

Use it in a fresh venv with a chosen pandas version, to see if the course still runs there.
Run:  <python> _tools/notebooks/test_env.py [work_dir]
"""
import sys
from pathlib import Path

import nbformat as nbf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

work = sys.argv[1] if len(sys.argv) > 1 else "/private/tmp/pysc_work_env"
build.WORK = Path(work)
import pandas, matplotlib  # noqa: E402,F401
print("python", sys.version.split()[0], "pandas", pandas.__version__, "matplotlib", matplotlib.__version__, flush=True)

bad = 0
for folder in sorted((build.ROOT / "sessions").iterdir()):
    for kind, path in (("student", folder / "student.ipynb"),
                       ("solution", build.ROOT / "teacher_only" / "sessions" / folder.name / "solution.ipynb")):
        nb = nbf.read(path, 4)
        for c in nb.cells:
            if c.cell_type == "code":
                c["outputs"], c["execution_count"] = [], None
        ran = build.run(nb, folder.name)
        problems = [(i, n) for i, intended, n in build.errors(ran) if not intended]
        status = "ok" if not problems else f"FAIL {problems}"
        bad += bool(problems)
        print(f"{folder.name:30s} {kind:9s} {status}", flush=True)
print("ALL OK" if not bad else f"{bad} notebook(s) failed")
