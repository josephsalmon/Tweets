
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
# points = [cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]

# lines:
# points = [0, 1, 2 + 1j, 4 + 2j, 4 + 4j, 2 + 2j, 1 + 3j, 2j]

minval_x = -4
maxval_x = 4
minval_y = -3
maxval_y = 3
# for i in range(len(points)):
#     minval_x = min(minval_x, points[i].real)
#     maxval_x = max(maxval_x, points[i].real)
#     minval_y = min(minval_y, points[i].real)
#     maxval_y = max(maxval_y, points[i].real)

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


def plot_trajs_points(points, nb_rec=12, ax=sub1, t=0.5, lw=2, closed=True,
                      color=color_blind_list[0]):
    list_traj, end_points = computer_mid_iter(points, nb_rec=nb_rec, t=t,
                                              closed=closed)
    # print(list_traj)
    for i, points in enumerate(list_traj):
        # print(1 - i / len(list_traj))
        plot_traj(points, ax=sub1, closed=closed, alpha=1 - i / len(list_traj),
                  lw=lw, color=color)
    return end_points


def translate_polygone_centers(points):
    new_centers = []
    for i, values in enumerate(points):
        new_centers.append(points[(i) % len(points)] + points[(i + 1) % len(points)])
    return new_centers


nb_rec = 70
t_vals = np.linspace(0, 1, num=96)
saving = True
closed = True
files = ''


# hexagone_points = [cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]


# new_centers = translate_polygone_centers(points)
# new_centers.append(0)

# list_points = []

Triangle_ne1 = np.array([4, 2, 4 + 3j])
Triangle_se1 = Triangle_ne1.real - 1j * Triangle_ne1.imag
Triangle_nw1 = -Triangle_ne1.real + 1j * Triangle_ne1.imag
Triangle_sw1 = -Triangle_ne1.real - 1j * Triangle_ne1.imag


Triangle_ne2 = np.array([4 + 3j, 2 + 3j, 2])
Triangle_se2 = Triangle_ne2.real - 1j * Triangle_ne2.imag
Triangle_nw2 = -Triangle_ne2.real + 1j * Triangle_ne2.imag
Triangle_sw2 = -Triangle_ne2.real - 1j * Triangle_ne2.imag

Trapeze_ne1 = np.array([2, 2 + 3j, 3j, 2j])
Trapeze_se1 = Trapeze_ne1.real - 1j * Trapeze_ne1.imag
Trapeze_nw1 = -Trapeze_ne1.real + 1j * Trapeze_ne1.imag
Trapeze_sw1 = -Trapeze_ne1.real - 1j * Trapeze_ne1.imag

Carre = np.array([2, -2j, -2, 2j])
list_points = [Triangle_ne1, Triangle_se1, Triangle_nw1, Triangle_sw1,
               Triangle_ne2, Triangle_se2, Triangle_nw2, Triangle_sw2,
               Trapeze_ne1, Trapeze_se1, Trapeze_nw1, Trapeze_sw1,
               Carre]
# list_points = [Carre]

for image_nb, t in enumerate(t_vals):
    sns.set_context("poster")
    sns.set_palette("colorblind")
    sns.set_style("white")
    sns.axes_style()
    fig = plt.figure()
    sub1 = fig.add_subplot(111)
    sub1.set_aspect('equal')
    sub1.set_ylim([1.05 * minval_y, 1.05 * maxval_y])
    sub1.set_xlim([1.05 * minval_x, 1.05 * maxval_x])
    sub1.get_yaxis().set_ticks([])
    sub1.get_xaxis().set_ticks([])
    sub1.axis('off')
    for points in list_points:
        print(points)
        # blue:  color_blind_list[0]
        # Frame:
        plot_traj(points, ax=sub1, color='k', lw=1, closed=closed)
        # Midpoints:
        end_points = plot_trajs_points(points, nb_rec=nb_rec, ax=sub1, t=t,
                                       lw=1, closed=closed, color='k')
    plt.show()

    if saving is True:

        plt.savefig("for_nanou/bezier_%s.png" % str(image_nb).zfill(3))
        plt.savefig("for_nanou/bezier_%s.pdf" % str(image_nb).zfill(3))
        plt.savefig("for_nanou/bezier_%s.svg" % str(image_nb).zfill(3))

        files = files + ' for_nanou/bezier_{}.png'.format(str(image_nb).zfill(3))

        print(files)

        plt.close('all')


job = 'convert -layers optimize -delay 6 {} -loop 1 for_nanou/Bezier.gif'.format(files)
os.system(job)
