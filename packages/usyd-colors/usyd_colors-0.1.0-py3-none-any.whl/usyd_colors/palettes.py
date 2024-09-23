from typing import List, Tuple
from enum import Enum


class Palette:
    def __init__(self, colors: List[str]) -> None:
        """
        Initialize a color palette.

        :param name: Name of the palette.
        :param colors: List of HEX color codes.
        """
        self.colors_hex = colors
        self.colors_rgb = [self.hex_to_rgb(c) for c in colors]

    def hex_colors(self) -> List[str]:
        """Return colors as HEX codes."""
        return self.colors_hex

    def rgb_colors(self) -> List[Tuple[float, float, float]]:
        """Return colors as RGB tuples."""
        return self.colors_rgb

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
        """Convert HEX to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore

    def matplotlib_colormap(self, continuous: bool = True):
        try:
            import matplotlib.colors as mcolors
        except ImportError:
            raise ImportError(
                "Matplotlib is not installed. Install it with `poetry install --extras matplotlib`"
            )
        if continuous:
            return mcolors.LinearSegmentedColormap.from_list('usyd_palette', self.colors_hex)
        else:
            return mcolors.ListedColormap(self.colors_hex)

class PaletteName(str, Enum):
    PRIMARY = 'primary'
    MODERN_DIVERGING = 'modern_diverging'
    EXTENDED = 'extended'
    SECONDARY = 'secondary'
    PASTEL = 'pastel'
    COMPLEMENTARY_REGR = 'complementary_ReGr'
    COMPLEMENTARY_REBL = 'complementary_ReBl'
    BRIGHT = 'bright'
    MUTED = 'muted'
    TRAFFICLIGHT = 'trafficlight'
    HEATMAP = 'heatmap'
    FLAMETREE = 'flametree'
    JACARANDA = 'jacaranda'
    HARBOUR = 'harbour'
    SANDSTONE = 'sandstone'
    OCHRE = 'ochre'
    GREYSCALE = 'greyscale'
    BLGRYE = 'BlGrYe'
    BLOR = 'BlOr'
    DIVERGING_BLUE_RED = 'diverging_blue_red'
    DIVERGING_BLUE_ORANGE = 'diverging_blue_orange'

def get_palette(name: PaletteName | str) -> Palette:
    """Retrieve a palette by name."""
    from usyd_colors.palette_data import usyd_palettes
    try:
        return usyd_palettes[name]  # type: ignore
    except KeyError:
        raise ValueError(f"Palette '{name}' not found. Available palettes: {list(usyd_palettes.keys())}")


if __name__ == '__main__':
    print(get_palette('primary'))
