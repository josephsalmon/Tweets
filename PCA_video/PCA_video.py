"""Created on Thu Oct  2 16:49:12 2014.

Reproduce the pictures for the course "LeastSquare_Def"
REM:
  - you need TeX install on your machine (otherwise errors could appends)

# Author: Joseph Salmon <joseph.salmon@umontpellier.fr>
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from os import mkdir, path
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from math import cos, sin, pi, acos

# Uncomment the following 2 lines for Mac OS X / Spyder for using Tex display
# import os as macosx
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

dirname = "../prebuiltimages/"
if not path.exists(dirname):
    mkdir(dirname)

imageformat = '.pdf'
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
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
# display function:

saving = True

###############################################################################
# PCA interpretation

color_blind_list = sns.color_palette("colorblind", 8)

centers = [(-5, -5), (0, 0), (5, 5)]
centers = [(-5, -5), (5, 5)]
n_samples = 50
n_features = 2
Z, _ = make_blobs(n_samples=n_samples, n_features=n_features, cluster_std=2.7,
                  centers=centers, shuffle=False, random_state=42)

scaler = StandardScaler(with_mean=True, with_std=True).fit(Z)
X = scaler.transform(Z)


# PCA and rotating to align axis:

pca = PCA(n_components=2)
pca.fit(X)
rotation = np.asarray([pca.components_[0][0], pca.components_[0][0]])
# X = np.outer(X.dot(rotation), rotation)
theta_opt = acos(pca.components_[0][0])
X = X @ np.asarray([[cos(-theta_opt - pi / 2), - sin(-theta_opt - pi / 2)],
                    [sin(-theta_opt - pi / 2), cos(-theta_opt - pi / 2)]])
# cos_opt = np.asarray([cos(theta_opt), -cos(theta_opt)])
# sin_opt = np.asarray([sin(theta_opt), -sin(theta_opt)])

rotation_0 = np.asarray([cos(0), sin(0)])
var_opt = np.var(X.dot(rotation_0))

pca.fit(X)


rotation_opt = np.asarray([cos(theta_opt), sin(theta_opt)])


my_orange = color_blind_list[1]

sns.set_context("poster")
sns.set_palette("colorblind")
sns.set_style("white")

s_large = 200
s_small = 50

nb_images = 90

thetas = np.linspace(- pi / 2, pi / 2, num=nb_images)
theta_grid = np.linspace(- pi / 2, pi / 2, num=200)
var_grid = np.zeros(theta_grid.shape)

for image_nb, theta in enumerate(theta_grid):
    rotation = np.asarray([cos(theta), sin(theta)])
    var_grid[image_nb] = np.var(X.dot(rotation))

# sns.axes_style()

files = ''
for image_nb, theta in enumerate(thetas):

    fig = plt.figure(image_nb, figsize=(17, 7))
    with sns.axes_style("white"):
        sub1 = fig.add_subplot(121)
        # sns.set_style("white")

        sub1.set_aspect('equal')
        sub1.set_ylim([-3., 3.])
        sub1.set_xlim([-3., 3.])
        cos_var = np.asarray([cos(theta), -cos(theta)])
        sin_var = np.asarray([sin(theta), -sin(theta)])
        rotation = np.asarray([cos(theta), sin(theta)])
        points_projected = np.outer(X.dot(rotation), rotation)
        for i in range(X.shape[0]):
            point_projected = points_projected[i]
            point_ini = X[i, :]
            sub1.plot([point_ini[0], point_projected[0]],
                      [point_ini[1], point_projected[1]],
                      '--k', linewidth=1, zorder=1)
            sub1.scatter(point_projected[0], point_projected[1],
                         s=s_small, alpha=1, color='k', zorder=2)
            amplitude = 4
            sub1.plot(amplitude * cos_var, amplitude * sin_var, '--k',
                      linewidth=1,
                      zorder=2)
            sub1.plot([-4, 4], [0, 0], color=color_blind_list[0],
                      linewidth=1,
                      zorder=2)
        sub1.scatter(X[:, 0], X[:, 1], s=s_small, alpha=1,
                     color=my_orange, zorder=3,
                     edgecolors='k')
        sub1.scatter(0, 0, s=s_large, alpha=1, color='r', zorder=4,
                     edgecolors='k')
        sub1.get_yaxis().set_ticks([])
        # sub1.get_xaxis().set_ticks([])
        plt.xticks(color='w')
        sub1.set_xlabel(u'Data, center of mass and projected data \n (principal axis in blue)')
        var = np.var(X.dot(rotation))

    with sns.axes_style({'xtick.bottom': True, 'axes.spines.bottom': True,
                         'axes.spines.left': True, 'axes.spines.right': False,
                         'axes.spines.top': False}):
        sub2 = fig.add_subplot(122)

    sub2.plot(theta_grid, var_grid, color='k', linewidth=3, zorder=1)
    sub2.tick_params(length=5, pad=10)
    sub2.set_xticks([-np.pi / 2, 0, np.pi / 2])
    sub2.set_xticklabels([u'$-\\frac{\\pi}{2}$', u'$0$', u'$\\frac{\\pi}{2}$'])

    sub2.set_ylim([0.01, 2.2])
    sub2.set_xlim([- pi / 2 - 0.2, pi / 2 + 0.2])
    sub2.scatter(0, var_opt, color=color_blind_list[0], s=s_large, zorder=2, edgecolors='k')
    sub2.scatter(theta, var, color=my_orange, s=s_large, zorder=2, edgecolors='k')
    # print(var)
    # print(var_opt)
    sub2.set_xlabel('Angle with respect to principal axis')
    sub2.set_ylabel('Variance of projected data')
    sub2.get_yaxis().set_ticks([])
    plt.tight_layout()
    plt.show()
    filename = 'fig_pca_axis' + str(image_nb)

    if saving is True:

        plt.savefig("gifs/PCA_%s.png" % str(image_nb).zfill(3))
        files = files + ' gifs/PCA_{}.png'.format(str(image_nb).zfill(3))

        print(files)
        # command = 'convert -delay 5 {} -loop 100 gifs/gauss_pivot.gif'.format(' '.join(files))
        plt.close('all')

job = 'convert -layers optimize -resize 1000 -delay 6 {} -loop 3 gifs/PCA.gif'.format(files)
os.system(job)