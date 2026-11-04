# Themes

The colour and font values are in `assets/themes.json`; this file says when to use each theme. Every theme has the same roles, so any pattern works in any theme:

| Role | Used for |
|---|---|
| `bg` | slide background |
| `card`, `card2` | rounded panels; `card2` is the quieter one (limitations, alternate table rows) |
| `ink`, `muted` | main text; labels, sources, axis text |
| `accent` | coloured text: card headings, big numbers (dark enough to read on `bg` and `card`) |
| `fill`, `on_fill` | solid fills (numbered circles, the hero card) and the text on them |
| `rule` | thin lines under panel headings, highlight lines in charts |
| `highlight` | tinted table cells that matter |
| `cover_bg`, `cover_ink` | title, section and thank-you slides |
| `series` | chart colours in order: the first is the main series (usually the actual data) |

## The library

| Id | Theme | Personality font (only if asked) | Suits | Avoid for |
|---|---|---|---|---|
| A | Warm gold | Proxima Nova | NUS academic work, group projects, analytics with a friendly tone (Bryan's default for NUS) | dark rooms (the yellow cover glares) |
| B | NUS blue and orange | Aptos | formal NUS or faculty talks, proposals, official reviews | playful topics |
| C | Earthy tourism | Georgia / Gill Sans MT | tourism, travel, culture, food, hospitality, storytelling | dense quantitative tables |
| D | Consulting minimal | Aptos | business cases, strategy, executive summaries, recommendations | fun events |
| E | Navy editorial | Georgia / Franklin Gothic Book | finance, economics, investment theses, policy briefs | young or casual audiences |
| F | Clinical clean | Calibri | health, life science, public policy, surveys, lab results | brand or marketing pitches |
| G | Data dark | Aptos | tech, AI, IoT, software demos, live talks in dark rooms | printing and read-only decks |
| H | Forest sustainability | Gill Sans MT | ESG, environment, energy, agriculture, green supply chains | finance-heavy decks |
| I | Singapore red | Franklin Gothic Demi / Book | Singapore topics, public sector, national data, urban planning | topics where red reads as alarm (losses, risk) |
| J | Playful pastel | Century Gothic / Trebuchet MS | fun talks, workshops, team introductions, student events | graded analytics, formal reviews |
| K | Startup pitch | Arial Black / Arial | pitches, business plans, entrepreneurship, product launches | academic method talks |
| L | Maritime blue | Aptos | logistics, procurement, operations, shipping, supply chain | warm, human topics |
| M | Swiss grid | Arial | design, quantitative research with few words, big-number talks | text-heavy decks |
| N | Research poster | Rockwell / Georgia | seminars, literature reviews, humanities, history, qualitative work | dashboards of many numbers |

## Tones and alignment

Each theme comes in three tones through `toned(theme, tone)`:
- **soft**: the cover becomes a light tint of the theme's card colour, and cards and fills fade toward the page. Calm, friendly, good for read-only decks and small rooms.
- **regular**: as designed.
- **hard**: a dark solid cover (theme A turns warm brown; light covers turn to the ink colour; dark covers go darker), stronger cards and highlights. Bold, high contrast, good for big rooms and pitches.

Text colours on covers and fills are re-chosen for contrast automatically.

Alignment is `left` (rata kiri, the default) or `center` (rata tengah). Themes J and K default to center. Any theme can be centered. Alignment and tone are always offered to the user as their own choices next to the theme, with a recommendation that follows from the content (see SKILL.md, step 4).

## How to shortlist five

1. Start from the topic (column "Suits"), then the nature: academic group project, business, pitch, fun, read-only.
2. Drop themes in "Avoid for". Drop G for anything that will be printed or read on paper.
3. Keep variety in the five: at most two serif-heading themes (C, E, N), at most one dark theme (G), and one safe formal option (A, B or D).
4. If the user has a known favourite or an institution colour, include it.
5. Mix tones and alignment across the five: at least one soft, one hard and one centered variant.
6. Say in one line per variant why it fits this content.

Example for a tourism forecast at NUS: `A` (the user's NUS default), `A:hard` (the same in brown), `B:soft:center` (institutional, calm), `C:soft` (tourism), `I:hard:center` (Singapore data, bold).

## Fonts

Every theme uses **Proxima Nova** for headings and body (the user's standing choice), so themes differ by colour, tone and alignment. The `alt_head` and `alt_body` fields in `themes.json` (the "personality font" column) are only used when the user asks for a different font: pass them with `new_deck.py --head-font --body-font`.

- Office fonts (Aptos, Calibri, Georgia, Gill Sans MT, Franklin Gothic, Century Gothic, Rockwell, Trebuchet MS, Arial) come with Microsoft Office on Mac and Windows, so teammates see the same deck.
- Proxima Nova is installed on this Mac as a system asset font. It is not on Windows. For a team deck in theme A, either embed fonts when saving in PowerPoint (File, Options, Save, embed fonts) or use the fallback Montserrat, which is installed in `~/Library/Fonts`.
- `new_deck.py --head-font X --body-font Y` swaps fonts for one deck without touching the library.
- `render.py` copies the fonts it finds into a private LibreOffice profile so the PDF embeds them, and warns when a font was substituted. Always read that warning.

## Adding or changing a theme

Add an entry to `assets/themes.json` with every role above. Check that `accent` text on `bg` and on `card`, and `on_fill` on `fill`, have strong contrast (about 4.5:1 or better), and that the first two `series` colours are easy to tell apart in greyscale. Then run `preview_themes.py` with it before using it on a real deck.
