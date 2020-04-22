
"""Created on Thu Oct  12 16:49:12 2019.
# Author: Joseph Salmon <joseph.salmon@umontpellier.fr>
"""

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
import seaborn as sns
from os import mkdir, path, getcwd
import cmath
import matplotlib.lines as lines
import shapely
from shapely.geometry import LineString, Point

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


def plot_traj(points, ax, color=color_blind_list[0],
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


def plot_points(points, ax, color=color_blind_list[0], ms=2, alpha=1):
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


def plot_trajs_points(points, ax, nb_rec=12, t=0.5, lw=2, closed=True):
    list_traj, end_points = computer_mid_iter(points, nb_rec=nb_rec, t=t, closed=closed)
    # print(list_traj)
    for i, points in enumerate(list_traj):
        # print(1 - i / len(list_traj))
        plot_traj(points, ax=ax, closed=closed, alpha=1 - i / len(list_traj), lw=lw)
    return end_points


def translate_polygone_centers(points):
    new_centers = []
    for i, values in enumerate(points):
        new_centers.append(points[(i) % len(points)] + points[(i + 1) % len(points)])
    return new_centers


nb_points = 10
nb_rec = 1
t_vals = np.linspace(0, 1, num=96)
saving = True
closed = True
files = ''

basis_points = [cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]


# polygone
dodecagone = np.array([cmath.exp(1j * 2 * np.pi * i / nb_points) for i in range(nb_points)]) * cmath.exp(1j * np.pi / nb_points)

pentagone1 = np.array([cmath.exp(1j * 2 * np.pi * i / 5) for i in range(nb_points)]) * cmath.exp(1j * np.pi / 10)
pentagone2 = np.array([cmath.exp(1j * 2 * np.pi * i / 5) for i in range(nb_points)]) * cmath.exp(-1j * np.pi / 10)

line_zigzag = dodecagone[3 * np.arange(10) % 10]


A = (0, 1)
B = (pentagone2[0].real, pentagone2[0].imag)

C = (pentagone2[1].real, pentagone2[1].imag)
D = (pentagone2[2].real, pentagone2[2].imag)

line1 = LineString([A, B])
line2 = LineString([C, D])

int_pt = line1.intersection(line2)

seg1 = np.array([int_pt.x + int_pt.y * 1j, int_pt.x - int_pt.y * 1j])
seg2 = np.array([-int_pt.x + int_pt.y * 1j, -int_pt.x - int_pt.y * 1j])

# print(point_of_intersection)


linewidth = 0.8

sns.set_context("poster")
sns.set_palette("colorblind")
sns.set_style("white")
sns.axes_style()
fig = plt.figure()
sub1 = fig.add_subplot(111)
sub1.set_aspect('equal')
sub1.set_ylim([-1.05, 1.05])
sub1.set_xlim([-1.05, 1.05])
sub1.get_yaxis().set_ticks([])
sub1.get_xaxis().set_ticks([])
# plot_traj(dodecagone, ax=sub1, color='k', lw=2,
          # closed=closed)
# plot_traj(pentagone1, ax=sub1, color='k', lw=linewidth,
#           closed=closed)
# plot_traj(pentagone2, ax=sub1, color='k', lw=linewidth,
#           closed=closed)

# plot_traj(seg1, ax=sub1, color='k', lw=linewidth,
#           closed=False)
# plot_traj(seg2, ax=sub1, color='k', lw=linewidth,
#           closed=False)

plot_traj(line_zigzag, ax=sub1, color='k', lw=linewidth,
          closed=closed)
for i in range(10):
    plot_traj(seg1 * cmath.exp(1j * 2 * np.pi * i / 10), ax=sub1, color='k', lw=linewidth,
              closed=False)
    plot_traj(seg2 * cmath.exp(1j * 2 * np.pi * i / 10), ax=sub1, color='k', lw=linewidth,
              closed=False)

sub1.axis('off')
plt.show()


for my_format in ["svg", "pdf", "png"]:
    filename = path.join(getcwd(), my_format, "ten_star" + "." + my_format)
    fig.savefig(filename, bbox_inches=0, transparent=True)
