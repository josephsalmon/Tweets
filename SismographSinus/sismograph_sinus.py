# formula: https://1ucasvb.tumblr.com/post/42906053623/in-a-previous-post-i-showed-how-to-geometrically

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

n_polygons = 4
height = n_polygons * 2
n_discr = 200
n_lap = 2
n_frames = n_discr * n_lap

x = np.linspace(0, n_lap * 2 * np.pi, n_frames)
cosx, sinx = np.cos(x), np.sin(x)


plt.close('all')
fig, ax = plt.subplots(1 + n_polygons, 2, sharey=True, figsize=[height, height],
                       gridspec_kw={'width_ratios': [1, 3]})
plt.subplots_adjust(wspace=0.03, hspace=0.1)

polygones = []
sismographs = []
dot_borders = []
dot_centers = []
lines = []
bars_horiz = []
bars_pendulum = []

display_options = {'lw': 2}
for i in range(n_polygons + 1):
    n_vertex = i + 3
    if i < n_polygons:
        PPnx = 1 / np.cos((2 / n_vertex) * np.arcsin(np.sin((n_vertex / 2) * x)))
    else:
        PPnx = 1
    real_val = PPnx * np.cos(x)
    imag_val = PPnx * np.sin(x)
    ax[i, 0].plot([], [])
    ax[i, 0].set_xlim([-2, 2])
    ax[i, 0].set_ylim([-2, 2])
    ax[i, 0].set_xticks([], [])
    ax[i, 0].set_yticks([], [])
    llin10, = ax[i, 0].plot(real_val, imag_val,
                            color='k',
                            **display_options)
    polygones.append(llin10)

    sismograph, = ax[i, 1].plot([], [], color='k',
                                **display_options)
    ax[i, 1].set_xlim([-0.1, 8])
    ax[i, 1].set_yticks([], [])
    ax[i, 1].set_xticks([], [])
    sismographs.append(sismograph)

    dot_border, = ax[i, 1].plot([], [], 'o', color='k',
                                **display_options)
    dot_center, = ax[i, 0].plot([], [], 'o', color='k',
                                **display_options)

    bar_horiz, = ax[i, 0].plot([], [], '--', color='k', lw=1)
    bar_pendulum, = ax[i, 0].plot([], [], '--', color='k', lw=1)
    bars_horiz.append(bar_horiz)
    bars_pendulum.append(bar_pendulum)

    dot_centers.append(dot_center)
    dot_borders.append(dot_border)


def animate(i):
    for axi in range(n_polygons + 1):
        n_vertex = axi + 3

        if axi < n_polygons:
            PPnx = 1 / np.cos((2 / n_vertex) * np.arcsin(np.sin((n_vertex / 2) * x)))
        else:
            PPnx = 1
        real_val = PPnx * np.cos(x)
        imag_val = PPnx * np.sin(x)

        realz = np.roll(real_val, i)
        imz = np.roll(imag_val, i)

        sismographs[axi].set_data(x, imz)
        dot_centers[axi].set_data(realz[0], imz[0])
        dot_borders[axi].set_data(0, imz[0])
        bars_horiz[axi].set_data([0, realz[0]], [0, imz[0]])
        bars_pendulum[axi].set_data([realz[0], 2], [imz[0], imz[0]])

    return sismographs + dot_borders + dot_centers + bars_pendulum + bars_horiz


anim = animation.FuncAnimation(fig, animate, frames=n_frames,
                               interval=2, blit=True)
anim.save('sismograph_sinus.mp4', fps=100)
plt.show()
