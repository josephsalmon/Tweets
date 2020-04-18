
"""Created on Thu Oct  12 16:49:12 2019.
# Author: Joseph Salmon <joseph.salmon@umontpellier.fr>
"""

import os
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
import seaborn as sns
from os import mkdir, path
import cmath
import matplotlib.lines as lines

# Uncomment the following 2 lines for Mac OS X / Spyder for using Tex display
# import os as macosx
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

dirname = "../prebuiltimages/"
if not path.exists(dirname):
    mkdir(dirname)

imageformat = '.pdf'
# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 16,
          'font.size': 23,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True
          }
plt.rcParams.update(params)
plt.close("all")


###############################################################################
# PCA interpretation

color_blind_list = sns.color_palette("colorblind", 8)


nb_points = 6

# Hexagone
points = [cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]

# lines:
# points = [0, 1, 2 + 1j, 4 + 2j, 4 + 4j, 2 + 2j, 1 + 3j, 2j]

minval_x = np.infty
maxval_x = - np.infty
minval_y = np.infty
maxval_y = - np.infty
for i in range(len(points)):
    minval_x = min(minval_x, points[i].real)
    maxval_x = max(maxval_x, points[i].real)
    minval_y = min(minval_y, points[i].real)
    maxval_y = max(maxval_y, points[i].real)

deltax = 4 * (maxval_x - minval_x)
deltay = 4 * (maxval_y - minval_y)

# print(minval_x)
# print(maxval_x)
# print(minval_y)
# print(maxval_y)

sns.set_context("poster")
sns.set_palette("colorblind")
sns.set_style("white")
sns.axes_style()
fig = plt.figure()
sub1 = fig.add_subplot(111)
sub1.set_aspect('equal')
sub1.set_ylim([1.2 * minval_x - deltax / 5, 1.2 * maxval_x + deltax / 5])
sub1.set_xlim([1.2 * minval_y - deltay / 5, 1.2 * maxval_y + deltay / 5])
sub1.get_yaxis().set_ticks([])
sub1.get_xaxis().set_ticks([])
sub1.axis('off')


def compute_midpoints(points, t=0.5, closed=True):
    """Compute mid points in complex."""
    midpoints = []
    max_num = len(points)
    for i in range(max_num):
        midpoints.append(points[i % len(points)] * t + points[(i + 1) % len(points)] * (1 - t))
    return midpoints


def computer_mid_iter(points, nb_rec=12, t=0.5, closed=True):
    """Return iterative lists of midpoints.
    Parameters
    ----------
    points: list,
        list of points with complex format
    t : float, optional
        proportion of line done.
    Returns
    -------
    list_traj : list, (same length as points)
        Returns the list of list of points
    """
    newpoints = points.copy()
    list_traj = []
    for i in range(nb_rec):
        newpoints = compute_midpoints(newpoints, t, closed=closed)
        list_traj.append(newpoints)
    # print(newpoints)
    end_points = newpoints[-1]
    return list_traj, end_points


# print(computer_mid_iter(points))
# def cplx2pt(points):
#     pt_float = []
#     for in points:
#         pt_float.append()
#     return

# for i in range(nb_points):
#     midpoints


def plot_traj(points, ax=sub1, color=color_blind_list[0],
              lw=2, closed=True, alpha=1):
    """Plots line between points.

    Parameters
    ----------
    points: list,
        list of points with complex format
    Returns
    -------
       none, modify ax.
    """
    if closed:
        max_num = len(points)
    else:
        max_num = len(points) - 1
    for i, idx in enumerate(points[:max_num]):
        # print(points[i])
        x1, y1 = points[i].real, points[i].imag
        x2, y2 = points[(i + 1) % len(points)].real, points[(i + 1) % len(points)].imag
        l = lines.Line2D([x1, x2], [y1, y2], color=color,
                         linewidth=lw, alpha=alpha)
        ax.add_line(l)


def plot_points(points, ax=sub1, color=color_blind_list[0], ms=2, alpha=1):
    """Return iterative lists of midpoints.

    Parameters
    ----------
    points: list,
        list of points with complex format
    Returns
    -------
       none, modify ax.
    """
    for i, idx in enumerate(points):
        # print(points[i])
        x1, y1 = points[i].real, points[i].imag
        ax.plot(x1, y1, 'o', color=color, ms=ms, alpha=alpha)

# plot_traj(points, ax=sub1)
# plot_points(points, ax=sub1, color=color_blind_list[0], ms=10)


plt.show()
# print(computer_mid_iter(points, t=0.5))


def plot_trajs_points(points, nb_rec=12, ax=sub1, t=0.5, lw=2, closed=True):
    list_traj, end_points = computer_mid_iter(points, nb_rec=nb_rec, t=t, closed=closed)
    # print(list_traj)
    for i, points in enumerate(list_traj):
        # print(1 - i / len(list_traj))
        plot_traj(points, ax=sub1, closed=closed, alpha=1 - i / len(list_traj), lw=lw)
    return end_points


def translate_polygone_centers(points):
    new_centers = []
    for i, values in enumerate(points):
        new_centers.append(points[(i) % len(points)] + points[(i + 1) % len(points)])
    return new_centers


nb_rec = 24
t_vals = np.linspace(0, 1, num=96)
saving = True
closed = True
files = ''



basis_points = [cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]
new_centers = translate_polygone_centers(points)
new_centers.append(0)


for image_nb, t in enumerate(t_vals):
    sns.set_context("poster")
    sns.set_palette("colorblind")
    sns.set_style("white")
    sns.axes_style()
    fig = plt.figure()
    sub1 = fig.add_subplot(111)
    sub1.set_aspect('equal')
    sub1.set_ylim([1.2 * minval_x - deltax / 5, 1.2 * maxval_x + deltax / 5])
    sub1.set_xlim([1.2 * minval_y - deltay / 5, 1.2 * maxval_y + deltay / 5])
    sub1.get_yaxis().set_ticks([])
    sub1.get_xaxis().set_ticks([])
    sub1.axis('off')
    for i, values in enumerate(new_centers):
        points = [basis_points[j] + values for j in range(nb_points)]
        print(points)
        list_red_traj = []

        plot_traj(points, ax=sub1, color=color_blind_list[0], lw=2, closed=closed)
        end_points = plot_trajs_points(points, nb_rec=nb_rec, ax=sub1, t=t, lw=1, closed=closed)
        # print(end_points)
        # list_red_traj.append(end_points)
        # plot original points + original lines
        # plot_points(points, ax=sub1, color=color_blind_list[0], ms=2)
        # print(end_points)
        # plot_points([end_points], ax=sub1, color=color_blind_list[1], ms=3)
        # plot_traj(list_red_traj, ax=sub1, color=color_blind_list[1], lw=3, closed=False)
    plt.show()
    filename = 'fig_bezier' + str(image_nb)

    if saving is True:

        plt.savefig("gifs/bezier_%s.png" % str(image_nb).zfill(3))
        files = files + ' gifs/bezier_{}.png'.format(str(image_nb).zfill(3))

        print(files)

        command = 'convert -delay 5 {} -loop 100 gifs/Bezier.gif'.format(' '.join(files))
        plt.close('all')


job = 'convert -layers optimize -resize 1000 -delay 6 {} -loop 3 gifs/Bezier.gif'.format(files)
os.system(job)
