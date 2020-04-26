
"""
Annie Perkins Math Art Challenge.
https://twitter.com/anniek_p/status/1244220881347502080
Adapted from https://github.com/hackingmath/pygame_sketches/blob/master/binary_grid_challenge.py
by J. Salmon
Inkscape advice:
https://graphicdesign.stackexchange.com/questions/15450/remove-background-based-on-color-in-inkscape
April 13, 2020
"""
import matplotlib.pylab as plt
from mpmath import mp

from hitomezashi import make_hitomezashi, plot_hitomezashi

# random Seed
seed = 123456
# Saving activated:
saving = True

# Quantifzation level for colored images (n_qt = 2 is slow though)
# best pi 14? 25? 31? 34?
n_qt = 30

# Color Style:
# color_style = 'tab20'
color_style = 'nb'
# color_style = 'twilight_shifted'
# color_style = 'RdBu'
# color_style = 'twilight'
# color_style = 'viridis'
# color_style = 'Blues'
# color_style = 'PRGn'
# color_style = 'Dark2'
# color_style = 'gist_earth'
# color_style = 'coolwarm'

# Size : number of columns/vector in the picture
n_digit = 150
mp.dps = n_digit + 3  # set number of digits


# export format: pdf, png, svg (bad interpolation though!)
img_format = "svg"
print("Export format is {}".format(img_format))


# Seed" of the picture, default is random
nature = 'sqrt2'
# nature = 'exp'  # 'sqrt2'
nature = 'pi'
nature = 'random'

# Size of the inflate ratio:
inflate = 5
# inflate = 5, means they are 5 spaces between dashes.

# Mirror the row/columns
mirror = False

# Parralel lines (XXX variant not good rigt now)
cartesian = True

# Is movie?
movie = False
plt.close('all')


hito_mat = make_hitomezashi(n_digit=n_digit, nature=nature, inflate=inflate,
                            cartesian=cartesian, seed=seed)


img_directory = plot_hitomezashi(hito_mat, n_digit=n_digit, inflate=inflate,
                                 color_style=color_style, n_qt=n_qt,
                                 mirror=mirror, img_format=img_format,
                                 movie=movie, nature=nature, saving=saving)
