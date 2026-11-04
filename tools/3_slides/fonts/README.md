# DejaVu fonts

The course decks set code in **DejaVu Sans Mono**, so that code is monospaced and the PDF looks the same on any machine. The two font files in this folder are:

- `DejaVuSansMono.ttf`
- `DejaVuSansMono-Bold.ttf`

Source: DejaVu Fonts, release 2.37, https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37

Licence: the DejaVu fonts are free software under a permissive licence derived from the Bitstream Vera Fonts Copyright (see the `LICENSE` file in the release). They may be redistributed and embedded in documents.

`tools/3_slides/ppt_maker/ppt-maker/scripts/render.py` was patched to look in this folder first when it prepares the LibreOffice font profile, so `deck.pdf` embeds DejaVu Sans Mono. The deck `.pptx` files name the font; if PowerPoint on another machine does not have it installed, PowerPoint substitutes a monospace font, which is acceptable for editing.
