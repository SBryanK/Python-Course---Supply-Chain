# Outside sources and images

## Evaluating the content (before any design)

Read the user's material as a critical reviewer, not a typist. For every slide-to-be, ask:
- Is the message clear in one sentence? If not, what is missing: a definition, a comparison, a number, a reason?
- Is each claim supported? By which file, figure or source?
- Is anything wrong, outdated, inconsistent between files, or stated more strongly than the evidence allows (a partial year called a year, an association called a cause)?
- Would the audience need context the material does not give (what a term means, why it matters, how big a number is compared with something familiar)?

Write the gaps down for the user with a suggested fix each. Mark what needs their decision. Do not silently rewrite their conclusions.

## Searching outside sources

Use web search (WebSearch, then WebFetch on the page) when the content needs:
- an official figure for context (a statistics office, a central bank, a ministry, a company's annual report);
- a definition or method from a textbook, standard or paper;
- a date, a name or an event that the deck states and should be checked;
- recent facts the user's files may not have.

Rules:
1. Prefer primary sources: government statistics (SingStat, data.gov.sg, STB, MAS), international bodies (UN, World Bank, IMF, OECD), official company filings, peer-reviewed papers, the course textbook and slides. Use news only for events, and say so.
2. Open the page and read the number in context before using it. Note the exact title, publisher, date, URL and access date.
3. The user's own verified results win. If a web figure differs from a project number, do not replace it: tell the user both, with sources, and ask.
4. Put a short source line on the slide that uses an outside fact ("Source: SingStat, Table M550001, accessed 31 Oct 2026"). Collect full references on one appendix slide.
5. Say in chat which facts came from outside sources, so the user can check them. Never present a guess as a found fact; if the search finds nothing solid, say so.
6. Searching is not a download. Reading web pages to check facts needs no permission. Saving files does.

## Images

Good images show the subject: the place, the product, the people, the data source, the object being measured. Decorative stock photos (handshakes, light bulbs, abstract networks) make a deck look generated. Use them never.

Where images come from, in this order:
1. **The user's own**: photos, screenshots, logos, figures from their notebook or report.
2. **Bundled assets**: `assets/logos/nus_crest.png` (NUS crest, transparent, 668 x 852) for any NUS deck; `assets/images/nus_campus.jpg` (NUS signage photo, only 768 x 432, so use it on half a slide or under a veil, never full-bleed sharp).
3. **Screenshots of a data source or tool**, when they help explain where data came from.
4. **Openly licensed photos online**, through `scripts/fetch_image.py`:
   - `search "query"`: lists candidates from Wikimedia Commons and Openverse with size, licence and author. It downloads nothing, so it needs no permission.
   - Before `preview` (thumbnails) or `get` (the full photo), ask the user. Name the file or files, the source site, the licence and the approximate size: thumbnails about 30 to 60 KB each; a full photo at 1920 px is about 0.3 to 1 MB. Download only what they approve, into the deck's `assets` folder.
   - `get` writes the credit to `credits.json`. Put that credit on the slide's source line ("Photo: Moheen Reeyad, CC BY-SA 4.0, Wikimedia Commons").
   - If the user asks for test downloads to be deleted, delete the files and anything built from them (decks, renders) as soon as the check is done.
5. **Generated images** (an image-generation tool, if the session has one), only when the user asks, and only for illustrations, never for something presented as real.

Never download from sites whose licence is unclear, never strip a watermark, and never use a logo of an organisation the deck is not from or about.

## Placing images

| Need | Pattern |
|---|---|
| set the scene on the title slide | `cover(..., image=)`: right 42% with left alignment, full-bleed under a veil with center alignment |
| show the subject next to its numbers | `photo(title, image, text, stats, side=)`: half the slide, edge to edge |
| a section break or a closing image | `full_photo(title, image, sub, credit=)` |
| a figure or screenshot inside a slide | `picture()` (fits without cropping) inside `panels` or `chart_stats` |
| the institution's logo | `Deck(..., logo=path)`: cover and thank-you slides; `corner_logo=True` also puts a small one in every footer |

`image_focus=(x, y)` (0 to 1) keeps the important part of a cropped photo in view, for example `(0.8, 0.5)` when the subject is on the right. Check every cropped photo in the render.
