from nbkit import md

cells = [
    md("""# Session 10: Showtime

**Question for today:** can you explain it like an analyst?"""),

    md("""## Before you start

- [ ] My slides open and I know the order.
- [ ] My answer comes first, in the first 30 seconds.
- [ ] I will say numbers simply.
- [ ] I will not read the slides.

Your talk is 5 minutes: about 1 minute for the question, 2 for the finding and evidence, 1 for the recommendation, and 1 spare."""),

    md("""## Questions to expect

- Walk me through your project in 2 minutes.
- Why did you remove those rows?
- What would you do with more time?
- How did you check your numbers?

*Notes for my answers:*"""),

    md("""## Feedback I received

*Two things I did well:*

*One thing to improve:*"""),

    md("""## Reflection review

We read your reflection together.

*What I want to remember:*"""),

    md("""## Course look-back: keep, stop, start

- **Keep:** what worked well in the course
- **Stop:** what did not help
- **Start:** what I want more of

*My answers:*"""),

    md("""## What next

Ideas for January (optional): deeper Power BI, more SQL lessons, VS Code, and git on the command line.

*What I want to do in the next 30 days:*"""),
]

SESSION = {"folder": "s10_showtime", "cells": cells, "expect": []}
