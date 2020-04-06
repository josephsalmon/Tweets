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
import matplotlib.pylab as plt
import numpy as np
from mpmath import exp, nstr, sqrt, mp, pi, rand


# Size : number of columns/vector in the picture
n_digit = 50
mp.dps = n_digit  # set number of digits

# export format: pdf, png, svg (bad interpolation though!)
img_format = "png"
print("Export format is {}".format(img_format))

# nature: the "seed" of the picture, default is random
# nature = 'exp'  # 'sqrt2'
# nature = 'sqrt2'
# nature = 'pi'
nature = 'random'

# Size of the inflate ratio:
# inflate = 5, means they are 5 spaces between dashes.
inflate = 5

# Saving activated:
saving = True


def plt_hitomezashi(n_digit=n_digit, nature=nature, inflate=inflate):
    """Main function to plot the hitomezashi."""
    plt.close('all')

    print('Type : {}'.format(nature))

    # Note: the " / 10 " below (and the i+2) is to avoid "." issues
    if nature is "exp":
        offset_row_str = (nstr(exp(1, dps=n_digit) / 10, n=n_digit + 2))
    elif nature is "sqrt2":
        offset_row_str = (nstr(sqrt(2, dps=n_digit) / 10, n=n_digit + 2))
    elif nature is "pi":
        offset_row_str = nstr(pi(dps=n_digit) / 10, n=n_digit + 2)
    elif nature is "random":
        offset_row_str = nstr(rand(), n=n_digit + 2)
    print(offset_row_str)
    bin_matrix = np.zeros([n_digit, n_digit])

    odd_row_pattern = np.zeros(n_digit,)
    odd_row_pattern[::2] = 1
    even_row_pattern = np.zeros(n_digit,)
    even_row_pattern[1::2] = 1

    for i in range(n_digit):
        if int(offset_row_str[i + 2]) % 2 is 1:
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

    # Border issue in pdf export (???)
    dim_row = hitomezashi_mat.shape[0]
    dim_col = hitomezashi_mat.shape[1]

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    hitomezashi_mat_big = np.zeros([dim_row + 10, dim_col + 10])
    hitomezashi_mat_big[5:dim_row + 5, 5:dim_col + 5] = hitomezashi_mat
    ax.imshow(hitomezashi_mat_big, cmap='Greys', interpolation='none', aspect='equal')
    ax.set_axis_off()
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    # plt.tight_layout()
    plt.show()
    return fig, hitomezashi_mat_big


fig, hitomezashi_mat = plt_hitomezashi(n_digit=n_digit, nature=nature)

print(nature)

if saving:
    img_directory = os.path.join(os.getcwd(), img_format)
    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    filename = 'hitomezashi_{}_{}.{}'.format(nature, n_digit, img_format)
    fig.savefig(os.path.join(os.getcwd(), img_format, filename), pad_inches=0,
                format=img_format, bbox_inches=None, transparent=True)
