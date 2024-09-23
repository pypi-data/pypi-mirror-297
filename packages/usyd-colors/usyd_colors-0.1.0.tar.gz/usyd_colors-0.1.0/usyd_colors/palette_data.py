from usyd_colors.palettes import Palette, PaletteName
from typing import Dict

usyd_palettes: Dict[PaletteName, Palette] = {
    PaletteName.PRIMARY: Palette(['#424242', '#E64626', '#0148A4', '#FFB800', '#F1F1F1']),
    PaletteName.MODERN_DIVERGING: Palette(['#25584D', '#71A499', '#E0E0E0', '#FFAD8C', '#E74726']),
    PaletteName.EXTENDED: Palette(['#424242', '#E64626', '#0148A4', '#FFB800', '#007E3B', '#4E98D3', '#F79C72', '#FDCA90',
        '#FBF38D', '#BDDC96', '#00A485', '#68C6B6', '#91BDE5', '#B896C6', '#7F3F98', '#D6519D',
        '#F8B9CC', '#F9A134', '#7A2000', '#0A0A0A', '#F1F1F1'
    ]),
    PaletteName.SECONDARY: Palette(['#E64626', '#4E98D3', '#FFB800', '#00A485', '#B896C6']),
    PaletteName.PASTEL: Palette(['#FBF38D', '#F79C72', '#F8B9CC', '#B896C6', '#91BDE5', '#68C6B6', '#BDDC96']),
    PaletteName.COMPLEMENTARY_REGR: Palette(['#E64626', '#F79C72', '#7A2000', '#00A485', '#68C6B6']),
    PaletteName.COMPLEMENTARY_REBL: Palette(['#E64626', '#F79C72', '#FDCA90', '#0148A4', '#4E98D3', '#91BDE5']),
    PaletteName.BRIGHT: Palette(['#E64626', '#007E3B', '#BDDC96', '#91BDE5', '#4E98D3', '#F9A134', '#FFB800']),
    PaletteName.MUTED: Palette(['#91BDE5', '#FBF38D', '#F79C72']),
    PaletteName.TRAFFICLIGHT: Palette(['#00A485', '#FBF38D', '#E64626']),
    PaletteName.HEATMAP: Palette(['#00A485', '#FFFFFF', '#E64626']),
    PaletteName.FLAMETREE: Palette(['#FBF38D', '#F9A134', '#E64626', '#7A2000']),
    PaletteName.JACARANDA: Palette(['#F8B9CC', '#B896C6', '#4E98D3', '#0148A4']),
    PaletteName.HARBOUR: Palette(['#BDDC96', '#68C6B6', '#4E98D3', '#0148A4']),
    PaletteName.SANDSTONE: Palette(['#F8EFDD', '#FDCA90', '#7A2000', '#424242']),
    PaletteName.OCHRE: Palette(['#F8EFDD', '#FDCA90', '#F79C72', '#E64626']),
    PaletteName.GREYSCALE: Palette(['#424242', '#F1F1F1']),
    PaletteName.BLGRYE: Palette(['#0148A4', '#BDDC96', '#FBF38D']),
    PaletteName.BLOR: Palette(['#0148A4', '#F9A134', '#FBF38D']),
    PaletteName.DIVERGING_BLUE_RED: Palette(['#7A2000', '#E64626', '#F79C72', '#FFFFFF', '#91BDE5', '#4E98D3', '#0148A4']),
    PaletteName.DIVERGING_BLUE_ORANGE: Palette(['#F9A134', '#FFFFFF', '#0148A4'])
}