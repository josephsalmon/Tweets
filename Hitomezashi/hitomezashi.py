"""
Annie Perkins Math Art Challenge.
https://twitter.com/anniek_p/status/1244220881347502080
Adapted from https://github.com/hackingmath/pygame_sketches/blob/master/binary_grid_challenge.py
by J. Salmon
Inkscape advice:
https://graphicdesign.stackexchange.com/questions/15450/remove-background-based-on-color-in-inkscape
April 05, 2020
"""

import os
import matplotlib
import matplotlib.pylab as plt
import numpy as np
from mpmath import exp, nstr, sqrt, mp, pi, rand
from skimage import measure

# Color Style
color_style = 'nb'
color_style = 'coolwarm'
# color_style = 'viridis'
# color_style ='RdBu'
# color_style ='Blues'
if color_style is 'nb':
    cmap = plt.get_cmap('Greys')
else:    # cmap = matplotlib.cm.twilight_shifted
    cmap = plt.get_cmap(color_style)


# Size : number of columns/vector in the picture
n_digit = 100
mp.dps = n_digit + 3  # set number of digits


# export format: pdf, png, svg (bad interpolation though!)
img_format = "png"
print("Export format is {}".format(img_format))


# Seed" of the picture, default is random
nature = 'sqrt2'
# nature = 'exp'  # 'sqrt2'
# nature = 'pi'
# nature = 'random'

# Size of the inflate ratio:
inflate = 5
# inflate = 5, means they are 5 spaces between dashes.

# Saving activated:
saving = False

plt.close('all')


def make_hitomezashi(n_digit=n_digit, nature=nature, inflate=inflate):
    """Main function to create a hitomezashi matrix."""
    print('Type : {}'.format(nature))
    # Note: the " / 10 " below (and the i+2) is to avoid "." issues
    if nature is "exp":
        offset_row_str_int = (nstr(exp(1) / 10, n=n_digit + 3))
    elif nature is "sqrt2":
        offset_row_str_int = (nstr(sqrt(2) / 10, n=n_digit + 3))
    elif nature is "pi":
        offset_row_str_int = nstr(pi / 10, n=n_digit + 3)
    elif nature is "random":
        offset_row_str_int = nstr(rand(), n=n_digit + 3)
    offset_row_str = offset_row_str_int[2:]
    print("Seed={}".format(offset_row_str))
    bin_matrix = np.zeros([n_digit, n_digit])

    odd_row_pattern = np.zeros(n_digit,)
    odd_row_pattern[::2] = 1
    even_row_pattern = np.zeros(n_digit,)
    even_row_pattern[1::2] = 1

    for i in range(n_digit):
        if int(offset_row_str[i]) % 2 is 1:
            bin_matrix[i, :] = odd_row_pattern
        else:
            bin_matrix[i, :] = even_row_pattern

    inflate_row = np.zeros([inflate, inflate])
    inflate_row[0, :] = 1

    bin_matrix_kr = np.kron(bin_matrix, inflate_row)
    bin_matrix_kr = np.clip(bin_matrix_kr + bin_matrix_kr.T, 0, 1)

    bin_matrix_patch = 1 - bin_matrix  # missing dots top left
    inflate_row_patch = np.zeros([inflate, inflate])
    inflate_row_patch[0, 0] = 1
    bin_matrix_kr_patch = np.kron(bin_matrix_patch, inflate_row_patch)
    bin_matrix_kr_patch = np.clip(bin_matrix_kr_patch + bin_matrix_kr_patch.T,
                                  0, 1)
    hitomezashi_mat = np.clip(bin_matrix_kr + bin_matrix_kr_patch, 0, 1)
    hitomezashi_mat[0, :] = 1
    hitomezashi_mat[:, 0] = 1
    hitomezashi_mat[n_digit * inflate - 1, :] = 1
    hitomezashi_mat[:, n_digit * inflate - 1] = 1

    return hitomezashi_mat


hitomezashi_mat = make_hitomezashi(n_digit=n_digit, nature=nature)


if color_style is 'nb':
    # Black an white part
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.imshow(hitomezashi_mat, cmap=cmap, interpolation='none',
              aspect='equal')
    ax.set_axis_off()
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    plt.show()


else:
    # Color part
    black_mask = hitomezashi_mat > 0.5
    hitomezashi_labels_raw = measure.label(hitomezashi_mat, neighbors=4,
                                           background=1)
    hitomezashi_labels = np.triu(hitomezashi_labels_raw, k=1).T.copy() \
        + (np.triu(hitomezashi_labels_raw)).copy()

    unique_elem, counts_elem = np.unique(hitomezashi_labels, return_counts=True)
    hitomezashi_labels[black_mask] = -1

    # simples squares in white?
    small_squares_labels = unique_elem[counts_elem == (inflate - 1)**2]
    small_squares_labels_dble = unique_elem[counts_elem == 2 * (inflate - 1)**2]
    for val in small_squares_labels:
        hitomezashi_labels[hitomezashi_labels == val] = -2
    for val in small_squares_labels_dble:
        hitomezashi_labels[hitomezashi_labels == val] = -2
    cmap.set_under(color='w')
    cmap.set_bad(color='k')
    masked_array = np.ma.masked_where(hitomezashi_labels == -1,
                                      hitomezashi_labels)

    normalize = matplotlib.colors.Normalize(vmin=1, vmax=np.max(unique_elem))

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    plt.imshow(masked_array, cmap=cmap, vmin=1, norm=normalize,
               interpolation='none', aspect='equal')
    ax.set_axis_off()
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    plt.show()


def saving_hitomezashi(fig, nature=nature, n_digit=n_digit,
                       img_format=img_format, saving=saving,
                       color_style=color_style):
    """Saving part."""
    if saving:
        img_directory = os.path.join(os.getcwd(), img_format)
        if not os.path.isdir(img_directory):
            os.mkdir(img_directory)
        if color_style is None:
            filename = 'hitomezashi_{}_{}.{}'.format(nature, n_digit, img_format)
        else:

            filename = 'hitomezashi_color_{}_{}_{}.{}'.format(color_style,
                                                              nature,
                                                              n_digit,
                                                              img_format)

        fig.savefig(os.path.join(os.getcwd(), img_format, filename),
                    pad_inches=0, format=img_format,
                    bbox_inches=None, transparent=True)


saving_hitomezashi(fig, nature=nature, n_digit=n_digit,
                   img_format=img_format, saving=saving,
                   color_style=color_style)
