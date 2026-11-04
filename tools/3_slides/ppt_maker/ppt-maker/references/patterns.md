# Grid and slide patterns

Measured from the IND5003 Group 10 final deck (46 slides, Oct 2026) and built into `scripts/pptkit.py`.

## The grid

- Slide 13.333 x 7.5 in (16:9 wide). Blank layout; every element is a text box, a shape, a native chart or a native table.
- Margins 0.6 in left and right, so the content is 12.13 in wide (`M`, `CW`).
- Title at y 0.45. Content starts at y 1.65 under a one-line title, or about 2.2 under a two-line title or a takeaway line (`title()` returns the y to use). Content ends at y 6.75.
- Footer row at y 6.98: a short source on the left, the speaker tag and page number on the right.
- Columns: two panels of about 5.96 in with a 0.2 to 0.25 in gap; three of about 3.9 in. A chart with a side column uses about 7.6 in for the chart and 4.4 in for the side.
- Text boxes have zero inner margin, so text lines up with shapes and rules at the same x.
- Type sizes come from `SIZES[format]` (see SKILL.md). Box heights are computed from the font size, so a bigger scale does not clip.
- Cards have a rounded corner of about 0.1 in, no outline, no shadow.

## Patterns

Each pattern is a method on `Deck`. All take `notes=`, `speaker=`, `seconds=`; most take `source=` for the one-line source.

| Pattern | Looks like | Use it for |
|---|---|---|
| `cover(title, course, group, members, image)` | cover colour; logo and course line top left (centered when `align="center"`); group; big title; a rule; names with IDs; optional photo on the right 42% (or full-bleed under a veil when centered) | the title slide. Nothing else on it |
| `questions(title, questions, steps, steps_title)` | 2 to 4 question cards, then a numbered strip of approach steps | research questions and approach; an agenda |
| `findings(title, tiles)` | 2 to 4 tiles: heading, one big number, one or two sentences (3 tiles sit in one row; long numbers shrink to one line) | key findings, the answers before the details |
| `chart_stats(title, draw, stats, sub, aside)` | chart on the left two thirds, 2 or 3 big numbers (or a short text) on the right | most result slides: one chart, its reading in numbers |
| `photo(title, image, text, stats, side, caption, source)` | a photo filling one half edge to edge; title, short text and numbers on the other half | introducing the place, product, people or data source, with its key numbers |
| `full_photo(title, image, sub, credit)` | full-bleed photo with the title on a tinted band | an opener after the title, a section break, a closing image |
| `panels(title, panels)` | 2 or 3 columns, each with a numbered heading over a rule, a figure, small stats and a short text | before and after, method steps side by side, two related results |
| `table_slide(title, rows, highlight, below, stats)` | native table (dark header, quiet rows, tinted key cells), a one-line reading, optional numbers on the right | model comparisons, scores by period, data snippets |
| `cards(title, cards, cols)` | grid of cards: heading, optional value, text; card height follows the content, a short block sits a little above the middle | requirements, checks, options, a pipeline in steps |
| `two_lists(title, left, right)` | two cards with numbered points | recommendations and limitations; pros and cons |
| `conclusion(title, rows, hero)` | label-and-sentence rows on the left, one solid hero card with the key number on the right | the conclusion |
| `section(title, items)` | cover colour, a title and up to four rows of what comes next | a divider between parts; the appendix divider |
| `thanks(line, subtitle, members_line, course, image)` | cover colour, a big "Thank you", the title, the names, the logo and course line | the last slide of the talk, before the appendix |

`Deck(theme, fmt, align="left"|"center", tone="soft"|"regular"|"hard", logo=path, corner_logo=False)` sets these for the whole deck. With a logo, the cover and thank-you slides show it; `corner_logo=True` also puts a small one at the left of every footer.

Building blocks, when a slide needs its own layout: `flow` (boxes with arrows), `text` (supports `**bold**` runs and per-paragraph dicts), `rect` (`opacity=` for a veil), `oval`, `line`, `picture` (fits without cropping), `photo_fill` (fills and crops, with `focus`), `logo_mark`, `stat` (big number plus label), `panel_head` (numbered heading with a rule), `steps` (numbered strip), `line_chart`, `bar_chart`, `table`.

## Visual devices beyond charts

A deck made only of charts and cards looks thin. When the content is a process, a comparison or a plan, draw it:

| Content | Device | How |
|---|---|---|
| a pipeline, a cause and effect, problem to solution | flow of 3 to 5 boxes with arrows | `flow(slide, y, [(head, text), ...], fills={2: theme fill})` |
| options against criteria | a matrix table with short ratings (Strong, Partial, No) and the best cell tinted | `table(..., highlight={(r, c)})` |
| a plan over time | a numbered strip or a timeline of bars | `steps()`; or `rect` bars on a month or year axis |
| before and after | two stat tiles joined by "→" | `stat()` twice, or one tile with "0.06 → 0.84" |
| parts of a whole | a ranked horizontal bar chart | `bar_chart(..., horizontal=True)` |
| a place, product or data source | a real photo with its numbers | `photo()` |

Pick the device that matches how the speaker would explain it with their hands. Keep it on the same grid and colours.

## Patterns from the model deck that are worth copying

- **Stat tile.** A big number in the accent colour with a three-to-eight-word label under it ("17.02 m / our forecast for 2027"). Put the label in plain words, not a variable name.
- **"What we saw. So we decided."** A two-paragraph text under a figure, each starting with a bold lead-in. It turns a chart into a decision without a bullet list.
- **Numbered panels.** "1  Look", "2  Split and check" over a thin rule in the theme's `rule` colour. Good for showing a method in order on one slide.
- **Timeline of splits.** For train, validate and test windows: rows of bars in `card2` (training), `highlight` (scored) and `fill` (held out or forecast), with a small legend. Draw it with `rect` and `text` on a year axis.
- **Before and after.** Two numbers joined by an arrow in a stat tile ("0.06 → 0.84") with what was measured under it. Use an arrow only here, where it means "changed to".
- **Tinted cells.** In a comparison table, tint the cells where the model beats the benchmark, and say so in the one-line reading under the table.
- **Appendix with owners.** After the thank-you slide, a divider, then appendix slides (A1, A2, ...) whose notes start with "Not in the video. Owner: Name." and name the source.

## Charts

- Native first. `line_chart` takes `{name: values}` with `None` for gaps (for example actuals that stop and a forecast that starts), `dashed=` for interval bounds, `label_every=` to thin monthly labels, `number_format=`.
- `bar_chart` shows value labels, `horizontal=True` for ranked categories (it puts the first category on top), `point_colors={index: hex}` to mark one bar.
- The first series colour is for the main data, the second for the comparison (forecast, benchmark, plan). Grey (`series[2]`) is for context.
- Keep the legend short, or drop it and label lines directly with a small text box at the line's end.
- A shaded period (for example a pandemic gap or a forecast window) can be a `rect` in `card` or `card2` added before the chart, so it sits behind it. The chart and plot area must then have no fill, and the rectangle must be lined up with the axis by hand. Check both in the render. If that is fiddly, an annotation text next to the period is enough.
- Matplotlib figures: same font (the theme's body font), the theme's `series` colours, tick labels at least the format's label size when the figure fills its box, no chart title inside the image (the slide title does that job), and a transparent or `bg` background.
