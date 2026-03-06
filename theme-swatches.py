#!/usr/bin/env python
# coding: utf-8

import json
import seaborn as sns
from os import listdir, path, mkdir
import matplotlib.pyplot as plt
from PIL import Image

# check if directory "swatches" exists and if not, create it
if not path.exists('swatches'):
    os.mkdir('swatches')

def invert_hex(h):
    """
    Take a hexadecimal color and return it's inverse.

    Parameters:
    h (str): hexadecimal color

    Returns:
    h_inv (str): inverted hexadecimal color

    Examples:
    >>> invert_hex('#000000')
    #FFFFFF
    >>> invert_hex('##E0E0E0')
    #1F1F1F
    """
    h_inv = "#{:02X}{:02X}{:02X}".format(*(255-int(h[i:i+2], 16) for i in (1,3,5)))
    return h_inv

def draw_swatch(colors,ax):
    #for color in colors:
    #    sns.palplot(color)
    return sns.palplot(colors)

# Initialize seaborn
sns.set()

# Loop through all themes, drawing a swatch for each theme
for theme_file in listdir('themes'):
    with open('themes/' + theme_file) as th:
        # load theme
        theme = json.load(th)
        # extract theme name and delete
        theme_name = theme['name']
        del(theme['name'])
        # extract theme description and delete
        theme_description = theme['description']
        del(theme['description'])

		# Draw swatch
        sns.palplot(theme.values())

		# Add title to swatch
        plt.title(theme_name)
        # Add key and hexadecimal color
        for i, key in enumerate(theme):
            plt.text(
                i, 0.2,
                key+'\n'+theme[key],
                ha='center',
                va='bottom',
                color=invert_hex(theme[key]),
                fontsize=7
            )
        plt.tight_layout()
        plt.savefig('swatches/'+theme_name+'.png')

# read in swatches
swatches = [Image.open('swatches/'+swf) for swf in listdir('swatches')]
# extract widths and heights
widths, heights = zip(*(sw.size for sw in swatches))
# compute dimensions of new image
max_width = max(widths)
total_height = sum(heights)

# create composite image
swatches_im = Image.new('RGB', (max_width, total_height))
y_offset = 0
for sw in swatches:
    swatches_im.paste(sw, (0,y_offset))
    y_offset += sw.size[1]
swatches_im.save('theme_swatches.png')
