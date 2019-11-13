import itertools
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call


save = True


def berhu(x, L=0.4):
    """BerHu function following Owen terminology."""
    x = np.atleast_1d(x)
    # L = 15  # init for the vides on Fenchel.ipynb
    # L = 3   # init for the videos in Smoothing.ipynb
    z = np.abs(x)
    if isinstance(x, np.ndarray):
        j = np.abs(x) > L
        z[j] = (x[j] ** 2 + L ** 2) / (2 * L)
    else:
        if np.abs(x) > L:
            z = (x ** 2 + L ** 2) / (2 * L)
    return L * z

plt.rcParams['text.usetex'] = True
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

x = np.arange(-1., 1.1, 0.1)
X, Y = np.meshgrid(x, x)
Z = np.abs(X) + np.abs(Y)

plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')


x = np.linspace(0.04, 1, endpoint=True, num=5)

# # for val, style in zip([1, x], ['-', '--']):
# for val, style in zip([1], ['-']):
#     ax.plot(np.zeros_like(x), x, val, color='k', linestyle=style)
#     ax.plot(np.zeros_like(x), -x, val, color='k', linestyle=style)
#     ax.plot(x, np.zeros_like(x), val, color='k', linestyle=style)
#     ax.plot(- x, np.zeros_like(x), val, color='k', linestyle=style)

# x = np.linspace(0.01, 1, endpoint=True, num=5)

# for x1, x2 in itertools.product([x, -x], [x, -x]):
#     X, Y = np.meshgrid(x1, x2)
#     ax.plot_surface(X, Y, 2 * np.ones_like(X), color='k',
#                     linewidth=0, rstride=10, cstride=10)

# ax.scatter(0, 0, 0, color='k')


ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_zticks([0, 1])

ax.set_zlim(0, 1.2)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

x = np.arange(-1., 1.1, 0.05)

X, Y = np.meshgrid(x, x)


Z = berhu(X) + berhu(Y)
ax.plot_surface(X, Y, Z, color='k', alpha=0.2, cstride=10, rstride=10)
ax.plot(np.zeros_like(x), x, berhu(x), color='k', linestyle='-', linewidth=0.6)
ax.plot(x, np.zeros_like(x), berhu(x), color='k', linestyle='-', linewidth=0.6)


plt.show(block=False)
nb_angles = 360

for angle in range(0, nb_angles):
    ax.view_init(10, angle)
    plt.draw()
    plt.pause(.005)
    # plt.savefig("gifs/burhu_rotation%s.png" % str(angle).zfill(3))
    # or:
    plt.savefig("gifs/berhu_rotation_%s.png" % str(angle))

if save is True:

    files = []
    for i in range(0, nb_angles):
        files.append('gifs/berhu_rotation_{}.png'.format(i))
    # print(files)
    command = 'convert -delay 5 {} -loop 100 gifs/berhu_rotation.gif'.format(' '.join(files))
    call(command, shell=True)

# then in bash:
# convert -delay 5 -loop 100 burhu_rotation* burhu_rotation.gif

# convert -delay 5 $(for i in $(seq 0 5 100); do echo burhu_rotation${i}.png; done) -loop 100 burhu_rotation.gif