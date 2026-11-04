# Flows, titles and speaker notes

## Slide orders by nature

Adapt these to the brief; a rubric's required sections always win.

**Academic group project, recorded or live** (the model deck: 27 video slides in 10 minutes, then an appendix)
1. Title (names and IDs if required)
2. Research questions and approach (the method as a numbered strip)
3. Key findings, one tile per question (when the brief asks for findings first)
4. The data: sources, coverage, how the files were joined, one real snippet
5. Method slides in the order of the approach, each with one decision and its evidence
6. The answer to the main question (the forecast, the estimate, the decision)
7. The link the brief asks for (economy, policy, business value)
8. Section divider, then one slide per remaining question, each opening with its answer
9. Recommendations and limitations
10. Conclusion: what we found, what we learned
11. Thank you
12. Appendix divider, then A1, A2, ... (details, robustness checks, full tables, data sources and references)

**Individual class presentation**: title, the question and why it matters, background (one slide), two or three findings, what it means, limits, thank you.

**Business or consulting**: title; the answer (a recommendation in one sentence plus three reasons); situation and complication; one slide per reason with its evidence; risks and how to manage them; next steps with owners and dates; thank you; appendix.

**Pitch**: title, the problem (one person's story or one number), the solution, how it works, market size, business model, traction, competition, team, the ask, thank you.

**Fun or workshop**: title, what we will do today, three to five short parts (each with one picture or one number), something to try, thank you. Keep words even fewer than usual.

**Read-only deck** (submitted, read without a speaker): no speaker notes, so every slide must stand alone: a finding title, a one-line takeaway under it, the figure, and two or three full sentences that say how to read it and what it means. Sources on the slide. A short contents slide after the title helps a reader jump.

## Titles

- One line when possible, two at most. The title is the slide's message.
- Finding titles say what the evidence shows: "Countries group by holiday timing, not by region". Descriptive titles name the content when there is no finding yet: "Research questions and approach".
- Numbers in titles only when they are the point: "The pandemic cost 49–57 million arrivals".
- No question titles, no prefixes ("Q2 ·", "Step 4"), no labels like "Our tour" or "Deep dive".

## Speaker notes

Write the notes the speaker will actually say, in their voice: short sentences, first person plural for a group ("we"), plain words, no stage directions except the pointing cues.

Format:
```
BRYAN (about 25 seconds)
First, the data. [point: the three tables] We have arrivals by air, sea and land, from January 2008 to August 2026. ...
```
- The first line is the speaker in capitals and the time; `audit.py` reads it to add up time per speaker.
- `[point: ...]` tells the speaker where to move the mouse; it is not read aloud. One or two per slide.
- Open each slide with a transition from the last one ("But similar seasons did not mean similar recovery."), then read the figure ("Each dot is a country; the bar is the group average."), then the finding, then a bridge to the next slide when the speaker changes ("Galih will now show what one-off events did.").
- About 130 words a minute for a calm pace. A 25-second slide is about 55 words.
- Opening notes sound like students introducing their group ("Hi, we are Group 10: ..."), not like a narrator.
- Never: "As the TA suggested", "In this slide we will delve into", "It is important to note that". Advice from a TA or the brief is already the group's own work.
- Appendix notes: "Not in the video. Owner: Name." then what each number means and its source.

## When the deck must be recorded

- Check the brief's video rules (length, no speed-up, real voices) and the speaker split; time each part with `audit.py`.
- Total spoken words should leave about a minute of slack for slide changes and pauses. If it runs long, cut words, not speed.
