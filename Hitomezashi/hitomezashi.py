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
from mpmath import exp, nstr, sqrt, pi
from skimage import measure


def make_hitomezashi(n_digit=150, nature="cartesian", inflate=5,
                     cartesian=True, seed=123456):
    """Main function to create a hitomezashi matrix."""
    r = np.random.RandomState(seed)
    print('Type : {}'.format(nature))
    # Note: the " / 10 " below (and the i+2) is to avoid "." issues
    if nature is "101010":
        a = np.zeros(n_digit + 3, dtype=int)
        a[::2] = 1
        offset_row_str_int = np.array2string(a,
                                             max_line_width=n_digit + 10,
                                             separator='')
    elif nature is "exp":
        offset_row_str_int = (nstr(exp(1) / 10, n=n_digit + 3))
    elif nature is "sqrt2":
        offset_row_str_int = (nstr(sqrt(2) / 10, n=n_digit + 3))
    elif nature is "pi":
        offset_row_str_int = nstr(pi / 10, n=n_digit + 3)
    elif nature is "random":
        offset_row_str_int = np.array2string(r.randint(low=0, high=9,
                                             size=n_digit + 3),
                                             max_line_width=n_digit + 10,
                                             separator='')
    print(offset_row_str_int)
    offset_row_str_int = offset_row_str_int[1:-1]
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
    if cartesian:
        inflate_row[0, :] = 1
    else:
        for i in range(inflate):
            inflate_row[i, i] = 1

    bin_matrix_kr = np.ones([inflate * n_digit + 1, inflate * n_digit + 1])
    bin_matrix_kr[:-1, : -1] = np.kron(bin_matrix, inflate_row)  # border excl.
    bin_matrix_kr = np.clip(bin_matrix_kr + bin_matrix_kr.T, 0, 1)

    # Corner / padding issues
    bin_matrix_patch = 1 - bin_matrix  # missing dots top left
    inflate_row_patch = np.zeros([inflate, inflate])
    if cartesian:
        inflate_row_patch[0, 0] = 1
    else:
        for i in range(inflate - 2):
            inflate_row_patch[i, inflate - i - 1] = 1
    bin_matrix_kr_patch = np.ones([inflate * n_digit + 1,
                                   inflate * n_digit + 1])
    bin_matrix_kr_patch[:-1, : -1] = np.kron(bin_matrix_patch,
                                             inflate_row_patch)

    bin_matrix_kr_patch = np.clip(bin_matrix_kr_patch + bin_matrix_kr_patch.T,
                                  0, 1)
    hito_mat = np.clip(bin_matrix_kr + bin_matrix_kr_patch, 0, 1)
    hito_mat[0, :] = 1
    hito_mat[:, 0] = 1
    hito_mat[n_digit * inflate, :] = 1
    hito_mat[:, n_digit * inflate] = 1

    return hito_mat

#adapted from :
# https://scipy-cookbook.readthedocs.io/items/Matplotlib_ColormapTransformations.html


def cmap_discretize(cmap, N, shift=15):
    """Return a discrete colormap from the continuous colormap cmap.
        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.
    """
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(np.roll(colors_i, shift))
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki],
                      colors_rgba[i, ki]) for i in range(N + 1)]
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)


