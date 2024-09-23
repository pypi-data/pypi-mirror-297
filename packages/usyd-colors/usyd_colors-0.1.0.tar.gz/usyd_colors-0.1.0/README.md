# usyd_colors

A Python version of the University of Sydney's brand color palettes. Inspired by the wonderful package for R: https://github.com/Sydney-Informatics-Hub/usydColours/tree/master

## Installation

```bash
pip install usyd-colors
```

or

```bash
poetry add usyd-colors
```

## Usage

### 1. Get a palette
```python
from usyd_colors import get_palette

# Get the "primary" palette
primary_palette = get_palette("primary")

# Access and print the HEX colors
hex_colors = primary_palette.hex_colors()
print("HEX Colors in Primary Palette:", hex_colors)

# Access and print the RGB colors
rgb_colors = primary_palette.rgb_colors()
print("RGB Colors in Primary Palette:", rgb_colors)
```

outputs:
```
HEX Colors in Primary Palette: ['#424242', '#E64626', '#0148A4', '#FFB800', '#F1F1F1']

RGB Colors in Primary Palette: [(0.25882352941176473, 0.25882352941176473, 0.25882352941176473), (0.9019607843137255, 0.27450980392156865, 0.14901960784313725), (0.00392156862745098, 0.2823529411764706, 0.6431372549019608), (1.0, 0.7215686274509804, 0.0), (0.9450980392156862, 0.9450980392156862, 0.9450980392156862)]
```

### 2. Use with matplotlib

```python
import numpy as np
import matplotlib.pyplot as plt
from usyd_colors import get_palette

# Get the "primary" palette
primary_palette = get_palette('primary')

# Generate some random data for a heatmap
data = np.random.rand(10, 10)

# Use the palette to create a Matplotlib colormap
colormap = primary_palette.matplotlib_colormap()

# Plot the heatmap using the colormap
plt.figure(figsize=(6, 6))
plt.imshow(data, cmap=colormap)
plt.colorbar()
plt.title('Heatmap with USYD Primary Palette Colormap', fontsize=16)
plt.show()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
