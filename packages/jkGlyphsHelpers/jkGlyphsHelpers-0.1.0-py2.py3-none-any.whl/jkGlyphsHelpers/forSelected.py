from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from GlyphsApp import Glyphs

if TYPE_CHECKING:
    from GlyphsApp import GSFont


def forAllLayersOfSelectedGlyphs(
    call_function: Callable, font: GSFont | None = None, **kwargs
) -> None:
    """
    Call a function for each layer of each selected glyph in the supplied font, passing
    the layer and any keyword arguments. If font is None, the function will be called
    for the currently active Glyphs file.
    """
    if font is None:
        font = Glyphs.font

    font.disableUpdateInterface()
    for selected_layer in font.selectedLayers:
        glyph = selected_layer.parent
        for layer in glyph.layers:
            call_function(layer, **kwargs)
    font.enableUpdateInterface()


def forSelectedLayers(
    call_function: Callable, font: GSFont | None = None, **kwargs
) -> None:
    """
    Call a function for each selected layer of the supplied font, passing the layer and
    any keyword arguments. If font is None, the function will be called for the
    currently active Glyphs file.
    """
    if font is None:
        font = Glyphs.font

    font.disableUpdateInterface()
    for selected_layer in font.selectedLayers:
        call_function(selected_layer, **kwargs)
    font.enableUpdateInterface()
