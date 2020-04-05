"""
Annie Perkins Math Art Challenge.
https://twitter.com/anniek_p/status/1244220881347502080
Adapted from https://github.com/hackingmath/pygame_sketches/blob/master/binary_grid_challenge.py
by J. Salmon
Inkscape advice:
https://graphicdesign.stackexchange.com/questions/15450/remove-background-based-on-color-in-inkscape
April 05, 2020
"""

import matplotlib.pylab as plt
import numpy as np
from mpmath import exp, nstr, sqrt, mp, pi

# from tempfile import mkdtemp
from joblib import Memory

# cache memory with joblib
# cachedir = mkdtemp()
memory = Memory(verbose=1)

n_digit = 128
nature = 'exp'  # 'sqrt2'
# nature = 'sqrt2'
# nature = 'pi'

mp.dps = n_digit  # set number of digits
inflate = 5


@memory.cache
def plt_hitomezashi(n_digit=n_digit, nature=nature, inflate=inflate):

    plt.close('all')

    print('Type : {}'.format(nature))

    # Note: the " / 10 " below (and the i+2) is to avoid "." issues
    if nature is "exp":
        offset_row_str = (nstr(exp(1, dps=n_digit) / 10, n=n_digit + 2))
    elif nature is "sqrt2":
        offset_row_str = (nstr(sqrt(2, dps=n_digit) / 10, n=n_digit + 2))
    elif nature is "pi":
        offset_row_str = nstr(pi(dps=n_digit) / 10, n=n_digit + 2)

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

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plt.subplots_adjust(top=0.9)  # border issues somtimes without
    # ax.set_xlim(dim_col + 1, -1)
    # ax.set_ylim(dim_row + 1, -1)
    # ax.autoscale(False)
    hitomezashi_mat_big = np.zeros([dim_row + 5, dim_col + 5])
    hitomezashi_mat_big[5:dim_row + 5, 5:dim_col + 5] = hitomezashi_mat
    ax.imshow(hitomezashi_mat_big, cmap='Greys', interpolation='none',
              origin='upper'
              # , extent=(-5, dim_col + 10, -5, dim_row + 10)
              )
    ax.axis('off')
    plt.show()
    return fig, hitomezashi_mat_big


fig, hitomezashi_mat = plt_hitomezashi(n_digit=n_digit, nature=nature)

print(nature)
fig.savefig('pdf/hitomezashi_{}_{}.pdf'.format(nature, n_digit),
            format="pdf", bbox_inches='tight', transparent=True)
