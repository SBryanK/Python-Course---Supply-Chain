---
name: ppt-maker
description: Build or refactor PowerPoint decks (.pptx plus PDF and speaker notes) that look clean, natural and human-made, never "AI-ish". It reviews the content critically, checks and enriches it with outside sources, finds openly licensed photos online, shortlists five themes from a 14-theme library (soft or hard tone, left or centered), previews three slides in each, then builds an editable deck in Proxima Nova from a rerunnable Python script, with the NUS logo for NUS work. Use it whenever the user wants slides, a deck, a ppt or pptx, a presentation, "bikin slide", "buat presentasi", "rapikan ppt", "remake/redesign this deck", "too texty", "too AI", a final project presentation, a recorded video presentation, a class presentation, a pitch, a business or consulting deck, a fun or workshop deck, or a deck to be read. Works from scratch (notes, report, notebook, brief, data) or from an existing .pptx. Prefer it over the generic pptx skill whenever design, flow, images or speaker notes matter.
---

# ppt-maker

Make decks that a careful student or consultant would make by hand. Each slide carries one message and a title that says the finding. The evidence is a clear chart, a real photo or a few big numbers, and the reasoning goes in the speaker notes rather than on the slide.

The model deck is the IND5003 Group 10 final presentation (Oct 2026), described in `references/patterns.md`. What made it work came from its owner's corrections, collected under "Natural, not AI-ish" below.

Talk to the user in the language they write in. Write slides and notes in the language of the course or audience (English unless told otherwise).

## Files in this skill

| File | Use |
|---|---|
| `assets/themes.json` | the 14 themes (roles, colours, chart colours). Source of truth for all scripts |
| `assets/logos/nus_crest.png`, `assets/images/nus_campus.jpg` | NUS crest for every NUS deck; NUS signage photo (low resolution) |
| `references/themes.md` | what each theme suits, tones, alignment, how to shortlist five, fonts |
| `references/patterns.md` | the grid, type scale and every slide pattern, with when to use it |
| `references/flows.md` | slide orders for each kind of presentation; titles; speaker notes |
| `references/sources.md` | reviewing content, searching outside sources, finding and placing images, credits |
| `scripts/pptkit.py` | the drawing kit: `Deck(theme, fmt, align, tone, logo)` with patterns `cover`, `questions`, `findings`, `chart_stats`, `photo`, `full_photo`, `panels`, `table_slide`, `cards`, `two_lists`, `conclusion`, `section`, `thanks`, plus `line_chart`, `bar_chart`, `table`, `picture`, `photo_fill`, `flow`, `stat`, `steps`, `notes`, `footer`, `clean_copy` |
| `scripts/inventory.py deck.pptx` | read an existing deck: shapes, positions, sizes, colours, notes |
| `scripts/fetch_image.py search/preview/get` | find openly licensed photos (Wikimedia Commons, Openverse); download only with permission; record credits |
| `scripts/preview_themes.py spec.json --themes "A,B:hard,C:soft,E:center,I" --out preview.pptx` | the same three slides in five variants, one contact-sheet row each |
| `scripts/new_deck.py --theme A --tone regular --align left --logo nus --format video --out build_x.py --deck-name X` | writes a self-contained build script (kit, theme, logo in `assets/`, skeleton) |
| `scripts/render.py deck.pptx` | PDF with Proxima Nova embedded, page images, contact sheets, font check |
| `scripts/audit.py deck.pptx --format video --fonts "Proxima Nova"` | size floor, overflow, overlaps, off-slide shapes, word counts, filler words, notes time per speaker |

Python: any interpreter with `python-pptx`, `lxml` and `pillow`. If none has them, make a venv in the scratchpad (`python3 -m venv pv && pv/bin/pip install python-pptx pillow`). Do not install into a project's environment without asking. Never name a script after a standard-library module (`inspect.py`, `copy.py`), because it breaks imports. Rendering needs LibreOffice (`soffice`) and poppler (`pdftoppm`, `pdffonts`).

## Workflow

### 1. Intake: read first, then ask only what the files cannot answer

Read everything the user gives before asking anything: the old deck (`inventory.py`, then `render.py` to see it), the report, notebook outputs, brief and rubric, data. Then write down:
- **Purpose and audience**: who watches or reads it, and what they must take away.
- **Nature**: academic group project, individual class talk, business or consulting, pitch, fun or workshop, or read-only.
- **Format**: recorded video, live in a room, or read without a speaker. This sets the type scale (`video`, `live`, `read`).
- **Limits**: duration, slide count, appendix rules, speakers, required sections. Quote the source of each limit. Never assume extra slides are allowed.
- **Must-keep content**: numbers, figures and conclusions, each with its source file.

Ask in one round (AskUserQuestion when available) only what is still open:
- nature and format;
- the one to three messages that matter most and where they should land;
- duration and speaker split;
- the user's own photos or logos, and whether you may search online for openly licensed photos;
- which outside sources would make the content clearer (offer specific ones);
- for a refactor, what must not change.

### 2. Review the content, then research the gaps