def plot_hitomezashi(hito_mat, n_digit=150, inflate=5, color_style='RdBu',
                     n_qt=30, mirror=True, img_format="png", movie=True,
                     nature="cartesian", saving=False, shift=15):
    # Black an white part
    if color_style is 'nb':
        cmap = plt.get_cmap('Greys')
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.imshow(hito_mat, cmap=cmap, interpolation='none',
                  aspect='equal')
        ax.set_axis_off()
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
        plt.show()

    # Color part
    elif color_style is not'color' and n_qt > 2:
        cmap = plt.get_cmap(color_style)
        cmap = cmap_discretize(cmap, shift)
        # symmetry along the diagonal
        hito_lbls_raw = measure.label(hito_mat, neighbors=4,
                                      background=1)
        hito_lbls_init = np.triu(hito_lbls_raw, k=1).T.copy() \
            + (np.triu(hito_lbls_raw)).copy()
        # get connected components labels and frequency
        unique_elem, counts_elem = np.unique(hito_lbls_init,
                                             return_counts=True)

        # Identify (smalle) unit squares to plot them white
        small_squares_labels = unique_elem[counts_elem <= (inflate - 1)**2]
        small_squares_labels_dble = unique_elem[counts_elem == 2 * (inflate - 1)**2]

        # Handle quantization
        hito_lbls = np.zeros(hito_lbls_init.shape)
        if n_qt > 1:
            hito_lbls = (hito_lbls_init % n_qt) + 1
        else:
            hito_lbls = hito_lbls_init

        # Black pixels
        black_mask = hito_mat > 0.5
        hito_lbls[black_mask] = -1
        cmap.set_bad(color='k')

        # White pixels
        for val in small_squares_labels:
            hito_lbls[hito_lbls_init == val] = -2
        for val in small_squares_labels_dble:
            hito_lbls[hito_lbls_init == val] = -2
        cmap.set_under(color='w')

        if mirror:
            new_labels = np.concatenate((np.concatenate((hito_lbls[:-1, :-1],
                                         hito_lbls[:-1, -3::-1]), axis=1),
                                         np.concatenate((hito_lbls[-3::-1, :-1],
                                                         hito_lbls[-3::-1, -3::-1]),
                                         axis=1)), axis=0)
            masked_array = np.ma.masked_where(new_labels == -1,
                                              new_labels)
        else:
            masked_array = np.ma.masked_where(hito_lbls == -1,
                                              hito_lbls)
        normalize = matplotlib.colors.Normalize(vmin=1,
                                                vmax=np.max(hito_lbls[:]))

        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        plt.imshow(masked_array, cmap=cmap, vmin=1, norm=normalize,
                   interpolation='none', aspect='equal')
        ax.set_axis_off()
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
        plt.show()
    else:
        # Black pixels
        black_mask = hito_mat > 0.5
        hito_lbls_raw = measure.label(hito_mat, neighbors=4,
                                      background=1)
        n1, n2 = np.shape(hito_mat)
        bin_matt = np.full([n1, n2], -1)
        diff_hito_v = np.zeros_like(hito_mat)
        diff_hito_v[:, 1:] = np.diff(hito_mat, axis=1)
        diff_hito_h = np.zeros_like(hito_mat)
        diff_hito_h[1:, :] = np.diff(hito_mat, axis=0)
        last_value = 0
        # Iinit border north and wesst.
        for j in range(n2):
                if (diff_hito_v[1, j] == -1):
                    last_value = 1 - last_value
                    bin_matt[hito_lbls_raw == hito_lbls_raw[1, j]] = last_value
        last_value = 0
        for i in range(n1):
                if (diff_hito_h[i, 1] == -1):
                    last_value = 1 - last_value
                    bin_matt[hito_lbls_raw == hito_lbls_raw[i, 1]] = last_value

        for j in range(2, n2, 1):
            print(j / n2)
            if bin_matt[1, j] < 0:
                current_col = bin_matt[1, j - 1]
                current_class = hito_lbls_raw[1, j - 1]
            else:
                current_col = bin_matt[1, j]
                current_class = hito_lbls_raw[1, j]
            for i in range(2, n1, 1):
                if (hito_lbls_raw[i, j] > 0):
                    bin_matt[hito_lbls_raw == hito_lbls_raw[i, j]] = current_col
                    if current_class != hito_lbls_raw[i, j]:
                        current_class = hito_lbls_raw[i, j]
                        current_col = 1 - current_col
        bin_matt[black_mask] = -1
        cmap.set_bad(color='k')

        masked_array = np.ma.masked_where(bin_matt == -1,
                                          bin_matt)
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.imshow(masked_array, cmap=cmap, interpolation='none', aspect='equal')
        ax.set_axis_off()
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
        plt.show()

    """Saving part."""
    if movie:
        img_format_directory = os.path.join(os.getcwd(), img_format + "_movie")
    else:
        img_format_directory = os.path.join(os.getcwd(), img_format)
    if not os.path.isdir(img_format_directory):
        os.mkdir(img_format_directory)
    img_directory = os.path.join(img_format_directory, color_style)
    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    if mirror:
        part_name = 'hitomezashi_mirror_'
    else:
        part_name = 'hitomezashi_'
    if color_style is None:
        filename = part_name + '{}_{}.{}'.format(nature, n_digit,
                                                 img_format)
    else:
        filename = part_name + 'cmap_{}_{}_nq{}.{}'.format(nature,
                                                           n_digit,
                                                           str(shift).zfill(3),
                                                           img_format)
    fig.savefig(os.path.join(img_directory, filename),
                pad_inches=0, format=img_format,
                bbox_inches=None, transparent=True)
    return img_directory, filename
