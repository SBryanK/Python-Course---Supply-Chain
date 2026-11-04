# Python for Supply Chain

A 10-session beginner Python course for one learner, Michella (16 Nov to 17 Dec 2026, Google Colab).

Read first:
- `PLAN.md`: the build spec (numbers, sessions, style rules).
- `PROGRESS.md`: what is built, where it is, upload dates. Update it when status changes.
- `tools/README.md`: the build scripts and how to run them.

Rules:
- Keep the root clean: only `README.md`, `PLAN.md`, `PROGRESS.md`, `CLAUDE.md` and the deliverable folders (`sessions/`, `course_home/`, `data/`).
- Every build or check script goes in `tools/<n>_<part>/`. No `_tools`, `_review`, `_verify`, `_arsip`, scratch or one-off folders. Delete one-off scripts after use.
- No venvs or caches in the repo. The venv lives at `~/.venvs/python-course`.
- `teacher_only/` is local only (the repo is public). Never commit it.
- Do not edit `README.md`; the owner maintains it.
- Overwrite files in place. No `v2` or `final` copies.