Review the material critically (`references/sources.md`, "Evaluating the content"):
- Is each message clear?
- Is each claim supported?
- What is outdated, inconsistent or overstated?
- What context does the audience lack?

Use web search to check facts and fill the gaps with primary sources. The user's verified results win over web figures. Report any conflict instead of resolving it yourself.

Then write the outline in chat. For each slide, give:
- its one message (which becomes the title);
- the evidence (chart, table, photo or numbers) with its source;
- the speaker.

Follow `references/flows.md`. List the gaps you found and the outside facts you plan to add, so the user can approve them. For a refactor, say per slide whether it is kept, split, merged, moved to the appendix or cut, and why.

Verify every number against its source before it goes on a slide. If a number cannot be traced, say so and leave it out. Never claim you checked a file or page you could not open.

### 3. Images

Gather images by the order in `references/sources.md`: the user's own, then bundled assets, then screenshots, then openly licensed photos.
- `fetch_image.py search` needs no permission.
- Before `preview` or `get`, ask the user, naming the files, the source, the licence and the size.
- Every downloaded photo gets its credit on the slide that uses it.
- A photo must show the subject. Decorative stock photos are out.

### 4. Theme shortlist and preview: five variants, three slides each

Pick five variants from `references/themes.md` that fit the content and nature, and say in one line each why each fits. A variant is a theme plus a tone and an alignment, for example `A`, `A:hard`, `B:soft:center`, `C:soft`, `I:hard:center`.
- Mix them so the user can compare: at least one soft and one hard tone, and at least one centered variant.
- For Bryan's NUS work, include theme A and use the NUS crest (`"logo": "nus"` in the spec).

Write `spec.json` with real content for three slides:
1. the opening (with the logo and a cover photo if there is one);
2. the questions and approach, or the agenda;
3. one real result slide with its real chart and numbers.

Run `preview_themes.py`. Look at the contact sheet yourself and fix what is broken. Then show it to the user, with sample speaker notes for the three slides.

Before asking, decide internally, from what the deck is for, which alignment and tone you would recommend:
- left for analytic, data-heavy or read-only decks;
- center for openers, pitches, fun talks and decks with few words;
- hard tones for big rooms and pitches, soft tones for calm or printed decks.

Then ask the style choices as separate questions in one round (AskUserQuestion when available), each with your recommendation first and a one-line reason:
1. **Theme**: the five previewed variants.
2. **Alignment**: rata kiri (left) or rata tengah (center).
3. **Tone**: soft, regular or hard.

Alignment and tone apply to any theme, so the user can combine them freely, for example theme C with center alignment and a hard tone. If they want to see a combination before deciding, rerun `preview_themes.py` with just that entry (for example `C:hard:center`, or `A:left,A:center` side by side). Also ask what to change in density and font size.

Build the full deck only after the user picks.

### 5. Build the deck from a script

Run `new_deck.py` with the chosen theme, tone, alignment, logo and format. Write `build_<deck>.py` where the deck should live (the project folder when it belongs to a project). Replace the skeleton `build()` with the real slides, using the patterns in `references/patterns.md`.

Keep the script readable: plain calls, short names, few comments. When no pattern fits, compose from the kit's primitives on the same grid rather than inventing a new visual language. Use the visual devices in `references/patterns.md` (flows, rating matrices, timelines, before and after) wherever the content is a process, a comparison or a plan; a deck of only charts and cards looks thin.

- **Font.** Every theme uses Proxima Nova for headings and body; keep it. On a Windows machine, Proxima Nova must be embedded (PowerPoint: File, Options, Save, embed fonts) or the fallback Montserrat used. Say this when the deck goes to a team.
- **Charts and tables.** Keep them native so the team can edit them. Use a picture only for photos, screenshots, diagrams, or chart types PowerPoint cannot draw (heatmaps, dendrograms, maps). Redraw those with matplotlib in Proxima Nova and the theme's `series` colours, at the format's label size or larger, and keep the script that draws them.
- **Speaker notes.** When the deck will be presented, use `notes=` with `speaker=` and `seconds=`, in the voice of `references/flows.md`. A read-only deck gets no notes; its slides carry full sentences instead.
- **Speaker names.** They go only in the removable `speaker_tag`. `clean_copy(src, dst)` makes a copy without them, only when asked.

### 6. Check, then check again

Run `render.py` and `audit.py`, then look at every page image, not just the warnings. Look for:
- clipped or overflowing text, or a title that wraps into the content;
- labels on top of lines, or chart labels unreadable at the format's size;
- a cropped photo that lost its subject;
- colours used without meaning, or empty cards;
- read-only slides that need a speaker to make sense.

Fix everything in the build script and rerun. Two rounds are normal. Then confirm:
- the timing per speaker fits the limit, at 130 words a minute;
- the PDF embeds Proxima Nova (`render.py` warns otherwise);
- chart XML stays valid (see the comment in `pptkit._skip_labels` if you touch it).

### 7. Deliver

