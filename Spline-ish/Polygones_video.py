
"""Created on Thu Oct  12 16:49:12 2019.
# Author: Joseph Salmon <joseph.salmon@umontpellier.fr>
"""

import os
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
import seaborn as sns
from os import mkdir, path
import matplotlib.lines as lines

###############################################################################
# Plot initialization

dirname = "../prebuiltimages/"
if not path.exists(dirname):
    mkdir(dirname)

imageformat = '.pdf'
params = {'axes.labelsize': 16,
          'font.size': 23,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True
          }
plt.rcParams.update(params)
plt.close("all")

color_blind_list = sns.color_palette("colorblind", 8)


def compute_midpoints(points, t=0.5, closed=True):
    """Compute mid points in complex."""
    midpoints = []
    max_num = len(points)
    for i in range(max_num):
        midpoints.append(points[i % len(points)] * t +
                         points[(i + 1) % len(points)] * (1 - t))
    return midpoints


def computer_mid_iter(points, recursive_level=12, t=0.5, closed=True):
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
    for i in range(recursive_level):
        newpoints = compute_midpoints(newpoints, t, closed=closed)
        list_traj.append(newpoints)
    end_points = newpoints[-1]
    return list_traj, end_points


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


plt.show()
# print(computer_mid_iter(points, t=0.5))


def plot_trajs_points(points, ax, recursive_level=12, t=0.5, lw=2, alpha=True,
                      closed=True,
                      color=color_blind_list[0]):
    list_traj, end_points = computer_mid_iter(points,
                                              recursive_level=recursive_level,
                                              t=t, closed=closed)
    for i, points in enumerate(list_traj):
        if alpha:
            plot_traj(points, ax, closed=closed, alpha=1 - i / len(list_traj),
                      lw=lw, color=color)
        else:
            plot_traj(points, ax, closed=closed, alpha=1,
                      lw=lw, color=color)
    return end_points

t = 0.08
recursive_level = 55
recursive_levels = np.arange(1, recursive_level)
# t_vals = np.linspace(0, 1, num=96)

saving = True
closed = True
files = ''

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

minval_x = -4
maxval_x = 4
minval_y = -3
maxval_y = 3

alpha = False

# for image_nb, t in enumerate(t_vals):
for image_nb, recursive_level in enumerate(recursive_levels):

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
        plot_traj(points, sub1, color='k', lw=1, closed=closed)
        # Midpoints:
        end_points = plot_trajs_points(points, sub1, recursive_level=recursive_level,
                                       t=t, alpha=alpha,
                                       lw=1, closed=closed, color='k')
    plt.show()

    if saving is True:
        if alpha:
            plt.savefig("for_nanou/prog_spline_no_alpha%s.png" % str(image_nb).zfill(3))
            plt.savefig("for_nanou/prog_spline_no_alpha%s.pdf" % str(image_nb).zfill(3))
            plt.savefig("for_nanou/prog_spline_no_alpha%s.svg" % str(image_nb).zfill(3))

            files = files + ' for_nanou/prog_spline_no_alpha{}.png'.format(str(image_nb).zfill(3))
        else:
            plt.savefig("for_nanou/prog_spline_alpha%s.png" % str(image_nb).zfill(3))
            plt.savefig("for_nanou/prog_spline_alpha%s.pdf" % str(image_nb).zfill(3))
            plt.savefig("for_nanou/prog_spline_alpha%s.svg" % str(image_nb).zfill(3))
            files = files + ' for_nanou/prog_spline_alpha{}.png'.format(str(image_nb).zfill(3))

    print(files)

    plt.close('all')

if alpha:
    job = 'convert -layers optimize -delay 6 {} -coalesce -duplicate 1,-2-1 for_nanou/prog_spline_no_alpha.gif'.format(files)
else:
    job = 'convert -layers optimize -delay 6 {} -coalesce -duplicate 1,-2-1 for_nanou/prog_spline_alpha.gif'.format(files)

os.system(job)
