from __future__ import annotations
from GlyphsApp import Glyphs
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from GlyphsApp import GSFont


def forCurrentFont(call_function: Callable, **kwargs) -> None:
    """
    Call a function for the currently active Glyphs file. Any keyword arguments are
    passed on to the function.
    """
    if Glyphs.font is None:
        return

    forFonts(call_function, [Glyphs.font], **kwargs)


def forFonts(
    call_function: Callable, fonts: List[GSFont] | None = None, **kwargs
) -> None:
    """
    Call a function for each font of the fonts list, passing the font and any keyword
    arguments. If `fonts` is None, the function will be called for each open Glyphs
    file.
    """
    if fonts is None:
        fonts = Glyphs.fonts

    for font in fonts:
        font.disableUpdateInterface()
        call_function(font, **kwargs)
        font.enableUpdateInterface()


def forAllGlyphs(call_function: Callable, font: GSFont | None = None, **kwargs) -> None:
    """
    Call a function for each glyph in the supplied font, passing the glyph and any
    keyword arguments. If `font` is None, the function will be called for the currently
    active Glyphs file.
    """
    if font is None:
        font = Glyphs.font

    font.disableUpdateInterface()
    for glyph in font.glyphs:
        call_function(glyph, **kwargs)
    font.enableUpdateInterface()


def forAllLayersOfAllGlyphs(
    call_function: Callable, font: GSFont | None = None, **kwargs
) -> None:
    """
    Call a function for each layer of each glyph in the supplied font, passing the layer
    and any keyword arguments. If `font` is None, the function will be called for the
    currently active Glyphs file.
    """
    if font is None:
        font = Glyphs.font

    font.disableUpdateInterface()
    for glyph in font.glyphs:
        for layer in glyph.layers:
            call_function(layer, **kwargs)
    font.enableUpdateInterface()