Give the user the `.pptx`, the `.pdf` and the build script, and say in a few lines:
- what changed;
- which facts and images came from outside, with their sources and licences;
- what you could not verify. The render is LibreOffice, not PowerPoint itself;
- what they must do themselves: embed or install the font for Windows teammates, record, upload.

Do not create extra markdown files unless asked. The notes live in the deck.

Once the user edits the deck by hand, the build script no longer matches it. Say so. From then on, edit the .pptx in place (python-pptx on the existing file, or the user in PowerPoint) instead of rerunning the script over their edits. A revision overwrites the same file; make `v2` copies only when the user asks for one.

## Type scale and density by format

Each level is clearly bigger than the one below it, so the eye finds the title, then the number, then the detail. Sizes are in points.

| | video (recorded, 1080p) | live (projected) | read (no speaker) |
|---|---|---|---|
| cover title | 54 | 60 | 44 |
| slide title | 32 | 36 | 28 |
| takeaway line under the title | 20 | 22 | 17 |
| panel or card heading | 18 | 20 | 15 |
| body | 14 | 18 | 12 |
| chart and tile labels (floor) | 12 | 14 | 10 |
| big number | 40 | 48 | 32 |
| hero number | 56 | 64 | 44 |
| source line | 10.5 | 11 | 9 |
| visible words per slide, aim | 70 or fewer | 45 or fewer | up to 170 |

These live in `pptkit.SIZES`. Nothing except the source line, the page number and the speaker tag goes under the floor. If text does not fit, cut words or split the slide; do not shrink it. A rubric that caps the slide count is the one case for compressing, and then the appendix takes the overflow.

## Alignment and tone

- **Left alignment** (the default) suits analytic decks: titles, numbers and text start on the same left edge.
- **Center alignment** (`align="center"`) suits openers, closers, fun talks, pitches and decks with few words. It centers titles, cover and closing slides, tiles, cards and stat numbers.
- **Long text stays left-aligned in every mode.** Lists, tables, conclusion rows and paragraphs longer than two lines are hard to read centered.
- **Tone** changes how strong the colours are, not which colours they are:
  - `soft`: light tinted covers, pale cards; calm and friendly;
  - `regular`: the theme as designed;
  - `hard`: dark solid covers and stronger cards; bold, high contrast, good for live rooms.

  `toned()` keeps the text readable on every fill by checking contrast.

## Natural, not AI-ish

These are the corrections the deck's owner made when an earlier deck looked machine-made. Apply them to every deck.

- **Opening.** The title slide holds the title, the course or occasion, the group or presenter, names with IDs if required, and the institution's logo. No slogan, no tagline, no chart, no dataset description. A cover photo is fine if it shows the subject.
- **Questions, then answers.** Introduce the questions and the approach, then answer them one by one, each section opening with its short answer. A key-findings slide right after the agenda is fine when the brief asks for findings first.
- **Titles say something.** Use a finding ("Recovery followed reopening dates") or a plain description. No question titles, and no empty framing ("Four questions, answered with one workflow").
- **No label prefixes or kickers.** No "Q1(a) ·", "Step 3", "Our tour", "The TA's advice", no pills or dots above titles. Mapping to the brief goes in the notes or the appendix.
- **No repeated long footer.** One short source line where a figure needs it, and full references on one appendix slide.
- **Advice becomes the group's own work.** Never write "the TA suggested" on slides or in notes. Keep real citations.
- **Hierarchy in three levels.** A big title, the takeaway one level down, then the details. One focal element per slide (a chart, a photo or one big number) where the eye lands first.
- **Charts explain themselves quietly.** A short legend or direct labels, an annotation beside the thing it explains, the rest in the notes. Keep actuals, forecasts and mixed years visibly different.
- **Real images only.** Each image shows what the slide is about, with its credit. No decorative stock, no clip art, no emoji.
- **Honest numbers.** Every number traceable, from the user's files or a cited source. Never call a partial year a full year, or a sum of monthly bounds an annual interval without saying what it is.
- **Plain words.** No "delve", "leverage", "seamless", "unlock", "journey", "game-changer", "In conclusion", no exclamation marks. Write short sentences that a speaker whose first language is not English can say comfortably.
- **Not too texty.** If a slide needs a paragraph, the paragraph belongs in the notes, or the slide should become two.
- **Close properly.** Recommendations and limitations, a conclusion, then a thank-you slide with the logo. The appendix comes after, each slide naming its owner in the notes.
- **Editable.** Any text, number, chart or table can be changed in PowerPoint. Never flatten a slide into an image.

## Refactoring an existing deck

1. Run `inventory.py` and `render.py`. Read every slide image and every note.
2. Diagnose in chat. Separate content problems (unclear message, unsupported or outdated number, wrong order) from design problems (density, size floor, AI-ish tells, colours, fonts, non-native charts, missing logo or images).
3. Keep the analysis, numbers and wording the team agreed on; change the look, hierarchy, flow, images and notes. If a change would touch the method or a conclusion, flag it and ask first. A redesign is not permission to change the content.
4. Follow steps 3 to 7 above. Overwrite in place unless the user wants the original kept or names a new location.
